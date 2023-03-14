import faiss
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore import InMemoryDocstore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain import OpenAI
from langchain.llms import OpenAIChat
from langchain.docstore.document import Document

import requests, json, pandas as pd, biobricks as bb, pyarrow as pa
import textwrap, itertools
from brickchat import prompts

import dotenv
dotenv.load_dotenv()

import importlib
importlib.reload(prompts)

import biobricks as bb

def bricklist():
    """get list of bricks from github.com/biobricks-ai"""
    url = "https://api.github.com/users/biobricks-ai/repos?per_page=100"
    r = requests.get(url)
    j = json.loads(r.text)
    bricks = [i["name"] for i in j]
    return bricks

bricks = bricklist()

def install_bricks():    
    for brick in bricks:
        try:
            print(f"installing {brick}...")
            bb.install(brick)
        except Exception as e:
            # print a short message from the error along with the brickname
            print(f"{brick}: {str(e)[:50]}")
            pass
    
def local_bricks():
    for brick in bricks:
        try:
            tbls = vars(bb.load(brick))
            if(len(tbls) == 0):
                raise Exception("no tables")
            if(len(tbls) > 20):
                raise Exception("too many tables")
            yield brick
        except:
            pass

def make_brick_docs(brickref):
    brickdict = vars(bb.load(brickref))
    assets = list(brickdict.keys())
    for asset in assets:
        try:
            tbl = brickdict[asset]
            meta = tbl.metadata
            if(meta.num_columns > 20):
                continue
            
            batch = next(tbl.iter_batches(2000)).to_pandas()
            batch = batch.sample(n=10,replace=False)
            coldesc = "\n".join(str(tbl.schema_arrow).splitlines()[:meta.num_columns])
            summary = f"""\
            BRICK: {brickref}
            TABLE: {asset}
            NCOLS:{meta.num_columns}
            NROWS:{meta.num_rows}
            """
            summary = textwrap.dedent(summary)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_colwidth', 20)
            summary = summary + "\nCOLUMNS:\n" + coldesc + "\n\nSAMPLE:\n" + str(batch)
            yield Document(page_content=summary,metadata={"brick":brickref,"table":asset})
        except Exception as e:
            pass

lbrick = list(local_bricks())

def build_faiss_documents():
    brickdocs = [make_brick_docs(brick) for brick in lbrick]
    docs = itertools.chain(*brickdocs)
    prompt = prompts.docprompt()
    docchn = LLMChain(llm=OpenAIChat(), prompt=prompt)
    
    for doc in docs:
        doc.metadata['summary'] = doc.page_content
        content = docchn.run(doc.page_content)
        yield Document(page_content=content, metadata=doc.metadata)


def build_faiss():
    """build an index for a brick"""
    docs = build_faiss_documents()
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents([Document(page_content="NA",metadata={})],embeddings)
    
    # TODO for some reason FAISS is broken and needs docs to be added one by one
    # otherwise the metadata gets lost
    for doc in docs:
        print(f"adding {doc.metadata['brick']}/{doc.metadata['table']}...")
        db.add_documents([doc])
    return db


db = build_faiss()
db.save_local("brickchat.faiss")
