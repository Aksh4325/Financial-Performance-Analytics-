"""
Financial Performance Analytics
Main Application - Simple and Clean
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.append('src')

from data_generator import generate_financial_data, save_data
from database import FinancialDB
from financial_analysis import FinancialAnalyzer
from forecasting import SimpleForecaster
from excel_generator import ExcelDashboard
from visualization import FinancialCharts


def print_header(text):
    """Simple header"""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")


def clear_screen():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("FINANCIAL PERFORMANCE ANALYTICS".center(60))
    print("="*60)
    print("\n1. Generate Transaction Data")
    print("2. View Overall Summary")
    print("3. Analyze Segments")
    print("4. Revenue Forecasting")
    print("5. Generate Excel Reports")
    print("6. Create Charts")
    print("7. Business Recommendations")
    print("8. Run Complete Analysis")
    print("9. Exit")
    print("="*60)


def generate_data():
    """Generate financial data"""
    print_header("DATA GENERATION")
    
    data = generate_financial_data(10000)
    save_data(data)
    
    input("\nPress Enter to continue...")
    return data


def view_summary(db):
    """Show overall summary"""
    print_header("OVERALL FINANCIAL SUMMARY")
    
    summary = db.get_overall_summary()
    
    print(f"Total Transactions:  {summary['total_transactions'].values[0]:,}")
    print(f"Total Revenue:       ₹{summary['total_revenue'].values[0]:,.2f}")
    print(f"Total Cost:          ₹{summary['total_cost'].values[0]:,.2f}")
    print(f"Total Profit:        ₹{summary['total_profit'].values[0]:,.2f}")
    print(f"Average Margin:      {summary['avg_margin'].values[0]:.2f}%")
    
    print("\n" + "-"*60)
    print("YEARLY PERFORMANCE")
    print("-"*60)
    
    yearly = db.get_yearly_performance()
    print(yearly.to_string(index=False))
    
    input("\nPress Enter to continue...")


def analyze_segments(db, data):
    """Segment analysis"""
    print_header("SEGMENT PERFORMANCE ANALYSIS")
    
    segment_perf = db.get_segment_performance()
    print("\nPerformance by Segment:")
    print(segment_perf.to_string(index=False))
    
    print("\n" + "-"*60)
    print("HIGH vs LOW MARGIN SEGMENTS")
    print("-"*60)
    
    high_low = db.get_high_low_margin_products()
    print(high_low.to_string(index=False))
    
    # Low margin analysis
    analyzer = FinancialAnalyzer(data)
    low_margin = analyzer.find_low_margin_segments(threshold=20)
    
    if len(low_margin) > 0:
        print("\n⚠️  LOW MARGIN SEGMENTS (< 20%):")
        for segment in low_margin.index:
            print(f"\n{segment}:")
            print(f"  Revenue: ₹{low_margin.loc[segment, 'revenue']:,.2f}")
            print(f"  Margin:  {low_margin.loc[segment, 'profit_margin']:.2f}%")
            print(f"  Cost:    ₹{low_margin.loc[segment, 'total_cost']:,.2f}")
    
    input("\nPress Enter to continue...")


def revenue_forecasting(data):
    """Generate revenue forecast"""
    print_header("REVENUE FORECASTING")
    
    forecaster = SimpleForecaster(data)
    
    print("Generating 6-month forecast...")
    forecast = forecaster.forecast_with_confidence(periods=6)
    
    print("\nFORECAST RESULTS:\n")
    for _, row in forecast.iterrows():
        print(f"{row['date'].strftime('%Y-%m')}: ₹{row['final_forecast']:,.2f}")
        print(f"  Range: ₹{row['lower_bound']:,.2f} - ₹{row['upper_bound']:,.2f}")
    
    # Calculate accuracy
    print("\nCalculating forecast accuracy...")
    accuracy = forecaster.calculate_forecast_accuracy(test_months=3)
    
    if accuracy:
        print(f"\nForecast Accuracy (MAPE): {accuracy['mape']:.2f}%")
        if accuracy['mape'] < 10:
            print("✓ Excellent accuracy (<10% error)")
        elif accuracy['mape'] < 15:
            print("✓ Good accuracy (<15% error)")
        else:
            print("⚠ Moderate accuracy")
    
    input("\nPress Enter to continue...")
    return forecast, accuracy


def generate_excel_reports(data, kpis, forecast, accuracy):
    """Create Excel dashboards"""
    print_header("GENERATING EXCEL REPORTS")
    
    excel = ExcelDashboard(data)
    
    # Create reports
    excel.create_kpi_dashboard(kpis)
    excel.create_segment_analysis(data)
    excel.create_monthly_trends()
    excel.create_forecast_report(forecast, accuracy)
    
    print("\n✓ All Excel reports created in 'excel/' folder")
    input("\nPress Enter to continue...")


def create_charts(data, forecast):
    """Generate all charts"""
    print_header("CREATING VISUALIZATIONS")
    
    charts = FinancialCharts(data)
    
    print("Creating charts...")
    charts.plot_revenue_trend()
    charts.plot_segment_performance()
    charts.plot_profit_margin()
    charts.plot_yearly_comparison()
    charts.plot_cost_breakdown()
    charts.plot_quarterly_trends()
    
    # Forecast chart
    monthly = data.groupby(pd.to_datetime(data['date']).dt.to_period('M'))['revenue'].sum()
    charts.plot_forecast(monthly, forecast)
    
    print("\n✓ All charts saved in 'output/' folder")
    input("\nPress Enter to continue...")


def business_recommendations(db, data):
    """Generate business recommendations"""
    print_header("BUSINESS RECOMMENDATIONS")
    
    print("Analyzing financial performance...\n")
    
    # Get key metrics
    analyzer = FinancialAnalyzer(data)
    
    # High/Low margin segments
    high_low = db.get_high_low_margin_products()
    
    print("KEY FINDINGS:\n")
    
    # 1. High margin segments
    high_margin = high_low[high_low['margin_category'] == 'High Margin']
    if len(high_margin) > 0:
        print("✓ HIGH MARGIN SEGMENTS (>35%):")
        for _, seg in high_margin.iterrows():
            print(f"  • {seg['segment']}: {seg['avg_margin']:.1f}% margin")
    
    # 2. Low margin segments
    low_margin = high_low[high_low['margin_category'] == 'Low Margin']
    if len(low_margin) > 0:
        print("\n⚠ LOW MARGIN SEGMENTS (<20%):")
        for _, seg in low_margin.iterrows():
            print(f"  • {seg['segment']}: {seg['avg_margin']:.1f}% margin")
    
    # 3. Cost analysis
    cost_eff = analyzer.calculate_cost_efficiency()
    high_cost = cost_eff[cost_eff['cost_to_revenue_ratio'] > 75]
    
    if len(high_cost) > 0:
        print("\n⚠ HIGH COST SEGMENTS (Cost/Revenue > 75%):")
        for seg in high_cost.index:
            print(f"  • {seg}: {high_cost.loc[seg, 'cost_to_revenue_ratio']:.1f}% cost ratio")
    
    # Recommendations
    print("\n" + "="*60)
    print("RECOMMENDATIONS:")
    print("="*60)
    
    print("\n1. INVESTMENT REALLOCATION:")
    if len(high_margin) > 0:
        best_segment = high_margin.iloc[0]
        print(f"   → Increase focus on '{best_segment['segment']}'")
        print(f"     (Current margin: {best_segment['avg_margin']:.1f}%)")
        print(f"     Expected Impact: +20-30% profit")
    
    print("\n2. COST OPTIMIZATION:")
    if len(low_margin) > 0:
        worst_segment = low_margin.iloc[0]
        print(f"   → Reduce costs in '{worst_segment['segment']}'")
        print(f"     (Current margin: {worst_segment['avg_margin']:.1f}%)")
        print(f"     Target: Improve margin to >20%")
    
    print("\n3. OPERATIONAL EFFICIENCY:")
    if len(high_cost) > 0:
        print("   → Focus on cost reduction in:")
        for seg in high_cost.index[:2]:
            print(f"     • {seg}")
        print(f"     Target: Reduce cost ratio by 10-15%")
    
    # Seasonal insights
    seasonal = analyzer.seasonal_analysis()
    print(f"\n4. SEASONAL PLANNING:")
    print(f"   → Peak Quarter: {seasonal['peak_quarter']}")
    print(f"     Plan inventory and staffing accordingly")
    
    input("\nPress Enter to continue...")


def run_complete_analysis():
    """Run full analysis pipeline"""
    print_header("COMPLETE FINANCIAL ANALYSIS")
    
    print("This will run the complete analysis pipeline:\n")
    print("1. Generate transaction data")
    print("2. Load to database")
    print("3. Perform financial analysis")
    print("4. Create revenue forecast")
    print("5. Generate Excel reports")
    print("6. Create visualizations")
    print("7. Business recommendations\n")
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Step 1: Generate data
    print("\n[1/7] Generating data...")
    data = generate_financial_data(10000)
    save_data(data)
    
    # Step 2: Load to database
    print("\n[2/7] Loading to database...")
    db = FinancialDB()
    db.connect()
    db.load_data('data/transactions.csv')
    
    # Step 3: Analysis
    print("\n[3/7] Performing analysis...")
    analyzer = FinancialAnalyzer(data)
    kpis = analyzer.calculate_kpis()
    
    # Step 4: Forecasting
    print("\n[4/7] Generating forecast...")
    forecaster = SimpleForecaster(data)
    forecast = forecaster.forecast_with_confidence(periods=6)
    accuracy = forecaster.calculate_forecast_accuracy(test_months=3)
    
    # Step 5: Excel reports
    print("\n[5/7] Creating Excel reports...")
    excel = ExcelDashboard(data)
    excel.create_kpi_dashboard(kpis)
    excel.create_segment_analysis(data)
    excel.create_monthly_trends()
    excel.create_forecast_report(forecast, accuracy)
    
    # Step 6: Charts
    print("\n[6/7] Creating charts...")
    charts = FinancialCharts(data)
    charts.plot_revenue_trend()
    charts.plot_segment_performance()
    charts.plot_profit_margin()
    charts.plot_yearly_comparison()
    
    # Step 7: Summary
    print("\n[7/7] Analysis complete!\n")
    
    print("="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(f"\nTotal Revenue:      ₹{kpis['total_revenue']:,.2f}")
    print(f"Total Profit:       ₹{kpis['total_profit']:,.2f}")
    print(f"Profit Margin:      {kpis['avg_profit_margin']:.2f}%")
    print(f"Forecast Accuracy:  {accuracy['mape']:.2f}% MAPE")
    
    print("\nGenerated Files:")
    print("  • data/transactions.csv")
    print("  • excel/financial_dashboard.xlsx")
    print("  • excel/segment_analysis.xlsx")
    print("  • excel/forecast_report.xlsx")
    print("  • output/*.png (7 charts)")
    
    db.close()
    
    input("\nPress Enter to continue...")


def main():
    """Main application loop"""
    
    db = None
    data = None
    forecast = None
    accuracy = None
    
    while True:
        clear_screen()
        show_menu()
        
        try:
            choice = int(input("\nEnter choice: "))
        except ValueError:
            print("Invalid input!")
            input("Press Enter...")
            continue
        
        if choice == 1:
            data = generate_data()
        
        elif choice == 2:
            if db is None:
                db = FinancialDB()
                db.connect()
                db.load_data('data/transactions.csv')
            view_summary(db)
        
        elif choice == 3:
            if db is None:
                db = FinancialDB()
                db.connect()
                db.load_data('data/transactions.csv')
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            analyze_segments(db, data)
        
        elif choice == 4:
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            forecast, accuracy = revenue_forecasting(data)
        
        elif choice == 5:
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            analyzer = FinancialAnalyzer(data)
            kpis = analyzer.calculate_kpis()
            if forecast is None:
                forecaster = SimpleForecaster(data)
                forecast = forecaster.forecast_with_confidence()
                accuracy = forecaster.calculate_forecast_accuracy(3)
            generate_excel_reports(data, kpis, forecast, accuracy)
        
        elif choice == 6:
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            if forecast is None:
                forecaster = SimpleForecaster(data)
                forecast = forecaster.forecast_with_confidence()
            create_charts(data, forecast)
        
        elif choice == 7:
            if db is None:
                db = FinancialDB()
                db.connect()
                db.load_data('data/transactions.csv')
            if data is None:
                data = pd.read_csv('data/transactions.csv')
            business_recommendations(db, data)
        
        elif choice == 8:
            run_complete_analysis()
        
        elif choice == 9:
            if db:
                db.close()
            print("\n" + "="*60)
            print("Thank you for using Financial Analytics!")
            print("\nDeveloper: Akshay Tiwari")
            print("Email: akshay.tiwari@example.com")
            print("\n© 2026 College Analytics Project")
            print("="*60 + "\n")
            break
        
        else:
            print("Invalid choice!")
            input("Press Enter...")


if __name__ == "__main__":
    main()
