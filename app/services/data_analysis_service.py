from typing import Tuple
import pandas as pd
from app.services.prompt_service import PromptService

class DataAnalysisService():

    def __init__(self):
        print('Data Analysis Service')
        self.__prompt_service = PromptService()
        self.__system_prompt = self.__prompt_service.get_system_prompt()
        self.__analytic_prompt = self.__prompt_service.get_analytic_prompt()
    
    def chat_with_text_file(self, __context: str, __query: str):
            return F"""
{self.__prompt_service.build_text_prompt(__context, __query)}
""".strip()
    
    def chat_with_file(self, __context: str, __query: str):
        if not __query or len(__query) == 0:
            return F"""
{self.__prompt_service.build_prompt(__context)}
{self.__analytic_prompt}"""
        else:
            return F"""
{self.__prompt_service.build_prompt(__context)}
{__query}""".strip()

    def chat(self, query: str) -> Tuple[str, str]:
        __system_message_excel = self.__system_prompt
        __df = pd.read_excel(
            "C:/Users/rogerio.rodrigues/documents/exRelCoop.xlsx",
            sheet_name=[0],
            date_format="DD/MM/YYYY HH:MM:SS",
            na_values='-',
            verbose=True
        )

        if not query or len(query) == 0:
            return F"""
{self.__prompt_service.build_llama_prompt(data_frame=__df[0].to_csv(compression='infer', index=False, encoding="UTF-8", sep=";"))}

{self.__analytic_prompt}""", __system_message_excel
        else:
            return F"""
{self.__prompt_service.build_llama_prompt(data_frame=__df[0].to_csv(compression='infer', index=False, encoding="UTF-8", sep=";"))}

Com base no conjunto de dados fornecido. {query}
""", __system_message_excel
