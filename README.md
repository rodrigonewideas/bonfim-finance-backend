

# Bonfim Finance Backend

Backend da aplicação de consulta financeira e cobrança, desenvolvido em **Python** com **FastAPI**.

> **Projeto privado** — código proprietário para controle, consulta e exportação de informações financeiras da base de dados do Cemitério Bonfim.

---

## Funcionalidades

- Consulta de recebíveis e contratos via API REST.
- Filtros avançados por data de pagamento, vencimento, nome, CNPJ, contrato, etc.
- Exportação dos dados filtrados em Excel (XLSX).
- Autenticação básica HTTP (ou JWT, se configurado).
- Estrutura preparada para integração com frontend React ou outros sistemas.
- Modularização para fácil manutenção e evolução.

---

## Requisitos

- Python 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Firebird ou PostgreSQL (ajustar conforme seu projeto)
- Virtualenv ou similar

Instale as dependências com:

```bash
pip install -r requirements.txt

Como rodar o backend localmente

    Clone o repositório:

git clone https://github.com/rodrigonewideas/bonfim-finance-backend.git
cd bonfim-finance-backend

Crie o ambiente virtual e ative:

python -m venv cobranca-venv
source cobranca-venv/bin/activate  # Linux/macOS
# ou
cobranca-venv\Scripts\activate     # Windows

Instale as dependências:

pip install -r requirements.txt

Configure variáveis de ambiente
Copie ou crie um arquivo .env com suas credenciais, por exemplo:

DB_HOST=localhost
DB_USER=SYSDBA
DB_PASS=xxxxxx
DB_NAME=CAMINHO_PARA_O_BANCO.FDB

Execute o servidor:

    uvicorn main:app --reload --host 0.0.0.0 --port 8010

Estrutura dos diretórios

bonfim-finance-backend/
│
├── main.py                # Ponto de entrada FastAPI
├── routes_cobranca.py     # Rotas da API de cobrança
├── requirements.txt
├── README.md
├── .env                   # NÃO subir para o git!
├── cobranca-venv/         # Ambiente virtual (ignorar)
└── ...

Endpoints principais

    GET /api/cobranca/consulta: Consulta de recebíveis/contratos com filtros.

    GET /api/cobranca/consulta_xlsx: Exportação dos dados filtrados em Excel.

    (Adicionar outros endpoints conforme evolução do projeto...)

Observações

    Este repositório é privado e o uso do código é restrito ao projeto do Cemitério Bonfim.

    Dados sensíveis como senhas e arquivos .env não devem ser versionados.

    Para dúvidas ou solicitações, fale com Rodrigo de Paula Soares.

TODOs futuros

    Implementar autenticação JWT.

    Adicionar testes automatizados.

    Documentar todos os endpoints via OpenAPI/Swagger.


Se quiser personalizar algum trecho (por exemplo, incluir instruções para outro banco, explicar endpoints específicos ou citar contato diferente), me avise!  
Caso prefira, posso também gerar o arquivo pronto para colar direto no seu projeto.

Você disse:
voce tem todas as informações do projeto. Como podemos incluir no readme? 
O ChatGPT disse:

Excelente pergunta! Com base no histórico das conversas e no seu projeto, posso montar um README bem mais rico e personalizado, com informações sobre:

    Contexto do sistema (controle financeiro e cobrança do Cemitério Bonfim)

    Stack utilizada (Python, FastAPI, Firebird, integração com frontend React/Vite)

    Organização de código, segurança, práticas e fluxo de trabalho

    Explicações dos principais endpoints e exemplos de uso

    Orientações sobre deploy, .env, backup, contribuições, e até visão futura

Veja abaixo um exemplo de README.md completo e contextualizado para seu projeto. Sinta-se à vontade para editar o que achar necessário.

# Bonfim Finance Backend

Backend de consulta e gestão financeira para o projeto Cemitério Bonfim, desenvolvido em Python com FastAPI, integrado ao banco de dados Firebird.

## 🏢 Sobre o projeto

O **Bonfim Finance Backend** é a API responsável por toda a lógica de consulta, exportação e filtragem dos dados financeiros do Cemitério Bonfim, atendendo às demandas administrativas, de cobrança, auditoria e integração com o painel React/Vite do projeto.

---

## 🚀 Funcionalidades

- Consulta de recebíveis e contratos por API REST
- Filtros robustos: datas de pagamento/vencimento, nome, CNPJ, número do contrato
- Exportação dos resultados em Excel (.xlsx) com macro customizada
- Autenticação HTTP básica (e preparada para JWT)
- Integração transparente com frontend React/Vite/Tailwind (projeto bonfim-finance-viewer)
- Estrutura modular, pronta para novas integrações (Power BI, dashboards, etc)
- Suporte a logs de importação, controle de duplicidade e auditoria

---

## 🔧 Stack e dependências

- **Python 3.10+**
- **FastAPI** — estrutura principal da API
- **Uvicorn** — servidor ASGI
- **Firebird** — banco de dados legado (versão 1.5+)
- **PyODBC** — driver de conexão ao Firebird
- **Pandas, Openpyxl** — manipulação e exportação Excel
- **dotenv** — variáveis sensíveis em `.env`

Instale todas as dependências:

```bash
pip install -r requirements.txt

