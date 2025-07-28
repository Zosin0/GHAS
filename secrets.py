# --- MySQL ---
mysql_connection_uri = "mysql://myhost:1234@myapplicationuser:3306/es_extended?charset=utf8mb4"
mysql_connection_kvp = "user=root;password=12345;host=localhost;port=3306;database=es_extended;charset=utf8mb4"
mysql --host=myhost --port=1234 --user=myapplicationuser --password applicationdb
my_uris = """
jdbc:mysql://myhost1:1111,myhost2:2222/db
jdbc:mysql://address=(host=myhost1)(port=1111)(key1=value1),address=(host=myhost2)(port=2222)(key2=value2)/db
jdbc:mysql://(host=myhost1,port=1111,key1=value1),(host=myhost2,port=2222,key2=value2)/db
jdbc:mysql://myhost1:1111,(host=myhost2,port=2222,key2=value2)/db
mysqlx://(address=host1:1111,priority=1,key1=value1),(address=host2:2222,priority=2,key2=value2)/db
jdbc:mysql://(host=myhost1,port=1111),(host=myhost2,port=2222)/db?key1=value1&key2=value2&key3=value3
"""
# --- MongoDB ---
mongodb_connection_uri = "mongodb+srv://root:12345@cluster0.abcde.mongodb.net/es_extended?retryWrites=true&w=majority"
mongodb_local_connection_uri = "mongodb://root:12345@localhost:27017/es_extended"

# --- PostgreSQL ---
postgres_connection_uri = "postgresql://root:12345@localhost:5432/es_extended"
postgres_connection_kvp = "user=root password=12345 host=localhost port=5432 dbname=es_extended"
ptcn = "postgresql://sally:sallyspassword@dbserver.example:5555/userdata?connect_timeout=10&sslmode=require&target_session_attrs=primary"


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
