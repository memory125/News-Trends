# TrendRadar MCP Server 使用指南

## 📖 快速开始（5 分钟上手）

### 第一步：安装依赖

```bash
cd /home/wing/.openclaw/workspace/skills/trendradar-mcp
pip install -r requirements.txt
```

### 第二步：配置基本信息

编辑 `config/config.yaml`，至少需要配置以下两项：

```yaml
# 1. 通知渠道（选填）
notification:
  channels:
    telegram:
      enabled: true
      bot_token: "YOUR_BOT_TOKEN"
      chat_id: "YOUR_CHAT_ID"

# 2. AI 分析（可选，但推荐）
ai:
  api_key: "YOUR_API_KEY"
  model: "deepseek/deepseek-chat"
```

### 第三步：运行 MCP Server

```bash
python mcp_server/server.py
```

## 🎯 核心功能使用

### 1. 查询热点新闻

**工具名称：** `search_news`

**使用示例：**

```python
# 搜索今日热点
result = await search_news(
    query="人工智能",
    date_range="today"
)

# 跨平台搜索
result = await search_news(
    query="新能源汽车",
    platforms=["baidu", "weibo", "zhihu"],
    include_rss=True
)
```

**返回格式：**
```json
{
    "success": true,
    "summary": "找到 15 条相关新闻",
    "data": [
        {
            "title": "AI 大模型突破",
            "platform": "baidu",
            "rank": 3,
            "url": "...",
            "timestamp": "2026-03-31T09:00:00"
        }
    ],
    "error": null
}
```

### 2. 分析话题趋势

**工具名称：** `get_trending_topics`

**使用示例：**

```python
# 获取今日热门话题
result = await get_trending_topics(
    date="today",
    limit=10,
    auto_extract=True
)

# 自定义正则匹配
result = await get_trending_topics(
    pattern=r"/\bai\b/",
    display_name="AI 相关"
)
```

### 3. 读取新闻文章

**工具名称：** `read_article` / `read_articles_batch`

**使用示例：**

```python
# 单篇文章（Jina AI Reader）
result = await read_article(
    url="https://example.com/article/123"
)

# 批量读取（最多 5 篇，自动限速）
result = await read_articles_batch(
    urls=[
        "https://example.com/1",
        "https://example.com/2",
        "https://example.com/3"
    ]
)
```

### 4. 跨平台聚合对比

**工具名称：** `aggregate_news` / `compare_periods`

**使用示例：**

```python
# 聚合去重（跨平台）
result = await aggregate_news(
    query="华为",
    date_range="today"
)

# 时期对比分析
result = await compare_periods(
    query="芯片",
    period1="2026-03-24",
    period2="2026-03-31"
)
```

## ⚙️ 配置详解

### 配置文件结构

```
config/
├── config.yaml          # 主配置文件
├── timeline.yaml        # 调度系统配置（v6.0.0+）
├── frequency_words.txt  # 关键词过滤文件
└── ai/
    ├── ai_interests.txt      # AI 兴趣描述（v6.5.0+）
    └── ai_analysis_prompt.txt # AI 分析提示词
```

### 核心配置项说明

#### 1. 推送模式（config.yaml）

```yaml
app:
  mode: "incremental"  # daily | current | incremental
```

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| **daily** | 企业管理者/普通用户 | 每日汇总，包含历史内容 |
| **current** | 自媒体人/创作者 | 当前榜单，持续在榜的每次都出现 |
| **incremental** | 投资者/交易员 | 仅新增内容，零重复 |

#### 2. 调度系统（timeline.yaml）

```yaml
# 预设模板：always_on / morning_evening / office_hours / night_owl / custom
preset: "morning_evening"

# 自定义时间段示例
periods:
  - name: "morning"
    time: "08:00-10:00"
    platforms: ["baidu", "weibo"]
    filter_method: "keyword"
    
  - name: "evening"
    time: "20:00-22:00"
    platforms: ["all"]
    filter_method: "ai"
```

#### 3. AI 筛选（v6.5.0+）

**启用方式：**

```yaml
# config.yaml
filter:
  method: "ai"  # keyword | ai
  
ai_filter:
  min_score: 6  # 推送最低分数阈值（1-10）
```

**AI 兴趣描述文件（config/ai/ai_interests.txt）：**

```txt
# 用自然语言描述你的关注方向
我想看 AI 大模型相关的新闻，特别是国内科技公司的进展
关注新能源汽车和智能驾驶技术的发展
对芯片半导体行业的动态感兴趣
```

