# Build a RAG in 10 minutes with Python, ChromaDB and OpenAI

GitHub Repository: [https://github.com/Parashar-dev/RAG](https://github.com/Parashar-dev/RAG)

---

## 📖 What is RAG (Retrieval-Augmented Generation)?

Standard Large Language Models (LLMs) have a cutoff date and do not know your private documents or specialized data. If asked about unknown facts, they often hallucinate.

**RAG** solves this by connecting an external knowledge base to the LLM in three key phases:

1. **Phase 1: Ingestion & Indexing (`fill_db.py`)**
   - **Load**: Read raw PDF documents from the `data/` folder.
   - **Chunk**: Split large pages into smaller, overlapping text chunks so context is preserved.
   - **Embed & Store**: Generate vector embeddings for each chunk and index them in a local **ChromaDB** vector database.

2. **Phase 2: Retrieval (`ask.py`)**
   - The user inputs a natural language question.
   - ChromaDB searches the database using semantic similarity (vector distance) and fetches the top matching text chunks.

3. **Phase 3: Augmentation & Generation (`ask.py`)**
   - **Augmentation**: Inject the retrieved text chunks into the prompt as factual context.
   - **Generation**: Pass the prompt to **OpenAI GPT-4o** with strict instructions to answer *only* using the provided knowledge.

```
┌────────────────────────────────────────────────────────┐
│ Phase 1: Ingestion (fill_db.py)                        │
│ PDFs in /data ──► Text Splitter ──► ChromaDB Vector DB │
└───────────────────────────────────────────┬────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2 & 3: Retrieval & Generation (ask.py)           │
│ User Question ──► ChromaDB Similarity Search           │
│                         │                              │
│                         ▼                              │
│     [System Guardrails + Retrieved Chunks]             │
│                         │                              │
│                         ▼                              │
│                 OpenAI GPT-4o                          │
│                         │                              │
│                         ▼                              │
│                 Factual AI Answer                      │
└────────────────────────────────────────────────────────┘
```

---

## Prerequisites
- Python 3.11+
- OpenRouter API Key (or OpenAI API Key)

---

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/Parashar-dev/RAG.git
cd RAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:
```bash
venv\Scripts\Activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

### 4. Install libraries

```bash
pip install -r requirements.txt
```

### 5. Add API Key

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your API key:
- **OpenRouter (Recommended)**: Get a key from [https://openrouter.ai/keys](https://openrouter.ai/keys) and set `OPENROUTER_API_KEY`. You can also configure `LLM_MODEL` (e.g. `meta-llama/llama-3.3-70b-instruct`, `openai/gpt-4o`, `deepseek/deepseek-chat`).
- **OpenAI**: Get a key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) and set `OPENAI_API_KEY`.

---

## 🚀 Step-by-Step Guide to Run

### Step 1: Activate Virtual Environment
Always activate your virtual environment before running scripts so Python can find `chromadb` and other installed libraries:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
*(Your terminal prompt should now show `(.venv)`).*

---

### Step 2: Configure API Key in `.env`
If you haven't already, copy `.env.example` to `.env` and add your **OpenRouter** or **OpenAI** API key:
```bash
cp .env.example .env
```
In `.env`:
```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
LLM_MODEL="meta-llama/llama-3.3-70b-instruct"
```

---

### Step 3: Ingest Data into Vector DB (`fill_db.py`)
Ensure your PDF document is in the `data/` folder (e.g., `data/VH021.pdf`), then run:
```bash
python fill_db.py
```
**What happens here:**
- Extracts text from the PDF.
- Breaks it into 300-character chunks with 100-character overlap.
- Converts each chunk into vectors using local embedding (`all-MiniLM-L6-v2`).
- Saves the vectors to disk in `chroma_db/`.

---

### Step 4: Ask Questions (`ask.py`)
Run the query script to chat with your document:
```bash
python ask.py
```
Example question:
> *What vegetables can grow in Florida?*

---

