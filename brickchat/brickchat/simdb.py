from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain import OpenAI

import requests, json, pandas
from . import prompts

loader = TextLoader('../../state_of_the_union.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

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

# build docs for a brick
def brickdoc(brickref):
    brick = bb.load(brickref)
        
def build_brick_index(brick):
    """build an index for a brick"""
    bricks = bricklist()
    # install bricks
    for brick in bricks:
        bb.install(brick)
    
    # build index
    prompt = prompts.docprompt()   
    docchn = LLMChain(llm=OpenAI(), prompt=prompt)