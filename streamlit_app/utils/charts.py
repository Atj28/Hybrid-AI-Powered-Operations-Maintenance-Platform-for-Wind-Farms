"""
Chart utilities for Wind Farm Dashboard
Using Plotly for interactive visualizations
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.settings import CHART_THEME, SEVERITY_COLORS, STATUS_COLORS


def create_kpi_gauge(value: float, title: str, max_val: float = 100, 
                     suffix: str = "%", threshold_good: float = 80, 
                     threshold_warn: float = 50) -> go.Figure:
    """Create a gauge chart for KPI display"""
    
    # Determine color based on thresholds
    if value >= threshold_good:
        bar_color = STATUS_COLORS["green"]
    elif value >= threshold_warn:
        bar_color = STATUS_COLORS["yellow"]
    else:
        bar_color = STATUS_COLORS["red"]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16}},
        number={'suffix': suffix, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, max_val], 'tickwidth': 1},
            'bar': {'color': bar_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, threshold_warn], 'color': '#ffcccc'},
                {'range': [threshold_warn, threshold_good], 'color': '#fff3cd'},
                {'range': [threshold_good, max_val], 'color': '#d4edda'}
            ],
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_turbine_comparison_bar(df: pd.DataFrame, metric: str, title: str) -> go.Figure:
    """Create bar chart comparing turbines"""
    
    fig = px.bar(
        df,
        x="turbine_id",
        y=metric,
        title=title,
        color=metric,
        color_continuous_scale="Blues",
    )
    
    fig.update_layout(
        xaxis_title="Turbine",
        yaxis_title=title,
        showlegend=False,
        height=400,
    )
    
    return fig


def create_power_curve(scada_df: pd.DataFrame, turbine_id: str = None) -> go.Figure:
    """Create power curve scatter plot"""
    
    df = scada_df.copy()
    if turbine_id:
        df = df[df["turbine_id"] == turbine_id]
    
    fig = px.scatter(
        df,
        x="wind_speed",
        y="power_kw",
        color="turbine_id" if not turbine_id else None,
        opacity=0.5,
        title=f"Power Curve {'- ' + turbine_id if turbine_id else '- All Turbines'}",
    )
    
    fig.update_layout(
        xaxis_title="Wind Speed (m/s)",
        yaxis_title="Power (kW)",
        height=500,
    )
    
    return fig


def create_time_series(df: pd.DataFrame, y_col: str, title: str, 
                       color_col: str = "turbine_id") -> go.Figure:
    """Create time series line chart"""
    
    fig = px.line(
        df,
        x="timestamp",
        y=y_col,
        color=color_col,
        title=title,
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=y_col,
        height=400,
        hovermode="x unified",
    )
    
    return fig


def create_fault_distribution_pie(fault_summary: dict) -> go.Figure:
    """Create pie chart of fault distribution"""
    
    # Remove NO_FAULT for clearer visualization
    faults = {k: v for k, v in fault_summary.items() if k != "NO_FAULT"}
    
    if not faults:
        faults = {"No Faults Detected": 1}
    
    fig = px.pie(
        names=list(faults.keys()),
        values=list(faults.values()),
        title="Fault Distribution",
        hole=0.4,
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig


def create_health_score_bar(health_df: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart of health scores"""
    
    df = health_df.sort_values("health_score", ascending=True)
    
    # Color based on score
    colors = []
    for score in df["health_score"]:
        if score >= 80:
            colors.append(STATUS_COLORS["green"])
        elif score >= 50:
            colors.append(STATUS_COLORS["yellow"])
        else:
            colors.append(STATUS_COLORS["red"])
    
    fig = go.Figure(go.Bar(
        x=df["health_score"],
        y=df["turbine_id"],
        orientation='h',
        marker_color=colors,
        text=df["health_score"].apply(lambda x: f"{x:.0f}"),
        textposition='inside',
    ))
    
    fig.update_layout(
        title="Turbine Health Scores",
        xaxis_title="Health Score",
        yaxis_title="Turbine",
        height=300,
        xaxis=dict(range=[0, 100]),
    )
    
    return fig


def create_heatmap(df: pd.DataFrame, turbine_col: str, time_col: str, 
                   value_col: str, title: str) -> go.Figure:
    """Create heatmap for turbine metrics over time"""
    
    # Pivot data for heatmap
    pivot = df.pivot_table(
        index=turbine_col,
        columns=pd.Grouper(key=time_col, freq='D'),
        values=value_col,
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        reversescale=True,
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Turbine",
        height=400,
    )
    
    return fig


def create_trend_line(df: pd.DataFrame, turbine_id: str, 
                      metrics: list) -> go.Figure:
    """Create multi-metric trend line for a turbine"""
    
    turbine_data = df[df["turbine_id"] == turbine_id].copy()
    turbine_data = turbine_data.sort_values("timestamp")
    
    fig = make_subplots(
        rows=len(metrics), cols=1,
        shared_xaxes=True,
        subplot_titles=metrics,
        vertical_spacing=0.08,
    )
    
    for i, metric in enumerate(metrics, 1):
        fig.add_trace(
            go.Scatter(
                x=turbine_data["timestamp"],
                y=turbine_data[metric],
                mode='lines',
                name=metric,
                line=dict(width=1),
            ),
            row=i, col=1
        )
    
    fig.update_layout(
        height=200 * len(metrics),
        title=f"Trends for {turbine_id}",
        showlegend=False,
    )
    
    return fig

