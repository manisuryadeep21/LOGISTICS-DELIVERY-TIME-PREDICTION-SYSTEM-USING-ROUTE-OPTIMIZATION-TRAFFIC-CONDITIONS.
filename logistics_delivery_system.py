"""
Logistics Delivery Time Prediction System
Route optimization, traffic conditions, and historical delivery records
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def generate_delivery_data():
    """Generate synthetic logistics delivery data"""
    np.random.seed(42)
    n_deliveries = 1000
    
    data = {
        'Delivery_ID': range(1, n_deliveries + 1),
        'Distance_km': np.random.uniform(5, 100, n_deliveries),
        'Traffic_Level': np.random.choice(['Low', 'Medium', 'High'], n_deliveries),
        'Weather_Condition': np.random.choice(['Clear', 'Rainy', 'Foggy'], n_deliveries),
        'Vehicle_Type': np.random.choice(['Bike', 'Car', 'Van'], n_deliveries),
        'Delivery_Priority': np.random.choice(['Standard', 'Express', 'Urgent'], n_deliveries),
        'Time_of_Day': np.random.choice(['Morning', 'Afternoon', 'Evening'], n_deliveries),
        'Number_of_Stops': np.random.randint(1, 10, n_deliveries),
        'Previous_Avg_Time': np.random.uniform(20, 180, n_deliveries)
    }
    
    df = pd.DataFrame(data)
    
    # Encode categorical variables
    traffic_map = {'Low': 1, 'Medium': 2, 'High': 3}
    weather_map = {'Clear': 1, 'Rainy': 2, 'Foggy': 1.5}
    vehicle_map = {'Bike': 1.2, 'Car': 1.0, 'Van': 1.1}
    priority_map = {'Standard': 1.0, 'Express': 0.8, 'Urgent': 0.7}
    time_map = {'Morning': 1.0, 'Afternoon': 1.1, 'Evening': 1.2}
    
    df['Traffic_Code'] = df['Traffic_Level'].map(traffic_map)
    df['Weather_Code'] = df['Weather_Condition'].map(weather_map)
    df['Vehicle_Code'] = df['Vehicle_Type'].map(vehicle_map)
    df['Priority_Code'] = df['Delivery_Priority'].map(priority_map)
    df['Time_Code'] = df['Time_of_Day'].map(time_map)
    
    # Generate delivery time based on features
    df['Delivery_Time_min'] = (
        0.8 * df['Distance_km'] +
        5 * df['Traffic_Code'] +
        3 * df['Weather_Code'] +
        2 * df['Vehicle_Code'] +
        -5 * df['Priority_Code'] +
        2 * df['Time_Code'] +
        3 * df['Number_of_Stops'] +
        0.2 * df['Previous_Avg_Time'] +
        np.random.normal(0, 10, n_deliveries)
    )
    
    df['Delivery_Time_min'] = df['Delivery_Time_min'].clip(10, 300)
    df.to_csv('/home/ubuntu/logistics_delivery_data.csv', index=False)
    
    return df

def train_models(df):
    """Train regression models for delivery time prediction"""
    X = df[['Distance_km', 'Traffic_Code', 'Weather_Code', 'Vehicle_Code', 
             'Priority_Code', 'Time_Code', 'Number_of_Stops', 'Previous_Avg_Time']]
    y = df['Delivery_Time_min']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    results = {}
    
    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    y_pred_lr = lr_model.predict(X_test_scaled)
    results['Linear Regression'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'MAE': mean_absolute_error(y_test, y_pred_lr),
        'R2': r2_score(y_test, y_pred_lr),
        'predictions': y_pred_lr
    }
    
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    results['Random Forest'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'MAE': mean_absolute_error(y_test, y_pred_rf),
        'R2': r2_score(y_test, y_pred_rf),
        'predictions': y_pred_rf,
        'feature_importance': rf_model.feature_importances_
    }
    
    # Gradient Boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    results['Gradient Boosting'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'MAE': mean_absolute_error(y_test, y_pred_gb),
        'R2': r2_score(y_test, y_pred_gb),
        'predictions': y_pred_gb,
        'feature_importance': gb_model.feature_importances_
    }
    
    return results, X_test, y_test, X.columns

def generate_visualizations(df, results, X_test, y_test, feature_names):
    """Generate delivery time prediction visualizations"""
    
    # 1. Delivery Analysis
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Logistics Delivery Time Analysis', fontsize=16, fontweight='bold')
    
    axes[0, 0].hist(df['Delivery_Time_min'], bins=30, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Delivery Time Distribution')
    axes[0, 0].set_xlabel('Time (minutes)')
    axes[0, 0].set_ylabel('Frequency')
    
    axes[0, 1].scatter(df['Distance_km'], df['Delivery_Time_min'], alpha=0.6, color='green')
    axes[0, 1].set_title('Distance vs Delivery Time')
    axes[0, 1].set_xlabel('Distance (km)')
    axes[0, 1].set_ylabel('Time (minutes)')
    
    traffic_times = df.groupby('Traffic_Level')['Delivery_Time_min'].mean()
    axes[1, 0].bar(traffic_times.index, traffic_times.values, color=['green', 'orange', 'red'])
    axes[1, 0].set_title('Traffic Impact on Delivery Time')
    axes[1, 0].set_ylabel('Avg Time (minutes)')
    
    vehicle_times = df.groupby('Vehicle_Type')['Delivery_Time_min'].mean()
    axes[1, 1].bar(vehicle_times.index, vehicle_times.values, color=['blue', 'purple', 'brown'])
    axes[1, 1].set_title('Vehicle Type Impact')
    axes[1, 1].set_ylabel('Avg Time (minutes)')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/logistics_delivery_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Model Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    models = list(results.keys())
    rmse_vals = [results[m]['RMSE'] for m in models]
    mae_vals = [results[m]['MAE'] for m in models]
    r2_vals = [results[m]['R2'] for m in models]
    
    x = np.arange(len(models))
    width = 0.25
    
    ax.bar(x - width, rmse_vals, width, label='RMSE', color='skyblue')
    ax.bar(x, mae_vals, width, label='MAE', color='lightcoral')
    ax.bar(x + width, r2_vals, width, label='R² Score', color='lightgreen')
    
    ax.set_xlabel('Models', fontweight='bold')
    ax.set_ylabel('Score', fontweight='bold')
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/logistics_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Predictions vs Actual
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Predictions vs Actual Delivery Time', fontsize=14, fontweight='bold')
    
    for idx, model_name in enumerate(results.keys()):
        y_pred = results[model_name]['predictions']
        axes[idx].scatter(y_test, y_pred, alpha=0.6, color='blue')
        axes[idx].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[idx].set_xlabel('Actual Time (min)')
        axes[idx].set_ylabel('Predicted Time (min)')
        axes[idx].set_title(f'{model_name}\nR² = {results[model_name]["R2"]:.4f}')
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/logistics_predictions_vs_actual.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Feature Importance
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Feature Importance Analysis', fontsize=14, fontweight='bold')
    
    for idx, model_name in enumerate(['Random Forest', 'Gradient Boosting']):
        importance = results[model_name]['feature_importance']
        sorted_idx = np.argsort(importance)
        
        axes[idx].barh(range(len(sorted_idx)), importance[sorted_idx], color='steelblue')
        axes[idx].set_yticks(range(len(sorted_idx)))
        axes[idx].set_yticklabels([feature_names[i] for i in sorted_idx])
        axes[idx].set_xlabel('Importance')
        axes[idx].set_title(f'{model_name} Feature Importance')
        axes[idx].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/logistics_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Route and Traffic Analysis
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Route and Traffic Analysis', fontsize=16, fontweight='bold')
    
    priority_dist = df['Delivery_Priority'].value_counts()
    axes[0, 0].pie(priority_dist.values, labels=priority_dist.index, autopct='%1.1f%%', colors=['green', 'orange', 'red'])
    axes[0, 0].set_title('Delivery Priority Distribution')
    
    time_of_day = df.groupby('Time_of_Day')['Delivery_Time_min'].mean()
    axes[0, 1].bar(time_of_day.index, time_of_day.values, color=['yellow', 'orange', 'purple'])
    axes[0, 1].set_title('Time of Day Impact')
    axes[0, 1].set_ylabel('Avg Time (minutes)')
    
    stops_times = df.groupby('Number_of_Stops')['Delivery_Time_min'].mean()
    axes[1, 0].plot(stops_times.index, stops_times.values, marker='o', color='teal', linewidth=2)
    axes[1, 0].set_title('Number of Stops vs Delivery Time')
    axes[1, 0].set_xlabel('Number of Stops')
    axes[1, 0].set_ylabel('Avg Time (minutes)')
    axes[1, 0].grid(alpha=0.3)
    
    weather_dist = df['Weather_Condition'].value_counts()
    axes[1, 1].bar(weather_dist.index, weather_dist.values, color=['blue', 'gray', 'cyan'])
    axes[1, 1].set_title('Weather Condition Distribution')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/logistics_route_traffic_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations generated successfully!")

def save_model_results(results):
    """Save model results to CSV"""
    results_data = []
    for model_name, metrics in results.items():
        results_data.append({
            'Model': model_name,
            'RMSE': round(metrics['RMSE'], 4),
            'MAE': round(metrics['MAE'], 4),
            'R2_Score': round(metrics['R2'], 4)
        })
    
    df_results = pd.DataFrame(results_data)
    df_results.to_csv('/home/ubuntu/logistics_model_results.csv', index=False)
    print("\nModel Results:")
    print(df_results)

def main():
    print("Generating logistics delivery data...")
    df = generate_delivery_data()
    
    print("Training regression models...")
    results, X_test, y_test, feature_names = train_models(df)
    
    print("Generating visualizations...")
    generate_visualizations(df, results, X_test, y_test, feature_names)
    
    print("Saving model results...")
    save_model_results(results)
    
    print("\nLogistics Delivery Time Prediction System completed successfully!")

if __name__ == "__main__":
    main()
