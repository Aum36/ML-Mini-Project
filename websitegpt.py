import dash
from dash import dcc, html, callback, ctx, MATCH, ALL
from dash.dependencies import Input, Output
import dash_leaflet as dl
from datetime import datetime
import xgboost as xgb
import pandas as pd

df_bs = pd.read_csv('dataset/BSinfo.csv')
df_bs = df_bs[0:20]
df = pd.read_csv('dataset/Station_Data.csv', parse_dates=True
                 )
print(df.columns)
df["Time"] = pd.to_datetime(df["Time"])
cols =['BS', 'load', 'ESMode1', 'ESMode2', 'ESMode3',
       'active_cells', 'load_1', 'load_sum', 'load_mult', 'RUType', 'Frequency',
       'Bandwidth', 'Antennas', 'TXpower', 'Frequency_1', 'Bandwidth_1',
       'Antennas_1', 'TXpower_1', 'BS_count', 'Hour', 'Hour_sin', 'Hour_cos',
       'hour_class', 'Day_of_week', 'Is_weekend', 'Day_of_month',
       'Energy_Saving_Intensity',
       'BS_std_load', 'BS_mean_load', 'BS_min_load',
       'BS_max_load', 'next_load']
lat_lon = pd.read_csv('random_points.csv')
lat_lon.reset_index(inplace=True)
print(lat_lon.dtypes)
df_bs['lat'] = lat_lon['lat'][:df_bs.shape[0]]
print(lat_lon.head())
df_bs['lon'] = lat_lon['lon'][:df_bs.shape[0]]

# Sample data (coordinates and names)
marker_data = [
    {"name": "Marker 1", "lat": 51.505, "lon": -0.09},
    {"name": "Marker 2", "lat": 51.51, "lon": -0.1},
    {"name": "Marker 3", "lat": 51.515, "lon": -0.11}
]
df_bs.reset_index(inplace=True)
xgb_model = xgb.XGBRegressor()
xgb_model.load_model('xgb_model.model')


# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=datetime(2023, 1, 1),
        max_date_allowed=datetime(2023, 1, 7),
        initial_visible_month=datetime(2023, 1, 1),
        date=datetime(2023, 1, 1),
        style={'position': 'relative', 'zIndex': '1'}
    ),
    dcc.Input(type='time', min="0:00", max="24:00", value="0:00", id='my-time', step='1:00'),
    html.Div(id='marker-info', style={'height': '20vh'}),  # HTML div to display marker info
    dl.Map(center=[37.46412802679991,-102.0996437005695],zoom=10, style={'height': '50vh'}, children=[
        dl.TileLayer(),
        # Add markers
        *[dl.Marker(position=[marker['lat'], marker['lon']], children=[
            dl.Tooltip(marker['BS'])  # Display marker name on hover
        ], id={
            'type': 'marker',
            'index': index
        }) for index, marker in df_bs.iterrows()]
    ]),
    html.Div(id='energy-consumption')
])

# Define callback to update marker info
@callback(
    Output('marker-info', 'children'),
    Output('energy-consumption', 'children'),
    Input({'type': 'marker', 'index': ALL}, 'n_clicks'),
    Input('my-date-picker-single', 'date'), 
    Input('my-time', 'value'))
def update_marker_info(n_clicks, date, value):
    bs = ""
    result = ['']
    print(ctx.triggered_id)
    # Get ID of the clicked marker
    if ctx.triggered_id is not None and ctx.triggered_id != 'my-date-picker-single' and ctx.triggered_id != 'my-time':
        check = datetime.strptime(date.split("T")[0], "%Y-%d-%m")
        mydt = datetime.combine(check, 
                              datetime.strptime(value, '%H:%M').time())
        print(mydt)
        mydt = pd.to_datetime(mydt)
        print(type(mydt))
        print(type(df["Time"].dt))
        # print(date.split("T")[0])
        # print(df_row)
        # print(df_row[0:1])
        # print(xgb_model.predict(df[cols]))
        index = ctx.triggered_id['index']
        bs = df_bs[index:index+1]['BS'].values[0]
        df_row = df.loc[(df['_BS'] == bs) & (df['Time'].dt.day == mydt.day) & (df['Time'].dt.month == mydt.month) & (df['Time'].dt.year == mydt.year)]
        print(df_row.values[0])
        print(df_row[cols].columns)
        result = xgb_model.predict([df_row[cols].values[0]])
        print(result)
        return f"You clicked on: {bs}", f"The energy consumption of {bs} is: {result[0]}"
    
    return f"Nothing is clicked", f""

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=False)
