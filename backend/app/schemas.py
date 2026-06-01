# =============================================================
# schemas.py - CONTRATOS DE ENTRADA E SAÍDA (Pydantic)
# =============================================================
# "Schemas" definem o FORMATO dos dados que entram e saem da API.
# São diferentes do modelo ORM (models.py): o ORM fala com o
# banco; os schemas validam o JSON e geram a documentação.
# =============================================================

from pydantic import BaseModel   # Base para criar modelos de validação


# -------------------------------------------------------------
# SCHEMA DE ENTRADA (o que o cliente ENVIA ao criar/atualizar)
# -------------------------------------------------------------
# Repare que NÃO tem 'id': o id é gerado pelo banco, não pelo
# cliente. Aqui só pedimos o título e (opcionalmente) o status.
class TaskCreate(BaseModel):
    title: str            # Texto da tarefa (obrigatório)
    done: bool = False    # Status; se não vier, assume False


# -------------------------------------------------------------
# SCHEMA DE SAÍDA (o que a API RETORNA ao cliente)
# -------------------------------------------------------------
# Inclui o 'id' porque o cliente precisa saber qual id o banco
# atribuiu (para depois editar ou remover a tarefa).
class TaskOut(BaseModel):
    id: int
    title: str
    done: bool

    # Configuração que permite ao Pydantic ler dados direto de um
    # objeto ORM (a classe Task), e não apenas de um dicionário.
    # Em Pydantic v2 usa-se 'from_attributes = True'.
    class Config:
        from_attributes = True   # (no Pydantic v1 seria: orm_mode = True)