# Projeto TRABALHO PRÁTICO 3

## 📌 Descrição
Este projeto utiliza FastAPI para criar uma API que gerencia informações astronômicas, incluindo astrônomos, estrelas, exoplanetas, fenômenos celestes, observações, planetas e telescópios.

## 🚀 Tecnologias Utilizadas
- **Python**
- **FastAPI**
- **MongoDB** 

## 📁 Estrutura do Projeto
```
TRABALHOPRATICO3/
│-- app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py
│   ├── models/
│   ├── routers/
│   ├── main.py
│   ├── routes.py
│-- .env
│-- .gitignore
│-- README.md
│-- Relatório do Trabalho Prático 3
```

## ⚙️ Configuração do Banco de Dados
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
# MongoDB 
MONGO_URI=mongodb://usuario:senha@localhost:27017
DB_NAME=nome_do_banco
```

## 🛠️ Como Executar o Projeto
1. Clone o repositório:
   ```bash
   git clone https://github.com/AndressaLColares/TrabalhoPratico3.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd trabalhopratico3
   cd app
   ```
3. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Execute a aplicação:
   ```bash
   python -m uvicorn main:app --reload
   ```
6. Acesse a documentação interativa em:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📌 Rotas Principais
| Método | Rota | Descrição |
|---------|------|-------------|
| GET | `/astronomos/` | Lista todos os astrônomos |
| POST | `/astronomos/` | Adiciona um novo astrônomo |
| GET | `/estrelas/` | Lista todas as estrelas |
| GET | `/planetas/` | Lista todos os planetas |
| GET | `/telescopios/` | Lista todos os telescópios |

Entre outros endpoints...


## 👥 Colaboradores
- **Andressa Colares - 471151**
- **Carlos Ryan Santos - 473007**

---

Caso tenha dúvidas, entre em contato ou abra uma issue no repositório! 🚀

