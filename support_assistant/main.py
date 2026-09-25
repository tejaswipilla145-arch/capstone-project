import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq


def main():
    print("Starting RAG assistant...")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to persistent ChromaDB
    chroma_client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Get existing collection
    collection = chroma_client.get_collection(
        name="zepto_policies"
    )

    # Get Groq API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("GROQ_API_KEY is not set!")
        return

    # Create Groq client
    client = Groq(api_key=api_key)

    print()
    print("RAG assistant is ready!")
    print("Type 'exit' to stop.")

    # Continuous question loop
    while True:

        question = input("\nAsk your question: ")

        # Exit condition
        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Ignore empty questions
        if not question.strip():
            print("Please enter a question.")
            continue

        # Convert question into embedding
        question_embedding = model.encode(question).tolist()

        # Retrieve top 3 relevant documents
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=3
        )

        documents = results["documents"][0]

        # Combine retrieved documents
        context = "\n\n".join(documents)

        # Create RAG prompt
        prompt = f"""
You are a helpful Zepto customer support assistant.

Answer the user's question using only the information
provided in the context below.

Do not make up information.

If the answer is not available in the context, say:
"I don't have enough information in the provided policies."

Context:
{context}

User question:
{question}
"""

        # Send request to Groq
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        # Get answer
        answer = response.choices[0].message.content

        print()
        print("Assistant:")
        print(answer)


if __name__ == "__main__":
    main()