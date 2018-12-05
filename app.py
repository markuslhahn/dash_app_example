
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("nama_10_gdp_1_Data.csv")

df = df.drop(columns=['Flag and Footnotes'])

df = df[df.GEO!= 'European Union (current composition)']
df = df[df.GEO!= 'European Union (without United Kingdom)']
df = df[df.GEO!= 'European Union (15 countries)']
df = df[df.GEO!= 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)']
df = df[df.GEO!= 'Euro area (19 countries)']
df = df[df.GEO!= 'Euro area (12 countries)']
df = df[df.Value != ':']

countries = df['GEO'].unique()
years = df['TIME'].unique()
units = df['UNIT'].unique()
items = df['NA_ITEM'].unique()

markdown_text = '''
![Image](https://www.migueldiaz.com/images/clientes/esade.png)
'''

markdown_text3 = '''

Actual footage of me when the code finally worked:

![Image](https://media.giphy.com/media/102h4wsmCG2s12/giphy.gif)
'''

app.layout = html.Div([
    
    html.Div([
    dcc.Markdown(children=markdown_text)
    ],
    style ={"float":"right",'marginTop':20}),
    
    html.H2("Markus L Hahn: Final Assignment", style ={"textAlign":"left","color": "RGB(168, 27, 25)"}),
    html.H4("Cloud Computing, 03.12.2018", style ={"textAlign":"left","color": "RGB(168, 27, 25)"}),
    html.H3("Graph 1: Relative Measures", style ={"textAlign":"center","color": "RGB(232, 38, 34)",'marginBottom': 20, 'marginTop':20}),
    
    html.Div([
        html.Div([
            html.Label('Pick an indicator for the x-axis',style={'width': '100%', 'display': 'inline-block',"textAlign":"center"}),            
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            )
        ],
        style={"float":"left","textAlign":"center",'width': '35%', 'display': 'inline-block',"padding-left":100}),
        
        html.Div([
            html.Label('Pick an indicator for the y-axis',style={'width': '100%', 'display': 'inline-block',"textAlign":"center"}),            
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Final consumption expenditure'
            )
        ],
        style={"float":"right","textAlign":"center",'width': '35%', 'display': 'inline-block',"padding-right":100}),
        
        html.Div([
            html.Label('Pick a unit',style={'width': '100%', 'display': 'inline-block',"textAlign":"center"}),
            dcc.RadioItems(
                id='unit1',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'},
            style={"textAlign":"center"}
            )              
        ],
        style={'width': '100%', 'display': 'inline-block', "padding-top":10, "padding-bottom":20}),

    ],style={'width': '100%', 'display': 'inline-block'}
    
    ),
    
    
    dcc.Graph(id='1-graphic', animate="True", hoverData={'points': [{'customdata': 'Belgium'}]}),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

    html.H3("Graph 2: Country Measure Timeline", style ={"textAlign":"center","color": 'RGB(8, 108, 181)','marginBottom': 20, 'marginTop':50}),

    html.H5("Hover over the markers in the first graph to manipulate this graph", style ={"textAlign":"center","color": 'RGB(15, 96, 156)'}),

    html.Div([

        html.Div([
            html.Label('Pick an indicator for the y-axis',style={'width': '100%', 'display': 'inline-block',"textAlign":"center"}),            
            dcc.Dropdown(
                id='2xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            )
        ],
        style={'width': '35%', 'display': 'inline-block', "padding":20}),

        html.Div([
            html.Label('Pick a unit',style={'width': '100%', 'display': 'inline-block',"textAlign":"center"}),
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'},
            style={"textAlign":"center"}
            )            
        ],
        style={'width': '100%', 'display': 'inline-block', "padding-left":10, "padding-right":20}),

    ],
    style={"text-align":"center"}
    ),
       
    dcc.Graph(id='2-graphic'),
    
    html.Div([
    dcc.Markdown(children=markdown_text3)
    ],style={"textAlign":"center"}),

])

@app.callback(
    dash.dependencies.Output('1-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name, unit,
                 year_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit)]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name)&(dff['GEO']==i)]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name)&(dff['GEO']==i)]['Value'],
            text=dff[(dff['NA_ITEM'] == yaxis_column_name)&(dff['GEO']==i)]['GEO'],
            customdata=dff[(dff['NA_ITEM'] == yaxis_column_name)&(dff['GEO']==i)]['GEO'],            
            mode='markers',
            hoveron=("points"),
            hoverinfo=("text+y+x"),
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i[:15])
                 for i in df.GEO.unique()
        ],
        'layout': go.Layout(
            
            xaxis={
                'title': '<b>{}</b>'.format(xaxis_column_name)
            },
            yaxis={
                'title': '<b>{}</b>'.format(yaxis_column_name)
            },
            margin={'l': 100, 'b': 60, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }


@app.callback(
    dash.dependencies.Output('2-graphic', 'figure'),
    [dash.dependencies.Input('2xaxis-column', 'value'),
     dash.dependencies.Input('1-graphic', 'hoverData'),
     dash.dependencies.Input('unit', 'value')])

def update_graph(xaxis_column_name, hoverData, unit):
    
    country_name = hoverData['points'][0]['customdata']
    dff = df[(df['GEO'] == country_name) & (df['UNIT'] == unit)]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == country_name]['GEO'],
            mode='lines+markers',
            marker={
                'size': 11,
                'color': 'white',
                'line': {'width': 3, 'color': 'RGB(8, 108, 181)'}
            },
            line=dict(shape='spline', color = ('RGB(8, 108, 181)'), width = 6)
        )],
        'layout': go.Layout(
            xaxis={
                'title': "Year",'showgrid': False
            },
            yaxis={
                'title': '<b>{}</b><br><b>{}</b>'.format(country_name, xaxis_column_name)
            },
            margin={'l': 100, 'b': 60, 't': 40, 'r': 40},
            hovermode='closest'

            
        )
    }

if __name__ == '__main__':
    app.run_server()

