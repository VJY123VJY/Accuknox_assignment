# AccuKnox AI/ML Trainee Technical Assignment Solution & Interview Guide

This repository contains the complete, tested solutions for the AccuKnox AI/ML Trainee technical assessment, structured for clean execution, strong engineering practices, and thorough interview readiness.

---

## Table of Contents
1. [Problem Statement 1: Practical Coding Solutions](#problem-statement-1-practical-coding-solutions)
   - [Question 1: Book API Data Ingestion into SQLite](#question-1-book-api-data-ingestion-into-sqlite)
   - [Question 2: Student Test Scores API, Average Calculation & Bar Chart](#question-2-student-test-scores-api-average-calculation--bar-chart)
   - [Question 3: User Information CSV ETL into SQLite](#question-3-user-information-csv-etl-into-sqlite)
   - [Question 4: Link & Showcase: Most Complex Python Code](#question-4-link--showcase-most-complex-python-code)
   - [Question 5: Link & Showcase: Most Complex Database Code](#question-5-link--showcase-most-complex-database-code)
2. [Assignment 2: Conceptual & Architectural Deep-Dives](#assignment-2-conceptual--architectural-deep-dives)
   - [Question 1: Self-Rating (A/B/C) with Justification](#question-1-self-rating-abc-with-justification)
   - [Question 2: High-Level Architecture of an LLM Chatbot](#question-2-high-level-architecture-of-an-llm-chatbot)
   - [Question 3: Vector Databases & Hypothetical Problem Selection](#question-3-vector-databases--hypothetical-problem-selection)
3. [Mock Interview Q&A (Preparing for Trainee Technical Round)](#mock-interview-qa)

---

# Problem Statement 1: Practical Coding Solutions

## Question 1: Book API Data Ingestion into SQLite
**File:** `problem1_q1_books.py`

### What it does:
- Queries the public **Open Library Search API** (`https://openlibrary.org/search.json?q=artificial+intelligence&limit=8`).
- Uses `requests` with timeouts and HTTP status checks (`raise_for_status()`).
- Creates an SQLite database `books.db` with an auto-incrementing primary key and audit timestamp.
- Executes parameterized `INSERT` statements (`?` placeholders) using `cursor.executemany()` to prevent SQL injection.
- Queries `SELECT * FROM books` and formats the records in a terminal table.

### Execution:
```bash
python problem1_q1_books.py
```

---

## Question 2: Student Test Scores API, Average Calculation & Bar Chart
**File:** `problem1_q2_student_scores.py`

### What it does:
- Provides a self-contained REST API using Python's built-in `http.server` running in a daemon thread (ensuring 100% offline stability during live interview demos), while remaining compatible with any external REST endpoint.
- Fetches student test-score records via HTTP GET (`requests`).
- Computes comprehensive statistical metrics:
  - **Mean (Average)**: `82.20`
  - **Median**: `84.00`
  - **Max / Min**: `96 / 64`
- Renders an informative bar chart using `matplotlib` (using `'Agg'` backend):
  - Individual student bars color-coded by performance (green if $\ge$ average, amber if $<$ average).
  - Prominent horizontal dashed line indicating the class average.
  - Data labels on top of each bar.
  - Saves high-resolution chart to `student_scores_bar_chart.png`.

### Execution:
```bash
python problem1_q2_student_scores.py
```

---

## Question 3: User Information CSV ETL into SQLite
**File:** `problem1_q3_csv_to_sqlite.py` & `users.csv`

### What it does:
- Parses `users.csv` using `csv.DictReader` for safe key-value column mapping.
- Validates data integrity: checks for required schema fields, trims whitespace, standardizes emails to lowercase, and validates IDs.
- Creates `users.db` with a strict schema (`user_id PRIMARY KEY`, `email UNIQUE`, timestamps).
- Employs SQLite UPSERT logic (`ON CONFLICT(user_id) DO UPDATE ...`) to maintain idempotency (running the script multiple times updates existing records without crashing or duplicating).
- Selects and displays the stored records to confirm successful ingestion.

### Execution:
```bash
python problem1_q3_csv_to_sqlite.py
```

---

## Question 4: Link to Most Complex Python Code
**Recommendation for Submission:**
Provide a link to your public GitHub repository containing a real project.

### Recommended Project Profile:
- **Project Name:** End-to-End Multimodal / RAG Search Pipeline or Asynchronous Model Serving Microservice
- **Example GitHub Link Format:** `https://github.com/<your-username>/rag-semantic-search-pipeline`

### Technical Explanation to Give in the Interview:
> "My most complex Python project is an end-to-end RAG (Retrieval-Augmented Generation) pipeline built using FastAPI, PyTorch / Hugging Face Transformers, and FAISS/Qdrant. 
> Key technical highlights:
> 1. **Asynchronous Architecture:** Used Python `asyncio` and `httpx` to handle concurrent document scraping and embedding generation without blocking the event loop.
> 2. **Chunking & Preprocessing:** Implemented recursive character text splitters with token-count thresholds and regex cleaners.
> 3. **Batch Vectorization:** Implemented dynamic batching for the sentence-transformers model (`all-MiniLM-L6-v2`) to maximize GPU memory efficiency.
> 4. **Resilience & Testing:** Used Pydantic v2 for strict runtime schema validation, custom exception handlers, and `pytest` test suites covering edge cases like empty chunks and out-of-vocabulary queries."

*(A ready-to-upload template script is provided in `complex_python_sample.py`)*

---

## Question 5: Link to Most Complex Database Code
**Recommendation for Submission:**
Provide a link to a GitHub repository or Gist containing advanced SQL schema, window functions, indexing, or an ORM data pipeline.

### Recommended Profile:
- **Project Name:** Analytical E-Commerce / Telemetry Data Warehouse Schema with Window Functions & CTEs
- **Example GitHub / Gist Link Format:** `https://gist.github.com/<your-username>/advanced-sql-analytics-schema`

### Technical Explanation to Give in the Interview:
> "My most complex database work involves a multi-table relational schema designed in PostgreSQL with high-volume indexing strategies and analytical queries.
> Key technical highlights:
> 1. **Data Modeling & Integrity:** Designed a normalized (3NF) relational schema with composite primary keys, foreign key constraints with `ON DELETE CASCADE`, and `CHECK` constraints on numeric ranges.
> 2. **Advanced SQL Features:** Wrote Common Table Expressions (CTEs), recursive CTEs for hierarchical data, and window functions (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` and `LAG()` / `LEAD()` to detect rolling trends).
> 3. **Performance Optimization:** Added composite B-Tree indexes on heavily filtered columns and GIN indexes for full-text search fields. Used `EXPLAIN ANALYZE` to eliminate sequential table scans and optimize query cost."

*(A ready-to-upload SQL script is provided in `complex_database_sample.sql`)*

---

# ASSIGNMENT 2: Conceptual & Architectural Deep-Dives

## Question 1: Self-Rating (A/B/C) with Justification

| Domain | Rating | Honest Justification for Trainee Level |
| :--- | :---: | :--- |
| **Machine Learning (ML)** | **A** | **Can code independently.** Strong foundational knowledge of supervised and unsupervised learning algorithms (Linear/Logistic Regression, Random Forests, XGBoost, K-Means). Comfortable with data preprocessing (scaling, one-hot encoding, handling nulls), feature engineering, cross-validation, and evaluation metrics (ROC-AUC, F1-score, RMSE) using `scikit-learn`, `pandas`, and `numpy`. |
| **Artificial Intelligence (AI)** | **B** | **Can code under supervision.** Understands core AI paradigms including state-space search (A*, minimax), heuristic optimization, and probabilistic reasoning. Capable of building rule engines and foundational agents, but seeks architectural guidance for large-scale multi-agent coordination. |
| **Deep Learning (DL)** | **B** | **Can code under supervision.** Comfortable designing, training, and fine-tuning neural networks (CNNs for image classification, RNNs/LSTMs, and basic Transformer blocks) using `PyTorch`. Understands backpropagation, loss functions, learning rate schedules, and regularization (Dropout, BatchNorm). Requires supervision when tuning distributed training (DDP) or optimizing low-level CUDA kernels. |
| **Large Language Models (LLMs)** | **B** | **Can code under supervision.** Experienced in building applications around modern LLMs: prompt engineering, RAG pipelines with vector databases, function calling/tool use, and evaluation frameworks. Can perform LoRA/QLoRA parameter-efficient fine-tuning using Hugging Face `peft` and `transformers`. Requires guidance on pre-training from scratch or custom attention kernel optimizations (FlashAttention). |

---

## Question 2: High-Level Architecture of an LLM Chatbot

### System Architecture Diagram
```
[ User Client: Web / Mobile / CLI ]
                │
                ▼ (HTTPS / WSS)
   ┌───────────────────────────┐
   │    API Gateway / FastAPI  │
   │  (Auth, Rate Limiting)    │
   └────────────┬──────────────┘
                │
                ▼
   ┌───────────────────────────┐
   │     Input Guardrails      │ ──► [Filter PII / Prompt Injections / Toxicity]
   └────────────┬──────────────┘
                │
        ┌───────┴────────────────────────┐
        ▼                                ▼
┌──────────────────┐          ┌──────────────────────┐
│  Session Memory  │          │  Knowledge Retrieval │
│ (Redis / Dynamo) │          │       (RAG)          │
│ - Chat History   │          │ - Query Embedding    │
│ - User Profile   │          │ - Vector DB (Qdrant) │
└───────┬──────────┘          └──────────┬───────────┘
        │                                │
        └───────────────┬────────────────┘
                        │
                        ▼
       ┌─────────────────────────────────┐
       │   Prompt Assembly & Context     │
       │ (System Prompt + History + RAG) │
       └────────────────┬────────────────┘
                        │
                        ▼
       ┌─────────────────────────────────┐
       │     LLM Inference Engine        │
       │ (vLLM / Ollama / OpenAI API)    │
       └────────────────┬────────────────┘
                        │
                        ▼
       ┌─────────────────────────────────┐
       │     Output Guardrails           │ ──► [Hallucination check, Moderation]
       └────────────────┬────────────────┘
                        │
                        ▼ (Token Streaming)
[ Streamed Response back to User Client ]
```

### Detailed Component Breakdown:

1. **Client & API Gateway:**
   - Handles incoming client requests over WebSockets or HTTP Server-Sent Events (SSE) for low-latency token streaming.
   - Manages JWT authentication, request validation, and rate limiting (e.g., token bucket algorithm).

2. **Input Guardrails (Safety Layer):**
   - Employs lightweight classification models or rule-based filters (e.g., NeMo Guardrails, regex, or small RoBERTa classifiers) to intercept prompt injections, jailbreaks, toxicity, and Sensitive PII (Personally Identifiable Information) before hitting the LLM.

3. **Conversation Memory & Context Management:**
   - **State Store (Redis):** Persists multi-turn conversation history with session TTLs.
   - **Context Window Trimmer:** Uses sliding window or summary buffering to ensure total token counts stay within the model's maximum context length.

4. **Retrieval-Augmented Generation (RAG Pipeline):**
   - Ingestion: Documents are chunked (e.g., 512 tokens with 50-token overlap) and embedded via an embedding model (e.g., `text-embedding-3-small` or `bge-large-en`).
   - Retrieval: Converts the user's latest query into a dense vector, performs Approximate Nearest Neighbor (ANN) search in a Vector DB with metadata filtering, and re-ranks top-$k$ hits using a cross-encoder.

5. **LLM Orchestration & Inference:**
   - Synthesizes the final prompt: `System Instructions + Retrieved Chunks + Conversation History + Current Query`.
   - Dispatches to the inference layer: either self-hosted open-weights models (via **vLLM** for continuous batching and PagedAttention) or proprietary endpoints (OpenAI / Claude).

6. **Output Guardrails & Observability:**
   - Checks response for factual consistency, sensitive data leaks, and formatting rules (JSON schema).
   - Telemetry: Integrates **OpenTelemetry** or **Langfuse** / **LangSmith** to monitor latency, token consumption, cost, and hallucination scores.

---

## Question 3: Vector Databases & Hypothetical Problem Selection

### 1. What is a Vector Database?
Traditional databases (SQL/NoSQL) excel at exact matches (`WHERE id = 5` or `WHERE name = 'Alice'`). However, unstructured data (text, images, audio) cannot be queried using exact equality. 

A **Vector Database** stores high-dimensional dense numerical vectors (embeddings) generated by deep learning models. Instead of exact equality, it performs **similarity search**: identifying vectors closest to a query vector in multi-dimensional space.

#### Key Mechanics:
- **Distance Metrics:**
  - *Cosine Similarity:* Measures the angle between vectors (scale-invariant; range $-1$ to $1$). Best for text embeddings.
  - *Dot Product:* Measures angle and magnitude. Best when vectors are normalized.
  - *Euclidean Distance ($L_2$):* Measures straight-line distance.
- **Indexing Algorithms (ANN - Approximate Nearest Neighbor):**
  - *HNSW (Hierarchical Navigable Small World):* Multi-layer graph traversal. Provides optimal speed-recall tradeoff with sub-millisecond query latency.
  - *IVF-PQ (Inverted File with Product Quantization):* Clustered indexing with vector compression to drastically reduce RAM usage.

---

### 2. Comparative Matrix of Leading Vector Databases

| Feature | **Qdrant** | **Pinecone** | **ChromaDB** | **pgvector** |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture** | Native Rust, standalone engine | Cloud-native SaaS | Python/SQLite-backed | PostgreSQL Extension |
| **Deployment** | Self-hosted (Docker) or Cloud | Managed Cloud only | Embedded in-process / Local | Extends existing Postgres |
| **Payload/Metadata Filtering** | Pre-filtering during HNSW traversal | Yes (Cloud metadata) | Post-filtering (slower) | Standard SQL `WHERE` |
| **Scalability** | Distributed clustering, millions of vectors | Billions of vectors | Small-to-medium (in-memory) | Millions of vectors |
| **Resource Footprint** | Extremely efficient (Rust, low RAM) | Zero infra management | Minimal (great for prototyping) | Leverages Postgres pool |

---

### 3. Hypothetical Problem & Selection

#### The Problem:
> *"Building an enterprise-grade AI technical support assistant that searches across 2,000,000 internal documentation chunks, code snippets, and customer ticket resolutions. It requires sub-50ms search latency, strict tenant-level metadata filtering (e.g., `tenant_id == X` and `permission_level <= Y`), on-premise/hybrid deployment support due to data privacy regulations, and predictable infrastructure cost."*

#### Selected Vector Database: **Qdrant**

#### Justification:
1. **Payload-Aware HNSW Graph Traversal (Pre-filtering):**
   Most vector databases perform post-filtering (find top 100 similar items, then discard those not matching metadata), which leads to empty results if metadata is restrictive. Qdrant integrates payload filtering directly into the HNSW graph traversal step, ensuring high recall and constant sub-30ms latency even under strict tenant isolation.
2. **On-Premise & Cloud Agnostic Deployment:**
   Unlike Pinecone (proprietary SaaS only), Qdrant is open-source and written in Rust. It can be deployed inside an enterprise VPC via Docker/Kubernetes, satisfying data residency and GDPR/HIPAA compliance requirements.
3. **Memory Efficiency & Disk-Backed Storage:**
   Qdrant supports memory-mapped files (mmap) and scalar quantization (SQ). This allows storing vector payloads on NVMe SSDs while maintaining high throughput, cutting RAM costs by up to 70% compared to purely in-memory solutions.
4. **Developer Experience:**
   Provides an official, well-maintained Python client (`qdrant-client`), native async support, and built-in REST and gRPC interfaces for high-concurrency production deployments.

---

# Mock Interview Q&A (Preparing for Trainee Technical Round)

### Q1: Why did you use `executemany()` and `?` placeholders in SQLite instead of string formatting (`f"INSERT INTO ... VALUES ('{title}')"`)?
**Answer:**
> "Using `f-strings` or string concatenation creates a critical security risk known as **SQL Injection**, where malicious user input can execute arbitrary database queries. Furthermore, string formatting breaks whenever input text contains quotes or special characters (e.g., a book titled *Don't Make Me Think*).
> `executemany()` with `?` placeholders sends the query structure and the parameters separately to the database engine. The driver treats the values strictly as literal data, preventing injection and improving execution speed through prepared statement reuse."

### Q2: How would you handle an API that returns 50,000 records instead of 10?
**Answer:**
> "I would implement **pagination** and **batch streaming**:
> 1. Ingest page by page using `page` and `limit` query parameters.
> 2. Avoid holding all 50,000 JSON objects in memory simultaneously to prevent Out-Of-Memory (OOM) errors.
> 3. Use a Python generator to yield chunks of 500–1,000 records and commit them in database transactions using `conn.commit()` per batch."

### Q3: Why did you choose `matplotlib.use('Agg')` in your plotting script?
**Answer:**
> "`Agg` is a non-interactive backend for Matplotlib that rasterizes figures directly to file formats like PNG without requiring an active graphical desktop window (X11 / Wayland / Windows GUI). This ensures the script runs reliably on headless cloud servers, CI/CD pipelines, and automated background jobs without crashing with a 'cannot connect to display' error."

### Q4: In CSV ingestion, what happens if the CSV file contains duplicate user IDs or duplicate emails?
**Answer:**
> "In my implementation, `user_id` is defined as the `PRIMARY KEY` and `email` has a `UNIQUE` constraint. To handle duplicate IDs gracefully, I used SQLite's `INSERT INTO ... ON CONFLICT(user_id) DO UPDATE ...` (UPSERT). If a record with an existing `user_id` is encountered, it updates the record with the latest values instead of raising an unhandled `sqlite3.IntegrityError` and crashing the pipeline."

### Q5: How do you measure the accuracy and performance of a RAG pipeline?
**Answer:**
> "I evaluate a RAG pipeline across two core dimensions:
> 1. **Retrieval Metrics:**
>    - **Hit Rate / Recall@K:** Was the ground-truth document retrieved in the top $K$ results?
>    - **MRR (Mean Reciprocal Rank):** How high up in the ranking was the first relevant document?
> 2. **Generation Metrics (using frameworks like Ragas or TruLens):**
>    - **Faithfulness / Groundedness:** Is the answer strictly derived from the retrieved context (hallucination check)?
>    - **Answer Relevance:** Does the generated response directly answer the user's query?"
