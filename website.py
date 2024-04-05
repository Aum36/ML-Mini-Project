import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_leaflet as dl

# Sample data (coordinates and names)
marker_data = [
    {"name": "Marker 1", "lat": 51.505, "lon": -0.09},
    {"name": "Marker 2", "lat": 51.51, "lon": -0.1},
    {"name": "Marker 3", "lat": 51.515, "lon": -0.11}
]

# Create Dash app
app = dash.Dash(__name__)
# app.layout = html.Div([html.Div([html.P("Hello World!"), dl.Map([
#     dl.TileLayer()
# ], center=[56, 10], zoom=6, style={'height': '50vh'})])])

markerElements = [dl.Marker(position=[marker['lat'], marker['lon']], children=[
            dl.Tooltip(marker['name'])  # Display marker name on hover
        ], id=f"marker-{index}") for index, marker in enumerate(marker_data)]

# Define layout
app.layout = html.Div([
    html.Div(id='marker-info'),  # HTML div to display marker info
    dl.Map([dl.TileLayer()] + markerElements, id='map', center=[51.505, -0.09], zoom=10, style={'height': '50vh'})
])

# Define callback to update marker info
@app.callback(
    Output('marker-info', 'children'),
    Input('map', 'click_lat_lng'))
def update_marker_info(click_lat_lng):
    if click_lat_lng is None:
        # If no marker is clicked
        return "Click on a marker to display its name."
    
    print(click_lat_lng)
    clicked_lat, clicked_lon = click_lat_lng
    for marker in marker_data:
        if marker['lat'] == clicked_lat and marker['lon'] == clicked_lon:
            return f"You clicked on: {marker['name']}"
    
    return "No marker found at clicked location."

if __name__ == '__main__':
    app.run_server(debug=True)
