# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

# funkcija atzymom skirtom slider bar


def atzymos(min, max):
    marks = {}
    for i in range(min, max+1):
        marks[i] = str(i)
    return marks


# grazina miesto, tipo... label pagal value
def gauti_pav(data, ieskomas):
    for i in data:
        if i.get('value') == ieskomas:
            return i.get('label')


def tipai():
    return [
        {'label': 'Didžiausia temperatūra (C)', 'value': 'maxtempC'},
        {'label': 'Mažiausia temperatūra (C)', 'value': 'mintempC'},
        {'label': 'Sniegas (cm)', 'value': 'totalSnow_cm'},
        {'label': 'Saulėtos valandos', 'value': 'sunHour'},
        {'label': 'Mėnulio apšvietimas', 'value': 'moon_illumination'},
        {'label': 'Mėnesiena', 'value': 'moonrise'},
        {'label': 'Mėnulio leidimasis', 'value': 'moonset'},
        {'label': 'Saulėtekis', 'value': 'sunrise'},
        {'label': 'Saulėlydis', 'value': 'sunset'},
        {'label': 'Rasos taškas (c)', 'value': 'DewPointC'},
        {'label': 'Vėjo šaltis (c)', 'value': 'WindChillC'},
        {'label': 'Vėjo gūsis (km/h)', 'value': 'WindGustKmph'},
        {'label': 'Debesuotumas', 'value': 'cloudcover'},
        {'label': 'Drėgmė', 'value': 'humidity'},
        {'label': 'Slėgis', 'value': 'pressure'},
        {'label': 'Matomumas', 'value': 'visibility'},
        {'label': 'Vėjos greitis (km/h)', 'value': 'windspeedKmph'},
        {'label': 'Šilumos indeksas', 'value': 'HeatIndexC'}
    ]


def menesiai():
    return [
        {'label': 'Sausis', 'value': 'sausis'},
        {'label': 'Vasaris', 'value': 'vasaris'},
        {'label': 'Kovas', 'value': 'kovas'},
        {'label': 'Balandis', 'value': 'balandis'},
        {'label': 'Gegužė', 'value': 'geguze'},
        {'label': 'Birželis', 'value': 'birzelis'},
        {'label': 'Liepa', 'value': 'liepa'},
        {'label': 'Rugpjūtis', 'value': 'rugpjutis'},
        {'label': 'Rugsėjis', 'value': 'rugsejis'},
        {'label': 'Spalis', 'value': 'spalis'},
        {'label': 'Lapkritis', 'value': 'lapkritis'},
        {'label': 'Gruodis', 'value': 'gruodis'}
    ]


def menesiu_zymos():
    return {
        'sausis': ['-01-00', '-02-00'],
        'vasaris': ['-02-00', '-03-00'],
        'kovas': ['-03-00', '-04-00'],
        'balandis': ['-04-00', '-05-00'],
        'geguze': ['-05-00', '-06-00'],
        'birzelis': ['-06-00', '-07-00'],
        'liepa': ['-07-00', '-08-00'],
        'rugpjutis': ['-08-00', '-09-00'],
        'rugsejis': ['-09-00', '-10-00'],
        'spalis': ['-10-00', '-11-00'],
        'lapkritis': ['-11-00', '-12-00'],
        'gruodis': ['-12-00', '-12-31']
    }


def miestai():
    return [
        {'label': 'Vilnius', 'value': 'vilnius'},
        {'label': 'Kaunas', 'value': 'kaunas'},
        {'label': 'Palanga', 'value': 'palanga'},

    ]


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Tabs(id='tabai', value='vizua', children=[
        dcc.Tab(label='Vizualiacija', value='vizua'),
        dcc.Tab(label='Duomenys', value='duom'),
    ]),
    html.Div(id='rodymas')
])

# callbackas skirtas pereiti tarp vizualiacijos ir duomenu skilciu


@app.callback(Output('rodymas', 'children'),
              [Input('tabai', 'value')])
def rodyti(tab):
    # vizualizacijos skiltis
    if tab == 'vizua':
        return html.Div([
            dcc.Dropdown(
                id='menuo',
                options=menesiai(),
                value='sausis'
            ),
            dcc.Dropdown(
                id='tipas',
                options=tipai(),
                value='maxtempC'
            ),
            dcc.Dropdown(
                id='miestas',
                options=miestai(),
                value='kaunas'
            ),
            dcc.Dropdown(
                id='grafiko_tipas',
                options=[
                    {'label': 'Juostas', 'value': 'bar'},
                    {'label': 'Linija', 'value': 'line'}
                ],
                value='line'

            ),
            dcc.RangeSlider(
                id='slider_metai',
                min=2010,
                max=2019,
                step=1,
                marks=atzymos(2010, 2019),
                value=[2010, 2019]
            ),
            html.Div(id='grafikas')

        ])
    # duomenu skiltis
    elif tab == 'duom':
        return html.Div([
            dcc.Dropdown(
                id='duomenu_miestas',
                options=miestai(),
                value='vilnius'

            ),
            html.Div(id='duomenu_vaizdavimas')
        ])

# callbackas skirtas atvaizduoti duomenis pagal pasirinkta miesta


@app.callback(
    Output(component_id='duomenu_vaizdavimas', component_property='children'),
    [Input(component_id='duomenu_miestas', component_property='value')]
)
def lenta_duomenu(miestas):
    df = pd.read_csv(
        'https://raw.githubusercontent.com/yellowishcarpet/weather-data-visualization/master/'+miestas + '.csv')
    return dash_table.DataTable(
        id='duomenys',
        columns=[{"name": i, "id": i, "deletable": True, }
                 for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
    )


# callbackas skirtas vizualizuoti informacija pagal pasirinktus parametrus vizualiacijos skiltyje
@app.callback(
    Output(component_id='grafikas', component_property='children'),
    [Input(component_id='menuo', component_property='value'),
     Input('tipas', 'value'),
     Input('miestas', 'value'),
     Input('grafiko_tipas', 'value'),
     Input('slider_metai', 'value'),
     ]
)
def atnaujinti_grafika(menuo, tipas, miestas, grafiko_tipas, slider_metai,):
    menesis = menesiu_zymos()
    df = pd.read_csv(
        'https://raw.githubusercontent.com/yellowishcarpet/weather-data-visualization/master/'+str(miestas) + '.csv')
    m = menesis[menuo]
    datos = df[df['date_time'].between('2016'+m[0], '2016'+m[1])]
    d_menesiai = [i[-2:] for i in datos.date_time]
    visa = []
    for metai in range(slider_metai[0], slider_metai[1]+1):
        metai = str(metai)
        temp = [i for i in df[df['date_time'].between(
            metai+m[0], metai+m[1])][tipas]]
        visa.append({'x': d_menesiai, 'y': temp,
                    'type': grafiko_tipas, 'name': metai})
    return dcc.Graph(
        id='grafikas_v',
        figure={
            'data': visa,
            'layout': {
                'title': gauti_pav(tipai(), tipas) + ", " + gauti_pav(miestai(), miestas) + ", " + gauti_pav(menesiai(), menuo)
            }
        }
    )


if __name__ == "__main__":
    app.run_server(debug=False)
