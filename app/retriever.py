import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

FAISS_INDEX_PATH = DATA_DIR / "faiss.index"

METADATA_PATH = DATA_DIR / "metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# retriever class create
class Retriever:
    """
    Semantic Retriever for SHL Assessments.
    """

    def __init__(self):

        self.model = self._load_model()

        self.index = self._load_faiss_index()

        self.metadata = self._load_metadata()

    # load model 
    def _load_model(self):
        """
        Load Sentence Transformer model.
        """

        print("Loading embedding model...")

        model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded.")

        return model
    
    #load faiss
    def _load_faiss_index(self):
        """
        Load FAISS vector index.
        """

        print("Loading FAISS index...")

        index = faiss.read_index(str(FAISS_INDEX_PATH))

        print(f"Loaded {index.ntotal} vectors.")

        return index
    
    #load metadata
    def _load_metadata(self):
        """
        Load assessment metadata.
        """

        print("Loading metadata...")

        with open(METADATA_PATH, "r", encoding="utf-8") as file:

            metadata = json.load(file)

        print(f"Loaded {len(metadata)} metadata entries.")

        return metadata
   
    # embed_query for 1 query not all 
    def embed_query(self, query: str):
        """
        Convert a user query into a vector embedding.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        embedding = embedding.astype(np.float32)

        embedding = embedding.reshape(1, -1) # done for faiss req: (number_of_vectors, dimensions) so if only have ONE vector (384,) -> (1, 384)

        return embedding
    
    # Retrieve Similar Assessments
    def retrieve(self, query: str, top_k: int = 10):
        """
        Retrieve the most relevant SHL assessments.
        """

        query_embedding = self.embed_query(query)

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results
    

if __name__ == "__main__":

    retriever = Retriever()

    query = "Graduate financial analyst"

    results = retriever.retrieve(query, top_k=5)

    print("\nTop Results:\n")

    for i, result in enumerate(results, start=1):

        print(f"{i}. {result['name']}")
        print(f"   URL: {result['url']}")
        print(f"   Categories: {', '.join(result['categories'])}")
        print(f"   Duration: {result['duration']}")
        print()
    
     