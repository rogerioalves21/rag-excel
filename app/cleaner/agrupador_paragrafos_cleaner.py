from app.cleaner.cleaner_base import BaseCleaner
import re
from app.cleaner.helper import (
    PARAGRAPH_PATTERN,
    PARAGRAPH_PATTERN_RE,
    DOUBLE_PARAGRAPH_PATTERN_RE,
    UNICODE_BULLETS_RE,
    E_BULLET_PATTERN,
    UNICODE_BULLETS_RE_0W,
    TWO_OR_MORE_SPACES_NOT_NEW_LINE
)

class AgrupadorParagrafosCleaner(BaseCleaner):
    
    def _group_bullet_paragraph(self, paragraph: str) -> list:
        """Groups paragraphs with bullets that have line breaks for visual/formatting purposes.
        For example:

        '''○ The big red fox
        is walking down the lane.

        ○ At the end of the lane
        the fox met a friendly bear.'''

        Gets converted to

        '''○ The big red fox is walking down the lane.
        ○ At the end of the land the fox met a bear.'''
        """
        clean_paragraphs = []
        paragraph = (re.sub(E_BULLET_PATTERN, "·", paragraph)).strip()

        bullet_paras = re.split(UNICODE_BULLETS_RE_0W, paragraph)
        for bullet in bullet_paras:
            if bullet:
                clean_paragraphs.append(re.sub(PARAGRAPH_PATTERN, " ", bullet))
        return clean_paragraphs


    def _agrupar_paragrafos(
        self,
        text: str,
        line_split: re.Pattern[str] = PARAGRAPH_PATTERN_RE,
        paragraph_split: re.Pattern[str] = DOUBLE_PARAGRAPH_PATTERN_RE,
    ) -> str:
        """Groups paragraphs that have line breaks for visual/formatting purposes.
        For example:

        '''The big red fox
        is walking down the lane.

        At the end of the lane
        the fox met a bear.'''

        Gets converted to

        '''The big red fox is walking down the lane.
        At the end of the land the fox met a bear.'''
        """
        paragraphs = paragraph_split.split(text)
        clean_paragraphs = []

        for paragraph in paragraphs:
            if not paragraph.strip():
                clean_paragraphs.append(paragraph)
                continue
            if re.search(TWO_OR_MORE_SPACES_NOT_NEW_LINE, paragraph):
                clean_paragraphs.append(paragraph)
                continue
            
            para_split = line_split.split(paragraph)
            all_lines_short = all(len(line.split(" ")) < 5 for line in para_split) # .strip().split(" ")) < 5 for line in para_split)

            if UNICODE_BULLETS_RE.match(paragraph) or E_BULLET_PATTERN.match(paragraph): # .strip()) or E_BULLET_PATTERN.match(paragraph.strip()):
                clean_paragraphs.extend(self._group_bullet_paragraph(paragraph))
            elif all_lines_short:
                clean_paragraphs.extend([line for line in para_split if line]) #.strip()])
            else:
                clean_paragraphs.append(re.sub(PARAGRAPH_PATTERN, " ", paragraph))
        
        return "".join(clean_paragraphs)
        ## return "\n\n".join(clean_paragraphs)
    
    def clean(self, content) -> str:
        # print(content)
        para_split_re = re.compile(r"(\s*[\.;\n]\n\s*){1}")# re.compile(r"(\s*\n\s*){2}")
        clenead = self._agrupar_paragrafos(content, paragraph_split=para_split_re)
        para_split_re = re.compile(r"(\s*\n\s*){2}")
        return self._agrupar_paragrafos(clenead, paragraph_split=para_split_re)