**工作原理：**
1. AI 先从兴趣描述提取结构化标签（如：AI、大模型、科技公司）
2. 对每条新闻按标签批量分类打分
3. 分数低于阈值的新闻不推送
4. AI 筛选失败时自动回退到关键词匹配

#### 4. AI 配置 - 云端 vs 本地模型

TrendRadar 支持两种 AI 分析模式：**云端 API**（如 DeepSeek、OpenAI）和 **本地部署**（如 Ollama、LM Studio）。根据你的网络环境、隐私需求和硬件条件选择。

---

### 🌐 方案一：云端 API（推荐新手）

**适用场景：**
- ✅ 没有高性能 GPU
- ✅ 希望快速上手，零配置
- ✅ 愿意付费使用高质量模型

**支持的服务商：**

| 服务商 | 优势 | 价格参考 | Model ID 格式 |
|-------|------|---------|--------------|
| **DeepSeek** | 性价比高，中文理解好 | ¥1-2/百万 token | `deepseek/deepseek-chat` |
| **OpenAI** | GPT-4o 系列，综合能力最强 | $3-15/百万 token | `openai/gpt-4o` |
| **Google Gemini** | 免费额度高，长上下文 | 免费 tier 可用 | `gemini/gemini-1.5-flash` |
| **Anthropic Claude** | 推理能力强，适合复杂分析 | $3-7.5/百万 token | `anthropic/claude-3-haiku` |

**配置示例：**

```yaml
# config.yaml
ai:
  enabled: true
  provider: "deepseek"
  api_key: "sk-your-api-key-here"
  model: "deepseek/deepseek-chat"
  base_url: null  # 云端 API 不需要设置
```

**环境变量方式（推荐）：**

```bash
# GitHub Secrets / .env
AI_API_KEY=sk-your-api-key-here
AI_PROVIDER=deepseek
AI_MODEL=deepseek/deepseek-chat
```

---

### 🖥️ 方案二：本地部署（隐私优先/免费）

**适用场景：**
- ✅ 有高性能 GPU（建议≥8GB VRAM）
- ✅ 注重数据隐私，不希望上传到云端
- ✅ 希望零成本使用 AI 功能
- ✅ 愿意花时间配置环境

#### **2.1 Ollama（推荐，最简单）**

**特点：**
- 🚀 一键安装，开箱即用
- 📦 内置模型管理工具
- 🔧 自动处理 API 格式兼容
- 💰 完全免费

**安装步骤：**

```bash
# macOS (Homebrew)
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 下载官网安装包：https://ollama.com/download
```

**拉取模型示例：**

```bash
# Qwen2.5（中文理解优秀，推荐）
ollama pull qwen2.5:7b

# Llama3（英文能力强）
ollama pull llama3

# Mistral（轻量级，速度快）
ollama pull mistral

# 查看已安装模型
ollama list

# 启动服务（默认端口 11434）
ollama serve
```

**TrendRadar 配置：**

```yaml
# config.yaml
ai:
  enabled: true
  provider: "ollama"
  api_key: ""  # Ollama 不需要 API Key，留空即可
  model: "qwen2.5:7b"  # 替换为你拉取的模型名称
  base_url: "http://127.0.0.1:11434/v1"  # Ollama 的兼容 API 地址
```

**环境变量方式：**

```bash
AI_PROVIDER=ollama
AI_MODEL=qwen2.5:7b
AI_API_BASE=http://127.0.0.1:11434/v1
# AI_API_KEY 留空或不设置
```

#### **2.2 LM Studio（图形界面，适合调试）**

**特点：**
- 🖱️ 可视化模型管理界面
- 🔍 内置模型搜索和下载
- 🧪 提供本地 API Server
- 💻 跨平台支持

**安装步骤：**

1. **下载安装：** https://lmstudio.ai/
2. **搜索并下载模型：**
   - 在 LM Studio 中搜索 `qwen2.5`、`llama3` 等
   - 选择适合你 GPU 显存的版本（7B-14B 推荐）
3. **启动本地 API Server：**
   - 进入左侧"🔌 Local Server"标签页
   - 选择已下载的模型
   - 点击"Start Server"（默认端口 1234）

**TrendRadar 配置：**

