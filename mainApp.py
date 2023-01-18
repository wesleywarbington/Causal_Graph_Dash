import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc, ctx
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
from styling import styles, cytoscape_stylesheets

df = pd.read_csv('data/student-por.csv', delimiter=';')
graph = nx.drawing.nx_agraph.read_dot('data/graph.dot')
cyto.load_extra_layouts()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL]) # https://bootswatch.com/default/ 
# CERULEAN, COSMO, CYBORG, FLATLY, JOURNAL, LITERA, LUMEN
# *********************************************************************************************************
# Graph data

nodes = [{'data': {"id": node, 'label': node}, 'classes': 'normal'} for node in graph.nodes()]

edges = [
    {'data': {'id': source+target, 'source': source, 'target': target}}
    for source, target in graph.edges()
]

elements = nodes + edges

# *********************************************************************************************************
# components

addEdge = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Input(id='edgeSourceInput', placeholder='Source', style={'margin-top': '10px'})),
        dbc.Col(dbc.Input(id='edgeTargetInput', placeholder='Target', style={'margin-top': '10px'})),
        dbc.Col(dbc.Button('Add Edge', id='btn-add-edge', n_clicks_timestamp=0, style={'width': '100%', 'margin-top': '10px'}))
    ])
])

targetFreezeNormalize = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Button('Freeze Node', id='freezeNodeButton', n_clicks_timestamp=0, style={'width': '100%', 'margin-top': '10px'})),
        dbc.Col(dbc.Button('Make Target Node', id='targetNodeButton', n_clicks_timestamp=0, style={'width': '100%', 'margin-top': '10px'})),
        dbc.Col(dbc.Button('Normalize Node', id='normalizeNodeButton', n_clicks_timestamp=0, style={'width': '100%', 'margin-top': '10px'}))
    ])
])

saveModel = dbc.Container([
    dbc.Button('Save Model', id='saveModelButton', n_clicks_timestamp=0, color='primary', style={'width': '100%', 'margin-top': '10px'})
])

edgePopup = (
        html.Div(
            [
                dbc.Modal([
                    dbc.ModalHeader('Remove Edge from blank to blank?', id='removeEdgeHeader'),
                    dbc.ModalBody([
                        dbc.Button('Yes', id='btn-remove-edge', n_clicks_timestamp=0, style={'width': '100%', 'margin-top': '5px', 'margin-bottom': '5px'}),
                        dbc.Button("No", id="removeEdgeClose", className="ml-auto", style={'width': '100%', 'margin-top': '5px', 'margin-bottom': '5px'})
                ]),
                    dbc.ModalFooter(
                        dbc.Button('Reverse Edge', id='reverseEdge', style={'width': '100%', 'margin-top': '5px', 'margin-bottom': '5px'})
                    )
                ],
                    id="removeEdgeModal",
                    is_open=False,    # True, False
                    size="sm",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    centered=True,    # True, False
                    fade=True         # True, False
                ),
            ]
        )
    )

histPopup = (
    html.Div(
            [
                dbc.Modal([
                    dbc.ModalHeader(id='histPopUpId'),
                    dbc.ModalBody(
                        dcc.Graph(id='histogram')
                    ),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="histClose", className="ml-auto")
                    ),
                ],
                    id="histModal",
                    is_open=False,    # True, False
                    size="xl",        # "sm", "lg", "xl"
                    backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                    scrollable=True,  # False or True if modal has a lot of text
                    centered=True,    # True, False
                    fade=True         # True, False
                ),
            ]
        )
    )

chart_orientation_dropdown = (
    dbc.Container(
        [dcc.Dropdown
            (id='dpdn',
            value='cose-bilkent',
            style=styles['dropdown_style'],
            clearable=False,
            options=[{'label': 'Graph Layout: ' + name.capitalize(), 'value': name}for name in ['klay', 'dagre', 'spread', 'euler', 'cola', 'cose-bilkent', 'breadthfirst' ,'grid', 'random', 'circle', 'cose', 'concentric']]), ]
            )
        )

