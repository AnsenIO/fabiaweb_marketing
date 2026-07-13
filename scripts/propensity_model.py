#!/usr/bin/env python3
"""
Propensity model trainer.

Based on the standard CXL-style propensity-modeling workflow:
- Treat an observed binary outcome (e.g. purchase, signup, pre-order) as the target.
- Build a logistic regression that estimates P(outcome = 1 | user features).
- Output a propensity score for every row so you can rank users from "least likely"
  to "most likely" to convert and prioritise marketing spend / outreach.

Usage:
    python scripts/propensity_model.py path/to/data.csv \
        --target converted \
        --id-col email \
        --output data/scored.csv

The script is generic.  It expects a CSV where:
    - one column is the binary outcome (0/1, default column name "converted")
    - the remaining columns are features that describe the user / session / lead
      (numeric or categorical strings are both fine)

If your data is very small (e.g. the current shop only has a couple of test rows)
the model will train without error but the scores will not be meaningful yet.
Feed it a real lead / order / visitor export before using the scores.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a logistic-regression propensity model and score every row."
    )
    parser.add_argument("csv", help="Path to the CSV file with features and target.")
    parser.add_argument(
        "--target",
        default="converted",
        help="Name of the binary outcome column (0/1). Default: converted",
    )
    parser.add_argument(
        "--id-col",
        default=None,
        help="Optional ID column (e.g. email, user_id) to keep in the output.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of data held out for evaluation. Default: 0.2",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducible train/test split. Default: 42",
    )
    parser.add_argument(
        "--output",
        default="propensity_scored.csv",
        help="Where to save the scored CSV. Default: propensity_scored.csv",
    )
    return parser.parse_args()


def load_data(path: str, target: str, id_col: str | None) -> pd.DataFrame:
    """Load CSV, check the target exists, and make sure it is binary."""
    df = pd.read_csv(path)

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found. Columns: {list(df.columns)}")

    # Force target to numeric 0/1 (handles True/False, yes/no via factorisation if needed)
    if df[target].dtype == object:
        df[target] = pd.factorize(df[target])[0]
    df[target] = df[target].astype(int)

    if not df[target].isin([0, 1]).all():
        raise ValueError("Target column must contain only two classes (converted vs not).")

    print(f"Loaded {len(df)} rows, {df[target].sum()} conversions ({df[target].mean():.1%} rate)")
    return df


def build_feature_matrix(df: pd.DataFrame, target: str, id_col: str | None):
    """
    Separate features from target.
    Identify numeric and categorical columns so we can scale numbers and
    one-hot encode categories automatically.
    """
    drop_cols = [target]
    if id_col and id_col in df.columns:
        drop_cols.append(id_col)

    X = df.drop(columns=drop_cols)
    y = df[target]

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

    print(f"Features: {len(numeric_cols)} numeric, {len(categorical_cols)} categorical")
    return X, y, numeric_cols, categorical_cols


def build_pipeline(numeric_cols: list[str], categorical_cols: list[str]) -> Pipeline:
    """
    Build a scikit-learn pipeline:
      1. Preprocess: scale numeric features, one-hot encode categoricals.
      2. Logistic regression: outputs probabilities we can use as propensity scores.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
        ],
        remainder="drop",
    )

    # class_weight='balanced' helps when conversions are rare (typical for propensity data)
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        solver="lbfgs",
    )

    return Pipeline([("preprocess", preprocessor), ("model", model)])


def evaluate(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> None:
    """Print standard binary-classification diagnostics."""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n=== Evaluation on hold-out test set ===")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"ROC AUC:  {roc_auc_score(y_test, y_prob):.3f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, target_names=["not converted", "converted"]))


def report_coefficients(model: Pipeline, feature_names: list[str]) -> None:
    """
    After one-hot encoding the feature names change (e.g. country_FR, country_US).
    Pull the final logistic-regression coefficients and sort by impact.
    """
    # The pipeline is (preprocess, model).  We extract the fitted preprocessor
    # to reconstruct feature names.
    preprocessor = model.named_steps["preprocess"]
    try:
        final_names = preprocessor.get_feature_names_out()
    except AttributeError:
        # Fallback for older scikit-learn versions
        final_names = []
        for name, trans, cols in preprocessor.transformers_:
            if name == "num":
                final_names.extend(cols)
            elif name == "cat":
                final_names.extend(trans.get_feature_names_out(cols))

    coefs = model.named_steps["model"].coef_[0]
    coef_df = pd.DataFrame({"feature": final_names, "coefficient": coefs})
    coef_df["odds_ratio"] = pd.Series(coefs).apply(lambda c: round(2.71828 ** c, 3))
    coef_df = coef_df.sort_values("coefficient", key=abs, ascending=False)

    print("\n=== Top features by impact on conversion probability ===")
    print(coef_df.head(15).to_string(index=False))


def main() -> int:
    args = parse_args()

    # 1. Load data
    df = load_data(args.csv, args.target, args.id_col)

    # 2. Build feature matrix
    X, y, numeric_cols, categorical_cols = build_feature_matrix(df, args.target, args.id_col)

    # Guard against a tiny dataset: scikit-learn needs at least a few rows of each class
    if len(df) < 10 or y.value_counts().min() < 2:
        print(
            "\nWARNING: The dataset is too small to train a reliable propensity model. "
            "The script will still produce scores, but they should not be used for decisions "
            "until you have more conversions and non-conversions.",
            file=sys.stderr,
        )

    # 3. Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y if y.value_counts().min() >= 2 else None,
    )

    # 4. Fit model
    pipeline = build_pipeline(numeric_cols, categorical_cols)
    pipeline.fit(X_train, y_train)

    # 5. Evaluate
    if len(X_test) > 0 and y_test.nunique() > 1:
        evaluate(pipeline, X_test, y_test)

    # 6. Score the full dataset
    df["propensity_score"] = pipeline.predict_proba(X)[:, 1]
    df["propensity_rank"] = df["propensity_score"].rank(ascending=False, method="dense").astype(int)

    # 7. Explain features
    report_coefficients(pipeline, list(X.columns))

    # 8. Save
    output_path = Path(args.output)
    df.to_csv(output_path, index=False)
    print(f"\nScored {len(df)} rows and saved to: {output_path.resolve()}")
    print("\nTop 10 most likely to convert:")
    display_cols = [args.id_col] if args.id_col else []
    display_cols += [args.target, "propensity_score", "propensity_rank"]
    print(df[display_cols].sort_values("propensity_score", ascending=False).head(10).to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
