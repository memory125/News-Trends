# TrendRadar AI 配置指南 - 本地 LLM

## 🎯 当前状态

**系统检查：**
```bash
❌ Ollama: 未安装
❌ vLLM: 未安装  
❌ LM Studio Server: 未运行
✅ DeepSeek API: 可配置（推荐）
```

---

## 📋 方案选择

### 方案 A: DeepSeek API（推荐，快速启动）

**优点：**
- ✅ 无需本地部署
- ✅ 免费额度充足
- ✅ 响应速度快
- ✅ 质量稳定

**步骤：**
1. **注册账号**: https://platform.deepseek.com/
2. **获取 API Key**: Dashboard → API Keys → Create New Key
3. **设置环境变量**:
   ```bash
   export AI_API_KEY="sk-xxxxxxxxxxxxxxxx"
   ```
4. **测试连接**:
   ```bash
   cd ~/.openclaw/workspace/skills/trendradar-mcp && \
   python3 -c "import os; print('API Key:', os.getenv('AI_API_KEY')[:10] + '...')"
   ```

**成本估算：**
- 默认配置（50 条新闻/次）：约 ¥0.002/次
- GitHub Action 每日推送 20 次：约 ¥0.04/天
- Docker 部署每半小时推送：约 ¥0.10/天

---

### 方案 B: Ollama（完全本地，免费）

**优点：**
- ✅ 完全离线运行
- ✅ 数据隐私安全
- ✅ 零成本

**步骤：**

#### 1️⃣ 安装 Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
winget install Ollama.Ollama
```

#### 2️⃣ 拉取模型
```bash
# 推荐模型（中文能力强）：
ollama pull qwen2.5:7b      # 7B，速度快，中文优秀
ollama pull llama3.2:3b     # 3B，超轻量
ollama pull deepseek-r1:1.5b # 1.5B，推理能力强

# 如果需要更强能力：
ollama pull qwen2.5:14b     # 14B，平衡性能
ollama pull llama3.1:8b     # 8B，通用性强
```

#### 3️⃣ 启动服务（Ollama 自动运行）
```bash
# Ollama 默认在 http://localhost:11434 运行
ollama serve
```

#### 4️⃣ 配置 TrendRadar
编辑 `config/config.yaml`：
```yaml
ai:
  model: "ollama/qwen2.5:7b"  # 替换为你拉取的模型名
  
  api_key: ""                 # Ollama 不需要 API Key
  
  api_base: "http://localhost:11434"  # Ollama 服务地址
```

#### 5️⃣ 测试连接
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "你好，请自我介绍"
}'
```

---

### 方案 C: vLLM（高性能生产环境）

**适用场景：**
- 需要高并发推理
- 多用户同时使用
- GPU 资源充足

**步骤：**
```bash
# 安装 vLLM
pip install vllm

# 启动服务
vllm serve qwen2.5:7b --port 8000

# 配置 TrendRadar
api_base: "http://localhost:8000/v1"
model: "qwen2.5:7b"
```

---

## 🔧 快速切换方案

### 切换到 DeepSeek API
```bash
export AI_API_KEY="sk-xxxxxxxx"
cd ~/.openclaw/workspace/skills/trendradar-mcp && \
PYTHONPATH=$(pwd) python3 -m mcp_server.server --transport stdio &
```

### 切换到 Ollama
1. 编辑 `config/config.yaml`，修改 ai 段：
   ```yaml
   model: "ollama/qwen2.5:7b"
   api_key: ""
   api_base: "http://localhost:11434"
   ```
2. 重启 MCP Server

---

## 📊 模型推荐对比

| 模型 | 类型 | 显存需求 | 速度 | 中文能力 | 推荐场景 |
|------|------|---------|------|---------|---------|
| **qwen2.5:7b** | Ollama | ~6GB | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 本地首选 |
| **deepseek-r1:1.5b** | Ollama | ~3GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 轻量推理 |
| **llama3.2:3b** | Ollama | ~4GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | 通用任务 |
| **DeepSeek API** | Cloud | - | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 快速启动 |

---

## 🎯 推荐配置（新手）

**立即开始：**
1. 使用 DeepSeek API（免费额度足够测试）
2. 后续再考虑部署本地模型

**长期方案：**
- 有 GPU：Ollama + qwen2.5:7b
- 无 GPU：DeepSeek API

---

## 📝 下一步

选择方案后，运行以下命令验证：

```bash
# 测试 MCP Server AI 功能
cd ~/.openclaw/workspace/skills/trendradar-mcp && \
mcporter call trendradar.get_system_status | jq '.'
```

需要我帮你执行哪个方案的配置？
