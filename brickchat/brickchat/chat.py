import os, pandas as pd, numpy as np, re, sqlite3, textwrap
from typing import Dict, List, Any
from model import Doc, BrickDoc, Table
import chains        
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
        
    def livetype(self,text,fore):
        for char in text:
            char = char if fore is None else fore + char
            print(char, end='', flush=True)
            time.sleep(0.01)
            
    def query(self,query):
        
        # SELECT TABLE =========================================
        # TODO we need a database selection step
        self.livetype("Finding tables...\n",Fore.GREEN)
        tchain = chains.SelectTableChain(self.docs.bricks[0],3)
        tables = tchain.run(query)
        
        # SELECT COLUMNS =======================================
        self.livetype("Finding columns...\n",Fore.GREEN)
        def SelectColumns(table : Table):
            cchain = chains.SelectColumnsChain(table,4)
            columns = cchain.run(query)
            return Table(table.name, table.description, columns)

        tables = [SelectColumns(t) for t in tables]
        tables = [t for t in tables if len(t.columns) > 0]
        
        # GENERATE REPLY =======================================
        self.livetype("Generating response...\n",Fore.GREEN)
        def reply(tbl):
            chain = chains.ReplyChain(tables[0])
            tblref = self.tableref(tbl) 
            reply = chain.run({"tableref":tblref,"query":query})
            self.livetype(tbl.name.upper(),Fore.MAGENTA)
            self.livetype("\n" + self.table_output(tbl),Fore.MAGENTA)
            self.livetype("\n\n" + reply,Fore.LIGHTMAGENTA_EX)
            self.livetype("\n\n",Fore.RESET)
            return tblref + "\n\n" + reply
        
        response = "\n\n".join([reply(t) for t in tables])
        # return "\n\n".join([reply(t) for t in tables])
