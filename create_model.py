import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, make_scorer
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('log.txt'),
        logging.StreamHandler()
    ]
)


def data_analysis(data):
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f")
    plt.title("Correlation matrix")
    # plt.show()

    logging.info("Finished data analysis")


def data_preparation(url):
    logging.info("Started data preparation")
    data = pd.read_csv(url)

    # Drop rows with empty cells
    data.replace('', np.nan, inplace=True)
    data.dropna(inplace=True)
    logging.info("---Dropped rows with empty values")

    categorical_columns = data.select_dtypes(exclude=[np.number])

    # Changing categorical columns to numeric
    le = LabelEncoder()
    for column in categorical_columns:
        data[column] = le.fit_transform(data[column])
    logging.info("---Changed categorical columns to numeric")

    # Standardizing data
    sc = StandardScaler()
    standardized_data = pd.DataFrame(sc.fit_transform(data), columns=data.columns, index=data.index)
    data = standardized_data
    data.drop('rownames', axis=1)
    logging.info("---Standardized data")

    return data


def split_data(data):
    # Splitting data into train and test sets
    X = data.iloc[:, data.columns != 'score']
    y = data['score']

    logging.info("Split data into train and test sets")
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train):
    logging.info("Started training model")
    model = RandomForestRegressor(max_depth=10, max_features='sqrt', min_samples_split=5,
                                  n_estimators=300)
    model.fit(X_train, y_train)

    importances = model.feature_importances_
    feature_importance = pd.Series(importances, index=X_train.columns)
    feature_importance.nlargest(10).plot(kind='barh')
    plt.title("Feature importance")
    # plt.show()

    logging.info("Finished training model")
    return model


def evaluate_model(model, X_test, y_test, X_train, y_train):
    logging.info("Started model evaluation")
    # Set up k-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_scorer = make_scorer(r2_score)
    mae_scorer = make_scorer(mean_absolute_error)
    mse_scorer = make_scorer(mean_squared_error)

    # Perform cross-validation for each metric
    r2_scores = cross_val_score(model, X_train, y_train, cv=kf, scoring=r2_scorer)
    mae_scores = cross_val_score(model, X_train, y_train, cv=kf, scoring=mae_scorer)
    mse_scores = cross_val_score(model, X_train, y_train, cv=kf, scoring=mse_scorer)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    residuals = y_test - y_pred
    sns.scatterplot(x=y_pred, y=residuals)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residuals vs Predicted Values')
    # plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, bins=30, kde=True)
    plt.axvline(0, color='red', linestyle='--')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals')
    # plt.show()

    logging.info("Finished model evaluation")

    logging.info("Generating report")
    generate_report("report.txt", model, r2_scores, mae_scores, mse_scores, r2, mse, mae)
    logging.info("Report generated")


def generate_report(file_name, model, r2_scores, mae_scores, mse_scores, r2, mse, mae):
    report = f"""
    =========== REPORT ===========
    Model used: {model}
    Cross-validation scores:
        R2 scores: {r2_scores}
        MAE scores: {mae_scores}
        MSE scores: {mse_scores}
    Train set - Mean R2: {np.mean(r2_scores)}
    Train set - Mean MAE: {np.mean(mae_scores)}
    Train set - Mean MSE: {np.mean(mse_scores)}
    Test set - R2: {r2:.2f}
    Test set - MAE: {mae:.2f}
    Test set - MSE: {mse:.2f}
    """
    with open(file_name, 'w') as file:
        file.write(report)


def save_model_to_file(file_name, model):
    with open(file_name, "wb") as f:
        pickle.dump(model, f)


def result_analyser(file_name):
    logging.info("Script started")
    data = data_preparation(file_name)
    data_analysis(data)
    X_train, X_test, y_train, y_test = split_data(data)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test, X_train, y_train)
    save_model_to_file("model.pkl", model)
    logging.info("Script finished")


file_url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv"
result_analyser(file_url)
