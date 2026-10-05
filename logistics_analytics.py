"""
Logistics Analytics Utilities
Detailed analysis and statistical reports for delivery systems
"""

import pandas as pd
import numpy as np

def generate_analytics():
    """Generate detailed logistics analytics"""
    
    # Load delivery data
    df = pd.read_csv('/home/ubuntu/logistics_delivery_data.csv')
    
    # 1. Delivery Statistics
    stats = {
        'Total_Deliveries': len(df),
        'Avg_Delivery_Time': round(df['Delivery_Time_min'].mean(), 2),
        'Min_Delivery_Time': round(df['Delivery_Time_min'].min(), 2),
        'Max_Delivery_Time': round(df['Delivery_Time_min'].max(), 2),
        'Std_Dev_Time': round(df['Delivery_Time_min'].std(), 2),
        'Avg_Distance': round(df['Distance_km'].mean(), 2),
        'Avg_Stops': round(df['Number_of_Stops'].mean(), 2)
    }
    
    stats_df = pd.DataFrame([stats])
    stats_df.to_csv('/home/ubuntu/logistics_statistics.csv', index=False)
    
    # 2. Traffic Impact Analysis
    traffic_analysis = df.groupby('Traffic_Level').agg({
        'Delivery_Time_min': ['count', 'mean', 'std', 'min', 'max']
    }).round(2)
    traffic_analysis.columns = ['Count', 'Avg_Time', 'Std_Dev', 'Min_Time', 'Max_Time']
    traffic_analysis.to_csv('/home/ubuntu/logistics_traffic_analysis.csv')
    
    # 3. Vehicle Performance
    vehicle_analysis = df.groupby('Vehicle_Type').agg({
        'Delivery_Time_min': ['count', 'mean', 'std'],
        'Distance_km': 'mean'
    }).round(2)
    vehicle_analysis.columns = ['Count', 'Avg_Time', 'Std_Dev', 'Avg_Distance']
    vehicle_analysis.to_csv('/home/ubuntu/logistics_vehicle_performance.csv')
    
    # 4. Route Efficiency
    route_efficiency = df.groupby('Delivery_Priority').agg({
        'Delivery_Time_min': ['count', 'mean'],
        'Distance_km': 'mean'
    }).round(2)
    route_efficiency.columns = ['Count', 'Avg_Time', 'Avg_Distance']
    route_efficiency.to_csv('/home/ubuntu/logistics_route_efficiency.csv')
    
    # 5. Time of Day Analysis
    time_analysis = df.groupby('Time_of_Day').agg({
        'Delivery_Time_min': ['count', 'mean', 'std']
    }).round(2)
    time_analysis.columns = ['Count', 'Avg_Time', 'Std_Dev']
    time_analysis.to_csv('/home/ubuntu/logistics_time_analysis.csv')
    
    # 6. Weather Impact
    weather_analysis = df.groupby('Weather_Condition').agg({
        'Delivery_Time_min': ['count', 'mean', 'std']
    }).round(2)
    weather_analysis.columns = ['Count', 'Avg_Time', 'Std_Dev']
    weather_analysis.to_csv('/home/ubuntu/logistics_weather_analysis.csv')
    
    # 7. Distance vs Time Correlation
    distance_bins = pd.cut(df['Distance_km'], bins=5)
    distance_analysis = df.groupby(distance_bins).agg({
        'Delivery_Time_min': ['count', 'mean', 'std']
    }).round(2)
    distance_analysis.columns = ['Count', 'Avg_Time', 'Std_Dev']
    distance_analysis.to_csv('/home/ubuntu/logistics_distance_analysis.csv')
    
    # 8. Stops Impact
    stops_analysis = df.groupby('Number_of_Stops').agg({
        'Delivery_Time_min': ['count', 'mean']
    }).round(2)
    stops_analysis.columns = ['Count', 'Avg_Time']
    stops_analysis.to_csv('/home/ubuntu/logistics_stops_analysis.csv')
    
    # 9. Correlation Matrix
    numeric_cols = ['Distance_km', 'Traffic_Code', 'Weather_Code', 'Vehicle_Code', 
                    'Priority_Code', 'Time_Code', 'Number_of_Stops', 'Previous_Avg_Time', 'Delivery_Time_min']
    correlation = df[numeric_cols].corr().round(3)
    correlation.to_csv('/home/ubuntu/logistics_correlation_matrix.csv')
    
    # 10. Performance Categories
    df['Time_Category'] = pd.cut(df['Delivery_Time_min'], 
                                  bins=[0, 60, 120, 180, 300],
                                  labels=['Fast', 'Normal', 'Slow', 'Very Slow'])
    category_dist = df['Time_Category'].value_counts().sort_index()
    category_df = pd.DataFrame({
        'Category': category_dist.index,
        'Count': category_dist.values,
        'Percentage': (category_dist.values / len(df) * 100).round(2)
    })
    category_df.to_csv('/home/ubuntu/logistics_performance_categories.csv', index=False)
    
    print("Analytics generated successfully!")
    print("\nDelivery Statistics:")
    print(stats_df)
    print("\nTraffic Impact Analysis:")
    print(traffic_analysis)
    print("\nVehicle Performance:")
    print(vehicle_analysis)

if __name__ == "__main__":
    generate_analytics()
