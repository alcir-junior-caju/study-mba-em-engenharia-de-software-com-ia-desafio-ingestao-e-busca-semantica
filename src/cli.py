"""CLI principal usando Typer e Rich."""

import os
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from cli_utils import (
    console,
    print_error,
    print_header,
    print_info,
    print_success,
    progress_spinner,
    setup_logging,
)

load_dotenv()

app = typer.Typer(
    name="rag-cli",
    help="CLI para ingestão, busca e chat com RAG",
    add_completion=False,
)

# Setup logging
logger = setup_logging()

# Configurações
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
PDF_PATH = os.getenv("PDF_PATH", "./document.pdf")


@app.command()
def ingest(
    pdf_path: Annotated[
        str | None,
        typer.Option(
            "--pdf-path",
            "-p",
            help="Caminho para o arquivo PDF (opcional, usa PDF_PATH do .env se não fornecido)",
        ),
    ] = None,
):
    """Ingere um PDF no banco de dados vetorial."""
    # Usar PDF_PATH do .env se não fornecido
    if pdf_path is None:
        pdf_path = PDF_PATH

    pdf_file = Path(pdf_path)

    # Validar se o arquivo existe
    if not pdf_file.exists():
        print_error(f"Arquivo PDF não encontrado: {pdf_path}")
        raise typer.Exit(code=1)

    if not pdf_file.is_file():
        print_error(f"O caminho não é um arquivo: {pdf_path}")
        raise typer.Exit(code=1)

    print_header("Ingestão de PDF", f"Processando: {pdf_file.name}")

    if not GOOGLE_API_KEY:
        print_error("GOOGLE_API_KEY não encontrada no arquivo .env")
        raise typer.Exit(code=1)

    try:
        # 1. Carregar PDF
        print_info("Carregando PDF...")
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()
        print_success(f"PDF carregado: {len(documents)} página(s)")

        # 2. Dividir em chunks
        print_info("Dividindo documento em chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(documents)
        print_success(f"Documento dividido em {len(chunks)} chunks")

        # 3. Configurar embeddings
        print_info("Configurando embeddings do Gemini...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,  # type: ignore[arg-type]  # type: ignore[arg-type]
        )
        print_success(f"Embeddings configurados: {EMBEDDING_MODEL}")

        # 4. Armazenar no banco
        print_info("Armazenando no banco de dados...")
        with progress_spinner() as progress:
            progress.add_task("[cyan]Salvando chunks...", total=None)
            PGVector.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=COLLECTION_NAME,
                connection=DATABASE_URL,
                use_jsonb=True,
            )

        print_success(f"Ingestão concluída! {len(chunks)} chunks armazenados")
        print_info(f"Coleção: {COLLECTION_NAME}")

    except Exception as e:
        print_error(f"Erro ao ingerir PDF: {e}")
        logger.exception("Erro detalhado:")
        raise typer.Exit(code=1) from e


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Texto da busca")],
    top_k: Annotated[
        int,
        typer.Option("--top-k", "-k", help="Número de resultados"),
    ] = 10,
):
    """Busca documentos similares usando busca vetorial."""
    print_header("Busca Vetorial", f"Query: '{query}'")

    if not GOOGLE_API_KEY:
        print_error("GOOGLE_API_KEY não encontrada no arquivo .env")
        raise typer.Exit(code=1)

    try:
        # Configurar embeddings
        print_info("Configurando embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,  # type: ignore[arg-type]
        )

        # Conectar ao vector store
        print_info("Conectando ao banco de dados...")
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )

        # Buscar documentos similares
        print_info(f"Buscando top {top_k} documentos similares...")
        with progress_spinner() as progress:
            progress.add_task("[cyan]Buscando...", total=None)
            results = vectorstore.similarity_search_with_score(query, k=top_k)

        if not results:
            print_info("Nenhum documento encontrado")
            return

        # Exibir resultados
        from rich.table import Table

        table = Table(title=f"Top {len(results)} Resultados", show_lines=True)
        table.add_column("Rank", style="cyan", width=6, justify="center")
        table.add_column("Score", style="magenta", width=10, justify="right")
        table.add_column("Conteúdo", style="white")

        for idx, (doc, _score) in enumerate(results, 1):
            # Truncar conteúdo se for muito longo
            content = doc.page_content
            if len(content) > 200:
                content = content[:200] + "..."

            table.add_row(str(idx), f"{_score:.4f}", content)

        console.print()
        console.print(table)
        print_success(f"Encontrados {len(results)} documentos")

    except Exception as e:
        print_error(f"Erro na busca: {e}")
        logger.exception("Erro detalhado:")
        raise typer.Exit(code=1) from e


@app.command()
def chat():
    """Inicia chat interativo com RAG."""

    print_header("Chat RAG Interativo", "Digite 'sair' para encerrar")

    if not GOOGLE_API_KEY:
        print_error("GOOGLE_API_KEY não encontrada no arquivo .env")
        raise typer.Exit(code=1)

    try:
        # Configurar embeddings
        print_info("Inicializando sistema...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,  # type: ignore[arg-type]
        )

        # Conectar ao vector store
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )

        # Configurar LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            google_api_key=GOOGLE_API_KEY,  # type: ignore[arg-type]
            temperature=0,
        )

        # Criar prompt template
        PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

        prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["contexto", "pergunta"])

        # Criar chain usando a nova sintaxe (RunnableSequence)
        chain = prompt | llm | StrOutputParser()

        print_success("Sistema pronto!")
        console.print()

        # Loop do chat
        while True:
            try:
                # Prompt do usuário
                user_input = console.input("[bold cyan]💬 Você:[/bold cyan] ").strip()

                if user_input.lower() in ["sair", "exit", "quit", "q"]:
                    print_info("Encerrando chat...")
                    break

                if not user_input:
                    continue

                # Buscar contexto e gerar resposta
                with progress_spinner() as progress:
                    progress.add_task("[cyan]Buscando contexto e gerando resposta...", total=None)

                    # Buscar documentos relevantes
                    results = vectorstore.similarity_search_with_score(user_input, k=10)

                    if not results:
                        resposta = "Não tenho informações necessárias para responder sua pergunta."
                    else:
                        # Concatenar contexto
                        contexto = "\n\n".join([doc.page_content for doc, _score in results])

                        # Gerar resposta usando a nova sintaxe
                        resposta = chain.invoke({"contexto": contexto, "pergunta": user_input})
                from cli_utils import print_panel

                print_panel(resposta, title="🤖 Assistente", style="green")
                console.print()

            except KeyboardInterrupt:
                console.print()
                print_info("Chat interrompido")
                break

    except Exception as e:
        print_error(f"Erro no chat: {e}")
        logger.exception("Erro detalhado:")
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
