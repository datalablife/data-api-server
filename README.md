# Data API Server

A Python FastAPI backend server with Docker containerization and Vercel deployment support.

## =� Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python run.py
   ```
   Server will be available at: http://localhost:8000

3. **Using Docker**:
   ```bash
   docker build -t data-api .
   docker run -p 8000:8000 data-api
   ```

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /data/users` - Get users list
- `POST /data/users` - Create user
- `GET /data/stats` - Get server stats

## =� Project Structure

```
DataApiServer/
   api/
      index.py          # Vercel entry point
   app/
      main.py           # FastAPI application
      routers/
          data.py       # Data API routes
   Dockerfile            # Docker configuration
   requirements.txt      # Python dependencies
   vercel.json          # Vercel deployment config
   run.py               # Local development script
```

## =� Tech Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **Containerization**: Docker
- **Deployment**: Vercel Serverless
- **Language**: Python 3.9+

## < Deployment

### Vercel Deployment
1. Connect this GitHub repository to Vercel
2. Vercel will automatically deploy on every push to main branch

### Docker Deployment
```bash
docker build -t data-api-server .
docker run -p 8000:8000 data-api-server
```

## =� API Documentation

When running locally, visit http://localhost:8000/docs for interactive API documentation.

## =� Project Analysis

### Technical Architecture Overview

#### Design Patterns and Architecture Style
- **REST API Architecture**: Project follows RESTful API design principles
- **MVC Pattern**: Separates data models (Pydantic models), views (API responses), and controllers (route handlers)
- **Stateless Design**: API service maintains no state between requests
- **Serverless Architecture**: Configured for Vercel serverless deployment

#### Core Technology Stack
- **FastAPI (0.104.1)**: Main web framework for building the API
- **NumPy (1.24.3)**: Data processing and numerical computation
- **Matplotlib (3.7.2)**: Data visualization
- **Seaborn (0.12.2)**: Enhanced statistical data visualization
- **Pydantic (2.4.2)**: Data validation and model definition
- **Python 3.9+**: Base runtime environment

### Code Quality Assessment

#### Code Style Consistency
- Consistent Python standard naming conventions
- RESTful endpoint naming using nouns and HTTP methods
- Clear function and variable naming that express their purpose

#### Test Coverage
- Test coverage improvements planned for future versions
- Goal to reach 90%+ unit test coverage in v2.1.0

#### Documentation Completeness
- Basic docstrings for API endpoints
- Detailed project history and plans in development logs
- Interactive API documentation available at `/docs` endpoint

#### Technical Debt
1. Matplotlib font warnings in serverless environment
2. Performance limitations for large datasets (currently limited to 1000 samples)
3. Error handling user-friendliness needs improvement

### Code Organization and Modularity

#### Module Coupling Analysis
- API layer and algorithm layer separated through clear function calls
- Frontend and backend completely decoupled through REST API
- Data generation and analysis functions appropriately separated

#### Interface Design
- Clear API interface design using Pydantic models for request/response validation
- Well-defined endpoint functionality (e.g., `/generate-data`, `/regression`)
- Demo endpoint (`/demo`) provided for quick feature exploration

#### Extensibility and Maintainability
- Clear project structure facilitates adding new features
- FastAPI framework provides good extensibility foundation
- Version planning in development logs indicates ongoing maintenance plans

### Function Call Relationships

#### Core Functions
- **Entry Points**: `read_root()`, `health_check()`, `generate_data()`, `demo_analysis()`
- **Key Utility Functions**: `MultipleLinearRegression.fit()`, `generate_sample_data()`, `create_regression_plots()`

#### Module Dependencies
- `api/index.py` is the main entry point, depending on regression analysis module and FastAPI
- `python_modules/regression_analysis.py` contains core algorithms, depending on NumPy and Matplotlib
- Frontend (`templates/index.html`) interacts with backend through API
- Two possible entry points: `api/index.py` (Vercel) and `app/main.py` (traditional deployment)

## 模块间依赖
```mermaid
  graph TD;
    A[api/index.py] --> B[python_modules/regression_analysis.py]
    A --> C[templates/index.html]
    B --> D[numpy]
    B --> E[matplotlib]
    A --> D
    F[app/main.py] --> G[app/routers/data.py]
    F --> H[FastAPI]
    A --> H
```


## 调用链路分析

FastAPI应用初始化
│
├── GET / → read_root()
│
├── GET /health → health_check()
│
├── POST /generate-data → generate_data()
│   └── generate_sample_data()
│
├── POST /regression → (未在代码片段中显示完整实现)
│   ├── MultipleLinearRegression.fit()
│   └── 返回回归结果
│
├── POST /regression-with-plots → (未在代码片段中显示完整实现)
│   ├── MultipleLinearRegression.fit()
│   ├── create_regression_plots()
│   └── 返回回归结果和可视化
│
└── GET /demo → demo_analysis()
    ├── generate_sample_data()
    ├── MultipleLinearRegression.fit()
    ├── create_regression_plots()
    └── 返回演示数据、结果和可视化