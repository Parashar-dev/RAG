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

## 🎓 How to Teach and Explain RAG to Students

### The "Open-Book Exam" Analogy
Explain RAG using a simple metaphor:
- **Standard LLM without RAG = Closed-Book Exam**: The model relies only on memory. If it doesn't know the exact details of a private document, it guesses or hallucinates.
- **RAG = Open-Book Exam**:
  1. **Retrieval**: The student quickly looks up the index and flips to the exact relevant textbook page.
  2. **Augmentation**: The student reads that page and places it on their desk as reference notes.
  3. **Generation**: The student writes the answer strictly citing what is on those notes.

---

## 🔍 How to Analyze the System with Students (Live Demonstrations)

Have students run these 4 experiments to understand how each component behaves:

### 🔬 Experiment 1: Verify Grounded Generation (Happy Path)
- **Question:** *"What varieties of squash can grow in Florida?"*
- **What to analyze:**
  - Look at the `--- Retrieved Knowledge Chunks ---` printed in the terminal.
  - Notice how the final AI answer directly quotes the varieties (Cocozelle, Spineless Beauty, Table King, etc.) found in those exact chunks.

### 🔬 Experiment 2: The Hallucination Prevention Test
- **Question:** *"What is the capital of France?"* or *"Who won the 2022 FIFA World Cup?"*
- **What to analyze:**
  - Notice that ChromaDB might still return some loosely related text chunks (because vector search finds the nearest mathematical vectors even if relevance is low).
  - However, because of our strict system prompt:
    > *"You only answer based on knowledge I'm providing you... If you don't know the answer, just say: I don't know"*
  - The model responds: **"I don't know."**
  - **Key takeaway for students:** Prompt engineering combined with retrieval prevents LLMs from hallucinating.

### 🔬 Experiment 3: Inspecting Vector Distance & Relevance
- In [`ask.py`](file:///home/parashar/Desktop/Retrieval-Augmented-Generation-main/ask.py), uncomment or inspect `results['distances']`:
  ```python
  print(results['distances'])
  ```
- **What to analyze:**
  - For relevant questions, distances are smaller (closer in vector space).
  - For irrelevant questions, distances are larger.

### 🔬 Experiment 4: Chunking Trade-Offs (`fill_db.py`)
- Change `chunk_size` from `300` to `50` or `2000` in [`fill_db.py`](file:///home/parashar/Desktop/Retrieval-Augmented-Generation-main/fill_db.py#L68-L73).
- **What to analyze:**
  - **Too small (e.g. 50 characters):** Chunks lose sentence context; retrieval fails to provide meaningful information.
  - **Too big (e.g. 2000 characters):** Chunks contain too much noise and dilute semantic relevance.
  - **Overlap (100 characters):** Explains why sentences cut across chunk boundaries don't lose their meaning.
