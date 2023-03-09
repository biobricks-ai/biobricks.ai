import dotenv, sqlite3, pandas as pd

dotenv.load_dotenv()

import sys
sys.path.append('./brickchat')

from brickchat.model import Doc, Table, Column
import importlib, pandas as pd, numpy as np, re, sqlite3, textwrap

from langchain.prompts import PromptTemplate
from langchain import OpenAI
from langchain.chains import LLMChain

import brickchat.chains as chains
import brickchat.chat as bc

importlib.reload(bc)
importlib.reload(chains)
chat = bc.BrickChat()
chat.query("Where can I find SMARTS for structural alerts?")
chat.query("What can Chembl tell me about toxicology?")
