<h1 align="center"> AI-CHATKIT </h1>
<p align="center">
  <strong style="background-color: green;">English</strong>
  |
  <a href="./README_zh.md" target="_Self">中文</a>
</p>
AI-CHATKIT is a full-stack AI agent chat tool built using components such as langGraph, FastAPI, NextJS, and Chroma.

This project serves as a template to help you quickly build related AI agent chat applications using the langGraph framework, and supports RAG (Retrieval-Augmented Generation) to enhance the knowledge base Q&A capabilities of agents.

<img src="./pictures/chat_img.png" width="700"/>  

multi-agent:

<img src="./pictures/chat_multi_agent_img.png" width="700"/>


## Features

1. AI agent chat application built on the langGraph framework, supporting custom behavior logic orchestration for agents.
2. Supports custom knowledge base Q&A capabilities for agents, using ChromaDB for knowledge base storage and querying.
3. Supports custom tool invocation for agents.
4. Python backend interface API, implemented based on FastAPI, Support full asynchronous calls.
5. Supports custom frontend applications for agents, implemented using NextJS.
6. Supports chat streaming output, with frontend support for SSE (Server-Sent Events) streaming.
7. Supports multiple custom agents
8. Support multi-agent collaboration
9. Chat history is saved in the local browser cache



## Structure

- `backend`: Backend service code
- `frontend`: Frontend service code

## Quick Start

### Backend Service


Backend .env file configuration
Rename .env.example to .env

```properties
# Environment variable configuration

# Database configuration
# SQLite URL
DATABASE_URL=sqlite+aiosqlite:///resource/database.db
# MySQL
# DATABASE_URL=mysql+aiomysql://root:root@localhost/ai-chatkit

# Application configuration
DEBUG=True
APP_NAME=AI ChatKit

# OpenAI
OPENAI_BASE_URL=
OPENAI_API_KEY=
DEFAULT_MODEL=gpt-4o-mini

# DashScope
#DASHSCOPE_API_KEY=
#DEFAULT_MODEL=qwen-plus

#DeepSeek
#DEEPSEEK_API_KEY=
#DEFAULT_MODEL=deepseek-chat



# Use bge-m3 as the embedding model, supporting both Chinese and English; requires local deployment of the bge-m3 model via Ollama
EMBEDDING_MODEL=bge-m3

# Relative storage path for ChromaDB
CHROMA_PATH=resource/chroma_db
```
run backend server:
```sh
# Use the uv tool to manage Python dependencies
pip install uv

# Replace ${workdir} with your own working directory
cd ${workdir}/backend

uv sync --frozen
# activate a Python virtual environment.
source .venv/bin/activate

# activate the environment variables on windows
# .venv/Script/active

#run server
python app/run_server.py
```

### RAG Deployment

This project by default accesses the locally deployed bge-m3 model via Ollama. Therefore, to access the knowledge base locally, you need to deploy Ollama locally. For local Ollama deployment of bge-m3, please refer to: https://ollama.com/library/bge-m3


### Frontend Application

```sh
# Replace ${workdir} with your own working directory
cd ${workdir}/frontend
# Use pnpm to manage dependencies
pnpm install
# Start the frontend application
pnpm dev
```

After successful startup, you can access the application at: http://localhost:3000/

You can use the langGraph extension in this project to create and orchestrate multiple agents, each with its own behavioral logic. The orchestration logic for agents can be written in the `backend/app/ai/agent` directory. You can switch between different agents for conversation in the frontend.

This project comes with the following agents:

1. **OA-ASSISTANT**: Mainly used to demonstrate the OA assistant agent, supporting employee information query and employee handbook knowledge base retrieval.
   For details, please refer to: `backend/app/ai/agent/oa_assistant.py`

2. **MULTI_AGENT**: Mainly used to demonstrate multi-agent collaboration, supporting collaboration between multiple agents. The multi_agent includes three agents:
   1) `math_agent`: Mathematical agent, mainly used for mathematical calculations
   2) `code_agent`: Code agent, mainly used for code generation
   3) `general_agent`: General agent, mainly used for handling general questions
   These three agents are collaboratively managed through a supervisor.

   For details, please refer to: `backend/app/ai/agent/multi_agent.py`







