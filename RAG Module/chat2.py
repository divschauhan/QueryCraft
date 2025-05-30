# from langchain_together import Together
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate

# # Initialize the language model
# llm = Together(
#     model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
#     max_tokens=512,
#     temperature=0.1,
#     top_k=1,
#     together_api_key="c29bdce30b40ed391cbd8fd78a003a25d0078cc01def76746bba9c1f6aa6337e"
# )

# # Set up the retrieval QA chain
# def setup_retrieval_qa(db):
#     retriever = db.as_retriever(similarity_score_threshold=0.6)

#     # Define the prompt template
#     prompt_template = """ Your name is KrishiAI, Please answer questions related to Agriculture. Try explaining in simple words. Answer in less than 100 words. If you don't know the answer, simply respond with 'Don't know.'
#      CONTEXT: {context}
#      QUESTION: {question}"""

#     PROMPT = PromptTemplate(template=f"[INST] {prompt_template} [/INST]", input_variables=["context", "question"])

#     # Initialize the RetrievalQA chain
#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type='stuff',
#         retriever=retriever,
#         input_key='query',
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": PROMPT},
#         verbose=True
#     )
#     return chain


# from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

# # Initialize the OpenAI language model
# llm = ChatOpenAI(
#     model_name="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" or "gpt-4" as needed
#     openai_api_key="sk-proj-5u-nwI0s0D4gwwutVR8Roa",
#     temperature=0.1,
#     max_tokens=512
# )

# # Set up the retrieval QA chain
# def setup_retrieval_qa(db):
#     retriever = db.as_retriever(similarity_score_threshold=0.6)

#     # Define the prompt template
#     prompt_template = """Your name is KrishiAI. Please answer questions related to Agriculture. Try explaining in simple words. Answer in less than 100 words. If you don't know the answer, simply respond with 'Don't know.'
#      CONTEXT: {context}
#      QUESTION: {question}"""

#     PROMPT = PromptTemplate(template=f"[INST] {prompt_template} [/INST]", input_variables=["context", "question"])

#     # Initialize the RetrievalQA chain
#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type='stuff',
#         retriever=retriever,
#         input_key='query',
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": PROMPT},
#         verbose=True
#     )
#     return chain

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Initialize the OpenRouter language model
llm = ChatOpenAI(
    model_name="openai/gpt-3.5-turbo",  # Use "openai/gpt-3.5-turbo" or "openai/gpt-4"
    openai_api_key="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",  # Replace with your OpenRouter API key
    openai_api_base="https://openrouter.ai/api/v1",  # OpenRouter API base URL
    temperature=0.1,
    max_tokens=512
)

# Set up the retrieval QA chain
def setup_retrieval_qa(db):

    #db.as_retriever(): Converts the ChromaDB database into a retriever object.
    retriever = db.as_retriever(similarity_score_threshold=0.6)
    #retriever is a ChromaDB retriever (db.as_retriever()). this is provided by Langchain
    
    # Define the prompt template
   
    prompt_template = """Your name is KrishiAI. Please answer questions related to Agriculture.  
    Try explaining in simple words. Answer in less than 100 words.  
    Use **only** the provided context to generate your answer.  
    If the context does not contain information, respond with: "That is a great question. I do not have that information right now."  

    CONTEXT: {context}  
    QUESTION: {question}"""


    # Create a LangChain Prompt, The prompt template ensures the LLM follows the format correctly.
    PROMPT = PromptTemplate(template=f"[INST] {prompt_template} [/INST]", input_variables=["context", "question"])

    # Initialize the RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever, #Uses ChromaDB to fetch relevant text
        input_key='query',
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=True
        
        # retriever=retriever → This connects the retriever to the RetrievalQA chain.
        # The retriever automatically receives the query when chain(query) is called.

    )
    return chain

#------ How the context is inserted?------
# chain_type='stuff' means all retrieved documents are concatenated and passed to the LLM as context.
# in the prompt The {context} placeholder will be replaced by the retrieved documents.

# RetrievalQA.run(query) Replaces {context}
# Inside RetrievalQA, the following happens:

# docs = self.retriever.get_relevant_documents(query)  # Retrieves relevant documents

# formatted_prompt = self.prompt.format(context=docs, question=query)  # Inserts retrieved docs

# docs (retrieved text chunks) replace {context}.
# query replaces {question}.

#  Example Final Prompt Given to LLM

# Your name is KrishiAI. Please answer questions related to Agriculture. 
# Try explaining in simple words. Answer in less than 100 words. 
# If you don't know the answer, simply respond with 'Don't know.'

# CONTEXT: 
# 1. "Rice needs 120-150 days for full maturity."
# 2. "Urea is a nitrogen-rich fertilizer used for rice production."

# QUESTION: "What fertilizer should I use for rice?"

#The retrieved text chunks (from the PDFs) are inserted as context before passing to GPT.

