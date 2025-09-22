# LLM Starter Kit - Core Implementation

## Overview
This module contains foundational LLM integration patterns demonstrated through three key implementations:

1. **Data Pipeline (`first_csv_html_pdf_llama.py`)**
   - Read content between CSV/HTML/PDF formats
   - Integrated LLM data interpretation
   - Batch processing capabilities

2. **Core LLM Interactions (`first_llm_llama.py`)**
   - Chat completion patterns
   - Streaming responses
   - Model configuration management

3. **LangChain Integration (`ollama_langchain.py`)**
   - Ollama local model integration
   - Chain construction examples
   - Custom output parsers

## Features
- 🔄 Async/await support for high-throughput applications
- 📊 Built-in telemetry for LLM call monitoring
- 🔐 Environment-based secret management


## Usage Examples
- cd 0-first_steps/
- uv run python3 first_llm_llama.py
- uv run python3 first_csv_html_pdf_llama.py
- ollama serve &
- uv run python3 ollama_langchain.py
