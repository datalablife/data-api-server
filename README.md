

# 1. 项目系统设计

data-analysis-api/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # GitHub Actions CI/CD
│       └── deploy.yml                # 部署工作流
├── api/                              # API应用主目录
│   ├── __init__.py
│   ├── main.py                       # FastAPI应用入口
│   ├── routers/                      # API路由模块
│   │   ├── __init__.py
│   │   ├── analysis.py               # 数据分析API路由
│   │   └── health.py                 # 健康检查路由
│   ├── services/                     # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── instruction_parser.py     # 指令解析服务
│   │   ├── task_scheduler.py         # 任务调度服务
│   │   └── matlab_engine.py          # Matlab引擎接口
│   ├── models/                       # 数据模型
│   │   ├── __init__.py
│   │   ├── request_models.py         # 请求模型
│   │   └── response_models.py        # 响应模型
│   ├── utils/                        # 工具函数
│   │   ├── __init__.py
│   │   ├── logger.py                 # 日志配置
│   │   └── config.py                 # 配置管理
│   └── middleware/                   # 中间件
│       ├── __init__.py
│       ├── auth.py                   # 认证中间件
│       └── cors.py                   # CORS中间件
├── matlab_functions/                 # Matlab函数目录
│   ├── correlation_analysis.m        # 相关性分析函数
│   └── visualization.m               # 可视化函数
├── tests/                           # 测试目录
│   ├── __init__.py
│   ├── test_api.py                  # API测试
│   └── test_services.py             # 服务测试
├── docker/                          # Docker相关文件
│   ├── Dockerfile                   # 主应用Docker文件
│   ├── Dockerfile.matlab            # Matlab环境Docker文件
│   └── docker-compose.yml           # 本地开发环境
├── docs/                            # 文档目录
│   ├── README.md                    # 项目说明
│   ├── API.md                       # API文档
│   └── DEPLOYMENT.md                # 部署文档
├── scripts/                         # 脚本目录
│   ├── setup.sh                     # 环境设置脚本
│   └── deploy.sh                    # 部署脚本
├── .env.example                     # 环境变量示例
├── .env                             # 环境变量（不提交到git）
├── .gitignore                       # Git忽略文件
├── .dockerignore                    # Docker忽略文件
├── requirements.txt                 # Python依赖
├── requirements-dev.txt             # 开发依赖
├── pyproject.toml                   # 项目配置（Poetry）
├── Dockerfile                       # 生产环境Dockerfile
├── vercel.json                      # Vercel配置文件
├── README.md                        # 项目主文档
└── LICENSE                          # 开源协议

# 2. 技术栈配置

Python后端框架
主框架: FastAPI（异步支持，自动API文档生成）
ASGI服务器: Uvicorn
数据验证: Pydantic
异步任务: Celery + Redis
数据库ORM: SQLAlchemy + Alembic
HTTP客户端: httpx
开发工具
包管理: Poetry（推荐）或 pip + virtualenv
代码格式化: Black + isort
代码检查: Flake8 + mypy
测试框架: pytest + pytest-asyncio
API测试: httpx + pytest

# 3. Docker容器化策略

多阶段构建Dockerfile

```
# 基础镜像选择考虑
FROM python:3.11-slim as base
# 或者使用 python:3.11-alpine（更小但可能有兼容性问题）

# 开发阶段
FROM base as development
# 安装开发依赖

# 生产阶段  
FROM base as production
# 只安装生产依赖

```

Docker Compose配置

- 应用服务: Python FastAPI应用
- 数据库服务: PostgreSQL
- 缓存服务: Redis
- 队列监控: Flower（Celery监控）

# 4. Vercel配置要求

vercel.json配置要点
- 构建设置: 指定Python运行时
- 路由配置: API路由映射
- 环境变量: 生产环境变量配置
- 函数配置: Serverless函数配置

Vercel适配考虑
- 无服务器函数: 将API端点适配为Vercel Functions
- 冷启动优化: 减少依赖包大小，优化启动时间
- 静态文件: 分离静态资源到CDN
- 数据库连接: 使用连接池，处理Serverless环境的连接限制

# 5. GitHub版本管理策略
分支策略
- main: 生产环境分支
- develop: 开发环境分支
- feature/*: 功能开发分支
- hotfix/*: 紧急修复分支

GitHub Actions工作流
- CI流程: 代码检查、测试、构建
- CD流程: 自动部署到Vercel
- Docker构建: 自动构建和推送Docker镜像
- 安全扫描: 依赖漏洞扫描

代码质量控制
- Pre-commit hooks: 提交前代码检查
- PR模板: 标准化Pull Request
- Issue模板: 标准化问题报告
- 代码审查: 必须通过代码审查才能合并

# 6. 环境配置管理

配置层级
- .env.local: 本地开发配置
- .env.development: 开发环境配置
- .env.staging: 测试环境配置
- .env.production: 生产环境配置

敏感信息管理
- GitHub Secrets: 存储API密钥、数据库连接等
- Vercel环境变量: 生产环境配置
- Docker Secrets: 容器运行时敏感信息

7. 开发工作流程
初始化步骤
- 创建GitHub仓库
- 本地克隆项目
- 设置Python虚拟环境
- 安装依赖包
- 配置环境变量
- 运行本地开发服务器
- 设置Docker环境
- 配置Vercel项目

日常开发