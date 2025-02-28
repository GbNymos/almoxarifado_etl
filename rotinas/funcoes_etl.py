import pdfplumber
from prettytable import PrettyTable
import sqlite3
from sqlite3 import Error

def tratar_erro(funcao):
    """Decorator para tratamento de  erros."""
    def wrapper(*paramet, **chavs):
        try:
            return funcao(*paramet, **chavs)
        except Exception as erro:
            print(f"\033[31;40m Problema: {erro.__class__} - {erro} \033[0m")
            return None
    return wrapper    

@tratar_erro
def extracaoTabela(path_pdf):
    """ Recebe como parametro o caminho do pdf
    Extarir dados de um pdf 
    O retorno: listas de tabelas(paginas) em uma unica tabela(lista_processamento)"""
    tabela_processamento=list()
    with pdfplumber.open(path_pdf) as pdf:
        for paginas in pdf.pages:
            tabelas=paginas.extract_tables()
            for tabela in tabelas:
                for linhas in tabela:
                    tabela_processamento.append(linhas)
        return tabela_processamento

@tratar_erro
def tratamentoDados(tabela_processamento):
    """Recebe como parametro uma lista
    Tratar os dados dividindo-os em duas listas de acordo com a quantidade de None 
    Retirar os None
    retorna duas listas separadas por padrao."""
    tabela_processamento.pop(0)

    item_grupo = [
        [item for item in linhas if item is not None] 
        for linhas in tabela_processamento 
        if linhas.count(None) >= 2 
        ]      
    item_almoxarifado= [
        [item for item in linhas if item is not None]
        for linhas in tabela_processamento
        if linhas.count(None) < 2
        ]
    del tabela_processamento
    return item_grupo , item_almoxarifado

def conexao(path_bd):
    """Recebi o caminho do banco de dados
       Retorna a conexao"""
    try:
        conector=sqlite3.connect(path_bd)
        print("\033[32;40m Conectado com sucesso \033[0m")
        return conector
    except Error as erro:
        print(f"\033[31;40m ERRO AO CONECTAR: {erro} \033[0m")
        return None
    
def carregamento(grupo,item,path_bd):
    """Carregar os dados para o banco_dados com condicao para inserir a Fk
    Parametros lista,lista,caminho_para_banco_dados
    fechar o banco_de_dados"""
    try:
        conx=conexao(path_bd)
        cursor=conx.cursor()

        for linhas in grupo:
            cursor.execute("INSERT OR IGNORE INTO Grupo (codigo_grupo, denominacao_grupo) VALUES (?, ?);", (linhas[0], linhas[1]))
        for linhas in item:
            codigo_item = str(linhas[1]) 
            codigo_grupo = codigo_item[:4] 

            cursor.execute("SELECT codigo_grupo FROM Grupo WHERE codigo_grupo = ?;", (codigo_grupo,))
            grupo_existente = cursor.fetchone()

            if grupo_existente:  
                cursor.execute("""
                    INSERT OR IGNORE INTO Item_almoxarifado 
                    (codigo_item, denominacao_item, unidade_medida, codigo_grupo) 
                    VALUES (?, ?, ?, ?);
                """, (linhas[1], linhas[2], linhas[3], codigo_grupo))
            else:
                print(f"\033[31;40m Erro: Grupo {codigo_grupo} não encontrado para o item de codigo: ({linhas[2]}). \033[0m")
        conx.commit()
        print("\033[32;40m Dados inseridos com sucesso \033[0m")
    except Error as erro:
        print(f"\033[31;40m Erro ao inserir dados {erro} \033[0m")
        return None
    finally:
        conx.close()

def visualizacao_final(path_bd):
    """Exibe uma demostracao organizada da tabela Grupo do Banco de dados
       incentiva a continuar fazendo consultas com o Sqlite"""
    
    print("\033[33;40m -- PROGRAMA FINALIZADO COM SUCESSO -- \033[0m")
    conx=conexao(path_bd)
    cursor=conx.cursor()
    cursor.execute("SELECT * FROM Grupo;")
    dados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    tabela = PrettyTable()
    tabela.field_names = colunas
    for linha in dados:
        tabela.add_row(linha)
    conx.close()
    print(tabela)
    print("\033[32mAgora é sua vez! Experimente novas consultas nesse banco de dados. \033[0m ")