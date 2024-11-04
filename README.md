
# Objetivo do Projeto

Desenvolver uma API pública para consulta de dados do site: [Embrapa Vitibrasil](http://vitibrasil.cnpuv.embrapa.br/).

Para realizar a consulta dos dados, foi necessário criar um crawler para extrair informações diretamente do HTML do site. Em seguida, para tornar esses dados acessíveis publicamente, utilizamos o FastAPI para criar endpoints de consulta e realizamos o deploy na plataforma Vercel.

O entregável do projeto inclui:

- Desenvolvimento da API
- Documentação no Swagger
- Publicação da API (com link compartilhável)
- Desenho da arquitetura, com visão end-to-end dos dados extraídos até o consumo (desenho macro)

A documentação da API está disponível em: [Swagger Documentation](https://api-embrapa-tech-1-i9l0snkng-leonardo-lucas-pereiras-projects.vercel.app/docs)

Link para a API em produção: [API Pública](https://api-embrapa-tech-1-i9l0snkng-leonardo-lucas-pereiras-projects.vercel.app/)

Desenho da arquitetura:

![Desenho da arquitetura](https://github.com/lleonardo-p/api_embrapa_tech_1/blob/4a53ae8887de5876ea081f8d4e6e99fe4100307a/architecture/architecture.jpg)



---

# Instruções de Instalação e Execução

## Pré-requisitos

- Python 3.12 ou superior
- Poetry 1.8.4

## Passos para Instalação

1. **Criação de um Ambiente Virtual:**
   ```bash
   # Clone o repositório
   cd /caminho/para/o/repo

   # Crie um ambiente virtual com Poetry
   poetry env use python3.12

   # Ative o ambiente virtual
   poetry shell
   
   # Instale os pacotes necessários
   poetry install
   ```

2. **Execução da Aplicação:**
   ```bash
   poetry run uvicorn main:app --reload
   ```

3. **Acessar a API:**
   - Acesse a API em `http://localhost:8000`.

---
