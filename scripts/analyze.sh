#!/bin/bash
# TrendRadar MCP Skill - 分析助手脚本

set -e

cd "$(dirname "$0")/../.."

# 检查 MCP Server 是否运行
check_server() {
    if ! mcporter list trendradar &>/dev/null; then
        echo "❌ MCP Server 未注册，请先执行：mcporter config add trendradar ..."
        exit 1
    fi
}

# 解析日期范围
resolve_date() {
    local expression="$1"
    mcporter call trendradar.resolve_date_range "expression:$expression" | jq -r '.date_range'
}

# 获取最新新闻
get_latest() {
    local limit="${2:-30}"
    mcporter call trendradar.get_latest_news "limit:$limit" include_url:true
}

# 搜索新闻
search_news() {
    local query="$1"
    local platforms="${2:-all}"
    local top_n="${3:-50}"
    
    if [ "$platforms" = "all" ]; then
        mcporter call trendradar.search_news "query:$query" "top_n:$top_n" include_url:true
    else
        mcporter call trendradar.search_news "query:$query" "platforms:[\"$platforms\"]" "top_n:$top_n" include_url:true
    fi
}

# 情感分析
analyze_sentiment() {
    local topic="$1"
    local date_range="${2:-$(resolve_date '最近 7 天')}"
    
    mcporter call trendradar.analyze_sentiment "topic:$topic" "date_range:$date_range"
}

# 周期对比
compare_periods() {
    local period_a="${1:-最近 7 天}"
    local period_b="${2:-前 7 天}"
    
    mcporter call trendradar.compare_periods "period_a:$period_a" "period_b:$period_b"
}

# 批量阅读文章
read_articles() {
    local urls="$@"
    mcporter call trendradar.read_articles_batch "urls:[$urls]"
}

# 主菜单
show_menu() {
    echo "=========================================="
    echo "   TrendRadar MCP Skill - 分析助手"
    echo "=========================================="
    echo "1. 获取最新热点新闻"
    echo "2. 搜索特定话题"
    echo "3. AI 情感分析（最近 7 天）"
    echo "4. 周期趋势对比"
    echo "5. 自定义日期范围"
    echo "6. 查看服务器状态"
    echo "0. 退出"
    echo "=========================================="
}

# 主程序
main() {
    check_server
    
    case "$1" in
        "date")
            resolve_date "${2:-本周}"
            ;;
        "latest")
            get_latest "${2:-30}"
            ;;
        "search")
            search_news "${2:-AI}" "${3:-all}" "${4:-50}"
            ;;
        "sentiment")
            analyze_sentiment "${2:-AI}" "${3:-$(resolve_date '最近 7 天')}"
            ;;
        "compare")
            compare_periods "${2:-最近 7 天}" "${3:-前 7 天}"
            ;;
        "status")
            mcporter call trendradar.system action:"status"
            ;;
        *)
            show_menu
            echo ""
            read -p "请选择操作 [0-6]: " choice
            
            case $choice in
                1) get_latest ;;
                2) read -p "搜索关键词： " query; search_news "$query" ;;
                3) analyze_sentiment "AI" ;;
                4) compare_periods ;;
                5) read -p "日期表达式（如'本周'、'最近 7 天'）: " expr; resolve_date "$expr" ;;
                6) status ;;
                *) echo "退出"; exit 0 ;;
            esac
            ;;
    esac
}

main "$@"
