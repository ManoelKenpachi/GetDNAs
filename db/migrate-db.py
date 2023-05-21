import sqlite3

# Conectar-se ao banco de dados DNAs_Motorbooks1
conn_db1 = sqlite3.connect('DNAs_Motorbooks1.db')
cursor_db1 = conn_db1.cursor()

# Obter a lista de tabelas do DNAs_Motorbooks1
cursor_db1.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables_db1 = cursor_db1.fetchall()

# Conectar-se ao banco de dados DNAs_Motorbooks2
conn_db2 = sqlite3.connect('DNAs_Motorbooks2.db')
cursor_db2 = conn_db2.cursor()

# Obter a lista de tabelas do DNAs_Motorbooks2
cursor_db2.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables_db2 = cursor_db2.fetchall()

# Criar o banco de dados DNAs_Motorbooks.db
conn_db3 = sqlite3.connect('DNAs_Motorbooks.db')
cursor_db3 = conn_db3.cursor()

# Iterar sobre as tabelas do DNAs_Motorbooks1
for table in tables_db1:
    table_name = table[0]
    create_table_query = cursor_db1.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    create_table_query = create_table_query.fetchone()[0]
    create_table_query = create_table_query.replace(table_name, f'DNAs_Motorbooks.{table_name}')
    cursor_db3.execute(create_table_query)

# Iterar sobre as tabelas do DNAs_Motorbooks2
for table in tables_db2:
    table_name = table[0]
    create_table_query = cursor_db2.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    create_table_query = create_table_query.fetchone()[0]
    create_table_query = create_table_query.replace(table_name, f'DNAs_Motorbooks.{table_name}')
    cursor_db3.execute(create_table_query)

# Fechar as conexões e salvar as alterações
conn_db1.close()
conn_db2.close()
conn_db3.commit()
conn_db3.close()
