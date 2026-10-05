# Air Quality Index (AQI) Prediction and Spatial Clustering

**Developed by: Bhumika Nimkar**

## Project Overview

This project focuses on analyzing air-quality data to predict the Air Quality Index (AQI) and identify spatial pollution patterns using Machine Learning and K-Means clustering.

A Flask-based web application has been developed to provide an interactive interface for AQI analysis, prediction, pollution mapping, and spatial clustering.

## Objectives

* Analyze air-quality data using Machine Learning.
* Predict AQI based on major air pollutants.
* Classify AQI into different pollution categories.
* Identify spatial pollution patterns using clustering.
* Visualize AQI and pollution clusters through a web application.

## Pollutants Used

* PM2.5
* PM10
* O3
* NO2
* SO2
* CO

## Machine Learning

The AQI prediction model uses pollutant concentrations as input features.

For spatial clustering, K-Means clustering is applied using:

* Latitude
* Longitude
* AQI

Three pollution clusters are identified:

* High Pollution
* Moderate Pollution
* Low Pollution

## Model Performance

| Metric   | Result |
| -------- | -----: |
| MAE      |   7.76 |
| MSE      | 200.26 |
| R² Score |  0.922 |

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Flask
* HTML
* CSS
* OpenPyXL
* Joblib
* Gunicorn

## Website Features

* Dashboard
* AQI Analysis
* AQI Prediction
* Pollution Map
* Pollutant Analysis
* Spatial Clustering
* Dataset Information
* About Project

## Project Structure

```text
app.py
aqi_model.pkl
airpollution.xlsx
requirements.txt
templates/
static/
```

## Live Website

https://aqi-prediction-and-spatial-clustering.onrender.com

## Developer

**Bhumika Nimkar**

