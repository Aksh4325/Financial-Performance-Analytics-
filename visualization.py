"""
Visualization Module
Simple charts for financial analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


class FinancialCharts:
    """Create simple financial charts"""
    
    def __init__(self, data, output_dir='output'):
        self.df = data.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.output_dir = output_dir
        
        # Simple style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
    
    def plot_revenue_trend(self):
        """Simple revenue trend line"""
        
        monthly = self.df.groupby(self.df['date'].dt.to_period('M'))['revenue'].sum()
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly.index.astype(str), monthly.values, 
                marker='o', linewidth=2, markersize=6)
        plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=11)
        plt.ylabel('Revenue (₹)', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/revenue_trend.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_segment_performance(self):
        """Bar chart of segment performance"""
        
        segment_data = self.df.groupby('segment').agg({
            'revenue': 'sum',
            'profit': 'sum'
        })
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Revenue by segment
        ax1.bar(segment_data.index, segment_data['revenue'], color='steelblue')
        ax1.set_title('Revenue by Segment', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Revenue (₹)', fontsize=10)
        ax1.tick_params(axis='x', rotation=45)
        
        # Profit by segment
        ax2.bar(segment_data.index, segment_data['profit'], color='seagreen')
        ax2.set_title('Profit by Segment', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Profit (₹)', fontsize=10)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        filename = f'{self.output_dir}/segment_performance.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_profit_margin(self):
        """Profit margin comparison"""
        
        margins = self.df.groupby('segment')['profit_margin'].mean().sort_values()
        
        plt.figure(figsize=(10, 6))
        colors = ['red' if x < 20 else 'orange' if x < 35 else 'green' 
                 for x in margins.values]
        plt.barh(margins.index, margins.values, color=colors)
        plt.title('Average Profit Margin by Segment', fontsize=14, fontweight='bold')
        plt.xlabel('Profit Margin (%)', fontsize=11)
        plt.axvline(x=20, color='red', linestyle='--', label='Low Margin (<20%)')
        plt.axvline(x=35, color='green', linestyle='--', label='High Margin (>35%)')
        plt.legend()
        plt.tight_layout()
        
        filename = f'{self.output_dir}/profit_margins.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_yearly_comparison(self):
        """Year-wise performance comparison"""
        
        yearly = self.df.groupby('year').agg({
            'revenue': 'sum',
            'profit': 'sum'
        })
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(yearly))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], yearly['revenue'], width, 
              label='Revenue', color='skyblue')
        ax.bar([i + width/2 for i in x], yearly['profit'], width, 
              label='Profit', color='lightgreen')
        
        ax.set_title('Year-wise Revenue & Profit', fontsize=14, fontweight='bold')
        ax.set_ylabel('Amount (₹)', fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(yearly.index)
        ax.legend()
        plt.tight_layout()
        
        filename = f'{self.output_dir}/yearly_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_cost_breakdown(self):
        """Cost breakdown by segment"""
        
        costs = self.df.groupby('segment').agg({
            'cogs': 'sum',
            'operating_cost': 'sum'
        })
        
        plt.figure(figsize=(10, 6))
        costs.plot(kind='bar', stacked=True, color=['coral', 'lightcoral'])
        plt.title('Cost Breakdown by Segment', fontsize=14, fontweight='bold')
        plt.ylabel('Cost (₹)', fontsize=11)
        plt.xlabel('Segment', fontsize=11)
        plt.legend(['COGS', 'Operating Cost'])
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filename = f'{self.output_dir}/cost_breakdown.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_quarterly_trends(self):
        """Quarterly performance trends"""
        
        quarterly = self.df.groupby(['year', 'quarter'])['revenue'].sum().reset_index()
        quarterly['period'] = quarterly['year'].astype(str) + '-' + quarterly['quarter']
        
        plt.figure(figsize=(12, 6))
        plt.plot(quarterly['period'], quarterly['revenue'], 
                marker='s', linewidth=2, markersize=8, color='darkorange')
        plt.title('Quarterly Revenue Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Quarter', fontsize=11)
        plt.ylabel('Revenue (₹)', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/quarterly_trends.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
    
    def plot_forecast(self, historical, forecast):
        """Plot historical and forecasted revenue"""
        
        plt.figure(figsize=(14, 6))
        
        # Historical data
        plt.plot(historical.index, historical.values, 
                marker='o', linewidth=2, label='Actual', color='blue')
        
        # Forecast
        forecast_dates = pd.to_datetime(forecast['date'])
        plt.plot(forecast_dates, forecast['final_forecast'], 
                marker='s', linewidth=2, linestyle='--', 
                label='Forecast', color='red')
        
        # Confidence interval
        plt.fill_between(forecast_dates, 
                        forecast['lower_bound'], 
                        forecast['upper_bound'], 
                        alpha=0.2, color='red', label='95% Confidence')
        
        plt.title('Revenue Forecast (6 Months)', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=11)
        plt.ylabel('Revenue (₹)', fontsize=11)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f'{self.output_dir}/revenue_forecast.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")
