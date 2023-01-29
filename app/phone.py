from pydantic import BaseModel


class CreatePhoneModel(BaseModel):
    model: str
    developer: str


class Phone:
    def __init__(self, id: int, model: str, developer: str):
        self.id = id
        self.model = model
        self.developer = developer
