# Day 2: fit something simple, and publish the result where the dashboard can read it.
#
#   python predict.py
#
# The shape of the job is here. The thinking is not.
#
# The obvious prediction for this dataset is lap time from tyre age, tyre compound and
# track temperature — you get tyre age by joining laps to stints, and temperature from
# the weather endpoint. But any honest prediction will do, and a linear regression you
# can explain in one sentence beats something clever that you cannot.
#
# Two rules:
#   1. Score the model on data it never saw. Otherwise you are reporting how well it
#      memorised the answers, which is not a finding.
#   2. Publish the real value next to the predicted one. A prediction nobody can check
#      is decoration, and the panel will ask.

import os
import sys

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def read_features(database_url: str) -> pd.DataFrame:
    engine = create_engine(database_url)

    # TODO write the query.
    #
    # Read from your normalised tables, not from raw. If the join is awkward, that is
    # a sign it belongs in a view — which the API may well want too.
    sql = """
        select 1 as placeholder
    """
    return pd.read_sql(sql, engine)


def fit(frame: pd.DataFrame):
    # TODO
    #
    # from sklearn.model_selection import train_test_split
    # from sklearn.linear_model import LinearRegression
    #
    # X = frame[["tyre_age_laps", "track_temperature", ...]]
    # y = frame["lap_time_ms"]
    #
    # Categorical inputs like tyre compound are text, and a linear model needs
    # numbers. Look up one-hot encoding, or pandas.get_dummies.
    raise NotImplementedError("fit() is yours")


def publish(document: dict) -> None:
    # Writes one small document to Firestore, which the Angular app reads directly
    # without going through the Java API. Keep it small: a handful of numbers, not a
    # dataset.
    import firebase_admin
    from firebase_admin import credentials, firestore

    credentials_path = os.environ.get("FIREBASE_CREDENTIALS")
    if not credentials_path:
        sys.exit("FIREBASE_CREDENTIALS is not set. See .env.example")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(credentials_path))

    client = firestore.client()
    collection = os.environ.get("FIREBASE_COLLECTION", "predictions")
    client.collection(collection).document("latest").set(document)
    print(f"published to {collection}/latest")


def main() -> None:
    load_dotenv()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        sys.exit("DATABASE_URL is not set. Copy .env.example to .env and fill it in.")

    frame = read_features(database_url)
    print(f"{len(frame)} rows of features")

    model, score = fit(frame)

    # The shape the dashboard expects. Agree the field names with the development
    # team and write them into AGREEMENT.md, the same as any other endpoint.
    document = {
        "predicts": "lap time in milliseconds",
        "from": ["tyre age in laps", "tyre compound", "track temperature"],
        "model": "linear regression",
        "r2_on_unseen_data": score,
        "example": {
            "driver": None,
            "lap": None,
            "predicted_ms": None,
            "actual_ms": None,
        },
        "generated_at": pd.Timestamp.utcnow().isoformat(),
        "known_weaknesses": "",
    }
    publish(document)


if __name__ == "__main__":
    main()
