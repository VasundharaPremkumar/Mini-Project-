# Intelligent Crime Analysis & Prediction Platform

An AI/ML-powered crime analysis system developed as a mini project to analyze historical crime data, identify spatial crime patterns, detect potential hotspots, and provide interactive analytics through a web-based platform.

## Project Overview

Traditional crime analysis often relies on manual monitoring and reactive approaches. This project aims to provide a data-driven system that assists in analyzing crime patterns and supporting proactive decision-making.

The system combines machine learning, spatial analysis, database management, and web technologies into an end-to-end crime intelligence platform.

## Key Features

- Crime data collection and preprocessing
- Historical crime data analysis
- Crime pattern and spatial analysis
- Crime-type based matching and prediction
- Geographic hotspot analysis
- Interactive crime statistics and visualization
- Admin authentication portal
- Incident reporting and database storage
- ML model retraining through the backend
- REST APIs for crime analytics and prediction

## Machine Learning

The project explores both supervised and unsupervised machine learning approaches, including:

- Random Forest
- Decision Tree
- K-Nearest Neighbors (KNN)
- K-Means Clustering
- Nearest Neighbors for spatial crime-pattern matching

The system uses historical crime records and geographic coordinates to identify similar crime patterns and provide location-based insights.

## System Workflow

```text
Crime Data
    ↓
Data Collection & Preprocessing
    ↓
MongoDB Database
    ↓
Machine Learning / Spatial Analysis
    ↓
FastAPI Backend
    ↓
Interactive Web Interface
    ↓
Crime Analytics & Decision Support
