# Exemplo de `eca-lib` em Produção com PostgreSQL e Redis

Este repositório demonstra uma implementação de nível de produção da **Engenharia de Contexto Aumentada (ECA)**, migrando do conceito de protótipo com arquivos JSON para um stack de dados robusto e escalável.

O objetivo é mostrar como a `eca-lib`, graças à sua arquitetura de adaptadores, pode ser facilmente integrada com tecnologias de produção como **PostgreSQL** (com a extensão `pgvector`) para memória de longo prazo e **Redis** para o gerenciamento de sessões em tempo real.

A infraestrutura de banco de dados é totalmente gerenciada via **Docker Compose** para facilitar a configuração e execução.

## 🚀 O que este Exemplo Demonstra?

  * **✅ Migração Transparente:** Como trocar os adaptadores de dados (de JSON para bancos de dados) sem alterar a lógica de orquestração principal da aplicação.
  * **🧠 Memória Persistente e Vetorial:** O uso do PostgreSQL + `pgvector` como uma base de conhecimento unificada, combinando a integridade de dados do SQL com buscas semânticas de alta performance.
  * **⚡ Gerenciamento de Sessão Escalável:** A utilização do Redis para armazenar o estado das conversas (`CognitiveWorkspace`), garantindo altíssima velocidade para milhares de usuários simultâneos.
  * **🔍 Busca Semântica Real:** A aplicação da biblioteca `sentence-transformers` para gerar embeddings vetoriais reais e realizar uma detecção de domínio muito mais precisa e inteligente.
  * **🔄 Orquestração Completa:** O ciclo completo de uma conversa com troca de contexto e injeção de dados de tarefa, agora rodando em um ambiente de produção.

## ⚙️ Arquitetura do Exemplo

O diagrama abaixo ilustra a interação entre a aplicação Python e a infraestrutura de dados gerenciada pelo Docker.

```mermaid
graph TD
    subgraph "Aplicação Python (Local)"
        A[main.py <br><i>ECAOrchestrator</i>]
        B[setup_database.py]
    end

    subgraph "Infraestrutura (Docker Compose)"
        C[<b>PostgreSQL + pgvector</b><br><i>(Personas, Memória Semântica)</i>]
        D[<b>Redis</b><br><i>(Estado da Sessão, Workspace)</i>]
    end

    A -- Conecta via Adaptador --> C
    A -- Conecta via Adaptador --> D
    B -- Popula o Banco --> C

    style A fill:#FFC300,stroke:#333,stroke-width:2px
    style B fill:#lightgrey,stroke:#333,stroke-width:2px
    style C fill:#3574A3,stroke:#FFF,stroke-width:2px,color:#fff
    style D fill:#D82C20,stroke:#FFF,stroke-width:2px,color:#fff
```

## 🛠️ Como Executar

Siga os passos abaixo para rodar o ambiente completo.

### 1\. Pré-requisitos

  * **Docker** e **Docker Compose:** Essenciais para rodar a infraestrutura. [Instale aqui](https://docs.docker.com/get-docker/).
  * **Python 3.10** ou superior.

### 2\. Clone o Repositório

```bash
git clone https://github.com/coagentis/eca-lib-pgvector-example.git
cd eca-lib-pgvector-example.git
```

### 3\. Inicie a Infraestrutura

Este comando irá iniciar os contêineres do PostgreSQL e do Redis em segundo plano.

```bash
docker-compose up -d
```

Aguarde alguns segundos para que os bancos de dados estejam prontos para aceitar conexões.

### 4\. Crie um Ambiente Virtual e Instale as Dependências

```bash
# Crie o ambiente
python -m venv venv

# Ative o ambiente
# No Linux ou macOS:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instale os pacotes necessários
pip install "eca-lib[postgres,redis]" sentence-transformers
```

### 5\. Popule o Banco de Dados

Execute este script para criar as tabelas e inserir os dados das personas e memórias, agora com embeddings vetoriais reais.
*(Nota: na primeira execução, pode levar um momento para baixar o modelo de embedding)*

```bash
python setup_database.py
```

### 6\. Execute a Simulação

Finalmente, execute o script principal para ver a simulação da conversa.

```bash
python main.py
```

## 📄 Saída Esperada

A saída no seu terminal será funcionalmente idêntica à do exemplo simples, mostrando os 3 turnos da conversa. No entanto, a mágica agora acontece nos bastidores.

  * **No Turno 1 e 3:** A detecção de domínio para `CATÁLOGO` agora é feita via busca semântica vetorial, tornando-a muito mais robusta.
  * **No Turno 2:** A identidade `ÁBACO` é carregada do PostgreSQL, o conteúdo da nota fiscal é injetado, e o estado da sessão é salvo no Redis.
  * **A Troca de Contexto:** Ao final do Turno 3, você terá a prova de que o estado da sessão foi perfeitamente preservado e recuperado do Redis para retomar uma tarefa pausada.

Para verificar, você pode usar um cliente de banco de dados para se conectar ao Postgres na porta `5432` ou usar o `redis-cli` para inspecionar as chaves de sessão no Redis.

## 📚 Para Saber Mais

  * **Explore a Biblioteca:** Visite o repositório oficial da **[eca-lib no GitHub](https://www.google.com/search?q=LINK_PARA_SEU_REPOSITORIO_DA_LIB)**. Se gostar, sua estrelinha (⭐) é o melhor agradecimento\!
  * **Aprofunde-se na Arquitetura:** Para um entendimento completo dos conceitos, leia nosso **[Whitepaper de Arquitetura](https://www.google.com/search?q=LINK_PARA_SEU_WHITEPAPER)**.
  * **Conecte-se:** Siga o criador do projeto no **[LinkedIn](https://www.google.com/search?q=SEU_LINK_DO_LINKEDIN)**.