```yaml
# config.yaml
ai:
  enabled: true
  provider: "ollama"  # LM Studio 兼容 OpenAI API，用 ollama provider
  api_key: "sk-"  # LM Studio 接受任意虚拟 key
  model: "qwen2.5:7b"  # 替换为你下载的模型名称
  base_url: "http://192.168.61.1:1234/v1"  # LM Studio 的 API 地址（注意 IP）
```

**环境变量方式：**

```bash
# 假设你的电脑 IP 是 192.168.61.1
AI_PROVIDER=ollama
AI_MODEL=qwen2.5:7b
AI_API_KEY=sk-
AI_API_BASE=http://192.168.61.1:1234/v1
```

> 💡 **注意：** LM Studio 的 API 地址中的 IP 需要替换为你实际电脑的局域网 IP，可以通过 `ipconfig`（Windows）或 `ifconfig`（macOS/Linux）查看。

#### **2.3 vLLM（高性能推理）**

**适用场景：**
- ✅ 多用户并发访问
- ✅ 需要高吞吐量
- ✅ GPU 显存≥16GB

**安装与启动：**

```bash
# 安装 vLLM
pip install vllm

# 启动服务
python -m vllm.entrypoints.api_server \
  --model qwen2.5:7b \
  --port 8000 \
  --host 0.0.0.0
```

**TrendRadar 配置：**

```yaml
ai:
  enabled: true
  provider: "ollama"  # vLLM 兼容 OpenAI API
  api_key: "sk-"
  model: "qwen2.5:7b"
  base_url: "http://127.0.0.1:8000/v1"
```

#### **本地模型配置对比表**

| 方案 | 安装难度 | GPU 要求 | 速度 | 推荐场景 |
|------|---------|---------|------|---------|
| **Ollama** | ⭐ 简单 | ≥4GB VRAM | 快 | 个人使用，首选推荐 |
| **LM Studio** | ⭐⭐ 中等 | ≥6GB VRAM | 中 | 需要图形界面调试 |
| **vLLM** | ⭐⭐⭐ 复杂 | ≥16GB VRAM | 极快 | 高并发生产环境 |

---

### 🔄 方案三：混合模式（灵活切换）

**配置多个 AI 提供商，根据需求自动选择：**

```yaml
ai:
  enabled: true
  
  # 默认使用云端 API
  provider: "deepseek"
  api_key: "sk-your-key"
  model: "deepseek/deepseek-chat"
  
  # 备用本地模型（当云端失败时自动切换）
  fallback_provider: "ollama"
  fallback_model: "qwen2.5:7b"
  fallback_base_url: "http://127.0.0.1:11434/v1"
```

**工作原理：**
1. 优先尝试云端 API（速度快，质量高）
2. 如果云端失败（网络问题/配额耗尽），自动切换到本地模型
3. 本地模型作为兜底方案，保证服务可用性

---

### ⚙️ 通用配置参数

无论使用哪种 AI 提供商，以下参数都适用：

```yaml
ai:
  enabled: true
  
  # 基础配置（必填）
  provider: "deepseek"  # ollama / deepseek / openai / gemini / anthropic
  api_key: "sk-xxx"     # 云端 API 需要，本地模型可留空或填任意值
  model: "qwen2.5:7b"   # 模型名称/ID
  
  # 高级配置（可选）
  base_url: null        # 自定义 API 地址（本地模型必填）
  temperature: 0.7      # 采样温度（0-2，越高越随机）
  max_tokens: 5000      # 最大生成 token 数
  timeout: 120          # 请求超时时间（秒）
  num_retries: 2        # 失败重试次数
  
  # AI 分析开关
  analysis_enabled: true
  translation_enabled: false  # 是否启用翻译功能
```

**参数说明：**

| 参数 | 默认值 | 说明 |
|------|-------|------|
| `temperature` | `1.0` | 控制生成随机性，越低越确定（推荐 0.7-1.0） |
| `max_tokens` | `5000` | AI 回答的最大长度，分析任务建议≥3000 |
| `timeout` | `120` | 超时时间，本地模型较慢可适当调高 |
| `num_retries` | `2` | 失败自动重试次数，提高稳定性 |

---

### 🚀 快速配置指南

#### **新手推荐路径：**

```bash
# 步骤 1：安装 Ollama
brew install ollama  # macOS
curl -fsSL https://ollama.com/install.sh | sh  # Linux

# 步骤 2：拉取模型（中文理解优秀）
ollama pull qwen2.5:7b

# 步骤 3：启动服务
ollama serve

# 步骤 4：配置 TrendRadar
# config.yaml
ai:
  enabled: true
  provider: "ollama"
  api_key: ""
  model: "qwen2.5:7b"
  base_url: "http://127.0.0.1:11434/v1"

# 步骤 5：测试连接
python -c "from trendradar.ai.client import AIClient; print(AIClient().test_connection())"
```

