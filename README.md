# migration_backend

### Install requirements

pip install -r requirements/local.txt
pip install -r requirements/base.txt

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd migration_backend
celery -A config.celery_app worker -l info --concurrency=16
```

```bash
cd migration_backend
celery -A config.celery_app flower
```

## Explicação da solução

Para esse projeto foi utilizado o dataset MovieLens 20M, com funcionalidades de importação de seus dados e tabelas, nosso banco de dados ficou da seguinte forma:

## Modelos de Dados

Todas essas tabelas vem diretamente das colunas dos arquivos

### Movie

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `movieid` | `IntegerField`  | `primary_key=True`, `unique=True`  | ID do filme                  |
| `title`   | `CharField`     | `max_length=255`, `null=True`     | Título do filme              |
| `genres`  | `CharField`     | `max_length=255`, `null=True`     | Gêneros do filme             |

### Link

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `movieid` | `ForeignKey`    | `on_delete=models.CASCADE`        | Relacionado a `Movie`        |
| `imdbid`  | `CharField`     | `max_length=100`, `null=True`     | ID do IMDb                   |
| `tmdbid`  | `CharField`     | `max_length=100`, `null=True`     | ID do TMDb                   |

### GenomeScore

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `movieid` | `ForeignKey`    | `on_delete=models.CASCADE`        | Relacionado a `Movie`        |
| `tagid`  | `IntegerField`   | `null=True`                       | ID da tag                    |
| `relevance` | `FloatField`  | `null=True`                       | Relevância da tag            |

### GenomeTag

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `tagid`  | `IntegerField`   | `null=True`                       | ID da tag                    |
| `tag`    | `CharField`     | `max_length=255`, `null=True`     | Nome da tag                  |

### Rating

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `userid` | `IntegerField`   | `null=True`                       | ID do usuário                |
| `movieid` | `ForeignKey`    | `on_delete=models.CASCADE`        | Relacionado a `Movie`        |
| `rating` | `FloatField`     | `null=True`                       | Nota atribuída               |
| `timestamp` | `CharField`   | `max_length=100`, `null=True`     | Timestamp da avaliação       |

### Tag

| Campo    | Tipo            | Atributos                         | Descrição                    |
|----------|-----------------|-----------------------------------|------------------------------|
| `userid` | `IntegerField`   | `null=True`                       | ID do usuário                |
| `movieid` | `ForeignKey`    | `on_delete=models.CASCADE`        | Relacionado a `Movie`        |
| `tag`    | `CharField`     | `max_length=255`, `null=True`     | Tag associada ao filme       |
| `timestamp` | `CharField`   | `max_length=100`, `null=True`     | Timestamp da tag


### UploadedFile

Essa tabela foi feita para guardar o caminho do arquivo salvo e as informações do processamento

| Campo            | Tipo            | Atributos                         | Descrição                        |
|------------------|-----------------|-----------------------------------|----------------------------------|
| `file_name`      | `CharField`     | `max_length=255`                  | Nome do arquivo                  |
| `uploaded_at`    | `DateTimeField` | `auto_now_add=True`               | Data e hora do upload            |
| `status`         | `CharField`     | `max_length=50`, `default='Processing'` | Status do processamento         |
| `success_count`  | `IntegerField`  | `default=0`, `null=False`, `blank=True` | Contador de sucessos            |
| `error_count`    | `IntegerField`  | `default=0`, `null=False`, `blank=True` | Contador de erros               |
| `processing_duration` | `DurationField` | `null=True`, `blank=True`         | Duração do processamento         |
| `start_time`     | `DateTimeField` | `null=True`, `blank=True`         | Hora de início do processamento  |
| `end_time`       | `DateTimeField` | `null=True`, `blank=True`         | Hora de término do processamento |

### ProcessChunk

Aqui são salvos todos os chunks processados dos arquivos, e também serve para contabilizar os chunks terminados, bem como os erros que possam ter encontrado

| Campo            | Tipo            | Atributos                         | Descrição                        |
|------------------|-----------------|-----------------------------------|----------------------------------|
| `uploaded_file`  | `ForeignKey`    | `on_delete=models.CASCADE`        | Relacionado a `UploadedFile`     |
| `ended`          | `DateTimeField` | `auto_now_add=True`               | Data e hora de término           |
| `start_row`      | `IntegerField`  | `null=True`                       | Linha inicial                    |
| `end_row`        | `IntegerField`  | `null=True`                       | Linha final                      |
| `status`         | `CharField`     | `max_length=255`, `null=True`     | Status do processamento          |
| `errors`         | `TextField`     | `null=True`                       | Erros encontrados                |


## Modelo lógico

![image](https://github.com/user-attachments/assets/285e0b17-0508-4e98-9609-5140ebaa4912)

## Explicação do Projeto

Nosso projeto é dividido em duas partes principais: Front End e Back End. A divisão foi feita para facilitar o consumo de APIs externas e o envio de arquivos. Algumas abordagens de processamento no Front End foram abandonadas em favor de uma solução mais eficiente no Back End.

O projeto pode ser dividido em três momentos principais:

1. **Envio e Salvamento do Arquivo:**
   - Inicialmente, considerou-se a divisão do arquivo diretamente no Front End, enviando-o em partes para o Back End. No entanto, optamos por uma abordagem mais eficiente, lendo o arquivo no Back End em chunks (pedaços) e salvando-o dessa forma. Isso proporciona um melhor desempenho e facilita o gerenciamento do processamento de grandes arquivos.

2. **Processamento dos Dados:**
   - O processamento é realizado em etapas, onde o arquivo é dividido em pedaços menores para processamento paralelo. Cada pedaço é lido, transformado e inserido no banco de dados de forma eficiente. O uso de processamento em chunks permite lidar com grandes volumes de dados sem sobrecarregar o sistema.

3. **Gerenciamento de Erros e Monitoramento:**
   - Implementamos um sistema robusto para o gerenciamento de erros durante o processamento. Caso ocorra algum problema, o sistema tenta processar novamente até um máximo de três tentativas. Se o problema persistir, registramos o erro e atualizamos o status do arquivo para monitorar o progresso e facilitar a identificação de problemas.

## Processamento de Arquivos CSV

O processamento de arquivos CSV é gerenciado em duas etapas principais para garantir eficiência e robustez na inserção de dados no banco de dados.

### Etapa 1: Divisão do Arquivo em Pedaços

**Função: `stream_csv_in_chunks`**

1. **Leitura do Arquivo**:
   - O arquivo CSV é lido para calcular o número total de linhas.

2. **Determinação do Tamanho dos Pedaços**:
   - O arquivo é dividido em pedaços de tamanho definido por `chunk_size` (30.000 linhas por padrão). Se o número total de pedaços for menor que 12, o tamanho do pedaço é ajustado para garantir que o arquivo seja dividido em pelo menos 12 pedaços.

3. **Criação de Tarefas**:
   - Para cada pedaço, uma tarefa `process_chunk` é criada e agendada. Cada tarefa é responsável pelo processamento e inserção de um pedaço específico do arquivo CSV.

### Etapa 2: Processamento dos Pedaços

**Função: `process_chunk`**

1. **Leitura do Pedaço**:
   - O pedaço do arquivo CSV correspondente ao intervalo de linhas (`start_row` a `end_row`) é lido usando a biblioteca Polars.

2. **Preparação dos Dados**:
   - Os dados do pedaço são convertidos em um buffer de bytes, pronto para a inserção em massa no banco de dados PostgreSQL.

3. **Inserção em Massa**:
   - Dependendo do nome da tabela associado ao arquivo (`ratings`, `tags`, `movies`, `links`, `genome_scores`, `genome_tags`), os dados são inseridos na tabela apropriada usando o comando `COPY` do Psycopg2.

4. **Gerenciamento de Erros**:
   - Se ocorrer um erro durante a inserção, a transação é revertida e a tarefa é re-tentada até um máximo de 3 vezes. Se todas as tentativas falharem, um registro é criado na tabela `ProcessChunk` com detalhes do erro.

5. **Atualização de Status**:
   - Após o processamento de cada pedaço, o status do arquivo carregado é atualizado para refletir o número de sucessos e erros. A duração total do processamento é calculada e registrada.


## Descrição dos passos de desenvolvimento

Dividiu-se o desenvolvimento também em 3 partes, onde inicialmente testou-se abordagens do envio do arquivo CSV e salvamento.

Depois fomos para as técnicas de leitura do CSV e escrita no banco de dados. Nesse ponto decidiu-se usar o polars por sua boa otimização e o cursor do psycopg2 para ser o mais otimizado possível.
