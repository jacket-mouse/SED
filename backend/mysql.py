import pandas as pd
from sqlalchemy import create_engine, text, inspect
import os

# MySQL配置
user = 'root'
password = 'admin123'
host = 'localhost'
database = 'security'

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
inspector = inspect(engine)

def db_import(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    table_name = os.path.basename(file_path)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"{os.path.basename(file_path)} has been successfully imported into MYSQL")

def get_columns(table_name):
    columns = inspector.get_columns(table_name)
    column_names = [column['name'] for column in columns]
    return column_names

def get_tables():
    tables = inspector.get_table_names()
    return tables

def fuzzy_query(table_name, value):
    results = []
    column_names = get_columns(table_name)
    for column_name in column_names:
        query = text(f"SELECT * FROM `{table_name}` WHERE {column_name} LIKE :value")
        with engine.connect() as connection:
            result = connection.execute(query, {"value": f"%{value}%"})
            for row in result:
                results.append(dict(row._mapping))
                # print(row)
    return results

def search(value):
    tables = get_tables()
    results = list()
    for table in tables:
        result = fuzzy_query(table, value)
        for r in result:
            results.append(r)
    return results


if __name__ == "__main__":
    file_path = "/Users/leeson/Documents/SED/backend/酒店开房数据库-B-200W-400W.csv"
    # db_import(file_path)
    # fuzzy_query(os.path.basename(file_path), "M")
    # print(os.path.basename(file_path))
    results = fuzzy_query(get_tables()[0], "江西省")
    # fuzzy_query(os.path.basename(file_path), "江西省")
    for result in results:
        print(result)
    for result in search("江西省"):
        print(result)