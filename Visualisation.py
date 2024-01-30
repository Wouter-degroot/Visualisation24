import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go

location = 'C:/Users/wglde/OneDrive/Documents/Visualisation/FIFA DataSet'
# Match data
df_match_data = pd.read_csv(location + '/Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')

# Player data
df_player_defense       = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_defense.csv', delimiter=',')
df_player_gca           = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_gca.csv', delimiter=',')
df_player_keepers       = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_keepers.csv', delimiter=',')
df_player_keepersadv    = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_keepersadv.csv', delimiter=',')
df_player_misc          = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_misc.csv', delimiter=',')
df_player_passing       = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_passing.csv', delimiter=',')
df_player_passing_types = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_passing_types.csv', delimiter=',')
df_player_playingtime   = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_playingtime.csv', delimiter=',')
df_player_possession    = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_possession.csv', delimiter=',')
df_player_shooting      = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')
df_player_stats         = pd.read_csv(location + '/Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')

# Team data
df_team_data        = pd.read_csv(location + '/Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
df_team_group_stats = pd.read_csv(location + '/Data/FIFA World Cup 2022 Team Data/group_stats.csv', delimiter=',')
"""
Creates the Dataframes by merging relevant dataframes and then filtering out the values which we do not need.
"""
df_keepers = pd.merge(df_player_keepers, df_player_keepersadv, how='left')
df_keepers = pd.merge(df_keepers, df_player_stats, how='left')
df_keepers = df_keepers[df_keepers['position'] == 'GK']
df_keepers = df_keepers[['player','minutes', 'gk_goals_against_per90', 'gk_save_pct', 'gk_clean_sheets_pct'
                             ,'gk_pens_save_pct', 'gk_crosses_stopped_pct', 'gk_def_actions_outside_pen_area_per90'
                             ,'gk_passes_completed_launched', 'gk_passes_pct_launched']]

df_defenders = pd.merge(df_player_defense, df_player_misc, how='left')
df_defenders = pd.merge(df_defenders, df_player_passing, how='left')
df_defenders = pd.merge(df_defenders, df_player_stats, how='left')
df_defenders = df_defenders[df_defenders['position'] == 'DF']
df_defenders = df_defenders[['player','tackles_won', 'dribble_tackles', 'dribbled_past', 'blocks','interceptions'
                             ,'clearances','ball_recoveries','aerials_won_pct', 'passes_pct'
                             ,'minutes']]

df_midfielders = pd.merge(df_player_defense, df_player_passing_types, how='left')
df_midfielders = pd.merge(df_midfielders, df_player_misc, how='left')
df_midfielders = pd.merge(df_midfielders, df_player_passing, how='left')
df_midfielders = pd.merge(df_midfielders, df_player_possession, how='left')
df_midfielders = pd.merge(df_midfielders, df_player_stats, how='left')
df_midfielders = df_midfielders[df_midfielders['position'] == 'MF']
df_midfielders = df_midfielders[['player','tackles_won', 'interceptions', 'crosses', 'ball_recoveries'
                                 ,'passes_pct_short', 'passes_pct_medium', 'passes_pct_long',
                                 'passes_into_final_third', 'dribbles_completed_pct', 'aerials_won_pct', 'minutes']]

df_attackers = pd.merge(df_player_passing_types, df_player_passing, how='left')
df_attackers = pd.merge(df_attackers, df_player_possession, how='left')
df_attackers = pd.merge(df_attackers, df_player_shooting, how='left')
df_attackers = pd.merge(df_attackers, df_player_stats, how='left')
df_attackers = pd.merge(df_attackers, df_player_misc, how='left')
df_attackers['xg/goals'] = df_attackers['xg']/df_attackers['goals']
df_attackers['xg/goals'] = df_attackers['xg/goals'].fillna(0)
df_attackers = df_attackers[df_attackers['position'] == 'FW']
df_attackers = df_attackers[['player','crosses','passes_pct', 'dribbles_completed_pct', 'shots_on_target_pct', 'pens_made'
                             ,'aerials_won_pct', 'minutes', 'xg/goals']]

attacker_map = {
    'crossesq' : 'crosses',
    'passes_pctq' : 'passes completion percentage',
    'dribbles_completed_pctq' : 'dribbles completed percentage',
    'shots_on_target_pctq' : 'shots on target percentage',
    'pens_madeq' : 'penalty kicks made',
    'aerials_won_pctq' : 'aerials won percentage',
    'xg/goalsq' : 'expected goals per goal'
}
defender_map = {
    'tackles_wonq' : 'tackles won',
    'dribble_tacklesq' : 'dribblers tackled',
    'dribbled_pastq' : 'dribbled past',
    'blocksq' : 'blocks',
    'interceptionsq' : 'interceptions',
    'clearancesq' : 'clearances',
    'ball_recoveriesq' : 'ball recoveries',
    'aerials_won_pctq' : 'aerials won percentage',
    'passes_pctq': 'passes completion percentage'
}
midfielder_map = {
    'aerials_won_pctq' : 'aerials won percentage',
    'interceptionsq' : 'interceptions',
    'crossesq' : 'crosses',
    'ball_recoveriesq' : 'ball recoveries',
    'passes_pct_shortq' : 'short passes completed percentage',
    'passes_pct_mediumq' : 'medium passes completed percentage',
    'passes_pct_longq' : 'long passes completed percentage',
    'passes_into_final_thirdq' : 'passes that enter final third',
    'dribbles_completed_pct' : 'dribbles completed percentage',
}
keeper_map = {
    'gk_goals_against_per90q' : 'goals against per 90 minutes',
    'gk_save_pctq' : 'goals saved percentage',
    'gk_clean_sheets_pctq' : 'match percentage with 0 goals against',
    'gk_pens_save_pctq' : 'penalty save percentage',
    'gk_crosses_stopped_pctq' : 'percentage of succesful crosses stopped',
    'gk_def_actions_outside_pen_area_per90q' : 'actions outside penalty area per 90 minutes',
    'gk_passes_completed_launchedq' : 'completed passes',
    'gk_passes_pct_launchedq' : 'pass completion percentage'
}
#Creates the keys of every single Dataframe, so that we only have to do this once
keeper_keys = df_keepers.keys()
defender_keys = df_defenders.keys()
midfielder_keys = df_midfielders.keys()
attacker_keys = df_attackers.keys()

attacker_players = df_attackers['player']
midfielder_players = df_midfielders['player']
defender_players = df_defenders['player']
keeper_players = df_keepers['player']
"""
Create the quantile data of every single variables, for an easier comparison
"""
for keys in attacker_keys:
    temp = df_attackers[keys]
    df_attackers[keys+'q'] = [(temp<=i).mean() for i in df_attackers[keys]]
for keys in midfielder_keys:
    temp = df_midfielders[keys]
    df_midfielders[keys+'q'] = [(temp<=i).mean() for i in df_midfielders[keys]]
for keys in defender_keys:
    temp = df_defenders[keys]
    df_defenders[keys+'q'] = [(temp<=i).mean() for i in df_defenders[keys]]
for keys in keeper_keys:
    temp = df_keepers[keys]
    df_keepers[keys+'q'] = [(temp<=i).mean() for i in df_keepers[keys]]

df_attackers = df_attackers.drop(['playerq'],axis=1)
df_midfielders = df_midfielders.drop(['playerq'],axis=1)
df_defenders = df_defenders.drop(['playerq'],axis=1)
df_keepers = df_keepers.drop(['playerq'],axis=1)
"""
Create a copy of the original Dataframes so that they never get changed.
"""
df_attackers_filtered = df_attackers.copy()
df_defenders_filtered = df_defenders.copy()
df_keepers_filtered = df_keepers.copy()
df_midfielders_filtered = df_midfielders.copy()
#creating 2 flags for the next function which have to stand outside the function to save their values
flag = True
old_pos = None
def reset_dataframe():
    global df
    if old_pos == 'Keeper':
        df = df_keepers_filtered.copy()
        df['highlighted'] = False
    elif old_pos == 'Defender':
        df = df_defenders_filtered.copy()
        df['highlighted'] = False
    elif old_pos == 'Midfielder':
        df = df_midfielders_filtered.copy()
        df['highlighted'] = False
    elif old_pos == 'Attacker':
        df = df_attackers_filtered.copy()
        df['highlighted'] = False
def make_line_graph(val, selectedData, clickData):
    """
    :param val: The currently selected variables, to be filtered on is a list of strings
    :param selectedData: The selected data by dragging the mouse over a figure, a dictionary with ranges
    :return: Returns a subplot, of list n where n is the length of val. with all line plots of val.
    """
    global df
    fig = make_subplots(rows = len(val)//2+1, cols=len(val)//2+1)
    imax = len(val)//2+1
    temp_df = df[val]
    changed = False
    for i in range(len(val)):
        """
        Goes through all the different variables in the val list,
        sorts the temporary and main dataframe to the variable in descending order
        """
        df = df.sort_values(by=str(val[i]), ascending=False).reset_index(drop=True)
        temp_df = temp_df.sort_values(by=str(val[i]), ascending=False).reset_index(drop=True)
        if clickData is not None:
            if i*2 == clickData['points'][0]['curveNumber']:
                df['highlighted'] = False
                df.loc[clickData['points'][0]['x'], 'highlighted'] = True
            elif i == clickData['points'][0]['curveNumber']:
                df['highlighted'] = False
                df.loc[clickData['points'][0]['x'], 'highlighted'] = True
        if selectedData is not None and 'range' in selectedData.keys():
            """
            If there is data selected filter the main Dataframe to only include the selected data,
            If statement is there because of a difference in formatting for the first subplot and subsequent subplots
            """
            if 'x' in selectedData['range'].keys() and changed is False:
                changed = True
                val1,val2 = selectedData['range'][f'x'][0], selectedData['range'][f'x'][1]
                df = df.iloc[round(val1):round(val2)]
            else:
                if f'x{i+1}' not in selectedData['range'].keys():
                    continue
                val1, val2 = selectedData['range'][f'x{i+1}'][0], selectedData['range'][f'x{i+1}'][1]
                df = df.iloc[round(val1):round(val2)]
        j = i // imax
        #Adds the current value to the currently looked at subplot.

        fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df[val[i]], text=val[i], name=val[i], legend="legend2"),
                      row=j+1, col =i%imax+1)
        zoomed = False
        if selectedData is not None:
            if 'range' in selectedData:
                zoomed = True
        if clickData is not None and not zoomed:
            clicked = df[df['highlighted'] == True]
            if not clicked.empty:
                fig.add_trace(go.Scatter(x=[clicked.index[0]], y=clicked[val[i]], mode='markers', marker_symbol ='star', marker_size = 15,
                                         showlegend=False, text=val[i], name=val[i]),
                              row=j+1, col =i%imax+1)
    fig.update_layout(dragmode='select')
    return fig

