# Build a RAG in 10 minutes with Python, ChromaDB and OpenAI

GitHub Repository: [https://github.com/Parashar-dev/RAG](https://github.com/Parashar-dev/RAG)

## Prerequisites
- Python 3.11+

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

```bash
venv\Scripts\Activate
# (or on macOS/Linux): source venv/bin/activate
```

### 4. Install libraries

```bash
pip install -r requirements.txt
```

### 5. Add OpenAI API Key

Get an OpenAI API Key from here: https://platform.openai.com/settings/organization/admin-keys  
Add it to `.env.example` and rename to `.env` (or copy it):
```bash
cp .env.example .env
```

## Executing the scripts

- Open a terminal in VS Code
- Execute the following commands:

```bash
python fill_db.py
python ask.py
```
