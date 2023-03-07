from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.chains import SQLDatabaseSequentialChain, LLMChain
import os, pandas as pd, numpy as np, wget
import dotenv

# set OPENAI_API_KEY environment variable
dotenv.load_dotenv()

# uri = "sqlite:///./chembl.db"
# sdb = SQLDatabase.from_uri(uri)
llm = OpenAI(temperature=0)

# download this file
# TODO we need a schema for biobricks
if(not os.path.exists("chembl_schema.txt")):
    url = "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/schema_documentation.txt"
    wget.download(url, "chembl_schema.txt")

if(not os.path.exists("chembl_schema.html")):
    url = "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/schema_documentation.html"
    wget.download(url, "chembl_schema.html")

# read chembl_schema.txt to get the table names and column descriptions
# skip the first line
chembldocs = ""
with open("chembl_schema.txt", "r") as f:
    chembldocs = f.read().strip()
chembldocs = "\n".join(chembldocs.split("\n")[3:])
chembldocs = chembldocs.split("\n\n\n")

class Column:
    
    def __init__(self, name, description, stype, skey):
        self.name = name
        self.description = description
        self.stype = stype
        self.skey = skey
    
class Table:
    
    def __init__(self, name, description, columns):
        self.name = name
        self.description = description
        self.columns = columns
        
    def print_cols(self):
        header = "name\tkey\ttype\tdescription"
        txt = ""
        for col in self.columns:
            txt += f"{col.name}\t{col.stype}\t{col.skey}\t{col.description}\n"
        return header + "\n" + txt
        
    def __str__(self):
        return f"{self.name}: {self.description}"

chemblhtml = ""
with open("chembl_schema.html", "r") as f:
    chemblhtml = f.read().strip()

dfs = pd.read_html(chemblhtml)

tables = []      
for txt,table in list(zip(chembldocs, dfs)):
    block = txt.split("\n")
    tablename = block[0].replace(":","")
    tabledesc = block[1]
    arrs = np.array(table.values)[1:]
    columns = []
    for col in arrs:
        columns.append(Column(col[1], col[4], col[2], col[0]))
    tables.append(Table(tablename, tabledesc, columns))

# chn = SQLDatabaseChain(llm=llm, database=sdb, verbose=True)
# chn = SQLDatabaseSequentialChain.from_llm(llm, sdb, verbose=True)

# take the first 3000 characters from chembldocs
shortdoc = ""
for table in tables:
    shortdoc += str(table) + "\n"

prompt = PromptTemplate(
    input_variables = ["research question"],
    template=f"""Here is a chembl schema:\n\n{shortdoc}\n\n use the schema to find relevant tables 
    to answer the research question: {{research question}}. 
    Don't print anything other than the table names, one per line.
    Choose at most 3 tables.""")

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
res = chain.run("what action types exist in chembl?")

print(res)
rawtables = res.split("\n")
# get the results from rawtables where the result is in the set of table names
restables = [table for table in tables if table.name in rawtables]

coldocs = ""
for table in restables:
    coldocs += f"{table.name}: {table.description}\n"
    coldocs += f"{table.print_cols()}\n"
    coldocs += "\n"

colprompt = PromptTemplate(
    input_variables = ["research question"],
    template=f"""Here is the schema for selected tables:\n\n${coldocs}\n\n 
    write a sqlquery with this schema to answer the research question: {{research question}}. 
    Don't print anything other than the query""")


colchn = LLMChain(llm=llm, prompt=colprompt, verbose=True)
res = colchn.run("what action types exist in chembl?")
