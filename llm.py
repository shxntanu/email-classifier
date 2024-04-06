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
retriever = BM25Retriever(docu_store, top_k = 3)

qa_template = PromptTemplate(
    prompt =
    '''
    DON'T ADD UNNECEASSARY INFO IN RESULT.
    YOU MUST IDENTIFY TO WHOM THE QUERY SHOULD BE MAILED.
    YOU MUST ADD MAILS IN RESULT IF YOU THINK THE INFO MUST BE SUBMITTED TO THEM
    YOUR TASK IS TO IDENTIFY BEST SUITABLE OPTION(S) FROM CONTEXT FOR QUERY,
    ANSWER IN COMMA SEPARATED VALUES WITHOUT ADDING SUGGESTIONS OR OPINIONS.
    ANSWER MUST CONTAIN ALL THE MAILS IN LEAF NODE.
    ANSWER MUST BE LEAF NODE.
    RESULT CAN BE COMBINATION OF MULTIPLE LEAF NODES
    Context: {documents};
    Prompt: {query}
    '''
)

prompt_node = PromptNode(
    model_name_or_path = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key = HF_TOKEN,
    default_prompt_template=qa_template,
    max_length = 3000,
    model_kwargs={"model_max_length":500000}
)

rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name = 'retriever', inputs=['Query'])
rag_pipeline.add_node(component=prompt_node, name = 'prompt_node', inputs=['retriever'])


q = f"I want training on python"
ans = rag_pipeline.run(query = q)
print(ans['results'])
for i in ans['results'][0].split(','):
    print(i.strip())

