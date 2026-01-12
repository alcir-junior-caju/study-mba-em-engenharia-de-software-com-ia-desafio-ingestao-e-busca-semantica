# MBA em Engenharia de Software com IA - Desafio MBA Engenharia de Software com IA - Full Cycle

<div>
    <img alt="Criado por Alcir Junior [Caju]" src="https://img.shields.io/badge/criado%20por-Alcir Junior [Caju]-%23f08700">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-%23f08700">
</div>

---

## Descrição

Desafio: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector. Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

---

## Repositório Pai
https://github.com/alcir-junior-caju/study-mba-em-engenharia-de-software-com-ia

---

## Visualizar o projeto na IDE:

Para quem quiser visualizar o projeto na IDE clique no teclado a tecla `ponto`, esse recurso do GitHub é bem bacana

---

## Print:

<p align="center">
  <img alt="Ingest" src="_images/ingest.png" width="75%" style="margin: 15px 0" />
</p>

<p align="center">
  <img alt="Chat" src="_images/chat.png" width="75%" style="margin: 15px 0" />
</p>

<p align="center">
  <img alt="Search" src="_images/search.png" width="75%" style="margin: 15px 0" />
</p>

---

## 📋 Pré-requisitos

- **Docker e Docker Compose** - Para executar o PostgreSQL com pgVector
- **Python 3.11+** (recomendado 3.13) - Linguagem de programação
- **[uv](https://docs.astral.sh/uv/)** - Gerenciador de pacotes Python ultrarrápido
- **API Key do Google Gemini** - [Obter aqui](https://aistudio.google.com/app/apikey)

## Instalação do uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🚀 Setup e Uso da Aplicação

### Setup Rápido Automático

```bash
# 1. Executar script de setup automático
./setup.sh

# 2. Editar o arquivo .env e adicionar sua GOOGLE_API_KEY
nano .env  # ou use seu editor preferido

# 3. Subir o banco de dados
docker-compose up -d

# 4. Executar a ingestão do PDF (usando CLI)
uv run python src/cli.py ingest

# 5. Iniciar o chat interativo (usando CLI)
uv run python src/cli.py chat
```

### Setup Manual Passo a Passo

#### 1️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar e adicionar sua API Key do Gemini
# GOOGLE_API_KEY=sua-api-key-aqui
```

O arquivo `.env` deve conter:

```bash
# Google Gemini API (OBRIGATÓRIO)
GOOGLE_API_KEY=sua-chave-google
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# Configuração do Banco de Dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents

# Caminho do PDF para ingestão
PDF_PATH=./document.pdf
```

#### 2️⃣ Subir o Banco de Dados PostgreSQL

```bash
# Iniciar PostgreSQL com pgVector
docker-compose up -d

# Verificar se está rodando
docker-compose ps

# Ver logs (opcional)
docker-compose logs -f postgres
```

#### 3️⃣ Configurar Ambiente Python

```bash
# Criar ambiente virtual
uv venv

# Sincronizar dependências
uv sync

# Ativar ambiente (opcional - uv run funciona sem ativar)
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

#### 4️⃣ Executar Ingestão do PDF

```bash
# Processar e armazenar o PDF no banco de dados
# (usa PDF_PATH do arquivo .env)
uv run python src/cli.py ingest

# Ou especificar um PDF diferente:
uv run python src/cli.py ingest --pdf-path outro_documento.pdf
```

**Saída esperada:**

```
======================================================================
 INGESTÃO DE PDF
 Processando: document.pdf
======================================================================

ℹ️ Carregando PDF...
✅ PDF carregado: 5 página(s)

ℹ️ Dividindo documento em chunks...
✅ Documento dividido em 42 chunks

ℹ️ Configurando embeddings do Gemini...
✅ Embeddings configurados: models/embedding-001

ℹ️ Armazenando no banco de dados...
✅ Ingestão concluída! 42 chunks armazenados
ℹ️ Coleção: documents
```

#### 5️⃣ Usar o Chat Interativo

```bash
# Iniciar interface de chat
uv run python src/cli.py chat
```

**Exemplo de uso:**

```
======================================================================
 CHAT RAG INTERATIVO
 Digite 'sair' para encerrar
======================================================================

ℹ️ Inicializando sistema...
✅ Sistema pronto!

Exemplos de perguntas que foram testadas:
- Em que ano foi fundada a empresa Alfa Energia S.A.?
- Qual o faturamento da SuperTechIABrazil?
- Pode me dizer quantas empresas estão cadastradas?
- Traga a soma do faturamento de todas empresas cadastradas

💬 Você: sair

ℹ️ Encerrando chat...
```

## 🎯 Comandos da CLI

### Ver Ajuda

```bash
# Ajuda geral
uv run python src/cli.py --help

# Ajuda de comando específico
uv run python src/cli.py ingest --help
uv run python src/cli.py search --help
uv run python src/cli.py chat --help
```

### Comando: ingest

Ingere um PDF no banco de dados vetorial.

```bash
# Ingerir PDF (usa PDF_PATH do .env)
uv run python src/cli.py ingest

# Ou especificar um PDF diferente
uv run python src/cli.py ingest --pdf-path documento.pdf
uv run python src/cli.py ingest -p /path/to/file.pdf
```

### Comando: search

Busca documentos similares usando busca vetorial.

```bash
# Buscar com top-k padrão (10)
uv run python src/cli.py search "inteligência artificial"

# Especificar número de resultados
uv run python src/cli.py search "python" --top-k 5

# Ou usando a forma curta
uv run python src/cli.py search "machine learning" -k 15
```

### Comando: chat

Inicia chat interativo com RAG.

```bash
# Iniciar chat
uv run python src/cli.py chat
```

## 🎯 Características do Sistema RAG

- ✅ **CLI moderna e integrada** usando Typer + Rich
- ✅ **Chunks de 1000 caracteres** com overlap de 150
- ✅ **Embeddings usando Gemini** (models/embedding-001)
- ✅ **LLM usando Gemini 2.0 Flash Lite** para geração de respostas
- ✅ **Busca vetorial** com top 10 resultados mais relevantes (k=10)
- ✅ **Respostas baseadas apenas no contexto do PDF**
- ✅ **Detecção inteligente de perguntas fora do contexto**
- ✅ **PostgreSQL com pgVector** para armazenamento vetorial
- ✅ **Interface CLI interativa** para chat
- ✅ **Output formatado e colorido** com Rich

## 🔧 Comandos Úteis

### Gerenciamento do Banco de Dados

```bash
# Ver logs do banco
docker-compose logs -f postgres

# Parar o banco
docker-compose down

# Reiniciar o banco (limpar dados)
docker-compose down -v
docker-compose up -d
# Nota: Após reiniciar, execute a ingestão novamente
```

### Executar CLI

```bash
# Forma recomendada usando uv run
uv run python src/cli.py ingest document.pdf
uv run python src/cli.py search "texto"
uv run python src/cli.py chat
```

## ❓ Solução de Problemas

### ❌ Erro: "GOOGLE_API_KEY não encontrada"

**Solução:** Certifique-se de que o arquivo `.env` existe e contém a chave da API.

```bash
# Verificar se o arquivo existe
cat .env | grep GOOGLE_API_KEY

# Se não existir, criar a partir do exemplo
cp .env.example .env
# Depois edite e adicione sua chave
```

### ❌ Erro: "could not connect to server"

**Solução:** O banco de dados não está rodando.

```bash
# Iniciar o banco
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs para mais detalhes
docker-compose logs postgres
```

### ❌ Erro durante a ingestão

**Possíveis causas:**
1. Arquivo PDF não existe no caminho especificado
2. API Key do Gemini é inválida
3. Banco de dados não está acessível

**Soluções:**
```bash
# Verificar se o PDF existe
ls -la document.pdf

# Testar conexão com o banco
docker-compose exec postgres psql -U postgres -d rag -c "SELECT 1;"

# Verificar se a API Key está configurada
echo $GOOGLE_API_KEY  # Se ambiente ativado
# ou
cat .env | grep GOOGLE_API_KEY
```

### ❌ Chat retorna respostas vazias ou erro

**Solução:** Execute a ingestão novamente para garantir que os dados foram armazenados:

```bash
uv run python src/cli.py ingest
```

### ❌ Problemas com dependências

```bash
# Limpar e reinstalar dependências
rm -rf .venv
uv venv
uv sync
```

## Como executar

### Setup Rápido

```bash
# Configurar tudo automaticamente
./setup.sh
```

Este script irá:
- Verificar e instalar o `uv` se necessário
- Criar o ambiente virtual
- Instalar todas as dependências
- Criar o arquivo `.env` a partir do exemplo

### Comandos Detalhados

#### 1. Subir o banco de dados PostgreSQL com pgvector

```bash
docker-compose up -d
```

#### 2. Configurar o ambiente Python com uv

```bash
# Criar ambiente virtual
uv venv

# Sincronizar dependências
uv sync

# Ativar o ambiente virtual (opcional, uv run funciona sem ativar)
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

#### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha as variáveis:

```bash
cp .env.example .env
```

#### 4. Executar os scripts

```bash
# Executar comandos via CLI
uv run python src/cli.py ingest
uv run python src/cli.py search "texto de busca"
uv run python src/cli.py chat
```

## Interface de Linha de Comando (CLI)

O projeto utiliza uma **CLI moderna e integrada** usando **Typer** e **Rich** para uma experiência de usuário superior.

### Recursos da CLI

- ✅ **Comandos unificados**: `ingest`, `search` e `chat`
- ✅ Interface colorida e formatada com **Rich**
- ✅ Logs bonitos e informativos
- ✅ Renderização de Markdown no terminal
- ✅ Tabelas, painéis e progress bars
- ✅ Help automático e validação de argumentos
- ✅ Output consistente e profissional

### Comandos Disponíveis

```bash
# Ver ajuda geral
uv run python src/cli.py --help

# Ingerir PDF no banco de dados (usa PDF_PATH do .env)
uv run python src/cli.py ingest

# Ou especificar PDF diferente
uv run python src/cli.py ingest --pdf-path documento.pdf

# Buscar documentos similares
uv run python src/cli.py search "inteligência artificial"
uv run python src/cli.py search "python" --top-k 10

# Chat interativo com RAG
uv run python src/cli.py chat

# Ver ajuda de comando específico
uv run python src/cli.py ingest --help
uv run python src/cli.py search --help
uv run python src/cli.py chat --help
```

### Output Rico e Formatado

A CLI usa **Rich** para fornecer output profissional:

- **Logs coloridos** com ícones informativos (✅ ❌ ℹ️)
- **Progress bars** durante processamento
- **Tabelas** para exibir resultados de busca
- **Painéis** para destacar respostas do chat
- **Markdown renderizado** no terminal
- **Formatação consistente** em todos os comandos

## Estrutura do Projeto

```
.
├── docker-compose.yml      # Configuração do PostgreSQL com pgvector
├── pyproject.toml         # Configuração do projeto (dependências, metadados)
├── uv.lock                # Lock file de dependências
├── .python-version        # Versão do Python (3.13)
├── .env.example           # Exemplo de variáveis de ambiente
├── setup.sh               # Script de setup automático
├── README.md              # Este arquivo
├── docs/                  # Documentação adicional
│   ├── COMANDOS_UV.md    # Referência de comandos uv
│   ├── CONTEXTO.md       # Contexto do desafio
│   └── GUIA_CLI.md       # Guia completo da CLI
├── examples/              # Exemplos e demonstrações
│   └── cli_exemplos_avancados.py  # Exemplos avançados Rich
└── src/
    ├── cli.py            # ⭐ CLI principal (Typer + Rich)
    ├── cli_utils.py      # ⭐ Utilitários de CLI (Rich)
    └── search.py         # Lógica de busca vetorial e LLM
```

**Arquivos principais:**
- **cli.py** - Interface CLI unificada com 3 comandos: `ingest`, `search`, `chat`
- **cli_utils.py** - Funções auxiliares para formatação e logging com Rich
- **search.py** - Lógica de busca vetorial e LLM (usado internamente pela CLI)

## Arquivos de Configuração

### pyproject.toml
Arquivo principal de configuração do projeto usando o padrão PEP 518. Define:
- Metadados do projeto
- Dependências com versões fixadas
- Configuração de build com Hatchling
- Configuração do `uv`

### uv.lock
Lock file gerado automaticamente pelo `uv` que garante:
- Reprodutibilidade do ambiente
- Mesmas versões em diferentes máquinas
- Resolução consistente de dependências

### .python-version
Especifica a versão do Python a ser usada (3.13), permitindo que ferramentas como `uv` e `pyenv` selecionem automaticamente a versão correta.

## Vantagens do uv

- **Velocidade**: 10-100x mais rápido que pip
- **Consistência**: Resolução de dependências determinística com lock file
- **Simplicidade**: Interface unificada para gerenciamento de pacotes e ambientes
- **Moderno**: Suporta os padrões mais recentes do Python (PEP 518, 621, 631)
- **Reprodutível**: Lock file garante mesmas versões em qualquer ambiente

## 📖 Tecnologias Utilizadas

### Backend & Framework
- **Python 3.11+** - Linguagem de programação
- **LangChain** - Framework para aplicações com LLMs
- **LangChain Community** - Extensões e integrações

### Banco de Dados & Vetorial
- **PostgreSQL** - Banco de dados relacional
- **pgVector** - Extensão para busca vetorial
- **asyncpg** - Driver assíncrono para PostgreSQL

### IA & Embeddings
- **Google Gemini** - LLM para geração de respostas
  - Embeddings: `models/embedding-001`
  - LLM: `gemini-2.0-flash-lite`
- **langchain-google-genai** - Integração Gemini com LangChain

### Processamento de Documentos
- **PyPDF** - Leitura de arquivos PDF
- **RecursiveCharacterTextSplitter** - Divisão de textos em chunks

### Gerenciamento de Ambiente
- **uv** - Gerenciador de pacotes Python (ultrarrápido)
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Docker & Docker Compose** - Containerização

### CLI & Interface (Opcional)
- **Typer** - Framework para CLIs modernas
- **Rich** - Formatação bonita de output no terminal

## Variáveis de Ambiente

O arquivo `.env` deve conter:

```bash
# Google Gemini API
GOOGLE_API_KEY=sua-chave-google
GOOGLE_EMBEDDING_MODEL=models/embedding-001

# Configuração do Banco de Dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents

# Caminho do PDF para ingestão
PDF_PATH=./document.pdf
```
