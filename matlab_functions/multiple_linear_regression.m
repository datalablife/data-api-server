function [coefficients, r_squared, y_pred, residuals] = multiple_linear_regression(X, y)
    % Multiple Linear Regression Function
    % Input:
    %   X - Matrix of independent variables (m x n)
    %   y - Vector of dependent variable (m x 1)
    % Output:
    %   coefficients - Regression coefficients including intercept
    %   r_squared - R-squared value
    %   y_pred - Predicted values
    %   residuals - Residual values
    
    % Add intercept term (column of ones)
    [m, n] = size(X);
    X_with_intercept = [ones(m, 1), X];
    
    % Calculate regression coefficients using normal equation
    % beta = (X'X)^(-1) * X'y
    coefficients = (X_with_intercept' * X_with_intercept) \ (X_with_intercept' * y);
    
    % Predict values
    y_pred = X_with_intercept * coefficients;
    
    % Calculate residuals
    residuals = y - y_pred;
    
    % Calculate R-squared
    ss_total = sum((y - mean(y)).^2);
    ss_residual = sum(residuals.^2);
    r_squared = 1 - (ss_residual / ss_total);
    
    % Display results
    fprintf('Regression Analysis Results:\n');
    fprintf('Intercept: %.4f\n', coefficients(1));
    for i = 2:length(coefficients)
        fprintf('Coefficient %d: %.4f\n', i-1, coefficients(i));
    end
    fprintf('R-squared: %.4f\n', r_squared);
end