import dash
import numpy as np
import pandas as pd
from datetime import date 
import datetime as dt
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


nsw_covid_df = pd.read_csv('https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv')
nsw_covid_df.columns = ["Notification Date","Postcode","LHD_Code","LHD_District","LGA_Code","LGA_Name"]
df = nsw_covid_df.dropna()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Location"),
                dcc.Dropdown(
                    id="location",
					multi = "True",
					value = "Select All",
					placeholder="Select Area..",
                    options=[
                        {"label": col, "value": col} for col in df["LGA_Name"]
                    ],
                    
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Date"),
                dcc.DatePickerSingle(
					id='date_picker',
					min_date_allowed=date(2020, 1, 25),
					max_date_allowed=dt.date.today(),
					initial_visible_month=dt.date.today(),
					clearable=True
					#date=dt.date.today(),
				),
            ]
        ),
        
    ],
    body=True,
)

app.layout = dbc.Container(
    [
	 
        html.H1("NSW COVID-19 cases by location"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(id="covid_cases_barchart", md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
	Output("covid_cases_barchart", "children"),
    [
        Input("location", "value"),
        Input("date_picker", "date"),
    ],
)
def covid_cases_barchart(location,case_date):
	
	if not location and not case_date or "Select All" in location:
	    fig = px.histogram(df, x='LGA_Name',title="Number of Covid Cases based on Local Government Areas (LGA)")
	    return dcc.Graph(figure=fig)
	elif location is not None or "Select All" in case_date:
		df_new = df[df["LGA_Name"].isin(location)]
		fig = px.histogram(df_new, x='LGA_Name',title="Number of Covid Cases based on the selected Local Government Areas (LGA)")
		return dcc.Graph(figure=fig)
	elif location is not None and case_date is not None:
		df_new = df[df["LGA_Name"].isin(location) & df["Notification Date"].isin(case_date)]
		fig = px.histogram(df_new, x='LGA_Name',title="Number of Covid Cases based on the selected Local Government Areas (LGA)")
		return dcc.Graph(figure=fig)
if __name__ == "__main__":
    app.run_server(debug=False)