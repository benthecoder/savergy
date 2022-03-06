import json
import requests
import os
import streamlit as st

MAGE_API_KEY = st.secrets["MAGE_API_KEY"]
MODEL_NAME = st.secrets["MODEL_NAME"]

# MAGE_API_KEY = "MAGE_API_KEY"
# MODEL_NAME = "MAGE_MODEL_NAME"
VERSION = 2


def get_predictions(features: dict):

    try:
        response = requests.post(
            url="https://api.mage.ai/v1/predict",
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "api_key": MAGE_API_KEY,
                    "model": MODEL_NAME,
                    "version": VERSION,
                    "features": [features],
                }
            ),
        )
        pred = response.json()
    except Exception as e:
        st.write(e)

    return pred
