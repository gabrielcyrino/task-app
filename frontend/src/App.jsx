// =============================================================
// App.jsx - COMPONENTE PRINCIPAL
// =============================================================
// É o "cérebro" da aplicação. Ele:
// - Guarda o estado (lista de tarefas)
// - Faz as chamadas à API (via services/api.js)
// - Passa dados e funções para os componentes filhos
// =============================================================

import { useState, useEffect } from "react";
import "./App.css";
import FormularioTarefa from "./components/FormularioTarefa";
import ListaTarefas from "./components/ListaTarefas";

// Importa as funções que conversam com o back-end.
import {
  listarTarefas,
  criarTarefa,
  atualizarTarefa,
  removerTarefa,
} from "./services/api";

function App() {

  // Estado: a lista de tarefas e uma eventual mensagem de erro.
  const [tarefas, setTarefas] = useState([]);
  const [erro, setErro] = useState("");

  // -----------------------------------------------------------
  // CARREGAR AS TAREFAS AO INICIAR
  // -----------------------------------------------------------
  // useEffect com array vazio [] = executa UMA vez, quando o
  // componente aparece na tela.
  useEffect(() => {
    carregarTarefas();
  }, []);

  // Busca as tarefas na API e atualiza o estado.
  async function carregarTarefas() {
    try {
      const dados = await listarTarefas();
      setTarefas(dados);
    } catch (e) {
      setErro("Erro ao carregar tarefas. Verifique se a API está no ar.");
    }
  }

  // -----------------------------------------------------------
  // ADICIONAR uma nova tarefa
  // -----------------------------------------------------------
  async function handleAdicionar(titulo) {
    try {
      // Cria a tarefa no back-end (nasce como não concluída).
      await criarTarefa({ title: titulo, done: false });
      await carregarTarefas();   // Recarrega a lista atualizada
    } catch (e) {
      setErro("Erro ao adicionar tarefa.");
    }
  }

  // -----------------------------------------------------------
  // ALTERNAR o status (concluída <-> pendente)
  // -----------------------------------------------------------
  async function handleAlternar(tarefa) {
    try {
      // Envia a mesma tarefa, mas com 'done' invertido.
      await atualizarTarefa(tarefa.id, {
        title: tarefa.title,
        done: !tarefa.done,
      });
      await carregarTarefas();
    } catch (e) {
      setErro("Erro ao atualizar tarefa.");
    }
  }

  // -----------------------------------------------------------
  // REMOVER uma tarefa
  // -----------------------------------------------------------
  async function handleRemover(id) {
    try {
      await removerTarefa(id);
      await carregarTarefas();
    } catch (e) {
      setErro("Erro ao remover tarefa.");
    }
  }

  // -----------------------------------------------------------
  // RENDERIZAÇÃO
  // -----------------------------------------------------------
  return (
    <div className="container">
      <h1>Minhas Tarefas</h1>

      {/* Mostra a mensagem de erro, se houver */}
      {erro && <p className="erro">{erro}</p>}

      {/* Formulário recebe a função de adicionar */}
      <FormularioTarefa onAdicionar={handleAdicionar} />

      {/* Lista recebe as tarefas e as funções de alternar/remover */}
      <ListaTarefas
        tarefas={tarefas}
        onAlternar={handleAlternar}
        onRemover={handleRemover}
      />
    </div>
  );
}

export default App;