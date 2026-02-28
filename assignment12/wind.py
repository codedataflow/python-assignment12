import plotly.express as px
import plotly.data as pldata
import pandas as pd

# ----------------------------
# Load the dataset
# ----------------------------
df = pldata.wind(return_type='pandas')

# Inspect first and last 10 rows
print("First 10 rows:")
print(df.head(10))
print("\nLast 10 rows:")
print(df.tail(10))

# ----------------------------
# Data cleaning: convert 'strength' to float
# ----------------------------
# Remove any non-numeric characters (e.g., % or whitespace) and convert
df['strength'] = df['strength'].astype(str).str.replace(r"[^\d\.]", "", regex=True)
df['strength'] = df['strength'].astype(float)

# Optional: verify conversion
print("\nStrength column after cleaning:")
print(df['strength'].head(10))

# ----------------------------
# Interactive scatter plot
# ----------------------------
fig = px.scatter(
    df,
    x='strength',
    y='frequency',
    color='direction',
    title="Wind Strength vs Frequency by Direction",
    hover_data=['strength', 'frequency', 'direction'],
)

# Save to HTML and open automatically in browser
fig.write_html("wind.html", auto_open=True)

print("\nInteractive plot saved as 'wind.html'. Opened in browser.")
