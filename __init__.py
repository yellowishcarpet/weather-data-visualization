import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import plotly.graph_objects as go
import requests
import json
from pytz import timezone
from datetime import datetime, timedelta, date

# funkcija atzymom skirtom slider bar


def convert_tipas(duomenys):
    tvarkingi = []
    for i in range(len(duomenys)):
        eile = []
        for j in range(6):
            eile.append(heatmap_condition_tipai(duomenys[i][j]))
        tvarkingi.append(eile)
    return tvarkingi


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


def dataLietuvos(data):
    f = "%Y-%m-%d %H:%M:%S"
    dataUtc = datetime.strptime(data, f)
    dataUtc = timezone('UTC').localize(dataUtc)
    dataLTU = dataUtc.astimezone(timezone('Europe/Vilnius')).strftime(f)
    return dataLTU


def paskutinis_atnaujinimas(miestas):
    adr = 'https://api.meteo.lt/v1/places/'+miestas+'/forecasts/long-term'
    response = requests.get(adr)
    info = json.loads(response.content.decode("utf-8"))
    stringas = "Paskutinį kartą atnaujinta: " + \
        str(dataLietuvos(info['forecastCreationTimeUtc'])) + ","
    i = 0
    siandien = str(datetime.now())[:10]
    valandos = []
    duomenys = []
    kita = []
    while siandien == dataLietuvos(info['forecastTimestamps'][i]['forecastTimeUtc'])[:10]:
        valandos.append(dataLietuvos(
            info['forecastTimestamps'][i]['forecastTimeUtc'])[11:])
        i = i+1
    for j in range(len(valandos)):
        duomenys.append(info['forecastTimestamps'][j]['airTemperature'])
    dar = " "+miestas.capitalize()+', Šiandien vidutinė temperatūra: ' + \
        str(round(sum(duomenys)/len(duomenys), 2)) + " C"
    stringas = stringas + " " + dar
    return stringas


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


def heatmap_condition_tipai(tipas):
    vertes = {
        'clear': 1,
        'isolated-clouds': 2,
        'scattered-clouds': 3,
        'overcast': 4,
        'light-rain': 5,
        'moderate-rain': 6,
        'heavy-rain': 7,
        'sleet': 8,
        'fog': 9,
        'na': 10,
    }
    return vertes.get(tipas)


def heatmap_tipai():
    return [
        {'label': 'Oro temperatūra', 'value': 'airTemperature'},
        {'label': 'Vėjo greitis', 'value': 'windSpeed'},
        {'label': 'Vėjo gūsis', 'value': 'windGust'},
        {'label': 'Vėjo kryptis', 'value': 'windDirection'},
        {'label': 'Debesuotumas', 'value': 'cloudCover'},
        {'label': 'Santykinė drėgmė', 'value': 'relativeHumidity'},
        {'label': 'Viso krituliu', 'value': 'totalPrecipitation'},
        {'label': 'Kondicija', 'value': 'conditionCode'},
    ]


