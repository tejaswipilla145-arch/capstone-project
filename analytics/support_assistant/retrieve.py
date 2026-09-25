import chromadb
from sentence_transformers import SentenceTransformer


def main():
    print("Starting retrieval test...")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to the same persistent ChromaDB
    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Get the existing collection
    collection = chroma_client.get_collection(
        name="zepto_policies"
    )

    # User question
    question = "What is the refund policy?"

    # Convert question into an embedding
    question_embedding = model.encode(question).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    print()
    print("Question:")
    print(question)

    print()
    print("Retrieved documents:")

    for i, document in enumerate(results["documents"][0]):
        print()
        print(f"Document {i + 1}:")
        print(document)


if __name__ == "__main__":
    main()