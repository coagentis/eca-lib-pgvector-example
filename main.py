from datetime import datetime
from eca import ECAOrchestrator
# Importando os adaptadores de produção
from eca.adapters import PostgresPersonaProvider, PostgresMemoryProvider
from eca.adapters import RedisSessionProvider
from eca.memory import EpisodicMemory
from sentence_transformers import SentenceTransformer

# --- 1. CONFIGURAÇÃO DO STACK DE PRODUÇÃO ---
DSN = "postgresql://eca_user:eca_password@localhost:5432/eca_db"
REDIS_HOST = "localhost"
model = SentenceTransformer('all-MiniLM-L6-v2')
DIMENSION = 384

def embed_function(text: str) -> list[float]:
    return model.encode(text).tolist()

# Trocamos os adaptadores JSON pelos de produção
persona_provider = PostgresPersonaProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION)
memory_provider = PostgresMemoryProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION)
session_provider = RedisSessionProvider(host=REDIS_HOST)

# --- 2. Instanciação do Orquestrador ---
# A lógica do orquestrador não muda NADA.
orchestrator = ECAOrchestrator(
    persona_provider=persona_provider,
    memory_provider=memory_provider,
    session_provider=session_provider,
    knowledge_base_path='.'
)
print("✅ Orquestrador ECA pronto para uso com Postgres e Redis!")

# --- 3. Simulação da Conversa (CÓDIGO IDÊNTICO AO ANTERIOR) ---
# ... (a função `run_complete_interaction` e as chamadas dos 3 turnos
# são exatamente as mesmas do artigo anterior) ...