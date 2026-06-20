import os
import sys
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Ensure src directory is on the path when running via `streamlit run`
sys.path.insert(0, os.path.dirname(__file__))

from vectorstore import FaissVectorStore
from langchain_groq import ChatGroq


class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "groq/compound-mini",
    ):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()

        groq_api_key = os.environ.get("GROQ_API_KEY", "")
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)

    def search_and_summarize(self, query: str, top_k: int = 5) -> tuple[str, list[dict]]:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found.", []
        prompt = (
            f"Summarize the following context for the query: '{query}'\n\n"
            f"Context:\n{context}\n\nSummary:"
        )
        response = self.llm.invoke([prompt])
        return response.content, results


# ── Streamlit App ──────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading RAG pipeline...")
def get_rag(persist_dir: str, llm_model: str) -> RAGSearch:
    return RAGSearch(persist_dir=persist_dir, llm_model=llm_model)


def main():
    st.set_page_config(
        page_title="FinanceRAG",
        page_icon="💹",
        layout="wide",
    )

    st.title("💹 FinanceRAG — Document Q&A")
    st.caption("Ask questions about your financial documents powered by FAISS + Groq LLM.")

    # ── Sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("Settings")
        persist_dir = st.text_input("Vector store path", value="faiss_store")
        llm_model = "groq/compound-mini"
        st.info(f"Model: `{llm_model}`")
        top_k = st.slider("Retrieved chunks (top-k)", min_value=1, max_value=10, value=5)
        show_sources = st.checkbox("Show source chunks", value=True)

        st.divider()
        if st.button("Clear cache / reload index"):
            st.cache_resource.clear()
            st.rerun()

    # ── Main area ──────────────────────────────────────────────────────────────
    with st.form("query_form"):
        query = st.text_area(
            "Your question",
            placeholder="e.g. What are trade debts?",
            height=100,
        )
        submitted = st.form_submit_button("Search", use_container_width=True, type="primary")

    if submitted:
        query = query.strip()
        if not query:
            st.warning("Please enter a question before searching.")
            st.stop()

        try:
            rag = get_rag(persist_dir, llm_model)
        except Exception as e:
            st.error(f"Failed to initialise RAG pipeline: {e}")
            st.stop()

        with st.spinner("Searching and generating answer..."):
            try:
                answer, sources = rag.search_and_summarize(query, top_k=top_k)
            except Exception as e:
                st.error(f"Query failed: {e}")
                st.stop()

        st.subheader("Answer")
        st.write(answer)

        if show_sources and sources:
            st.subheader("Source Chunks")
            for i, src in enumerate(sources, 1):
                text = src.get("metadata", {}).get("text", "") if src.get("metadata") else ""
                dist = src.get("distance", 0)
                with st.expander(f"Chunk {i}  —  distance: {dist:.4f}"):
                    st.write(text or "_No text available_")


if __name__ == "__main__":
    main()
