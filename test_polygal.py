# pip install pygal

import pygal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


new_profile = pd.read_csv(
    "https://gist.githubusercontent.com/khuyentran1401/98658198f0ef0cb12abb34b4f2361fd8/raw/ece16eb32e1b41f5f20c894fb72a4c198e86a5ea/github_users.csv"
)

# Create a bar chart showing top GitHub users by followers
top_followers = new_profile.sort_values(by="followers", ascending=False)[:10]

bar_chart = pygal.Bar(
    title='Top 10 GitHub Users by Followers',
    x_title='Users',
    y_title='Followers'
)
bar_chart.x_labels = top_followers['user_name'].tolist()
bar_chart.add('Followers', top_followers['followers'].tolist())

# Save chart as SVG file
bar_chart.render_to_file('github_top_users.svg')
