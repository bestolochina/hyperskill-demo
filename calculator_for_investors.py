from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'
    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'
    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


engine = create_engine('sqlite:///investor.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Read CSVs, treating empty strings as NaN
df_companies = pd.read_csv('test/companies.csv', na_values=['', ' '])
df_financial = pd.read_csv('test/financial.csv', na_values=['', ' '])

# Replace NaN with None
df_companies = df_companies.where(pd.notnull(df_companies), None)
df_financial = df_financial.where(pd.notnull(df_financial), None)

# Add data to the database
session.add_all([Companies(**row) for row in df_companies.to_dict(orient='records')])
session.add_all([Financial(**row) for row in df_financial.to_dict(orient='records')])

session.commit()
print('Database created successfully!')
