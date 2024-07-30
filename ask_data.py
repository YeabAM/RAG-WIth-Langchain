import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import os
from get_embedding_function import get_embedding_function
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get('OPEN_AI_KEY')
client = OpenAI(
    api_key=openai_api_key
)


chroma_persistent_path = os.environ.get('CHROMA_PATH', 'chroma')
prompt_template = ChatPromptTemplate.from_template(
    """
    Please carefully read the following context:
    {context}
    And then answer the following question:
    {question}
    Please provide a clear and concise response based only on the context.
    """
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str, help='query')
    args = parser.parse_args()
    query_text = args.query
    ask_data(query_text)


def ask_data(query_text):
    db = Chroma(persist_directory=chroma_persistent_path, embedding_function=get_embedding_function())
    search_results = db.similarity_search_with_score(query_text, k=3)
    context = "\n\n----\n\n".join([doc.page_content for doc, _score in  search_results])
    prompt = prompt_template.format(context=context, question=query_text)

    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )

    answer = response.choices[0].message.content
    print(answer)
    sources = set([doc.metadata.get("id", None) for doc, _score in search_results])
    answer_with_sources = f"{answer}, and the source it was based at are:\n{sources}"

    print(answer_with_sources)

    return answer_with_sources

if __name__ == "__main__":
    main()


