# mini-rag-app

This is a minimal implementaion of the RAG for question answering.

## Requirements

- Python 3.8 or later.

## Installation
### Setup the environment variables

```bash
$ pip install -r requirements.txt
```

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file like `OPENAI_API_KEY` value.

## Run the FastApi server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 
```

