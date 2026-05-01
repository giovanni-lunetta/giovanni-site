# Giovanni Lunetta

**AI Engineer & Data Scientist**

glunetta02@gmail.com | Pequannock, NJ | [GitHub](https://github.com/giovannilunetta) | [Medium](https://medium.com/@giovannilunetta) | [LinkedIn](https://linkedin.com/in/giovannilunetta) | [giovannilunetta.com](https://giovannilunetta.com)

---

## PROFESSIONAL SUMMARY

AI Engineer and Data Scientist with 2+ years building production GenAI and ML systems in healthcare. Designed and shipped a fully autonomous agentic document platform with semantic mapping, confidence-aware automation, LLM governance, and 409 tests in under 4 weeks. Built multi-brand ML pipelines across 3 therapeutic areas and architected event-driven AWS pipelines eliminating 200+ hours of manual processing annually. Skilled in Python, LangChain, agentic workflow orchestration, RAG architectures, XGBoost, clustering, and AWS.

---

## WORK EXPERIENCE

### Technology LDP Analyst — Data & Decision Science
**Johnson & Johnson (MedTech R&D)** | 06/2024 – Present | Raritan, NJ

**Agentic Document Intelligence Platform:**
- Designed and delivered a fully autonomous agentic onboarding platform that enables business users to independently discover automation opportunities and generate production-ready extraction rules — without requiring data science involvement. Features two operating modes (Mapping Mode for source-to-template variable mapping; Explore Mode for template-free discovery), semantic-first mapping, and confidence-aware automation (AUTO_MAP vs. NEEDS_REVIEW).
- Built with pipeline resumability via checkpointing, full LLM governance with per-call audit trails, and a Flask web UI with API key authentication, SSE streaming, and per-user rate limiting. CI/CD via GitHub Actions with pytest (409 tests) and Playwright E2E. Delivered production-hardened in 3–4 weeks.

**Vision-Based PDF Document Extraction:**
- Built vision-based PDF table extraction using GPT-4o multimodal capabilities, rendering 400+ page regulatory documents as 300 DPI images paired with extracted text to accurately capture complex tables with merged cells, multi-row headers, and hierarchical structures. Engineered automated TOC-based document segmentation (62 sections per CER) to fit within LLM context windows. Achieved 90–95% accuracy on complex regulatory tables vs. 70–80% with text-only approaches, reducing manual processing from 4+ hours to <30 minutes per document.

**Persistency Modeling — Multi-Brand ML Pipelines:**
- Built a persistency model for a treatment-resistant depression therapy from scratch — extracting and integrating 3 fulfillment channels (70K patients, 3.6M patient-weeks), engineering 35 leakage-safe features across 7 clinical phases, and training XGBoost with Optuna hyperparameter tuning (F1=0.782, ROC-AUC=0.750, 12.9x lift).
- Designed phase-aware gap thresholds grounded in synthesis of 6+ published clinical studies, replacing the one-size-fits-all approach. Conducted methodology audit identifying that the new cohort captured 37% more patients than the vendor pipeline.
- Validated a 14-node Kedro ML pipeline for a biologic drug persistency model (1.3M+ records, XGBoost, ROC-AUC=0.717), identifying a critical sampling bug that caused loss of validation/test splits — preventing erroneous model evaluations from reaching production and producing comprehensive documentation for cross-brand replication.
- Integrated 4 heterogeneous data sources for a combination oncology therapy analysis (76K events, 5.1K patients) with clinically grounded persistency target definitions validated through sensitivity analysis. Identified that combination therapy patients showed materially better persistence (64% non-persistent vs. 83% monotherapy), informing medical affairs and market access strategy.

**Surgical Preference Modeling for Robotic-Assisted Surgery:**
- Delivered surgeon preference classification for a robotic-assisted surgery platform using two complementary approaches: rule-based classification achieving 67% coverage (+23 points over baseline) through 10 iterative refinements, and Fuzzy C-Means clustering across 4 independent feature sets (silhouette=0.66) to capture surgeons with multiple preference profiles. Cross-validated cluster assignments against rule-based labels. Built a Tableau dashboard iterated 6 times that was used in clinical decision support, marketing discussions, and to inform product strategy.

**HCP Segmentation & Treatment Pattern Analytics:**
- Segmented healthcare providers treating a rare hematologic condition across two datasets (~10K HCP Universe, ~27K Prescription Universe) by engineering 90+ features from claims and provider-level data, training K-Means clustering (silhouette=0.42), and delivering 6 HCP personas adopted by the commercial team for targeted outreach of an emerging therapy. Validated with ANOVA and Kruskal-Wallis; cross-validated against market research findings. Extended into treatment pattern analysis (awarded as follow-on), building custom classification logic for biologic dosing complexity and irregular dosing patterns to identify innovative prescribers vs. those needing clinical education, supporting differentiated commercial engagement strategies.

**Product Ownership — Regulatory Document Platform:**
- Led product management for an internal regulatory document platform across 4+ releases (backlog, QA/Prod change execution, cross-functional coordination). Proactively expanded scope to own all GenAI integration — automated citation extraction, semantic search with document embeddings and hash-based deduplication, header extraction replacing keyword-based chunking, and an LLM consistency testing framework. Selected as a featured project for the 2025 MedTech Data Science & AI Showcase.

**AWS Cost Optimization & Data Engineering:**
- Architected dual 3-Lambda event-driven pipelines (daily + monthly) with 42-column enrichment schema, EventBridge scheduling, UUID-based lineage, and concurrent Lambda serialization fixes — eliminating 200+ hours annually of manual processing. Attributed $2.3M+ in AWS costs at 85%+ coverage across enterprise accounts with self-service Tableau dashboards.

### Technology Summer Intern — Data Science
**Johnson & Johnson (Janssen Pharmaceuticals)** | 05/2023 – 08/2023 | Titusville, NJ

- Developed a machine learning model using healthcare claims data to predict patient drug eligibility 6 months in advance, optimizing doctor outreach targeting and pharmaceutical processes.

---

## PROJECTS

**AI Portfolio Assistant** *(Self-Evaluating LLM System)* — [giovannilunetta.com](https://giovannilunetta.com)
- Architected production conversational AI using GPT-4o-mini and Gemini 2.0 Flash featuring automated quality control, function calling for lead capture, and self-improving feedback loop. Implemented evaluation retry loop with dual-model assessment (generation vs. evaluation) and JSONL-based analytics for continuous improvement. Deployed via Gradio.

**Hack4Health — Surgical Intelligent Assistant (SURiA)**
- Created voice-activated, offline-capable AI assistant supporting surgical teams in the OR with real-time guidance and automation. Placed Top 3 in MedTech category; selected for Proof-of-Concept funding — one of only three teams across all of MedTech chosen for Hack4Health 2025 funding.

**DateBack** *(macOS Application)*
- Built production macOS desktop app (Electron + Python) processing Snapchat exports (50GB+) with EXIF date restoration, batched cloud streaming, and Apple code signing. Full professional distribution (notarization, auto-updates, DMG installer) with 100% offline-first architecture.

---

## EDUCATION

**M.S. in Data Science**, University of Connecticut | 09/2023 – 05/2024 | Storrs, CT

**B.A. in Statistics & Political Science, Math (Minor)**, University of Connecticut | 09/2020 – 05/2023 | Storrs, CT

---

## SKILLS

- **Agentic AI & LLM Engineering:** OpenAI API, GPT-4o multimodal, LangChain, LangGraph, RAG architectures, hybrid retrieval (vector + BM25), Postgres + pgvector (HNSW), agentic workflow design (stage orchestration, checkpointing, resumability), semantic search, document embeddings, schema-validated extraction, LLM governance/audit trails, prompt engineering, token optimization, vision-based document extraction, Flask (SSE streaming, API auth)
- **Machine Learning & Modeling:** Python, R, XGBoost, neural networks, Kedro pipelines, semi-supervised learning (co-training, self-training), clustering (Fuzzy C-Means, K-Means), PCA, evaluation (CV, AUC/PR, F1, silhouette, SHAP), ANOVA, Kruskal-Wallis, feature engineering, leakage-safe design
- **Data Engineering & Cloud:** AWS (Lambda, S3, Athena, Redshift, IAM, EventBridge, CloudShell), event-driven pipelines, ETL automation, SQL (Postgres, Redshift), Databricks (fundamentals), GitHub Actions CI/CD, pytest, schema design, query optimization, concurrent execution patterns
- **Analytics, BI & Product:** Tableau (Desktop Specialist certified), Power BI, agile delivery, stakeholder coordination, technical documentation

---

## CERTIFICATES

- **Certified:** AWS Certified Cloud Practitioner | Tableau Desktop Specialist
- **Professional Programs:** Harvard/edX — Data Science Professional Certificate; CS50x | Babson Exec Ed — J&J Design Thinking
- **Specialized Training:** AI Engineer Agentic Track: The Complete Agent & MCP Course | DeepLearning.AI — ML Specialization, Prompt Engineering, LangChain, Diffusion Models | Databricks Fundamentals Accreditation
