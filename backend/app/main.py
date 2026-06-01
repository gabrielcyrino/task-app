# =============================================================
# main.py - APLICAÇÃO E ROTAS DA API (To-Do)
# =============================================================
# Este é o coração da API: cria a aplicação FastAPI, configura
# o CORS (para o front-end poder chamar a API) e define as
# rotas CRUD que conversam com o banco via SQLAlchemy.
# =============================================================

import os                                              # Para ler variáveis de ambiente
from fastapi import FastAPI, Depends, HTTPException    # Framework, injeção de dependência e erros
from fastapi.middleware.cors import CORSMiddleware     # Middleware para liberar CORS
from sqlalchemy.orm import Session                     # Tipo da sessão do banco

from . import models, schemas                          # Nossos modelos e schemas
from .database import engine, get_db, Base             # Conexão e dependência de sessão


# -------------------------------------------------------------
# 1. CRIAÇÃO DAS TABELAS NO BANCO
# -------------------------------------------------------------
# Lê todos os modelos que herdam de Base e cria as tabelas
# correspondentes no banco, caso ainda não existam.
Base.metadata.create_all(bind=engine)


# -------------------------------------------------------------
# 2. CRIAÇÃO DA APLICAÇÃO
# -------------------------------------------------------------
# 'app' é a instância principal do FastAPI; é por meio dela que
# registramos as rotas (endpoints) da nossa API.
app = FastAPI(title="API To-Do")


# -------------------------------------------------------------
# 3. CONFIGURAÇÃO DO CORS
# -------------------------------------------------------------
# Por segurança, o navegador bloqueia chamadas entre origens
# diferentes (Same-Origin Policy). Como o front-end roda em
# OUTRA URL (localhost:5173 em dev, e o domínio do Vercel em
# produção), precisamos liberar essas origens via CORS.
#
# Lemos a lista de origens permitidas da variável de ambiente
# FRONTEND_URL (separadas por vírgula). Em desenvolvimento,
# se a variável não existir, liberamos o localhost do Vite.
frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:5173")
origens_permitidas = [url.strip() for url in frontend_urls.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,  # Origens do front-end (dev e produção)
    allow_credentials=True,            # Permite cookies/autenticação
    allow_methods=["*"],               # Libera todos os métodos HTTP
    allow_headers=["*"],               # Libera todos os cabeçalhos
)


# -------------------------------------------------------------
# 4. ROTAS DA API (Endpoints CRUD)
# -------------------------------------------------------------
# Repare no padrão: cada rota recebe 'db: Session = Depends(get_db)'.
# Isso pede ao FastAPI uma sessão de banco já aberta (e que será
# fechada automaticamente ao final da requisição).

# -------- GET: Listar todas as tarefas -----------------------
# response_model=list[schemas.TaskOut] → garante que a resposta
# terá o formato definido em TaskOut (e gera a documentação).
@app.get("/api/tasks", response_model=list[schemas.TaskOut])
def listar_tarefas(db: Session = Depends(get_db)):
    """Retorna todas as tarefas cadastradas."""
    return db.query(models.Task).all()   # SELECT * FROM tasks


# -------- POST: Criar uma nova tarefa ------------------------
# status_code=201 → código HTTP padrão para "recurso criado".
@app.post("/api/tasks", response_model=schemas.TaskOut, status_code=201)
def criar_tarefa(tarefa: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Cria uma nova tarefa e retorna o objeto criado (com id)."""
    nova = models.Task(title=tarefa.title, done=tarefa.done)  # Cria o objeto ORM
    db.add(nova)        # Marca para inserção
    db.commit()         # Confirma a gravação no banco
    db.refresh(nova)    # Recarrega a tarefa já com o id gerado
    return nova         # Retorna a tarefa criada


# -------- PUT: Atualizar uma tarefa existente ----------------
# O id vem na URL; os novos dados vêm no corpo da requisição.
@app.put("/api/tasks/{tarefa_id}", response_model=schemas.TaskOut)
def atualizar_tarefa(
    tarefa_id: int,
    dados: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    """Atualiza o título e/ou o status de uma tarefa."""
    # Busca a tarefa pelo id.
    tarefa = db.query(models.Task).filter(models.Task.id == tarefa_id).first()
    # Se não existir, retorna erro 404.
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    # Atualiza os campos com os novos valores.
    tarefa.title = dados.title
    tarefa.done = dados.done
    db.commit()          # Confirma a alteração
    db.refresh(tarefa)   # Recarrega os dados atualizados
    return tarefa


# -------- DELETE: Remover uma tarefa -------------------------
# status_code=204 → "sucesso, sem conteúdo para retornar".
@app.delete("/api/tasks/{tarefa_id}", status_code=204)
def remover_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Remove uma tarefa pelo id."""
    tarefa = db.query(models.Task).filter(models.Task.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)   # Marca para remoção
    db.commit()         # Confirma a remoção
    # Não retornamos corpo: a resposta 204 não tem conteúdo.