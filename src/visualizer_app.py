import os
import sys
import base64
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

from worldometers import WorldometersHTMLDataParser
from visualization_utils import get_pie_chart_multi_categories, get_bar_chart_single

url_to_parse = "https://www.worldometers.info/coronavirus/"
df_parsed = None

def country_wise():
    st.title("Countrywise covid-19 data")
    st.write(df_parsed)

    csv_file = df_parsed.to_csv(index=False)
    byte_file = base64.b64encode(csv_file.encode()).decode()
    date_time_string = datetime.now().isoformat(sep="_")[:-7].replace(":", "-")
    csv_file_name = f"{date_time_string}_covid19_worldometers.csv"
    href = f"<a href='data:file/csv;base64,{byte_file}' download={csv_file_name}>Download as csv file</a>"
    st.markdown(href, unsafe_allow_html=True)

    st.header("World covid-19 stats")
    total_cases_world = np.sum(df_parsed.TotalCases.to_numpy().astype(np.int32))
    total_deceased_world = np.sum(df_parsed.TotalDeaths.to_numpy().astype(np.int32))
    mortality_rate_world = np.around(100 * total_deceased_world / total_cases_world, 4)
    st.write(f"Total cases : {total_cases_world} ({total_cases_world/10**6:.2f}M)")
    st.write(f"Total deceased : {total_deceased_world} ({total_deceased_world/10**6:.2f}M)")
    st.write(f"Mortality rate : {mortality_rate_world} %")
    st.markdown("_Source of data - [Worldometers](https://www.worldometers.info/coronavirus/)_")
    return

def continent_wise():
    fig_1, fig_2, fig_3, fig_4 = None, None, None, None
    st.title("Continentwise covid-19 data")
    #st.write(df_parsed)
    continents = np.unique(df_parsed.Continent.to_numpy())
    selected_continent = st.sidebar.selectbox("Select continent", continents, index=1)
    show_percent = st.sidebar.checkbox("Show percentage in plot legend", True)

    df_continent = df_parsed[df_parsed["Continent"] == selected_continent]
    st.write(df_continent)

    csv_file = df_continent.to_csv(index=False)
    byte_file = base64.b64encode(csv_file.encode()).decode()
    date_time_string = datetime.now().isoformat(sep="_")[:-7].replace(":", "-")
    csv_file_name = f"{date_time_string}_{selected_continent.replace(' ', '_').replace('/', '_').lower()}_covid19_worldometers.csv"
    href = f"<a href='data:file/csv;base64,{byte_file}' download={csv_file_name}>Download as csv file</a>"
    st.markdown(href, unsafe_allow_html=True)

    st.header(f"{selected_continent} covid-19 stats")
    total_cases_continent = np.sum(df_continent.TotalCases.to_numpy().astype(np.int32))
    total_deceased_continent = np.sum(df_continent.TotalDeaths.to_numpy().astype(np.int32))
    mortality_rate_continent = np.around(100 * total_deceased_continent / total_cases_continent, 4)
    st.write(f"Total cases : {total_cases_continent} ({total_cases_continent/10**6:.2f}M)")
    st.write(f"Total deceased : {total_deceased_continent} ({total_deceased_continent/10**6:.2f}M)")
    st.write(f"Mortality rate : {mortality_rate_continent} %")

    fig_1 = get_pie_chart_multi_categories(df_continent.TotalCases.to_numpy(),
        df_continent["Country,Other"].to_numpy(),
        f"Distribution of total cases in {selected_continent} continent",
        show_percent=show_percent)

    if fig_1 is not None:
        st.pyplot(fig_1)

    fig_2 = get_pie_chart_multi_categories(df_continent.TotalDeaths.to_numpy(),
        df_continent["Country,Other"].to_numpy(),
        f"Distribution of total deceased in {selected_continent} continent",
        show_percent=show_percent)

    if fig_2 is not None:
        st.pyplot(fig_2)

    fig_3 = get_bar_chart_single(df_continent.TotalDeaths.to_numpy(),
        df_continent["Country,Other"].to_numpy(),
        f"Total deceased in countries in {selected_continent} continent",
        color="r")

    if fig_3 is not None:
        st.pyplot(fig_3)

    fig_4 = get_bar_chart_single(df_continent.MortalityRate.to_numpy(),
        df_continent["Country,Other"].to_numpy(),
        f"Mortality Rate in countries in {selected_continent} continent",
        color="b")

    if fig_4 is not None:
        st.pyplot(fig_4)

    st.markdown("_Source of data - [Worldometers](https://www.worldometers.info/coronavirus/)_")
    return

def app_info():
    st.title("App info")
    st.markdown("_Developer - Abhishek R. S._")
    st.markdown("_Github - [github.com/AbhishekRS4](https://github.com/AbhishekRS4)_")
    st.markdown("_Source of data - [Worldometers](https://www.worldometers.info/coronavirus/)_")
    return

modes = {
    "Country-wise" : country_wise,
    "Continent-wise": continent_wise,
    "App Info" : app_info,
}

def start_visualizer():
    worldometers_parser = WorldometersHTMLDataParser(url_to_parse)

    worldometers_parser.init_url_parser()
    worldometers_parser.init_beautiful_soup()
    worldometers_parser.find_table_with_id(table_id="main_table_countries_today")
    worldometers_parser.find_rows_of_table()
    worldometers_parser.find_header_of_table()
    worldometers_parser.preprocess_worldometers_covid_table()
    worldometers_parser.parse_numeric_data()
    worldometers_parser.calculate_mortality_rate()
    global df_parsed
    df_parsed = worldometers_parser._data_frame_parsed

    selected_mode = st.sidebar.selectbox("Select mode", list(modes.keys()))
    modes[selected_mode]()
    return

def main():
    start_visualizer()

if __name__ == "__main__":
    main()
