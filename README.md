# Automated Production Planning & Performance Analytics

An integrated production monitoring and analytics solution developed to improve production plan tracking, automate data collection, and analyze machine performance using Python, Microsoft Excel, and Power BI.

## Project Overview

This project focuses on developing an integrated system for monitoring Production Plan Achievement (PPA), identifying the causes of production deviations, and analyzing historical machine performance.

The solution combines automated data collection with interactive business intelligence dashboards to provide better visibility into production operations and support data-driven decision-making.

## Project Workflow

The project was implemented in three main stages:

### 1. Production KPI Development

- Defined a Production Plan Achievement KPI to measure the percentage of actual production against planned production for each machine on a daily basis.
- Developed a structured process for recording and categorizing reasons for production plan deviations.
- Established historical records of operational issues and recurring production disruptions.

### 2. Data Collection Automation

- Developed Python scripts to automate the extraction of planned and actual production quantities for each machine.
- Automated Excel data updates, eliminating manual data entry and improving data consistency and reporting efficiency.

### 3. Power BI Dashboard Development

Designed a multi-page interactive Power BI dashboard with the following capabilities:

- **Production Plan Achievement:** Monitoring daily and long-term production plan fulfillment.
- **Deviation Analysis:** Identifying and analyzing the most frequent reasons for production plan deviations.
- **Performance Trends:** Tracking production performance over different time periods.
- **Machine History:** Exploring historical machine activities, manufactured products, production quantities, breakdowns, and downtime.
- **Machine Comparison:** Comparing machine performance and identifying recurring operational issues.


## Technologies & Tools

- **Power BI:** Interactive dashboards, KPI development, and performance analytics.
- **Python:** Data extraction and process automation.
- **Microsoft Excel:** Data storage and automated reporting.
- **DAX:** KPI calculations and analytical measures.

## Repository Structure

```text
Production-Planning-Analytics/
│
├── README.md
│
├── PowerBI/
│   └── PPC_Performance_Dashboard.pdf
│
├── Python/
   └── Production_Data_Automation.py
```

## Project Objective

To improve production performance visibility, reduce manual reporting activities, identify the main causes of production deviations, and support more effective production planning and operational decision-making.
