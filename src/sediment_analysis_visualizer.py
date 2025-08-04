import pandas as pd
import matplotlib.pyplot as plt


daily_data = pd.read_csv("data/processed/merged_df.csv")


fig, ax1 = plt.subplots(figsize=(12, 6))
plt.xticks(rotation=45)
plt.tight_layout()
# Stock Price (Left Axis)
ax1.plot(daily_data['Date'], daily_data['Close'], color='tab:blue', label='Stock Price')
ax1.set_ylabel('Stock Price (USD)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True, alpha=0.3)

# Sentiment (Right Axis)
ax2 = ax1.twinx()
ax2.plot(daily_data['Date'], daily_data['Average_Sentiment'], color='tab:red', linestyle='--', label='Sentiment')
ax2.set_ylabel('Avg. Sentiment (-1 to +1)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_ylim(-1, 1)  # Fixed sentiment range

plt.title('Stock Price vs. Sentiment (Dual Axes)')

fig.legend(loc='upper left')
plt.show()