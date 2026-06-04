# FinanceRAG

FinancerAg is a finance-focused retrieval and embedding project that ingests documents from `financerag/data`, converts them into LangChain documents, builds a FAISS vector store, and performs RAG-style queries.

## Project structure

- `data/`
  - `pdf/` — PDF documents used for ingestion
  - any supported document format under this folder is loaded recursively
- `src/`
  - `data_loader.py` — loads supported documents and converts them into LangChain documents
  - `embedding.py` — defines the embedding pipeline and chunking logic
  - `vectorstore.py` — builds, saves, loads, and queries a FAISS vector store
  - `search.py` — wraps vector search and Groq LLM summarization
- `faiss_store/` — persisted FAISS index and metadata after building the vector store
- `.env` — environment variables for API keys and credentials

## Supported document formats

- PDF
- TXT
- CSV
- Excel (`.xlsx`)
- Word (`.docx`)
- JSON

## Setup

1. Create and activate a Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install required packages:

```powershell
pip install langchain langchain-community sentence-transformers numpy faiss-cpu pymupdf python-dotenv langchain-groq
```

3. Create a `.env` file in `financerag/` and add your Groq API key:

```ini
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Load documents

Run the data loader to verify the supported files in `data/` can be loaded:

```powershell
python .\src\data_loader.py
```

### Build the FAISS vector store

Use the vector store script to embed documents and persist the index:

```powershell
python .\src\vectorstore.py
```

### Perform a search

Run the RAG search flow, which builds or loads the FAISS index and summarizes relevant results with Groq:

```powershell
python .\src\search.py
```

## Notes

- `search.py` uses `langchain_groq.ChatGroq` for query summarization.
- If the FAISS index files are not present, `search.py` attempts to rebuild the index from the `data/` folder.
- The current loader implementation is designed for finance documents and can be extended with additional file types.

## Troubleshooting

- If imports fail, confirm you are running the script from the `financerag` root and that the Python environment contains the required packages.
- If `GROQ_API_KEY` is missing, set it in `.env` and reload the environment.
