# Python 2 Legacy Code Conversion

Scripts for automated Python 2 to 3 migration:

## python_223_llm_llama.py
- **Purpose**: Batch conversion of legacy Python 2 codebases to Python 3
- **Key Features**:
  - Token-aware code chunking (512 token limit)
  - Llama-2 7B-powered code translation
  - Directory recursion for bulk processing
- **Conversion Logic**:
  - File handling modernization (with statements)
  - Print statement → function conversion
  - Exception handling syntax updates
  - Deprecated library replacements
- **Dependencies**:
  - LangChain Core
  - CTransformers
  - Llama-2 7B GGML model
- **Usage**:
```bash
python python_223_llm_llama.py
```
- **Output**: Creates *_converted.py files alongside originals
- **Note**: Always verify conversions - LLM may introduce subtle errors
