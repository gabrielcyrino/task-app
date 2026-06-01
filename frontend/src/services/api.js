// =============================================================
// api.js - COMUNICAÇÃO COM O BACK-END
// =============================================================
// Centraliza TODAS as chamadas HTTP à API FastAPI. Manter a
// comunicação isolada aqui facilita a manutenção: se a URL da
// API mudar, alteramos em um único lugar.
// Usamos a função 'fetch' nativa do navegador (sem bibliotecas).
// =============================================================

// Lê a URL base da API da variável de ambiente do Vite.
// Em dev vem do arquivo .env (localhost:8000); em produção,
// vem das configurações do Vercel (URL do Render).
// O '||' define um valor padrão caso a variável não exista.
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";


// -------------------------------------------------------------
// GET /api/tasks → Lista todas as tarefas
// -------------------------------------------------------------
export async function listarTarefas() {
  const resposta = await fetch(`${API_URL}/api/tasks`);
  // .json() converte o corpo da resposta (texto) em objeto JS.
  return await resposta.json();
}


// -------------------------------------------------------------
// POST /api/tasks → Cria uma nova tarefa
// Recebe um objeto { title, done }.
// -------------------------------------------------------------
export async function criarTarefa(tarefa) {
  const resposta = await fetch(`${API_URL}/api/tasks`, {
    method: "POST",                                  // Método HTTP
    headers: { "Content-Type": "application/json" }, // Avisamos que enviamos JSON
    body: JSON.stringify(tarefa),                    // Converte o objeto em texto JSON
  });
  return await resposta.json();
}


// -------------------------------------------------------------
// PUT /api/tasks/:id → Atualiza uma tarefa existente
// -------------------------------------------------------------
export async function atualizarTarefa(id, tarefa) {
  const resposta = await fetch(`${API_URL}/api/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(tarefa),
  });
  return await resposta.json();
}


// -------------------------------------------------------------
// DELETE /api/tasks/:id → Remove uma tarefa
// -------------------------------------------------------------
export async function removerTarefa(id) {
  await fetch(`${API_URL}/api/tasks/${id}`, { method: "DELETE" });
  // A resposta 204 não tem corpo, então não chamamos .json().
}