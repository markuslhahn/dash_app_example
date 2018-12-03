
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

df = pd.read_csv("/Users/markushahn/Dropbox/02 ESADE/04 Cloud Computing/CC 7/nama_10_gdp_1_Data.csv")

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
#### Markus L Hahn Final Project

### Graph 1: Measure Scatterplot
'''

markdown_text2 = '''

### Graph 2: Country Measure Timeline
'''

markdown_text3 = '''

Actual footage of me when the code finally worked:

![Image](https://media.giphy.com/media/102h4wsmCG2s12/giphy.gif)
'''

app.layout = html.Div([
    
    html.Div([
    dcc.Markdown(children=markdown_text)
    ]),
    
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            )
        ],
        style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Final consumption expenditure'
            )
        ],
        style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.RadioItems(
                id='unit1',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )              
        ],
        style={'width': '100%', 'display': 'inline-block'}),

    ]),
    
    dcc.Graph(id='1-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

    html.Div([
    dcc.Markdown(children=markdown_text2)
    ]),
    
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='2xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            ),
        ],
        style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='2yaxis-column',
                options=[{'label': i, 'value': i} for i in countries],
                value='France'
            ),
        ],
        style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )            
        ],
        style={'width': '100%', 'display': 'inline-block'}),

    ]),
    
    dcc.Graph(id='2-graphic'),
    
    html.Div([
    dcc.Markdown(children=markdown_text3)
    ]),   

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
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'color': 'red',
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 60, 'b': 60, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('2-graphic', 'figure'),
    [dash.dependencies.Input('2xaxis-column', 'value'),
     dash.dependencies.Input('2yaxis-column', 'value'),
     dash.dependencies.Input('unit', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name, unit):
    
    dff = df[(df['GEO'] == yaxis_column_name) & (df['UNIT'] == unit)]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='lines+markers',
            marker={
                'size': 10,
                'color': 'white',
                'line': {'width': 1, 'color': 'red'}
            },
            line=dict(shape='spline', color = ('red'), width = 6)
        )],
        'layout': go.Layout(
            
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 60, 'b': 60, 't': 40, 'r': 40},
            hovermode='closest'
            
        )
    }

if __name__ == '__main__':
    app.run_server()

