import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


df = pd.read_csv('data/netflix_titles.csv')
# print(df.head())
# print(df.tail())
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())
# print(df.duplicated().sum())


# df['director'] = df['director'].fillna('Unknown')
# df['cast'] = df['cast'].fillna('Unknown')
# df['country'] = df['country'].fillna('Unknown')
# df.dropna(subset=['date_added', 'duration'], inplace=True)
# df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
# df["date_added"] = df["date_added"].str.strip()
# df['date_added'] = pd.to_datetime(df['date_added'])
df.to_csv('data/netflix_titles_cleaned.csv', index=False)


# print(df.isnull().sum())
# print(df.dtypes)
# print(df.shape)
# print(df['date_added'].head())
# print(df.shape)
# print(df.info())
# print(df.isnull().sum())
# print(df.duplicated().sum())


# ax = sns.countplot(x='type', data=df)
# plt.title('Movies vs TV Shows on Netflix')
# for container in ax.containers:
#     ax.bar_label(container, fontsize=11)
# plt.show()


# type chart
# type
# sns.set_style("whitegrid")  # changes the bg  into grid
# sns.set_palette("Set2")    # set the color palette for the plot

# plt.figure(figsize=(8, 5))   # width and height of the plot

# ax = sns.countplot(data=df, x="type")

# for container in ax.containers:
#     ax.bar_label(container, fontsize=11)

# plt.title("Distribution of Movies and TV Shows on Netflix",
#           fontsize=18,
#           fontweight="bold")

# plt.xlabel("Content Type", fontsize=13)
# plt.ylabel("Number of Titles", fontsize=13)

# sns.despine()   # will remove the top and right spines from the plot
# plt.tight_layout()
# plt.show()


# RELEASE YEAR
# release_counts = df["release_year"].value_counts().sort_index()

# plt.figure(figsize=(12, 6))

# ax = sns.lineplot(
#     x=release_counts.index,
#     y=release_counts.values,
#     marker="o",
#     linewidth=2.5,
#     color="royalblue"
# )

# plt.title("Netflix Titles Released by Year",
#           fontsize=18,
#           fontweight="bold")

# plt.xlabel("Release Year", fontsize=13)
# plt.ylabel("Number of Titles", fontsize=13)

# plt.grid(alpha=0.3)

# plt.tight_layout()
# plt.show()


# RATINGS

# plt.figure(figsize=(12, 6))
# sns.histplot(df['rating'], color='skyblue')


# plt.title("Distribution of Ratings on Netflix",
#           fontsize=18,
#           fontweight="bold")

# plt.xlabel("Ratings", fontsize=13, fontweight="bold")
# plt.ylabel("Number of Titles", fontsize=13, fontweight="bold")

# sns.despine()
# plt.tight_layout()
# plt.show()


# Country


# plt.figure(figsize=(12, 6))
# ax = sns.countplot(data=df, y="country",
#                    order=df["country"].value_counts().head(10).index,
#                    palette="viridis")

# for container in ax.containers:
#     ax.bar_label(container, fontsize=11)

# plt.title("Top 10 Countries with Most Netflix Titles",
#           fontsize=18,
#           fontweight="bold")

# plt.xlabel("Number of Titles", fontsize=13, fontweight="bold")
# plt.ylabel("Country", fontsize=13, fontweight="bold")
# sns.despine()
# plt.tight_layout()
# plt.show()

# listed_in


# plt.figure(figsize=(12, 6))
# abc = df['listed_in'] = df['listed_in'].str.split(
#     ', ').explode().value_counts().head(10)
# ax = sns.barplot(x=abc.values, y=abc.index, hue=abc.index, palette="viridis")


# for container in ax.containers:
#     ax.bar_label(container, fontsize=11)

# plt.title("Top 10 Genres with Most Netflix Titles",
#           fontsize=18,
#           fontweight="bold")

# plt.xlabel("Number of Titles", fontsize=13, fontweight="bold")
# plt.ylabel("Genre", fontsize=13, fontweight="bold")
# plt.grid(axis='x', alpha=0.3)
# plt.tight_layout()
# plt.show()

# Duration


# Movies
# movies = df[df['type'] == 'Movie'].copy()

# movies['movie_duration'] = (
#     movies['duration']
#     .str.replace(' min', '')
#     .astype(int)
# )

# # TV Shows
# tv = df[df['type'] == 'TV Show'].copy()

# tv['tv_duration'] = (
#     tv['duration']
#     .str.extract(r'(\d+)')
#     .astype(int)
# )

# # print(movies[['duration', 'movie_duration']].head())
# # print(tv[['duration', 'tv_duration']].head())


# plt.figure(figsize=(8, 5))

# sns.boxplot(
#     y=movies["movie_duration"],
#     color="skyblue"
# )

# plt.title("Distribution of Movie Durations",
#           fontsize=16,
#           fontweight="bold")

# plt.ylabel("Duration (Minutes)")

# plt.show()


# plt.figure(figsize=(8, 5))

# sns.boxplot(
#     y=tv["tv_duration"],
#     color="skyblue"
# )

# plt.title("Distribution of TV Durations",
#           fontsize=16,
#           fontweight="bold")

# plt.ylabel("Duration (Sessions)")

# plt.show()


# print(df[['rating', 'type']].dtypes)


#                             bivariate variables
# print(df[['rating', 'type']].dtypes)

# plt.figure(figsize=(10, 6))
# sns.countplot(data=df, x='rating', hue='type')
# plt.title("Type of Content by Rating",
#           fontsize=18,
#           fontweight="bold")
# plt.show()


# top_countries = df['country'].value_counts().head(10).index

# plt.figure(figsize=(12, 6))
# sns.countplot(
#     data=df[df['country'].isin(top_countries)],
#     x='country',
#     hue='type'
# )
# plt.xticks(rotation=45)
# plt.title("Top 10 Countries by Content Type",
#           fontsize=18,
#           fontweight="bold")
# plt.show()


# print(df[['release_year', 'type']].dtypes)


# sns.boxplot(data=df, x='type', y='release_year')

# plt.title("Release Year Distribution by Content Type",
#           fontsize=18,
#           fontweight="bold")

# plt.show()


# sns.boxplot(data=movies, x='rating', y='movie_duration')

# plt.xticks(rotation=45)
# plt.title("Movie Duration by Rating")
# plt.show()


# fig = px.histogram(df, x='type')
# fig.show()
