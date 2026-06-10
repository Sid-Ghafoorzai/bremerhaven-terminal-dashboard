# Bremerhaven Container Terminal Performance Dashboard

## Project Overview

This project simulates and analyzes operations at a container terminal inspired by the Port of Bremerhaven. The goal is to provide operational insights into vessel handling, container throughput, crane productivity, and terminal efficiency using Power BI.

The project demonstrates end-to-end data analytics skills including:

* Data modeling (Star Schema)
* Synthetic data generation with Python
* Data transformation and validation
* Power BI dashboard development
* KPI design and operational reporting

---

## Business Problem

Container terminals handle thousands of containers and vessel movements every day. Terminal managers require visibility into:

* Container throughput (TEUs)
* Vessel turnaround performance
* Crane productivity
* Operational delays
* Shipping line activity
* Terminal utilization trends

This dashboard provides a centralized view of these operational KPIs.

---

## Project Architecture

### Data Generation

Because detailed operational port data is generally not publicly available, realistic synthetic datasets were generated using Python.

Generated datasets include:

* Vessel Calls
* Container Movements
* Crane Operations

The simulation covers:

* 500 vessel calls
* ~153,000 container movements
* ~1,500 crane operation records
* Two years of activity (2024–2025)

---

## Data Model

The project follows a Star Schema design.

### Fact Tables

#### Fact_VesselCalls

Contains vessel visit information:

* Arrival and departure times
* Berth assignment
* Import/export moves
* Delay information

#### Fact_ContainerMoves

Contains container-level movement data:

* Container type
* Move type
* Dwell time
* TEU value
* Weight

#### Fact_CraneOperations

Contains crane activity data:

* Crane assignments
* Moves completed
* Operating hours

### Dimension Tables

* Dim_Date
* Dim_Vessel
* Dim_ShippingLine
* Dim_Berth
* Dim_Terminal
* Dim_Port
* Dim_Crane
* Dim_ContainerType

---

## Key KPIs

### Throughput Metrics

* Total TEUs
* Total Container Moves
* Total Vessel Calls

### Operational Efficiency

* Average Dwell Time
* Average Vessel Delay
* Crane Productivity

### Customer Analysis

* Throughput by Shipping Line
* Throughput by Vessel

### Time Analysis

* Monthly Throughput Trends
* Seasonal Activity Patterns

---

## Tools & Technologies

### Data Generation

* Python
* Pandas
* NumPy

### Analytics & Visualization

* Power BI
* DAX

### Version Control

* Git
* GitHub

---

## Repository Structure

```text
bremerhaven-terminal-dashboard/
│
├── data/
│   ├── Fact_VesselCalls.csv
│   ├── Fact_ContainerMoves.csv
│   ├── Fact_CraneOperations.csv
│   └── Dimension Tables
│
├── powerbi/
│   └── Bremerhaven_Dashboard.pbix
│
├── python/
│   └── data_simulation.py
│
├── docs/
│   └── dashboard_screenshots/
│
└── README.md
```

---

## Future Improvements

Planned enhancements include:

* Forecasting container throughput
* Vessel delay prediction
* Yard occupancy analysis
* Multi-port comparison
* Real AIS vessel movement integration
* Advanced DAX optimization

---

## Author

This project was developed as part of a professional data analytics portfolio focused on logistics, operations, and business intelligence by Sadaqat Ghafoorzai. M.Sc MIS
