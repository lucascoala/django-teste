# Django Project with Docker

Este é um projeto Django configurado para rodar em ambiente local usando Docker e Docker Compose. Siga as instruções abaixo para configurar e executar o projeto.

---

## Pré-requisitos

Certifique-se de que os seguintes softwares estão instalados no seu sistema:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Como Configurar o Ambiente Local

### 1. Clone o Repositório

Clone o repositório do projeto para o seu ambiente local:

```bash
git clone https://github.com/Serjao67/mysite.git
cd mysite
```

2. Configuração de Variáveis de Ambiente

Certifique-se de que um arquivo .env esteja presente no diretório raiz do projeto. Caso contrário, crie-o com base no arquivo de exemplo (.env.example):

```bash
cp .env.example .env
```

Atualize as variáveis no .env conforme necessário, como credenciais do banco de dados ou configurações de depuração.

3. Suba os Contêineres com Docker Compose

Para rodar o ambiente local, utilize o comando abaixo para iniciar os contêineres do Docker:

```bash
docker-compose up --build
```

Isso irá:
	•	Construir as imagens Docker (caso ainda não estejam construídas).
	•	Criar e inicializar os contêineres para o servidor Django, banco de dados e outros serviços configurados no docker-compose.yml.

4. Acesse o Projeto

Após o comando ser executado com sucesso, o servidor Django estará disponível em:

```bash
http://localhost:8000
```

Comandos Úteis

Executar Migrações

Se você precisar executar migrações no banco de dados, use o seguinte comando:

```bash
docker-compose exec web python manage.py migrate
```

Criar um Superusuário

Para criar um superusuário para acessar o admin do Django:

```bash
docker-compose exec web python manage.py createsuperuser
```

Acessar o Shell do Django

Para acessar o shell interativo do Django:

```bash
docker-compose exec web python manage.py shell
```

Parar os Contêineres

Para parar os contêineres em execução:

```bash
docker-compose down
```

Estrutura do Projeto

	•	docker-compose.yml: Configuração para os contêineres Docker.
	•	Dockerfile: Instruções para construir a imagem Docker do servidor Django.
	•	requirements.txt: Dependências do projeto Django.
	•	manage.py: Script de gerenciamento do Django.

Tecnologias Usadas

	•	Django: Framework backend Python.
	•	MySQL: Banco de dados relacional.
	•	Docker: Gerenciamento de contêineres.
	•	Docker Compose: Orquestração de múltiplos contêineres.

Possíveis Problemas e Soluções

1. Permissões no Docker

Se você enfrentar problemas de permissão ao executar os comandos do Docker, tente executá-los com sudo:

```bash
sudo docker-compose up --build
```

2. Problemas de Cache

Se alterações recentes no código não estiverem refletindo, remova os contêineres e as imagens do cache:

```bash
docker-compose down --rmi all
docker-compose up --build
```

3. Conflito de Portas

Se a porta 8000 já estiver sendo usada por outro processo, altere a porta mapeada no docker-compose.yml para outra porta disponível, por exemplo, 8080.

No docker-compose.yml:

ports:
  - "8080:8000"

Contribuição

Se você deseja contribuir para o projeto:

- Faça um fork do repositório.

- Crie uma branch para sua feature/bugfix:
```bash
git checkout -b minha-feature
```
- Faça o commit de suas alterações:
```bash
git commit -m "Minha nova feature"
```
- Envie as alterações:
```bash
git push origin minha-feature
```
- Abra um Pull Request.

Contato

Para dúvidas ou sugestões, entre em contato:
	•	GitHub: Serjao67

