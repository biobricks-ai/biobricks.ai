import os, pandas as pd, numpy as np, re, sqlite3, textwrap
from typing import Dict, List, Any
from .model import Doc, BrickDoc, Table
from . import chains     
import colorama
from colorama import Fore, Back, Style
import time

class BrickChat:
        
    def __init__(self):
        
        if(not 'OPENAI_API_KEY' in os.environ.keys()):
            raise Exception("must set the OPENAI_API_KEY environment variable")
        
        self.docs = Doc.get_docs()

    def table_output(self, table : Table):
        """print a table in a nice format"""
        con = sqlite3.connect("chembl.db")
        qcols = ",".join([col.name for col in table.columns])
        query = f"SELECT {qcols} FROM {table.name} LIMIT 5"
        df = pd.read_sql_query(query, con)  
        output = df.to_string()
        con.close()
        return output
    
    def tableref(self,table:Table):
        output = f"{table.name}\n{table.description}\n"
        output += "COLUMNS:\n"
        for col in table.columns:
            output += f"{col.name}:{col.description}\n"
        output+="\n"
        output+=self.table_output(table)
        return output
            
    def query(self,query):
        
        # SELECT TABLE =========================================
        # TODO we need a database selection step
        print("Finding tables...\n")
        tchain = chains.SelectTableChain(self.docs.bricks[0],1)
        tables = tchain.run(query)
        
        # SELECT COLUMNS =======================================
        print("Finding columns...\n")
        def SelectColumns(table : Table):
            cchain = chains.SelectColumnsChain(table,4)
            columns = cchain.run(query)
            return Table(table.name, table.description, columns)

        tables = [SelectColumns(t) for t in tables]
        tables = [t for t in tables if len(t.columns) > 0]
        
        # GENERATE REPLY =======================================
        print("Generating response...\n")
        def reply(tbl):
            chain = chains.ReplyChain(tables[0])
            tblref = self.tableref(tbl) 
            reply = chain.run({"tableref":tblref,"query":query})
            return tblref + "\n\n" + reply
        
        return "\n\n".join([reply(t) for t in tables])