cytoGraph1 = (cyto.Cytoscape(
            id="cytoscape-graph",
            elements=elements,
            layout={'name': 'cose'},
            style=styles['cytoscape'],
            minZoom=0.3,
            maxZoom=5,
            responsive=True,
            stylesheet=cytoscape_stylesheets
        )
    )
# *********************************************************************************************************
# Layout
app.layout = html.Div([ 
    dbc.Container(html.H1('Causal Graph')),
    dbc.Container([
        chart_orientation_dropdown, 
        addEdge, targetFreezeNormalize, 
        saveModel
        ]),
    cytoGraph1,
    edgePopup,
    histPopup
    ])

# *********************************************************************************************************
# User input/output (callbacks)

# Send edge source and target data of edge tapped to popup header
@app.callback(
    Output("removeEdgeHeader", 'children'),
    Input('cytoscape-graph', 'tapEdgeData')
)
def changeText(mouse_on_edge):
    if mouse_on_edge is None:
        text = 'Remove Edge from blank to blank'
    else:
        text = 'Remove Edge from "{}" to "{}"?'.format(mouse_on_edge['source'], mouse_on_edge['target'])
    return text

# Change layout of graph
@app.callback(Output("cytoscape-graph", 'layout'),
              Input('dpdn', 'value'))
def update_layout(layout_value):
    if layout_value == 'cose':
        return {'name': layout_value, 'animate': True}
    else:
        return {'name': layout_value, 'animate': True}

# Interaction with nodes and edges of cytoscape graph

@app.callback(
    Output('cytoscape-graph', 'elements'),
    [Input('targetNodeButton', "n_clicks"), Input('freezeNodeButton', "n_clicks"), Input('normalizeNodeButton', "n_clicks"), Input('btn-remove-edge', "n_clicks"), Input('btn-add-edge', "n_clicks")],
    [State('edgeSourceInput', 'value'), State('edgeTargetInput', 'value'), State('cytoscape-graph', 'elements'), State('cytoscape-graph', 'selectedEdgeData'), State('cytoscape-graph', 'selectedNodeData')]
)

def removeAddEdge(tgtNode, btnFreeze, btnNormalize, btnRemove, btnAdd,  src, tgt, elements, edgedata, nodedata):
    button_clicked = ctx.triggered_id
    if button_clicked == 'btn-remove-edge':
        if elements and edgedata:
            ids_to_remove = {ele_data['id'] for ele_data in edgedata}
            elements = [ele for ele in elements if ele['data']['id'] not in ids_to_remove]

    if button_clicked == 'btn-add-edge' and src in graph.nodes() and tgt in graph.nodes():
        elements += [{'data': {'id': src+tgt, 'source': src, 'target': tgt}}]
    

    if button_clicked == 'freezeNodeButton':
        for index, nodes in enumerate(elements):
            if nodes['data']['id'] == nodedata[0]['id']:
                elements[index] = {'data': nodes['data'], 'classes': 'frozen'}

    if button_clicked == 'targetNodeButton':
        for index, nodes in enumerate(elements):
            if nodes['data']['id'] == nodedata[0]['id']:
                elements[index] = {'data': nodes['data'], 'classes': 'special'}

    if button_clicked == 'normalizeNodeButton':
        for index, nodes in enumerate(elements):
            if nodes['data']['id'] == nodedata[0]['id']:
                elements[index] = {'data': nodes['data'], 'classes': 'normal'}

    return elements

# Pop Up confirming if user wants to remove edge
@app.callback(
    Output("removeEdgeModal", "is_open"),
    [Input('cytoscape-graph', 'tapEdgeData'), Input("removeEdgeClose", "n_clicks"), Input('btn-remove-edge', "n_clicks"), Input('reverseEdge', "n_clicks")],
    [State("removeEdgeModal", "is_open")],
)
def toggle_modal(n1, n2, n3, n4, is_open):
    if n1 or n2 or n3 or n4:
        return not is_open
    return is_open

# *********************************************************************************************************

if __name__ == "__main__":
    app.run_server(debug=True)