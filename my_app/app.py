from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import gradio as gr
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime, timezone


load_dotenv(override=True)

def push(text):
    token = os.getenv("PUSHOVER_TOKEN")
    user = os.getenv("PUSHOVER_USER")
    if not token or not user:
        return
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": token,
                "user": user,
                "message": text,
            },
            timeout=10,
        )
    except Exception as e:
        print(f"Pushover notification failed: {e}", flush=True)


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    try:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        log = {
            "question": question,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(data_dir / "unknown_questions.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")
    except Exception as e:
        print(f"Failed to log unknown question: {e}", flush=True)
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


class Me:

    def __init__(self):
        # Verify API key is available
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set. Please add it to your .env file.")
        
        self.openai = OpenAI()
        self.name = "Giovanni Lunetta"
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-4o-mini")
        self.eval_model = os.getenv("EVAL_MODEL", "gpt-4o-mini")
        self.gemini_evaluator_model = os.getenv("GEMINI_EVALUATOR_MODEL", "gemini-3.1-flash-lite-preview")
        fallback_models_env = os.getenv(
            "GEMINI_EVALUATOR_FALLBACK_MODELS",
            "gemini-3.1-flash-lite,gemini-3.1-lite,gemini-2.5-flash-lite"
        )
        self.gemini_fallback_models = [m.strip() for m in fallback_models_env.split(",") if m.strip()]
        
        # Load LinkedIn profile
        with open("me/linkedin.txt", "r", encoding="utf-8") as f:
            self.linkedin = f.read()
        
        # Load Resume
        try:
            with open("me/resume.txt", "r", encoding="utf-8") as f:
                self.resume = f.read()
        except FileNotFoundError:
            print("Warning: resume.txt not found in me/ directory. Continuing without resume.")
            self.resume = ""
        
        # Load personal context
        try:
            with open("me/personal_context.txt", "r", encoding="utf-8") as f:
                self.personal_context = f.read()
        except FileNotFoundError:
            print("Warning: personal_context.txt not found in me/ directory. Continuing without personal context.")
            self.personal_context = ""
        
        # Load summary
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        
        # Initialize Gemini for evaluation (optional - falls back to OpenAI if not available)
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if google_api_key:
            try:
                self.gemini = OpenAI(
                    api_key=google_api_key,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                self.gemini_evaluator_model = self.resolve_gemini_model(
                    google_api_key,
                    self.gemini_evaluator_model,
                    self.gemini_fallback_models,
                )
                self.use_gemini_evaluator = True
            except Exception:
                self.use_gemini_evaluator = False
        else:
            self.use_gemini_evaluator = False

    def resolve_gemini_model(self, api_key, preferred_model, fallback_models):
        """Pick the best available Gemini evaluator model at runtime."""
        preferred_order = [preferred_model] + [m for m in fallback_models if m != preferred_model]
        try:
            response = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": api_key},
                timeout=15,
            )
            response.raise_for_status()
            models = response.json().get("models", [])
            available = set()
            for model in models:
                methods = model.get("supportedGenerationMethods", [])
                if "generateContent" not in methods:
                    continue
                name = model.get("name", "")
                available.add(name.split("/")[-1])

            for candidate in preferred_order:
                if candidate in available:
                    if candidate != preferred_model:
                        print(
                            f"Gemini preferred model '{preferred_model}' unavailable; using '{candidate}'",
                            flush=True,
                        )
                    return candidate

            print(
                f"Gemini preferred/fallback models unavailable; using configured model '{preferred_model}'",
                flush=True,
            )
            return preferred_model
        except Exception as e:
            print(f"Gemini model discovery failed ({e}); using '{preferred_model}'", flush=True)
            return preferred_model


    # Whitelist of allowed tool functions to prevent arbitrary code execution
    ALLOWED_TOOLS = {
        "record_user_details": record_user_details,
        "record_unknown_question": record_unknown_question,
    }

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                print(f"WARNING: Invalid tool arguments for {tool_name}: {e}", flush=True)
                results.append({
                    "role": "tool",
                    "content": json.dumps({"error": f"Invalid arguments for {tool_name}"}),
                    "tool_call_id": tool_call.id,
                })
                continue
            print(f"Tool called: {tool_name}", flush=True)
            tool = self.ALLOWED_TOOLS.get(tool_name)
            if tool is None:
                print(f"WARNING: Unknown tool requested: {tool_name}", flush=True)
                result = {"error": f"Unknown tool: {tool_name}"}
            else:
                try:
                    result = tool(**arguments)
                except Exception as e:
                    print(f"WARNING: Tool execution failed for {tool_name}: {e}", flush=True)
                    result = {"error": f"Tool failed: {tool_name}"}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background, personal context, LinkedIn profile, and resume which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        
        if self.personal_context:
            system_prompt += f"## Personal Context:\n{self.personal_context}\n\n"
        
        if self.resume:
            system_prompt += f"## Resume:\n{self.resume}\n\n"
        
        system_prompt += f"## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def evaluator_system_prompt(self):
        evaluator_prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {self.name} and is representing {self.name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {self.name} in the form of their summary, personal context, resume, and LinkedIn details. Here's the information:"
        
        evaluator_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        
        if self.personal_context:
            evaluator_prompt += f"## Personal Context:\n{self.personal_context}\n\n"
        
        if self.resume:
            evaluator_prompt += f"## Resume:\n{self.resume}\n\n"
        
        evaluator_prompt += f"## LinkedIn Profile:\n{self.linkedin}\n\n"
        evaluator_prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."
        return evaluator_prompt
    
    def evaluator_user_prompt(self, reply, message, history):
        # Convert history to readable format
        history_text = ""
        for msg in history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            history_text += f"{role.capitalize()}: {content}\n\n"
        
        user_prompt = f"Here's the conversation between the User and the Agent:\n\n{history_text}\n\n"
        user_prompt += f"Here's the latest message from the User:\n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent:\n\n{reply}\n\n"
        user_prompt += (
            "Please evaluate the response, replying with whether it is acceptable and your feedback. "
            "Respond ONLY with a JSON object in the following format: "
            "{\"is_acceptable\": boolean, \"feedback\": string}. "
            "Do not include any extra text outside this json."
        )
        return user_prompt

    def log_evaluation(self, reply, message, history, evaluation: Evaluation, model: str):
        """Log evaluation results to data/evaluations.jsonl for offline analysis."""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "model": model,
                "message": message,
                "reply": reply,
                "history": history,
                "is_acceptable": evaluation.is_acceptable,
                "feedback": evaluation.feedback,
            }
            with open(data_dir / "evaluations.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log) + "\n")
        except Exception as e:
            print(f"Failed to log evaluation: {e}", flush=True)
    
    def evaluate(self, reply, message, history) -> Evaluation:
        """Evaluate a response using Gemini (or OpenAI if Gemini not available)"""
        evaluator_sys_prompt = self.evaluator_system_prompt()
        evaluator_user_prompt = self.evaluator_user_prompt(reply, message, history)
        
        messages = [
            {"role": "system", "content": evaluator_sys_prompt},
            {"role": "user", "content": evaluator_user_prompt}
        ]
        
        if self.use_gemini_evaluator:
            try:
                # Use Gemini with structured output parsing
                response = self.gemini.beta.chat.completions.parse(
                    model=self.gemini_evaluator_model,
                    messages=messages,
                    response_format=Evaluation
                )
                evaluation = response.choices[0].message.parsed
                self.log_evaluation(reply, message, history, evaluation, model=self.gemini_evaluator_model)
                return evaluation
            except Exception as e:
                print(f"Gemini evaluation failed: {e}. Falling back to OpenAI.", flush=True)
                # Fall through to OpenAI
        
        # Fallback to OpenAI with JSON mode
        response = self.openai.chat.completions.create(
            model=self.eval_model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        try:
            result = json.loads(response.choices[0].message.content)
            evaluation = Evaluation(**result)
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"Failed to parse OpenAI evaluation response: {e}", flush=True)
            evaluation = Evaluation(is_acceptable=True, feedback="Evaluation parse error; accepted by default.")
        self.log_evaluation(reply, message, history, evaluation, model=self.eval_model)
        return evaluation
    
    def rerun(self, reply, message, history, feedback):
        """Retry generating a response after evaluation failure"""
        updated_system_prompt = self.system_prompt()
        updated_system_prompt += "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        updated_system_prompt += "Please provide a better response that addresses the feedback."
        
        messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
        response = None
        for _ in range(self.MAX_TOOL_ITERATIONS):
            response = self.openai.chat.completions.create(model=self.chat_model, messages=messages, tools=tools)
            if response.choices[0].finish_reason == "tool_calls":
                message_obj = response.choices[0].message
                tool_calls = message_obj.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message_obj)
                messages.extend(results)
            else:
                break
        if response is None:
            return "I had trouble generating a response just now. Please try again."
        content = response.choices[0].message.content
        if content:
            return content
        return "I had trouble completing that request. Please try again in a moment."
    
    MAX_TOOL_ITERATIONS = 10

    def chat(self, message, history):
        # Clean up history format (in case Gradio adds extra fields)
        history = [{"role": h.get("role", "user"), "content": h.get("content", "")} for h in history]
        
        # Generate initial response
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        response = None
        for _ in range(self.MAX_TOOL_ITERATIONS):
            response = self.openai.chat.completions.create(model=self.chat_model, messages=messages, tools=tools)
            if response.choices[0].finish_reason == "tool_calls":
                message_obj = response.choices[0].message
                tool_calls = message_obj.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message_obj)
                messages.extend(results)
            else:
                break
        if response is None:
            return "I had trouble generating a response just now. Please try again."

        reply = response.choices[0].message.content
        if not reply:
            return "I had trouble completing that request. Please try again in a moment."
        
        # Evaluate the response
        evaluation = self.evaluate(reply, message, history)
        
        if evaluation.is_acceptable:
            print("✓ Passed evaluation - returning reply", flush=True)
            return reply
        else:
            print(f"✗ Failed evaluation - retrying\nFeedback: {evaluation.feedback}", flush=True)
            # Retry with feedback
            reply = self.rerun(reply, message, history, evaluation.feedback)
            return reply
    

