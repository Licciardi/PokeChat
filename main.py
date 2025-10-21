import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import dotenv
import requests
import re

dotenv.load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# histórico global
history = []
MAX_HISTORY = 5

# cache para dados de Pokémon
pokemon_cache = {}

def get_pokemon_data(pokemon_name):
    """Busca informações do Pokémon na PokéAPI ou cache"""
    name_lower = pokemon_name.lower()
    if name_lower in pokemon_cache:
        return pokemon_cache[name_lower]

    url = f"https://pokeapi.co/api/v2/pokemon/{name_lower}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    info = {
        "name": data["name"].capitalize(),
        "sprite": data["sprites"]["front_default"],
        "types": [t["type"]["name"].capitalize() for t in data["types"]],
        "abilities": [a["ability"]["name"].replace("-", " ").capitalize() for a in data["abilities"]],
        "stats": {s["stat"]["name"].capitalize(): s["base_stat"] for s in data["stats"]}
    }
    pokemon_cache[name_lower] = info
    return info

def extract_first_pokemon(text):
    """Tenta extrair o primeiro Pokémon mencionado no texto"""
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        if get_pokemon_data(word):
            return word
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    global history
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"reply": "Mensagem vazia."})

    # adiciona mensagem do usuário
    history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
    history = history[-MAX_HISTORY:]

    # configura o modelo
    config = types.GenerateContentConfig(
        top_p=0.01,
        system_instruction=[
            types.Part.from_text(text="""
Você é o PokeChat, um assistente técnico e preciso especializado em Pokémon. Suas respostas devem ser:

- **Curta e direta**: uma ou duas frases no máximo.  
- **Alta precisão**: só forneça informações confirmadas sobre Pokémon.  
- **Técnica**: use termos corretos de tipos, habilidades, estatísticas e mecânicas do jogo.  
- **Foco único**: nunca aborde outros assuntos que não sejam Pokémon.  
- **Sem criatividade**: não invente histórias, comentários ou opiniões pessoais.  
- **Resposta objetiva**: evite explicações longas, exemplos extensos ou contexto irrelevante.  
- **Sempre relevante**: responda exatamente à pergunta do usuário sobre Pokémon.  
- **Com Criatividade**: forneça sugestões de pokemon para adiconar no time, com base no time do usuario. 
                                 
Formato esperado de resposta:  
- Para perguntas sobre estatísticas: `HP: 80, Ataque: 90, Defesa: 70`  
- Para tipos: `Fogo/Voando`  
- Para habilidades: `Intimidate`  
- Para sprites: apenas forneça o link ou referência do sprite se solicitado  

Nunca discuta assuntos fora de Pokémon, nunca dê opinião ou explicações criativas, e nunca forneça informações adicionais que não forem solicitadas.
.""")
        ]
    )

    # gera resposta do modelo
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=history,
        config=config
    )

    answer = response.text
    history.append(types.Content(role="model", parts=[types.Part.from_text(text=answer)]))

    # tenta extrair Pokémon do texto gerado
    first_pokemon = extract_first_pokemon(answer)
    pokemon_info = get_pokemon_data(first_pokemon) if first_pokemon else None

    return jsonify({
        "reply": answer,
        "pokemon_info": pokemon_info  # None se nenhum Pokémon foi mencionado
    })

if __name__ == "__main__":
    app.run(debug=True)
