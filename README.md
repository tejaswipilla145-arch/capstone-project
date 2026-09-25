\# Zepto AI/ML Capstone Project



&#x20;Project Overview



This project contains three modules developed as part of the Zepto AI/ML capstone project:



1\. \*\*Data Pipeline\*\* – Scrapes book data, cleans it, stores it in SQLite, and performs SQL and pandas analysis.

2\. \*\*Analytics\*\* – Performs exploratory data analysis and machine learning analysis using the Titanic dataset.

3\. \*\*Support Assistant\*\* – A Retrieval-Augmented Generation (RAG) based customer support assistant that retrieves relevant Zepto policy documents and uses an LLM to answer user questions.



\---



&#x20;Project Structure



```text

capstone-project/

│

├── data\_pipeline/

│   └── scraper.py

│

├── analytics/

│   ├── 01\_eda.ipynb

│   ├── 02\_modeling.ipynb

│   ├── titanic.csv

│   └── support\_assistant/

│       ├── Dockerfile

│       ├── README.md

│       ├── ingest.py

│       ├── retrieve.py

│       ├── main.py

│       ├── requirements.txt

│       └── docs/

│           ├── doc\_01.txt

│           ├── doc\_02.txt

│           ├── doc\_03.txt

│           ├── doc\_04.txt

│           ├── doc\_05.txt

│           ├── doc\_06.txt

│           ├── doc\_07.txt

│           └── doc\_08.txt

│

├── books.db

├── requirements.txt

└── README.md

```



\---



\# 1. Data Pipeline



&#x20;Objective



The data pipeline collects book information from the public practice website `books.toscrape.com`.



The pipeline uses Python to scrape, clean, transform, store, and analyze the data.



\## Technologies Used



\* Python

\* Requests

\* BeautifulSoup

\* pandas

\* SQLite



\## Main Steps



\### Scraping



`requests` is used to download the web pages and `BeautifulSoup` is used to extract:



\* Book title

\* Price in GBP

\* Star rating

\* Availability

\* Category



&#x20;Data Cleaning



The scraped data is cleaned by:



\* Removing the GBP currency symbol

\* Converting prices into numeric values

\* Converting rating words into numbers from 1 to 5

\* Converting availability into True/False

\* Handling missing or invalid values



&#x20;Currency Conversion



A fixed conversion rate is used:



```text

1 GBP = 105.50 INR

```



The INR price is calculated from the GBP price.



&#x20;SQLite Database



The cleaned data is stored in SQLite.



The database contains:



\* `categories` table

\* `books` table



The `books` table uses a foreign key to connect books with their categories.



&#x20;SQL and pandas Analysis



SQL queries are used for:



\* SELECT

\* WHERE

\* ORDER BY

\* LIMIT

\* DISTINCT

\* BETWEEN

\* JOIN



The results are also read into pandas DataFrames using `pd.read\_sql`.



`pd.merge()` is used to reproduce the SQL JOIN operation and compare the results.



\## Run



From the project root:



```bash

python data\_pipeline/scraper.py

```



\---



&#x20;2. Analytics



&#x20;Objective



The analytics module performs exploratory data analysis and machine learning using the Titanic dataset.



&#x20;Files



```text

analytics/

├── 01\_eda.ipynb

├── 02\_modeling.ipynb

└── titanic.csv

```



\### EDA



The EDA notebook is used to explore the dataset, understand the variables, check missing values, and visualize the data.



\### Modeling



The modeling notebook contains machine learning analysis using the Titanic dataset.



\## Run



Open the notebooks using Jupyter Notebook or JupyterLab:



```bash

jupyter notebook

```



Then open:



```text

analytics/01\_eda.ipynb

analytics/02\_modeling.ipynb

```



\---



\# 3. Support Assistant



\## Objective



The support assistant is a Retrieval-Augmented Generation (RAG) application.



It answers customer support questions using Zepto policy documents.



Instead of directly asking the LLM to answer a question, the application first retrieves relevant policy documents and then provides those documents as context to the LLM.



\## Technologies Used



