# FinanceRAG Pipeline

A production-ready **Retrieval-Augmented Generation (RAG)** system designed for finance document analysis. This pipeline ingests financial documents, converts them to embeddings, indexes them with FAISS, and performs intelligent semantic search with AI-powered summarization using Groq LLM.

## 🎯 Overview

FinanceRAG enables users to ask complex questions about financial documents and receive contextual, summarized answers powered by:
- **Multi-format Document Loading** (PDF, TXT, CSV, Excel, Word, JSON)
- **Advanced Chunking & Embeddings** (Sentence Transformers)
- **Vector Search** (FAISS - Facebook AI Similarity Search)
- **LLM Summarization** (Groq API for fast inference)

## ✨ Features

- 📄 **Multi-format Support**: Automatically loads and processes PDFs, Word docs, Excel sheets, CSVs, JSON, and text files
- 🔍 **Semantic Search**: Find relevant documents using semantic similarity, not keyword matching
- 📊 **Smart Chunking**: Recursive text splitting with overlap to preserve context
- ⚡ **Fast Inference**: Groq LLM provides quick, cost-effective summarization
- 💾 **Persistent Storage**: FAISS index cached locally for fast repeated queries
- 🔧 **Scalable Architecture**: Modular design for easy extension and customization

## 🏗️ Project Structure

```
financerag/
├── data/                    # Input financial documents (all supported formats)
│   └── pdf/                # Example: Place PDFs here
├── faiss_store/            # Persisted FAISS index and metadata
│   ├── faiss.index         # Serialized FAISS index
│   └── metadata.pkl        # Document metadata
├── src/
│   ├── data_loader.py      # Multi-format document loader
│   ├── embedding.py        # Embedding pipeline & chunking logic
│   ├── vectorstore.py      # FAISS vector store management
│   └── search.py           # RAG search with Groq LLM summarization
└── README.md               # This file
```

## 📋 Supported Document Formats

| Format | Extension | Handler |
|--------|-----------|---------|
| PDF | `.pdf` | PyPDFLoader |
| Text | `.txt` | TextLoader |
| CSV | `.csv` | CSVLoader |
| Excel | `.xlsx`, `.xls` | UnstructuredExcelLoader |
| Word | `.docx` | Docx2txtLoader |
| JSON | `.json` | JSONLoader |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one free](https://console.groq.com))

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd financerag
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the `financerag/` directory:
   ```ini
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Basic Usage

#### 1. Prepare Your Data
Place financial documents in the `data/` directory. Supported formats include PDFs, CSVs, Word docs, etc.

#### 2. Load and Verify Documents
```bash
python src/data_loader.py
```
This will scan the `data/` directory and display loaded documents.

#### 3. Build FAISS Vector Store
```bash
python src/vectorstore.py
```
This creates embeddings for all documents and saves the index to `faiss_store/`.

#### 4. Query with RAG
```bash
python src/search.py
```
Perform semantic search and get AI-summarized answers. Modify the query in `search.py`:
```python
query = "What are the company's total assets?"
summary = rag_search.search_and_summarize(query, top_k=5)
print("Answer:", summary)
```

## 🔧 Configuration

### Embedding Model
Default: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- Lightweight and fast
- Good balance of performance and speed

To use a different model, modify [src/embedding.py](src/embedding.py):
```python
emb_pipe = EmbeddingPipeline(model_name="sentence-transformers/all-mpnet-base-v2")
```

### Chunk Size & Overlap
Adjust document chunking in [src/embedding.py](src/embedding.py):
```python
emb_pipe = EmbeddingPipeline(chunk_size=1000, chunk_overlap=200)
```

### LLM Model
Change the Groq model in [src/search.py](src/search.py):
```python
self.llm = ChatGroq(model_name="mixtral-8x7b-32768")  # Default is groq/compound-mini
```

## 📚 Architecture

```
Financial Documents
        ↓
[Data Loader] ← Supports: PDF, TXT, CSV, Excel, Word, JSON
        ↓
[Text Chunking] ← RecursiveCharacterTextSplitter
        ↓
[Embeddings] ← SentenceTransformer (all-MiniLM-L6-v2)
        ↓
[FAISS Index] ← Persisted locally for fast retrieval
        ↓
[Semantic Search] ← User query → Find top-k similar chunks
        ↓
[LLM Summarization] ← Groq ChatGroq → Contextual answer
        ↓
Result to User
```

## 🐛 Troubleshooting

### Import Errors
```bash
# Ensure you're running from the financerag directory
cd financerag

# Verify all dependencies are installed
pip install -r ../requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Missing GROQ_API_KEY
```bash
# Verify .env file exists and contains the key
cat .env

# Or set it directly in the terminal (not recommended for production)
$env:GROQ_API_KEY = "your_key_here"  # Windows PowerShell
```

### No Documents Found
```bash
# Check data directory
ls data/

# Ensure files are in supported formats
# Verify recursive loading with debug output in data_loader.py
```

### Slow Embeddings
- Use CPU-optimized model: `all-MiniLM-L6-v2`
- Reduce chunk size in `embedding.py`
- Use GPU if available with `sentence-transformers`

### FAISS Index Errors
```bash
# Clear old index to rebuild from scratch
rm -r faiss_store/

# Rebuild index
python src/vectorstore.py
```

## 📦 Dependencies

- **langchain** & **langchain-community** - LLM orchestration framework
- **sentence-transformers** - Embedding model
- **faiss-cpu** - Vector similarity search
- **pymupdf** - PDF processing
- **python-dotenv** - Environment variable management
- **langchain-groq** - Groq LLM integration

Full list in [../requirements.txt](../requirements.txt)

## 🔐 Security Notes

- **Never commit `.env` file** - Add to `.gitignore`
- **Keep API keys confidential** - Rotate keys periodically
- **Use environment variables** - Don't hardcode credentials in code

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Submit a pull request

## 📄 License

[Specify your license here - e.g., MIT, Apache 2.0, etc.]

## 📧 Support

For questions, issues, or suggestions, please open an issue on GitHub or contact the maintainers.

---

**Last Updated:** June 2026  
**Repository:** [FinanceRAG_Pipeline](https://github.com/aiengineer1992-wq/FinanceRAG_Pipeline)
