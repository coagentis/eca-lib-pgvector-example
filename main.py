from datetime import datetime
from eca import ECAOrchestrator
# Importando os adaptadores de produção
from eca.adapters import PostgresPersonaProvider, PostgresMemoryProvider
from eca.adapters import RedisSessionProvider
from eca.memory import EpisodicMemory
from sentence_transformers import SentenceTransformer

# --- 1. CONFIGURAÇÃO DO STACK DE PRODUÇÃO ---
DSN = "postgresql://eca_user:eca_password@localhost:55432/eca_db"
REDIS_HOST = "localhost"
model = SentenceTransformer('all-MiniLM-L6-v2')
DIMENSION = 384

def embed_function(text: str) -> list[float]:
    return model.encode(text).tolist()

# Trocamos os adaptadores JSON pelos de produção
persona_provider = PostgresPersonaProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION)
memory_provider = PostgresMemoryProvider(dsn=DSN, embedding_function=embed_function, vector_dimension=DIMENSION)
session_provider = RedisSessionProvider(host=REDIS_HOST,  port=6380)

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
user_id = "ana_paula"

def run_complete_interaction(user_input: str, turn: int):
    print("----------------------------------------------------")
    print(f"🔷 TURNO {turn} 🔷")
    print(f"🗣️  USUÁRIO (Ana Paula): '{user_input}'")
    
    context_object = orchestrator.generate_context_object(user_id, user_input)
    dynamic_context_str = orchestrator._flatten_context_to_string(context_object, user_input)
    final_prompt = orchestrator.meta_prompt_template.replace("{{DYNAMIC_CONTEXT}}", dynamic_context_str)

    print("\n✨ PROMPT 'ACHATADO' GERADO PELA ECA: ✨")
    print(final_prompt)
    
    fake_llm_response = f"Resposta simulada para '{user_input[:25]}...'"
    print(f"\n🤖 RESPOSTA (Simulada do LLM): '{fake_llm_response}'")

    interaction_to_log = EpisodicMemory(
        user_id=user_id,
        domain_id=context_object.current_focus,
        user_input=user_input,
        assistant_output=fake_llm_response,
        timestamp=datetime.now().isoformat()
    )
    memory_provider.log_interaction(interaction_to_log)
    session_provider.save_workspace(context_object)
    print(f"\n[INFO: Turno {turn} salvo na memória e sessão.]")
    print("----------------------------------------------------\n")

# Limpa os logs para uma execução limpa
import os
if os.path.exists("interaction_log.json"): os.remove("interaction_log.json")
if os.path.exists("user_sessions.json"): os.remove("user_sessions.json")

# --- TURNO 1: Foco em Catálogo de Produtos ---
run_complete_interaction(
    user_input="Preciso de ajuda para cadastrar um novo notebook no sistema.",
    turn=1
)

# --- TURNO 2: Troca de Contexto para Fiscal (com consulta a dados) ---
run_complete_interaction(
    user_input="Ok, mudei de ideia. Por favor, analise a Nota Fiscal de Entrada nº 78910.",
    turn=2
)

# --- TURNO 3: Retorno ao Contexto de Catálogo ---
run_complete_interaction(
    user_input="Certo, voltando ao cadastro de produto. Sobre aquele notebook que mencionei, qual é o próximo código que devo usar?",
    turn=3
)