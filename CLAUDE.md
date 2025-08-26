# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains course materials and examples for "Claude Code: A Highly Agentic Coding Assistant" course. It includes practical examples demonstrating Claude Code capabilities through hands-on projects.

## Project Structure

The repository is organized into several key areas:

- `lesson7_files/` - Complete e-commerce data analysis project with Python modules and Streamlit dashboard
- `reading_notes/` - Lesson notes and course documentation
- `additional_files/` - Supplementary course materials (Figma files, visualizations)
- `links_to_course_repos.md` - References to external course repositories

## Development Commands

### Python Environment Setup
```bash
# Navigate to the lesson7 project directory
cd lesson7_files/

# Install required dependencies
pip install -r requirements.txt
```

### Running the Streamlit Dashboard
```bash
# From the lesson7_files directory
streamlit run dashboard.py
```

### Running Jupyter Notebooks
```bash
# Launch Jupyter for analysis notebooks
jupyter notebook EDA_Refactored.ipynb
```

## Code Architecture

### E-commerce Analytics Project (lesson7_files/)

The lesson7 project demonstrates a professional business intelligence framework with three main modules:

#### Data Loading (`data_loader.py`)
- `EcommerceDataLoader` class handles CSV data ingestion from `ecommerce_data/` directory
- Processes orders, order items, products, customers, reviews, and payments datasets
- Provides filtering capabilities by year, month, and order status
- Creates comprehensive sales datasets through intelligent table joins

#### Business Metrics (`business_metrics.py`)
- `BusinessMetricsCalculator` class computes key business KPIs
- `MetricsVisualizer` class creates professional charts and visualizations
- Supports revenue analysis, product performance, geographic insights, and customer satisfaction metrics
- Includes year-over-year comparison functionality

#### Dashboard (`dashboard.py`)
- Professional Streamlit application with responsive design
- Interactive filtering by year and month
- KPI cards with trend indicators
- 2x2 chart grid layout featuring revenue trends, category performance, geographic analysis, and customer satisfaction
- Real-time data updates based on filter selections

### Data Flow
1. Raw CSV files in `ecommerce_data/` directory
2. `EcommerceDataLoader` processes and joins datasets
3. `BusinessMetricsCalculator` computes metrics from processed data
4. Streamlit dashboard displays interactive visualizations and KPIs

## Key Features

### Configurable Analysis
- Time period filtering (year/month) without code changes
- Order status filtering (delivered, shipped, etc.)
- Comparison analysis between different time periods

### Professional Visualizations
- Plotly-based interactive charts
- Geographic choropleth maps for state-level analysis
- Consistent color schemes and business-ready styling
- Currency formatting with K/M suffixes for readability

### Modular Design
- Reusable data loading and metrics calculation modules
- Separation of concerns between data processing and visualization
- Easy extension for additional metrics or data sources

## Data Requirements

The e-commerce project expects CSV files in `lesson7_files/ecommerce_data/`:
- `orders_dataset.csv`
- `order_items_dataset.csv`
- `products_dataset.csv`
- `customers_dataset.csv`
- `order_reviews_dataset.csv`
- `order_payments_dataset.csv`

## Python Dependencies

Key packages used in the e-commerce analysis:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Basic plotting
- `seaborn` - Statistical visualization
- `plotly` - Interactive visualizations
- `streamlit` - Web application framework
- `jupyter` - Notebook environment

## Course Context

This repository serves as practical examples for learning Claude Code workflows:
- Codebase understanding and analysis
- Feature addition and enhancement
- Testing and debugging
- Refactoring Jupyter notebooks into production-ready modules
- Creating professional dashboards from exploratory analysis