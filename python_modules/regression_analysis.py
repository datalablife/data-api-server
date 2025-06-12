import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List, Dict
import io
import base64

class MultipleLinearRegression:
    def __init__(self):
        self.coefficients = None
        self.intercept = None
        self.r_squared = None
        self.fitted = False
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """
        Fit multiple linear regression model
        
        Args:
            X: Independent variables matrix (m x n)
            y: Dependent variable vector (m,)
            
        Returns:
            Dictionary with regression results
        """
        # Add intercept term
        X_with_intercept = np.column_stack([np.ones(X.shape[0]), X])
        
        # Calculate coefficients using normal equation
        # beta = (X'X)^(-1) * X'y
        coefficients_full = np.linalg.solve(
            X_with_intercept.T @ X_with_intercept, 
            X_with_intercept.T @ y
        )
        
        self.intercept = coefficients_full[0]
        self.coefficients = coefficients_full[1:]
        
        # Predict values
        y_pred = X_with_intercept @ coefficients_full
        
        # Calculate residuals
        residuals = y - y_pred
        
        # Calculate R-squared
        ss_total = np.sum((y - np.mean(y))**2)
        ss_residual = np.sum(residuals**2)
        self.r_squared = 1 - (ss_residual / ss_total)
        
        self.fitted = True
        
        return {
            'intercept': float(self.intercept),
            'coefficients': self.coefficients.tolist(),
            'r_squared': float(self.r_squared),
            'predictions': y_pred.tolist(),
            'residuals': residuals.tolist(),
            'n_samples': X.shape[0],
            'n_features': X.shape[1]
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using fitted model"""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction")
        
        return self.intercept + X @ self.coefficients

def generate_sample_data(n_samples: int = 100, n_features: int = 2, noise_level: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate sample data for regression analysis
    
    Args:
        n_samples: Number of data points
        n_features: Number of independent variables
        noise_level: Standard deviation of noise
        
    Returns:
        Tuple of (X, y) arrays
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate random independent variables
    X = np.random.randn(n_samples, n_features)
    
    # Create true coefficients
    true_coefficients = np.random.randn(n_features) * 2
    true_intercept = np.random.randn() * 5
    
    # Generate dependent variable with noise
    y = true_intercept + X @ true_coefficients + noise_level * np.random.randn(n_samples)
    
    return X, y

def create_regression_plots(X: np.ndarray, y: np.ndarray, model_results: Dict) -> str:
    """
    Create visualization plots for regression analysis
    
    Args:
        X: Independent variables
        y: Dependent variable
        model_results: Results from regression model
        
    Returns:
        Base64 encoded plot image
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Multiple Linear Regression Analysis', fontsize=16)
    
    predictions = np.array(model_results['predictions'])
    residuals = np.array(model_results['residuals'])
    
    # Plot 1: Actual vs Predicted
    axes[0, 0].scatter(y, predictions, alpha=0.7)
    axes[0, 0].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    axes[0, 0].set_xlabel('Actual Values')
    axes[0, 0].set_ylabel('Predicted Values')
    axes[0, 0].set_title(f'Actual vs Predicted (R² = {model_results["r_squared"]:.3f})')
    
    # Plot 2: Residuals vs Predicted
    axes[0, 1].scatter(predictions, residuals, alpha=0.7)
    axes[0, 1].axhline(y=0, color='r', linestyle='--')
    axes[0, 1].set_xlabel('Predicted Values')
    axes[0, 1].set_ylabel('Residuals')
    axes[0, 1].set_title('Residuals vs Predicted')
    
    # Plot 3: Histogram of Residuals
    axes[1, 0].hist(residuals, bins=20, alpha=0.7, edgecolor='black')
    axes[1, 0].set_xlabel('Residuals')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Distribution of Residuals')
    
    # Plot 4: Feature importance (coefficients)
    feature_names = [f'Feature {i+1}' for i in range(len(model_results['coefficients']))]
    axes[1, 1].bar(feature_names, model_results['coefficients'])
    axes[1, 1].set_xlabel('Features')
    axes[1, 1].set_ylabel('Coefficient Value')
    axes[1, 1].set_title('Feature Coefficients')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    plot_data = buffer.getvalue()
    buffer.close()
    plt.close()
    
    plot_base64 = base64.b64encode(plot_data).decode()
    return f"data:image/png;base64,{plot_base64}"