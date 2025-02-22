from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator, SQLColumnCheckOperator
from airflow.models import Variable
from include.fetch_api import *
from include.constant import *
import logging
import time
import os

@dag(
    start_date=datetime(2025, 2, 21), schedule='@daily',
    catchup=False, doc_md=__doc__,
    default_args={'owner': 'Wingscape'}, tags=['to_raw_db'],
    template_searchpath=[os.environ['AIRFLOW_HOME']])
def openaq_to_raw():
    """This DAG is used to get raw data from an API. Initial with manually triggered."""

    @task
    def get_raw_openaq(
        seconds_delayed: int = 1,
        api_pause_delayed: int = 5) -> list:
        """Fetch data from OpenAQ API.
        
        Args:
            seconds_delayed: Delay in seconds between each API call.
            api_pause_delayed: Number of API calls before pausing.
        """
        today_date = datetime.now().strftime('%Y-%m-%d')
        yesterday_date = (datetime.now() - timedelta(days = 1)).strftime('%Y-%m-%d')
        openaq_api_key = Variable.get('openaq_api_key')

        with open(OPENAQ_TEMP_FILENAME, 'w', encoding='utf-8', newline='') as file:
            for index, data in enumerate(OPENAQ_SOURCES):
                logging.info('Fetching data from OpenAQ API: {0}'.format(data['context']))

                data['params']['datetime_from'] = yesterday_date
                data['params']['datetime_to'] = today_date
                data['headers']['X-API-Key'] = openaq_api_key

                if (index+1) % api_pause_delayed == 0:
                    logging.info('Pausing for {0} seconds'.format(seconds_delayed))
                    time.sleep(seconds_delayed)

                openaq_data = fetch_data_from_api(api_url=data['endpoint'], 
                                                  params=data['params'], 
                                                  headers=data['headers'])
                
                file.write(set_api_to_query(openaq_data, data))
                logging.info('{0} data fetched and added to file'.format(data['context']))

    store_raw_data = SQLExecuteQueryOperator(
        task_id='store_raw_data',
        conn_id='urban_snowflake',
        sql=OPENAQ_TEMP_FILENAME,
        database='raw')
    
    raw_quality_check = SQLColumnCheckOperator(
        task_id='raw_quality_check',
        conn_id='urban_snowflake',
        database='raw',
        table='raw.public.data_source',
        column_mapping={'raw_data': {'null_check': {'equal_to': 0}}})
        
    get_raw_openaq() >> store_raw_data >> raw_quality_check

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOGGING_DATE_FORMAT,
    level=logging.INFO)

openaq_to_raw()
