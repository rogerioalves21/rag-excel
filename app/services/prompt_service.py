import re
import yaml
from typing import Union

class PromptService():

    def __init__(self):
        print('Prompt Service')
        self.__prompts_file = '/home/rogerio_rodrigues/workspace/ragexcel/rag-excel/app/templates/prompts.yaml'

    def get_system_prompt(self) -> Union[str, None]:
        with open(self.__prompts_file, 'r', encoding='utf-8') as yamlfile:
            __data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            return __data['app']['system_prompt']
    
    def get_system_prompt_texto(self) -> Union[str, None]:
        with open(self.__prompts_file, 'r', encoding='utf-8') as yamlfile:
            __data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            return __data['app']['system_prompt_texto']
    
    def get_analytic_prompt(self) -> Union[str, None]:
        with open(self.__prompts_file, 'r', encoding='utf-8') as yamlfile:
            __data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            return __data['app']['analytic_prompt']

    def build_llama_prompt(self, __content: str) -> str:
        __content = re.sub('Unnamed: \\d{1,2}','', __content)
        return F"""
<dataframe>
{__content}
</dataframe>""".strip()


    def build_prompt(self, __content: str) -> str:
            return F"""
<dataframe>
{__content}
</dataframe>""".strip()

    def build_text_prompt(self, __content: str, __query: str) -> str:
                return F"""
**Documentos**
{__content}

**Pergunta**
{__query}""".strip()
