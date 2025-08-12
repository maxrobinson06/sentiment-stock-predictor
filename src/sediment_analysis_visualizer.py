import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load data and ensure 'Date' is a datetime type
daily_data = pd.read_csv("data/processed/merged_df.csv")
daily_data['Date'] = pd.to_datetime(daily_data['Date'])


# Create figure and primary axis
fig, ax1 = plt.subplots(figsize=(14, 7))
plt.title('Stock Price vs. Sentiment Over Time', fontsize=16, pad=20)

# Stock Price (Left Axis)
ax1.plot(daily_data['Date'], daily_data['Close'], 
         color='tab:blue', linewidth=2, label='Stock Price')
ax1.set_ylabel('Stock Price (USD)', color='tab:blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True, linestyle='--', alpha=0.6)

# Sentiment (Right Axis)
ax2 = ax1.twinx()
ax2.plot(daily_data['Date'], daily_data['Average_Sentiment'], 
         color='tab:red', linestyle='-', alpha=0.8, linewidth=1.5, label='Sentiment')
ax2.set_ylabel('Avg. Sentiment (-1 to +1)', color='tab:red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_ylim(-1.1, 1.1)  # Slightly extended range for visibility

# Improve x-axis (dates)
ax1.xaxis.set_major_locator(mdates.MonthLocator())  # Major ticks every month
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format as "Jan 2023"
plt.xticks(rotation=45, ha='right')  # Rotate labels for readability

# Add legend (merged)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=1)

# Add horizontal line at sentiment=0 for neutrality reference
ax2.axhline(0, color='gray', linestyle=':', alpha=0.5)

# Tight layout and show
plt.tight_layout()
plt.show()