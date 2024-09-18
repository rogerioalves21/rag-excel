import pandas as pd
import io
import asyncio
from fastapi import UploadFile
import codecs
from app.utils import formatar_nome_arquivo, remover_caracteres_nulos, xlsx_to_txt, xlsx_to_md, xlsx_to_csv

class FilesService():


    def __init__(self):
        print('Files Service')
        self.__files_path = '/home/rogerio_rodrigues/workspace/ragexcel/rag-excel/app/uploaded_files'

    async def save_content_file(self, __file_path: str, __file_name: str) -> None:
        __tabs = pd.read_excel(__file_path, engine="calamine", sheet_name=None, parse_dates=True, date_format="%d/%M/%Y", index_col=None)
        __keys = __tabs.keys()
        for __key in __keys:
            __excel = __tabs[__key]
            __content = remover_caracteres_nulos(__excel.to_csv())
            __nome_arquivo = xlsx_to_csv(__file_name, __key)
            __nome_arquivo = formatar_nome_arquivo(__nome_arquivo)
            __nome_arquivo = f"{self.__files_path}/{__nome_arquivo.lower()}"
            with codecs.open(__nome_arquivo, 'w', encoding='UTF-8') as arquivo:
                arquivo.write(__content)

    async def save_content(self, __files: list[UploadFile]) -> None:
        __file = __files.pop()
        __file_contents = await __file.read()
        __tabs = pd.read_excel(io.BytesIO(__file_contents), engine="calamine", sheet_name=None)
        __keys = __tabs.keys()
        for __key in __keys:
            __excel = __tabs[__key]
            __content = remover_caracteres_nulos(__excel.to_string())
            __nome_arquivo = xlsx_to_txt(__file.filename, __key)
            __nome_arquivo = formatar_nome_arquivo(__nome_arquivo)
            __nome_arquivo = f"{self.__files_path}/{__nome_arquivo.lower()}"
            with codecs.open(__nome_arquivo, 'w', encoding='UTF-8') as arquivo:
                arquivo.write(__content)

    def get_content(self, __filename: str) -> str:
        __content = ''
        __full_path = f"{self.__files_path}/{__filename}"
        with open(__full_path, 'r', encoding='UTF-8') as arquivo_leitura:
            __content = arquivo_leitura.read()
        return __content

if __name__ == "__main__":
    servico = FilesService()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(servico.save_content_file('/home/rogerio_rodrigues/workspace/rag-excel/rag-excel/intercredis_remessa_expressa.xlsx'))