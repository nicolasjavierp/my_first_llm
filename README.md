# My First LLM Project

## Installation
```bash
# 1. Clone repository
git clone https://github.com/nicolasjavierp/my_first_llm.git
cd my_first_llm

# 2. Install core dependencies
pip install -r requirements.txt

# 3. Set up MCP (Model Control Protocol)
cd MCP
docker-compose up -d  # Requires Docker 20.10+
```

## Key Components
| Component | Description | Docs Link |
|-----------|-------------|-----------|
| MCP | Model serving & tool orchestration | [MCP/README.md](MCP/README.md) |
| Chains | Sequential processing pipelines | [chains/README.md](chains/README.md) |
| Examples | Implementation patterns | [examples/README.md](examples/README.md) |
| Python2 Converter | Legacy code migration | [python2_code/README.md](python2_code/README.md) |

## Quickstart
```bash
# Start MCP server
cd MCP && docker-compose up -d

# Convert Python 2 code
python python2_code/python_223_llm_llama.py

# Run example chain
python chains/llm_Chain_PRs.py --review "your_performance_review.txt"

# Validate with test data
pytest tests/  # Coming soon!
```

## Version Compatibility
| Component | Python | LLM Model | LangChain |
|-----------|--------|-----------|-----------|
| MCP | 3.11 | llama3.1:8b | 0.1.11 |
| Chains | 3.9+ | deepseek-r1:1.5b | 0.1.15 |
| Converter | 2.7/3.11 | llama-2-7b-chat | 0.1.8 |

## Troubleshooting
```bash
# Common issues:
# 1. Missing model files - verify paths in:
#    - MCP/client.py
#    - python2_code/python_223_llm_llama.py 

# 2. Dependency conflicts:
python -m venv .venv
source .venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

