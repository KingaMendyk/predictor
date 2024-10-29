import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import json
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from io import StringIO
import typer

# Load the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()
cli = typer.Typer()


# Define data model for JSON input
class DataModel(BaseModel):
    data: List[List[float]]


def clean_data(data):
    # Drop rows with empty cells
    data.replace('', np.nan, inplace=True)
    data.dropna(inplace=True)

    categorical_columns = data.select_dtypes(exclude=[np.number])

    # Changing categorical columns to numeric
    le = LabelEncoder()
    for column in categorical_columns:
        data[column] = le.fit_transform(data[column])

    # Standardizing data
    sc = StandardScaler()
    standardized_data = pd.DataFrame(sc.fit_transform(data), columns=data.columns, index=data.index)
    data = standardized_data
    data.drop('rownames', axis=1)
    return data


def predict(data):
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        df = pd.DataFrame(data)
    predictions = model.predict(df)
    return predictions.tolist()


# Endpoint for JSON input
@app.post("/predict-json")
async def predict_json(data: DataModel):
    try:
        df = pd.DataFrame(data.data)
        df = clean_data(df)
        predictions = predict(df)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for CSV input
@app.post("/predict-csv")
async def predict_csv(file: UploadFile):
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        df = clean_data(df)
        predictions = predict(df)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# CLI command for JSON input.
@cli.command("predict-json")
def cli_predict_json(data: str):
    try:
        json_data = json.loads(data)
        df = pd.DataFrame(json_data["data"])
        df = clean_data(df)
        predictions = predict(df)
        print({"predictions": predictions})
    except Exception as e:
        print("Error: ", e)


# CLI command for CSV file input
@cli.command("predict-csv")
def cli_predict_csv(filepath: str):
    try:
        df = pd.read_csv(filepath)
        df = clean_data(df)
        predictions = predict(df)
        print({"predictions": predictions})
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    typer.run(cli)
