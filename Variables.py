from dotenv import load_dotenv
import os

load_dotenv()


#login
varejo_user = os.getenv("VF_USER")
verejo_senha = os.getenv("VF_PASSWORD")

#banco
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", 3306)
user = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "")
database = os.getenv("DB_DATABASE")
