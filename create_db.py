from database import Base, engine
from models import Product

print("creating database")
Base.metadata.create_all(engine)

