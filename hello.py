import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ════════════════════════════════════════
# 🔧 SETTINGS — control your plots here
# ════════════════════════════════════════

SHOW_PLOTS = False  # Change to True if you want to see plots, False to skip

# ════════════════════════════════════════
# PHASE 1 — LOAD & CLEAN DATA
# ════════════════════════════════════════

# Create folders if they don't exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("visuals", exist_ok=True)

# Load raw Excel file
df = pd.read_excel("data/raw/Data 1.xlsx")

# Clean column names
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# Rename columns
df.rename(columns={
    'production_(mt)': 'production',
    'area_planted_(ha)': 'area',
    'yield_per_ha': 'yield',
    'rainfall_(mm)': 'rainfall'
}, inplace=True)

# Save cleaned data
df.to_csv("data/processed/clean_maize_climate.csv", index=False)
print("✅ Phase 1 done — Data cleaned and saved!")

# ════════════════════════════════════════
# PHASE 2 — TREND PLOTS
# ════════════════════════════════════════

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Maize & Climate Trends in Eswatini (1993–2023)',
             fontsize=16, fontweight='bold')

# Maize Yield
axes[0, 0].plot(df['year'], df['yield'], color='green', marker='o', linewidth=2)
axes[0, 0].set_title('Maize Yield (t/ha)')
axes[0, 0].set_xlabel('Year')
axes[0, 0].set_ylabel('Yield (t/ha)')

# Temperature
axes[0, 1].plot(df['year'], df['temperature'], color='red', marker='o', linewidth=2)
axes[0, 1].set_title('Average Temperature (°C)')
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('Temperature (°C)')

# Rainfall
axes[1, 0].plot(df['year'], df['rainfall'], color='blue', marker='o', linewidth=2)
axes[1, 0].set_title('Annual Rainfall (mm)')
axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Rainfall (mm)')

# Carbon Emissions
axes[1, 1].plot(df['year'], df['carbon'], color='gray', marker='o', linewidth=2)
axes[1, 1].set_title('Carbon Emissions (Mt CO₂)')
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Carbon (Mt CO₂)')

plt.tight_layout()
plt.savefig('visuals/trend_plots.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:       # ← if switch is ON, show the plot on screen
    plt.show()
else:                # ← if switch is OFF, just move on
    plt.close()

print("✅ Phase 2 done — Trend plots saved!")

# ════════════════════════════════════════
# PHASE 3 — CORRELATION ANALYSIS
# ════════════════════════════════════════

# Select only the climate and yield columns
corr_data = df[['yield', 'temperature', 'rainfall', 'carbon']]

# Calculate correlation matrix
corr_matrix = corr_data.corr()

print("\n📊 Correlation Matrix:")
print(corr_matrix)

# Plot heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix,
            annot=True,          # show numbers on the chart
            cmap='RdYlGn',       # red = negative, green = positive
            fmt='.2f',           # round to 2 decimal places
            linewidths=0.5,
            ax=ax)

