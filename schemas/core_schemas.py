from pydantic import RootModel, BaseModel
from sqlmodel import SQLModel, Field

class OurBaseModel(BaseModel):
    pass


class OurRootModel(RootModel):
    """
    Used for iterations and lists validation
    """

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
