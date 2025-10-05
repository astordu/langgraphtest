# LangGraph 研究助手

一个基于 LangGraph 构建的智能研究助手，使用 DeepSeek 模型和 Tavily 搜索引擎，能够自动进行网络搜索和信息收集，为用户提供全面的研究结果。

## 功能特性

- 🤖 **智能研究流程**: 基于 LangGraph 的状态图管理复杂的研究工作流
- 🔍 **网络搜索**: 集成 Tavily 搜索引擎，支持并行搜索多个查询
- 🧠 **深度思考**: 内置反思工具，确保研究质量和策略性决策
- 🌐 **中文支持**: 完全支持中文查询和回答
- ⚡ **高效执行**: 异步搜索和智能工具调用优化

## 项目架构

```
langgraphtest/
├── src/agent/           # 核心代理代码
│   ├── researcher.py    # 主要研究代理和图定义
│   ├── utils.py         # 工具函数（搜索、思考）
│   └── prompts.py       # 系统提示模板
├── test/                # 测试文件
├── langgraph.json       # LangGraph 配置
└── pyproject.toml       # 项目依赖配置
```

## 核心组件

### 1. 研究代理 (Researcher Agent)
- 使用 DeepSeek Chat 模型作为核心 LLM
- 实现状态图管理研究流程
- 支持工具调用和条件分支

### 2. 搜索工具 (Tavily Search)
- 支持多个并行搜索查询
- 可配置搜索结果数量和主题过滤
- 返回格式化的搜索结果

### 3. 思考工具 (Think Tool)
- 研究过程中的战略反思
- 评估信息完整性和下一步决策
- 防止过度搜索的智能控制

## 安装和使用

### 环境要求
- Python >= 3.13
- uv 包管理器

### 安装依赖

```bash
# 使用 uv 安装依赖
uv sync

# 或者使用 pip
pip install -e .
```

### 环境配置

创建 `.env` 文件并配置必要的 API 密钥：

```bash
# Tavily API 密钥（必需）
TAVILY_API_KEY=your_tavily_api_key_here

# DeepSeek API 密钥（如果使用）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 运行Agent

```bash
# 启动 LangGraph 服务
uv run langgraph dev

```

