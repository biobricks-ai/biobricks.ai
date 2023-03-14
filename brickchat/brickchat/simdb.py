from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate as PT
from langchain import OpenAI
import textwrap

embeddings = OpenAIEmbeddings()
db = FAISS.load_local("brickchat.faiss",embeddings)
llm = OpenAI()

def find_tables(query):
    results = db.similarity_search_with_score(query, 5)
    results = [x for x in results if len(x[0].metadata) > 0]
    
    querylength = len(query)
    if(querylength > 2048):
        raise Exception(f"query is {querylength} characters, shorten to 2048 characters or less.")
    
    prompt = textwrap.dedent(f"""\
        The below is a table description and sample:\n\n
        {{tableref}}\n\n
        A user makes the following query for tables:\n\n
        {query}\n\n
        Describe why the given table and columns are a good reference.
        """)
    
    if len(results) == 0:
        raise Exception("No results found")
    
    for res in results:
        sumlength = 4056 - len(prompt)
        summ = res[0].metadata['summary'][0:sumlength]
        prompt = prompt.replace("{tableref}",summ)
        resp = llm.generate([prompt]).generations[0][0].text
        yield (res[0].metadata, resp)
    
    