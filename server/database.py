from sqlalchemy import create_engine, Column, Integer, Enum, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
import json

engine = create_engine("sqlite:///./contacts.sqlite?check_same_thread=False")
Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer(), primary_key=True)
    firstName = Column(String(30))
    lastName = Column(String(30))
    phone = Column(String(30), unique=True)
    category = Column(Enum("family", "work", "friends"))

    def __init__(self, firstName: str, lastName: str, phone: str, category: str):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.category = category

    def __repr__(self):
        return "Contact(name=({} {}), phone=({}), category=({})".format(
            self.firstName, self.lastName, self.phone, self.category
        )



Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
