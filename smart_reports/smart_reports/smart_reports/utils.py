import json
from django.db import connection
from decimal import Decimal

class Utils:

    def execute_sql_and_generate_chartjs_data(self, sql_command, chart_type, label_column, value_column):
        """
        Execute SQL command using Django's connection and generate Chart.js compatible data.

        Args:
            sql_command (str): The SQL query to execute.
            chart_type (str): The type of chart (e.g., 'bar', 'line', 'pie').
            label_column (str): The column to use as labels in the chart.
            value_column (str): The column to use as values in the chart.

        Returns:
            dict: Chart.js compatible data structure or error message.
        """
        try:
            with connection.cursor() as cursor:
                # Execute the SQL query
                cursor.execute(sql_command)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]  # Get column names
                
                # Ensure the required columns exist
                if chart_type not in ["single value", "table"] :
                    if (label_column not in columns or value_column not in columns):
                        raise ValueError("Specified label_column or value_column not in query results")
                else:      
                    if(len(rows) == 0):
                        data = []              
                    else:
                        data = rows if chart_type == "table" else [rows[0][0]]
                    return {
                        'type': chart_type,
                        'data': {
                            'labels': [],
                            'datasets': [
                                {
                                    'label': 'Dataset',
                                    'data': data,
                                    'backgroundColor': [],
                                    'borderColor': [],
                                }
                            ]
                        }
                    }
                
                # Prepare Chart.js data structure
                chart_data = {
                    'type': chart_type,
                    'data': {
                        'labels': [],
                        'datasets': []
                    }
                }

                if chart_type == 'table':
                    chart_data['data'] = {
                        'labels': [],  # column headers
                        'datasets': [
                            {
                                'data': []  # data rows
                            }
                        ]
                    }
                else:
                    chart_data['data'] = {
                        'labels': [],
                        'datasets': [
                            {
                                'label': 'Dataset',
                                'data': [],
                                'backgroundColor': [],
                                'borderColor': [],
                            }
                        ]
                    }

                if chart_type == 'table':
                    chart_data['data']['labels'] = columns
                    chart_data['data']['datasets'][0]['data'] = rows
                    return chart_data

                # Fill in the labels and data
                for row in rows:
                    chart_data['data']['labels'].append(row[columns.index(label_column)])
                    value = row[columns.index(value_column)]    
                    # Convert Decimal values to string
                    if isinstance(value, Decimal):
                        value = str(value)
                    
                    chart_data['data']['datasets'][0]['data'].append(value)
                    
                    # Add dynamic colors for certain chart types
                    if chart_type in ['pie', 'doughnut', 'polarArea']:
                        chart_data['data']['datasets'][0]['backgroundColor'].append(
                            f"rgba({row[columns.index(value_column)] % 256}, 100, 150, 0.7)"
                        )
                        chart_data['data']['datasets'][0]['borderColor'].append(
                            f"rgba({row[columns.index(value_column)] % 256}, 100, 150, 1)"
                        )
                
                return chart_data
        
        except Exception as e:
            print(e)
            return {'error': str(e)}

if __name__ == "__main__":
    print("Charts")