def miestai():
    return [
        {'label': 'Vilnius', 'value': 'vilnius'},
        {'label': 'Kaunas', 'value': 'kaunas'},
        {'label': 'Palanga', 'value': 'palanga'},

    ]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Tabs(id='tabai', value='vizua', children=[
        dcc.Tab(label='Istoriniai duomenys', value='vizua'),
        dcc.Tab(label='Duomenys', value='duom'),
        dcc.Tab(label='Prognozės', value='dabar'),
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
    elif tab == 'dabar':

        return html.Div([
            html.Div(id='papildoma_informacija'),
            dcc.Dropdown(
                id='heatmapas_miestas',
                options=miestai(),
                value='vilnius'
            ),
            dcc.Dropdown(
                id='heatmapas_tipas',
                options=heatmap_tipai(),
                value='airTemperature'
            ),
            html.Div(id='heatmapas_siandiena'),
            html.Div(id='heatmapas')
        ])


@app.callback(
    Output(component_id='papildoma_informacija',
           component_property='children'),
    [Input(component_id='heatmapas_miestas', component_property='value')]
)
def naujiena(miestas):
    stringas = paskutinis_atnaujinimas(miestas)
    return html.H3(children=stringas)


@app.callback(
    Output(component_id='heatmapas_siandiena', component_property='children'),
    [Input(component_id='heatmapas_miestas', component_property='value'),
        Input('heatmapas_tipas', 'value'),
     ]
)
def informacija_siandien(miestas, tipas):
    i = 0
    adr = 'https://api.meteo.lt/v1/places/'+miestas+'/forecasts/long-term'
    response = requests.get(adr)
    info = json.loads(response.content.decode("utf-8"))
    siandien = str(datetime.now())[:10]
    valandos = []
    kita = []
    duomenys = []
    spalvos = [[0, 'rgb(253,132,132)'], [1, 'rgb(255,0,0)']]
    while siandien == dataLietuvos(info['forecastTimestamps'][i]['forecastTimeUtc'])[:10]:
        valandos.append(dataLietuvos(
            info['forecastTimestamps'][i]['forecastTimeUtc'])[11:])
        i = i+1
    for j in range(len(valandos)):
        duomenys.append(info['forecastTimestamps'][j][tipas])
    if tipas == 'conditionCode':
        spalvos = [[0, 'rgb(209,250,255)'], [1, 'rgb(27,144,162)']]
        for g in range(len(duomenys)):
            duomenys[g] = heatmap_condition_tipai(duomenys[g])
    print(duomenys)
    fig = go.Figure(
        data=go.Heatmap(
            z=[duomenys],
            x=valandos,
            y=[siandien[5:]],
            colorscale=spalvos,
        ),
        layout={'title': 'Šiandienos informacija',
                'xaxis': {
                    'title': 'Valandos'
                },
                'yaxis': {
                    'title': 'Dienos'
                }
                }
    )
    return dcc.Graph(figure=fig)


@app.callback(
    Output(component_id='heatmapas', component_property='children'),
    [Input(component_id='heatmapas_miestas', component_property='value'),
        Input('heatmapas_tipas', 'value'),
     ]
)
def informacija(miestas, tipas):
    galimos = ['00:00:00', '03:00:00', '06:00:00',
               '09:00:00', '12:00:00', '18:00:00']
    adr = 'https://api.meteo.lt/v1/places/'+miestas+'/forecasts/long-term'
    response = requests.get(adr)
    info = json.loads(response.content.decode("utf-8"))
    reiksmes = []
    siandien = datetime.now()
    i = 0
    datos = []
    spalvos = [[0, 'rgb(253,132,132)'], [1, 'rgb(255,0,0)']]
    galimos = ['00:00:00', '03:00:00', '06:00:00',
               '09:00:00', '12:00:00', '18:00:00']
    for j in range(1, 6):
        viskas = []
        ryt = str(siandien + timedelta(j))[:10]
        datos.append(str(siandien + timedelta(j))[:10][5:])
        while len(viskas) < 6:
            if ryt == info['forecastTimestamps'][i]['forecastTimeUtc'][:10]:
                if info['forecastTimestamps'][i]['forecastTimeUtc'][11:] in galimos:
                    viskas.append(info['forecastTimestamps'][i][tipas])
            i = i+1
        reiksmes.append(viskas)
    if tipas == 'conditionCode':
        spalvos = [[0, 'rgb(209,250,255)'], [1, 'rgb(27,144,162)']]
        reiksmes = convert_tipas(reiksmes)
    metai_sie = str(date.today().year)+"-"
    for i in range(len(datos)):
        datos[i] = metai_sie + datos[i]
    fig = go.Figure(
        data=go.Heatmap(
            z=reiksmes,
            x=['03:00:00', '06:00:00', '09:00:00',
               '12:00:00', '15:00:00', '21:00:00'],
            y=datos,
            colorscale=spalvos,
            hoverongaps=False),
        layout={'title': 'Kitų dienų informacija',
                'xaxis': {
                    'title': 'Valandos'
                },
                'yaxis': {
                    'title': 'Dienos'
                }
                },
    )
    return dcc.Graph(figure=fig,)
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


server = app.server
if __name__ == "__main__":
    app.run_server(debug=False)
