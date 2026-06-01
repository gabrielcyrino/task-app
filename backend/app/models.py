# =============================================================
# models.py - MODELO ORM (a tabela do banco)
# =============================================================
# Aqui descrevemos a tabela 'tasks' como uma CLASSE Python.
# O SQLAlchemy traduz essa classe em comandos SQL por nós:
# não precisamos escrever SQL manualmente.
# =============================================================

from sqlalchemy import Column, Integer, String, Boolean  # Tipos de coluna
from .database import Base                                # Classe-base definida no database.py


# Cada classe que herda de Base representa UMA tabela.
class Task(Base):
    # Nome da tabela que será criada no banco.
    __tablename__ = "tasks"

    # id: chave primária, número inteiro que se autoincrementa.
    #   primary_key=True  → identifica unicamente cada linha
    #   index=True        → cria índice para buscas mais rápidas
    id = Column(Integer, primary_key=True, index=True)

    # title: o texto da tarefa (obrigatório, não pode ser nulo).
    title = Column(String, nullable=False)

    # done: indica se a tarefa foi concluída.
    #   default=False → toda tarefa nasce como "não concluída"
    done = Column(Boolean, default=False)