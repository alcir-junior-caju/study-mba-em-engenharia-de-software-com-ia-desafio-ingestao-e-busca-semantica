import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Configurações do ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "documents")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = "gemini-2.0-flash-lite"

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    """
    Cria uma chain que realiza busca vetorial e gera resposta usando LLM.

    Args:
        question: Pergunta do usuário (opcional, usado para teste)

    Returns:
        Uma função que recebe uma pergunta e retorna a resposta
    """
    if not GOOGLE_API_KEY:
        print("❌ ERRO: GOOGLE_API_KEY não encontrada no arquivo .env")
        return None

    try:
        # Configurar embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
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
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0,
        )

        # Criar prompt template
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["contexto", "pergunta"]
        )

        # Criar chain usando a nova sintaxe (RunnableSequence)
        chain = prompt | llm | StrOutputParser()

        def query_chain(user_question: str) -> str:
            """
            Executa a busca e retorna a resposta.

            Args:
                user_question: Pergunta do usuário

            Returns:
                Resposta baseada no contexto encontrado
            """
            # Buscar os 10 documentos mais relevantes
            results = vectorstore.similarity_search_with_score(user_question, k=10)

            if not results:
                return "Não tenho informações necessárias para responder sua pergunta."

            # Concatenar o contexto dos resultados
            contexto = "\n\n".join([doc.page_content for doc, score in results])

            # Gerar resposta usando a nova sintaxe
            resposta = chain.invoke({
                "contexto": contexto,
                "pergunta": user_question
            })

            return resposta

        # Se uma pergunta foi fornecida (para testes), executar
        if question:
            return query_chain(question)

        # Retornar a função de query
        return query_chain

    except Exception as e:
        print(f"❌ ERRO ao configurar busca: {e}")
        import traceback
        traceback.print_exc()
        return None
