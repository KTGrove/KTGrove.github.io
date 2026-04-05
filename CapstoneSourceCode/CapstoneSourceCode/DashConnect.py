# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output


# Configure the plotting routines
#import numpy as np - not being used [yet]
import pandas as pd
#import matplotlib.pyplot as plt - not being used [yet]

# 1 - Commented-out imports indicates leftover development artificats.
#TODO: Remove these and any other unused imports. 


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from MongoCrud import AnimalShelter  #changed to MongoCrud
# 2 - Import name is inconsistent with current file names
#TODO: Update names to be consistent with files.



###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name. NOTE: You will
# likely need more variables for your constructor to handle the hostname and port of the MongoDB
# server, and the database and collection names

# 3 - We have hardcoded credentials again.
#TODO: Move hardcoded credentials to config file to be called when necessary.
username = "aacuser"
password = "agkg1022"  #hardcoded password for my aacuser account
HOST = 'nv-desktop-services.apporto.com'   #added the other variables for host, port, DB, and collection
PORT = 34129
DB = 'AAC'
COL = 'animals'
shelter = AnimalShelter(username, password, HOST, PORT, DB, COL) #made sure all variables were present
#shelter = AnimalShelter(username, password)
# 4 - Duplicated configuration logic.
#TODO: Centralize the connection/configuration code in one place.

#dict = {shelter}
#df = pd.DataFrame(dict, index=[0])

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
query=shelter.read_all()
#df = pd.DataFrame.from_records(shelter.read({}))
df = pd.DataFrame.from_records(query)

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
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
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
app = JupyterDash('SimpleExample')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard - Kiersten Grove'))),
    html.Hr(),
    
    #addition of buttons
    #html.Div(className = 'buttonRow',
    #        style={'display' : 'flex'},
    #            children=[
    #                html.Button(id='submit-button-one', n_clicks=0, children='Cats'),
    #                html.Button(id='submit-button-two', n_clicks=0, children='Dogs'),
    #            ]),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'), 
     
        ######### Issues adding features, data won't populate if features are turned on ##########
        
        #FIXME: Set up the features for your interactive data table to make it user-friendly for your client
        
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
        page_current = 0,        #sets the first page in the application
        page_size = 5           #sets the number of visible data entries per page

        ##########################################################################################
        
    ),
    html.Br(),
    html.Hr(),
    #adds placement in the layout for the geolocation chart
     html.Div(
            id='map-id',
            className='col s12 m6',
            style={'width': '1000px', 'height': '500px'}
            )
])


#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')
     #Input('submit-button-one', 'n-clicks'), adds functionality to buttons
     #Input('submit-button-two', 'n-clicks')  uncomment when necessary
    ]
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


###debugger to ensure passing of data
# 5 - Debugs to be removed before application deployment.
def update_data_table(derived_virtual_data):
    print("Derived Virtual Data", derived_virtual_data)
    return derived_virtual_data or []

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
     Input('datatable-id', "derived_virtual_selected_rows")]
)
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
                    # 6 - Positional column access. 
                    #TODO: Replace numeric indexes with column names.
                    children=[
                        dl.Tooltip("Breed: " + dff.iloc[row,4]),
                        #column 9 defines the name of the animal
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

    

app.run_server(debug=True, mode='inline')

# 7 - Remaining issues/FIXME comments present in code above. 
#TODO: Remove these comments and ensure all errors have been handled accordingly.
