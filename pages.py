from re import L, S
import streamlit as st
from mage_api import get_predictions
import streamlit_authenticator as stauth
import pandas as pd

from weather_api import get_weather_pred, get_info_frm_res
from twilio_api import send_message

names = ["John Doe"]
usernames = ["jdoe"]
passwords = ["abc123"]

country_df = pd.read_csv(
    "https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv"
)

country_list = country_df["Alpha-2 code"].str.replace('"', "").tolist()


def home_page():

    st.markdown(
        """
        ## Welcome to Savergy  ⚡
        ### Your personal AI Energy assistant
        """
    )

    st.caption("username: jdoe | password: abc123")
    hashed_passwords = stauth.hasher(passwords).generate()

    authenticator = stauth.authenticate(
        names,
        usernames,
        hashed_passwords,
        "JWT_KEY",
        "Y3yZwmqOfq2JThKIkBaHtRLhfxt7odkuNlZGQfzVCLeJAoqY3PmEy6LPXmcdtCaareRzH3R9GBSmK7NtkJFCXQ==",
        cookie_expiry_days=30,
    )

    name, authentication_status = authenticator.login("Login", "main")

    if st.session_state["authentication_status"]:
        st.markdown(
            f"""
            ### Welcome back *{st.session_state['name']}*

            #### 👈 Click on the the prediction tab to see your energy usage now! 
            """
        )

        st.caption("source")
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")


def pred_page():
    submit = False

    st.title("Predictions🔮")
    with st.form("usr_energy_info"):

        st.subheader("Tell me about your home")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        heatroom = col1.number_input(
            "Enter number of rooms heated", min_value=0, max_value=10
        )
        acrooms = col2.number_input(
            "Enter number of rooms cooled", min_value=0, max_value=10
        )
        bedrooms = col3.number_input(
            "Enter the total number of bedrooms", min_value=0, max_value=10
        )
        ncombath = col4.number_input(
            "Enter the total number of bathrooms", min_value=0, max_value=10
        )
        totrooms = col5.number_input(
            "Enter the total number of rooms", min_value=0, max_value=10
        )
        totsqft = col6.number_input("Enter total square footage of the house", step=0.1)

        st.subheader("Tell me about your location")
        col1, col2 = st.columns(2)
        zip_code = col1.text_input("Enter your ZIP Code")
        cnt_code = col2.selectbox("Enter your country", country_list)

        st.subheader("We want to reduce your energy cost")
        st.caption("Don't forget to include the country code i.e. +1 for US")
        phone_num = st.text_input(
            "Enter your phone number",
        )

        opt_in = st.checkbox("Do you opt in for notifications?")

        user_input = {
            "heatroom": heatroom,
            "acrooms": acrooms,
            "bedrooms": bedrooms,
            "ncombath": ncombath,
            "totrooms": totrooms,
            "totsqft": totsqft,
        }

        weather_input = {"zip_code": zip_code, "cnt_code": cnt_code}

        submitted = st.form_submit_button("Submit")

        if submitted:
            pred = get_predictions(user_input)
            weather_pred = get_weather_pred(weather_input)
            st.success("Thanks for the information!")
            submit = True

    if submit is False:
        return

    coords_dict, cost_saved, day_temp, night_temp = get_info_frm_res(weather_pred)

    st.header("here's a breakdown")

    cost = 0.1 if pred[0]["prediction"] <= 0 else pred[0]["prediction"]
    energy_use = cost / 0.35

    st.caption("We assume cost of electricity is $0.35 per kWh")

    st.subheader(f"Estimated Cost of Energy Usage: ${round(cost * 24 * 30, 3)}")
    st.subheader(f"Estimated Energy Usage: {round(energy_use * 24 * 30, 3)} kW")

    map = pd.DataFrame(
        [[coords_dict["lat"], coords_dict["lon"]]], columns=["lat", "lon"]
    )

    map_dict = {"day": day_temp, "night": night_temp}

    chart_data = pd.DataFrame(map_dict)

    st.subheader("This is the map of your location")
    st.map(map)

    st.subheader("Day and Night temperature for the next 30 days")
    st.line_chart(chart_data)

    energy_saved = round(cost_saved / 0.35, 3)

    st.subheader(
        f"If you subscribed for notifications from us, and follow our advice, you can save ${round(cost_saved, 3)} and ${energy_saved} in the next 30 days"
    )

    next_day_temp = day_temp[0]
    next_night_temp = night_temp[0]

    message = ""

    if next_day_temp >= 25:
        message += "Don't turn on the AC tomorrow morning"
    elif next_night_temp < 25:
        message += "\n Don't use the heater tomorrow night"

    if opt_in:
        send_message(phone_num, message)


def analytics_page():
    st.write("Plots of data")


def rec_page():

    st.markdown(
        """

        DID YOU KNOW? 💡
        
        Energy use in buildings (residential and commercial) contribute to **17.5%** of Global greenhouse gas emissions, which amounts to 8.33 Billion tonnes carbon dioxide-equivalents (CO₂e) [source](https://ourworldindata.org/emissions-by-sector#co2-emissions-by-sector)
        
        - Residential buildings (10.9%): energy-related emissions from the generation of electricity for lighting, appliances, cooking etc. and heating at home.
        - Commercial buildings (6.6%): energy-related emissions from the generation of electricity for lighting, appliances, etc. and heating in commercial buildings such as offices, restaurants, and shops.

        This means the ligthing that lights up your home, the heater that keeps you warm, the laptop charger you keep on overnight, all that is contributing to CO2 gases

        Want to know what what just 1 tonne of the gas looks like? 
        """
    )

    st.image("media/1-ton.jpeg")
    st.image("media/1-ton=.jpeg")

    st.write("Here's how you can start saving energy")

    st.markdown(
        """
        ## Useful Facts to save energy
        1. Electronics that draw power even when they’re not being used – can add 5% to 10% to your electrical bill, Natural Resources Canada (NRCan) reports
        1. Inadequate windows and doors can drain up to 25% of the heat from your home, according to NRCan
        1. Sealing uncontrolled air leaks can save 10% to 20% on your heating and cooling bills, according to the U.S. Department of Energy
        1. Changing your temperature setting for only eight hours a day could save you up to 10% on your annual heating and cooling costs, the U.S. DOE says
        1. Programmable thermostats can help prevent carbon emissions and reduce your heating bill costs.
        
        
        ## Energy Efficiency Rebates and Incentives
        
        Some utility companies and federal and state government agencies offer tax credits, rebates and other incentives to encourage home energy-efficiency improvements and the use of renewable energy sources.

        The IRS offers the Nonbusiness Energy Property Credit that allows you to take tax credits to help you pay for some energy efficiency improvements you make to your home.


        1. Tax credits of 10% of the cost not to exceed $500 (excluding installation) may be available for some energy efficiency improvements, including insulation, roofs, and windows, doors and skylights.
        1. Renewable Energy Tax credits of 22%, 26%, or 30% are available for renewable energy products that meet specific requirements through Dec. 3, 2023, according to Energystar.gov. These include credits for items including solar energy systems, geothermal heat pumps, and biomass fuel stoves.

        --- 
        Sources:
        1. https://growensemble.com/how-to-save-energy-at-home/
        1. https://mygreenmontgomery.org/2022/15-energy-saving-tips-for-homeowners/
        """
    )
