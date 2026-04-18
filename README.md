# 🌽 Effects of Climate Change on Maize Yield in Eswatini (1993–2023)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)

## 📌 Project Overview
This project investigates how climate change variables  temperature, rainfall, 
and carbon emissions  have affected maize yield in Eswatini over a 30-year period 
(1993–2023). The analysis combines statistical methods, machine learning, and 
interactive visualizations to uncover meaningful patterns and forecast future yield trends.

---

## 🎯 Objectives
- Analyze trends in maize yield alongside key climate variables
- Measure the strength of relationships between climate and yield
- Build predictive models to explain yield variation
- Forecast maize yield through 2031 based on historical climate trends

---

## 📂 Project Structure
├── data/
│   ├── raw/                  # Original Excel dataset
│   └── processed/            # Cleaned CSV dataset
├── visuals/
│   ├── trend_plots.png
│   ├── correlation_heatmap.png
│   ├── regression_actual_vs_predicted.png
│   ├── scatter_plots.png
│   ├── decade_averages.png
│   ├── rf_actual_vs_predicted.png
│   ├── feature_importance.png
│   ├── yield_forecast.png
│   └── interactive_dashboard.html
├── hello.py                  # Main analysis script
└── README.md

---

## 📊 Dataset
| Variable | Description | Unit |
|----------|-------------|------|
| Year | 1993 to 2023 | — |
| Production | Total maize produced | Metric tonnes |
| Area | Land under maize cultivation | Hectares |
| Yield | Maize yield per hectare | t/ha |
| Rainfall | Annual rainfall | mm |
| Temperature | Average annual temperature | °C |
| Carbon | Carbon emissions | Mt CO₂ |

---

## 🔧 Tools & Libraries
- **Python** — pandas, numpy, matplotlib, seaborn, scikit-learn, plotly

---

## 📈 Methodology
1. **Data Cleaning** — standardized column names, verified data types, checked for missing values
2. **Exploratory Data Analysis** — time series trends for all variables
3. **Correlation Analysis** — measured relationships between climate variables and yield
4. **Linear Regression** — modelled yield as a function of climate variables
5. **Random Forest** — applied ensemble ML model and compared performance
6. **Feature Importance** — identified which climate variable drives yield most
7. **Forecasting** — projected yield through 2031 using historical climate trends

---

## 🔑 Key Findings
- 🌧️ **Rainfall is the strongest driver** of maize yield (correlation: +0.51)
- 🌡️ **Rising temperatures negatively affect yield** (correlation: -0.37)
- 📉 **2016 recorded the lowest yield** (0.73 t/ha) coinciding with the severe El Niño drought
- 📈 **1996 recorded the highest yield** (2.21 t/ha)
- 🤖 Climate variables explain **30.8% of yield variation** — remaining variation attributed to farming practices, soil quality and policy factors
- 🔮 **Yield is projected to decline gradually through 2031** if current climate trends continue

---

## ⚠️ Model Performance
| Model | R² Score | RMSE |
|-------|----------|------|
| Linear Regression | 30.8% | 0.2618 t/ha |
| Random Forest | 22.7% | 0.2594 t/ha |

> Linear Regression outperformed Random Forest due to the limited dataset size 
> of 31 observations, which is insufficient for ensemble methods to generalise effectively.

---

## 🔮 Yield Forecast (2024–2031)
| Year | Temp (°C) | Rainfall (mm) | Forecast Yield (t/ha) |
|------|-----------|---------------|----------------------|
| 2024 | 20.69 | 927.29 | 1.3281 |
| 2025 | 20.73 | 927.53 | 1.3270 |
| 2026 | 20.76 | 927.76 | 1.3259 |
| 2027 | 20.80 | 927.99 | 1.3248 |
| 2028 | 20.83 | 928.22 | 1.3237 |
| 2029 | 20.87 | 928.46 | 1.3227 |
| 2030 | 20.90 | 928.69 | 1.3216 |
| 2031 | 20.93 | 928.92 | 1.3205 |

> ⚠️ Forecasts assume historical climate trends continue. Uncertainty increases beyond 2028.

---

## 💡 Recommendations
- Invest in **irrigation infrastructure** to reduce rain-fed dependency
- Promote **drought-resistant maize varieties** suited for rising temperatures
- Strengthen **early warning systems** tied to seasonal rainfall forecasts
- Conduct further research incorporating **soil quality and farming practice data**

---

## 👤 Author
**Your Name**
- 📧 mlandvothwala@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/Mlandvo Thwala)
- 🐙 [GitHub](https://github.com/iNshiva)

---

## 📜 License
This project is licensed under the MIT License.
