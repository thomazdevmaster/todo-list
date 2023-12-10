# Todo-List API com Flask

## Esta é uma API de todo-list usando o framework Flask em Python, como produto do trabalho final da disciplina de Tópicos em Engenharia de Software 1 do Curso de Mestrado em Engenharia de Software da Universidade Federal de Lavras

- Professor: **Rafael Durelli**
- Aluno: **Thomaz Franklin de Souza Jorge**
- Data: **Dezembro de 2023**

---

## Execução e desenvolvimento

Certifique-se de ter o Python e o pip instalados no seu sistema.

> [veja o repositório aqui](https://github.com/thomazdevmaster/todo-list)

1. Clone o repositório

```git
git clone https://github.com/thomazdevmaster/todo-list
```

2. Entre na pasta

```sh
cd todo-list
```

3. Crie um Ambiente Virtual **(Opcional)**

```python
virtualenv venv

. ./venv/bin/activate
```

4. Instale as dependencias

```python
pip install -r requirements.txt
```

5. Toda a lógica do todo-list está no arquivo todo.py

6. Execute o flask

```python
python todo.py
```

7. Api rodando em localhost:5000/

- Estrutura json de uma task

```json
{
  "id": "id_task",
  "description": "descrição",
  "status": "Status",
  "created_at": "Data criação",
  "updated_at": "Última modificação",
  "completed_at": "Data de fechamento"
}
```

| Método | Endpoint          | Parâmetro                                     | retorno                    |
| ------ | ----------------- | --------------------------------------------- | -------------------------- | --------------------------------------- |
| GET    | /tasks            | - - -                                         | Lista com todas as tasks   | curl -X GET http://localhost:5000/tasks |
| POST   | /tasks            | body com task apenas com description e status |
| GET    | /tasks/< id: int> | id da task                                    | Task com id correspondente |
| PUT    | /tasks/< id: int> | id da task                                    | Mensagem de task alterada  |
| DELETE | /tasks/< id: int> | id da task                                    | Mensagem de task deletada  |

Exemplos com cURL:

- 1. Buscar todas tasks:

```sh
curl  -X GET \
  'localhost:5000/tasks' \
  --header 'Accept: */*'
```

- 2. Cadastrar task:

```sh
curl  -X POST \
  'localhost:5000/tasks' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "description": "Segunda tarefa do meu todo list",
    "status": "pending"
    }'
```

- 3. Buscar uma task pelo id

```sh
curl  -X GET \
  'localhost:5000/tasks/2' \
  --header 'Accept: */*'
```

- 4. Atualizar uma task

```sh
curl  -X PUT \
  'localhost:5000/tasks/2' \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "description": "Quinta tarefa do meu todo list",
    "status": "pending"
    }'
```

- 5. Apagar uma task

```sh
curl  -X DELETE \
  'localhost:5000/tasks/1' \
  --header 'Accept: */*'
```

## Docker

1. Dockerfile criado para ambiente de produção

```docker
# Imagem base
FROM python:3.9-alpine

# Instalação do gunicorn (ideal para produção)
RUN pip install gunicorn

# Configura algumas opções de execução do interpretador Python
# Não gerar bytecode e desativar buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Busca os arquivos necessários
WORKDIR /app
COPY . /app

# Cria e configura um usuário não privilegiado dentro do contêiner
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Subindo aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "todo:app"]

EXPOSE 5000
```

2. Criando imagem e colocando a tag de acordo com meu [DockerHub](https://hub.docker.com/r/thomazfsj/todo_list) e subindo a imagem

```docker
docker build -t thomazfsj/todo_list:latest .

docker push thomazfsj/todo_list:latest
```

## Helm Chart

1. Criação do chart

```sh
helm create helmchart
```

2. Substituição dos values

3. subindo aplicação

```sh
helm install todo helmchart
```

4. fazendo o port-forward para acessar
   4.1 setando environmens com nome do pod e porta do container

```sh
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=helmchart,app.kubernetes.io/instance=todo" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
```

4.2 Executando o port-forward

```sh
kubectl --namespace default port-forward $POD_NAME 5000:$CONTAINER_PORT
```

## Alterando o código:

1. Alteração de todas as mensagens para portugues

2. Realização do build da nova imagem com a tag latest

```sh
docker build -t thomazfsj/todo_list:latest .
```

3. Realização do push da imagem nova para o registry

```sh
docker push thomazfsj/todo_list:latest
```

4. atualização do chart executando

```sh
helm upgrade todo helmchart --install
```
