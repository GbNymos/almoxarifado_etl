# Extração e Modelagem de Dados de Almoxarifado
Script para extrair, transformar e carregar dados de um
arquivo PDF contendo informações de um almoxarifado, modelando-os em um banco de
dados relacional.

## Tecnologias usadas e Pré-requisitos
![Python](https://img.shields.io/badge/python-3.x-blue?logo=python&logoColor=white)

![SQLite](https://img.shields.io/badge/sqlite-3.x-green?logo=sqlite&logoColor=white)



## Dependências:
Para instalar as dependências necessárias, execute o comando:
```bash
pip install pdfplumber PrettyTable
```


## Como Executar
### 1_Passo: Criando o banco de dados:
Abra o terminal no diretório do projeto (almoxarifado_etl) e execute:
```bash
sqlite3 db/db_almoxarifado.db 
```
Carregue a estrutura do banco de dados:
```bash
.read db/ddl_almoxarifado.sql
```
Saia do SQLite:
```bash
.exit
```
### 2_Passo:  Executando o Script
Agora, basta rodar o programa principal:
```bash
python main.py
```


## Instruções de Uso
- O script lê um arquivo PDF contendo tabelas de almoxarifado.
- Os dados extraídos são processados e carregados no banco de dados db_almoxarifado.db.
- Você pode executar consultas no banco após a execução do script.
    - Exemplo: 
    Conectando-se ao banco novamente:
    ```bash 
    sqlite3 db/db_almoxarifado.db 
    SELECT * FROM Item_almoxarifado;
    ```


## Autora
- [@Gabriele sant](https://github.com/GbNymos)



## Licença
[MIT](https://choosealicense.com/licenses/mit/)
