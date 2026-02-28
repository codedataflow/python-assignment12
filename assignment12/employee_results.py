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
    conn.execute("PRAGMA foreign_keys = 1")  # ensure foreign keys are enforced

    # ----------------------------
    # SQL query
    # ----------------------------
    query = """
    SELECT last_name, 
           SUM(price * quantity) AS revenue
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY e.employee_id;
    """

    # Load query result into a DataFrame
    employee_results = pd.read_sql_query(query, conn)

# ----------------------------
# Plotting with Pandas & Matplotlib
# ----------------------------
# Create a single figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Bar plot of revenue by employee
employee_results.plot(
    x="last_name",
    y="revenue",
    kind="bar",
    color="skyblue",
    legend=False,
    ax=ax
)

# Add titles and labels (following lesson 12.1 style)
ax.set_title("Revenue by Employee", fontsize=16)
ax.set_xlabel("Employee Last Name", fontsize=12)
ax.set_ylabel("Total Revenue", fontsize=12)
ax.set_xticklabels(employee_results["last_name"], rotation=45, ha="right")

# Optional: show revenue values on top of bars
for bar in ax.patches:
    ax.annotate(
        f'{bar.get_height():.0f}',
        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
        ha='center',
        va='bottom',
        fontsize=10
    )

plt.tight_layout()
plt.show()

# ----------------------------
# Optional: check the first rows
# ----------------------------
print(employee_results.head())
