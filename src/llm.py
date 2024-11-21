from haystack import Document, Pipeline
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from json import loads
from dotenv import load_dotenv
load_dotenv()

with open('src/data/rag.json', 'r') as f:
    data = loads(f.read())

docs = [Document(content=str(data))]

cleaner = DocumentCleaner()
ppdocs = cleaner.run(documents=docs)

docu_store = InMemoryDocumentStore()
docu_store.write_documents(ppdocs['documents'])

retriever = InMemoryBM25Retriever(document_store=docu_store, top_k=1)

template = '''
    As the person in charge of mail distribution, your task is to direct emails to the right recipients.
    Use the context provided to determine the most fitting recipient(s) for the query.
    The context includes the organization's structure, departments, and teams.
    You can also use the description tag from the context to match the semantic meaning of the email.
    Your answer should be the id of the team(s) at the leaf node of the hierarchy to whom the query should be directed.
    
    Context: 
    {% for document in documents %}
        {{ document.content }};
    {% endfor %}
    
    Query: {{ query }}
    Please respond in the following format: <x>
    where 'x' is the id of the leaf node.
    Your answer should ONLY INCLUDE THE ID
    '''
    
prompt_builder = PromptBuilder(template=template)

generator = OllamaGenerator(model="qwen:1.8b",
                            url = "http://localhost:11434",
                            generation_kwargs={
                              "num_predict": 100,
                              "temperature": 0.9,
                              },
                            )

rag_pipeline = Pipeline()


rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", generator)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")


def return_ans(query):
    try:
        ans = rag_pipeline.run({"prompt_builder": {"query": query},
									"retriever": {"query": query}})
        
        response = {
            "team": int(ans['llm']['replies'][0].strip())
        }
        return response
    except:
        response = {
            "team": int(ans['llm']['replies'][0].strip())
        }
        return response
    
def test_output():
    content = '''
    I am writing to report a specific issue I have been facing with the online banking platform that requires attention and resolution.

The problem I am encountering revolves around inconsistencies in the transaction history displayed in my online banking account. Specifically, certain transactions appear to be duplicated or missing altogether, leading to confusion and inaccurate financial records.


For example, on 2nd April, I noticed that a transaction for $5000 appears twice in my transaction history, resulting in an incorrect balance calculation. Furthermore, transactions made on 4th April do not reflect in the transaction history, despite being successfully processed and confirmed by Barclays.


These discrepancies not only disrupt my ability to track and manage my finances accurately but also raise concerns about the reliability and integrity of the online banking system.


I urge your technical team to investigate this matter promptly and rectify the issues causing these inconsistencies in the transaction history. It is crucial to ensure that the online banking platform provides accurate and up-to-date information to customers to maintain trust and confidence in Barclays' services.


I kindly request regular updates on the progress made in resolving this issue and ensuring the stability of the online banking platform.

I look forward to a swift resolution and a seamless banking experience moving forward.'''

    print("Output of Model: ")
    print(return_ans(content))
    
# if __name__ == "__main__":
#     test_output()