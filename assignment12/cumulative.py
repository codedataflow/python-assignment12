import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# ----------------------------
# Database connection
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../db/lesson.db")

with sqlite3.connect(db_path) as conn:
    print("Connected to lesson.db successfully.")
    conn.execute("PRAGMA foreign_keys = 1")

    # ----------------------------
    # SQL query: total revenue per order
    # ----------------------------
    query = """
    SELECT o.order_id,
           SUM(price * quantity) AS total_price
    FROM orders o
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id;
    """

    # Load into DataFrame
    df = pd.read_sql_query(query, conn)

# ----------------------------
# Cumulative revenue column
# ----------------------------
df["cumulative"] = df["total_price"].cumsum()

# ----------------------------
# Plotting: Line plot
# ----------------------------
fig, ax = plt.subplots(figsize=(10, 6))  # single figure and axes

df.plot(
    x="order_id",
    y="cumulative",
    kind="line",
    color="green",
    legend=False,
    ax=ax
)

# Titles and labels
ax.set_title("Cumulative Revenue Over Time", fontsize=16)
ax.set_xlabel("Order ID", fontsize=12)
ax.set_ylabel("Cumulative Revenue", fontsize=12)

# Optional: highlight final revenue value on last point
last_order = df.iloc[-1]
ax.annotate(f'{last_order.cumulative:.0f}',
            xy=(last_order.order_id, last_order.cumulative),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center',
            fontsize=10)

plt.tight_layout()
plt.show()

# ----------------------------
# Optional: inspect DataFrame
# ----------------------------
print(df.head())