if __name__ == "__main__":
    me = Me()

    examples = [
        "What kinds of roles are you interested in after TLDP?",
        "Tell me about a data science project you're proud of.",
        "What kind of problems do you enjoy solving?",
        "What tools and technologies do you use most often?",
    ]

    # Custom CSS to match the website's Cobalt sky theme
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .gradio-container {
        background: linear-gradient(135deg, #021008 0%, #021008 100%) !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    .contain {
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    /* Main title */
    .gradio-container h1 {
        color: #ffffff !important;
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 20px rgba(52, 211, 153, 0.3);
        margin-bottom: 0.25rem !important;
    }

    /* All headings inherit theme colors */
    .gradio-container h2, .gradio-container h3 {
        color: #ffffff !important;
    }

    /* Markdown text */
    .gradio-container .markdown {
        color: #c8dce8 !important;
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center !important;
        font-size: 1.05rem !important;
        color: #6D8196 !important;
        margin-bottom: 1.5rem !important;
    }

    /* Hide the "Chatbot" tab label */
    .tabs, .tab-nav {
        display: none !important;
    }

    /* Chat area */
    .chatbot {
        background: rgba(15, 118, 110, 0.15) !important;
        border: 1px solid rgba(52, 211, 153, 0.2) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        min-height: 400px !important;
    }

    /* User messages */
    .message.user {
        background: linear-gradient(135deg, #0F766E 0%, #064e3b 100%) !important;
        border-radius: 12px !important;
    }

    /* Bot messages */
    .message.bot {
        background: rgba(15, 118, 110, 0.25) !important;
        border: 1px solid rgba(52, 211, 153, 0.15) !important;
        border-radius: 12px !important;
    }

    /* Input area */
    textarea, input {
        background: rgba(15, 118, 110, 0.15) !important;
        border: 2px solid rgba(52, 211, 153, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }

    textarea:focus, input:focus {
        border-color: #34D399 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.3) !important;
        outline: none !important;
    }

    textarea::placeholder {
        color: #6D8196 !important;
    }

    /* Send button */
    button.primary, button[class*="submit"] {
        background: linear-gradient(135deg, #0F766E 0%, #064e3b 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(15, 118, 110, 0.3) !important;
    }

    button.primary:hover, button[class*="submit"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(52, 211, 153, 0.4) !important;
    }

    /* Example prompt buttons */
    .examples button {
        background: rgba(15, 118, 110, 0.15) !important;
        border: 1px solid rgba(52, 211, 153, 0.25) !important;
        color: #34D399 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        transition: all 0.25s ease !important;
    }

    .examples button:hover {
        border-color: #34D399 !important;
        background: rgba(52, 211, 153, 0.08) !important;
        transform: translateY(-1px) !important;
    }

    /* Footer */
    .footer-note {
        text-align: center !important;
        font-size: 0.85rem !important;
        opacity: 0.6;
        margin-top: 2rem !important;
        color: #6D8196 !important;
    }

    /* Labels */
    label, .label-wrap {
        color: #c8dce8 !important;
    }
    """

    with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
        gr.Markdown(f"# Chat with {me.name}")
        gr.Markdown(
            "I'm an AI version of Giovanni, a Data Scientist and TLDP analyst at Johnson & Johnson. "
            "Ask me about my experience, projects, and what I'm looking for next.",
            elem_classes="subtitle"
        )

        gr.ChatInterface(
            me.chat,
            type="messages",
            examples=examples,

        )

        gr.Markdown(
            "_Powered by OpenAI and Gradio \u00b7 This is an AI representation of Giovanni, not live human chat._",
            elem_classes="footer-note"
        )

    demo.launch()
