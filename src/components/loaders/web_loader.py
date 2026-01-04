from langchain_community.document_loaders import WebBaseLoader

def load_web_pages(urls: list[str]):
    loader = WebBaseLoader(web_paths=urls)
    web_docs=loader.load()

    for doc in web_docs:
        doc.metadata["source_type"] = "web"
        doc.metadata["source_name"] = doc.metadata.get("title", "web")
        doc.metadata["source_id"] = doc.metadata.get("source")
        doc.metadata.pop("source", None)

        return web_docs