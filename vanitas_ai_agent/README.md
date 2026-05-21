# vanitas_ai_agent

一个完整可运行的 Python AI Agent 项目，支持：

- 接受自然语言指令
- 调用 OpenAI GPT-4 API 生成回答
- 文件操作（读写）
- 网络请求（HTTP）
- 数据保存（JSON）
- 本地交互日志记录
- CLI 命令行
- Tkinter 图形界面
- FastAPI HTTP 接口

---

## 项目结构

```text
vanitas_ai_agent/
├── __init__.py
├── main.py
├── agent.py
├── executor.py
├── utils.py
├── config.py
├── gui.py
├── api.py
├── requirements.txt
├── README.md
└── tests/
    ├── test_agent.py
    └── test_api.py
```

---

## 各文件功能说明

- `main.py`：项目入口，提供 CLI、交互模式、`--gui` 图形界面启动。
- `agent.py`：Agent 主逻辑，负责调用 OpenAI、解析动作、执行任务、记录日志。
- `executor.py`：任务执行模块，封装文件读写、HTTP 请求、JSON 数据保存。
- `utils.py`：工具函数（目录创建、JSONL 追加写入、时间戳、JSON 保存）。
- `config.py`：配置管理（OpenAI API Key、模型参数、日志与数据目录）。
- `gui.py`：Tkinter 图形界面，支持输入指令并查看回复。
- `api.py`：FastAPI 接口，支持通过 HTTP 请求调用 Agent。
- `requirements.txt`：依赖列表。
- `tests/test_agent.py`：Agent 单元测试。
- `tests/test_api.py`：API 单元测试。

---

## 安装依赖

> 需要 Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 设置 OpenAI API Key

### Linux / macOS

```bash
export OPENAI_API_KEY="你的API密钥"
```

### Windows (PowerShell)

```powershell
setx OPENAI_API_KEY "你的API密钥"
```

可选配置：

```bash
export OPENAI_MODEL="gpt-4"
export OPENAI_TEMPERATURE="0.2"
export OPENAI_MAX_TOKENS="800"
export VANITAS_DATA_DIR="./data"
export VANITAS_LOGS_DIR="./logs"
```

---

## 运行项目

### 1) 单次命令模式

```bash
python -m vanitas_ai_agent.main "请帮我写一个周报模板并保存成文件"
```

### 2) CLI 交互模式

```bash
python -m vanitas_ai_agent.main
```

输入 `exit` 或 `quit` 退出。

### 3) Tkinter 图形界面

```bash
python -m vanitas_ai_agent.main --gui
```

---

## FastAPI 接口

启动服务：

```bash
uvicorn vanitas_ai_agent.api:app --host 0.0.0.0 --port 8000 --reload
```

接口说明：

- `GET /health`：健康检查
- `POST /agent/run`：调用 Agent

请求示例：

```bash
curl -X POST http://127.0.0.1:8000/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"请生成一个会议纪要模板"}'
```

---

## 运行测试

```bash
pytest -q vanitas_ai_agent/tests
```

---

## 日志与数据

- 交互日志默认保存到：`./logs/interactions.jsonl`
- Agent 执行动作产生的数据默认保存到：`./data/`

你可以通过环境变量 `VANITAS_LOGS_DIR` 和 `VANITAS_DATA_DIR` 自定义目录。
