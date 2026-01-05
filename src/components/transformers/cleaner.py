import re

class TextCleaner:
    def __init__(self,min_length: int = 80):
        self.min_length=min_length

    def clean(self,text: str)->str:
        if not text:
            return ""
        
        text = text.replace("\x00", " ") # remplace les caractères nuls, cassent parfois les embeddings et splitters
        text = re.sub(r"\s+", " ", text) # normalise les espaces
        return text.strip() # supprime les espaces au début et à la fin  puis les retours à la ligne inutiles
    
    def filter(self,documents):
        cleaned_docs = []

        for doc in documents:
            doc.page_content = self.clean(doc.page_content)

            if len(doc.page_content) > self.min_length:   # enlève pages vides / quasi vides, 80 bon compromis
                cleaned_docs.append(doc)

        return cleaned_docs