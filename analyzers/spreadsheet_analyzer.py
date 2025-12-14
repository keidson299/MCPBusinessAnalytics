"""Spreadsheet analysis functions for business analytics MCP server"""

from typing import Dict, Any, List, Union
import json
from core.models import SpreadsheetData, CellAnalysis


def validate_spreadsheet_structure(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate and analyze spreadsheet structure.
    
    Args:
        data: List of row dictionaries from spreadsheet
        
    Returns:
        Dictionary with structure validation results
    """
    if not data:
        return {
            'is_valid': False,
            'message': 'Spreadsheet is empty',
            'row_count': 0,
            'column_count': 0,
            'columns': []
        }
    
    columns = list(data[0].keys())
    row_count = len(data)
    column_count = len(columns)
    
    # Check for missing values
    missing_count = sum(
        1 for row in data for col in columns if row.get(col) is None
    )
    
    return {
        'is_valid': True,
        'row_count': row_count,
        'column_count': column_count,
        'columns': columns,
        'missing_values': missing_count,
        'missing_percentage': round((missing_count / (row_count * column_count) * 100), 2) if row_count > 0 else 0,
        'data_types': _detect_column_types(data, columns)
    }


def _detect_column_types(data: List[Dict[str, Any]], columns: List[str]) -> Dict[str, str]:
    """Detect data types for each column."""
    types = {}
    
    for col in columns:
        sample_values = [row.get(col) for row in data if row.get(col) is not None]
        
        if not sample_values:
            types[col] = 'unknown'
        else:
            # Check first non-null value
            value = sample_values[0]
            if isinstance(value, bool):
                types[col] = 'boolean'
            elif isinstance(value, int):
                types[col] = 'integer'
            elif isinstance(value, float):
                types[col] = 'float'
            elif isinstance(value, str):
                types[col] = 'string'
            else:
                types[col] = type(value).__name__
    
    return types


def analyze_numeric_column(data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
    """
    Analyze numeric data in a column.
    
    Args:
        data: List of row dictionaries
        column: Column name to analyze
        
    Returns:
        Dictionary with numeric analysis
    """
    values = []
    
    for row in data:
        val = row.get(column)
        if val is not None and isinstance(val, (int, float)):
            values.append(float(val))
    
    if not values:
        return {'error': f'No numeric values found in column {column}'}
    
    values.sort()
    n = len(values)
    sum_val = sum(values)
    mean = sum_val / n
    
    # Calculate median
    if n % 2 == 0:
        median = (values[n // 2 - 1] + values[n // 2]) / 2
    else:
        median = values[n // 2]
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std_dev = variance ** 0.5
    
    return {
        'column': column,
        'count': n,
        'sum': sum_val,
        'mean': round(mean, 2),
        'median': round(median, 2),
        'min': values[0],
        'max': values[-1],
        'range': values[-1] - values[0],
        'std_dev': round(std_dev, 2),
        'q1': round(values[n // 4], 2) if n > 3 else None,
        'q3': round(values[3 * n // 4], 2) if n > 3 else None
    }


def detect_patterns(data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
    """
    Detect patterns and trends in column data.
    
    Args:
        data: List of row dictionaries
        column: Column name to analyze
        
    Returns:
        Dictionary with detected patterns
    """
    values = [row.get(column) for row in data]
    
    # Count occurrences
    value_counts = {}
    for val in values:
        if val is not None:
            key = str(val)
            value_counts[key] = value_counts.get(key, 0) + 1
    
    # Find most common values
    sorted_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'column': column,
        'unique_values': len(value_counts),
        'most_common': [{'value': val, 'count': count} for val, count in sorted_counts[:5]],
        'duplicates': sum(1 for count in value_counts.values() if count > 1)
    }


def filter_data(data: List[Dict[str, Any]], column: str, operator: str, value: Any) -> List[Dict[str, Any]]:
    """
    Filter spreadsheet data based on column criteria.
    
    Args:
        data: List of row dictionaries
        column: Column name to filter on
        operator: Comparison operator ('=', '!=', '>', '<', '>=', '<=', 'contains')
        value: Value to compare against
        
    Returns:
        Filtered list of rows
    """
    if column not in (data[0] if data else {}):
        return []
    
    filtered = []
    
    for row in data:
        cell_value = row.get(column)
        
        if operator == '=' or operator == '==':
            if cell_value == value:
                filtered.append(row)
        elif operator == '!=':
            if cell_value != value:
                filtered.append(row)
        elif operator == '>':
            try:
                if float(cell_value) > float(value):
                    filtered.append(row)
            except (TypeError, ValueError):
                pass
        elif operator == '<':
            try:
                if float(cell_value) < float(value):
                    filtered.append(row)
            except (TypeError, ValueError):
                pass
        elif operator == '>=':
            try:
                if float(cell_value) >= float(value):
                    filtered.append(row)
            except (TypeError, ValueError):
                pass
        elif operator == '<=':
            try:
                if float(cell_value) <= float(value):
                    filtered.append(row)
            except (TypeError, ValueError):
                pass
        elif operator == 'contains':
            if value in str(cell_value).lower():
                filtered.append(row)
    
    return filtered


def aggregate_data(data: List[Dict[str, Any]], group_by: str, aggregate_column: str, operation: str) -> List[Dict[str, Any]]:
    """
    Aggregate spreadsheet data by grouping and operation.
    
    Args:
        data: List of row dictionaries
        group_by: Column to group by
        aggregate_column: Column to aggregate
        operation: Operation ('sum', 'avg', 'count', 'min', 'max')
        
    Returns:
        List of aggregated results
    """
    groups = {}
    
    for row in data:
        key = row.get(group_by)
        value = row.get(aggregate_column)
        
        if key not in groups:
            groups[key] = []
        
        if value is not None:
            try:
                groups[key].append(float(value))
            except (TypeError, ValueError):
                if operation == 'count':
                    groups[key].append(1)
    
    results = []
    
    for key, values in groups.items():
        if not values:
            continue
        
        if operation == 'sum':
            result = sum(values)
        elif operation == 'avg' or operation == 'average':
            result = sum(values) / len(values) if values else 0
        elif operation == 'count':
            result = len(values)
        elif operation == 'min':
            result = min(values)
        elif operation == 'max':
            result = max(values)
        else:
            continue
        
        results.append({
            group_by: key,
            f'{operation}({aggregate_column})': round(result, 2) if isinstance(result, float) else result
        })
    
    return results
