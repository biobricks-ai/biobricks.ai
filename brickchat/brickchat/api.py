from .chat import BrickChat

chat = BrickChat()

def query(query):
  return chat.query(query)