# 🤖 Customer Support RAG Chatbot

A Retrieval-Augmented Generation (RAG) application that answers customer support questions using company documents. Instead of relying entirely on a language model's pre-trained knowledge, the chatbot retrieves relevant information from a custom knowledge base to provide more context-aware answers.

## 🚀 Overview

The **Customer Support RAG Chatbot** helps users find information from company documentation through a conversational interface. It processes documents, converts text into vector embeddings, retrieves relevant content using similarity search, and uses the retrieved context to generate answers.

### ✨ Key Features

- **Document-Based Question Answering:** Answer questions using company documentation.
- **Retrieval-Augmented Generation:** Retrieve relevant document chunks before generating responses.
- **Semantic Search:** Find relevant information based on meaning rather than exact keyword matches.
- **Vector Search with FAISS:** Efficiently search document embeddings.
- **Text Chunking:** Split large documents into smaller, searchable sections with overlapping context.
- **Interactive Chat Interface:** Ask questions through a Streamlit web application.
- **Local Development:** Run the application locally without requiring cloud deployment.

## 🏗️ Architecture

```text
Company Documents
       |
       v
Document Loading & Text Extraction
       |
       v
Text Chunking with Overlap
       |
       v
Embedding Generation
       |
       v
FAISS Vector Index
       |
       v
User Question
       |
       v
Question Embedding & Similarity Search
       |
       v
Relevant Document Chunks
       |
       v
LLM Response Generation
       |
       v
Final Answer in Chat Interface
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web interface |
| FAISS | Vector similarity search |
| Sentence Transformers | Text embedding generation |
| PyPDF | PDF text extraction |
| Ollama | Local LLM inference, if configured |
| Requests | HTTP communication with the LLM API |
| uv / pip | Python dependency management |

## 📂 Project Structure

```text
customer-support-rag-chatbot/
├── documents/             # Source company documents
├── src/
│   └── __init__.py        # Python package initialization
├── app.py                 # Streamlit user interface
├── chatbot.py             # RAG pipeline and answer generation
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock                # Locked dependency versions, if generated
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

*Adjust this structure to match your actual repository files.*

## ⚙️ Prerequisites

Before running the application, install:

- Python compatible with your project's dependencies
- Git
- uv, if you use it for dependency management
- Ollama and a supported model, if your chatbot uses a local LLM

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/adiityaa3/customer-support-rag-chatbot.git
cd customer-support-rag-chatbot
```

### 2. Create and activate a virtual environment

Using uv:

```bash
uv sync
```

Alternatively, using standard Python:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project's dependencies if you maintain a `requirements.txt` file:

```powershell
pip install -r requirements.txt
```

### 3. Prepare the documents

Place your supported company documents inside the `documents/` directory. For example:

- Product documentation
- Frequently asked questions (FAQs)
- Customer support guides
- Troubleshooting manuals
- Company policies

Use documents your application is configured to read.

### 4. Configure the language model

If your implementation uses Ollama, install and start Ollama, then download a supported model. For example:

```bash
ollama pull llama3.2
```

Ensure the model name and API endpoint in `chatbot.py` match your local configuration.

If you use a different LLM provider, configure that provider instead.

### 5. Run the application

Launch the Streamlit interface from the project root:

```bash
uv run streamlit run app.py
```

Or, if the dependencies are installed in your active virtual environment:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, typically:

`http://localhost:8501`

## 🧠 How RAG Works

1. **Ingestion:** Read and extract text from company documents.
2. **Chunking:** Split extracted text into smaller sections while preserving context through overlap.
3. **Embedding:** Convert each text chunk into a numerical vector using a sentence-transformer model.
4. **Indexing:** Store the vectors in a FAISS index for efficient retrieval.
5. **Retrieval:** Convert a user's question into an embedding and search for semantically similar chunks.
6. **Generation:** Supply the retrieved context and user question to the configured language model.
7. **Response:** Display the generated answer in the chat interface.

## 🔍 Example Use Case

**User:** What is the company's refund policy?

**RAG pipeline:**
- Searches the indexed company documentation.
- Retrieves the most relevant refund-policy sections.
- Passes those sections to the language model as context.

**Expected result:** A response based on the refund policy contained in the provided documents.

*The actual response depends on the documents you upload and the model you configure.*

## 🔧 Troubleshooting

### FAISS module not found

```bash
uv add faiss-cpu
```

Verify the installation:

```bash
uv run python -c "import faiss; print('FAISS is working')"
```

### Streamlit session-state warnings

Launch the app using:

```bash
uv run streamlit run app.py
```

Do not run a Streamlit application with `python app.py` when you want the web interface.

### Ollama connection errors

Check whether Ollama is running and verify that your configured model is available:

```bash
ollama list
```

If necessary, start the Ollama service using the method appropriate for your operating system.

## 🔐 Security and Privacy

- Do not commit API keys, passwords, or private company documents.
- Add `.env`, `.venv/`, `__pycache__/`, and generated index files to `.gitignore` as appropriate.
- Use only documents you are authorized to process.
- Review generated answers against source documents for important decisions.

## 🎯 Future Improvements

- Support additional document formats such as DOCX and TXT.
- Display source documents and relevant passages alongside answers.
- Add conversation history and improved session management.
- Introduce configurable retrieval parameters and similarity thresholds.
- Add evaluation tests for retrieval quality and answer relevance.
- Improve error handling and document-processing feedback.

