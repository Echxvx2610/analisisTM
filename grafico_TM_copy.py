import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import webbrowser
import threading
import logging
import datetime

# Configurar logging
logging.basicConfig(filename='TM_OEE\\Log\\grafico_TM.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def run_dash_app():
    file_path = r'H:\Publico\SMT-Prog-Status\DOWN TIME(Total navico)\TM_SMT_V3.csv'
    df = pd.read_csv(file_path, encoding='latin1')

    # Convertir la columna de fecha al formato datetime
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%m/%d/%Y', errors='coerce')

    # Verificar fecha mínima y máxima
    fecha_minima = df['FECHA'].min().strftime('%m/%d/%Y')
    fecha_maxima = df['FECHA'].max().strftime('%m/%d/%Y')
    
    #print(f'Fecha mínima: {fecha_minima}, Fecha máxima: {fecha_maxima}')

    # Obtener las causas (rango de columnas)
    causas = df.columns[8:-8]
    # Obtener las líneas únicas y ordenarlas de manera descendente
    lineas = sorted(df['LINEA'].unique(), reverse=True)
    #eliminar valor nan
    lineas = lineas[0:4]
    
    # mostrar hora y fecha actual en el dashboard
    hora_actual = pd.Timestamp.now().strftime("%H:%M:%S")
    fecha_actual = pd.Timestamp.now().strftime("%d/%m/%Y")
    logging.info(f'Iniciando el dashboard. Hora actual: {hora_actual}, fecha actual: {fecha_actual}')
        
    # Crear la aplicación Dash
    app = dash.Dash(__name__)

    # Diseñar el layout de la aplicación
    app.layout = html.Div([
        html.Img(src=app.get_asset_url('logo.png'), className='logo'),
        html.H1("DOWN TIME (TOTAL NAVICO)", style={'textAlign': 'center'}),
        html.H3(id='live-update-text', style={'textAlign': 'center'}),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # en milisegundos (1*1000 = 1000 ms = 1 s)
            n_intervals=0
        ),
        html.Div([
            html.Label("Seleccione el rango de fechas:"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df['FECHA'].min().strftime('%m/%d/%Y'),
                end_date=df['FECHA'].max().strftime('%m/%d/%Y'),
                display_format='M/D/YYYY'  # Ajusta el formato aquí
            ),
        ], style={'textAlign': 'left'}),
        html.Div([
            html.Label("Seleccione la línea:"),
            dcc.Dropdown(
                id='linea-dropdown',
                options=[{'label': 'Todas las líneas', 'value': 'all'}] +
                        [{'label': linea, 'value': linea} for linea in lineas],  # Convertir a cadena
                value='all',
                placeholder="Seleccione una línea"
            ),
        ], style={'textAlign': 'left'}),
        html.Br(),
        html.Div([
            html.Label("Seleccione la categoría:"),
            dcc.RadioItems(
                id='categoria-selector',
                options=[
                    {'label': 'Causas Totales', 'value': 'causas'},
                    {'label': 'Subcategorías Generales', 'value': 'subcategorías'}
                ],
                value='causas',
                labelStyle={'display': 'inline-block'}
            ),
        ], style={'textAlign': 'left'}),
        html.Br(),
        html.Div([
            html.Label("Seleccione la unidad de tiempo:"),
            dcc.RadioItems(
                id='unidad-selector',
                options=[
                    {'label': 'Minutos', 'value': 'minutos'},
                    {'label': 'Horas', 'value': 'horas'}
                ],
                value='minutos',
                labelStyle={'display': 'inline-block'}
            ),
        ], style={'textAlign': 'left'}),
        html.Hr(),
        html.H1("Tiempo Total de Fallas", style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='grafico'),
        ], className="graph-container"),
        html.Hr(),
        html.Div([
            html.H1('Tiempos Desglosados por Subcategoría General', style={'textAlign': 'center'}),
            dcc.Graph(id='stacked-grafico', clickData=None),
            html.Hr(),
            html.H1('Detalle de Causas para la Subcategoría Seleccionada', style={'textAlign': 'center'}),
            dcc.Graph(id='detalle-subcategoria-grafico')
        ], style={'textAlign': 'center'}),
        html.Hr(),
        html.Div([
            html.H1('Tendencia Diaria de Contribución por Subcategoría', style={'textAlign': 'center'}),
            dcc.Graph(id='tendencia-grafico', clickData=None),
            html.Hr(),
            html.H1('Detalle de Contribuciones para la Fecha Seleccionada', style={'textAlign': 'center'}),
            dcc.Graph(id='detalle-fecha-grafico'),
            html.Hr(),
            html.H1('Tiempos Desglosados por Causa', style={'textAlign': 'center'}),
            dcc.Graph(id='detalle-causa-grafico')
        ], style={'textAlign': 'center'})
    ])
    @app.callback(
        Output('live-update-text', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_time(n):
        now = datetime.datetime.now()
        return f"Última actualización: {now.strftime('%d/%m/%Y %H:%M:%S')}"

    # Definir la función de actualización del gráfico
    @app.callback(
        Output('grafico', 'figure'),
        [Input('linea-dropdown', 'value'),
         Input('categoria-selector', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('unidad-selector', 'value')]
    )
    def actualizar_grafico(linea, categoria, start_date, end_date, unidad):
        logging.debug(f'Actualizar gráfico: linea={linea}, categoria={categoria}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] >= start_date) & (df['FECHA'] <= end_date)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        if categoria == 'causas':
            datos = df_filtrado[causas].sum().reset_index(name='TIEMPO TOTAL').rename(columns={'index': 'Causa'})
            datos = datos.sort_values(by='TIEMPO TOTAL', ascending=False)
            titulo = 'Tiempo Total de Fallas por Causa'
            etiqueta_eje_x = 'Causa'
            if unidad == 'minutos':
                datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL']
                unidad_tiempo = 'minutos'
            else:
                datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL'] / 60
                unidad_tiempo = 'horas'
        else:
            datos = df_filtrado.groupby('SUBCATEGORIA')['TIEMPO TOTAL'].sum().reset_index()
            if unidad == 'minutos':
                datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL']
                unidad_tiempo = 'minutos'
            else:
                datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL'] / 60
                unidad_tiempo = 'horas'
            datos = datos.sort_values(by='TIEMPO TOTAL', ascending=False)
            titulo = 'Tiempo Total de Fallas por Subcategoría General'
            etiqueta_eje_x = 'SUBCATEGORIA'

        fig = go.Figure([go.Bar(x=datos[etiqueta_eje_x], y=datos['TIEMPO TOTAL'])])
        fig.update_layout(
            title=titulo,
            xaxis_title=etiqueta_eje_x,
            yaxis_title=f'Tiempo Total ({unidad_tiempo})',
            width=1500,
            height=1000
        )
        return fig

    # Definir la función de actualización del gráfico apilado
    @app.callback(
        Output('stacked-grafico', 'figure'),
        [Input('linea-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('unidad-selector', 'value')]
    )
    def actualizar_stacked_grafico(linea, start_date, end_date, unidad):
        logging.debug(f'Actualizar gráfico apilado: linea={linea}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] >= start_date) & (df['FECHA'] <= end_date)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        datos = df_filtrado.groupby('SUBCATEGORIA')[causas].sum().reset_index()

        if unidad == 'minutos':
            datos['TIEMPO TOTAL'] = datos[causas].sum(axis=1)
            unidad_tiempo = 'minutos'
        else:
            datos['TIEMPO TOTAL'] = datos[causas].sum(axis=1) / 60
            unidad_tiempo = 'horas'

        datos = datos.sort_values(by='TIEMPO TOTAL', ascending=False)

        traces = []
        for causa in causas:
            if unidad == 'minutos':
                traces.append(go.Bar(
                    x=datos['SUBCATEGORIA'],
                    y=datos[causa],
                    name=causa
                ))
            else:
                traces.append(go.Bar(
                    x=datos['SUBCATEGORIA'],
                    y=datos[causa] / 60,
                    name=causa
                ))

        fig = go.Figure(data=traces)
        fig.update_layout(
            barmode='stack',
            title='Tiempo Total de Fallas por Subcategoría y Causa',
            xaxis_title='Subcategoría',
            yaxis_title=f'Tiempo Total ({unidad_tiempo})',
            width=1200,
            height=800
        )

        return fig

    # Definir la función de actualización del gráfico de detalle para la subcategoría seleccionada
    @app.callback(
        Output('detalle-subcategoria-grafico', 'figure'),
        [Input('stacked-grafico', 'clickData'),
         Input('linea-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('unidad-selector', 'value')]
    )
    def actualizar_detalle_subcategoria_grafico(clickData, linea, start_date, end_date, unidad):
        if not clickData:
            return go.Figure()  # Devolver una figura vacía si no se selecciona una subcategoría

        subcategoria_seleccionada = clickData['points'][0]['x']
        logging.debug(f'Actualizar subcategoría detalle: linea={linea}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] >= start_date) & (df['FECHA'] <= end_date)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        df_filtrado = df_filtrado[df_filtrado['SUBCATEGORIA'] == subcategoria_seleccionada]

        datos = df_filtrado[causas].sum().reset_index(name='TIEMPO TOTAL').rename(columns={'index': 'Causa'})
        datos = datos[datos['TIEMPO TOTAL'] > 0].sort_values(by='TIEMPO TOTAL', ascending=False)  # Filtrar causas con tiempo total mayor a 0

        if unidad == 'minutos':
            unidad_tiempo = 'minutos'
        else:
            datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL'] / 60
            unidad_tiempo = 'horas'

        fig = go.Figure([go.Bar(x=datos['Causa'], y=datos['TIEMPO TOTAL'])])
        fig.update_layout(
            title=f'Tiempo Total de Fallas para {subcategoria_seleccionada}',
            xaxis_title='Causa',
            yaxis_title=f'Tiempo Total ({unidad_tiempo})',
            width=1200,
            height=800
        )

        return fig

    # Definir la función de actualización del gráfico de tendencia diaria
    @app.callback(
        Output('tendencia-grafico', 'figure'),
        [Input('linea-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('unidad-selector', 'value')]  # Agregar el input de la unidad de tiempo
    )
    def actualizar_tendencia_grafico(linea, start_date, end_date, unidad):
        logging.debug(f'Actualizar gráfico tedencia diaria: linea={linea}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] >= start_date) & (df['FECHA'] <= end_date)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        # Agrupar por fecha y subcategoría, y sumar el tiempo total
        datos = df_filtrado.groupby(['FECHA', 'SUBCATEGORIA'])['TIEMPO TOTAL'].sum().unstack(fill_value=0)

        # Formatear la columna de fechas para que solo muestre el día y la fecha
        datos.index = datos.index.strftime('%d/%m/%Y')

        # Convertir a horas si la unidad seleccionada es 'horas'
        if unidad == 'horas':
            datos = datos / 60

        # Crear trazas para cada subcategoría
        traces = []
        for subcategoria in datos.columns:
            traces.append(go.Bar(
                x=datos.index,
                y=datos[subcategoria],
                name=subcategoria
            ))

        fig = go.Figure(data=traces)
        fig.update_layout(
            barmode='stack',
            title='Tendencia Diaria de Contribución por Subcategoría',
            xaxis_title='Fecha',
            yaxis_title=f'Tiempo Total ({unidad})',  # Usar la unidad seleccionada dinámicamente
            width=1200,
            height=800
        )

        return fig

    # Definir la función de actualización del gráfico de detalle para la fecha seleccionada
    @app.callback(
        Output('detalle-fecha-grafico', 'figure'),
        [Input('tendencia-grafico', 'clickData'),
        Input('linea-dropdown', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('unidad-selector', 'value')]
    )
    def actualizar_detalle_fecha_grafico(clickData, linea, start_date, end_date, unidad):
        if not clickData:
            return go.Figure()  # Devolver una figura vacía si no se selecciona una fecha

        fecha_seleccionada = clickData['points'][0]['x']
        fecha_seleccionada = pd.to_datetime(fecha_seleccionada, format='%d/%m/%Y')
        logging.debug(f'Actualizar gráfico detalle para fecha: linea={linea}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] == fecha_seleccionada)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        datos = df_filtrado.groupby('SUBCATEGORIA')[causas].sum().reset_index()

        if unidad == 'minutos':
            datos['TIEMPO TOTAL'] = datos[causas].sum(axis=1)
            unidad_tiempo = 'minutos'
        else:
            datos['TIEMPO TOTAL'] = datos[causas].sum(axis=1) / 60
            unidad_tiempo = 'horas'

        datos = datos.sort_values(by='TIEMPO TOTAL', ascending=False)

        traces = []
        for causa in causas:
            if unidad == 'minutos':
                traces.append(go.Bar(
                    x=datos['SUBCATEGORIA'],
                    y=datos[causa],
                    name=causa
                ))
            else:
                traces.append(go.Bar(
                    x=datos['SUBCATEGORIA'],
                    y=datos[causa] / 60,
                    name=causa
                ))

        fig = go.Figure(data=traces)
        fig.update_layout(
            barmode='stack',
            title=f'Detalle de Contribuciones para {fecha_seleccionada.strftime("%d/%m/%Y")}',
            xaxis_title='Subcategoría',
            yaxis_title=f'Tiempo Total ({unidad_tiempo})',
            width=1200,
            height=800
        )

        return fig

    # Definir la función de actualización del gráfico de detalle para la causa seleccionada en una fecha específica
    @app.callback(
        Output('detalle-causa-grafico', 'figure'),
        [Input('detalle-fecha-grafico', 'clickData'),
         Input('linea-dropdown', 'value'),
         Input('unidad-selector', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def actualizar_detalle_causa(clickData, linea, unidad, start_date, end_date):
        if not clickData:
            return go.Figure()  # Devolver una figura vacía si no se selecciona una subcategoría

        subcategoria_seleccionada = clickData['points'][0]['x']
        logging.debug(f'Actualizar gráfico detalle causas en una fecha: linea={linea}, start_date={start_date}, end_date={end_date}, unidad={unidad}')
        df_filtrado = df[(df['FECHA'] >= start_date) & (df['FECHA'] <= end_date)]
        if linea != 'all':
            df_filtrado = df_filtrado[df_filtrado['LINEA'] == linea]

        df_filtrado = df_filtrado[df_filtrado['SUBCATEGORIA'] == subcategoria_seleccionada]

        datos = df_filtrado[causas].sum().reset_index(name='TIEMPO TOTAL').rename(columns={'index': 'Causa'})
        datos = datos[datos['TIEMPO TOTAL'] > 0].sort_values(by='TIEMPO TOTAL', ascending=False)  # Filtrar causas con tiempo total mayor a 0

        if unidad == 'minutos':
            unidad_tiempo = 'minutos'
        else:
            datos['TIEMPO TOTAL'] = datos['TIEMPO TOTAL'] / 60
            unidad_tiempo = 'horas'

        fig = go.Figure([go.Bar(x=datos['Causa'], y=datos['TIEMPO TOTAL'])])
        fig.update_layout(
            title=f'Tiempo Total de Fallas para {subcategoria_seleccionada}',
            xaxis_title='Causa',
            yaxis_title=f'Tiempo Total ({unidad_tiempo})',
            width=1200,
            height=800
        )

        return fig

    
    # Ejecutar la aplicación Dash
    app.run_server(port=8000,debug=True)  # Cambiar debug=True a debug=False
    

if __name__ == '__main__':
    run_dash_app()    