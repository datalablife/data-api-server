from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import sys
import os

# Add python_modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from regression_analysis import MultipleLinearRegression, generate_sample_data, create_regression_plots

app = FastAPI(
    title="Data Analysis API Server",
    description="A Python backend API server for data analysis and regression",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class RegressionRequest(BaseModel):
    X: List[List[float]]
    y: List[float]

class DataGenerationRequest(BaseModel):
    n_samples: int = 100
    n_features: int = 2
    noise_level: float = 0.1

class RegressionResponse(BaseModel):
    intercept: float
    coefficients: List[float]
    r_squared: float
    predictions: List[float]
    residuals: List[float]
    n_samples: int
    n_features: int

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Data Analysis API Server!", 
        "status": "success",
        "version": "2.0.0",
        "endpoints": [
            "/health - Health check",
            "/generate-data - Generate sample dataset",
            "/regression - Perform multiple linear regression",
            "/regression-with-plots - Regression with visualization"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "data-analysis-api"}

@app.post("/generate-data")
def generate_data(request: DataGenerationRequest):
    """Generate sample data for regression analysis"""
    try:
        X, y = generate_sample_data(
            n_samples=request.n_samples,
            n_features=request.n_features,
            noise_level=request.noise_level
        )
        
        return {
            "X": X.tolist(),
            "y": y.tolist(),
            "shape": {
                "samples": X.shape[0],
                "features": X.shape[1]
            },
            "message": f"Generated {X.shape[0]} samples with {X.shape[1]} features"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regression", response_model=RegressionResponse)
def perform_regression(request: RegressionRequest):
    """Perform multiple linear regression analysis"""
    try:
        X = np.array(request.X)
        y = np.array(request.y)
        
        if X.shape[0] != len(y):
            raise HTTPException(
                status_code=400, 
                detail="Number of samples in X and y must match"
            )
        
        model = MultipleLinearRegression()
        results = model.fit(X, y)
        
        return RegressionResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regression-with-plots")
def regression_with_plots(request: RegressionRequest):
    """Perform regression analysis and return results with visualization plots"""
    try:
        X = np.array(request.X)
        y = np.array(request.y)
        
        if X.shape[0] != len(y):
            raise HTTPException(
                status_code=400, 
                detail="Number of samples in X and y must match"
            )
        
        model = MultipleLinearRegression()
        results = model.fit(X, y)
        
        # Generate plots
        plot_image = create_regression_plots(X, y, results)
        
        return {
            "regression_results": results,
            "plot_image": plot_image,
            "summary": {
                "model_performance": "Good" if results["r_squared"] > 0.7 else "Moderate" if results["r_squared"] > 0.5 else "Poor",
                "interpretation": f"The model explains {results['r_squared']*100:.1f}% of the variance in the dependent variable"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo")
def demo_analysis():
    """Demo endpoint with pre-generated data and analysis"""
    try:
        # Generate sample data
        X, y = generate_sample_data(n_samples=100, n_features=3, noise_level=0.2)
        
        # Perform regression
        model = MultipleLinearRegression()
        results = model.fit(X, y)
        
        # Create plots
        plot_image = create_regression_plots(X, y, results)
        
        return {
            "data": {
                "X": X.tolist(),
                "y": y.tolist()
            },
            "regression_results": results,
            "plot_image": plot_image,
            "demo": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/app", response_class=HTMLResponse)
def get_web_app():
    """Serve the web application interface"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading web app: {str(e)}</h1>", status_code=500)