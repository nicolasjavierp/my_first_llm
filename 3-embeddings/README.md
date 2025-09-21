# Examples Directory

Collection of LLM implementation examples:

## llm_stuffing.py
- **Purpose**: Text summarization using "stuffing" technique
- **Functionality**:
  - Chunks large text documents using GPT-2 tokenization
  - Processes chunks through Llama-2 7B model
  - Aggregates summaries for long-form content
- **Dependencies**:
  - CTransformers
  - LangChain
  - HuggingFace Tokenizers

## pdf_rag.py
- **Purpose**: PDF-based Retrieval Augmented Generation
- **Features**:
  - PDF text extraction and chunking
  - Vector store integration
  - Context-aware question answering

## Embeddings Subdirectory
See [embedings/README.md](embedings/README.md) for specialized embedding examples
