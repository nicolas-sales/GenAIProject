from langchain_community.document_loaders import WebBaseLoader


class WebLoader:

    def __init__(self,urls: list[str]):
        if not isinstance(urls, list):
            raise TypeError("urls must be a list of strings")
        
        self.urls=urls

    def load(self):
        loader = WebBaseLoader(web_paths=self.urls)
        docs=loader.load()

        for doc in docs:
            doc.metadata["source_type"] = "web"
            doc.metadata["source_name"] = doc.metadata.get("title", "web")
            doc.metadata["source_id"] = doc.metadata.get("source")
            doc.metadata.pop("source", None)

        return docs