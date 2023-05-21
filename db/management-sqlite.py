import csv
import sqlite3

def drop_table(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table}")
        conn.commit()
        print(f"The table '{table}' has been dropped successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def csv_to_sqlite(conn, csv_file, table_name):
    cursor = conn.cursor()

    # Ler o arquivo CSV
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Ler o cabeçalho do CSV

        # Criar a tabela no SQLite baseado no cabeçalho do CSV
        columns = ', '.join(header)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(create_table_query)

        # Inserir os dados do CSV na tabela
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['?'] * len(header))})"
        for row in csv_reader:
            cursor.execute(insert_query, row)

    # Confirmar as alterações no banco de dados
    conn.commit()

def model_table(table_name, fields):
    # Criar a instrução SQL para a criação da tabela
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    # Adicionar os campos à instrução SQL
    for field in fields:
        sql += f"{field} TEXT,"
    
    # Remover a vírgula extra no final
    sql = sql.rstrip(',') + ")"

    # Conectar-se ao banco de dados
    conn = sqlite3.connect('DNAs_Motorbooks1.db')

    # Executar a instrução SQL para criar a tabela
    cursor = conn.cursor()
    cursor.execute(sql)

    # Fechar a conexão com o banco de dados
    conn.close()


# Exemplo de uso:
database_file = 'DNAs_Motorbooks2.db'
csv_file = 'dna_1.csv'
table_name = 'dados'

# Conectar-se ao banco de dados
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

lista_estranha = ['Intake_Manifold',
'Exhaust_Manifold',
'Flywheel',
'Flywheel_Bolt_Sealer',
'Flywheel_Surfacing',
'Damper',
'Damper_Bolt_Sealer',
'Main_Bearing_Cap',
'Additional_Main_Cap_Bolts',
'Connecting_Rod',
'Cylinder_Head',
'Camshaft_Cap_Torque',
'Camshaft_Gear_Bolt',
'Comments']

# drop_table(conn, 'CONNECTIONG_ROD')
# Importar o CSV para o SQLite
# model_table('TORQUE_SPEC', lista_estranha)

# Executar a consulta para listar todas as tabelas do banco de dados
tabelas = ['CASTING', 'VALVE', 'VALVE_SPRING', 'ROCKER_SHAFT', 'INSTALLATION', 'CYLINDER_BLOCK', 'PISTON', 'HOUSING_BORE', 'CYLINDER_SLEEVE']

tabelas_con = []

drop_table(conn, 'tabela')

for tabela in tabelas:
    colunas_table = []
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = cursor.fetchall()
    for coluna in colunas:
        colunas_table.append(coluna[1])

    model_table(tabela, colunas_table)
    


print(tabelas_con)
# Exibir o nome das colunas
# for coluna in colunas:
#     nome_coluna = coluna[1]
#     print(nome_coluna)

# Fechar a conexão com o banco de dados
conn.close()
