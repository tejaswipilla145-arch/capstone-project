from sentence_transformers import SentenceTransformer
import chromadb
import os


def main():
    print("Starting ingestion...")

    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Embedding model loaded!")

    
    chroma_client = chromadb.Client()

    
    collection = chroma_client.get_or_create_collection(
        name="zepto_policies"
    )

    
    docs_folder = "docs"

    # Check whether docs folder exists
    if not os.path.exists(docs_folder):
        print("docs folder not found!")
        return

    count = 0

    
    for filename in os.listdir(docs_folder):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(docs_folder, filename)

        print(f" Reading: {filename}")

        
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()

        
        except UnicodeDecodeError:
            print(f" {filename} is not UTF-8. Trying UTF-16...")

            with open(filepath, "r", encoding="utf-16") as file:
                text = file.read()

        
        if not text.strip():
            print(f" Skipping empty file: {filename}")
            continue

        
        embedding = model.encode(text).tolist()

        
        doc_id = filename.replace(".txt", "")

        
        collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding]
        )

        count += 1

        print(f"✅ Added: {filename}")

    print()
    print("✅ All documents embedded and stored in ChromaDB!")
    print("Final count:", collection.count())


if __name__ == "__main__":
    main()

