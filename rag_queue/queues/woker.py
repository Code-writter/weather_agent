from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model
)

def process_query(user_query : str):
    #take query and serach embedding
    search_result = vector_db.similarity_search(query=user_query)
    # Create Context
    context = "\n\n\n".join([f"Page Content : {result.page_content} \n Page Number : {result.metadata['page_label']} \n File location: {result.metadata['source']}" for result in search_result])

    SYSTEM_PROMPT = f"""
    You are a helpfull AI assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page_number.

    You should only answer the user based on the following context and navigate the user to open the right  page number to know more.

    Contex: {context}
    """
    
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT
            },
            {
                "role" : "user",
                "content" : user_query
            },
        ]
    )
    print(f"🤖 {response.choices[0].message.content}")
    return response.choices[0].message.content


