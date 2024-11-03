import warnings
import os
import sys
from typing import Callable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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


class Menu:
    def __init__(self, title: str, options: dict[str, dict[str, str | Callable]]):
        self.title = title
        self.options = options

    def display(self) -> None:
        print(self.title)
        for value in self.options.values():
            print(f"{value['prompt']}")

    def run(self) -> None:
        while True:
            self.display()
            choice = input('\nEnter an option:\n')
            if choice in self.options:
                self.options[choice]['function']()
                break
            else:
                print('Invalid option!\n')


class Calculator:
    def __init__(self, session: sessionmaker.object_session):
        self.session = session
        self.main_menu = Menu('MAIN MENU',
                              {'0': {'prompt': '0 Exit', 'function': self.main_exit},
                               '1': {'prompt': '1 CRUD operations', 'function': self.main_crud},
                               '2': {'prompt': '2 Show top ten companies by criteria', 'function': self.main_show}})
        self.crud_menu = Menu('CRUD MENU',
                              {'0': {'prompt': '0 Back', 'function': self.crud_back},
                               '1': {'prompt': '1 Create a company', 'function': self.crud_create},
                               '2': {'prompt': '2 Read a company', 'function': self.crud_read},
                               '3': {'prompt': '3 Update a company', 'function': self.crud_update},
                               '4': {'prompt': '4 Delete a company', 'function': self.crud_delete},
                               '5': {'prompt': '5 List all companies', 'function': self.crud_list}})
        self.top_10_menu = Menu('TOP TEN MENU',
                                {'0': {'prompt': '0 Back', 'function': self.top_back},
                                 '1': {'prompt': '1 List by ND/EBITDA', 'function': self.top_list_nd},
                                 '2': {'prompt': '2 List by ROE', 'function': self.top_list_roe},
                                 '3': {'prompt': '3 List by ROA', 'function': self.top_list_rda}})

    def main_exit(self) -> None:
        print('Have a nice day!')
        self.session.close()
        sys.exit(0)

    def main_crud(self) -> None:
        self.crud_menu.run()

    def main_show(self) -> None:
        self.top_10_menu.run()

    def crud_back(self) -> None:
        print('Not implemented!')

    def crud_create(self) -> None:
        ticker = input("Enter ticker (in the format 'MOON'):\n")
        company = input("Enter company (in the format 'Moon Corp'):\n")
        industries = input("Enter industries (in the format 'Technology'):\n")

        new_company = Companies(
            ticker=ticker,
            name=company,
            sector=industries
        )
        new_financial = self.new_financial(ticker=ticker)

        self.session.add(new_company)
        self.session.add(new_financial)
        self.session.commit()

        print('Company created successfully!')

    def crud_read(self) -> None:
        if not (company := self.get_company()):
            return
        financial = self.session.query(Financial).filter_by(ticker=company.ticker).first()

        try:
            pe_ratio = round(financial.market_price / financial.net_profit, 2) if financial.net_profit else None
            ps_ratio = round(financial.market_price / financial.sales, 2) if financial.sales else None
            pb_ratio = round(financial.market_price / financial.assets, 2) if financial.assets else None
            nd_ebitda_ratio = round(financial.net_debt / financial.ebitda, 2) if financial.ebitda else None
            roe = round(financial.net_profit / financial.equity, 2) if financial.equity else None
            roa = round(financial.net_profit / financial.assets, 2) if financial.assets else None
            la_ratio = round(financial.liabilities / financial.assets, 2) if financial.assets else None

            # Display results, defaulting to None where applicable
            print(company.ticker, company.name)
            print(f"P/E = {pe_ratio}")
            print(f"P/S = {ps_ratio}")
            print(f"P/B = {pb_ratio}")
            print(f"ND/EBITDA = {nd_ebitda_ratio}")
            print(f"ROE = {roe}")
            print(f"ROA = {roa}")
            print(f"L/A = {la_ratio}")

        except SQLAlchemyError as e:
            print("Database error occurred:", e)
        except TypeError as e:
            print("Calculation error due to missing data:", e)

    def get_company(self) -> Companies | None:
        company_name = input("Enter company name:\n")
        # Adding wildcards for partial matching
        company_results = self.session.query(Companies).filter(
            Companies.name.ilike(f"%{company_name}%")
        ).all()

        if not company_results:
            print('Company not found!')
        else:
            companies = dict(enumerate(company_results))
            for num, company in companies.items():
                print(num, company.name)
            while (num := int(input('Enter company number:\n'))) not in companies:
                continue

            return companies[num]  # This is the company!

    @staticmethod
    def new_financial(ticker: str):
        ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
        sales = float(input("Enter sales (in the format '987654321'):\n"))
        net_profit = float(input("Enter net profit (in the format '987654321'):"))
        market_price = float(input("Enter market price (in the format '987654321'):\n"))
        net_debt = float(input("Enter net debt (in the format '987654321'):\n"))
        assets = float(input("Enter assets (in the format '987654321'):\n"))
        equity = float(input("Enter equity (in the format '987654321'):\n"))
        cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
        liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))
        return Financial(
            ticker=ticker,
            ebitda=ebitda,
            sales=sales,
            net_profit=net_profit,
            market_price=market_price,
            net_debt=net_debt,
            assets=assets,
            equity=equity,
            cash_equivalents=cash_equivalents,
            liabilities=liabilities
        )

    def crud_update(self) -> None:
        if not (company := self.get_company()):
            return
        new_financial = self.new_financial(company.ticker)
        self.session.merge(new_financial)
        self.session.commit()
        print('Company updated successfully!')

    def crud_delete(self) -> None:
        if not (company := self.get_company()):
            return
        self.session.delete(company)
        self.session.commit()
        print('Company deleted successfully!')

    def crud_list(self) -> None:
        company_results = self.session.query(Companies.ticker,
                                             Companies.name,
                                             Companies.sector).order_by(Companies.ticker).all()
        print('COMPANY LIST')
        for company in company_results:
            print(company.ticker, company.name, company.sector)

    def top_back(self) -> None:
        print('Not implemented!')

    def top_list_nd(self) -> None:
        print('Not implemented!')

    def top_list_roe(self) -> None:
        print('Not implemented!')

    def top_list_rda(self) -> None:
        print('Not implemented!')


def main():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    database_path = 'investor.db'
    engine = create_engine(f'sqlite:///{database_path}')

    # Check if the database already exists
    if not os.path.exists(database_path):
        Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Read CSVs, treating empty strings as NaN
    df_companies = pd.read_csv(filepath_or_buffer='test/companies.csv', na_values=('', ' '))
    df_financial = pd.read_csv(filepath_or_buffer='test/financial.csv', na_values=('', ' '))

    # Replace NaN with None
    df_companies = df_companies.where(pd.notnull(df_companies), None)
    df_financial = df_financial.where(pd.notnull(df_financial), None)

    # Check if data already exists in the companies table
    if not session.query(Companies).first():
        try:
            # Add data to the database if the companies table is empty
            session.add_all([Companies(**row) for row in df_companies.to_dict(orient='records')])
            session.add_all([Financial(**row) for row in df_financial.to_dict(orient='records')])
            session.commit()
            # print("Data added to database.")
        except IntegrityError:
            # Rollback if there's an error (for example, duplicate entries)
            session.rollback()
            # print("Data already exists in the database, skipping data insertion.")

    print('Welcome to the Investor Program!\n')

    calculator = Calculator(session=session)
    while True:
        calculator.main_menu.run()


if __name__ == '__main__':
    main()
