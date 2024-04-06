from haystack.nodes import PreProcessor, PromptModel, PromptTemplate, PromptNode
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack import Pipeline
from haystack.nodes import BM25Retriever
from pprint import pprint
from json import loads, dumps
import numpy as np

HF_TOKEN = "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"

with open('output.json', 'r') as f:
    data = loads(f.read())

docs = np.array_split(data, 50)
docs = [str(doc.tolist()) for doc in docs]
docs = [Document(content=doc) for doc in docs]

processor = PreProcessor()
ppdocs = processor.process(docs)

docu_store = InMemoryDocumentStore(use_bm25=True)
docu_store.write_documents(ppdocs)
retriever = BM25Retriever(docu_store, top_k = 1)

qa_template = PromptTemplate(
    prompt =
    '''
    you will be given body of an email.
    your task is to find the industry and sentiment it is associated to.
    industry types are : medical, finance, energy, technology, travel.
    Sentiments are : neutral, complaint, urgent, query.
    Context: {join(documents)};
    Prompt: {query}
    You don't have to provide any additional information
    Answer in the following format: x-y
    where 'x' is industry based upon context it can be [medical, finance, energy, technology, travel]
    where 'y' is sentiment based upon context it can be [neutral, complaint, urgent, query]
    Just provide industry nothing more
    '''
)

prompt_node = PromptNode(
    model_name_or_path = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key = HF_TOKEN,
    default_prompt_template=qa_template,
    max_length = 25,
    model_kwargs={"model_max_length":20000}
)

rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name = 'retriever', inputs=['Query'])
rag_pipeline.add_node(component=prompt_node, name = 'prompt_node', inputs=['retriever'])

q = f'''

we want urgent support
"entergy corporation and subsidiaries management's financial discussion and analysis annually , beginning in 2006 , if power market prices drop below the ppa prices ." 'accordingly , because the price is not fixed , the table above does not report power from that plant as sold forward after 2005 .' "under the ppas with nypa for the output of power from indian point 3 and fitzpatrick , the non-utility nuclear business is obligated to produce at an average capacity factor of 85% ( 85 % ) with a financial true-up payment to nypa should nypa's cost to purchase power due to an output shortfall be higher than the ppas' price ." 'the calculation of any true-up payments is based on two two-year periods .' 'for the first period , which ran through november 20 , 2002 , indian point 3 and fitzpatrick operated at 95% ( 95 % ) and 97% ( 97 % ) , respectively , under the true-up formula .' 'credits of up to 5% ( 5 % ) reflecting period one generation above 85% ( 85 % ) can be used to offset any output shortfalls in the second period , which runs through the end of the ppas on december 31 , 2004 .' 'entergy continually monitors industry trends in order to determine whether asset impairments or other losses could result from a decline in value , or cancellation , of merchant power projects , and records provisions for impairments and losses accordingly .' "marketing and trading the earnings of entergy's energy commodity services segment are exposed to commodity price market risks primarily through entergy's 50%-owned , unconsolidated investment in entergy-koch ." "entergy-koch trading ( ekt ) uses value-at-risk models as one measure of the market risk of a loss in fair value for ekt's natural gas and power trading portfolio ." 'actual future gains and losses in portfolios will differ from those estimated based upon actual fluctuations in market rates , operating exposures , and the timing thereof , and changes in the portfolio of derivative financial instruments during the year .' 'to manage its portfolio , ekt enters into various derivative and contractual transactions in accordance with the policy approved by the trading committee of the governing board of entergy-koch .' 'the trading portfolio consists of physical and financial natural gas and power as well as other energy and weather-related contracts .' 'these contracts take many forms , including futures , forwards , swaps , and options .' "characteristics of ekt's value-at-risk method and the use of that method are as follows : fffd value-at-risk is used in conjunction with stress testing , position reporting , and profit and loss reporting in order to measure and control the risk inherent in the trading and mark-to-market portfolios ." 'fffd ekt estimates its value-at-risk using a model based on j.p .' "morgan's risk metrics methodology combined with a monte carlo simulation approach ." 'fffd ekt estimates its daily value-at-risk for natural gas and power using a 97.5% ( 97.5 % ) confidence level .' "ekt's daily value-at-risk is a measure that indicates that , if prices moved against the positions , the loss in neutralizing the portfolio would not be expected to exceed the calculated value-at-risk ." 'fffd ekt seeks to limit the daily value-at-risk on any given day to a certain dollar amount approved by the trading committee .' "ekt's value-at-risk measures , which it calls daily earnings at risk ( de@r )

'''


# q = f"hi im nigerian prince you have won a lottery"
# q = f"This is regarding purchase of your new computer server. please send me purchase order of the same."
ans = rag_pipeline.run(query = q)
print(type(ans['results']))
for i in ans['results']:
    print(i.strip())

