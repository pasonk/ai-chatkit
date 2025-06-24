<h1 align="center"> AI-CHATKIT </h1>
<p align="center">
  <strong style="background-color: green;">English</strong>
  |
  <a href="./README_zh.md" target="_Self">中文</a>
</p>
AI-CHATKIT is a full-stack AI agent chat tool built using components such as langGraph, FastAPI, NextJS, and Chroma.

This project serves as a template to help you quickly build related AI agent chat applications using the langGraph framework, and supports RAG (Retrieval-Augmented Generation) to enhance the knowledge base Q&A capabilities of agents.

<img src="./pictures/chat_img.png" width="700"/>  

## Features

1. AI agent chat application built on the langGraph framework, supporting custom behavior logic orchestration for agents.
2. Supports custom knowledge base Q&A capabilities for agents, using ChromaDB for knowledge base storage and querying.
3. Supports custom tool invocation for agents.
4. Python backend interface API, implemented based on FastAPI
5. Supports custom frontend applications for agents, implemented using NextJS.
6. Supports chat streaming output, with frontend support for SSE (Server-Sent Events) streaming.
7. Supports multiple custom agents

## Structure

- `backend`: Backend service code
- `frontend`: Frontend service code

## Quick Start

### Backend Service

```sh
# Use the uv tool to manage Python dependencies
pip install uv
uv sync --frozen
# Create a Python virtual environment
source .venv/bin/activate
# Replace ${workdir} with your own working directory
cd ${workdir}/backend
python app/run_server.py
```

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

# It is recommended to use DeepSeek API; you can also use OpenAI
DEEPSEEK_API_KEY=
DEFAULT_MODEL=deepseek-chat

# OpenAI
#OPENAI_API_KEY
#DEFAULT_MODEL=gpt-4o-mini



# Use bge-m3 as the embedding model, supporting both Chinese and English; requires local deployment of the bge-m3 model via Ollama
EMBEDDING_MODEL=bge-m3

# Relative storage path for ChromaDB
CHROMA_PATH=resource/chroma_db
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

### Multi-Agent Application

This project by default has only one agent: OA-ASSISTANT, mainly for demonstration purposes. You can use langGraph to create and orchestrate multiple agents, each with its own knowledge base and behavior logic.
For details, please refer to the directory: backend/app/ai/agent