\* Python

\* Sentence Transformers

\* ChromaDB

\* Groq API

\* Docker



\## RAG Flow



```text

Policy Documents

&#x20;      ↓

Sentence Transformer

&#x20;      ↓

Embeddings

&#x20;      ↓

ChromaDB

&#x20;      ↓

User Question

&#x20;      ↓

Question Embedding

&#x20;      ↓

Retrieve Top 3 Relevant Documents

&#x20;      ↓

Groq LLM

&#x20;      ↓

Final Answer

```



\## Main Files



\### `ingest.py`



Reads the policy documents from the `docs` folder.



Each document is converted into an embedding using:



```text

all-MiniLM-L6-v2

```



The documents and embeddings are stored in ChromaDB.



\### `retrieve.py`



Tests the retrieval process.



A user question is converted into an embedding and the top 3 relevant policy documents are retrieved.



\### `main.py`



Runs the complete RAG assistant.



It:



1\. Accepts a user question.

2\. Creates an embedding for the question.

3\. Retrieves the top 3 relevant documents.

4\. Creates a prompt using the retrieved documents.

5\. Sends the prompt to the Groq LLM.

6\. Displays the answer.



The assistant is instructed to use only the retrieved policy information and not make up information.



\## Run Locally



Go to the support assistant folder:



```bash

cd analytics/support\_assistant

```



Install the required libraries:



```bash

pip install -r requirements.txt

```



Set the Groq API key as an environment variable.



On PowerShell:



```powershell

$env:GROQ\_API\_KEY="your\_api\_key"

```



Run ingestion:



```bash

python ingest.py

```



Test retrieval:



```bash

python retrieve.py

```



Run the RAG assistant:



```bash

python main.py

```



Type:



```text

exit

```



to stop the assistant.



\## Docker



The support assistant also includes a Dockerfile.



Build the Docker image:



```bash

docker build -t zepto-support-assistant .

```



Run the container:



```powershell

docker run -it --rm -e GROQ\_API\_KEY="$env:GROQ\_API\_KEY" zepto-support-assistant

```



The API key is passed through an environment variable instead of being stored directly in the source code.



\---



\# Requirements



The project uses a \*\*consolidated requirements approach\*\*.



The root `requirements.txt` contains the Python dependencies required for the main project modules, while the support assistant has its own `requirements.txt` because it has additional RAG-specific dependencies.



\---



\# Design Decisions



\### Data Pipeline



\* `requests` and `BeautifulSoup` are used for web scraping.

\* SQLite is used as a lightweight relational database.

\* A fixed GBP-to-INR conversion rate is used as required for the benchmark.

\* Both SQL and pandas operations are demonstrated.



\### Analytics



\* Separate notebooks are used for EDA and modeling so that data exploration and machine learning steps are easier to follow.



\### Support Assistant



\* Sentence Transformers are used to create semantic embeddings.

\* ChromaDB is used for vector storage and similarity search.

\* Top 3 relevant documents are retrieved for each question.

\* The LLM receives the retrieved policy documents as context.

\* The application instructs the LLM not to invent information.

\* Docker is used to package the support assistant and make the application easier to run consistently.

\* The Groq API key is supplied through an environment variable instead of being hard-coded.



\---



\# End-to-End Execution



The three modules can be run independently.



\### Data Pipeline



```bash

python data\_pipeline/scraper.py

```



\### Analytics



Open:



```text

analytics/01\_eda.ipynb

analytics/02\_modeling.ipynb

```



\### Support Assistant



```bash

cd analytics/support\_assistant

python ingest.py

python retrieve.py

python main.py

```



For Docker:



```powershell

docker build -t zepto-support-assistant .

docker run -it --rm -e GROQ\_API\_KEY="$env:GROQ\_API\_KEY" zepto-support-assistant

```



\---



\# Conclusion



This project demonstrates a complete workflow covering web scraping and data pipelines, data analysis and machine learning, and a RAG-based AI support assistant.



The support assistant combines document embeddings, vector search, and an LLM to provide answers based on the available Zepto policy documents.



