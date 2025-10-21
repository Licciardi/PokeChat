document.addEventListener("DOMContentLoaded", () => {
  const sendButton = document.getElementById("sendButton");
  const input = document.getElementById("messageInput");
  const messagesArea = document.getElementById("messagesArea");
  const infoContent = document.getElementById("infoContent");

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    // Mostra mensagem do usuário
    messagesArea.innerHTML += `
      <div class="message user-message slide-in-right">
        <p>${message}</p>
      </div>
    `;
    input.value = "";
    messagesArea.scrollTop = messagesArea.scrollHeight;

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      // Mostra resposta do bot
      messagesArea.innerHTML += `
        <div class="message bot-message slide-in-left">
          <div class="bot-header">
            <div class="pokeball-icon"><div class="pokeball-center"></div></div>
            <span class="bot-label">POKÉDEX</span>
          </div>
          <p>${data.reply}</p>
        </div>
      `;
      messagesArea.scrollTop = messagesArea.scrollHeight;

      // Mostra informações do Pokémon se houver
      if (data.pokemon_info) {
        showPokemonInfo(data.pokemon_info);
      }

    } catch (error) {
      console.error("Erro ao enviar:", error);
      messagesArea.innerHTML += `<p class="error">Erro na conexão com o servidor.</p>`;
    }
  }

  sendButton.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

 function showPokemonInfo(pokemon) {
    infoContent.innerHTML = `
      <div class="pokemon-card fade-in">
          <div class="pokemon-sprite">
              <img src="${pokemon.sprite}" alt="${pokemon.name}">
          </div>
          
          <div class="pokemon-name">
              <h3>${pokemon.name}</h3>
              <p class="pokemon-id">Nº ${String(pokemon.id || "").padStart(3, '0')}</p>
          </div>
          
          <div class="info-section">
              <h4 class="section-title">Tipos</h4>
              <div class="types-container">
                  ${pokemon.types.map(type => `
                      <span class="type-badge type-${type.toLowerCase()}">${type}</span>
                  `).join('')}
              </div>
          </div>
          
          <div class="info-section">
              <h4 class="section-title">Habilidades</h4>
              <div class="abilities-box">
                  ${pokemon.abilities.map(ability => `
                      <div class="ability-item">• ${ability}</div>
                  `).join('')}
              </div>
          </div>
          
          <div class="info-section">
              <h4 class="section-title">Estatísticas Base</h4>
              ${Object.entries(pokemon.stats).map(([stat, value]) => `
                  <div class="stat-item">
                      <div class="stat-header">
                          <span class="stat-name">${stat.toUpperCase()}</span>
                          <span class="stat-value">${value}</span>
                      </div>
                      <div class="stat-bar">
                          <div class="stat-fill" style="width: ${(value / 150) * 100}%"></div>
                      </div>
                  </div>
              `).join('')}
          </div>
      </div>
    `;
}

});
