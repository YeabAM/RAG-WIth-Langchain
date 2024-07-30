# RAG-WIth-Langchain

## Overview

RAG-WIth-Langchain is a project that aims to provide a tool for answering questions about specific documents. It uses the Langchain library which is a toolkit for building dialogue systems and question answering systems. This project uses the Chroma library to store and retrieve documents and their embeddings.

## Technology

The project is built using Python and the following libraries:

- Langchain: a toolkit for building dialogue systems and question answering systems.
- Chroma: a library for storing and retrieving documents and their embeddings.
- PyPDF: a library for reading and writing PDF files.

## Installation

To install the project, please follow these steps:

1. Clone the repository:
   
   
    git clone https://github.com/Yeabkalu/RAG-WIth-Langchain.git

2. Install the required python packages:
   
    
    
    pip install -r requirements.txt

3. Set up environmental variables:

    You need to set the following environmental variables:

    - `OPEN_AI_KEY`: your OpenAI API key
    - `CHROMA_PATH`: path to the directory where chroma will store its data

4. Load the data:

    Run the following command to load the data:

    
    
    python -m RAG_WIth_Langchain.load_data --add path/to/pdfs

5. Ask a question:

    Run the following command to ask a question:
    python -m RAG_WIth_Langchain.ask_data "What is the answer to question 1?"
<<<<<<<<<<<<<<  ✨ Codeium Command ⭐ >>>>>>>>>>>>>>>>
<<<<<<<  51e82210-f6ad-4393-904a-d57051342cc1  >>>>>>>