# Instruções de Instalação e Execução

Este documento fornece instruções sobre como instalar e executar a aplicação.

## Pré-requisitos

- Python 3.7 ou superior.
- `pip` (geralmente já incluído com o Python).

## Passos para instalação

1. **Criação de um Ambiente Virtual:**
   - É recomendável criar um ambiente virtual para isolar as dependências do projeto. Abra um terminal (ou prompt de comando) e execute os seguintes comandos:
     ```bash
     # Navegue até o diretório onde deseja criar o ambiente virtual
     cd /caminho/para/o/diretorio

     # Crie um ambiente virtual
     python -m venv venv

     # Ative o ambiente virtual
     # No Windows
     venv\Scripts\activate

     # No macOS/Linux
     source venv/bin/activate
     ```

2. **Baixar o arquivo `.whl`:**
   - Baixe o arquivo `.whl` fornecido para o seu diretório local.

3. **Instalação do Pacote:**
   - Com o ambiente virtual ativado, instale o pacote usando `pip`:
     ```bash
     pip install nome_do_pacote.whl
     ```
     (Substitua `nome_do_pacote.whl` pelo nome do arquivo que você enviou.)

## Passos para Execução

1. **Executar a Aplicação:**
   - Após a instalação, execute a aplicação com o seguinte comando:
     ```bash
     python -m api_embrapa_tech_1.api.main
     ```
2. **Acessar a API:**
   - Acesse a API em `http://localhost:8000`.

---
