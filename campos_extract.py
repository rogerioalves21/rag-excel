# -*- coding=utf-8 -*-

# Kor
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

# Langchain Models
from langchain_ollama import ChatOllama

# Standard Helpers
import time
import json

# For token counting
from langchain_community.callbacks import get_openai_callback

def getFileContent():
    with open('50059699220248210038.txt', 'r', encoding='UTF-8') as file:
        return file.read()

def printOutput(output):
    print(json.dumps(output, sort_keys=True, indent=3))

llm = ChatOllama(
    model = "nemotron-mini",  
    temperature = 0,
    num_ctx = 2048,
    num_predict = 512,
    keep_alive="15m0s",
)

juridico_schema = Object(
    id="processo",
    description="Informações sobre processos judiciais.",
    attributes=[
        Text(
            id="numero_processo",
            description="O número do processo.",
            examples=[
                ("Nº do processo 1002369-15.2024.8.18.0017", "1002369-15.2024.8.18.0017"),
                ("Número: 0831105-76.2024.8.23.0010", "0831105-76.2024.8.23.0010"),
                ("Processo: 0831105-76.2024.8.23.0010", "0831105-76.2024.8.23.0010")
            ],
            many=False
        ),
        Text(
            id="valor_causa_processo",
            description="O valor da causa.",
            examples=[
                ("VALOR DE CAUSA CORRESPONDE À R$ 894.751,45", "R$ 894.751,45"),
                ("A causa corresponde ao valor de R$ 50,29", "R$ 50,29"),
                ("Valor da causa: R$ 501,29", "R$ 501,29")
            ],
            many=False
        ),
        Text(
            id="classe_processual",
            description="A classe processual.",
            examples=[
                ("Classe da ação:    PROCEDIMENTO COMUM CRIMINAL", "PROCEDIMENTO COMUM CRIMINAL"),
                ("Classe Processual: 7 - Procedimento Comum Cível", "Procedimento Comum Cível"),
                ("Classe: PROCEDIMENTO COMUM CÍVEL", "PROCEDIMENTO COMUM CÍVEL"),
            ],
            many=False
        ),
    ],
    examples=[
        (
            "Processo: 0831105-76.2024.8.23.0010.\nValor de causa: R$ 7.350,00.\n Classe Processual: 7 - Procedimento Comum Cível.",
            [
                {"numero_processo": "0831105-76.2024.8.23.0010"},
                {"valor_causa_processo": "R$ 7.350,00"},
                {"classe_processual": "Procedimento Comum Cível"},
            ]
        )
    ],
    many=False
)

chain = create_extraction_chain(llm, juridico_schema)

text = getFileContent()
#print(chain.get_prompts()[0].format_prompt(text=text).to_string())
output = chain.invoke((text))["data"]
printOutput(output)