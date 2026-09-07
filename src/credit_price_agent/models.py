from __future__ import annotations
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

RISK_NUM = ["revenue","ebitda_margin","leverage","interest_cover","relationship_years","repayment_score"]
ACC_NUM = RISK_NUM + ["previous_accept","market_rate","funding_spread","amount","tenor_years","offered_rate"]
CAT = ["industry"]

def _prep(num):
    return ColumnTransformer([
        ("num", StandardScaler(), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)
    ])

def fit_pd_model(train):
    pipe = Pipeline([
        ("prep", _prep(RISK_NUM)),
        ("model", LogisticRegression(max_iter=1000))
    ])
    pipe.fit(train[RISK_NUM+CAT], train["default"])
    return pipe

def fit_acceptance_model(train):
    pipe = Pipeline([
        ("prep", _prep(ACC_NUM)),
        ("model", LogisticRegression(max_iter=1000))
    ])
    pipe.fit(train[ACC_NUM+CAT], train["accepted"])
    return pipe

def predict_acceptance_at_rate(model, rows, rate):
    x = rows[ACC_NUM+CAT].copy()
    x["offered_rate"] = rate
    return model.predict_proba(x)[:,1]
