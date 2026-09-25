 Support Assistant – Code Description

I created a Zepto customer support chatbot using 1. Documents

First, I created a `docs` folder and added Zepto policy documents in `.txt` format.

These documents contain information about refunds, cancellations, missing items, damaged items, and other policies.

 2. `ingest.py`

I used `ingest.py` to read all the policy documents.

First, I loaded the `SentenceTransformer` model. It converts the text into embeddings, which are numbers representing the meaning of the text.

Then I used ChromaDB to store the documents and their embeddings.

I used `PersistentClient` so that the data is saved in the `chroma_db` folder and can be used later.

After running `ingest.py`, all 8 policy documents were stored in ChromaDB.

 3. `retrieve.py`

I used `retrieve.py` to test whether I could find the correct policy documents.

I gave a question like:

`What is the refund policy?`

The question was converted into an embedding and searched in ChromaDB.

ChromaDB returned the top 3 documents that were most relevant to the question.

 4. `main.py`

I used `main.py` to create the actual chatbot.

First, the user enters a question.

The question is converted into an embedding using SentenceTransformer.

Then the embedding is searched in ChromaDB to find the relevant policy documents.

The retrieved documents are added to the prompt along with the user's question.

I then sent this prompt to the Groq LLM.

The Groq model generates the final answer using the retrieved policy information.

I also added a condition that tells the model not to make up information if the answer is not available in the policies.

The chatbot continues asking questions until the user types `exit`.

 5. Docker

Finally, I created a `Dockerfile` to run the application inside a Docker container.

I installed the required Python packages, copied the project files into the container, and started the chatbot using `main.py`.

I passed the `GROQ_API_KEY` through an environment variable instead of writing the API key directly in the code.

 Overall Flow

The complete process is:

`Policy Documents → Embeddings → ChromaDB → User Question → Retrieve Relevant Policies → Groq LLM → Final Answer`

This helped me build a simple RAG-based customer support assistant.
