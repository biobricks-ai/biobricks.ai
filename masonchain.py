from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.chains import SQLDatabaseSequentialChain
import os

# set OPENAI_API_KEY environment variable
os.environ["OPENAI_API_KEY"] = "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"


uri = "sqlite:///./chembl.db"
sdb = SQLDatabase.from_uri(uri)
llm = OpenAI(temperature=0)

# chn = SQLDatabaseChain(llm=llm, database=sdb, verbose=True)
chn = SQLDatabaseSequentialChain.from_llm(llm, sdb, verbose=True)


