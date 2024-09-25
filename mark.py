import pymupdf4llm
import codecs

import pymupdf4llm
import pymupdf
import pathlib

# --------------------------------------------------------------------------
# EXTRAÇÃO DE PDF PARA MARKDOWN
# --------------------------------------------------------------------------
#md_text = pymupdf4llm.to_markdown("/home/rogerio_rodrigues/workspace/A.pdf")
#print(md_text)
#import sys; sys.exit(0)
# --------------------------------------------------------------------------
# EXTRAÇÃO DE PDF PARA MARKDOWN
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# EXTRAÇÃO DE TXT PARA MARKDOWN
# --------------------------------------------------------------------------
doc = pymupdf.open("A.txt", filetype="txt")
md_txt = pymupdf4llm.to_markdown(doc, extract_words=True)
print(md_txt)
pathlib.Path("A.md").write_bytes(md_txt.encode())
import sys; sys.exit(0)
# --------------------------------------------------------------------------
# EXTRAÇÃO DE TXT PARA MARKDOWN
# --------------------------------------------------------------------------

# now work with the markdown text, e.g. store as a UTF8-encoded file
# pathlib.Path("Pades_CREDIPEU370.949.md").write_bytes(md_text.encode())

#md_txt = pymupdf4llm.to_markdown(doc)

# write markdown string to some file
#pathlib.Path("cci.md").write_bytes(md_txt.encode())

print("FOI")

# https://github.com/search?q=repo%3Adiscourse%2Fdiscourse-ai+markdown&type=code


