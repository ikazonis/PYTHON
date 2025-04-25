# Required Libraries: requests, plotly[express], pandas
# Install them using: pip install requests plotly pandas

import requests
import plotly.express as px

# ------------------------- API REQUEST -------------------------
# Define the GitHub API URL to fetch repositories with more than 10k stars in Python
url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"  # GitHub API query
headers = {"Accept": "application/vnd.github.v3+json"}

# Send GET request to the API
response = requests.get(url, headers=headers)

# Convert response to JSON format
response_dict = response.json()

# Extract repository data from the response
repo_dicts = response_dict["items"]

# Print status code and whether results are incomplete
print("Status code:", response.status_code)
print("Complete results:", not response_dict["incomplete_results"])

# ---------------------- DATA EXTRACTION & FILTERING ----------------------
# Initialize lists for repository names, star counts, and hover texts
repo_names, star_counts, hover_texts = [], [], []

# Loop through each repository to collect relevant data
for repo in repo_dicts:
    # Repository name with a clickable link
    repo_names.append(f"<a href='{repo['html_url']}'>{repo['name']}</a>")
    
    # Star count for each repository
    star_counts.append(repo["stargazers_count"])
    
    # Hover text containing owner info and description
    hover_text = f"{repo['owner']['login']}<br>{repo['description']}"
    hover_texts.append(hover_text)

# -------------------- DATA VISUALIZATION WITH PLOTLY --------------------
# Set up the title and labels for the plot
title = "Most-Starred Python Projects on GitHub"
labels = {"x": "Repositories", "y": "Stars"}

# Create a bar chart using Plotly
fig = px.bar(
    x=repo_names,  # X-axis: Repository names (with links)
    y=star_counts,  # Y-axis: Number of stars
    title=title,    # Chart title
    labels=labels,  # Axis labels
    hover_name=hover_texts  # Hover text with owner and description
)

# Customize the layout and style of the plot
fig.update_layout(title_font_size=28, xaxis_title_font_size=20, yaxis_title_font_size=20)
fig.update_traces(marker_color='gold', marker_opacity=0.6)

# Display the plot
fig.show()