import dash
from dash import Dash, dcc, html, Input, Output,callback, State, ctx
from dash.exceptions import PreventUpdate
import Visualisation
old_df = 'a'
variable_position = [Visualisation.keeper_keys.drop('player'), Visualisation.defender_keys.drop('player'),
                     Visualisation.midfielder_keys.drop('player'), Visualisation.attacker_keys.drop('player')]
variable_players = [Visualisation.keeper_players, Visualisation.defender_players, Visualisation.midfielder_players,
                    Visualisation.attacker_players]
pos = None
app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Dropdown(
    ['Keeper', 'Defender', 'Midfielder', 'Attacker'],
    placeholder='Select a position',
    id = 'dropdown_position'),
    html.Button('Reset filters', id='reset_button', n_clicks=0),
    html.Div(["Select desired properties",dcc.Dropdown(id='multi-dynamic-dropdown', multi = True)]),
    html.Div(['Search for a player', dcc.Dropdown(id='player_search', multi=True)]),
    html.Div(dcc.Graph(id='spyder_graph')),
    html.Div(dcc.Graph(id='line_graph'))
])

@callback(
    Output('multi-dynamic-dropdown', 'options'),
    Input('dropdown_position', 'value')

)
def update_options(value):
    if value is None:
        return []
    global df
    df = value
    return variable_position[['Keeper', 'Defender', 'Midfielder', 'Attacker'].index(value)]

@callback(
    Output('player_search', 'options'),
    Input('player_search', 'value'),
    Input('dropdown_position', 'value'),
)
def update_options(chosen, position):
    if position is not None:
        players = variable_players[['Keeper', 'Defender', 'Midfielder', 'Attacker'].index(position)]
        if chosen is None :
            return players
        elif len(chosen) > 1:
            return chosen
        else:
            return players
    return []
@callback(
    Output('line_graph', 'figure'),
    Input('multi-dynamic-dropdown', 'value'),
    Input('line_graph', 'selectedData'),
    Input('line_graph', 'clickData'),
    Input('reset_button', 'n_clicks')
)

def Create_line(value, selectedData, clickData, clicked):
    if 'reset_button' == ctx.triggered_id:
        Visualisation.reset_dataframe()
    if value is not None:
        keys = [i+'q' for i in value]
        fig = Visualisation.make_line_graph(keys, selectedData, clickData)
        return fig
    else:
        return PreventUpdate

@callback(
    Output('spyder_graph', 'figure'),
    Input('multi-dynamic-dropdown', 'value'),
    Input('line_graph', 'selectedData'),
    Input('line_graph', 'clickData'),
    Input('player_search', 'value')
)

def Create_fig(value, selectedData, clickData, player_selected):
    if player_selected is None and value is not None:
        keys = [i + 'q' for i in value]
        fig = Visualisation.make_graph_spider(df, keys, player_selected)
        return fig
    if player_selected[0] not in list(variable_players[['Keeper', 'Defender', 'Midfielder', 'Attacker'].index(df)]):
        if value is not None:
            keys = [i + 'q' for i in value]
            fig = Visualisation.make_graph_spider(df, keys, None)
            return fig
    else:
        keys = [i + 'q' for i in value]
        fig = Visualisation.make_graph_spider(df, keys, player_selected)
        return fig

if __name__ == '__main__':
    app.run(debug=False)