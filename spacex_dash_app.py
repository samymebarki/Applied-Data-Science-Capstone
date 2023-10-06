# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                dcc.Graph(id='success-pie-chart'),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                marks={
                                                    0: str(min_payload),
                                                    2500: str(min_payload + 2500),
                                                    5000: str(min_payload + 5000),
                                                    7500: str(min_payload + 7500),
                                                    10000: str(max_payload)
                                                },
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                dcc.Graph(id='success-payload-scatter-chart'),
                                ])

# Callback to update pie chart and scatter chart
@app.callback(Output('success-pie-chart', 'figure'),
              Output('success-payload-scatter-chart', 'figure'),
              Input('site-dropdown', 'value'),
              Input('payload-slider', 'value'))
def update_charts(selected_site, payload_range):
    # Filter DataFrame based on selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Filter DataFrame based on payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create pie chart
    pie_chart = px.pie(filtered_df, names='class', title=f'Success vs. Failure for {selected_site}')

    # Create scatter chart
    scatter_chart = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                               title=f'Payload Mass vs. Success for {selected_site}')
    
    return pie_chart, scatter_chart

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