📁 Organização dos arquivos

bonfim-finance-backend/
│
├── main.py                   # Ponto de entrada FastAPI
├── routes_cobranca.py        # Rotas específicas da API de cobrança
├── requirements.txt
├── README.md
├── .env                      # Configurações sensíveis (NÃO versionar!)
├── cobranca-venv/            # Ambiente virtual Python
├── scripts/                  # Scripts auxiliares de importação e backup
└── ...

⚙️ Como executar

    Clone o repositório:

git clone https://github.com/rodrigonewideas/bonfim-finance-backend.git
cd bonfim-finance-backend

Crie e ative o ambiente virtual:

python -m venv cobranca-venv
source cobranca-venv/bin/activate  # Linux/macOS
cobranca-venv\Scripts\activate     # Windows

Instale as dependências:

pip install -r requirements.txt

Configure o arquivo .env:

FIREBIRD_HOST=localhost
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=xxxxxx
FIREBIRD_DB_PATH=/caminho/para/SEUBANCO.FDB
# Outras variáveis conforme necessidade

Inicie a API:

    uvicorn main:app --reload --host 0.0.0.0 --port 8010

    A API estará acessível em: http://localhost:8010

📌 Endpoints principais

    GET /api/cobranca/consulta
    Consulta contratos/recebíveis. Filtros por data, nome, CNPJ, contrato, etc.

    GET /api/cobranca/consulta_xlsx
    Exporta resultados para planilha Excel (.xlsx), incluindo macro para seleção automática de contas permitidas.

Exemplos de uso:

curl -u cobranca:bonfim2025@ "http://localhost:8010/api/cobranca/consulta?limite=10&nome=MARIA"

🔒 Segurança

    .env: Nunca envie para o repositório.

    Autenticação básica já configurada (usuário/senha em ambiente seguro).

    Pronto para autenticação via JWT se necessário.

📊 Integrações

    Frontend: Projeto React (bonfim-finance-viewer), consumo de endpoints via API REST.

    Excel: Exportação automática para integração com processos internos e auditoria.

    Futuro: Integração direta com Power BI, Supabase, automação via n8n.

📚 Contribuição

    Faça um fork desse repositório

    Crie sua branch: git checkout -b minha-feature

    Commit suas alterações: git commit -m 'feat: minha nova feature'

    Push para o seu fork: git push origin minha-feature

    Crie um Pull Request

🧑‍💻 Autor e contato

Projeto desenvolvido e mantido por Rodrigo de Paula Soares
Contato: LinkedIn | GitHub
📝 Licença

Projeto proprietário, uso restrito ao Cemitério Bonfim.
Entre em contato para novas integrações, consultorias ou parcerias.