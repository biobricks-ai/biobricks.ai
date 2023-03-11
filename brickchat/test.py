import faiss
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain import OpenAI
from langchain.llms import OpenAIChat
from langchain.docstore.document import Document

import requests, json, pandas as pd, biobricks as bb, pyarrow as pa
from brickchat import prompts

import dotenv
dotenv.load_dotenv()

import importlib
importlib.reload(prompts)

import biobricks as bb

# list bricks
def bricklist():
    """get list of bricks from github.com/biobricks-ai"""
    url = "https://api.github.com/users/biobricks-ai/repos?per_page=100"
    r = requests.get(url)
    j = json.loads(r.text)
    bricks = [i["name"] for i in j]
    return bricks

bricks = bricklist()

def build_brick_embedding(brickref):
    brick : dict = vars(bb.load("clinvar"))
    prompt = prompts.docprompt()
    docchn = LLMChain(llm=OpenAIChat(), prompt=prompt)
    assets = list(brick.keys())
    
    def mkdoc(tblref):
        print(f'making {brickref}/{tblref}')
        tbl = str(brick[tblref].take(pa.array(range(5)))).splitlines()[1:]
        tbl[tbl.index('----')] = 'COLUMN EXAMPLES:'
        tblstr = '\n'.join(tbl)
        text = f"DATABASE: {brickref}\nTABLE: {tblref}\n{tblstr}"
        text = text[:4095]
        return docchn.run(text)
    
    documents = []
    for tblref in assets:
        doc = mkdoc(tblref)
        mdata = { "brick": brickref, "table": tblref }
        documents.append(Document(page_content=doc, metadata=mdata))
                
    return documents

def build_brick_index(brick):
    """build an index for a brick"""
    bricks = bricklist()
    # install bricks
    for brick in bricks:
        bb.install(brick)
    

    
    