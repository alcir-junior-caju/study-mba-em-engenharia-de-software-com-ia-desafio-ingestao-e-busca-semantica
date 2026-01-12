#!/usr/bin/env bash

# Script para verificar e configurar o ambiente

set -e

echo "🔍 Verificando dependências..."

# Verificar uv
if ! command -v uv &> /dev/null; then
    echo "❌ uv não encontrado"
    echo "📦 Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    echo "✅ uv instalado com sucesso"
else
    echo "✅ uv encontrado: $(uv --version)"
fi

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado"
    echo "Por favor, instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
else
    echo "✅ Docker encontrado: $(docker --version)"
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não encontrado"
    echo "Por favor, instale o Docker Compose"
    exit 1
else
    echo "✅ Docker Compose encontrado"
fi

# Verificar arquivo .env
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado"
    if [ -f .env.example ]; then
        echo "📋 Copiando .env.example para .env"
        cp .env.example .env
        echo "⚠️  Por favor, edite o arquivo .env com suas chaves de API"
    fi
else
    echo "✅ Arquivo .env encontrado"
fi

# Criar ambiente virtual se não existir
if [ ! -d .venv ]; then
    echo "📦 Criando ambiente virtual..."
    uv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Sincronizar dependências
echo "📦 Sincronizando dependências..."
uv sync
echo "✅ Dependências sincronizadas"

echo ""
echo "🎉 Ambiente configurado com sucesso!"
echo ""
echo "Próximos passos:"
echo "1. Edite o arquivo .env com suas chaves de API"
echo "2. Inicie o banco de dados: docker-compose up -d"
echo "3. Execute a CLI:"
echo "   - Ingestão: uv run python src/cli.py ingest"
echo "   - Busca: uv run python src/cli.py search \"texto\""
echo "   - Chat: uv run python src/cli.py chat"
