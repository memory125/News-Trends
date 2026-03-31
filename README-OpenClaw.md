# TrendRadar MCP Skill - OpenClaw 集成文档

## 📦 技能封装状态

| 项目 | 状态 |
|------|------|
| **MCP Server** | ✅ 运行中 (PID: 21583) |
| **mcporter 注册** | ✅ `~/.mcporter/mcporter.json` |
| **SKILL.md** | ✅ 已创建 |
| **配置文件** | ✅ `config.json` |
| **分析脚本** | ✅ `scripts/analyze.sh` |
| **数据爬取** | ⚠️ 需要配置 AI API Key |

## 🎯 核心功能

### 1. 新闻聚合与搜索
```bash
# 获取最新热点
mcporter call trendradar.get_latest_news limit:30 include_url:true

# 关键词搜索
mcporter call trendradar.search_news query:"AI" platforms:["zhihu","weibo"] top_n:50
```

### 2. 智能日期解析（推荐优先使用）
```bash
mcporter call trendradar.resolve_date_range expression:"本周"
# 返回：{"date_range": {"start": "2026-03-30", "end": "2026-03-30"}}
```

### 3. 情感分析
```bash
mcporter call trendradar.analyze_sentiment topic:"AI" date_range:'{"start":"...","end":"..."}'
```

### 4. 周期对比
```bash
mcporter call trendradar.compare_periods period_a:"最近 7 天" period_b:"前 7 天"
```

## 📊 数据源平台

- **知乎** - 深度讨论
- **微博** - 实时热点  
- **微信公众号** - 专业文章
- **36Kr** - 科技新闻
- **虎嗅** - 商业分析
- **钛媒体** - 产业观察

## 🔧 使用流程

### 快速开始
```bash
# 1. 检查服务器状态
mcporter call trendradar.system action:"status"

# 2. 解析日期范围（推荐）
DATE_RANGE=$(mcporter call trendradar.resolve_date_range expression:"最近 7 天" | jq -r '.date_range')

# 3. 搜索 AI 新闻
mcporter call trendradar.search_news query:"AI" date_range:$DATE_RANGE top_n:50 include_url:true

# 4. 情感分析
mcporter call trendradar.analyze_sentiment topic:"AI" date_range:$DATE_RANGE
```

### 批量阅读文章
```bash
mcporter call trendradar.read_articles_batch urls:['https://example.com/1','https://example.com/2']
```

## ⚙️ 配置要求

### AI API Key（可选但推荐）
```bash
export AI_API_KEY="your-api-key"
# 或编辑 config/config.yaml 添加
```

### 数据爬取状态
当前数据尚未爬取，需要：
1. 配置 AI API Key
2. 运行 `python3 -m trendradar` 进行首次数据采集
3. MCP Server 将自动读取已爬取的数据

## 🛠️ 维护命令

```bash
# 重启 MCP Server
cd ~/.openclaw/workspace/skills/trendradar-mcp && \
PYTHONPATH=$(pwd) python3 -m mcp_server.server --transport stdio &

# 查看日志
tail -f /tmp/trendradar-mcp.log

# 运行环境体检
python3 -m trendradar --doctor

# 测试通知渠道（如果配置了）
python3 -m trendradar --test-notification
```

## 📈 下一步建议

1. **配置 AI API Key** - 启用完整情感分析功能
2. **运行首次爬取** - `python3 -m trendradar` 
3. **测试 MCP 工具** - 调用 `get_latest_news` 验证数据可用性
4. **集成到工作流** - 将 TrendRadar 与股票监控、McKinsey PPT 等任务结合

## 📝 故障排查

| 问题 | 解决方案 |
|------|---------|
| MCP Server 未启动 | `PYTHONPATH=$(pwd) python3 -m mcp_server.server --transport stdio &` |
| 数据未找到 | 运行 `python3 -m trendradar` 进行首次爬取 |
| AI API Key 缺失 | 设置环境变量或编辑 `config/config.yaml` |
| 工具调用失败 | 检查 mcporter 配置：`mcporter list --schema trendradar` |

## 📚 相关文档

- **原始项目**: https://github.com/sansan0/TrendRadar
- **MCP FAQ**: `README-MCP-FAQ.md`
- **Cherry Studio 集成**: `README-Cherry-Studio.md`
- **OpenClaw Skill 规范**: `SKILL.md`

---

**集成时间**: 2026-03-30 15:18 GMT+8  
**版本**: v6.6.0 (MCP Integration v1.0.0)  
**维护者**: OpenClaw Team