#### **云端快速路径：**

```bash
# 只需配置 API Key，其他自动处理
AI_API_KEY=sk-your-key-here
AI_PROVIDER=deepseek
AI_MODEL=deepseek/deepseek-chat
```

---

### 🐛 本地模型常见问题

**Q1: Ollama 服务启动失败？**

```bash
# 检查端口是否被占用
lsof -i :11434  # macOS/Linux
netstat -ano | findstr :11434  # Windows

# 查看 Ollama 日志
ollama serve --debug
```

**Q2: LM Studio API 无法连接？**

- ✅ 确认已启动"Local Server"（不是只下载模型）
- ✅ 检查 IP 地址是否正确（用 `ipconfig` 或 `ifconfig` 查看）
- ✅ 防火墙允许 LM Studio 访问网络

**Q3: 本地模型推理速度慢？**

- 降低 `max_tokens` 限制输出长度
- 使用量化版本模型（如 `qwen2.5:1.5b`、`qwen2.5:3b`）
- 关闭其他占用 GPU 的程序

**Q4: AI 分析推送不生效？**

```bash
# 检查配置是否正确
docker exec -it trendradar python manage.py config | grep ai

# 手动测试 API 连接
curl http://127.0.0.1:11434/api/chat  # Ollama
curl http://192.168.61.1:1234/v1/models  # LM Studio
```

**Q5：如何选择合适的模型？**

| GPU 显存 | 推荐模型 | 速度 | 质量 |
|---------|---------|------|------|
| **≥24GB** | qwen2.5:72b / llama3:70b | 中 | ⭐⭐⭐⭐⭐ |
| **16-24GB** | qwen2.5:32b / llama3:8b | 快 | ⭐⭐⭐⭐ |
| **8-16GB** | qwen2.5:7b / mistral:7b | 很快 | ⭐⭐⭐ |
| **4-8GB** | qwen2.5:1.5b / phi3:mini | 极快 | ⭐⭐ |

> 💡 **提示：** Qwen2.5 系列对中文支持最好，Llama3 英文能力强，Mistral 轻量级适合低配设备。

### 关键词过滤语法（frequency_words.txt）

#### 基础语法

| 符号 | 作用 | 示例 |
|------|------|------|
| **无** | 普通匹配 | `华为` |
| **+** | 必须词 | `+手机` |
| **!** | 过滤词 | `!广告` |
| **@** | 数量限制 | `@10` |

#### 高级语法（v4.7.0+）

```txt
# 正则表达式 + 显示名称
/(?<![a-z])ai(?![a-z])/ => AI 相关
人工智能

# 必须词 + 过滤词组合
华为
OPPO
+手机
!维修
!二手
@5
```

**使用技巧：**

1. **从宽到严：**
   ```txt
   # 第一步：宽泛关键词
   人工智能
   AI
   
   # 第二步：加入必须词限定
   人工智能
   AI
   +技术
   
   # 第三步：加入过滤词
   人工智能
   AI
   +技术
   !广告
   ```

2. **避免过度复杂：**
   - ❌ 不推荐：一个词组包含太多词汇
   - ✅ 推荐：拆分成多个精确的词组

## 🤖 MCP 客户端集成

### 支持的客户端

| 客户端 | 配置方式 | 文档链接 |
|--------|---------|---------|
| **Claude Desktop** | `claude_desktop_config.json` | [README-MCP-FAQ.md](./README-MCP-FAQ.md) |
| **Cherry Studio** | MCP Server 配置页面 | [README-Cherry-Studio.md](./README-Cherry-Studio.md) |
| **Cursor** | Settings → MCP | [README-MCP-FAQ.md](./README-MCP-FAQ.md) |
| **Cline** | VS Code 扩展配置 | [README-MCP-FAQ.md](./README-MCP-FAQ.md) |

### Claude Desktop 配置示例

```json
{
  "mcpServers": {
    "trendradar": {
      "command": "python",
      "args": ["/home/wing/.openclaw/workspace/skills/trendradar-mcp/mcp_server/server.py"],
      "cwd": "/home/wing/.openclaw/workspace/skills/trendradar-mcp"
    }
  }
}
```

### Cursor 配置示例

