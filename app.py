import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Data Preparation
data = pd.read_csv("C:\\Users\\karre\\OneDrive\\Documents\\PDDS\\UFO2000.csv")

# Group the data by 'season' and 'UFO_shape', then count sightings
season_ufo_counts = data.groupby(['Season', 'UFO_shape']).size().reset_index(name='count')

# Create a pivot table to restructure the data for plotting
pivot_data = season_ufo_counts.pivot(index='Season', columns='UFO_shape', values='count').fillna(0)
print(pivot_data)

# Create a Dash app
app = dash.Dash(__name__)

server = app.server

# Layout with Dropdown for UFO Shapes
app.layout = html.Div([
    html.H1('UFO Shapes Sighted by Season in 2000'),

    # Dropdown to select UFO Shape
    dcc.Dropdown(
        id='ufo-shape-dropdown',
        options=[{'label': shape, 'value': shape} for shape in pivot_data.columns],
        value=pivot_data.columns.tolist(),  # Default value (all UFO shapes)
        multi=True,  # Allow multi-selection
        placeholder="Select UFO shape(s)"
    ),

    # Graph to display the bar chart
    dcc.Graph(id='ufo-shape-chart')  # Graph for the chart
])

# Callback to update the bar chart based on selected UFO shapes
@app.callback(
    Output('ufo-shape-chart', 'figure'),
    Input('ufo-shape-dropdown', 'value')
)
def update_chart(selected_shapes):
    # Filter the data based on the selected UFO shapes
    filtered_data = pivot_data[selected_shapes]

    # Create a stacked bar chart using Plotly
    fig = px.bar(filtered_data,
                 x=filtered_data.index,
                 y=filtered_data.columns,
                 title='UFO Sighted by Season in 2000',
                 labels={'value': 'Number of UFOs sighted', 'Season': 'Season'},
                 barmode='stack')

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
