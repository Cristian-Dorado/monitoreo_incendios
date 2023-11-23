
# %%
import pandas as pd
import requests
from io import StringIO
from datetime import datetime

# %%
#consulta a la API de datos de SUD America
api_url_S_America = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/b6ffa785ddbf642d8d1dc54fe8fbb815/MODIS_NRT/-85,-57,-32,14/7"
response_S_Amarica = requests.get(api_url_S_America)

# %%
#Confitmacion de consulta y guardado de data en dataframe
if response_S_Amarica.status_code == 200:
    csv_data_bol = response_S_Amarica.text
    df_S_America = pd.read_csv(StringIO(csv_data_bol))

# %%
# Consulta API de datos de Bolivia
api_url_Bolivia = "https://firms.modaps.eosdis.nasa.gov/api/country/csv/b6ffa785ddbf642d8d1dc54fe8fbb815/MODIS_NRT/BOL/7"
response_Bolivia = requests.get(api_url_Bolivia)

# %%
#Confitmacion de consulta y guardado de data en dataframe
if response_Bolivia.status_code == 200:
    csv_data_bol = response_Bolivia.text
    df_Bolivia = pd.read_csv(StringIO(csv_data_bol))

# %%
#TOKEN PARA MAPBOX
token_mapbox = "pk.eyJ1IjoiY3Jpc3RpYW5vMTVjaWJlcm5ldGljYSIsImEiOiJjbGZ5ZXU1czcwbWJyM2VwNmRqcmFleWtiIn0.muQ0uhC2uSnawbOijnXlMQ"

# %% [markdown]
# Exploracion de data

# %%
# Dar nuevos nombres a las columnas
df_S_America = df_S_America.rename(columns={"brightness":"Brillo_21(Kelvin)","scan":"Escaneo",
                             "track":"Tamaño_Pixel","acq_date":"Fecha_adquisicion",
                             "acq_time":"Hora_adquisicion","satellite":"Satelite",
                             "instrument":"Instrumento","confidence":"Confianza(%)",
                             "version":"Version","bright_t31":"Brillo(kelvin)",
                             "frp":"Potencia_Radiativa(MW)","daynight":"Dia_Noche"})

# %%
df_Bolivia = df_Bolivia.rename(columns={"brightness":"Brillo_21(Kelvin)","scan":"Escaneo",
                             "track":"Tamaño_Pixel","acq_date":"Fecha_adquisicion",
                             "acq_time":"Hora_adquisicion","satellite":"Satelite",
                             "instrument":"Instrumento","confidence":"Confianza(%)",
                             "version":"Version","bright_t31":"Brillo(kelvin)",
                             "frp":"Potencia_Radiativa(MW)","daynight":"Dia_Noche"})

# %%
df_S_America["Adq_Fecha_Hora"] = pd.to_datetime(df_S_America["Fecha_adquisicion"] + " " + df_S_America["Hora_adquisicion"].
               astype(str).str.zfill(4), format="%Y-%m-%d %H%M")

# %%
df_Bolivia["Adq_Fecha_Hora"] = pd.to_datetime(df_Bolivia["Fecha_adquisicion"] + " " + df_Bolivia["Hora_adquisicion"].
               astype(str).str.zfill(4), format="%Y-%m-%d %H%M")

# %%
df_S_America["Hora_adquisicion"] = df_S_America["Adq_Fecha_Hora"].dt.time

# %%
df_Bolivia["Hora_adquisicion"] = df_Bolivia["Adq_Fecha_Hora"].dt.time

# %%
#Importación de librerias necesarias para el Tablero
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

# Inicializa data_frame_dat como None
data_frame_dat = None

#llamado de la aplicacion Dash
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SUPERHERO],
           title="Monitoreo de Incendios")

#Implementacion del menu desplegable
dropdown_menu = dbc.DropdownMenu(
            label=[
                        html.Img(
                            src="./assets/house-fill.svg",  # Ruta de tu imagen SVG
                            style={'width': '25px', 'height': '25px'},  # Ajusta el tamaño de la imagen
                        ),
                        
                    ],
            children=[
                dbc.DropdownMenuItem(
                    "NASA-MODIS", href="https://modis.gsfc.nasa.gov/sci_team/"
                ),
                dbc.DropdownMenuItem(
                    "Origen de Data", href="https://firms.modaps.eosdis.nasa.gov/api/area/csv/b6ffa785ddbf642d8d1dc54fe8fbb815/MODIS_NRT/-85,-57,-32,14/7"
                ),
                dbc.DropdownMenuItem(
                    "GitHub", href="https://github.com/Cristian-Dorado"
                ),
                dbc.DropdownMenuItem(
                    "Contáctanos",
                    href="https://www.linkedin.com/in/cristian-dorado/",
                    #external_link=True,
                ),
            ],
            align_end=True, className="my-custom-dropdown"
        )
 
#Implementacion de Tarjeta 
controls = dbc.Card(
    dbc.CardBody(
        [
            dcc.Markdown("Información de MODIS(Aqua y Terra) de la NASA", className="card-title"),
            dcc.Dropdown(
                [{'label': 'América del Sur', 'value': 'df_S_America'},
                 {'label': 'Bolivia', 'value': 'df_Bolivia'}
                 ], value='df_S_America', clearable=False, id='control_data_lugar',style={"color": "black"}
            ),
            dcc.RadioItems(id='cont-radioitem-dias', labelStyle={'display': 'inline-block','font-size':15},
                                        style={'margin-right': '30px', 'font-size': 30},
                                        options=[
                                            {'label': ' HOY', 'value': 'Hoy'},
                                            {'label': ' Ultimos 7 Días', 'value': '3_dias'}
                                        ], value='Hoy' ),
            dcc.Markdown(id="output-result-total"),
            html.Div(
                dcc.Graph(id='graf-scater-fecha',figure= {})
            )
        ]
    ),
    className="w-100 mb-3",
)

