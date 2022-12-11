# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import folium
import wget
import pandas as pd

spacex_df=pd.read_csv('spacex_launch_dash.csv')

spacex_df.head()

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



#______________SOLUTION_WORKS_______

# Create a dash application
app = dash.Dash(__name__)
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'All'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                             ],
                                             value='All',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                            ), #dropdown ends
                                
                                html.H2('Payload range (kg):',
                                       style={'textAlign': 'left', 'color': '#503D36','font-size': 15}
                                       ),
                                
                                dcc.RangeSlider(id='slider',
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                marks= c,
                                                value=[0, 10000]), 
                                
                                html.Div(dcc.Graph(id='site-success-scatter')),
                                                                
                              
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                               ]) #layout ends

@app.callback(
    [Output('site-success-scatter', 'figure'), Output('success-pie-chart', 'figure')], 
    [Input('site-dropdown', 'value'), Input('slider', 'value')] )



def display_my_pies(val, slide):
    spacex_dff = spacex_df[(spacex_df['Payload Mass (kg)'] > slide[0]) & (spacex_df['Payload Mass (kg)'] < slide[1])]
    if val == 'All':
        #spacex_df[spacex_df['class'] == 1]
        #spacex_dff = spacex_df[(spacex_df['Payload Mass (kg)'] > slide[0]) & (spacex_df['Payload Mass (kg)'] < slide[1])] 
        fig = px.scatter(spacex_dff, x="Payload Mass (kg)", y="class", color="Booster Version Category", title = 'Correlation between payload and success for all sites')
        fig.show()
        fig1 = px.pie(spacex_dff[spacex_dff['class'] == 1], names='Launch Site', title="Total Successful Launches By Site")
        fig1.show()
    else:
        fig = px.scatter(spacex_dff[spacex_dff['Launch Site'] == val], x="Payload Mass (kg)", y="class", color="Booster Version Category", title= ('Correlation between payload and success for site ' + val))
        fig.show()
        fig1 = px.pie(spacex_dff[spacex_dff['Launch Site'] == val], names='class', title= ('Total Successful Launches for site ' + val))
        fig1.show()
    return fig, fig1

if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    #app.run_server(mode="inline", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)
    app.run_server(host='localhost',port=8005)


#Background

spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
spacex_df=pd.read_csv(spacex_csv_file)
spacex_df.to_csv(index=False) #saved as 'spacex_launch_dash'

opt = spacex_df['Launch Site'].unique()
print(len(opt))
print(opt)
for i in opt:
    print(i)

spacex_df.head()

#checking graphs work

fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
fig.show()


spacex_df_success = spacex_df[spacex_df['class'] == 1]
site_name = 'CCAFS LC-40' #'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40'
#fig1 = px.pie(spacex_df_success, names='Launch Site', title="Pie Chart")
fig1 = px.pie(spacex_df[spacex_df['Launch Site'] == site_name], names='class', title= (site_name + ' Pie'))
fig1.show()

#Show all sites proportion of successful launches

#spacex_df_success
fig2 = px.pie(spacex_df_success, names='Launch Site', title="Pie Chart")
fig2.show()

def trial_def(val):
    
    if val == 'All':
        spacex_df[spacex_df['class'] == 1]
        fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        fig.show()
        fig2 = px.pie(spacex_df[spacex_df['class'] == 1], names='Launch Site', title="Pie Chart")
        fig2.show()
    else:
        fig = px.scatter(spacex_df[spacex_df['Launch Site'] == val], x="Payload Mass (kg)", y="class", color="Booster Version Category", title= ('Scatter for Site: ' + val))
        fig.show()
        fig1 = px.pie(spacex_df[spacex_df['Launch Site'] == val], names='class', title= (val + ' Pie'))
        fig1.show()
        

trial_def('All')


#messing around i think

import math
c = {}

h = math.ceil(max_payload)
for i in range(0, 10000, 2500):
    y = {i:str(i)}
    c.update(y)





    
