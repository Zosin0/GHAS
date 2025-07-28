# --- SECRETS GENÉRICAS PARA DETECÇÃO ---

# 1. PostgreSQL Connection String
# Formato padrão: postgresql://[user]:[password]@[host]:[port]/[database]
postgres_connection_string = "postgresql://db_user_postgres:Pg_S3cr3t_P4ss@db.internal.example.com:5432/production_db"

# 2. MySQL Connection String
# Formato padrão: mysql://[user]:[password]@[host]:[port]/[database]
mysql_connection_string = "mysql://db_user_mysql:My_S3cr3t_P4ss@10.0.0.12:3306/main_database"

# 3. MongoDB Connection String
# Formato padrão: mongodb+srv://[user]:[password]@[cluster]/[database]
mongodb_connection_string = "mongodb+srv://mongo_user:Mongo_S3cr3t_P4ss@cluster0.abcde.mongodb.net/app_data?retryWrites=true&w=majority"
