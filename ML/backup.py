from haystack.nodes import PreProcessor, PromptModel, PromptTemplate, PromptNode
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack import Pipeline
from haystack.nodes import BM25Retriever
from pprint import pprint
from json import loads, dumps


HF_TOKEN = "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"

with open('rag2.json', 'r') as f:
    data = loads(f.read())

docs = []
docs.append(Document(content = str(data)))
processor = PreProcessor()
ppdocs = processor.process(docs)

docu_store = InMemoryDocumentStore(use_bm25=True)
docu_store.write_documents(ppdocs)
retriever = BM25Retriever(docu_store, top_k = 1)

qa_template = PromptTemplate(
    prompt =
    '''
    You are given a mail.
    Your task is to forward the mail to appropriate team.
    You will have to traverse the context to find the mails of appropriate team.
    You must answer the mail addresses of the team(s) in a list.
    DON'T ADD ADDITONAL DETAILS IN ANSWER.
    Prompt: {query}
    Context: join({documents})
    Please provide your response in the following format: [x, y, z, ...]
    Where 'x/y/z' are email addresses.
    JUST GIVE ME MAILS NOTHING MORE.
    '''
)

prompt_node = PromptNode(
    model_name_or_path = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key = HF_TOKEN,
    default_prompt_template=qa_template,
    max_length = 20,
    model_kwargs={"model_max_length":20000}
)

rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name = 'retriever', inputs=['Query'])
rag_pipeline.add_node(component=prompt_node, name = 'prompt_node', inputs=['retriever'])

q = f"This is regarding purchase of your new computer server. please send me purchase order of the same."
ans = rag_pipeline.run(query = q)
print(type(ans['results']))
for i in ans['results']:
    print(i.strip())

