# =============================================================
# database.py - CONFIGURAÇÃO DA CONEXÃO COM O BANCO
# =============================================================
# Este arquivo concentra TODA a configuração de acesso ao banco.
# Em produção (Render) usamos PostgreSQL; para testar localmente
# é possível usar SQLite apenas descomentando uma linha.
# =============================================================

import os                                              # Para ler variáveis de ambiente
from sqlalchemy import create_engine                   # Cria o "motor" de conexão
from sqlalchemy.orm import sessionmaker, declarative_base  # Sessões e classe-base dos modelos


# -------------------------------------------------------------
# 1. URL DE CONEXÃO COM O BANCO
# -------------------------------------------------------------
# Em produção, a variável de ambiente DATABASE_URL é definida
# pelo Render automaticamente, apontando para o PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL")

# --- TESTE LOCAL COM SQLITE (opcional) -----------------------
# Se quiser testar SEM instalar o PostgreSQL, comente a linha
# acima e descomente a linha abaixo: o SQLite cria um arquivo
# 'test.db' na pasta do projeto, sem precisar de servidor algum.
#DATABASE_URL = "sqlite:///./test.db"

# O Render às vezes entrega a URL começando com "postgres://",
# mas o SQLAlchemy moderno espera "postgresql://". Ajustamos aqui
# para evitar erro de driver.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# -------------------------------------------------------------
# 2. CRIAÇÃO DO "ENGINE" (motor de conexão)
# -------------------------------------------------------------
# O SQLite precisa de um argumento extra (check_same_thread=False)
# para funcionar bem com o FastAPI, que usa várias threads.
# O PostgreSQL NÃO precisa disso, então só ativamos para SQLite.
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL and "sqlite" in DATABASE_URL
    else {}
)

# O 'engine' é o objeto central que sabe conversar com o banco.
engine = create_engine(DATABASE_URL, connect_args=connect_args)


# -------------------------------------------------------------
# 3. FÁBRICA DE SESSÕES
# -------------------------------------------------------------
# Cada requisição abre uma "sessão" para conversar com o banco.
# A sessão é o canal por onde fazemos consultas e gravações.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -------------------------------------------------------------
# 4. CLASSE-BASE DOS MODELOS
# -------------------------------------------------------------
# Todos os modelos (tabelas) herdarão desta classe Base.
# É assim que o SQLAlchemy sabe quais tabelas precisa criar.
Base = declarative_base()


# -------------------------------------------------------------
# 5. DEPENDÊNCIA PARA OBTER UMA SESSÃO DO BANCO
# -------------------------------------------------------------
# Esta função "entrega" uma sessão para cada rota que precisar
# e garante que ela seja FECHADA ao final, mesmo se der erro.
# O FastAPI a usa via Depends(get_db) nas rotas (ver main.py).
def get_db():
    db = SessionLocal()      # Abre uma nova sessão
    try:
        yield db             # Entrega a sessão para a rota usar
    finally:
        db.close()           # Sempre fecha a sessão no final