1. 打开 Settings → MCP
2. 点击 "Add new MCP server"
3. 填写：
   - **Name:** `trendradar`
   - **Type:** `command`
   - **Command:** `python /home/wing/.openclaw/workspace/skills/trendradar-mcp/mcp_server/server.py`

## 📊 常见问题解答

### Q1: AI 分析推送不生效？

**检查清单：**
- ✅ API Key 是否正确配置
- ✅ Model 名称是否支持（如 `deepseek/deepseek-chat`）
- ✅ config.yaml 中 `ai.enabled: true`
- ✅ 网络连接是否正常

**调试步骤：**
```bash
# 手动测试 AI 连接
python -c "from trendradar.ai.client import AIClient; client = AIClient(); print(client.test_connection())"
```

### Q2: 推送内容重复？

**原因分析：**
- 推送模式设置为 `daily`（会包含历史内容）
- 关键词过滤过宽，匹配到相似新闻
- RSS 新鲜度过滤未启用

**解决方案：**
1. 切换到 `incremental` 模式
2. 收紧关键词配置
3. 启用 RSS 新鲜度过滤：
   ```yaml
   rss:
     freshness_days: 7  # 只推送 7 天内的文章
   ```

### Q3: MCP Server 连接失败？

**常见原因：**
- Python 环境未激活
- 依赖包未安装完整
- 端口被占用（默认 3333）

**排查步骤：**
```bash
# 1. 检查依赖
pip list | grep -E "mcp|litellm"

# 2. 测试服务器启动
python mcp_server/server.py --test

# 3. 查看日志
tail -f logs/mcp_server.log
```

### Q4: Docker 部署数据不持久化？

**解决方案：**

使用 Volume 挂载：
```bash
docker run -d \
  --name trendradar \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/output:/app/output \
  wantcat/trendradar:latest
```

### Q5: GitHub Actions 签到提醒？

**签到流程：**
1. 访问：https://github.com/你的用户名/TrendRadar/actions
2. 选择 "Check In" workflow
3. 点击 "Run workflow"
4. 有效期重置为 7 天

**建议频率：** 每 5-6 天签到一次，避免过期

## 🔧 高级技巧

### 1. 自定义 AI 分析提示词

编辑 `config/ai_analysis_prompt.txt`：

```txt
你是一位专业的热点资讯分析师。请根据以下新闻数据进行分析：

【分析维度】
1. 核心热点态势：识别当天最重要的 3-5 个话题
2. 舆论风向争议：分析各平台的情感倾向和争议点
3. 异动与弱信号：发现新兴趋势和潜在风险
4. 研判策略建议：给出可操作的建议

【输出格式】
使用 Markdown，包含标题、列表、加粗等格式。
每个维度用独立的小节展示。
```

### 2. 跨平台对比分析

```python
# 获取同一话题在不同平台的排名
result = await search_news(
    query="华为",
    platforms=["baidu", "weibo", "zhihu"],
    date_range="today"
)

# 对比分析
for platform, news_list in result["data"].items():
    print(f"{platform}: {len(news_list)}条新闻")
```

### 3. 历史数据查询

```python
# 查询过去 7 天的数据
result = await search_news(
    query="芯片",
    date_range="last_7_days"
)

# 获取特定日期
result = await search_news(
    query="AI",
    date="2026-03-25"
)
```

### 4. 自定义推送时间窗口

```yaml
# config.yaml
push_window:
  enabled: true
  start_time: "09:00"
  end_time: "18:00"
  days_of_week: [1, 2, 3, 4, 5]  # 周一至周五
```

## 📚 相关文档

- **[README.md](./README.md)** - 项目完整介绍和快速开始
- **[README-MCP-FAQ.md](./README-MCP-FAQ.md)** - MCP 使用常见问题（中文版）
- **[README-MCP-FAQ-EN.md](./README-MCP-FAQ-EN.md)** - MCP FAQ（英文版）
- **[SETUP-LOCAL-AI.md](./SETUP-LOCAL-AI.md)** - 本地 AI 配置指南
- **[AI-TEST-REPORT.md](./AI-TEST-REPORT.md)** - AI 功能测试报告

## 🤝 社区支持

- **GitHub Issues:** [https://github.com/memory125/News-Trends/issues](https://github.com/memory125/News-Trends/issues)
- **原项目：** [https://github.com/sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)

## 📝 更新记录

本使用指南随 MCP Server 版本同步更新，建议定期查看 README.md 了解最新功能。
