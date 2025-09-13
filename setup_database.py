# --- PATCH COMPLETO PARA EVITAR CONFLITO DE DEFINIÇÃO DE MODELOS ---
import eca.database.schema
print("Aplicando patch correto na eca-lib para evitar redefinição de tabelas...")

original_get_schema_models = eca.database.schema.get_schema_models
# Cache baseado na dimensão
_cached_models_by_dim = {} 

def patched_get_schema_models(vector_dimension):
    if vector_dimension not in _cached_models_by_dim:
        print(f"ECA-Lib [Patch]: Criando modelos para dimensão {vector_dimension}")
        _cached_models_by_dim[vector_dimension] = original_get_schema_models(vector_dimension)
    else:
        print(f"ECA-Lib [Patch]: Usando cache para dimensão {vector_dimension}")
    return _cached_models_by_dim[vector_dimension]

eca.database.schema.get_schema_models = patched_get_schema_models
# --- FIM DO PATCH ---

from eca.adapters import PostgresPersonaProvider, PostgresMemoryProvider
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

# --- CONFIGURAÇÃO ---
DSN = "postgresql://eca_user:eca_password@localhost:55432/eca_db"
DIMENSION = 384
print("Carregando modelo de embedding...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_function(text: str) -> list[float]:
    return model.encode(text).tolist()

# --- GARANTIR EXTENSÃO PGVECTOR ---
print("Verificando se a extensão 'vector' está criada...")
engine = create_engine(DSN)
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()
print("Extensão 'vector' verificada.")

# --- INICIALIZAÇÃO DOS PROVIDERS ---
print("Instanciando PostgresPersonaProvider...")
persona_provider = PostgresPersonaProvider(
    dsn=DSN,
    embedding_function=embed_function,
    vector_dimension=DIMENSION,
    auto_setup=True
)

print("Instanciando PostgresMemoryProvider...")
memory_provider = PostgresMemoryProvider(
    dsn=DSN,
    embedding_function=embed_function,
    vector_dimension=DIMENSION,
    auto_setup=True
)

# --- DADOS A INSERIR ---

personas = [
    {
        "id": "fiscal",
        "name": "ÁBACO",
        "semantic_description": "Análise de documentos fiscais, notas fiscais, impostos.",
        "persona_config": {
            "persona": "Você é ÁBACO, um IA especialista em análise fiscal.",
            "objective": "Analisar documentos fiscais e garantir conformidade.",
            "golden_rules": ["A precisão é mais importante que a velocidade."]
        }
    },
    {
        "id": "product_catalog",
        "name": "CATÁLOGO",
        "semantic_description": "Gerenciamento de catálogo, cadastro de novos produtos, SKUs, códigos de item, notebook, celular.",
        "persona_config": {
            "persona": "Você é CATÁLOGO, um IA focado em manter a integridade do cadastro.",
            "objective": "Garantir a organização e padronização do catálogo.",
            "golden_rules": ["Verifique se o produto já existe antes de cadastrar."]
        }
    }
]

semantic_memories = [
    {
        "id": "mem-uuid-101",
        "domain_id": "fiscal",
        "type": "business_rule",
        "text_content": "Notas fiscais de serviço (NFS-e) devem ter o código de serviço validado contra a lista municipal."
    },
    {
        "id": "mem-uuid-202",
        "domain_id": "fiscal",
        "type": "business_rule",
        "text_content": "Para produtos com NCM iniciado em '8471', a empresa possui um regime especial de tributação de PIS/COFINS."
    },
    {
        "id": "mem-uuid-303",
        "domain_id": "fiscal",
        "type": "business_rule",
        "text_content": "O fornecedor 'Tecno Peças Ltda' frequentemente apresenta erros no cálculo do IPI na última semana do mês."
    },
    {
        "id": "mem-uuid-456",
        "domain_id": "fiscal",
        "type": "business_rule",
        "text_content": "Toda validação de ICMS-ST deve cruzar a informação com o Protocolo ICMS vigente."
    },
    {
        "id": "mem-uuid-789",
        "domain_id": "product_catalog",
        "type": "business_rule",
        "text_content": "O último código de notebook cadastrado foi 'NB-1098'. Novos códigos devem seguir a sequência."
    }
]

import eca.database.schema

# --- INSERÇÃO DOS DADOS NAS TABELAS ---

# Insert personas
with persona_provider.Session() as session:
    print("Inserindo personas com embeddings reais...")
    Base, PersonaModel, _, _ = eca.database.schema.get_schema_models(DIMENSION)
    for p in personas:
        embedding = embed_function(p["semantic_description"])
        persona = PersonaModel(
            id=p["id"],
            name=p["name"],
            semantic_description=p["semantic_description"],
            config=p["persona_config"],
            embedding=embedding
        )
        session.merge(persona)  # merge evita duplicação, atualiza se existir
    session.commit()
    print("Personas inseridas.")

# Insert semantic memories
with memory_provider.Session() as session:
    print("Inserindo memórias semânticas com embeddings reais...")
    Base, _, _, SemanticMemoryModel = eca.database.schema.get_schema_models(DIMENSION)
    for m in semantic_memories:
        embedding = embed_function(m["text_content"])
        memory = SemanticMemoryModel(
            id=m["id"],
            domain_id=m["domain_id"],
            type=m["type"],
            text_content=m["text_content"],
            embedding=embedding,
            attributes=None
        )
        session.merge(memory)
    session.commit()
    print("Memórias inseridas.")

print("\n✅ Setup do banco concluído com sucesso!")
