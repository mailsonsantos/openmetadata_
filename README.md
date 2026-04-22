# OpenMetadata Sandbox Environment

Este repositório contém um ambiente de sandbox para o OpenMetadata, utilizando componentes open-source para simular um ecossistema de dados moderno. Ele substitui a necessidade do LocalStack (Athena/Glue/S3) por alternativas equivalentes que podem ser executadas localmente via Docker.

## 🚀 Arquitetura do Ambiente

O ambiente é composto pelos seguintes serviços:

- **MinIO**: Storage compatível com S3 para armazenar arquivos Parquet.
- **Hive Metastore**: Gerencia o catálogo de metadados das tabelas no MinIO.
- **Trino**: Engine de consulta SQL distribuída (equivalente ao Athena).
- **OpenMetadata**: Plataforma central para governança, catálogo e linhagem de dados.
- **Spark**: Script para geração de dados sintéticos e registro de tabelas.

---

## 🛠 Pré-requisitos

Antes de começar, certifique-se de ter:

- **Docker** e **Docker Compose** instalados.
- Pelo menos **8GB-12GB de RAM** livre (os serviços são pesados).
- Espaço em disco suficiente para as imagens Docker.

---

## 🏁 Como Iniciar

### 1. Subir a Infraestrutura

Para subir todos os serviços, execute o comando abaixo na raiz do projeto:

```bash
docker-compose up -d
```

> **Nota:** A primeira execução pode demorar alguns minutos enquanto as imagens são baixadas e os serviços inicializados. Aguarde até que todos os containers estejam com o status `healthy`.

### 2. Verificar o Acesso aos Serviços

Após subir o ambiente, você pode acessar as interfaces dos serviços nos seguintes endereços:

| Serviço | URL | Credenciais (Padrão) |
| :--- | :--- | :--- |
| **OpenMetadata** | [http://localhost:8585](http://localhost:8585) | `admin` / `admin` |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | `minioadmin` / `minioadmin` |
| **Trino UI** | [http://localhost:8080](http://localhost:8080) | - |

---

## 📊 Gerando Dados Sintéticos

Para testar o ambiente, incluímos um script Spark que gera transações financeiras fictícias e as registra no Trino.

Execute o container do Spark para processar os dados:

```bash
docker-compose run --rm spark-app
```

Este comando irá:
1. Gerar dados sintéticos no formato Parquet.
2. Salvar os arquivos no MinIO em `s3a://datalake/sandbox/financial_transactions`.
3. Registrar a tabela `financial_transactions` no schema `sandbox` do catálogo Hive no Trino.

---

## 🔍 Configurando o OpenMetadata

Para visualizar os dados no catálogo do OpenMetadata:

1. Acesse o **OpenMetadata** ([http://localhost:8585](http://localhost:8585)).
2. Vá em **Settings** > **Database Services** > **Add New Service**.
3. Selecione **Trino**.
4. Configure a conexão:
   - **Host and Port**: `trino:8080`
   - **Username**: `admin`
   - **Catalog**: `hive`
5. Salve e vá na aba **Ingestion**.
6. Adicione um **Metadata Ingestion** e execute o pipeline.
7. Após a conclusão, a tabela `sandbox.financial_transactions` aparecerá na busca do OpenMetadata com seus metadados e linhagem.

---

## ✅ Verificação de Conformidade

Para garantir que tudo está funcionando conforme o esperado, verifique:

- [ ] Os containers `minio`, `hive-metastore`, `trino` e `openmetadata-server` estão rodando.
- [ ] Você consegue listar o bucket `datalake` no console do MinIO após a execução do script Spark.
- [ ] Você consegue consultar a tabela no Trino:
  ```bash
  docker exec -it trino trino --execute "SELECT * FROM hive.sandbox.financial_transactions LIMIT 10;"
  ```
- [ ] A tabela e suas colunas estão visíveis no OpenMetadata.

---

## 🧹 Limpando o Ambiente

Para parar e remover todos os recursos criados:

```bash
docker-compose down -v
```
*(O parâmetro `-v` remove os volumes persistentes, resetando o banco de dados e o storage).*
