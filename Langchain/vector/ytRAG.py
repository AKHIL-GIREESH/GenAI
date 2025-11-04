from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


video_id = 'Yq9NtTS90AE'
try:
    ytApiObj = YouTubeTranscriptApi()
    transcript_list = ytApiObj.fetch(video_id, languages=["en"])
    transcript = " ".join(i.text for i in transcript_list)
    print(len(transcript))
except TranscriptsDisabled:
    print("No captions available for the video")


splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=200)
chunks = splitter.create_documents([transcript])

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(chunks, embeddings)
vector_store.index_to_docstore_id
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)

question          = "anything about raspberry pi mentioned? Also is it a good idea to use pfsense?"
retrieved_docs    = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
final_prompt = prompt.invoke({"context": context_text, "question": question})


answer = model.invoke(final_prompt)
print(answer.content)