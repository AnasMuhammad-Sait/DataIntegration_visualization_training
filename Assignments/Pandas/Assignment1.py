import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv('C:/Users/anass/Documents/HxTraining/DI&DV_Training/28thJuly/winemag-data-130k-v2.csv')

df_clean = df.dropna(subset=['country','price'])

avg_ratings = df_clean.groupby('country')['price'].mean()
avg_rating_sorted = avg_ratings.sort_values(ascending=False)
print(avg_rating_sorted)

top10_countries = avg_rating_sorted.head(10)

plt.figure(figsize=(10, 6))
top10_countries.plot(kind='barh', color='orchid')
plt.xlabel('Average Price')
plt.ylabel('Country')
plt.title('Top 10 Countries by Average Wine Pricing')
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()