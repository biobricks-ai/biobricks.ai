import requests
import pandas as pd, numpy as np

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
        header = "skey\tname\ttype\tdescription"
        txt = ""
        for col in self.columns:
            txt += f"{col.skey}\t{col.name}\t{col.stype}\t{col.description}\n"
        return header + "\n" + txt
        
    def __str__(self):
        return f"{self.name}: {self.description}"

class BrickDoc:
    
    def __init__(self, name, tables, description):
        self.name = name
        self.tables = tables
        self.description = description
    
    def print_tables(self):
        txt = ""
        for table in self.tables:
            txt += str(table) + "\n"
        return txt
    
    def __str__(self):
        stripdesc = self.description.replace("\n"," ").replace("\t"," ")
        return f"{self.name}: {stripdesc}"

# TODO Bricks should be loaded by reference to BBLIB
class ChemblBrick(BrickDoc):
    
    def __init__(self):
        tbls = self.get_tables()
        desc = "ChEMBL is a manually curated database of bioactive molecules with drug-like properties. It brings together chemical, bioactivity and genomic data to aid the translation of genomic information into effective new drugs. ChEMBL is developed by the European Bioinformatics Institute (EMBL-EBI) and is funded by the European Medicines Agency (EMA)."
        super().__init__("ChEMBL", tbls, desc)
    
    # TODO bricks need a standard documentation file
    def get_tables(self):
        
        # read chembl_schema.txt to get the table names and column descriptions
        schematxt = requests.get("https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/schema_documentation.txt")
        schematxt = schematxt.text
        schematxt = "\n".join(schematxt.split("\n")[3:])
        schematxt = schematxt.split("\n\n\n")

        schemahtml = requests.get("https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/schema_documentation.html")
        schemahtml = schemahtml.text.strip()

        dfs = pd.read_html(schemahtml)

        tables = []      
        for txt,table in list(zip(schematxt, dfs)):
            block = txt.split("\n")
            tablename = block[0].replace(":","")
            tabledesc = block[1]
            arrs = np.array(table.values)[1:]
            columns = []
            for col in arrs:
                columns.append(Column(col[1], col[4], col[2], col[0]))
            tables.append(Table(tablename, tabledesc, columns))
            
        return tables

class Doc:
    
    def __init__(self, bricks):
        self.bricks = bricks
        
    def bricklist(self):
        txt = ""
        for brick in self.bricks:
            txt += str(brick)
        return txt
    
    @staticmethod
    def get_docs():
        # TODO This should load from BBLIB
        return Doc([ChemblBrick()])