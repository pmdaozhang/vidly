# YouTube 热搜选题抓取工具

基于 YouTube Data API v3 的视频搜索与热度分析工具，支持多关键词搜索、按播放量排序、时间范围过滤。

## 功能

- 多关键词同时搜索
- 按播放量降序排列
- 时间范围过滤（过去一周 / 一月 / 一年）
- CLI 命令行模式
- Web 可视化界面（Flask）
- 表格输出：标题、播放量、频道、发布时间、视频链接

## 环境准备

### 1. 获取 YouTube API Key

1. 访问 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. 创建项目或选择已有项目
3. 启用 **YouTube Data API v3**
4. 创建 API Key（凭据 → 创建凭据 → API 密钥）

### 2. 配置 API Key

```bash
# 方式一：.env 文件（推荐）
cp .env.example .env
# 编辑 .env，填入你的 API Key：
# YOUTUBE_API_KEY=你的密钥

# 方式二：环境变量
export YOUTUBE_API_KEY=你的密钥
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方式

### CLI 命令行模式

```bash
# 搜索单个关键词
python cli.py "Python"

# 搜索多个关键词
python cli.py "Python" "AI" "机器学习"

# 指定时间范围（过去一周）
python cli.py "Python" --time "last week"

# 指定返回数量（每关键词 20 条）
python cli.py "Python" -m 20

# 组合使用
python cli.py "AI" "LLM" --time "last month" -m 15

# 检查 API Key 是否有效
python cli.py --check-key
```

### Web 界面模式

```bash
python app.py
```

浏览器打开 `http://localhost:5000`

## 项目结构

```
├── app.py             # Flask Web 应用
├── cli.py             # CLI 命令行入口
├── youtube_api.py     # YouTube API 封装
├── config.py          # 配置管理
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量模板
├── .gitignore
├── templates/
│   └── index.html     # Web 前端页面
└── README.md
```

## 注意事项

- YouTube Data API v3 有每日配额限制（默认 10,000 单位/天），每次搜索请求约消耗 100 单位
- 建议在 Google Cloud Console 中设置 API Key 的应用限制，避免被滥用
