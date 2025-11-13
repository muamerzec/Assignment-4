import math
from typing import List
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go


def compute_a(pY: float, pLy: float, pNotLnotY: float, s: float):
    p_up = pY * pLy
    p_L_given_notY = 1 - pNotLnotY
    p_down = (1 - pY) * p_L_given_notY

    if p_down == 0:
        return float("inf"), p_up, p_down

    a = p_up / (p_down / s)
    return a, p_up, p_down


def stationary_distribution(a: float) -> List[float]:
    if a <= 0:
        return [1.0] + [0.0] * 7
    if math.isinf(a):
        return [0.0] * 7 + [1.0]

    values = [a ** i for i in range(8)]
    ssum = sum(values)
    return [v / ssum for v in values]


def build_figure(dist):
    fig = go.Figure()
    fig.add_bar(x=[f"State {i}" for i in range(1, 9)], y=dist)
    fig.update_layout(
        title="Stationary Distribution (8-state Literal Automaton)",
        yaxis=dict(title="Probability", range=[0, 1]),
        xaxis=dict(title="State (memory level: 1 = Forgotten ... 8 = Memorized)"),
        margin=dict(l=40, r=30, t=60, b=40),
    )
    return fig


app: Dash = dash.Dash(__name__)

app.layout = html.Div(
    style={"padding": "16px"},
    children=[
        html.H2("Interactive Stationary Distribution — Literal Automaton (8 states)"),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(2, 1fr)", "gap": "18px"},
            children=[
                html.Div([
                    html.Label("s (forget value)"),
                    dcc.Slider(id="s", min=1.0, max=25.0, step=0.1, value=15.0,
                               marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                ]),
                html.Div([
                    html.Label("P(Y)"),
                    dcc.Slider(id="pY", min=0.0, max=1.0, step=0.01, value=0.5,
                               marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                ]),
                html.Div([
                    html.Label("P(L | Y)"),
                    dcc.Slider(id="pLy", min=0.0, max=1.0, step=0.01, value=0.9,
                               marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                ]),
                html.Div([
                    html.Label("P(~L | ~Y)"),
                    dcc.Slider(id="pNotLnotY", min=0.0, max=1.0, step=0.01, value=0.1,
                               marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                ]),
            ],
        ),

        html.Br(),
        dcc.Graph(id="bar"),

        html.Div(id="numbers", style={"marginTop": "16px"}),
    ]
)


@app.callback(
    Output("bar", "figure"),
    Output("numbers", "children"),
    Input("s", "value"),
    Input("pY", "value"),
    Input("pLy", "value"),
    Input("pNotLnotY", "value"),
)
def update(s: float, pY: float, pLy: float, pNotLnotY: float):
    a, p_up, p_down = compute_a(pY, pLy, pNotLnotY, s)
    dist = stationary_distribution(a)
    fig = build_figure(dist)

    numbers = html.Div([
        html.Div(f"State {i+1}: {dist[i]:.3f}") for i in range(8)
    ] + [
        html.Div(f"p_up: {p_up:.3f}"),
        html.Div(f"p_down: {p_down:.3f}"),
        html.Div(f"a: {a:.3f}"),
        html.Div(f"sum π_i: {sum(dist):.6f}"),
    ])

    return fig, numbers


if __name__ == "__main__":
    app.run(debug=True)
