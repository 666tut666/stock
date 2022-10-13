from database import Base
from sqlalchemy import Column, String, Float, Text, Integer

class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True)
    name=Column(String(255),nullable=False,unique=True)
    category=Column(Text,nullable=False)
    price=Column(Float,nullable=False)

    def __repr__(self):
        return f"<Product name={self.name} price={self.price}>"
    
