# OpenMetadata Sandbox Environment

Ambiente de sandbox local para o OpenMetadata, utilizando componentes open-source para simular um ecossistema de dados moderno. Substitui LocalStack (Athena/Glue/S3) por alternativas equivalentes executadas via Docker.

## Arquitetura

| Serviço | Imagem | Função |
|---|---|---|
| **MinIO** | `minio/minio` | Storage compatível com S3 |
| **Hive Metastore** | `starburstdata/hive` | Catálogo de metadados das tabelas |
| **Trino** | `trinodb/trino` | Engine SQL distribuída (equivalente ao Athena) |
| **OpenMetadata** | `openmetadata/server` | Governança, catálogo e linhagem de dados |
| **Elasticsearch** | `elasticsearch` | Backend de busca do OpenMetadata |
| **Spark** | `bitnami/spark` | Geração de dados sintéticos (opcional) |

---

## Pré-requisitos

- Docker Engine 24+ e Docker Compose v2 (`docker compose`, não `docker-compose`)
- **10 GB de RAM** no host (ver seção de memória abaixo)
- Espaço em disco para imagens: ~8 GB

---

## Setup por Plataforma

### Windows (WSL2)

> Todos os comandos devem ser executados no terminal **WSL2** (Ubuntu/Debian) ou **Git Bash**. CMD e PowerShell não são suportados.

1. Instale o **Docker Desktop** com backend **WSL2** habilitado
2. No Docker Desktop: **Settings > Resources > Advanced**
   - Memory: `8 GB` (mínimo) — `10 GB` recomendado
   - CPUs: `4+`
3. Clone o repositório **dentro** do filesystem WSL2, por exemplo `~/projects/`
   - Evite clonar em `/mnt/c/...` — volume mounts ficam lentos e podem causar erros de permissão

```bash
# No terminal WSL2:
cd ~/projects
git clone <url-do-repo> openmetadata
cd openmetadata
```

### Linux (nativo)

```bash
# Instalar Docker Engine + plugin Compose
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Adicionar seu usuário ao grupo docker (evita sudo)
sudo usermod -aG docker $USER
newgrp docker
```

Verifique se cgroups v2 está ativo (necessário para `mem_limit`):

```bash
mount | grep cgroup2
# Se não aparecer nada, adicione ao /etc/default/grub:
# GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=1"
```

---

## Configuração

```bash
# Copie o .env de exemplo para o diretório do Docker
cp .env.example docker/.env
```

Edite `docker/.env` se quiser ajustar credenciais ou limites de memória (ver seção abaixo).

---

## Como Iniciar

> Todos os comandos `docker compose` devem ser executados a partir do diretório `docker/`.

```bash
cd docker

# Subir o stack principal (sem Spark)
docker compose up -d

# Acompanhar a inicialização (OpenMetadata leva ~3 min no primeiro boot)
docker compose logs -f openmetadata-server

# Verificar status de todos os serviços
docker compose ps
```

Aguarde todos os containers atingirem o status `healthy` antes de acessar as interfaces.

### Acessos

| Serviço | URL | Credenciais |
|---|---|---|
| **OpenMetadata** | http://localhost:8585 | `admin` / `admin` |
| **MinIO Console** | http://localhost:9001 | `minioadmin` / `minioadmin` |
| **Trino UI** | http://localhost:8080 | — |

---

## Gerando Dados Sintéticos (Spark)

O Spark é um serviço opcional com profile próprio. Ele gera 1.000 linhas de transações financeiras fictícias no MinIO e registra a tabela no Hive Metastore.

```bash
# Executar a partir do diretório docker/
docker compose --profile spark up spark-app
```

O job:
1. Gera dados sintéticos em formato Parquet
2. Salva em `s3a://datalake/sandbox/financial_transactions`
3. Registra a tabela `financial_transactions` no schema `sandbox` do Hive/Trino

Controle a quantidade de linhas via `docker/.env`:

```dotenv
NUM_ROWS=5000
```

---

## Configurando o OpenMetadata

1. Acesse http://localhost:8585 (login: `admin` / `admin`)
2. Vá em **Settings > Database Services > Add New Service**
3. Selecione **Trino** e configure:
   - **Host and Port**: `trino:8080`
   - **Username**: `admin`
   - **Catalog**: `hive`
4. Salve e vá em **Ingestion > Add Metadata Ingestion**
5. Execute o pipeline — a tabela `sandbox.financial_transactions` aparecerá no catálogo

---

## Memória — Requisitos e Configuração

### Alocação por serviço (padrão)

| Serviço | `mem_limit` | Heap JVM |
|---|---|---|
| minio | 512m | — (Go) |
| hive-metastore-db | 256m | — |
| hive-metastore | 1g | 512m |
| trino | 2g | 1g |
| openmetadata-db | 256m | — |
| elasticsearch | 1g | 512m |
| openmetadata-server | 1500m | 1g |
| **Total sem Spark** | **~6.5 GB** | |
| spark-app (opcional) | +2g | — |

### Ajustando no `.env`

Edite `docker/.env` para aumentar ou reduzir limites:

```dotenv
# Exemplo: aumentar Trino para queries mais pesadas
MEM_TRINO=3g
TRINO_HEAP_SIZE=2g

# Regra: ES_HEAP_SIZE deve ser menor que MEM_ELASTICSEARCH
# (Elasticsearch precisa de memória extra além da JVM para o Lucene)
MEM_ELASTICSEARCH=1g
ES_HEAP_SIZE=512m
```

---

## Verificação

```bash
# Elasticsearch deve retornar green ou yellow
curl http://localhost:9200/_cluster/health

# Consultar dados no Trino
docker exec -it trino trino --execute \
  "SELECT * FROM hive.sandbox.financial_transactions LIMIT 10;"

# Verificar se mem_limit está aplicado
docker inspect openmetadata-server | grep -i memory
```

---

## Troubleshooting

**Container reinicia ou sai imediatamente — OOMKilled**

```bash
docker inspect <nome-do-container> | grep OOMKilled
# Se "OOMKilled": true → aumente o MEM_* correspondente no docker/.env
```

**`hive-metastore` nunca fica `healthy`**

O Hive Metastore é o serviço mais lento para iniciar (JVM + conexão com PostgreSQL + MinIO). Aguarde até 90 segundos. Se ainda falhar, verifique os logs:

```bash
docker compose logs hive-metastore
```

**Trino responde mas retorna "No nodes available"**

Normal no cold start. Aguarde 30–60 segundos após o container ficar `healthy`.

**OpenMetadata não sobe / fica em loop**

Verifique se o Elasticsearch está `healthy` primeiro:

```bash
curl http://localhost:9200/_cluster/health
# status deve ser "green" ou "yellow", nunca "red"
```

**Erros de permissão em volumes (Linux)**

```bash
sudo chown -R $USER:$USER docker/
```

**Executar `docker compose` do diretório errado**

O `spark-app` monta `../src/spark` relativo ao `docker-compose.yml`. Sempre execute:

```bash
cd docker && docker compose ...
```

---

## Limpando o Ambiente

```bash
# Para e remove containers, networks e volumes (reseta tudo)
cd docker && docker compose down -v
```
