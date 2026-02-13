"""
Database Operations
Simple SQL queries for financial analysis
"""

import sqlite3
import pandas as pd


class FinancialDB:
    """Simple database class for financial data"""
    
    def __init__(self, db_path='database/financial.db'):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        print(f"✓ Connected to database")
    
    def load_data(self, csv_path):
        """Load CSV data into database"""
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Load to database
        df.to_sql('transactions', self.conn, if_exists='replace', index=False)
        
        print(f"✓ Loaded {len(df)} transactions into database")
    
    # ============ SQL QUERIES ============
    
    def get_overall_summary(self):
        """Overall financial summary"""
        query = """
        SELECT 
            COUNT(*) as total_transactions,
            SUM(revenue) as total_revenue,
            SUM(total_cost) as total_cost,
            SUM(profit) as total_profit,
            AVG(profit_margin) as avg_margin
        FROM transactions
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_yearly_performance(self):
        """Year-wise performance"""
        query = """
        SELECT 
            year,
            COUNT(*) as transactions,
            ROUND(SUM(revenue), 2) as revenue,
            ROUND(SUM(profit), 2) as profit,
            ROUND(AVG(profit_margin), 2) as avg_margin
        FROM transactions
        GROUP BY year
        ORDER BY year
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_monthly_trends(self):
        """Monthly revenue and profit trends"""
        query = """
        SELECT 
            year,
            month,
            COUNT(*) as transactions,
            ROUND(SUM(revenue), 2) as revenue,
            ROUND(SUM(profit), 2) as profit,
            ROUND(AVG(profit_margin), 2) as margin
        FROM transactions
        GROUP BY year, month
        ORDER BY year, month
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_segment_performance(self):
        """Performance by segment"""
        query = """
        SELECT 
            segment,
            COUNT(*) as transactions,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(SUM(profit), 2) as total_profit,
            ROUND(AVG(profit_margin), 2) as avg_margin,
            ROUND(SUM(total_cost), 2) as total_cost
        FROM transactions
        GROUP BY segment
        ORDER BY total_profit DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_quarterly_performance(self):
        """Quarterly breakdown"""
        query = """
        SELECT 
            year,
            quarter,
            COUNT(*) as transactions,
            ROUND(SUM(revenue), 2) as revenue,
            ROUND(SUM(profit), 2) as profit
        FROM transactions
        GROUP BY year, quarter
        ORDER BY year, quarter
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_top_customers(self, limit=10):
        """Top customers by revenue"""
        query = f"""
        SELECT 
            customer_id,
            COUNT(*) as transaction_count,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(SUM(profit), 2) as total_profit,
            ROUND(AVG(profit_margin), 2) as avg_margin
        FROM transactions
        GROUP BY customer_id
        ORDER BY total_revenue DESC
        LIMIT {limit}
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_churn_analysis(self):
        """Customer churn analysis"""
        query = """
        SELECT 
            segment,
            COUNT(DISTINCT customer_id) as total_customers,
            SUM(churned) as churned_customers,
            ROUND(SUM(churned) * 100.0 / COUNT(DISTINCT customer_id), 2) as churn_rate
        FROM transactions
        GROUP BY segment
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_revenue_growth(self):
        """Year-over-year revenue growth"""
        query = """
        SELECT 
            year,
            ROUND(SUM(revenue), 2) as revenue,
            LAG(ROUND(SUM(revenue), 2)) OVER (ORDER BY year) as prev_year_revenue
        FROM transactions
        GROUP BY year
        ORDER BY year
        """
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate growth percentage
        df['growth_rate'] = ((df['revenue'] - df['prev_year_revenue']) / 
                             df['prev_year_revenue'] * 100).round(2)
        
        return df
    
    def get_cost_breakdown(self):
        """Cost analysis by segment"""
        query = """
        SELECT 
            segment,
            ROUND(SUM(cogs), 2) as total_cogs,
            ROUND(SUM(operating_cost), 2) as total_operating_cost,
            ROUND(SUM(total_cost), 2) as total_cost,
            ROUND(AVG(total_cost / revenue * 100), 2) as cost_to_revenue_ratio
        FROM transactions
        GROUP BY segment
        ORDER BY total_cost DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def get_high_low_margin_products(self):
        """Identify high and low margin segments"""
        query = """
        SELECT 
            segment,
            ROUND(AVG(profit_margin), 2) as avg_margin,
            ROUND(SUM(revenue), 2) as total_revenue,
            COUNT(*) as transaction_count,
            CASE 
                WHEN AVG(profit_margin) > 35 THEN 'High Margin'
                WHEN AVG(profit_margin) < 20 THEN 'Low Margin'
                ELSE 'Medium Margin'
            END as margin_category
        FROM transactions
        GROUP BY segment
        ORDER BY avg_margin DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")
