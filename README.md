# Gapminder

An interactive bubble chart built with Streamlit, similar to Gapminder.

## Live Demo
http://gapminder.167.233.63.59.nip.io

## Features
- Interactive bubble chart with GNI per capita, life expectancy, and population
- Year slider with play button animation
- Country multi-select filter

## Run locally
streamlit run app/app.py

## Docker
docker build -t gapminder .
docker run -p 8501:8501 gapminder
