from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import os
from pydantic import BaseModel
from jina import Client, DocumentArray, Document

class Pipeline:
    class Valves(BaseModel):
        JINA_API_URL: str = "http://localhost:45678"
        JINA_MODEL: str = "jina-embeddings-v3"
        DATA_PATH: str = "/app/backend/data/docs"

    def __init__(self):
        self.valves = self.Valves()
        self.client = None
        self.documents = None

    async def on_startup(self):
        self.client = Client(host=self.valves.JINA_API_URL)
        self.documents = DocumentArray.from_files(self.valves.DATA_PATH)

    async def on_shutdown(self):
        self.client = None
        self.documents = None

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        query_doc = Document(text=user_message)
        response = self.client.search(query_doc, parameters={"model": self.valves.JINA_MODEL})
        return response[0].matches[0].text
