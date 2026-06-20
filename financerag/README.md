# FinanceRAG Pipeline

A **Retrieval-Augmented Generation (RAG)** system for financial document analysis. The pipeline ingests financial documents, chunks and embeds them, indexes with FAISS, and exposes a Streamlit web UI for semantic search with AI-powered answers via Groq LLM.

## Overview

FinanceRAG lets you ask natural-language questions about financial documents and receive contextual, summarized answers powered by:

- **Multi-format Document Loading** (PDF, TXT, CSV, Excel, Word, JSON)
- **Advanced Chunking & Embeddings** (Sentence Transformers)
- **Vector Search** (FAISS - Facebook AI Similarity Search)
- **LLM Summarization** (Groq API for fast inference)
- **Streamlit Web UI** (interactive Q&A interface)

## Features

- **Multi-format Support**: Automatically loads and processes PDFs, Word docs, Excel sheets, CSVs, JSON, and text files
- **Semantic Search**: Finds relevant chunks using vector similarity, not keyword matching
- **Smart Chunking**: Recursive text splitting with overlap to preserve context
- **Fast Inference**: Groq LLM provides quick, cost-effective summarization
- **Persistent Storage**: FAISS index cached locally — rebuilt automatically only when missing
- **Web Interface**: Streamlit app with configurable top-k, source chunk viewer, and cache controls

## Project Structure

```
financerag/
├── data/                    # Input financial documents (all supported formats)
├── faiss_store/             # Persisted FAISS index and metadata
│   ├── faiss.index          # Serialized FAISS index
│   └── metadata.pkl         # Document metadata
├── src/
│   ├── data_loader.py       # Multi-format document loader
│   ├── embedding.py         # Embedding pipeline & chunking logic
│   ├── vectorstore.py       # FAISS vector store management
│   └── demo.py              # Streamlit app + RAGSearch class
├── .env                     # API keys (not committed)
└── README.md
```

## Supported Document Formats

| Format | Extension | Handler |
|--------|-----------|---------|
| PDF | `.pdf` | PyPDFLoader |
| Text | `.txt` | TextLoader |
| CSV | `.csv` | CSVLoader |
| Excel | `.xlsx`, `.xls` | UnstructuredExcelLoader |
| Word | `.docx` | Docx2txtLoader |
| JSON | `.json` | JSONLoader |

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Groq API Key ([get one free](https://console.groq.com))

### Installation

1. **Clone and navigate to the repo root:**
   ```bash
   git clone <repo-url>
   cd naiveRAG
   ```

2. **Install dependencies:**
   ```bash
   # with uv (recommended)
   uv sync

   # or with pip
   pip install -e .
   ```

3. **Configure environment variables:**
   Create a `.env` file in the `financerag/` directory:
   ```ini
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Usage

#### 1. Add your documents

Place financial documents in `financerag/data/`. All supported formats are picked up automatically on first run.

#### 2. Launch the Streamlit app

Run from the `financerag/` directory:

```bash
cd financerag
streamlit run src/demo.py
```

The app will:
- Detect whether a FAISS index exists in `faiss_store/`
- If missing, load documents from `data/`, embed them, and build the index automatically
- Open the web UI in your browser at `http://localhost:8501`

#### 3. Query your documents

Enter a natural-language question in the text area and click **Search**. The app retrieves the most relevant document chunks, sends them to the Groq LLM, and displays a summarized answer along with the raw source chunks.

#### 4. (Optional) Rebuild the index

Use the **Clear cache / reload index** button in the sidebar, or delete `faiss_store/` and relaunch:

```bash
rm -rf faiss_store/
streamlit run src/demo.py
```

## Configuration

### Embedding Model

Default: `all-MiniLM-L6-v2` (384-dimensional embeddings)

To switch models, change the `embedding_model` argument when instantiating `RAGSearch` in [src/demo.py](src/demo.py):

```python
rag = RAGSearch(embedding_model="sentence-transformers/all-mpnet-base-v2")
```

### Chunk Size & Overlap

Adjust in [src/embedding.py](src/embedding.py):

```python
emb_pipe = EmbeddingPipeline(chunk_size=1000, chunk_overlap=200)
```

### LLM Model

Change the Groq model in [src/demo.py](src/demo.py):

```python
RAGSearch(llm_model="mixtral-8x7b-32768")
```

Default is `groq/compound-mini`.

## Architecture

```
Financial Documents (data/)
        |
[Data Loader]  — PDF, TXT, CSV, Excel, Word, JSON
        |
[Text Chunking]  — RecursiveCharacterTextSplitter
        |
[Embeddings]  — SentenceTransformer (all-MiniLM-L6-v2)
        |
[FAISS Index]  — persisted to faiss_store/
        |
[Semantic Search]  — query → top-k similar chunks
        |
[LLM Summarization]  — Groq ChatGroq → answer
        |
[Streamlit UI]  — browser-based Q&A interface
```

## Troubleshooting

### Import Errors

```bash
# Run from the financerag/ directory so relative imports resolve
cd financerag
streamlit run src/demo.py
```

### Missing GROQ_API_KEY

```bash
# Verify .env exists and contains the key
cat financerag/.env

# Or export it directly (not recommended for production)
$env:GROQ_API_KEY = "your_key_here"   # Windows PowerShell
export GROQ_API_KEY="your_key_here"   # macOS/Linux
```

### No Documents Found

```bash
# Verify files are in financerag/data/
ls financerag/data/
# Debug output is printed when the loader runs — check the terminal
```

### FAISS Index Errors

```bash
# Delete and rebuild the index
rm -rf financerag/faiss_store/
streamlit run src/demo.py
```

## Dependencies

Managed via `pyproject.toml` (requires Python 3.13+):

- **langchain** / **langchain-community** — document loaders and LLM orchestration
- **sentence-transformers** — embedding model
- **faiss-cpu** — vector similarity search
- **pymupdf** / **pypdf** — PDF processing
- **python-dotenv** — environment variable management
- **langchain-groq** — Groq LLM integration
- **streamlit** — web UI

## Security Notes

- **Never commit `.env`** — it is listed in `.gitignore`
- **Keep API keys confidential** — rotate periodically
- **Use environment variables** — do not hardcode credentials in source files

## License

[Specify your license here — e.g., MIT, Apache 2.0]
