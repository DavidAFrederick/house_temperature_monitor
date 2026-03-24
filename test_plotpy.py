import plotly.express as px

# fig = px.scatter(
#     new_profile[:100],
#     x="followers",
#     y="total_stars",
#     color="forks",
#     size="contribution",
# )
# fig.show()


import plotly.express as px

df = px.data.gapminder().query("country=='Canada'")
print ("==============================")
print (df)
print ("==============================")

fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig.show()

