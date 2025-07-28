# --- MySQL ---
mysql_connection_uri = "mysql://root:12345@localhost:3306/es_extended?charset=utf8mb4"
mysql_connection_kvp = "user=root;password=12345;host=localhost;port=3306;database=es_extended;charset=utf8mb4"

# --- MongoDB ---
mongodb_connection_uri = "mongodb+srv://root:12345@cluster0.abcde.mongodb.net/es_extended?retryWrites=true&w=majority"
mongodb_local_connection_uri = "mongodb://root:12345@localhost:27017/es_extended"

# --- PostgreSQL ---
postgres_connection_uri = "postgresql://root:12345@localhost:5432/es_extended"
postgres_connection_kvp = "user=root password=12345 host=localhost port=5432 dbname=es_extended"

# Imprimir todas as conexões para verificação
print("--- MySQL ---")
print(f"URI: {mysql_connection_uri}")
print(f"Chave-Valor: {mysql_connection_kvp}\n")

print("--- MongoDB ---")
print(f"URI (Atlas/Cluster): {mongodb_connection_uri}")
print(f"URI (Local): {mongodb_local_connection_uri}\n")

print("--- PostgreSQL ---")
print(f"URI: {postgres_connection_uri}")
print(f"Chave-Valor: {postgres_connection_kvp}")
