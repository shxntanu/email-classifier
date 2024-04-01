from haystack.nodes import PreProcessor, PromptModel, PromptTemplate, PromptNode
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack import Pipeline
from haystack.nodes import BM25Retriever
from pprint import pprint
from json import loads, dumps
from translator import translate_text

HF_TOKEN = "your_huggingface_token_here"

with open('rag.json', 'r') as f:
    data = loads(f.read())

vendor_data = data['vendors']
benefits_data = data['states']
docs = []
doc = dumps(vendor_data)
docs.append(Document(content = doc))
doc = dumps(benefits_data)
docs.append(Document(content = doc))

processor = PreProcessor()
ppdocs = processor.process(docs)


docu_store = InMemoryDocumentStore(use_bm25=True)
docu_store.write_documents(ppdocs)

retriever = BM25Retriever(docu_store, top_k = 3)


qa_template = PromptTemplate(
    prompt =
    '''
    DON'T PROVIDE IRRELEVANT INFORMATION.
    DON'T GIVE OTHERS IRRELEVANT INFORMATION about other cities/states.
    Your name is Surya Sahayak, you are a chatbot who deals with renewable energy related queries. You are chatting with a user who is interested in installing solar panels or facing problems.
    Provide information about vendor and state benefits about city/state only if asked by user.
    IF YOU DON'T KNOW THE ANSWER, JUST REPLY THAT YOU DON'T KNOW.
    Context: {join(documents)};
    Prompt: {query}
    '''
)

prompt_node = PromptNode(
    model_name_or_path = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key = HF_TOKEN,
    default_prompt_template=qa_template,
    max_length = 29000,
    model_kwargs={"model_max_length":500000}
)

rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name = 'retriever', inputs=['Query'])
rag_pipeline.add_node(component=prompt_node, name = 'prompt_node', inputs=['retriever'])

def chat(query):
    response = rag_pipeline.run(query = query)
    response = response['results'][0].strip()
    return response


# while 1:
#     query = input("Enter your query: ")
#     print(chat(query))