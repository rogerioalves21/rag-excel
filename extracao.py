from app.services.file_service import FilesService
from app.cleaner.agrupador_paragrafos_cleaner import AgrupadorParagrafosCleaner
import asyncio
from app.extractors.pdf_to_text import PdfToTextExtrator, Documento
from rich import print
import re
import codecs
from app.cleaner.helper import (
    PARAGRAPH_PATTERN,
    PARAGRAPH_PATTERN_RE,
    DOUBLE_PARAGRAPH_PATTERN_RE,
    UNICODE_BULLETS_RE,
    E_BULLET_PATTERN,
    UNICODE_BULLETS_RE_0W
)


async def get_pdf_content() -> None:
    pdftotext = PdfToTextExtrator()
    documento: Documento = pdftotext.extrair_texto('/home/rogerio_rodrigues/workspace/A.pdf')
    conteudo = documento.conteudo
    
    paginas = conteudo.split('\x0c')
    conteudo = paginas[0]
    
    # limpeza de textos
    #paragraph_split: re.Pattern[str] = DOUBLE_PARAGRAPH_PATTERN_RE
    
    #paragraphs = paragraph_split.split(conteudo)
    #clean_paragraphs = []
    #for paragraph in paragraphs:
    #    if not paragraph.strip():
    #            continue
    #    print('---------------------')
    #    print(paragraph)
    #    print('---------------------')
    
    paragrafo_cleaner = AgrupadorParagrafosCleaner()
    conteudo = paragrafo_cleaner.clean(conteudo)
    print(conteudo)
    with codecs.open('A.txt', 'w', encoding='UTF-8') as arquivo:
        arquivo.write(conteudo)
    

async def save_excel_content() -> None:
    servico = FilesService()
    servico.save_content_file(
        '/home/rogerio_rodrigues/workspace/rag-excel/rag-excel/intercredis_remessa_expressa.xlsx',
        'intercredis_remessa_expressa.xlsx'
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_pdf_content())