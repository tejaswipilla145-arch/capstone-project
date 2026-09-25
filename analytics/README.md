Task A – Data Exploration (EDA)
I loaded the Titanic dataset and saved it as titanic.csv

I checked the dataset with info(), describe(), and shape

I calculated missing values and handled them (drop rows, fill values, or drop column depending on percentage missing)

I plotted histograms and boxplots for age and fare

I found outliers using the IQR rule

I checked skewness of fare by comparing mean, median, and mode

I calculated survival rates by sex, class, and both together

I created a correlation heatmap for numeric columns and explained the strongest correlations

I made charts to show survival patterns

I standardized age and fare with z‑score to confirm scaling

Task B – Predictive Modeling
I split the data into train and test sets using stratified sampling

I built a preprocessing pipeline (impute missing values, encode categorical, scale numeric)

I trained Logistic Regression, Decision Tree, and Random Forest models

I evaluated them with accuracy, precision, recall, F1, AUC, and confusion matrix

I compared imbalance handling: baseline, balanced weights, and SMOTE oversampling

I tuned Random Forest with GridSearchCV and checked the OOB score

I did a regression task to predict fare with Linear Regression

I reported MAE, RMSE, R², Adjusted R², and plotted residuals

I made comparison tables for classification and regression metrics

I saved the best pipeline with joblib and reloaded it to confirm predictions