#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import altair as alt
import pandas as pd



def get_data_from_csv(columns, countries=None, start=None, end=None):
    """Creates pandas dataframe from .csv file.

    Data will be filtered based on data column name, list of countries to be plotted and
    time frame chosen.

    Args:
        columns (list(string)): a list of data columns you want to include
        countries ((list(string), optional): List of countries you want to include.
        If none is passed, dataframe should be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): The first date to include in the returned dataframe.
            If specified, records earlier than this will be excluded.
            Default: include earliest date
            Example format: "2021-10-10"
        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"
    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and countries chosen
    """
    # add path to .csv file from 6.0
    path = "owid-covid-data.csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"] + ["date"] + [columns],
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )
    print(df.columns)
    if countries is None:
        # no countries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
            
        else:
            
            end_date = datetime.strptime(end, "%Y-%m-%d")
        df_latest_dates = df[df.date.isin([end_date])]

        # identify the 6 countries with the highest case count
        # on the last included day
        countries = df_latest_dates.sort_values("new_cases_per_million", ascending=False).dropna().location.iloc[:6]
        
    # now filter to include only the selected countries
    cases_df = df[df.location.isin(countries)]

    if(start is None):
        start="2020-05-10"
  
    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        # exclude records earlier than start_date
        cases_df = cases_df[cases_df.date >= datetime.strptime(start, "%Y-%m-%d")]

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")
        # exclude records later than end date
        cases_df = cases_df[cases_df.date <= datetime.strptime(end, "%Y-%m-%d")]    

    
    return cases_df


def plot_reported_cases_per_million(countries=None, start=None, end=None):
    """Plots data of reported covid-19 cases per million using altair.
    Calls the function get_data_from_csv to receive a dataframe used for plotting.

    Args:
        countries ((list(string), optional): List of countries you want to filter.
        If none is passed, dataframe will be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
        of the dates will be older then this on
        end (string, optional): a string of the en date of the table, none of
        the dates will be newer then this one
    Returns:
        altair Chart of number of reported covid-19 cases over time.
    """
    # choose data column to be extracted
    columns = "new_cases_per_million"
    # create dataframe
    cases_df = get_data_from_csv(columns, countries, start, end)
    
    # Note: when you want to plot all countries simultaneously while enabling checkboxes, you might need to disable altairs max row limit by commenting in the following line
    alt.data_transformers.disable_max_rows()

    chart = (
        alt.Chart(cases_df, title="Daily new confirmed COVID-19 cases per million people.")
        .mark_line()
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                "new_cases_per_million",
                axis=alt.Axis(
                    title="Number of Reported Cases per Million",
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
        )
        .interactive()
    )
    return chart

def get_countries():
    """
    This function loads the csv data set and extracts the unique contry names

    Returns:
        (dataframe): dataframe consisting of unique country names
    """
    path = "owid-covid-data.csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"],
    )
    
    return df.location.unique()


def main():
    """Function called when run as a script

    Creates a chart and display it or save it to a file
    """
    listc = ["Slovenia", "Sweden", "Norway"]
    #get_countries()
    
    chart = plot_reported_cases_per_million(listc, "2020-08-11", "2021-11-14") 
    # Wrong date example:
    # chart = plot_reported_cases_per_million(listc, "2021-11-14", "2020-08-11") 

    # Requires altair_viewer.
    chart.show()

    # Please run the line below if u want to check the result for 6 countries with highest count on the
    # last date in the csv file (2021-11-16).
    # Default arguments are start="2020-05-10" and end=the last table entry for a given country.
    # chart = plot_reported_cases_per_million() 
    # chart.show()
    


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Oooups, the start date must be earlier than the end date.")



