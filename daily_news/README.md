# 📰 每日财经科技热点速递

每天自动抓取金融与科技领域的热点新闻，整理为适合**微信公众号**发布的推文格式。

## 功能特性

- ✅ 每日自动运行（北京时间 08:00）
- ✅ 覆盖 **金融** 与 **科技** 两大领域
- ✅ 自动去重、筛选 24 小时内的最新内容
- ✅ 输出标准 Markdown，适合直接复制到微信公众号编辑器
- ✅ 通过 GitHub Actions 自动提交到 `daily_news/output/` 目录

## 新闻来源

| 来源 | 分类 |
|------|------|
| 36氪 | 金融 & 科技 |
| 虎嗅网 | 金融 & 科技 |
| IT之家 | 科技 |
| 少数派 | 科技 |

## 文件结构

```
daily_news/
├── main.py           # 入口脚本
├── fetch_news.py     # 抓取 RSS 热点新闻
├── formatter.py      # 格式化为公众号推文 (Markdown)
├── sources.py        # 新闻源配置
├── requirements.txt  # Python 依赖
└── output/           # 每日生成的 Markdown 文件（按日期命名）
    └── YYYY-MM-DD.md
```

## 本地运行

```bash
# 安装依赖
pip install -r daily_news/requirements.txt

# 生成今日热点并写入 output/ 目录
python daily_news/main.py

# 仅输出到终端
python daily_news/main.py --stdout
```

## 公众号排版说明

生成的 Markdown 文件可直接导入支持 Markdown 的公众号排版工具（如 **Mdnice**、**墨滴**），
一键转换为精美的微信图文格式。