ax.set_title('Correlation Between Maize Yield & Climate Variables\nEswatini (1993–2023)',
             fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('visuals/correlation_heatmap.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:       # ← same switch controls this plot too
    plt.show()
else:
    plt.close()

print("✅ Phase 3 done — Correlation heatmap saved!")
# ════════════════════════════════════════
# PHASE 4 — REGRESSION ANALYSIS
# ════════════════════════════════════════

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Define our variables
# X = climate variables (what we use to predict)
# y = maize yield (what we are predicting)
X = df[['temperature', 'rainfall', 'carbon']]
y = df['yield']

# Build the regression model
model = LinearRegression()
model.fit(X, y)

# Get predictions
y_pred = model.predict(X)

# ── Model Performance
r2 = r2_score(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print("\n📈 Regression Results:")
print(f"   R² Score  : {r2:.4f}  → model explains {r2*100:.1f}% of yield variation")
print(f"   RMSE      : {rmse:.4f} t/ha")

# ── Coefficients (how much each variable affects yield)
print("\n🔍 How each climate variable affects yield:")
for name, coef in zip(X.columns, model.coef_):
    direction = "increases" if coef > 0 else "decreases"
    print(f"   {name:<15} → {coef:.4f}  (yield {direction} by {abs(coef):.4f} t/ha per unit)")

print(f"\n   Intercept : {model.intercept_:.4f}")

# ── Plot Actual vs Predicted Yield
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df['year'], y, color='green', marker='o',
        linewidth=2, label='Actual Yield')
ax.plot(df['year'], y_pred, color='orange', marker='s',
        linewidth=2, linestyle='--', label='Predicted Yield')

ax.set_title('Actual vs Predicted Maize Yield in Eswatini (1993–2023)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Yield (t/ha)')
ax.legend()

plt.tight_layout()
plt.savefig('visuals/regression_actual_vs_predicted.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("✅ Phase 4 done — Regression analysis complete!")
# ════════════════════════════════════════
# PHASE 5 — FINAL VISUALIZATIONS
# ════════════════════════════════════════

# ── 1. Scatter plots — Yield vs each climate variable
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Maize Yield vs Climate Variables in Eswatini (1993–2023)',
             fontsize=14, fontweight='bold')

# Yield vs Temperature
axes[0].scatter(df['temperature'], df['yield'], color='red', alpha=0.7, edgecolors='black')
z = np.polyfit(df['temperature'], df['yield'], 1)
p = np.poly1d(z)
axes[0].plot(sorted(df['temperature']), p(sorted(df['temperature'])),
             color='darkred', linestyle='--', linewidth=2)
axes[0].set_title('Yield vs Temperature')
axes[0].set_xlabel('Temperature (°C)')
axes[0].set_ylabel('Yield (t/ha)')

# Yield vs Rainfall
axes[1].scatter(df['rainfall'], df['yield'], color='blue', alpha=0.7, edgecolors='black')
z = np.polyfit(df['rainfall'], df['yield'], 1)
p = np.poly1d(z)
axes[1].plot(sorted(df['rainfall']), p(sorted(df['rainfall'])),
             color='darkblue', linestyle='--', linewidth=2)
axes[1].set_title('Yield vs Rainfall')
axes[1].set_xlabel('Rainfall (mm)')
axes[1].set_ylabel('Yield (t/ha)')

# Yield vs Carbon
axes[2].scatter(df['carbon'], df['yield'], color='gray', alpha=0.7, edgecolors='black')
z = np.polyfit(df['carbon'], df['yield'], 1)
p = np.poly1d(z)
axes[2].plot(sorted(df['carbon']), p(sorted(df['carbon'])),
             color='black', linestyle='--', linewidth=2)
axes[2].set_title('Yield vs Carbon Emissions')
axes[2].set_xlabel('Carbon (Mt CO₂)')
axes[2].set_ylabel('Yield (t/ha)')

plt.tight_layout()
plt.savefig('visuals/scatter_plots.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("✅ Scatter plots saved!")

# ── 2. Decade average comparison
df['decade'] = pd.cut(df['year'],
                      bins=[1992, 2000, 2010, 2020, 2023],
                      labels=['1993-2000', '2001-2010', '2011-2020', '2021-2023'])

decade_avg = df.groupby('decade', observed=True)[['yield', 'temperature', 'rainfall']].mean()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Decade Averages — Yield, Temperature & Rainfall',
             fontsize=14, fontweight='bold')

# Average Yield per decade
axes[0].bar(decade_avg.index, decade_avg['yield'],
            color=['#2ecc71', '#27ae60', '#1e8449', '#145a32'])
axes[0].set_title('Average Maize Yield')
axes[0].set_xlabel('Decade')
axes[0].set_ylabel('Yield (t/ha)')

# Average Temperature per decade
axes[1].bar(decade_avg.index, decade_avg['temperature'],
            color=['#e74c3c', '#c0392b', '#a93226', '#922b21'])
axes[1].set_title('Average Temperature')
axes[1].set_xlabel('Decade')
axes[1].set_ylabel('Temperature (°C)')

# Average Rainfall per decade
axes[2].bar(decade_avg.index, decade_avg['rainfall'],
            color=['#3498db', '#2980b9', '#1f618d', '#154360'])
axes[2].set_title('Average Rainfall')
axes[2].set_xlabel('Decade')
axes[2].set_ylabel('Rainfall (mm)')

plt.tight_layout()
plt.savefig('visuals/decade_averages.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("✅ Decade averages chart saved!")

# ── 3. Summary print
print("\n" + "="*50)
print("📋 PROJECT SUMMARY")
print("="*50)
print(f"   Period analysed     : 1993 - 2023")
print(f"   Average yield       : {df['yield'].mean():.2f} t/ha")
print(f"   Highest yield year  : {df.loc[df['yield'].idxmax(), 'year']} ({df['yield'].max():.2f} t/ha)")
print(f"   Lowest yield year   : {df.loc[df['yield'].idxmin(), 'year']} ({df['yield'].min():.2f} t/ha)")
print(f"   Avg temperature     : {df['temperature'].mean():.2f} °C")
print(f"   Avg rainfall        : {df['rainfall'].mean():.2f} mm")
print(f"   R² of climate model : {r2*100:.1f}%")
print("="*50)
print("\n🎉 All phases complete! Project ready for GitHub!")
# ════════════════════════════════════════
# PHASE 6 — RANDOM FOREST ML MODEL
# ════════════════════════════════════════

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# Define variables
X = df[['temperature', 'rainfall', 'carbon']]
y = df['yield']

# Split data — 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_rf = rf_model.predict(X_test)

# Model performance
r2_rf = r2_score(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))

print("\n🌲 Random Forest Results:")
print(f"   R² Score : {r2_rf:.4f}  → model explains {r2_rf*100:.1f}% of yield variation")
print(f"   RMSE     : {rmse_rf:.4f} t/ha")
print(f"\n   Comparing models:")
print(f"   Linear Regression R²  : {r2*100:.1f}%")
print(f"   Random Forest R²      : {r2_rf*100:.1f}%")

# Plot Actual vs Predicted
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(y_test.values, color='green', marker='o',
        linewidth=2, label='Actual Yield')
ax.plot(y_pred_rf, color='purple', marker='s',
        linewidth=2, linestyle='--', label='RF Predicted Yield')

ax.set_title('Random Forest — Actual vs Predicted Maize Yield',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Test Samples')
ax.set_ylabel('Yield (t/ha)')
ax.legend()

plt.tight_layout()
plt.savefig('visuals/rf_actual_vs_predicted.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("✅ Phase 6 done — Random Forest model complete!")
# ════════════════════════════════════════
# PHASE 7 — FEATURE IMPORTANCE CHART
# ════════════════════════════════════════

# Get feature importance from our Random Forest model
feature_names = ['Temperature', 'Rainfall', 'Carbon']
importances = rf_model.feature_importances_

# Sort from highest to lowest
indices = np.argsort(importances)[::-1]
sorted_features = [feature_names[i] for i in indices]
sorted_importances = importances[indices]

# Print results
print("\n🔍 Feature Importance Results:")
for feature, importance in zip(sorted_features, sorted_importances):
    bar = '█' * int(importance * 50)
    print(f"   {feature:<15} : {importance:.4f} {bar}")

# Plot
fig, ax = plt.subplots(figsize=(8, 5))

colors = ['#e74c3c', '#3498db', '#95a5a6']
bars = ax.barh(sorted_features, sorted_importances, color=colors, edgecolor='black')

# Add value labels on bars
for bar, val in zip(bars, sorted_importances):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:.4f}', va='center', fontweight='bold')

ax.set_title('Feature Importance — Which Climate Variable\nAffects Maize Yield Most?',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Importance Score')
ax.set_xlim(0, max(sorted_importances) + 0.08)

plt.tight_layout()
plt.savefig('visuals/feature_importance.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("✅ Phase 7 done — Feature importance chart saved!")
# ════════════════════════════════════════
# PHASE 8 — FUTURE YIELD FORECAST (2024-2031)
# ════════════════════════════════════════

from sklearn.linear_model import LinearRegression

# ── Build trend models for each climate variable
# We use year to predict future climate variables first
year_array = df['year'].values.reshape(-1, 1)

# Train trend models
temp_model = LinearRegression().fit(year_array, df['temperature'])
rain_model = LinearRegression().fit(year_array, df['rainfall'])
carbon_model = LinearRegression().fit(year_array, df['carbon'])

# ── Generate future years
future_years = np.array(range(2024, 2032)).reshape(-1, 1)

# ── Predict future climate variables based on historical trends
future_temp = temp_model.predict(future_years)
future_rain = rain_model.predict(future_years)
future_carbon = carbon_model.predict(future_years)

# ── Predict future maize yield using our regression model
future_X = pd.DataFrame({
    'temperature': future_temp,
    'rainfall': future_rain,
    'carbon': future_carbon
})

future_yield = model.predict(future_X)

# ── Print forecast results
print("\n🔮 Maize Yield Forecast (2024-2031):")
print(f"   {'Year':<8} {'Temp (°C)':<12} {'Rainfall (mm)':<16} {'Yield (t/ha)'}")
print("   " + "-"*50)
for i, year in enumerate(range(2024, 2032)):
    print(f"   {year:<8} {future_temp[i]:<12.2f} {future_rain[i]:<16.2f} {future_yield[i]:.4f}")

# ── Plot historical + forecast
fig, ax = plt.subplots(figsize=(12, 6))

# Historical yield
ax.plot(df['year'], df['yield'], color='green', marker='o',
        linewidth=2, label='Historical Yield')

# Forecast yield
ax.plot(range(2024, 2032), future_yield, color='orange', marker='s',
        linewidth=2, linestyle='--', label='Forecasted Yield')

# Add uncertainty band around forecast
ax.fill_between(range(2024, 2032),
                future_yield - 0.2,
                future_yield + 0.2,
                color='orange', alpha=0.2, label='Uncertainty Band')

# Add a vertical line separating historical from forecast
ax.axvline(x=2023, color='gray', linestyle=':', linewidth=2, label='Forecast Start')

ax.set_title('Maize Yield — Historical & Forecast (1993–2031)\nEswatini',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Yield (t/ha)')
ax.legend()

plt.tight_layout()
plt.savefig('visuals/yield_forecast.png', dpi=150, bbox_inches='tight')

if SHOW_PLOTS:
    plt.show()
else:
    plt.close()

print("\n⚠️  Note: Forecasts assume historical climate trends continue.")
print("         Uncertainty increases significantly beyond 2028.")
print("✅ Phase 8 done — Yield forecast complete!")
# ════════════════════════════════════════
# PHASE 9 — INTERACTIVE TABBED DASHBOARD
# ════════════════════════════════════════

import plotly.graph_objects as go

# ── Tab 1: Maize Yield Over Time
tab1 = go.Figure()
tab1.add_trace(
    go.Scatter(x=df['year'], y=df['yield'],
               mode='lines+markers',
               name='Maize Yield',
               line=dict(color='green', width=2),
               marker=dict(size=8),
               hovertemplate='Year: %{x}<br>Yield: %{y:.2f} t/ha')
)
tab1.update_layout(
    title='🌽 Maize Yield Over Time (1993–2023)',
    xaxis_title='Year',
    yaxis_title='Yield (t/ha)',
    template='plotly_white',
    height=500
)

# ── Tab 2: Temperature Over Time
tab2 = go.Figure()
tab2.add_trace(
    go.Scatter(x=df['year'], y=df['temperature'],
               mode='lines+markers',
               name='Temperature',
               line=dict(color='red', width=2),
               marker=dict(size=8),
               hovertemplate='Year: %{x}<br>Temp: %{y:.2f} °C')
)
tab2.update_layout(
    title='🌡️ Average Temperature Over Time (1993–2023)',
    xaxis_title='Year',
    yaxis_title='Temperature (°C)',
    template='plotly_white',
    height=500
)

# ── Tab 3: Rainfall Over Time
tab3 = go.Figure()
tab3.add_trace(
    go.Scatter(x=df['year'], y=df['rainfall'],
               mode='lines+markers',
               name='Rainfall',
               line=dict(color='blue', width=2),
               marker=dict(size=8),
               hovertemplate='Year: %{x}<br>Rainfall: %{y:.2f} mm')
)
tab3.update_layout(
    title='🌧️ Annual Rainfall Over Time (1993–2023)',
    xaxis_title='Year',
    yaxis_title='Rainfall (mm)',
    template='plotly_white',
    height=500
)

# ── Tab 4: Correlation Heatmap
corr_vars = ['yield', 'temperature', 'rainfall', 'carbon']
corr_matrix = df[corr_vars].corr()

tab4 = go.Figure()
tab4.add_trace(
    go.Heatmap(
        z=corr_matrix.values,
        x=corr_vars,
        y=corr_vars,
        colorscale='RdYlGn',
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        hovertemplate='%{x} vs %{y}: %{z:.2f}')
)
tab4.update_layout(
    title='🔥 Correlation Heatmap — Yield vs Climate Variables',
    template='plotly_white',
    height=500
)

# ── Tab 5: Feature Importance
tab5 = go.Figure()
tab5.add_trace(
    go.Bar(
        x=sorted_importances,
        y=sorted_features,
        orientation='h',
        marker=dict(color=['#3498db', '#e74c3c', '#95a5a6']),
        hovertemplate='%{y}: %{x:.4f}')
)
tab5.update_layout(
    title='🔍 Feature Importance — Which Climate Variable Affects Yield Most?',
    xaxis_title='Importance Score',
    template='plotly_white',
    height=500
)

# ── Tab 6: Yield Forecast
tab6 = go.Figure()

# Historical
tab6.add_trace(
    go.Scatter(x=df['year'], y=df['yield'],
               mode='lines+markers',
               name='Historical Yield',
               line=dict(color='green', width=2),
               marker=dict(size=8),
               hovertemplate='Year: %{x}<br>Yield: %{y:.2f} t/ha')
)

# Forecast
tab6.add_trace(
    go.Scatter(x=list(range(2024, 2032)), y=future_yield,
               mode='lines+markers',
               name='Forecasted Yield',
               line=dict(color='orange', width=2, dash='dash'),
               marker=dict(size=8),
               hovertemplate='Year: %{x}<br>Forecast: %{y:.2f} t/ha')
)

# Uncertainty band
tab6.add_trace(
    go.Scatter(
        x=list(range(2024, 2032)) + list(range(2024, 2032))[::-1],
        y=list(future_yield + 0.2) + list(future_yield - 0.2)[::-1],
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Uncertainty Band')
)

tab6.add_vline(x=2023, line_dash='dot', line_color='gray',
               annotation_text='Forecast Start')

tab6.update_layout(
    title='🔮 Maize Yield Forecast (2024–2031)',
    xaxis_title='Year',
    yaxis_title='Yield (t/ha)',
    template='plotly_white',
    height=500
)

# ── Build HTML with tabs
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Maize Yield & Climate Change — Eswatini</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        h1 {{
            text-align: center;
            color: #2c7a2c;
            margin-bottom: 5px;
        }}
        p.subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .tab-container {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }}
        .tab-btn {{
            padding: 10px 18px;
            background-color: #e0e0e0;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 13px;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .tab-btn:hover {{
            background-color: #2c7a2c;
            color: white;
        }}
        .tab-btn.active {{
            background-color: #2c7a2c;
            color: white;
        }}
        .tab-content {{
            display: none;
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .tab-content.active {{
            display: block;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>🌽 Effects of Climate Change on Maize Yield in Eswatini</h1>
    <p class="subtitle">Interactive Analysis Dashboard | 1993 – 2031 | Data Analytics Portfolio Project</p>

    <div class="tab-container">
        <button class="tab-btn active" onclick="showTab('yield')">🌽 Maize Yield</button>
        <button class="tab-btn" onclick="showTab('temp')">🌡️ Temperature</button>
        <button class="tab-btn" onclick="showTab('rain')">🌧️ Rainfall</button>
        <button class="tab-btn" onclick="showTab('corr')">🔥 Correlation</button>
        <button class="tab-btn" onclick="showTab('feat')">🔍 Feature Importance</button>
        <button class="tab-btn" onclick="showTab('fore')">🔮 Forecast</button>
    </div>

    <div id="yield" class="tab-content active">{tab1.to_html(full_html=False, include_plotlyjs='cdn')}</div>
    <div id="temp" class="tab-content">{tab2.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div id="rain" class="tab-content">{tab3.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div id="corr" class="tab-content">{tab4.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div id="feat" class="tab-content">{tab5.to_html(full_html=False, include_plotlyjs=False)}</div>
    <div id="fore" class="tab-content">{tab6.to_html(full_html=False, include_plotlyjs=False)}</div>

    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>

    <p class="footer">Built with Python | pandas • matplotlib • seaborn • scikit-learn • plotly</p>
</body>
</html>
"""

# Save dashboard
with open("visuals/interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Phase 9 done — Tabbed interactive dashboard saved!")
print("   📂 Open visuals/interactive_dashboard.html in your browser!")