def make_graph_spider(pos, values, players_selected):
    """
    :param pos: Looks at the currently looked at position, eg: Keeper, defender, midfielder, attacker
    :param values: The currently selected variables to take into consideration
    :return: A Spider plot with all currently selected variables
    """
    global df
    global flag
    #old_pos is the previous position, so the dataframe can be resetted when a new position is chosen
    global old_pos
    if flag is True or old_pos != pos:
        """
        If there is no position yet, or the position has been changed change the main dataframe to the 
        Chosen position
        """
        old_pos = pos
        if pos == 'Keeper':
            df = df_keepers_filtered.copy()
            df['highlighted'] = False
        elif pos == 'Defender':
            df = df_defenders_filtered.copy()
            df['highlighted'] = False
        elif pos == 'Midfielder':
            df = df_midfielders_filtered.copy()
            df['highlighted'] = False
        elif pos == 'Attacker':
            df = df_attackers_filtered.copy()
            df['highlighted'] = False
        flag = False
    """
    Create a temporary dataframe, filtered to chosen values, sort these values by the mean of the values in descending order.
    Transpose the Dataframe so that px.line_polar can more easily calculate the figure,
    """
    amount_plots = 1
    if players_selected is not None:
        amount_plots = 2

    temp_df = df.copy()[values]
    temp_df['player'] = df['player']
    temp_df['mean'] = temp_df.mean(axis=1, numeric_only=True)
    temp_df = temp_df.sort_values(by='mean', ascending=False).reset_index(drop=True)
    temp_df_t = temp_df.drop('player', axis=1).transpose()

    fig = make_subplots(rows = 1, cols = amount_plots,
                        specs=[[{"type": "polar"} for _ in range(amount_plots)] for _ in range(1)])

    highlighted_player_data = df[df['highlighted'] == True].reset_index()
    highlighted_player = highlighted_player_data[['player']]
    temp_high = highlighted_player_data[values]
    temp_high['mean'] = temp_high.mean(axis=1, numeric_only=True)
    temp_high_t = temp_high.transpose()

    if players_selected is not None:
        temp_selected = df.query(f'player in {players_selected}').reset_index()
        temp_selected = temp_selected[values]
        temp_selected['mean'] = temp_selected.mean(axis=1, numeric_only=True)
        temp_selected_t = temp_selected.transpose()

    if not highlighted_player_data.empty:
        fig.add_trace(go.Scatterpolar(
        r=temp_high_t[0],
        theta=temp_high_t.index,
        fill='toself',
        name = highlighted_player.loc[0, 'player'],
            opacity=0.3
        ), row=1, col=1)
    fig.add_trace(go.Scatterpolar(
        r=temp_df_t[0],
        theta=temp_df_t.index,
        fill='toself',
        name = temp_df['player'][0],
        opacity=0.3
    ), row=1, col=1)
    fig.add_trace(go.Scatterpolar(
        r = temp_df_t[1],
        theta=temp_df_t.index,
        fill='toself',
        name=temp_df['player'][1],
        opacity=0.3
    ), row=1, col=1)
    fig.add_trace(go.Scatterpolar(
        r=temp_df_t[2],
        theta=temp_df_t.index,
        fill='toself',
        name=temp_df['player'][2],
        opacity=0.3
    ), row=1, col=1)
    if players_selected is not None:
        fig.add_trace(go.Scatterpolar(
            r=temp_selected_t[0],
            theta=temp_selected_t.index,
            fill='toself',
            name=players_selected[0],
            opacity=0.3
        ), row=1, col=2)
        if len(players_selected) > 1:
            fig.add_trace(go.Scatterpolar(
                r=temp_selected_t[1],
                theta=temp_selected_t.index,
                fill='toself',
                name=players_selected[1],
                opacity=0.3
            ), row=1, col=2)
    return fig