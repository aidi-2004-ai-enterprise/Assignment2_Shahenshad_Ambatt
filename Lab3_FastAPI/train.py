"""
Train an XGBoost classifier on the Seaborn Penguins dataset and save the model.
"""

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import os


def load_and_preprocess_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    Load the penguins dataset and return processed features and labels.
    """
    df = sns.load_dataset("penguins").dropna()

    # Label encode target
    le = LabelEncoder()
    df["species"] = le.fit_transform(df["species"])

    # Manual one-hot encoding
    for col, values in {
        "sex": ["male", "female"],
        "island": ["Biscoe", "Dream", "Torgersen"]
    }.items():
        for val in values:
            df[f"{col}_{val}"] = (df[col] == val).astype(int)

    df.drop(columns=["sex", "island"], inplace=True)

    expected_cols = [
        "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year",
        "sex_female", "sex_male",
        "island_Biscoe", "island_Dream", "island_Torgersen"
    ]
    df = df.reindex(columns=expected_cols + ["species"])

    X = df.drop("species", axis=1)
    y = df["species"]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series) -> xgb.XGBClassifier:
    """
    Train and return an XGBoost classifier.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = xgb.XGBClassifier(
        max_depth=3,
        n_estimators=100,
        use_label_encoder=False,
        eval_metric="mlogloss"
    )
    model.fit(X_train, y_train)

    print("Training F1-score:", f1_score(y_train, model.predict(X_train), average='weighted'))
    print("Test F1-score:", f1_score(y_test, model.predict(X_test), average='weighted'))
    print("\nClassification Report:\n", classification_report(y_test, model.predict(X_test)))
    return model


def save_model(model: xgb.XGBClassifier, path: str) -> None:
    """
    Save the trained model to the given path.
    """
    model.save_model(path)
    print(f"✅ Model saved to: {path}")


if __name__ == "__main__":
    X, y = load_and_preprocess_data()
    model = train_model(X, y)
    save_path = os.path.join("app", "data", "model.json")
    save_model(model, save_path)
