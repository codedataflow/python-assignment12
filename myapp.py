from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load Gapminder dataset
df = px.data.gapminder()

# Create list of unique countries (remove duplicates)
countries = df["country"].drop_duplicates()

# Initialize Dash app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.H1("GDP Per Capita Growth Dashboard"),

    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": country, "value": country} for country in countries],
        value="Canada"  # Default selection
    ),

    dcc.Graph(id="gdp-growth")
])

# Callback
@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(selected_country):
    # Filter dataset for selected country
    filtered_df = df[df["country"] == selected_country]

    # Create line chart
    fig = px.line(
        filtered_df,
        x="year",
        y="gdpPercap",
        title=f"GDP Per Capita Growth for {selected_country}"
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
