# Chains Directory

Contains sequential processing chains for LLM workflows:

## llm_Chain_PRs.py
- **Purpose**: Automated performance review analysis pipeline
- **Functionality**:
  - 3-stage sequential processing:
    1. Review summarization
    2. Weakness identification
    3. Action plan generation
  - Preserves intermediate results using MultiOutputPreserver class
  - Supports both automated LCEL chains and manual step execution
- **Dependencies**:
  - LangChain
  - Ollama
  - Logging
- **Usage**:
```python
from chains.llm_Chain_PRs import seq_chain_lcel

result = seq_chain_lcel.invoke({"review": your_review_text})
