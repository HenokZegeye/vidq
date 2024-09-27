from langchain.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains.llm import LLMChain

def get_transcript(url):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)
    
    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    return db

def get_response_from_query(db, query, k=4):
    docs = db.similarity_search(query, k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    template = """
        You are a helpful assistant that can answer questions about videos based on the video's transcript: {docs}

        Only use the factual information from the transcript to answer question.

        If you feel like you don't have enough information to answer the question, say "I don't know".

        Your answers should be verbose and detailed.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    user_template = "Answer the following question: {question}"
    user_message_prompt = HumanMessagePromptTemplate.from_template(user_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, user_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    return response, docs