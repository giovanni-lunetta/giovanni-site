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
- Designed and delivered a fully autonomous agentic onboarding platform enabling business users to independently discover automation opportunities and generate production-ready extraction rules — without data science involvement. Two operating modes (Mapping Mode for source-to-template variable mapping; Explore Mode for template-free discovery), semantic-first mapping, and confidence-aware automation (AUTO_MAP vs. NEEDS_REVIEW).
- Engineered pipeline resumability via checkpointing, full LLM governance with per-call audit trails, and a Flask web UI with API key auth, SSE streaming, and rate limiting. CI/CD via GitHub Actions with pytest (409 tests) and Playwright E2E. Delivered production-hardened in 3–4 weeks.

**Vision-Based PDF Document Extraction:**
- Built vision-based PDF table extraction using GPT-4o multimodal, rendering 400+ page regulatory documents as 300 DPI images paired with extracted text to capture complex tables with merged cells and hierarchical structures. Engineered TOC-based document segmentation (62 sections per CER) to fit LLM context windows. Achieved 90–95% accuracy vs. 70–80% text-only, reducing manual processing from 4+ hours to <30 minutes per document.

**Persistency Modeling — Multi-Brand ML Pipelines:**
- Built a persistency model for a treatment-resistant depression therapy from scratch — integrating 3 fulfillment channels (70K patients, 3.6M patient-weeks), engineering 35 leakage-safe features across 7 clinical phases, and training XGBoost with Optuna tuning (F1=0.782, ROC-AUC=0.750, 12.9x lift). Designed phase-aware gap thresholds from synthesis of 6+ clinical studies, capturing 37% more patients than the vendor pipeline.
- Validated a 14-node Kedro ML pipeline for a biologic drug model (1.3M+ records, ROC-AUC=0.717), identifying a critical sampling bug that caused loss of validation/test splits — preventing erroneous evaluations from reaching production and producing comprehensive documentation for cross-brand replication.

**Commercial ML Analytics — Surgical Preference & HCP Segmentation:**
- Delivered surgeon preference classification for a robotic-assisted surgery platform combining rule-based classification (67% coverage, +23 pts over baseline) with Fuzzy C-Means clustering (silhouette=0.66) across 4 feature sets. Built a Tableau dashboard used in clinical decision support and product strategy.
- Segmented ~10K HCPs treating a rare hematologic condition by engineering 90+ features, training statistically validated K-Means clustering, and delivering 6 personas adopted by the commercial team for targeted outreach. Extended into treatment pattern analysis (awarded as follow-on) to identify innovative prescribers vs. those needing clinical education.

**Product Ownership — Regulatory Document Platform:**
- Led product management across 4+ releases, expanding scope to own all GenAI integration — citation extraction, semantic search with document embeddings, header-based chunking, and an LLM consistency testing framework. Selected as a featured project for the 2025 MedTech Data Science & AI Showcase.

**AWS Cost Optimization & Data Engineering:**
- Architected dual 3-Lambda event-driven pipelines (daily + monthly) with EventBridge scheduling, UUID-based lineage, and concurrent serialization fixes — eliminating 200+ hours annually. Attributed $2.3M+ in AWS costs at 85%+ coverage with self-service Tableau dashboards.

### Technology Summer Intern — Data Science
**Johnson & Johnson (Janssen Pharmaceuticals)** | 05/2023 – 08/2023 | Titusville, NJ

- Built an ML model on healthcare claims data to predict patient drug eligibility 6 months in advance, optimizing doctor outreach targeting.

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
