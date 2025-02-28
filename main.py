from rotinas import funcoes_etl

path_bd="db/db_almoxarifado.db"
path_pdf="pdf_dados\Lista_de_estoque_DMP.pdf" 


try:
    item_grupo,item_almoxarifado=funcoes_etl.tratamentoDados(funcoes_etl.extracaoTabela(path_pdf))
    funcoes_etl.carregamento(item_grupo,item_almoxarifado,path_bd)
    funcoes_etl.visualizacao_final(path_bd)

except Exception as erro:
    print(f"\033[31;40m Problema: {erro.__class__} - {erro} \033[0m")