#Implementacion del Contenedos de la app_layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("MONITOREO DE INCENDIOS"),md=11),
                dbc.Col(dropdown_menu,md=1 )
            ],style={'margin-bottom': '5px','margin-top': '5px'}  # Ajusta el margen inferior de dbc.Row
        ),
            
        html.Hr(style={'margin-top': '5px', 'margin-bottom': '5px'}),

        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(
                    [
                        dcc.RadioItems(id='map-radioitems', labelStyle={'display': 'inline-block'},
                                        style={'margin-left': 'auto'},
                                        options=[
                                            {'label': 'Modo Oscuro', 'value': 'dark'},
                                            {'label': 'Modo Satelital', 'value': 'satellite-streets'}
                                        ], value='dark'),
                        dcc.Graph(id='grafic-map',figure= {})
                    ], md=8,
                ),
            ],
        ),
    ],
    fluid=True,
)

#configuracion del callback del Mapa
@app.callback(
    Output('grafic-map', 'figure'),
    [Input('map-radioitems', 'value'),
     Input('control_data_lugar', 'value'),
     Input('cont-radioitem-dias','value')]
)
def update_map(value, data_location, selected_days):
    global data_frame_dat  # Hacer la variable global

    S_america_center_map = dict(
        lat=-19.802826271524722,
        lon=-63.18244305251598
        )
                
    Bol_center_map = dict(
        lat=-16.43010,
        lon=-64.88386
        )
    
    S_america_zoom = 2.7
    Bol_zoom = 4.9
    try:
        mapbox_style_dat = 'dark' if value == 'dark' else 'satellite-streets'
        data_frame_dat = df_S_America if data_location == 'df_S_America' else df_Bolivia
        center_dat = S_america_center_map if data_location == "df_S_America" else Bol_center_map
        zoom_dat = S_america_zoom if data_location == "df_S_America" else Bol_zoom

        #Filtrado para el elegir el Dia 
        if selected_days == "Hoy":
            fecha_actual = datetime.now().date()
            data_frame_dat = data_frame_dat[data_frame_dat['Adq_Fecha_Hora'].dt.date == fecha_actual]
            
        #Dibujar en Mapa
        fig_map = px.scatter_mapbox(
            data_frame=data_frame_dat,
            lat="latitude",
            lon="longitude",
            hover_name="Brillo(kelvin)",
            hover_data=["Fecha_adquisicion","Hora_adquisicion", "Satelite","Confianza(%)","Potencia_Radiativa(MW)"],
            zoom=zoom_dat,
            #size = 8,
            #symbol = 'square',
            color="Brillo(kelvin)",
            color_continuous_scale="YlOrRd",
            mapbox_style=mapbox_style_dat, # Configura el estilo del mapa directamente
            #width=800,
            height=600,

        )
      
        
    
        fig_map.update_layout(
        mapbox_accesstoken=token_mapbox,
        coloraxis_colorbar=dict(xanchor="right", x=1, tickfont=dict(color='white'), title_font=dict(color='white')),
        showlegend=False,
        autosize= True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox=dict(
            center=center_dat
            ),
        )
        return fig_map
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

#Configuracion del callback del resultado de totales
@app.callback(
    Output('output-result-total', 'children'),
    [Input('grafic-map', 'figure')]
)
def update_total_data(figure):
    global data_frame_dat  # Hacer la variable global

    if data_frame_dat is not None:
        return "Cantidad de Incendios: **{:,d}**".format(
            len(data_frame_dat)
        )
    else:
        return "No hay datos para mostrar"

#Programacion del grafico del Historico por fecha
@app.callback(
    Output('graf-scater-fecha', 'figure'),
    [Input('control_data_lugar', 'value')]
)

def update_graf_fecha(data_location):
    #global data_frame_dat  # Hacer la variable global
    
    try:
        data_frame_dat = df_S_America if data_location == 'df_S_America' else df_Bolivia
        # Verificar que data_frame_dat no sea None y tenga la columna 'Fecha_adquisicion'
        if data_frame_dat is not None and 'Fecha_adquisicion' in data_frame_dat.columns:
            # Calcular la cantidad por fecha
            counts_por_fecha = data_frame_dat['Fecha_adquisicion'].value_counts().sort_index()

            # Configuración del estilo del gráfico
            template = "seaborn"
            
            # Crear el gráfico de dispersión (scatter plot)
            fig_fech = px.line(
                x=counts_por_fecha.index,
                y=counts_por_fecha.values,
                labels={'x': 'Fechas', 'y': 'Incendios'},
                title='Histórico',
                markers=True,
                text= counts_por_fecha.values,
                line_shape='linear',  # Puedes ajustar la forma de la línea según tus preferencias
            )
             
            fig_fech.update_traces(textposition = "top center", line_color='orange')

            fig_fech.update_layout(
                title=dict(text='Histórico', y=0.97, x=0.5, xanchor='center', yanchor='top', font=dict(size=20, family='Arial', color='black')),
                template=template,  # Aplicar el estilo del gráfico
                margin=dict(l=0, r=0, t=50, b=0),  # Reducir los márgenes del gráfico
            )
            return fig_fech

        else:
            return px.line()  # Gráfico vacío si no hay datos o la columna 'Fecha_adquisicion' no existe

    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)


# %%



