from eca.adapters import PostgresPersonaProvider, PostgresMemoryProvider
from sentence_transformers import SentenceTransformer

# --- CONFIGURAÇÃO ---
DSN = "postgresql://eca_user:eca_password@localhost:5432/eca_db"
print("Carregando modelo de embedding...")
model = SentenceTransformer('all-MiniLM-L6-v2')
# A dimensão do vetor para este modelo é 384
DIMENSION = 384

def embed_function(text: str) -> list[float]:
    """Função que gera o embedding para um texto."""
    return model.encode(text).tolist()

# --- INICIALIZAÇÃO DOS PROVIDERS ---
# O `auto_setup=True` cria as tabelas no banco se elas não existirem
print("Configurando o Provedor de Personas...")
persona_provider = PostgresPersonaProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION, auto_setup=True)
print("Configurando o Provedor de Memória...")
memory_provider = PostgresMemoryProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION, auto_setup=True)

# --- INSERINDO OS DADOS NO POSTGRES ---
with persona_provider.Session() as session:
    print("Inserindo personas com embeddings reais...")
    # ... (O código de inserção das personas é similar ao do artigo anterior,
    # mas agora o `embedding` é gerado pela `embed_function` real) ...
    print("Personas inseridas.")

with memory_provider.Session() as session:
    print("Inserindo memórias semânticas com embeddings reais...")
    # ... (O código de inserção das memórias é similar,
    # mas o `embedding` também é gerado pela `embed_function`) ...
    print("Memórias inseridas.")

print("\n✅ Banco de dados de produção configurado com sucesso!")