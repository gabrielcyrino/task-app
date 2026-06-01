// =============================================================
// FormularioTarefa.jsx - CAMPO PARA ADICIONAR UMA TAREFA
// =============================================================
// Componente simples responsável por:
// - Exibir um campo de texto e um botão "Adicionar"
// - Enviar o título digitado ao componente pai (App)
// =============================================================

import { useState } from "react";

// Recebe 1 prop do pai:
// - onAdicionar: função chamada quando o formulário é enviado
function FormularioTarefa({ onAdicionar }) {

  // Estado que guarda o texto digitado no campo.
  const [titulo, setTitulo] = useState("");

  // Função executada ao enviar o formulário.
  function handleSubmit(evento) {
    evento.preventDefault();         // Impede o recarregamento da página

    // Ignora envios vazios (só espaços).
    if (titulo.trim() === "") return;

    onAdicionar(titulo);             // Avisa o pai que há uma nova tarefa
    setTitulo("");                   // Limpa o campo após adicionar
  }

  return (
    <form className="formulario" onSubmit={handleSubmit}>
      {/* Campo de texto controlado pelo estado 'titulo' */}
      <input
        type="text"
        placeholder="O que precisa ser feito?"
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
      />
      <button type="submit">Adicionar</button>
    </form>
  );
}

export default FormularioTarefa;