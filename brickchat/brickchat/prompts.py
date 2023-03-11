from langchain.prompts import PromptTemplate
import textwrap
# we want a prompt that takes a table excerpt and builds a description of that table


def docprompt() -> PromptTemplate:
    """build a prompt for a document"""
    
    vars = ["table"]
    tmpl = textwrap.dedent("""
    Summarize the below database. Include summaries of the overall database, 
    and summaries of each column: 
    \n{table}""")
    
    return PromptTemplate(input_variables=vars, template=tmpl)