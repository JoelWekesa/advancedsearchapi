This is a search API powered by FastAPI, Langchain, HuggingFace, and PGVector

## Getting Started


First, run the vector database with docker

```bash
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16

```


Then create a virtual env

```bash
python3 -m venv env #Check how to create virtual env for windows

```

Then activate the environment

```bash

source env/bin/activate

```

Then install the dependencies

```bash
pip install -r requirements.txt

```

Then create a .env file at the root of your project and replace the values in .env.example with actual values

```bash
touch .env
```

Then run the development server

```bash
fastapi dev main.py --port 9000

```

