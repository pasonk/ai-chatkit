<h1 align="center"> AI-CHATKIT </h1>
<p align="center">
  <a href="./README.md"  target="_Self">English</a> |
  <strong style="background-color: green;">中文</strong>

</p>
ai-chatkit 是一个AI Agent全栈聊天工具，基于langGraph, fastApi, nextjs, chroma等组件搭建

这个工程可以做为一个模板，帮助你使用langGraph框架快速搭建相关的AI智能体聊天应用，并且支持RAG来增强智能体的知识库问答能力。

<img src="./pictures/chat_img.png" width="700"/>  

## 特性

1、基于langGraph框架搭建的智能体聊天应用，支持自定义智能体的行为逻辑编排。
2、支持自定义智能体的知识库问答能力，基于ChromaDB来存储和查询知识库。
3、支持自定义智能体的工具调用
4、Python后端接口API，基于FastAPI来实现。
5、支持自定义智能体的前端应用，基于NextJS来实现。
6、支持聊天Streaming流输出，前端支持SSE流输出。
7、支持自定义多个智能体


## 结构
- `backend` : 后端服务代码
- `frontend`: 前端服务代码

## 快速开始
### 后端服务

```sh
# 使用uv工具来管理python依赖包
pip install uv
uv sync --frozen
# 创建python虚拟环境
source .venv/bin/activate
# ${workdir}替换为你自己的工作目录
cd ${workdir}/backend
python app/run_server.py
```

后端.env文件配置
修改.env.example文件名为.env

```properties
# 环境变量配置

# 数据库配置
#slqlite url
DATABASE_URL=sqlite+aiosqlite:///resource/database.db
#mysql  
# DATABASE_URL=mysql+aiomysql://root:root@localhost/ai-chatkit

# 应用配置
DEBUG=True
APP_NAME=AI ChatKit

# 建议使用deepseek api, 当然你也可以使用openAI
DEEPSEEK_API_KEY=
DEFAULT_MODEL=deepseek-chat

# openai
#OPENAI_API_KEY
#DEFAULT_MODEL=gpt-4o-mini




# 使用bge-m3为embedding模型，支持中英双文,需要本地通过ollama部署bge-me模型
EMBEDDING_MODEL=bge-m3

#chromadb的相对存储路径
CHROMA_PATH=resource/chroma_db
```

### RAG 部署
本工程默认访问本地的ollama部署的bge-m3，故如果要在本地访问知识库，则需要本地部署ollama，本地ollama部署bge-m3请参考：https://ollama.com/library/bge-m3


### 前端应用

```sh
# ${workdir}替换为你自己的工作目录
cd ${workdir}/frontend
# 采用pnpm管理依赖包
pnpm install
# 启动前端应用
pnpm dev
```

启动成功后则可以，访问地址：http://localhost:3000/

### 多智能体应用
本项目默认只有一个智能体：OA-ASSISTANT，主要用于演示，你可以使用langGraph创建并编排多个智能体，每个智能体都有自己的知识库和行为逻辑。
具体可以参考目录：backend/app/ai/agent


