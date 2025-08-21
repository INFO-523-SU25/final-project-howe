from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

agg_crimes = pd.read_csv("data/aggregated_mexi_crime.csv")
app = Dash()
 
app.layout = html.Div([ #layout of the Dash app
    html.H1(children='Crimes in Mexico (2015-2023)', style={'textAlign':'center'}), #title 
    
    html.Div([ # first drop down for state selection
        html.Label('Select State:'),
        dcc.Dropdown(
            id='dropdown-categoryA',
            options=[{'label': i, 'value': i} for i in agg_crimes['entity'].unique()],
            value=agg_crimes['entity'].unique()[0],  # Default to the first entity
            clearable=False
        ),
    ]),  
    
    html.Div([ # second drop down for crime type selection
        html.Label('Select Crime Type:'),     
        dcc.Dropdown(
            id='dropdown-categoryB',
            options=[{'label': i, 'value': i} for i in agg_crimes['type_of_crime'].unique()],
            value=agg_crimes['type_of_crime'].unique()[0],  # Default to the first subtype
            clearable =False
        ),
    ]), 
    dcc.Graph(id='line-graph')  
])
    
    
@app.callback( #callback to update the graph based on selected state and crime type
    Output('line-graph', 'figure'),
    [Input('dropdown-categoryA', 'value'),  
     Input('dropdown-categoryB', 'value')]  
)
def update_graph(selected_categoryA, selected_categoryB): # graph update function
    #filter the DataFrame based on selected state and crime type
    filtered_df = agg_crimes[(agg_crimes['entity'] == selected_categoryA) & (agg_crimes['type_of_crime'] == selected_categoryB)]
    
    fig = px.line(filtered_df, x='year', y='count', title=f'Crime Counts for {selected_categoryA}, {selected_categoryB}') #create line graph
    fig.update_layout(template="plotly_dark") #modfy graph appearance to dark mode
    return fig
    

    
if __name__ == '__main__':
    app.run(debug=True)

