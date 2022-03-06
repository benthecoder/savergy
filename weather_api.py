import json
import requests
import os
import streamlit as st

WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

# WEATHER_API_KEY = "WEATHER_API_KEY"
BASE_URL = "https://pro.openweathermap.org/data/2.5/forecast/climate"


def get_weather_pred(loc: dict):

    zip_code = loc["zip_code"]
    cnt_code = loc["cnt_code"].replace(" ", "")

    URL = BASE_URL + f"?zip={zip_code},{cnt_code}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(
            url=URL,
            headers={
                "Content-Type": "application/json",
            },
        )
        pred = response.json()

    except Exception as e:
        st.write(e)

    return pred


def get_info_frm_res(w_dict: dict):

    coords_dict = w_dict["city"]["coord"]

    cost_saved = 0
    temp_list = w_dict["list"]

    day_temp, night_temp = [], []

    for i in range(30):
        m_temp = temp_list[i]["temp"]["day"]
        n_temp = temp_list[i]["temp"]["night"]

        day_temp.append(m_temp)
        night_temp.append(n_temp)

        if m_temp >= 25:
            cost_saved += 0.35
        if n_temp < 25:
            cost_saved += 2.8

    return coords_dict, cost_saved, day_temp, night_temp
