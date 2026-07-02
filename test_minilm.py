from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")

text = "Java developer with Spring Boot"

embedding = model.encode(text)

print(f"Embedding Dimension: {len(embedding)}")

print(embedding[:10])