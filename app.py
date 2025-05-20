import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

def generate_irregular_points(n_points=30, radius_limit=1.0):
    r = radius_limit * np.sqrt(np.random.rand(n_points))  
    theta = 2 * np.pi * np.random.rand(n_points)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

np.random.seed(0)
x, y = generate_irregular_points()

app = Dash(__name__)

def create_point_cloud_figure(radius):
    points_trace = go.Scatter(x=x, y=y, mode='markers',
                              marker=dict(size=8, color='blue'))

    circles = []
    circle_resolution = 50
    for (px, py) in zip(x, y):
        circle_theta = np.linspace(0, 2 * np.pi, circle_resolution)
        circle_x = px + radius * np.cos(circle_theta)
        circle_y = py + radius * np.sin(circle_theta)
        circles.append(go.Scatter(x=circle_x, y=circle_y, mode='lines',
                                  line=dict(color='lightblue', width=2),
                                  fill='toself', fillcolor='rgba(173, 216, 230, 0.2)',
                                  showlegend=False, hoverinfo='skip'))

    layout = go.Layout(
        title=dict(
            text=f'Point Cloud with Radius {radius:.2f}',
            xanchor='left' 
        ),
        xaxis=dict(scaleanchor='y', scaleratio=1, range=[-2, 2]),
        yaxis=dict(range=[-2, 2]),
        height=500,
        width=500,
        hovermode='closest',
        showlegend=False
    )

    fig = go.Figure(data=[points_trace] + circles, layout=layout)
    return fig

def create_persistence_diagram_figure(radius):
    birth = np.array([0.0, 0.3, 0.5])
    death = birth + 0.4 + 0.2 * np.sin(radius * 10)

    mask = death > radius
    birth = birth[mask]
    death = death[mask]

    diag_trace = go.Scatter(
        x=birth,
        y=death,
        mode='markers',
        marker=dict(size=12, color='red')
    )

    diag_line = go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        line=dict(color='black', dash='dash'),
        showlegend=False,
        hoverinfo='skip'
    )

    layout = go.Layout(
        title='Persistence Diagram',
        xaxis=dict(title='Birth', range=[0, 1]),
        yaxis=dict(title='Death', range=[0, 1]),
        height=500,
        width=500,
        hovermode='closest',
        showlegend=False
    )

    fig = go.Figure(data=[diag_trace, diag_line], layout=layout)
    return fig

app.layout = html.Div([
    html.H1("Interactive Persistent Homology Demo"),
    dcc.Slider(
        id='radius-slider',
        min=0,
        max=0.8,
        step=0.02,
        value=0,  # Starts at 0 every time page loads
        marks={i/10: f'{i/10:.1f}' for i in range(0, 9)},
        tooltip={"placement": "bottom", "always_visible": True},
    ),
    html.Div([
        dcc.Graph(id='point-cloud'),
        dcc.Graph(id='persistence-diagram')
    ], style={'display': 'flex', 'justify-content': 'space-around'})
])

@app.callback(
    [Output('point-cloud', 'figure'),
     Output('persistence-diagram', 'figure')],
    [Input('radius-slider', 'value')]
)
def update_graphs(radius):
    pc_fig = create_point_cloud_figure(radius)
    pd_fig = create_persistence_diagram_figure(radius)
    return pc_fig, pd_fig

if __name__ == '__main__':
    app.run(debug=True)

server = app.server

