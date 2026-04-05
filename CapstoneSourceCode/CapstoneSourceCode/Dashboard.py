# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os # 1 - OS is imported but not used; remove unused imports.

# Configure the plotting routines
import numpy as np              # Numpy and matplotlib also appear to be imported and unused. Remove these. 
import pandas as pd
import matplotlib.pyplot as plt


# 2 - Currently does not match file structure/names. 
from MongoCrud import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

# 3 - Hardcoded credentials are currenly stored in UI layer.
# TODO: Credentials should be moved to a config file.
username = "aacuser"
password = "agkg1022"  #hardcoded password for my aacuser account
HOST = 'nv-desktop-services.apporto.com'   #added the other variables for host, port, DB, and collection
PORT = 34129
DB = 'AAC'
COL = 'animals'
shelter = AnimalShelter(username, password, HOST, PORT, DB, COL) #made sure all variables were present


# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
records=shelter.read_all()
#df = pd.DataFrame.from_records(shelter.read({}))

# 4 - All records are currently loaded at startup.
# TODO: Load data on demand or impliment paginated queries.

df = pd.DataFrame.from_records(records)

###debug check contents of dataframe
#print("DataFrame Loaded:")
#print(df)

###debug
#if df.empty:
#    print("Dataframe is empty. Check source.")
#else:
#    print("Dataframe loaded successfully.")

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will return a new dataframe that does not contain the dropped column(s)
if '_id' in df.columns:
    df.drop(columns=['_id'],inplace=True)

## Debug with additions
#print("DataFrame after dropping '_id':")
#print(df)
#print(len(df.to_dict(orient='records')))
#print(df.columns)

#########################
# Dashboard Layout / View
#########################
app = JupyterDash("SimpleExample") ##changed name

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png' ##updated image name to match given logo
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
# 5 - File access is currently not wrapped in error handling.
# Add try/except in case image is missing/inaccessible.

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Hr(),
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
        html.B(html.H3('Developed by: Kiersten Grove'))
    ]),
    html.Hr(),
    html.Div([
        dcc.RadioItems( ##addition of radio items to filter by
            id = 'filter-type',
            options = [
                {'label': 'Water Rescue', 'value': 'water_rescue'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'mw_rescue'},
                {'label': 'Disaster Rescue or Individual Tracking', 'value': 'disaster_rescue'},
                {'label': 'Reset', 'value': 'reset'}
            ],
            value = 'reset' ##sets default
        )

    ]),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'), 
     
        #added below features with explanatory comments
        #column parameters have been set above under id for the datatable
        
        editable = False,          #makes the content uneditable
        filter_action = "native",  #filters the content by column
        sort_action = "native",    #sorts the content by column
        sort_mode = "multi",       #allows user to sort using multiple columns 
        row_selectable = "single", #creates single-row selection for data table mapping
        row_deletable = False,     #makes rows undeletable 
        selected_rows = [0],       #select the first row by default
        page_action = "native",    #page sorting
        page_current = 0,          #sets the first page in the application
        page_size = 10             #sets the number of visible data entries per page
        
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################
    
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
## FIX ME Add code to filter interactive data table with MongoDB queries
    if filter_type == "water_rescue":
        query = {"breed": {"$in": ["Labrador Retriever Mix",
                                   "Chesapeake Bay Retriever", #only saw chesa bay retr in data, none were intact females
                                   "Newfoundland"]
                          },
                 "sex_upon_outcome": "Intact Female",
                 "$and": [{"age_upon_outcome_in_weeks": {"$gte": 26}},
                          {"age_upon_outcome_in_weeks": {"$lte": 156}}]
                }
    elif filter_type == "mw_rescue":
        query = {"breed": {"$in": ["German Shepherd",
                                   "Alaskan Malamute",
                                   "Old English Sheepdog",
                                   "Siberian Husky",
                                   "Rottweiler"]
                          },
                 "sex_upon_outcome": "Intact Male",
                 "$and": [{"age_upon_outcome_in_weeks": {"$gte": 26}},
                          {"age_upon_outcome_in_weeks": {"$lte": 156}}]
                }
    elif filter_type == "disaster_rescue":
        query = {"breed": {"$in": ["Doberman Pinscher",
                                   "German Shepherd",
                                   "Golden Retriever",
                                   "Bloodhound",
                                   "Rottweiler"]
                          },
                 "sex_upon_outcome": "Intact Male",
                 "$and": [{"age_upon_outcome_in_weeks": {"$gte": 20}},
                          {"age_upon_outcome_in_weeks": {"$lte": 300}}]
                }
    else:
        query = {}

    df = pd.DataFrame(list(shelter.read(query)))
    #df = pd.DataFrame.from_records(records)
    if '_id' in df.columns:
        df.drop(columns=['_id'],inplace=True)
    data = df.to_dict('records')
    
    return data

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    if viewData is None or len(viewData) == 0:
        return html.Div("No data available to display.")
    
    dff = pd.DataFrame.from_dict(viewData)
    fig = px.pie(dff, names='breed', title='Preferred Animals')
    return [
        dcc.Graph(
            #style = {"width": "500px", "height": "500px"},
            figure = fig
        )    
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    if selected_columns is None:
        return []
    else:
        return [
            {
                'if': { 'column_id': i },
                'background_color': '#D2F3FF'
            } for i in selected_columns
        ]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
    
    ###debugger checks if viewData is none or empty
    if viewData is None or len(viewData) == 0:
        return [html.Div("No data available.")]
    
#FIXME Add in the code for your geolocation chart
    dff = pd.DataFrame.from_dict(viewData)
    if index is None: #converted to single row index because single row selection is what is allowed
        row = 0
    else:
        row = index[0]
    ###checks the row exists in the data
    if row >= len(dff):
        return [html.Div("Invalid row selected.")]
    
        
    return [
        dl.Map(
            style = {'width': '1000px', 'height': '500px'},
            center = [30.75, -97.48], 
            zoom = 10, 
            children = [
                dl.TileLayer(id="base-layer-id"),
                #column 13 and 14 define the grid-coordinates for the map
                dl.Marker(
                    position=[dff.iloc[row, 13], dff.iloc[row, 14]],
                    # 6 - Map coordinates are accessed by numeric column index.
                    #TODO: Change to latitude/longitude reference by column name instead of position.
                    children=[
                        dl.Tooltip("Breed: " + dff.iloc[row,4]),
                        # 7 - Breed and animal accessed by numeric index.
                        #TODO: Use named columns for readability and reliability.
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(dff.iloc[row,9])
                        ])
                    ]
                )
            ]
        )
    ]

def update_map_callback(viewData, Index):
    return update_map(viewData, Index)

    

app.run_server(debug=True)
# 8 - Debugs should be removed prior to produciton deployment.