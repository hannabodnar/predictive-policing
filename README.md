# Predictive Policing: Utilizing Machine Learning Algorithms to Enhance Crime Prevention Strategies

## Overview

This project explores the applications of machine learning to criminology, focusing on analyzing and predicting crime patterns to improve public safety.
By leveraging data-driven insights, the project aims to assist law enforcement agencies in resource allocation and crime prevention. The project integrates methods like
Exploratory Data Analysis (EDA), predictive modeling, and spatial analysis to uncover actionable insights for strategic decision-making.

## Table of Contents

1. Problem Statement
2. Data Collection and Preprocessing
   * Data Source
   * Data Description
   * Data Cleansing
   * Feature Engineering
3. Methodology
   * Exploratory Data Analysis
   * Model Development and Evaluation
     * Random Forest
     * Spatial Autocorrelation Analysis
     * Time-Series Analysis
4. Key Findings
5. Installation
6. Usage
7. Results
8. Limitations and Future Work
9. Acknowledgments
10. References

## Problem Statement

Crime prediction and prevention are critical to public safety. This project investigates how machine learning can provide proactive solutions for crime
prevention, enabling efficient resource allocation, and reducing criminal activity.

## Data Collection and Preprocessing

### Data Source

The dataset was sourced from the Los Angeles Open Data Portal and features over 932,000 crime records from 2020 to the present.

### Data Description

The dataset contains 28 variables: crime type, date, location, and victim demographics.

### Data Cleaning

Steps included:
  * Removing variables with excessive missing data.
  * Imputing missing values for categorical and numerical variables.
  * Aggregating similar crime descriptions for simplicity.

### Feature Engineering

The date fields were used to create new features, such as year, month, and day, and categorical variables were label-encoded for model compatibility.

## Methodology

### Exploratory Data Analysis

EDA revealed patterns in crime demographics, trends over time, and spatial distributions forming the basis for modeling.

### Model Development and Evaluation

1. **Random Forest:** Predicts area codes based on crime and victim details.
2. **Spatial Autocorrelation Analysis:** Explores crime hotspots and spatial clustering.
3. **TIme-Series Analysis:** Investigate trends, seasonality, and forecasting using SARIMA and STL.

## Key Findings

* Geographic features significantly improve prediction accuracy (up to 99.7% using Random Forest).
* Certain districts exhibit strong spatial autocorrelation, identifying hotspots for focused intervention.
* Time-series analysis highlighted consistent crime rates but increasing trends for specific demographics.

## Results

* Random Forest received an accuracy of 99.77% using all features.
* Moran's I identified significant spatial patterns in districts like Wilshire and Hollywood.
* SARIMA models struggled due to data aggregation, but trends were identified qualitatively.

## Limitations and Future Work

* Time-series aggregation reduced forecasting accuracy.
* The study relies on historical data, which may introduce biases.
* Future work will explore real-time data integration and community-based solutions.

## Acknowledgments

* Data Source: Los Angeles Open Data Portal
* Geospatial Tools: GeoPandas, ArcGIS

## References

