# FastAPI RAG

Ask a question about FastAPI and get an answer with links to the docs pages it came from.

## How it works

1. Your question is turned into an embedding vector.
2. The 8 closest pieces of the FastAPI docs are found in ChromaDB.
3. If the closest piece is too far (distance > 0.4), the system says there is no answer.
4. Otherwise Gemini answers using only those pieces and returns the sources it used.

## Results

- Retrieval hit-rate: 93% (top-8)
- Details and known problems: see [EVALUATION.md](EVALUATION.md)

## Run it

1. `pip install -r requirements.txt`
2. Create a `.env` file with your Gemini API key
3. Build the database: `scrapper.py`, then `chunker.py`, then `embed_and_store.py`
4. Start the server: `uvicorn main:app --reload`
5. Open http://127.0.0.1:8000/docs and try `POST /query`

## Files

- `scrapper.py`: downloads the docs pages
- `chunker.py`: cuts pages into pieces
- `embed_and_store.py`: makes embeddings and saves them in ChromaDB
- `retriever.py`: finds the closest pieces
- `gemini_test.py`: builds the prompt and asks Gemini
- `main.py`: API with the `/query` endpoint and logging
- `evaluate.py`: measures retrieval quality
- `test_api.py`: tests
 
## Limitations

- The search can find the wrong page if my words are different from the docs.
- Gemini answers can be slow when the service is busy.

Built with Python, FastAPI, ChromaDB, sentence-transformers and Gemini.
