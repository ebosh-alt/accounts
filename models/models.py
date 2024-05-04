from pydantic import BaseModel


class DataDeals(BaseModel):
    id: int
    shop: str
    name: str
    price: float
    description: str
    data: str
    date: str
    guarantor: bool
    payment: int

    def len(self):
        return len(str(self.id) + str(self.shop) + str(self.name) + str(self.price) + str(self.description) + str(
            self.data) + str(self.date) + str(self.guarantor) + str(self.payment))
