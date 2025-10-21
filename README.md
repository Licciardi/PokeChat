# 🕹️ PokeChat - Chat interativo da Pokédex

PokeChat é um chat interativo inspirado na Pokédex, utilizando **IA generativa do Google Gemini** para responder perguntas sobre Pokémon. As respostas podem variar, trazendo mais dinamismo e naturalidade à conversa. Além disso, ele integra a **PokéAPI** para exibir sprites, tipos, habilidades e estatísticas do primeiro Pokémon mencionado.

## 📌 Funcionalidades

* Conversa com o PokeChat usando **IA generativa**, com respostas diversificadas e realistas.
* Exibe informações detalhadas do **primeiro Pokémon citado**:

  * Sprite
  * Tipos
  * Habilidades
  * Estatísticas base (HP, Ataque, Defesa)
* Histórico de conversas limitado às últimas 5 mensagens.
* Interface interativa feita em **HTML, CSS e JavaScript**.
* Design responsivo inspirado na Pokédex.

## 🛠 Tecnologias utilizadas

| Tecnologia           | Uso                                             |
| -------------------- | ----------------------------------------------- |
| Python 3             | Backend e integração com APIs                   |
| Flask                | Framework web para criar o servidor e endpoints |
| Google Gemini API    | Geração de respostas dinâmicas sobre Pokémon    |
| Requests             | Requisições à PokéAPI                           |
| HTML5 & CSS3         | Estrutura e estilo do frontend                  |
| JavaScript (Vanilla) | Comunicação com backend e manipulação do DOM    |
| dotenv               | Gerenciamento de variáveis de ambiente          |
| PokéAPI              | Fonte de dados oficial dos Pokémon              |

## 🎓 Conhecimentos aplicados

* Integração com APIs externas (Google Gemini e PokéAPI)
* Uso de IA generativa para respostas dinâmicas
* Criação de SPA simples com Flask e Fetch API
* Extração de informações de texto para detectar nomes de Pokémon
* Manipulação dinâmica do DOM para exibir sprites, tipos, habilidades e stats
* Design responsivo com CSS Grid e Flexbox
* Boas práticas de segurança usando `.env`
* Versionamento e deploy com Git/GitHub

## 🚀 Como rodar o projeto

1. **Clonar o repositório**

```bash
git clone https://github.com/seu-usuario/pokechat.git
cd pokechat
```

2. **Criar e ativar ambiente virtual (opcional)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

3. **Instalar dependências**

```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto com sua chave da Google Gemini API:

```ini
GEMINI_API_KEY=sua_chave_aqui
```

5. **Rodar o servidor Flask**

```bash
python main.py
```

6. **Acessar no navegador**
   Abra [http://127.0.0.1:5000](http://127.0.0.1:5000)

Converse com o PokeChat e digite o nome de um Pokémon para ver suas informações.
