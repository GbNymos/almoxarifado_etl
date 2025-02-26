import pdfplumber


path_pdf="./pdf_dados\Lista_de_estoque_DMP.pdf"   

def tratar_erro(funcao):
    def wrapper(*paramet, **chavs):
        try:
            return funcao(*paramet, **chavs)
        except Exception as erro:
            print(f"\033[31;40m Problema: {erro.__class__} - {erro} \033[0m")
            return None
    return wrapper    



@tratar_erro
def extracaoTabela(path_pdf):
    tabela_processamento=list()
    with pdfplumber.open(path_pdf) as pdf:
        #extrair as tabelas das paginas
        for paginas in pdf.pages:
            tabelas=paginas.extract_tables()
            #transforma as listas de paginas em matrix
            for tabela in tabelas:
                for linhas in tabela:
                    tabela_processamento.append(linhas)
        return tabela_processamento


tabela_final=extracaoTabela(path_pdf)


@tratar_erro
def tratamentoDados(tabela_processamento):
    tabela_processamento[0][0]="id_item"
    #Filtra as linhas que possuem mais de um None
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
    return item_grupo , item_almoxarifado


print(tratamentoDados(tabela_final))


