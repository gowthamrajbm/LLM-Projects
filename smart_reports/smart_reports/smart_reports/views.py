from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from smart_reports.chains import Chain
from smart_reports.utils import Utils

chain = Chain()
utils = Utils()

def home_view(request):
    metadata = {}

    with connection.cursor() as cursor:
        # Get table names
        tables = connection.introspection.table_names(cursor)
        metadata['tables'] = []

        for table in tables:
            # Get columns for each table and ignore default "django" and "auth" tables
            if "django" in table or "auth" in table:
                continue
            columns = connection.introspection.get_table_description(cursor, table)
            metadata['tables'].append({
                'name': table,
                'columns': [{'name': col.name, 'type': col.type_code} for col in columns]
            })
    
    #home_dashboard_query = chain.generate_home_dashboard_queries(str(metadata))
    home_dashboard_query = [{'query': 'SELECT COUNT(id) AS total_games FROM game', 'chart_type': 'single value', 'label_column': None, 'value_column': 'total_games', 'title': 'Total Number of Games'}, {'query': 'SELECT genre_name, COUNT(game.id) AS num_games FROM genre INNER JOIN game ON genre.id = game.genre_id GROUP BY genre_name', 'chart_type': 'bar chart', 'label_column': 'genre_name', 'value_column': 'num_games', 'title': 'Number of Games by Genre'}, {'query': 'SELECT platform_name, COUNT(game_platform.id) AS num_games FROM platform INNER JOIN game_platform ON platform.id = game_platform.platform_id GROUP BY platform_name', 'chart_type': 'bar chart', 'label_column': 'platform_name', 'value_column': 'num_games', 'title': 'Number of Games by Platform'}, {'query': 'SELECT publisher_name, COUNT(game_publisher.publisher_id) AS num_games FROM publisher INNER JOIN game_publisher ON publisher.id = game_publisher.publisher_id GROUP BY publisher_name', 'chart_type': 'bar chart', 'label_column': 'publisher_name', 'value_column': 'num_games', 'title': 'Number of Games by Publisher'}, {'query': 'SELECT region_name, SUM(num_sales) AS total_sales FROM region INNER JOIN region_sales ON region.id = region_sales.region_id GROUP BY region_name', 'chart_type': 'bar chart', 'label_column': 'region_name', 'value_column': 'total_sales', 'title': 'Total Sales by Region'}, {'query': 'SELECT game_name, SUM(num_sales) AS total_sales FROM game INNER JOIN region_sales ON game.id = region_sales.game_platform_id GROUP BY game_name ORDER BY total_sales DESC LIMIT 10', 'chart_type': 'bar chart', 'label_column': 'game_name', 'value_column': 'total_sales', 'title': 'Top 10 Games by Total Sales'}, {'query': 'SELECT platform_name, SUM(num_sales) AS total_sales FROM platform INNER JOIN game_platform ON platform.id = game_platform.platform_id INNER JOIN region_sales ON game_platform.id = region_sales.game_platform_id GROUP BY platform_name', 'chart_type': 'pie chart', 'label_column': 'platform_name', 'value_column': 'total_sales', 'title': 'Total Sales by Platform'}, {'query': 'SELECT release_year, COUNT(game_platform.id) AS num_games FROM game_platform GROUP BY release_year', 'chart_type': 'line chart', 'label_column': 'release_year', 'value_column': 'num_games', 'title': 'Number of Games Released by Year'}]

    #print(home_dashboard_query)

    charts = []

    for item in home_dashboard_query:
        query = item['query']
        title = item['title']
        chart_type = item['chart_type']
        label_column = item['label_column']
        value_column = item['value_column']

        chart_data = utils.execute_sql_and_generate_chartjs_data(query, chart_type, label_column, value_column)

        charts.append({'title': title, 'chart_type': chart_type, 'data': chart_data, 'label_columns': label_column, 'value_column': value_column})
    
    print(metadata)
    print(charts)

    return render(request, 'home.html', {'metadata': metadata, 'charts': charts})
