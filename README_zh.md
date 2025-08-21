<h1 align="center"> AI-CHATKIT </h1>
<p align="center">
  <a href="./README.md"  target="_Self">English</a> |
  <strong style="background-color: green;">中文</strong>

</p>
ai-chatkit 是一个AI Agent全栈聊天工具，基于langGraph, fastApi, nextjs, chroma等组件搭建

这个工程可以做为一个模板，帮助你使用langGraph框架快速搭建相关的AI智能体聊天应用，并且支持RAG来增强智能体的知识库问答能力。

<img src="./pictures/chat_img.png" width="700"/>  

多智能体聊天:

<img src="./pictures/chat_multi_agent_img.png" width="700"/>

## 特性

1、基于langGraph框架搭建的智能体聊天应用，支持自定义智能体的行为逻辑编排。

2、支持自定义智能体的知识库问答能力，基于ChromaDB来存储和查询知识库。

3、支持自定义智能体的工具调用

4、Python后端接口API，基于FastAPI来实现，支持全异步调用。

5、支持自定义智能体的前端应用，基于NextJS来实现。

6、支持聊天Streaming流输出，前端支持SSE流输出。

7、支持自定义多个智能体

8、支持多智能体协作

9、聊天历史记录保存在本地浏览器缓存中


## 结构
- `backend` : 后端服务代码
- `frontend`: 前端服务代码

## 快速开始
### 后端服务

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

# openai
OPENAI_API_KEY
DEFAULT_MODEL=gpt-4o-mini

# 通义千问API,因为deepseek的api响应比较慢，如果用不了openai的api，建议使用阿里百炼的api
#DASHSCOPE_API_KEY=
#DEFAULT_MODEL=qwen-plus

# deepseek api
#DEEPSEEK_API_KEY=
#DEFAULT_MODEL=deepseek-chat

# 使用bge-m3为embedding模型，支持中英双文,需要本地通过ollama部署bge-me模型
EMBEDDING_MODEL=bge-m3

#chromadb的相对存储路径
CHROMA_PATH=resource/chroma_db
```
启动后端服务：

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
本项目你可以使用langGraph扩展创建并编排多个智能体，每个智能体可以都有自己行为逻辑，智能体的编排逻辑可以写在backend/app/ai/agent目录。
在前端你可以切换不同的智能体进行对话

本项目自带以下智能体：

1、OA-ASSISTANT：主要用于演示OA助手智能体，支持员工信息查询和员工手册知识库检索
具体可以参考：backend/app/ai/agent/oa_assistant.py  

2、MULTI_AGENT：主要用于演示多智能体协作智能体，支持多个智能体之间的协作，multi_agent包含三个智能体：
    1）math_agent ：数学智能体, 主要用于处理数学计算
    2）code_agent ：代码智能体，主要用于处理代码生成
    3）general_agent  ：通用智能体，主要用于处理通用问题
  三个智能体通过supervisor进行协作管理

具体可以参考：backend/app/ai/agent/multi_agent.py




