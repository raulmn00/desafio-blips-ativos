# API de Gerenciamento de Leads

Uma API REST completa para gerenciar leads, construída com Python, FastAPI e MongoDB. A API enriquece automaticamente os dados dos leads buscando datas de nascimento de uma API externa.

## Funcionalidades

- Criar, ler e listar leads
- Enriquecimento automático de data de nascimento via API externa
- Suporte a async/await para alta performance
- MongoDB para persistência de dados
- Docker e Docker Compose para facilitar o deploy
- Arquitetura limpa com separação de responsabilidades
- Tratamento abrangente de erros e logging
- Documentação da API com Swagger UI
- Validação de entrada com Pydantic

## Stack Tecnológica

- **Python 3.11+**: Python moderno com suporte a async
- **FastAPI**: Framework web de alta performance
- **MongoDB**: Banco de dados NoSQL para flexibilidade
- **Motor**: Driver MongoDB assíncrono
- **Pydantic**: Validação de dados e gerenciamento de configurações
- **httpx**: Cliente HTTP assíncrono para chamadas de API externa
- **Docker & Docker Compose**: Containerização e orquestração

## Estrutura do Projeto

```
desafio-blips-ativos/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI e inicialização
│   ├── config.py               # Configuração da aplicação
│   ├── models/
│   │   ├── __init__.py
│   │   └── lead.py             # Modelo de dados de Lead
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── lead.py             # Schemas Pydantic para validação
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── lead_repository.py  # Operações de banco de dados
│   ├── services/
│   │   ├── __init__.py
│   │   ├── lead_service.py     # Lógica de negócio
│   │   └── external_api_service.py  # Integração com API externa
│   └── routes/
│       ├── __init__.py
│       └── lead_routes.py      # Endpoints da API
├── docker-compose.yml           # Configuração dos serviços Docker
├── Dockerfile                   # Definição do container da API
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

## Início Rápido

### Pré-requisitos

- Docker e Docker Compose instalados
- Git (para clonar o repositório)

### Executando com Docker Compose

1. Clone o repositório:
```bash
git clone <url-do-repositório>
cd desafio-blips-ativos
```

2. Inicie os serviços:
```bash
docker-compose up --build
```

3. A API estará disponível em:
   - API: http://localhost:8000
   - Documentação Swagger: http://localhost:8000/docs
   - Documentação ReDoc: http://localhost:8000/redoc

### Executando Localmente (sem Docker)

1. Instale Python 3.11+ e MongoDB

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
export MONGODB_URL="mongodb://admin:admin123@localhost:27017"
export MONGODB_DB_NAME="leads_db"
export EXTERNAL_API_URL="https://dummyjson.com"
```

4. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

## Endpoints da API

### 1. Criar um Lead

**POST** `/leads`

Cria um novo lead com enriquecimento automático de data de nascimento via API externa.

**Corpo da Requisição:**
```json
{
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "phone": "+5511999999999"
}
```

**Resposta (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "phone": "+5511999999999",
  "birth_date": "1998-02-05"
}
```

**Respostas de Erro:**
- `400 Bad Request`: Entrada inválida ou email duplicado
- `500 Internal Server Error`: Erro no servidor

### 2. Obter Todos os Leads

**GET** `/leads`

Recupera todos os leads do banco de dados.

**Resposta (200 OK):**
```json
{
  "leads": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "João Silva",
      "email": "joao.silva@example.com",
      "phone": "+5511999999999",
      "birth_date": "1998-02-05"
    }
  ],
  "total": 1
}
```

### 3. Obter Lead por ID

**GET** `/leads/{id}`

Recupera um lead específico pelo seu ID.

**Resposta (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "phone": "+5511999999999",
  "birth_date": "1998-02-05"
}
```

**Respostas de Erro:**
- `404 Not Found`: Lead não encontrado
- `500 Internal Server Error`: Erro no servidor

### Endpoints de Health Check

**GET** `/` - Endpoint raiz com informações da aplicação

**GET** `/health` - Verificação de saúde com status do banco de dados

## Integração com API Externa

