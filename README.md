# 📄 Document Q&A Bot (RAG)

A Retrieval-Augmented Generation (RAG) application that lets you upload any PDF and ask natural-language questions about it. The bot retrieves the most relevant sections of the document and uses an LLM to generate accurate, grounded answers — with source citations.

## How it works

1. **Upload** — A PDF is uploaded through the Streamlit interface.
2. **Extract & chunk** — Text is extracted from the PDF and split into overlapping chunks to preserve context across boundaries.
3. **Embed & store** — Each chunk is converted into a vector embedding and stored in a ChromaDB vector database.
4. **Query** — When a question is asked, it's embedded and compared against stored chunks to retrieve the most relevant ones.
5. **Generate** — The retrieved chunks are passed as context to an LLM (Llama 3.3 via Groq), which generates a grounded answer based only on the document content.

## Tech stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| PDF parsing | pypdf |
| Vector database | ChromaDB |
| LLM inference | Groq (Llama 3.3 70B) |
| Frontend | Streamlit |

## Project structure

```
rag-bot/
├── main.py          # FastAPI backend — upload, chunking, embedding, retrieval, generation
├── app.py           # Streamlit frontend
├── .env.example      # Template for required environment variables
└── requirements.txt  # Python dependencies
```

## Running locally

**1. Clone the repo**
```bash
git clone https://github.com/ShaikSulthan-dev/rag-document-qa-bot.git
cd rag-document-qa-bot
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

**3. Set up your API key**

Copy `.env.example` to `.env` and add your free Groq API key (get one at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_actual_key_here
```

**4. Start the backend**
```bash
uvicorn main:app --reload
```

**5. Start the frontend** (in a separate terminal)
```bash
streamlit run app.py
```

The app will open in your browser. Upload a PDF, wait for it to process, then ask questions about it.

## Example

Upload a resume PDF and ask: *"What is this person's experience with quality assurance?"*

The bot retrieves the relevant resume sections and generates a concise, grounded summary — along with the exact source chunks it used to answer.

## Future improvements

- Support multiple documents in a single session
- Persistent vector storage (currently in-memory, resets on restart)
- Conversation history / multi-turn follow-up questions
- Swap in Claude API for generation
