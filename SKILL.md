# TrendRadar MCP Skill

## 技能定位
新闻热点聚合与 AI 分析工具，通过 MCP (Model Context Protocol) 集成到 OpenClaw。提供实时新闻抓取、情感分析、趋势对比等功能。

## 触发条件
当用户需要：
- 搜索特定话题的新闻（如"AI 最新进展"）
- 获取今日/本周热点
- 分析某个品牌/产品的舆情
- 对比不同时间段的数据趋势
- 批量阅读文章并提取核心内容

## MCP Server 状态
- **运行中**: ✅ PID: 21583
- **配置路径**: `~/.mcporter/mcporter.json`
- **传输模式**: stdio (FastMCP 2.0)
- **服务器名称**: trendradar-news

## 可用工具列表

### 1. resolve_date_range(expression: string) → object
**自然语言日期解析** - 推荐优先调用

将"本周"、"最近 7 天"等转换为精确的 JSON 日期范围。

**支持表达式：**
- 单日：`今天`, `昨天`, `today`, `yesterday`
- 周：`本周`, `上周`, `this week`, `last week`
- 月：`本月`, `上月`, `this month`, `last month`
- 动态：`最近 7 天`, `last 30 days`, `最近 N 天`

**示例调用：**
```bash
mcporter call trendradar.resolve_date_range expression:"本周"
# 返回：{"date_range": {"start": "2026-03-24", "end": "2026-03-30"}, ...}
```

### 2. get_latest_news(platforms?: string[], limit?: number, include_url?: boolean) → object[]
**获取最新新闻** - 快速了解当前热点

**参数：**
- `platforms`: 平台 ID 列表，如 `["zhihu", "weibo"]`，不指定则使用所有平台
- `limit`: 返回条数限制，默认 50，最大 1000
- `include_url`: 是否包含 URL 链接，默认 False（节省 token）

**示例调用：**
```bash
mcporter call trendradar.get_latest_news limit:20 include_url:true
```

### 3. search_news(query: string, platforms?: string[], date_range?: object, top_n?: number) → object[]
**关键词搜索新闻**

**参数：**
- `query`: 搜索关键词（如 "AI", "特斯拉"）
- `platforms`: 平台过滤，可选
- `date_range`: 日期范围对象 `{start: "2026-03-01", end: "2026-03-30"}`
- `top_n`: 返回数量限制

**示例调用：**
```bash
mcporter call trendradar.search_news query:"AI 商业化" platforms:["zhihu","weibo"] top_n:50
```

### 4. analyze_sentiment(topic: string, date_range?: object) → object
**情感分析** - AI 话题情感倾向分析

**参数：**
- `topic`: 分析主题（如 "AI", "大模型"）
- `date_range`: 可选日期范围，建议先用 `resolve_date_range` 获取

**示例调用：**
```bash
mcporter call trendradar.resolve_date_range expression:"最近 7 天" | jq '.date_range'
# 然后：
mcporter call trendradar.analyze_sentiment topic:"AI" date_range:'{"start":"2026-03-24","end":"2026-03-30"}'
```

### 5. compare_periods(period_a: string, period_b: string) → object
**周期对比** - 趋势对比分析

**参数：**
- `period_a`: 第一个时间段（如 "最近 7 天"）
- `period_b`: 第二个时间段（如 "前 7 天"）

**示例调用：**
```bash
mcporter call trendradar.compare_periods period_a:"最近 7 天" period_b:"前 7 天"
```

### 6. read_articles_batch(urls: string[]) → object[]
**批量文章阅读** - 提取核心内容

**参数：**
- `urls`: 文章 URL 列表

**示例调用：**
```bash
mcporter call trendradar.read_articles_batch urls:['https://example.com/article1','https://example.com/article2']
```

### 7. config_mgmt(action: string, key?: string, value?: any) → object
**配置管理** - 管理 TrendRadar 配置

**支持操作：**
- `action: "list"` - 列出所有配置
- `action: "get", key: "xxx"` - 获取单个配置
- `action: "set", key: "xxx", value: "yyy"` - 设置配置
- `action: "reset"` - 重置为默认值

### 8. analytics(metric: string, date_range?: object) → object
**数据分析** - 深度分析指标

**支持指标：**
- `hot_topics` - 热门话题排行
- `platform_distribution` - 平台分布
- `sentiment_trend` - 情感趋势
- `growth_rate` - 增长率

### 9. system(action: string) → object
**系统管理** - MCP Server 状态检查

**支持操作：**
- `action: "status"` - 服务器状态
- `action: "health"` - 健康检查
- `action: "stats"` - 统计数据

## 使用流程示例

### 场景：分析 AI 本周热点

```bash
# Step 1: 解析日期范围
mcporter call trendradar.resolve_date_range expression:"本周"

# Step 2: 获取最新新闻
mcporter call trendradar.get_latest_news limit:30 include_url:true

# Step 3: 搜索 AI 相关话题
mcporter call trendradar.search_news query:"AI" date_range:'{"start":"2026-03-24","end":"2026-03-30"}' top_n:50

# Step 4: 情感分析
mcporter call trendradar.analyze_sentiment topic:"AI" date_range:'{"start":"2026-03-24","end":"2026-03-30"}'

# Step 5: 趋势对比
mcporter call trendradar.compare_periods period_a:"本周" period_b:"上周"
```

## 数据源平台
- **知乎** (zhihu) - 深度讨论
- **微博** (weibo) - 实时热点
- **微信公众号** (wechat) - 专业文章
- **36Kr** (36kr) - 科技新闻
- **虎嗅** (huxiu) - 商业分析
- **钛媒体** (tmtpost) - 产业观察

## 注意事项
1. **日期解析优先**：使用 `resolve_date_range` 确保时间范围一致性
2. **平台选择**：根据需求选择合适的平台组合
3. **数据量控制**：默认返回 50 条，超过 1000 会被截断
4. **URL 包含**：默认不包含 URL 以节省 token，需要时显式设置 `include_url:true`

## 维护信息
- **版本**: v6.6.0
- **作者**: sansan0
- **仓库**: https://github.com/sansan0/TrendRadar
- **集成时间**: 2026-03-30 14:45 GMT+8
- **Skill 封装**: OpenClaw MCP Integration

## 故障排查
```bash
# 检查服务器状态
mcporter call trendradar.system action:"status"

# 重启服务（如果停止）
cd ~/.openclaw/workspace/skills/trendradar-mcp && \
PYTHONPATH=$(pwd) python3 -m mcp_server.server --transport stdio &

# 查看日志
tail -f /tmp/trendradar-mcp.log
```
