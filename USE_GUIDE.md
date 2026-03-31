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

#### 4. 多渠道配置

```yaml
notification:
  channels:
    telegram:
      enabled: true
      bot_token: "YOUR_TOKEN"
      chat_id: "YOUR_CHAT_ID"
      
    dingtalk:
      enabled: true
      webhook_url: "https://oapi.dingtalk.com/robot/send?access_token=..."
      
    email:
      enabled: false  # 默认关闭，需要时启用
      smtp_server: "smtp.qq.com"
      smtp_port: 465
      from_email: "your@qq.com"
      password: "授权码"
      to_emails: ["you@example.com"]
```

**多账号配置（支持分号分隔）：**

```yaml
telegram:
  bot_token: "TOKEN1;TOKEN2"
  chat_id: "CHAT_ID_1;CHAT_ID_2"
```

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
