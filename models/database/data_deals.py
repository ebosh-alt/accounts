from pydantic import BaseModel
from datetime import datetime


class DataDeals(BaseModel):
    id:int
    shop: str
    name: str
    price: float
    description: str
    data: str
    date: datetime
    guarantor: bool

    def len(self):
        return len(str(self.id) +str(self.shop) +str(self.name) +str(self.price) +str(self.description) +str(self.data) +str(self.date) +str(self.guarantor))