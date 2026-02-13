"""
Financial Data Generator
Simple script to create realistic financial transaction data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_financial_data(num_transactions=10000):
    """
    Generate financial transaction data for 3 years
    Simple and straightforward approach
    """
    
    print(f"Generating {num_transactions} financial transactions...")
    
    # Product segments (simple categories)
    segments = ['Enterprise', 'SMB', 'Retail', 'Subscription', 'Services']
    
    # Start date: 3 years ago
    start_date = datetime.now() - timedelta(days=3*365)
    
    transactions = []
    
    for i in range(num_transactions):
        # Random date in last 3 years
        days_offset = random.randint(0, 3*365)
        transaction_date = start_date + timedelta(days=days_offset)
        
        # Pick a segment
        segment = random.choice(segments)
        
        # Revenue based on segment (realistic amounts)
        if segment == 'Enterprise':
            revenue = round(random.uniform(50000, 200000), 2)
            margin = random.uniform(0.35, 0.50)  # 35-50% margin
        elif segment == 'SMB':
            revenue = round(random.uniform(10000, 50000), 2)
            margin = random.uniform(0.25, 0.40)
        elif segment == 'Retail':
            revenue = round(random.uniform(500, 5000), 2)
            margin = random.uniform(0.10, 0.20)  # Low margin
        elif segment == 'Subscription':
            revenue = round(random.uniform(1000, 10000), 2)
            margin = random.uniform(0.40, 0.60)  # High margin
        else:  # Services
            revenue = round(random.uniform(5000, 30000), 2)
            margin = random.uniform(0.30, 0.45)
        
        # Calculate costs
        cogs = round(revenue * (1 - margin), 2)  # Cost of goods sold
        operating_cost = round(revenue * 0.15, 2)  # 15% operating cost
        total_cost = cogs + operating_cost
        
        # Calculate profit
        profit = revenue - total_cost
        profit_margin = round((profit / revenue) * 100, 2)
        
        # Customer info
        customer_id = f"CUST_{random.randint(1, 2000):04d}"
        
        # Is this customer churned? (simple logic)
        days_since = (datetime.now() - transaction_date).days
        churned = 1 if days_since > 180 and random.random() < 0.25 else 0
        
        transaction = {
            'transaction_id': f"TXN_{i+1:06d}",
            'date': transaction_date.strftime('%Y-%m-%d'),
            'year': transaction_date.year,
            'month': transaction_date.month,
            'quarter': f"Q{(transaction_date.month-1)//3 + 1}",
            'customer_id': customer_id,
            'segment': segment,
            'revenue': revenue,
            'cogs': cogs,
            'operating_cost': operating_cost,
            'total_cost': total_cost,
            'profit': profit,
            'profit_margin': profit_margin,
            'churned': churned
        }
        
        transactions.append(transaction)
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1} transactions...")
    
    # Create dataframe
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"\n✓ Generated {len(df)} transactions successfully!")
    
    return df


def save_data(df, filename='data/transactions.csv'):
    """Save data to CSV file"""
    df.to_csv(filename, index=False)
    print(f"✓ Data saved to {filename}")


if __name__ == "__main__":
    # Generate data
    data = generate_financial_data(10000)
    
    # Save to CSV
    save_data(data)
    
    # Show summary
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    print(f"Total Transactions: {len(data):,}")
    print(f"Date Range: {data['date'].min()} to {data['date'].max()}")
    print(f"Total Revenue: ₹{data['revenue'].sum():,.2f}")
    print(f"Total Profit: ₹{data['profit'].sum():,.2f}")
    print(f"Average Margin: {data['profit_margin'].mean():.2f}%")
    print(f"\nSegment Breakdown:")
    print(data['segment'].value_counts())
    print("="*50)
