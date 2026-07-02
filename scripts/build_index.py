import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

#Project 
ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

DOCUMENTS_PATH = DATA_DIR / "documents.json"

EMBEDDINGS_PATH = DATA_DIR / "embeddings.npy"

FAISS_INDEX_PATH = DATA_DIR / "faiss.index"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

#Load Doc
def load_documents():
    """
    Load retrieval documents from JSON.
    """

    print("Loading documents...")

    with open(DOCUMENTS_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    print(f"Loaded {len(documents)} documents.")

    return documents

#Load MiniLM
def load_model():
    """
    Load Sentence Transformer model.
    """

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Model loaded successfully.")

    return model

# create embeddings
def generate_embeddings(model, documents):
    """
    Generate vector embeddings for all documents.
    """

    print("Generating embeddings...")

    texts =  documents

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype(np.float32)

    print(f"Generated {len(embeddings)} embeddings.")
    print(f"Embedding dimension: {embeddings.shape[1]}")

    return embeddings

#save embeddings
def save_embeddings(embeddings):
    """
    Save embeddings as a NumPy file.
    """

    print("Saving embeddings...")

    np.save(EMBEDDINGS_PATH, embeddings)

    print(f"Embeddings saved to {EMBEDDINGS_PATH}")

#build faiss index
def build_faiss_index(embeddings):
    """
    Build FAISS vector index.
    """

    print("Building FAISS index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print(f"Indexed {index.ntotal} documents.")

    return index

#save faiss
def save_index(index):
    """
    Save FAISS index.
    """

    print("Saving FAISS index...")

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    print(f"Index saved to {FAISS_INDEX_PATH}")  


def main():
    """
    Build the complete FAISS index.
    """

    documents = load_documents()

    model = load_model()

    embeddings = generate_embeddings(model, documents)

    save_embeddings(embeddings)

    index = build_faiss_index(embeddings)

    save_index(index)

    print("\n✅ Build completed successfully!")


if __name__ == "__main__":
    main()