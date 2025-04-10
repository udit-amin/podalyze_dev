from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import os

DB_DIR = "./vectors"
embeddings = OpenAIEmbeddings()

def store_segments(segments, episode_id):
    texts, metadatas = [], []
    for s in segments:
        text = f"{s['speaker']}: {s['text']}"
        meta = {"speaker": s["speaker"], "start": s["start"], "end": s["end"], "episode_id": episode_id}
        texts.append(text)
        metadatas.append(meta)

    db = FAISS.from_texts(texts, embeddings, metadatas)
    db.save_local(os.path.join(DB_DIR, episode_id))

def ask_about_episode(episode_id, question):
    db = FAISS.load_local(os.path.join(DB_DIR, episode_id), embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=db.as_retriever())
    return qa.run(question)

def summarize_episode_transcript(episode_id):
    db = FAISS.load_local(os.path.join(DB_DIR, episode_id), embeddings)
    docs = [Document(page_content=doc.page_content) for doc in db.similarity_search(" ", k=100)]
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    chain = load_summarize_chain(OpenAI(), chain_type="map_reduce")
    return chain.run(chunks)
