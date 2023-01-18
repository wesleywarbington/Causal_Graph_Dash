styles = {
    "cytoscape": {
        "position": "absolute",
        "width": "100%",
        "height": "70%",
        "zIndex": 999,
        # 'border-color': 'black', 
        # 'border-width': '2',  
        # 'border-style': 'solid',
        # 'margin-left': '5px',
        # 'margin-right': '5px',
    },
    'containerBorder': {
        'border-color': 'black', 
        'border-width': '2',  
        'border-style': 'solid'
    },
    'cytoGraph': {
        'background-color': 'white',
        'border-color': 'black', 
        'border-width': '2',  
        'border-style': 'solid'
    },
    'dropdown_style': {
        'width': '100%',
        'margin-top': '10px',
        # "display": "flex", 
        # "flexWrap": "wrap"
    },
    'button_style': {
        # 'background-color': 'red',
        # 'color': 'white',
        'height': '50px',
        'width': '100%',
        'margin-top': '10px',
        'margin-left': '5px',
        'margin-right': '5px',
        'margin-bottom': '10px'
    },
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '400px'
    }
}

cytoscape_stylesheets =[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        'color': '#373A3C',
                        # 'text-valign': 'top',
                        "font-size": "10pt",
                        "font-family": "system-ui",
                        # "shape": 'pentagon',
                    },
                },
                {
                    'selector': '.special',
                    'style': {
                        'background-color': '#373A3C',
                        'border-width': '2',
                        'border-color': '#373A3C'
                    }
                },
                {
                    'selector': '.frozen',
                    'style': {
                        'background-color': 'red',
                        # 'border-width': '2',
                        # 'border-color': 'red'
                    }
                },
                                        {
                    'selector': '.normal',
                    'style': {
                        'background-color': 'white',
                        'border-width': '2',
                        'border-color': '#373A3C'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                    }
                }
            ]