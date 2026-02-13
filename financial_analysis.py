"""
Financial Analysis
Calculate KPIs and financial metrics
"""

import pandas as pd
import numpy as np


class FinancialAnalyzer:
    """Simple financial analysis functions"""
    
    def __init__(self, data):
        self.df = data.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        
        kpis = {
            'total_revenue': self.df['revenue'].sum(),
            'total_profit': self.df['profit'].sum(),
            'total_cost': self.df['total_cost'].sum(),
            'avg_profit_margin': self.df['profit_margin'].mean(),
            'total_transactions': len(self.df),
            'avg_transaction_value': self.df['revenue'].mean(),
            'total_customers': self.df['customer_id'].nunique()
        }
        
        # Additional calculations
        kpis['gross_margin'] = (kpis['total_profit'] / kpis['total_revenue']) * 100
        kpis['revenue_per_customer'] = kpis['total_revenue'] / kpis['total_customers']
        
        return kpis
    
    def analyze_segments(self):
        """Analyze performance by segment"""
        
        segment_stats = self.df.groupby('segment').agg({
            'revenue': ['sum', 'mean', 'count'],
            'profit': 'sum',
            'profit_margin': 'mean',
            'total_cost': 'sum'
        }).round(2)
        
        segment_stats.columns = ['total_revenue', 'avg_revenue', 'transactions',
                                 'total_profit', 'avg_margin', 'total_cost']
        
        # Calculate profitability score (simple scoring)
        segment_stats['profitability_score'] = (
            segment_stats['avg_margin'] * 0.6 + 
            (segment_stats['total_revenue'] / segment_stats['total_revenue'].max() * 100) * 0.4
        ).round(2)
        
        return segment_stats.sort_values('profitability_score', ascending=False)
    
    def calculate_revenue_growth(self):
        """Calculate month-over-month and year-over-year growth"""
        
        # Monthly revenue
        monthly = self.df.groupby([self.df['date'].dt.year, 
                                   self.df['date'].dt.month])['revenue'].sum()
        
        # Calculate growth rates
        monthly_growth = monthly.pct_change() * 100
        
        return {
            'monthly_revenue': monthly,
            'monthly_growth': monthly_growth,
            'avg_monthly_growth': monthly_growth.mean()
        }
    
    def identify_trends(self):
        """Identify revenue and profit trends"""
        
        # Group by month
        monthly_data = self.df.groupby(self.df['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'profit': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        monthly_data['date'] = monthly_data['date'].dt.to_timestamp()
        
        # Calculate simple moving average (3-month)
        monthly_data['revenue_ma'] = monthly_data['revenue'].rolling(window=3).mean()
        monthly_data['profit_ma'] = monthly_data['profit'].rolling(window=3).mean()
        
        return monthly_data
    
    def analyze_customer_value(self):
        """Calculate customer lifetime value metrics"""
        
        customer_metrics = self.df.groupby('customer_id').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'transaction_id': 'count',
            'churned': 'max'  # If churned in any transaction
        }).reset_index()
        
        customer_metrics.columns = ['customer_id', 'total_revenue', 'total_profit',
                                    'transaction_count', 'churned']
        
        # Calculate average customer lifetime value
        avg_clv = customer_metrics['total_revenue'].mean()
        
        # Active vs churned customers
        active_customers = len(customer_metrics[customer_metrics['churned'] == 0])
        churned_customers = len(customer_metrics[customer_metrics['churned'] == 1])
        
        return {
            'avg_clv': avg_clv,
            'active_customers': active_customers,
            'churned_customers': churned_customers,
            'churn_rate': (churned_customers / len(customer_metrics)) * 100,
            'avg_transactions_per_customer': customer_metrics['transaction_count'].mean()
        }
    
    def find_low_margin_segments(self, threshold=20):
        """Find segments with low profit margins"""
        
        segment_margins = self.df.groupby('segment')['profit_margin'].mean()
        
        low_margin = segment_margins[segment_margins < threshold]
        
        # Get detailed info for low margin segments
        low_margin_data = self.df[self.df['segment'].isin(low_margin.index)]
        
        analysis = low_margin_data.groupby('segment').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'total_cost': 'sum',
            'profit_margin': 'mean',
            'transaction_id': 'count'
        }).round(2)
        
        return analysis
    
    def calculate_cost_efficiency(self):
        """Analyze cost efficiency by segment"""
        
        cost_analysis = self.df.groupby('segment').agg({
            'revenue': 'sum',
            'total_cost': 'sum',
            'operating_cost': 'sum',
            'cogs': 'sum'
        }).round(2)
        
        # Calculate cost ratios
        cost_analysis['cost_to_revenue_ratio'] = (
            cost_analysis['total_cost'] / cost_analysis['revenue'] * 100
        ).round(2)
        
        cost_analysis['operating_cost_percentage'] = (
            cost_analysis['operating_cost'] / cost_analysis['revenue'] * 100
        ).round(2)
        
        return cost_analysis.sort_values('cost_to_revenue_ratio')
    
    def seasonal_analysis(self):
        """Analyze seasonal patterns"""
        
        # Group by quarter
        quarterly = self.df.groupby('quarter').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'transaction_id': 'count'
        }).round(2)
        
        quarterly.columns = ['revenue', 'profit', 'transactions']
        
        # Find peak quarter
        peak_quarter = quarterly['revenue'].idxmax()
        
        return {
            'quarterly_data': quarterly,
            'peak_quarter': peak_quarter,
            'peak_revenue': quarterly.loc[peak_quarter, 'revenue']
        }
