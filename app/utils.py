import re

cors_origins = [
    "*"
]

def xlsx_to_txt(__nome_arquivo: str, __tab: str) -> str:
    return __nome_arquivo.replace('.xlsx', f'_{__tab}.txt')

def xlsx_to_md(__nome_arquivo: str, __tab: str) -> str:
    return __nome_arquivo.replace('.xlsx', f'_{__tab}.md')

def xlsx_to_csv(__nome_arquivo: str, __tab: str) -> str:
    return __nome_arquivo.replace('.xlsx', f'_{__tab}.csv')

def formatar_nome_arquivo(__nome_arquivo: str) -> str:
    __nome_arquivo = __nome_arquivo.replace(' ', '_')
    return re.sub(r"[^a-zA-Z0-9\._]", "", __nome_arquivo)

def remover_caracteres_nulos(__conteudo: str) -> str:
    __content = re.sub('Unnamed: \\d{1,2}','          ', __conteudo)
    __content = __content.replace('NaN', '   ')
    __content = __content.replace('nan', '   ')
    return __content