A aplicação se integra com a API DummyJSON (https://dummyjson.com/users/1) para buscar datas de nascimento para novos leads.

### Estratégia de Tratamento de Erros

Se a API externa falhar (timeout, erro de rede ou resposta inválida), a aplicação irá:
1. Registrar o erro para monitoramento
2. Definir `birth_date` como `null` no registro do lead
3. Continuar com a criação do lead

Esta decisão de design garante que falhas da API externa não bloqueiem a criação de leads, priorizando disponibilidade ao invés de dados completos. O campo `birth_date` é opcional e pode ser atualizado posteriormente se necessário.

### Configuração de Timeout

O timeout da API externa é configurável através da variável de ambiente `EXTERNAL_API_TIMEOUT` (padrão: 10 segundos).

## Configuração

A configuração é gerenciada através de variáveis de ambiente:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `MONGODB_URL` | String de conexão do MongoDB | `mongodb://admin:admin123@localhost:27017` |
| `MONGODB_DB_NAME` | Nome do banco de dados | `leads_db` |
| `EXTERNAL_API_URL` | URL base da API externa | `https://dummyjson.com` |
| `EXTERNAL_API_TIMEOUT` | Timeout de requisição da API (segundos) | `10` |

## Arquitetura

A aplicação segue uma arquitetura limpa com clara separação de responsabilidades:

### Camadas

1. **Camada de Rotas** (`routes/`): Gerencia requisições/respostas HTTP
2. **Camada de Serviços** (`services/`): Contém lógica de negócio
3. **Camada de Repositório** (`repositories/`): Operações de banco de dados
4. **Camada de Modelos** (`models/`): Modelos de domínio
5. **Camada de Schemas** (`schemas/`): Validação de requisição/resposta

### Padrões de Design

- **Padrão Repository**: Abstrai o acesso a dados
- **Padrão Service**: Encapsula lógica de negócio
- **Injeção de Dependência**: Instâncias singleton para serviços
- **Async/Await**: Operações de I/O não bloqueantes

## Desenvolvimento

### Qualidade de Código

A base de código segue:
- Guia de estilo PEP 8
- Type hints para melhor suporte de IDE
- Docstrings abrangentes
- Nomes descritivos de variáveis e funções

### Logging

A aplicação usa o módulo de logging integrado do Python com os seguintes níveis:
- **INFO**: Operações normais (conexões, operações bem-sucedidas)
- **WARNING**: Problemas recuperáveis (falhas de API externa, erros de validação)
- **ERROR**: Problemas sérios (erros de banco de dados, exceções inesperadas)

### Tratamento de Erros

- Validação de entrada com Pydantic
- Tratamento de exceções customizado nos serviços
- Exceções HTTP nas rotas
- Degradação graceful para falhas de API externa

## Testes

Para testar manualmente a API:

1. Acesse o Swagger UI em http://localhost:8000/docs
2. Use a documentação interativa para testar os endpoints
3. Ou use curl/httpx:

```bash
# Criar um lead
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Santos",
    "email": "maria.santos@example.com",
    "phone": "+5511988888888"
  }'

# Obter todos os leads
curl http://localhost:8000/leads

# Obter lead por ID
curl http://localhost:8000/leads/{lead_id}
```

## Considerações para Produção

Para deploy em produção, considere:

1. **Segurança**:
   - Use credenciais fortes para MongoDB
   - Habilite autenticação e autorização
   - Use HTTPS/TLS
   - Implemente rate limiting
   - Adicione configuração CORS se necessário

2. **Performance**:
   - Adicione índices no banco de dados (campo email)
   - Configure connection pooling
   - Habilite cache para dados frequentemente acessados
   - Use um servidor ASGI de produção (Gunicorn + Uvicorn)

3. **Monitoramento**:
   - Integre com serviços de logging (ELK, Datadog)
   - Configure monitoramento de health check
   - Rastreie métricas e performance da API
   - Configure alertas para erros

4. **Escalabilidade**:
   - Use replica sets do MongoDB para alta disponibilidade
   - Faça deploy de múltiplas instâncias da API atrás de um load balancer
   - Considere implementar uma fila de mensagens para operações assíncronas

## Licença

MIT License

## Autor

Desenvolvido como parte do desafio Blips Ativos.
