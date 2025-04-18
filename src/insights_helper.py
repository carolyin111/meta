"""
Helper module for processing and analyzing Meta Ads insights data.
"""

from datetime import datetime, timedelta
import pandas as pd
import json


def format_date_range(days_ago=7, end_date=None):
    """
    Create a date range dictionary for Meta API insights queries.
    
    Args:
        days_ago: Number of days to look back from end_date
        end_date: End date for the range (defaults to today)
        
    Returns:
        Dictionary with 'since' and 'until' dates in YYYY-MM-DD format
    """
    if end_date is None:
        end_date = datetime.now()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
    start_date = end_date - timedelta(days=days_ago)
    
    return {
        'since': start_date.strftime('%Y-%m-%d'),
        'until': end_date.strftime('%Y-%m-%d')
    }


def insights_to_dataframe(insights):
    """
    Convert Meta insights data to a pandas DataFrame for easier analysis.
    
    Args:
        insights: List of insight objects from the Meta API
        
    Returns:
        pandas DataFrame containing the insights data
    """
    if not insights:
        return pd.DataFrame()
    
    # Extract the data from insights objects
    data_list = []
    for insight in insights:
        # Convert insight object to dict if it's not already
        insight_dict = insight if isinstance(insight, dict) else dict(insight)
        
        # Extract nested action data if present
        if 'actions' in insight_dict:
            action_data = {}
            for action in insight_dict['actions']:
                action_type = action.get('action_type', 'unknown')
                action_value = action.get('value', 0)
                action_data[f"action_{action_type}"] = action_value
            
            # Remove the original actions list and merge in the flattened data
            del insight_dict['actions']
            insight_dict.update(action_data)
            
        data_list.append(insight_dict)
    
    # Create DataFrame
    df = pd.DataFrame(data_list)
    
    # Convert numeric columns
    numeric_columns = ['impressions', 'clicks', 'spend', 'ctr', 'cpc', 'reach', 'frequency']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def calculate_performance_metrics(insights_df):
    """
    Calculate additional performance metrics from insights data.
    
    Args:
        insights_df: DataFrame of insights data
        
    Returns:
        DataFrame with additional calculated metrics
    """
    df = insights_df.copy()
    
    # Calculate additional metrics if the required columns exist
    if 'spend' in df.columns and 'clicks' in df.columns and df['clicks'].sum() > 0:
        df['cpc'] = df['spend'] / df['clicks']
    
    if 'clicks' in df.columns and 'impressions' in df.columns and df['impressions'].sum() > 0:
        df['ctr'] = df['clicks'] / df['impressions'] * 100
    
    if 'conversions' in df.columns and 'clicks' in df.columns and df['clicks'].sum() > 0:
        df['conversion_rate'] = df['conversions'] / df['clicks'] * 100
    
    if 'conversions' in df.columns and 'spend' in df.columns and df['conversions'].sum() > 0:
        df['cost_per_conversion'] = df['spend'] / df['conversions']
    
    return df


def export_insights_to_csv(insights_df, filename):
    """
    Export insights DataFrame to a CSV file.
    
    Args:
        insights_df: DataFrame of insights data
        filename: Name of the CSV file to create
    """
    insights_df.to_csv(filename, index=False)
    print(f"Insights data exported to {filename}")


def format_insights_summary(insights_df):
    """
    Generate a text summary of the insights data.
    
    Args:
        insights_df: DataFrame of insights data
        
    Returns:
        String with formatted summary
    """
    if insights_df.empty:
        return "No insights data available."
    
    summary = "=== INSIGHTS SUMMARY ===\n"
    
    # Overall metrics
    summary += "\nOverall Performance:\n"
    metrics = {
        'Impressions': insights_df['impressions'].sum() if 'impressions' in insights_df.columns else 0,
        'Clicks': insights_df['clicks'].sum() if 'clicks' in insights_df.columns else 0,
        'Spend': f"${insights_df['spend'].sum():.2f}" if 'spend' in insights_df.columns else 0,
        'Average CTR': f"{insights_df['ctr'].mean():.2f}%" if 'ctr' in insights_df.columns else 0,
        'Average CPC': f"${insights_df['cpc'].mean():.2f}" if 'cpc' in insights_df.columns else 0,
    }
    
    for metric, value in metrics.items():
        summary += f"  {metric}: {value}\n"
    
    # Add conversion metrics if available
    if 'conversions' in insights_df.columns:
        conversion_metrics = {
            'Total Conversions': insights_df['conversions'].sum(),
            'Conversion Rate': f"{insights_df['conversion_rate'].mean():.2f}%" if 'conversion_rate' in insights_df.columns else 'N/A',
            'Cost per Conversion': f"${insights_df['cost_per_conversion'].mean():.2f}" if 'cost_per_conversion' in insights_df.columns else 'N/A',
        }
        
        summary += "\nConversion Metrics:\n"
        for metric, value in conversion_metrics.items():
            summary += f"  {metric}: {value}\n"
    
    return summary