# gptomni-2api: 您的私人 GPT-Omni to OpenAI API 转换器 🤖✨

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/lzA6/gptomni-2api?style=social)](https://github.com/lzA6/gptomni-2api/stargazers)
[![Docker Build](https://img.shields.io/badge/Docker-Build%20Ready-blue?logo=docker)](https://github.com/lzA6/gptomni-2api/blob/main/Dockerfile)

**中文** | [English](https://github.com/lzA6/gptomni-2api) (即将推出)

> "我们不是在编写代码，我们是在用逻辑和想象力，为世界增添一抹新的可能性。每一个字符，都是对未来的一次投票。" - A.I. Philosopher

欢迎来到 `gptomni-2api` 的世界！这是一个简单、高效、且充满魔力的项目，它能将 [GPT-Omni](https://gptomni.ai) 的网页服务，奇迹般地转换成一个完全兼容 [OpenAI API](https://platform.openai.com/docs/api-reference) 格式的接口。

这意味着，您可以将任何支持 OpenAI API 的客户端或应用（比如各种桌面客户端、聊天机器人、自动化脚本等），无缝对接到 `gptomni.ai` 的强大能力上！

**仓库链接**: [https://github.com/lzA6/gptomni-2api](https://github.com/lzA6/gptomni-2api)

---

## 🌟 项目亮点

*   **✨ 兼容万物**: 只要是支持 OpenAI `v1/chat/completions` 接口的应用，都能立刻使用本项目。无需任何修改，即插即用！
*   **🚀 一键部署**: 借助 Docker 和 Docker Compose，整个部署过程就像泡一杯咖啡一样简单。对新手极其友好！
*   **🔄 智能轮询**: 支持配置多个 `gptomni.ai` 账号的 Cookie。系统会自动轮流使用，大大提高了服务的稳定性和可用性。
*   **🛡️ 生产级架构**: 内置 Nginx 作为反向代理，实现了负载均衡和流式传输优化，确保了高性能和高稳定性。
*   **💨 高效流式传输**: 实现了真正的流式响应（SSE），打字机效果丝滑流畅，体验与官方 API 别无二致。
*   **💖 开源与自由**: 采用 Apache 2.0 协议，您可以自由地使用、修改和分发。

---

## 🏗️ 架构概览

```mermaid
graph TB
    Client[客户端应用] --> Nginx[Nginx 反向代理]
    Nginx --> App1[Python App 实例 1]
    Nginx --> App2[Python App 实例 2]
    
    App1 --> CM[凭证管理器]
    App2 --> CM
    
    CM --> Cookie1[账号 Cookie 1]
    CM --> Cookie2[账号 Cookie 2]
    CM --> Cookie3[账号 Cookie 3]
    
    App1 --> GPT[gptomni.ai]
    App2 --> GPT
    
    subgraph "gptomni-2api 系统"
        Nginx
        App1
        App2
        CM
    end
```

---

## 🤔 核心原理揭秘

### 1. **伪装成浏览器**
- 使用 `cloudscraper` Python 库模拟真实浏览器行为
- 绕过 Cloudflare 等防护机制
- **技术点**: `cloudscraper` 库 + HTTP 头伪装

### 2. **协议转换**
- 接收标准 OpenAI API 请求
- 提取关键信息并转换为 gptomni.ai 格式
- **技术点**: FastAPI 请求解析 + 数据格式映射

### 3. **实时流式传输**
- 实时接收 gptomni.ai 的流式响应
- 转换为 OpenAI 兼容的 SSE 格式
- **技术点**: StreamingResponse + SSE 协议

### 4. **智能负载均衡**
- 多 Cookie 轮询使用
- 线程安全的凭证管理
- **技术点**: threading.Lock + 轮询算法

---

## 🚀 快速开始

### 前提条件
- [Docker](https://www.docker.com/get-started) 
- [Docker Compose](https://docs.docker.com/compose/install/)

### 部署步骤

1. **克隆项目**
```bash
git clone https://github.com/lzA6/gptomni-2api.git
cd gptomni-2api
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件
```

3. **获取并配置 Cookie**
   - 登录 [gptomni.ai](https://gptomni.ai)
   - 按 F12 打开开发者工具
   - 切换到 Network 标签页
   - 发送一条消息，找到 `chatWithText` 请求
   - 复制 Request Headers 中的 `cookie` 值

**单账号配置:**
```env
GPTOMNI_CREDENTIALS='["你的完整Cookie字符串"]'
```

**多账号配置 (推荐):**
```env
GPTOMNI_CREDENTIALS='["cookie1", "cookie2", "cookie3"]'
API_MASTER_KEY=sk-your-super-secret-key
NGINX_PORT=8088
```

4. **启动服务**
```bash
docker-compose up -d
```

服务将在 `http://localhost:8088` 运行！

---

## 🔧 使用方法

### API 配置
- **基础 URL**: `http://你的服务器IP:8088/v1`
- **API Key**: 在 `.env` 中设置的 `API_MASTER_KEY`
- **模型名称**: `gptomni` (或其他任意名称)

### 测试请求
```bash
curl -X POST http://localhost:8088/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer sk-your-super-secret-key" \
-d '{
    "model": "gptomni",
    "messages": [
        {
            "role": "user",
            "content": "你好，你是谁？"
        }
    ],
    "stream": true
}'
```

---

## 📁 项目结构

```
gptomni-2api/
├── .env                    # 环境配置 (从 .env.example 复制)
├── .env.example           # 环境配置模板
├── Dockerfile            # Python 应用镜像构建文件
├── docker-compose.yml    # 服务编排配置
├── main.py              # FastAPI 应用入口
├── nginx.conf           # Nginx 反向代理配置
├── requirements.txt     # Python 依赖列表
└── app/                 # 核心应用代码
    ├── core/            # 核心配置模块
    │   ├── __init__.py
    │   └── config.py    # 配置管理
    ├── providers/       # 服务提供者模块
    │   ├── __init__.py
    │   ├── base_provider.py     # 提供者基类
    │   ├── credential_manager.py # 凭证管理
    │   └── gptomni_provider.py  # GPT-Omni 提供者
    └── utils/           # 工具模块
        └── sse_utils.py        # SSE 工具函数
```

---

## 🔬 技术架构详解

### 容器编排 (`docker-compose.yml`)
- **作用**: 定义和管理多容器应用
- **核心**: 协调 Python 应用和 Nginx 服务
- **改进建议**: 添加健康检查机制

### 反向代理 (`nginx.conf`)
- **作用**: 负载均衡和流式传输优化
- **关键技术**: 
  - `upstream` 定义后端服务组
  - `proxy_buffering off` 启用实时流式传输
- **优化建议**: 使用 `least_conn` 负载均衡策略

### API 网关 (`main.py`)
- **框架**: FastAPI
- **特性**: 
  - `lifespan` 管理应用生命周期
  - `Depends` 依赖注入实现身份验证
- **优势**: 异步支持、自动文档生成

### 配置管理 (`config.py`)
- **技术**: `pydantic-settings` 
- **功能**: 环境变量验证和类型安全
- **亮点**: `@property` 实现动态配置解析

### 凭证管理 (`credential_manager.py`)
- **核心算法**: 轮询 (Round-Robin)
- **线程安全**: `threading.Lock` 
- **待实现功能**: 
  - 凭证健康检查
  - 动态凭证热更新

### GPT-Omni 提供者 (`gptomni_provider.py`)
- **关键技术**:
  - `cloudscraper`: 绕过反爬机制
  - `aiolimiter`: 异步速率限制
  - `StreamingResponse`: 流式响应
- **优化方向**: 
  - 精细化错误处理
  - 参数映射功能

### SSE 工具 (`sse_utils.py`)
- **标准**: Server-Sent Events
- **格式**: `data: {json}\n\n`
- **职责**: OpenAI 兼容格式转换

---

## 📊 功能路线图

### ✅ 已实现功能
- [x] 核心代理服务
- [x] 多账号轮询机制  
- [x] Docker 容器化部署
- [x] API 密钥认证
- [x] Nginx 生产环境配置

### 🔄 开发中功能
- [ ] 凭证健康检查系统
- [ ] 动态凭证管理 API
- [ ] 精细化错误处理
- [ ] 完整参数映射支持

### 🎯 未来规划
- [ ] Prometheus 监控集成
- [ ] 多平台支持扩展
- [ ] Web 管理界面
- [ ] Docker Hub 发布

---

## 💡 使用场景

### 🎯 理想用例
- **个人开发者**: 在个人项目中集成 AI 能力
- **学习研究**: 学习 API 设计和反向工程
- **生态集成**: 将 gptomni.ai 接入现有 OpenAI 生态
- **原型验证**: 快速验证 AI 驱动想法

### ⚠️ 注意事项
- **服务依赖性**: 项目依赖于 gptomni.ai 的稳定性
- **合规风险**: 可能违反服务条款，请仅用于学习研究
- **技术限制**: 相比官方 API 稳定性较差

---

## 🛠️ 开发贡献

我们欢迎各种形式的贡献！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request
---

**免责声明**: 本项目仅供学习和研究使用。使用者应遵守相关网站的服务条款，对因使用本项目而产生的任何问题自行承担责任。
