from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)


server = 'SEU_SERVIDOR'
database = 'SEU_BANCO_DE_DADOS'
username = 'SEU_USUARIO'
password = 'SUA_SENHA'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn


@app.route('/')
def index():
    return "Sistema de Controle de Produtos"

if __name__ == '__main__':
    app.run(debug=True)
