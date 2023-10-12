import os

import reflex as rx
from urllib.parse import quote_plus

pw = os.environ["MY_PASSWORD"]
params = quote_plus(
    rf'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:reflex-db.database.windows.net,1433;Database=reflex_db;Uid=smj02@reflex-db.database.windows.net;Pwd={pw};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = f'mssql+pyodbc:///?odbc_connect={params}'

config = rx.Config(
    app_name="index",
    db_url=conn_str
)
