from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load dataset
data = pd.read_csv('ph_dengue_cases2016-2020.csv')

# Initialize Flask app
app = Flask(__name__)

# Prepare data for visualization
def prepare_data():
    # Aggregate data by year and region
    summary = data.groupby(['Year', 'Region']).sum().reset_index()

    # Total cases and deaths
    total_cases = data['Dengue_Cases'].sum()
    total_deaths = data['Dengue_Deaths'].sum()

    # Time series for total cases by year
    yearly_cases = data.groupby('Year')['Dengue_Cases'].sum().reset_index()

    return summary, total_cases, total_deaths, yearly_cases

# Create graphs
def create_graphs(summary, yearly_cases):
    # Line graph: Total dengue cases per year
    fig_line = px.line(yearly_cases, x='Year', y='Dengue_Cases',
                       title='Dengue Cases Over Time', markers=True)

    # Bar chart: Cases and deaths by region
    fig_bar = px.bar(summary, x='Region', y=['Dengue_Cases', 'Dengue_Deaths'],
                     title='Cases and Deaths by Region', barmode='group')

    return fig_line, fig_bar

@app.route('/')
def dashboard():
    # Prepare data
    summary, total_cases, total_deaths, yearly_cases = prepare_data()

    # Generate graphs
    fig_line, fig_bar = create_graphs(summary, yearly_cases)

    # Convert graphs to HTML
    line_graph_html = fig_line.to_html(full_html=False)
    bar_graph_html = fig_bar.to_html(full_html=False)

    return render_template('dashboard.html',
                           total_cases=total_cases,
                           total_deaths=total_deaths,
                           line_graph=line_graph_html,
                           bar_graph=bar_graph_html)

if __name__ == '__main__':
    app.run(debug=True)