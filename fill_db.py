"""
=============================================================================
RAG (Retrieval-Augmented Generation) Tutorial - Step 1: Knowledge Ingestion
=============================================================================
What is RAG?
Large Language Models (LLMs) like GPT-4 are powerful, but they don't know your
private documents or the latest information. RAG solves this by:
  1. Ingestion: Reading your documents, cutting them into chunks, and saving
     them into a searchable Vector Database (This script: fill_db.py).
  2. Retrieval: Finding the most relevant chunks matching a user's question.
  3. Generation: Feeding those relevant chunks + the question to an LLM to
     produce an accurate, grounded answer (ask.py).

This script performs the INGESTION pipeline:
  PDF Files -> Load Text -> Split into Chunks -> Generate Embeddings -> Save to ChromaDB
=============================================================================
"""

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

# =============================================================================
# 1. Configuration & Storage Paths
# =============================================================================
# DATA_PATH: Directory where your raw PDF documents are placed.
DATA_PATH = r"data"

# CHROMA_PATH: Directory where ChromaDB stores its database files on disk.
# Keeping it on disk allows the embeddings to persist across program runs.
CHROMA_PATH = r"chroma_db"

# Initialize ChromaDB persistent client
# A "PersistentClient" saves the database to the local file system (CHROMA_PATH)
# instead of keeping it only in temporary memory (RAM).
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# A "Collection" in ChromaDB is like a table in SQL or a folder for documents.
# If the collection doesn't exist yet, it will create one; otherwise it loads it.
collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# =============================================================================
# 2. Loading the Documents
# =============================================================================
# PyPDFDirectoryLoader scans the specified folder (DATA_PATH) and extracts text
# from all PDF files inside it.
print("Loading PDF documents from folder...")
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()
print(f"Loaded {len(raw_documents)} raw document page(s).")

# =============================================================================
# 3. Splitting Documents into Smaller Chunks
# =============================================================================
# Why do we need chunking?
# 1. LLMs have context limits (token window).
# 2. Smaller, focused text chunks produce much more precise search results
#    than trying to match against an entire 50-page PDF at once.
#
# RecursiveCharacterTextSplitter splits text intelligently by trying:
# double newlines (paragraphs) -> single newlines -> spaces -> characters.
#
# Parameters:
# - chunk_size=300: Each chunk will have a maximum of ~300 characters.
# - chunk_overlap=100: Consecutive chunks share ~100 characters of overlap.
#   Why overlap? It ensures a sentence or idea is not abruptly cut in half
#   at the boundary, maintaining semantic context between adjacent chunks.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)
print(f"Split documents into {len(chunks)} text chunks.")

# =============================================================================
# 4. Preparing Data for ChromaDB
# =============================================================================
# ChromaDB requires:
# - documents: The actual text content of each chunk.
# - metadatas: Extra information (e.g., source file name, page number).
# - ids: A unique string identifier for each chunk so it can be indexed and updated.
documents = []
metadata = []
ids = []

i = 0
for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID" + str(i))
    metadata.append(chunk.metadata)
    i += 1

# =============================================================================
# 5. Storing and Indexing in ChromaDB (Upsert)
# =============================================================================
# What happens behind the scenes during "upsert"?
# 1. ChromaDB uses its default embedding model (e.g. all-MiniLM-L6-v2) to convert
#    each text chunk into a high-dimensional vector (list of numbers representing meaning).
# 2. It indexes both the text and vectors on disk for lightning-fast similarity search.
# 3. "upsert" inserts new records or updates existing ones if the ID already exists.
print(f"Adding/Updating {len(documents)} chunks in ChromaDB collection...")
collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)

print("Database successfully populated! You can now run ask.py to query it.")