import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

@st.cache_data
def load_data():
    lex = pd.read_csv('lex.csv', index_col=0)
    pop = pd.read_csv('pop.csv', index_col=0)
    gni = pd.read_csv('ny_gnp_pcap_pp_kd.csv', index_col=0).drop(columns=['name'])

    lex = lex.ffill(axis=1)
    pop = pop.ffill(axis=1)
    gni = gni.ffill(axis=1)

    lex = lex.reset_index().melt(id_vars='geo', var_name='year', value_name='life_expectancy')
    pop = pop.reset_index().melt(id_vars='geo', var_name='year', value_name='population')
    gni = gni.reset_index().melt(id_vars='geo', var_name='year', value_name='gni_per_capita')

    lex = lex[pd.to_numeric(lex['year'], errors='coerce').notna()]
    pop = pop[pd.to_numeric(pop['year'], errors='coerce').notna()]
    gni = gni[pd.to_numeric(gni['year'], errors='coerce').notna()]

    lex['year'] = lex['year'].astype(int)
    pop['year'] = pop['year'].astype(int)
    gni['year'] = gni['year'].astype(int)

    df = lex.merge(pop, on=['geo', 'year']).merge(gni, on=['geo', 'year'])
    df['gni_per_capita'] = pd.to_numeric(df['gni_per_capita'], errors='coerce')
    df['population'] = pd.to_numeric(df['population'], errors='coerce')
    df['life_expectancy'] = pd.to_numeric(df['life_expectancy'], errors='coerce')
    df = df.dropna()
    return df

df = load_data()

all_countries = sorted(df['geo'].unique().tolist())
selected_countries = st.multiselect('Select countries', all_countries, default=all_countries[:20])

min_year = int(df['year'].min())
max_year = int(df['year'].max())

col1, col2 = st.columns([3, 1])
with col1:
    selected_year = st.slider('Year', min_year, max_year, min_year, step=1)
with col2:
    play = st.button('▶ Play')

max_gni = df['gni_per_capita'].max()

def make_chart(year):
    filtered = df[df['geo'].isin(selected_countries) & (df['year'] == year)]
    fig = px.scatter(
        filtered,
        x='gni_per_capita',
        y='life_expectancy',
        size='population',
        color='geo',
        hover_name='geo',
        log_x=True,
        size_max=60,
        range_x=[100, max_gni * 1.1],
        range_y=[20, 90],
        title=f'Year: {year}',
        labels={
            'gni_per_capita': 'GNI per Capita (PPP, log scale)',
            'life_expectancy': 'Life Expectancy',
            'population': 'Population'
        }
    )
    fig.update_layout(height=600, showlegend=False)
    return fig

chart = st.empty()

if play:
    for year in range(selected_year, max_year + 1):
        chart.plotly_chart(make_chart(year), use_container_width=True)
        time.sleep(0.3)
else:
    chart.plotly_chart(make_chart(selected_year), use_container_width=True)
    