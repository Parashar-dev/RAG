"""
=============================================================================
RAG (Retrieval-Augmented Generation) Tutorial - Step 2: Query & Generation
=============================================================================
How does this script work?
This script executes the two final phases of RAG:

  1. RETRIEVAL (ChromaDB Vector Search):
     - The user asks a natural language question.
     - ChromaDB converts the question into a vector embedding.
     - It performs a semantic similarity search to find the top matching
       document chunks that were previously indexed by fill_db.py.

  2. AUGMENTATION & GENERATION (OpenAI GPT-4o):
     - Augmentation: We take the retrieved text chunks and inject them directly
       into the system prompt as "context / knowledge".
     - Generation: We instruct the LLM (GPT-4o) to answer the user's question
       strictly using the provided context, preventing hallucinations.
=============================================================================
"""

import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# =============================================================================
# 1. Environment & API Key Configuration
# =============================================================================
# load_dotenv() reads the .env file in the project root and sets environment
# variables such as OPENROUTER_API_KEY or OPENAI_API_KEY.
load_dotenv()

# =============================================================================
# 2. Connecting to the Existing Vector Database
# =============================================================================
# Paths must match what was used in fill_db.py
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# Open the persistent database saved on disk
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Access the collection where our document chunks are stored
collection = chroma_client.get_or_create_collection(name="growing_vegetables")

# =============================================================================
# 3. User Input (The Question)
# =============================================================================
user_query = input("What do you want to know about growing vegetables?\n\n")

# =============================================================================
# 4. Phase 1 of RAG: Retrieval (Semantic Search)
# =============================================================================
# How does query() work?
# 1. ChromaDB embeds the user_query using the same model that embedded the documents.
# 2. It calculates semantic similarity (e.g., cosine distance) between the query
#    vector and all chunk vectors in the collection.
# 3. n_results=4: Retrieves the top 4 closest (most relevant) document chunks.
results = collection.query(
    query_texts=[user_query],
    n_results=4
)

# Print the retrieved documents to the console so students can inspect
# exactly what knowledge was fetched before sending it to the LLM.
print("\n--- Retrieved Knowledge Chunks ---")
print(results['documents'])
# print(results['metadatas'])  # Optional: inspect source file names / page numbers

# =============================================================================
# 5. Phase 2 of RAG: Augmentation (Constructing the Prompt)
# =============================================================================
# Initialize client (supports both OpenRouter and standard OpenAI)
openrouter_key = os.getenv("OPENROUTER_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if openrouter_key:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_key,
    )
    # Default to a strong, cost-effective OpenRouter model or whatever is set in .env
    model = os.getenv("LLM_MODEL") or os.getenv("OPENROUTER_MODEL") or "meta-llama/llama-3.3-70b-instruct"
elif openai_key:
    client = OpenAI(api_key=openai_key)
    model = os.getenv("LLM_MODEL", "gpt-4o")
else:
    raise ValueError(
        "No API key found! Please set OPENROUTER_API_KEY or OPENAI_API_KEY in your .env file."
    )

# "Prompt Augmentation" is the core concept of RAG:
# We build a strict prompt containing:
#   a) System Instructions / Persona: Define the role and guardrails.
#   b) Grounding Rule: Explicitly instruct the model NOT to hallucinate or make
#      things up, and only use the provided knowledge.
#   c) The Retrieved Data: Insert the exact text chunks found by ChromaDB.
system_prompt = f"""
You are a helpful assistant. You answer questions about growing vegetables in Florida. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make things up.
If you don't know the answer, just say: I don't know
--------------------
The data:
{str(results['documents'])}
"""

# print(system_prompt)  # Optional: inspect the full augmented prompt

# =============================================================================
# 6. Phase 3 of RAG: Generation (Calling LLM with Context)
# =============================================================================
# We pass both the system prompt (containing the retrieved context and rules)
# and the user's original query. The chosen model synthesizes the final coherent answer.
print(f"\nGenerating answer using model: {model}...")
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}    
    ]
)

# =============================================================================
# 7. Output the Final Answer
# =============================================================================
print("\n\n------------------- Final AI Answer ------------------\n\n")
print(response.choices[0].message.content)