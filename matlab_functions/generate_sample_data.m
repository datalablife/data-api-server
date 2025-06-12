function [X, y] = generate_sample_data(n_samples, n_features, noise_level)
    % Generate sample data for regression analysis
    % Input:
    %   n_samples - Number of data points
    %   n_features - Number of independent variables
    %   noise_level - Standard deviation of noise
    % Output:
    %   X - Matrix of independent variables
    %   y - Vector of dependent variable
    
    if nargin < 3
        noise_level = 0.1;
    end
    
    % Generate random independent variables
    rng(42); % Set seed for reproducibility
    X = randn(n_samples, n_features);
    
    % Create true coefficients
    true_coefficients = randn(n_features, 1) * 2;
    true_intercept = randn() * 5;
    
    % Generate dependent variable with noise
    y = true_intercept + X * true_coefficients + noise_level * randn(n_samples, 1);
    
    fprintf('Generated %d samples with %d features\n', n_samples, n_features);
    fprintf('True intercept: %.4f\n', true_intercept);
    fprintf('True coefficients: ');
    fprintf('%.4f ', true_coefficients);
    fprintf('\n');
end