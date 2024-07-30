import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from langchain.schema.document import Document
from dotenv import load_dotenv

load_dotenv()

chroma_persistent_path = os.environ.get('CHROMA_PATH', 'chroma')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_load_document = subparsers.add_parser('load_document', help='load document')
    parser_load_document.add_argument('--add', action='store_true', help='add document to chroma')
    parser_load_document.add_argument('path', type=str, help='path to directory containing documents')

    parser_reset = subparsers.add_parser('reset', help='reset chroma persistence')

    args = parser.parse_args()

    if args.add:
        docs = load_and_split_data(path=args.path)
        add_to_chroma(docs)
    elif args.reset:
        shutil.rmtree(chroma_persistent_path , ignore_errors=True)
        os.makedirs(chroma_persistent_path , exist_ok=True)


def load_and_split_data(path):
    print(path)
    loader = PyPDFLoader(path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len, is_separator_regex=False)
    docs = text_splitter.split_documents(documents)
    return docs

def add_to_chroma(chunks: list[Document]):
    embeddings = get_embedding_function()
    db = Chroma(persist_directory=chroma_persistent_path , embedding_function=embeddings)
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])  
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}.......")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")
    return db

def calculate_chunk_ids(chunks):
    current_page_id = None
    chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == current_page_id:
            chunk_index += 1
        else:
            chunk_index = 0

        chunk_id = f"{current_page_id}:{chunk_index}"
        current_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

if __name__ == "__main__":
    main()
