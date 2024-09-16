from typing import Tuple
import pandas as pd
import io
import re
from fastapi import UploadFile
import codecs

class DataAnalysisService():
    """ Classe responsável por converter arquivos PDF em Imagens.
        Transforma as mesmas em textos, e inclui em base de dados (memória).
    """
    def __init__(self):
        print('Data Analysis Service')

    def __build_llama_prompt(self, data_frame: str) -> str:
        data_frame = re.sub('Unnamed: \\d{1,2}','', data_frame)
        return F"""Conjunto de dados:
```dataframe
{data_frame}
```
""".strip()

    def __build_prompt(self, __dataframe: str) -> str:
            return F"""Conjunto de dados:
    ```dataframe
    {__dataframe}
    ```
    """.strip()

    async def write_content_files(self, __files: list[UploadFile]) -> None:
        __file = __files.pop()
        __file_contents = await __file.read()
        __tabs = pd.read_excel(io.BytesIO(__file_contents), engine="calamine", sheet_name=None)
        print(__tabs)
        __keys = __tabs.keys()
        for __key in __keys:
            __excel = __tabs[__key]
            __content = re.sub('Unnamed: \\d{1,2}','          ', __excel.to_string())
            __content = __content.replace('NaN', '   ')
            __nome_arquivo = __file.filename.replace('.xlsx', f'_{__key}.txt')
            __nome_arquivo = __nome_arquivo.replace(' ', '_')
            with codecs.open(__nome_arquivo, 'w', encoding='UTF-8') as arquivo:
                arquivo.write(__content)

    def get_file_content(self, __filename: str) -> str:
        print(__filename)
        __content = ''
        with open(__filename, 'r', encoding='UTF-8') as arquivo_leitura:
            __content = arquivo_leitura.read()
            print(__content)
        return __content

    def chat_with_file(self, __context: str, __query: str):
        __system_message_excel = "Você é um dedicado analista de dados, especialista em tabelas, excel, relatórios e planilhas. Seu objetivo é ajudar as pessoas fazendo análises detalhadas, insights robustos e sugestões de análises específicas para informações relevantes sobre os dados do dataframe."
        
        if not __query or len(__query) == 0:
            return F"""
{self.__build_prompt(__context)}

Com base no conjunto de dados fornecido, analise e apresente de 2 a 5 observações, destaques, insights ou tendências mais interessantes.

Sua análise deve ser detalhada e criteriosa, concentrando-se nos aspectos mais atraentes do conjunto de dados.
Forneça um resumo claro e conciso que destaque as principais conclusões, garantindo que as tendências ou observações sejam apresentadas de forma envolvente e informativa.

Pense passo a passo.
Responda em português."""
        else:
            return F"""
{self.__build_prompt(__context)}

Com base no conjunto de dados fornecido. {__query}

Responda em português."""
       
    def chat(self, query: str) -> Tuple[str, str]:
        __system_message_excel = "Você é um dedicado analista de dados, especialista em tabelas, excel, relatórios e planilhas. Seu objetivo é ajudar as pessoas fazendo análises detalhadas, insights robustos e sugestões de análises específicas para informações relevantes sobre os dados do dataframe."
        __df = pd.read_excel(
            "C:/Users/rogerio.rodrigues/documents/exRelCoop.xlsx",
            sheet_name=[0],
            date_format="DD/MM/YYYY HH:MM:SS",
            na_values='-',
            verbose=True
        )

        if not query or len(query) == 0:
            return F"""
{self.__build_llama_prompt(data_frame=__df[0].to_csv(compression='infer', index=False, encoding="UTF-8", sep=";"))}

Com base no conjunto de dados fornecido, analise e apresente de 2 a 5 observações, destaques, insights ou tendências mais interessantes.

Sua análise deve ser detalhada e criteriosa, concentrando-se nos aspectos mais atraentes do conjunto de dados.
Forneça um resumo claro e conciso que destaque as principais conclusões, garantindo que as tendências ou observações sejam apresentadas de forma envolvente e informativa.

Pense passo a passo.
Responda em português.""", __system_message_excel
        else:
            return F"""
{self.__build_llama_prompt(data_frame=__df[0].to_csv(compression='infer', index=False, encoding="UTF-8", sep=";"))}

Com base no conjunto de dados fornecido. {query}

Responda em português.""", __system_message_excel

   