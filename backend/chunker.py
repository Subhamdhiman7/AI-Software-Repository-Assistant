from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = []

    for document in documents:

        texts = splitter.split_text(document["content"])

        for index, text in enumerate(texts):

            chunks.append({
                "content": text,
                "path": document["path"],
                "chunk_id": index
            })

    return chunks