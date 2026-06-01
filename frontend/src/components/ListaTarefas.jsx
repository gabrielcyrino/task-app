// =============================================================
// ListaTarefas.jsx - EXIBIÇÃO DA LISTA DE TAREFAS
// =============================================================
// Mostra todas as tarefas, permitindo marcar como concluída
// (clicando no texto) e remover (botão "X").
// =============================================================

// Recebe 3 props do pai:
// - tarefas: array de tarefas a exibir
// - onAlternar: função chamada ao clicar para concluir/reabrir
// - onRemover: função chamada ao clicar em remover
function ListaTarefas({ tarefas, onAlternar, onRemover }) {

  // Se não houver tarefas, exibe uma mensagem amigável.
  if (tarefas.length === 0) {
    return <p className="aviso">Nenhuma tarefa cadastrada ainda.</p>;
  }

  return (
    <ul className="lista">
      {/* .map() percorre o array e gera um <li> para cada tarefa */}
      {tarefas.map((tarefa) => (
        // 'key' é obrigatório em listas React (ajuda na performance).
        <li key={tarefa.id} className="item">
          {/* Clicar no texto alterna entre concluída e pendente.
              A classe 'concluida' risca o texto via CSS. */}
          <span
            className={tarefa.done ? "concluida" : ""}
            onClick={() => onAlternar(tarefa)}
          >
            {tarefa.title}
          </span>

          {/* Botão de remover a tarefa */}
          <button
            className="btn-remover"
            onClick={() => onRemover(tarefa.id)}
          >
            ✕
          </button>
        </li>
      ))}
    </ul>
  );
}

export default ListaTarefas;