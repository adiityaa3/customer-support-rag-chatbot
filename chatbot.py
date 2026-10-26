
from pathlib import Path
import faiss
import numpy as np
import requests
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

DOCUMENTS_DIR = Path("documents")
MODEL_NAME = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

def load_documents():
    documents = []

    for path in DOCUMENTS_DIR.glob("*.txt"):
        documents.append(
            (path.name, path.read_text(encoding="utf-8"))
        )

    for path in DOCUMENTS_DIR.glob("*.pdf"):
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        documents.append((path.name, text))

    return documents


def chunk_text(text, chunk_size=180, overlap=40):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks


def build_index():
    documents = load_documents()
    chunks = []

    for filename, text in documents:
        for chunk in chunk_text(text):
            chunks.append({"source": filename, "text": chunk})

    if not chunks:
        raise RuntimeError(
            "No documents found. Add TXT or PDF files to documents/."
        )

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    vectors = embedding_model.encode(
        [chunk["text"] for chunk in chunks],
        normalize_embeddings=True
    )
    vectors = np.asarray(vectors, dtype="float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    return embedding_model, index, chunks


def answer_question(question, model, index, chunks):
    query_vector = model.encode(
        [question], normalize_embeddings=True
    )
    query_vector = np.asarray(query_vector, dtype="float32")

    scores, ids = index.search(
        query_vector, min(3, len(chunks))
    )

    context_parts = []

    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue

        item = chunks[idx]
        context_parts.append(
            f"Source: {item['source']}\n{item['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a helpful customer support assistant.

Answer using only the supplied company-document context.
If the answer is not in the context, say:
"I couldn't find that information in the company documents."
Do not invent policies, prices, or promises.

Company-document context:
{context}

Customer question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()

    answer = response.json()["response"]

    sources = sorted({
        chunks[idx]["source"]
        for idx in ids[0]
        if idx >= 0
    })

    return answer, sources


if __name__ == "__main__":
    print("Loading documents and building the search index...")
    model, index, chunks = build_index()
    print(f"Ready! Indexed {len(chunks)} chunks.")

    while True:
        question = input("\nCustomer: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            answer, sources = answer_question(
                question, model, index, chunks
            )
            print(f"\nAssistant: {answer}")
            print(f"Sources: {', '.join(sources)}")

        except requests.RequestException as error:
            print(f"Could not contact Ollama: {error}")
