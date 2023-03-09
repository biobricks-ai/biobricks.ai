from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.chains import SQLDatabaseSequentialChain, LLMChain
from langchain.chains.base import Chain

import os, pandas as pd, numpy as np, re, sqlite3, textwrap
from typing import Dict, List, Any

# import the Column and Table classes from the model.py file
from model import Doc, BrickDoc, Table

class SQLRetryChain(Chain):
    "A language model chain that retries on error"
    querychain: LLMChain
    retrychain: LLMChain
    replychain: LLMChain
    tables: List[Table]
    max_iter: int = 5
    
    @property
    def input_keys(self) -> List[str]:
        return ["query"]

    @property
    def output_keys(self) -> List[str]:
        return ['result']
    
    def tryrun(self, query:str):
        con = sqlite3.connect("chembl.db")
        try:
            df = pd.read_sql_query(query, con)
            return {"table":str(df),"err":None}
        except Exception as e:
            return {"table":None,"err":str(e)}
        finally:
            con.close()
        
    def _call(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        query = self.querychain.run(inputs)
        res = self.tryrun(query)
        
        iter = 0
        while res['err'] is not None and iter < self.max_iter:
            iter = iter + 1
            print(f"Error: {res['err']}")
            inputs.update({"predicted_query":query, "error":res['err']})
            query = self.retrychain.run(inputs)
            res = self.tryrun(query)
        
        if res['err'] is not None:
            query = f"SELECT * FROM {self.tables[0].name} LIMIT 5"
            res = self.tryrun(query)
        
        inputs.update({"predicted_query":query, "table":res['table']})
        
        res = self.replychain.run(inputs)
        res = textwrap.dedent(f"""\
        {inputs["predicted_query"]}\n\n
        {inputs["table"]}\n\n
        {res}
        """)
        res.replace("\n\s+", "\n")
        return {"result":res}


class SelectionChain(Chain):
    """Select bricks from the output of a chain"""
    chain: LLMChain
    idict: Dict[str, Any]
    max_items : int = 100000
    
    
    @property
    def input_keys(self) -> List[str]:
        return ["query"]

    @property
    def output_keys(self) -> List[str]:
        return ['result']
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        out = self.chain.run(inputs).splitlines()
        out = [o.strip() for o in out if o in self.idict.keys()]
        items = [self.idict[o] for o in out]
        return {'result': items}


def SelectTableChain(brick:BrickDoc, max_items:int=3):
    "SELECT A TABLE FROM A BRICK"
    
    T = textwrap.dedent(f"""
        A researcher asks "{{query}}"\n\n
        Choose up to 3 good reference tables for this query from below:
        \n\n{brick.print_tables()}\n\n 
        Don't print anything other than the table names.
        One table name per line. Print at most 3 table names.
        Order tables from most to least relevant.
        """)
    
    P = PromptTemplate(input_variables=["query"],template=T)

    chain = LLMChain(llm=OpenAI(), prompt=P)
    idict = {t.name: t for t in brick.tables}
    
    return SelectionChain(chain=chain, idict=idict, max_items=max_items)

def SelectColumnsChain(table:Table, max_items:int=4):
    "SELECT RELEVANT COLUMNS FROM A TABLE"
    
    T = textwrap.dedent(f"""
        A researcher asks "{{query}}"\n\n
        Choose good reference columns for this query from below:
        \n\n{table.print_cols()}\n\n 
        Don't print anything other than the column names.
        One column name per line.
        Always include the first column.
        Never include more than four columns.
        Order columns from most to least relevant.""")
    
    P = PromptTemplate(input_variables=["query"],template=T)

    chain = LLMChain(llm=OpenAI(), prompt=P)
    idict = {c.name: c for c in table.columns}
    
    return SelectionChain(chain=chain, idict=idict, max_items=max_items)


def ReplyChain(table:Table):
    prompt = PromptTemplate(
        input_variables=["tableref","query"],
        template=textwrap.dedent(f"""
        The below is a table description and sample:\n\n
        {{tableref}}\n\n
        A user we love asks the following question:\n\n
        {{query}}\n\n
        Describe why the given table and columns are a good reference.
        """))

    return LLMChain(llm=OpenAI(), prompt=prompt)
        
def SQLQueryChain(tables : List[Table]):
    "Chain that generates sql queries from a user query and table schemas"
    
    tbldoc = ""
    for table in tables:
        tbldoc += "TABLE: " + table.name + "\n"
        tbldoc += "COLUMNS:\n" 
        tbldoc += table.print_cols() + "\n\n"
        
    p = PromptTemplate(
        input_variables = ["query"],
        template=textwrap.dedent(f"""
        A researcher asks "{{query}}"\n\n
        answer the question with a sqlquery from these docs:
        \n\n{tbldoc}\n\n 
        Don't print anything other than the query.
        The query should end with LIMIT 5.
        The query should not select more than 4 columns.
        
        Don't print anything other than the query."""))

    chn = LLMChain(llm=OpenAI(), prompt=p, verbose=False)
    return chn

class SQLRetryChain(Chain):
    "A language model chain that retries on error"
    querychain: LLMChain
    retrychain: LLMChain
    replychain: LLMChain
    tables: List[Table]
    max_iter: int = 5
    
    @property
    def input_keys(self) -> List[str]:
        return ["query"]

    @property
    def output_keys(self) -> List[str]:
        return ['result']
    
    def tryrun(self, query:str):
        con = sqlite3.connect("chembl.db")
        try:
            df = pd.read_sql_query(query, con)
            return {"table":str(df),"err":None}
        except Exception as e:
            return {"table":None,"err":str(e)}
        finally:
            con.close()
        
    def _call(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        query = self.querychain.run(inputs)
        res = self.tryrun(query)
        
        iter = 0
        while res['err'] is not None and iter < self.max_iter:
            iter = iter + 1
            print(f"Error: {res['err']}")
            inputs.update({"predicted_query":query, "error":res['err']})
            query = self.retrychain.run(inputs)
            res = self.tryrun(query)
        
        if res['err'] is not None:
            query = f"SELECT * FROM {self.tables[0].name} LIMIT 5"
            res = self.tryrun(query)
        
        inputs.update({"predicted_query":query, "table":res['table']})
        
        res = self.replychain.run(inputs)
        res = textwrap.dedent(f"""\
        {inputs["predicted_query"]}\n\n
        {inputs["table"]}\n\n
        {res}
        """)
        res.replace("\n\s+", "\n")
        return {"result":res}


def SQLChain(tables: List[Table]):
    # This chain should try to run the query
    # If it fails, it should take the error and the query
    # and try again
    querychn = SQLQueryChain(tables)
    
    tbldoc = ""
    for table in tables:
        tbldoc += "TABLE: " + table.name + "\n"
        tbldoc += "COLUMNS:\n" 
        tbldoc += table.print_cols() + "\n\n"
    
    retryprompt = PromptTemplate(
        input_variables = ["query", "predicted_query", "error"],
        template=textwrap.dedent(f"""
        A researcher asks "{{query}}"\n\n
        answer the question with a sqlquery from these docs:
        \n\n{tbldoc}\n\n 
        Don't print anything other than the query.
        The query should end with LIMIT 5.
        
        The last output was\n\n{{predicted_query}}\n\n.
        It failed with the error:\n\n{{error}}\n\n.
        Please try again:"""))
    
    retrychain = LLMChain(llm=OpenAI(), prompt=retryprompt, verbose=False)
    
    replyprompt = PromptTemplate(
        input_variables = ["query", "predicted_query", "table"],
        template=textwrap.dedent(f"""
        A database schema includes: \n\n{tbldoc}\n\n
        A researcher asks "{{query}}"\n\n
        A good sqlquery to reference is: \n\n{{predicted_query}}\n\n
        It generates response: \n\n{{table}}\n\n
        Describe what this query is doing and 
        how it could be used to answer the question.
        """))
    replychain = LLMChain(llm=OpenAI(), prompt=replyprompt, verbose=False)
    
    return SQLRetryChain(querychain = querychn, 
                            retrychain = retrychain, 
                            replychain = replychain, 
                            tables = tables)