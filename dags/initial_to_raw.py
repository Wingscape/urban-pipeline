from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator, SQLColumnCheckOperator
from include.fetch_api import fetch_data_from_api, set_api_to_query
from include.constant import WB_TEMP_FILENAME, WORLD_BANK_SOURCES, LOGGING_FORMAT, LOGGING_DATE_FORMAT
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
import logging
import time
import os

@dag(
    schedule=None, catchup=False, doc_md=__doc__,
    default_args={'owner': 'Wingscape'}, tags=['to_raw_db'],
    template_searchpath=[os.environ['AIRFLOW_HOME']])
def initial_to_raw():
    """Orchestrates the process of fetching raw data from the World Bank API, storing it in a Snowflake database, 
    and performing a quality check on the stored data.

    This function defines and executes a series of tasks:
    1. get_raw_world_bank: Fetches data from the World Bank API with specified delays between calls.
    2. store_raw_data: Executes an SQL query to store the fetched data in the 'raw' database.
    3. raw_quality_check: Performs a quality check on the stored data to ensure no null values in the 'raw_data' column.
    """
    dbt_project_path = '{0}/dbt/urban_transform'.format(os.environ['AIRFLOW_HOME'])
    dbt_executable_path = '{0}/dbt_env/bin/dbt'.format(os.environ['AIRFLOW_HOME'])

    profile_config = ProfileConfig(
        profile_name='urban_profile',
        target_name='urban',
        profile_mapping=SnowflakeUserPasswordProfileMapping(
            conn_id='urban_snowflake',
            profile_args={
                'database': 'urban',
                'schema': 'public'
            }))

    execution_config = ExecutionConfig(dbt_executable_path=dbt_executable_path)
    project_config = ProjectConfig(dbt_project_path=dbt_project_path)

    dimension_render_config = RenderConfig(select=['+dim_location', '+dim_source'],
                                           dbt_executable_path=dbt_executable_path)
    
    fact_render_config = RenderConfig(select=['stg_raw__world_banks', 'fact_urban_expansion'],
                                      dbt_executable_path=dbt_executable_path)

    @task
    def get_raw_world_bank(seconds_delayed: int = 1, api_pause_delayed: int = 5):
        """Fetches data from the World Bank API and writes it to a temporary file.

        Args:
            seconds_delayed: Number of seconds to pause after every 'api_pause_delayed' API calls.
            api_pause_delayed: Number of API calls after which to pause.
        """
        with open(WB_TEMP_FILENAME, 'w', encoding='utf-8', newline='') as file:
            for index, data in enumerate(WORLD_BANK_SOURCES):
                logging.info('Fetching data from World Bank API: {0}'.format(data['context']))

                if (index+1) % api_pause_delayed == 0:
                    logging.info('Pausing for {0} seconds'.format(seconds_delayed))
                    time.sleep(seconds_delayed)

                world_bank_data = fetch_data_from_api(api_url=data['endpoint'], 
                                                      params=data['params'], 
                                                      headers=data['headers'])
                
                file.write(set_api_to_query(world_bank_data, data))
                logging.info('{0} data fetched and added to file'.format(data['context']))

    store_raw_data = SQLExecuteQueryOperator(
        task_id='store_raw_data',
        conn_id='urban_snowflake',
        sql=WB_TEMP_FILENAME,
        database='raw')
    
    raw_quality_check = SQLColumnCheckOperator(
        task_id='raw_quality_check',
        conn_id='urban_snowflake',
        database='raw',
        table='raw.public.data_source',
        column_mapping={'raw_data': {'null_check': {'equal_to': 0}}})
    
    dimension_transform = DbtTaskGroup(
        group_id='world_bank_dimension',
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=dimension_render_config,
        operator_args={'install_deps': True})
    
    fact_transform = DbtTaskGroup(
        group_id='world_bank_fact',
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=fact_render_config,
        operator_args={'install_deps': True})
        
    get_raw_world_bank() >> store_raw_data >> raw_quality_check >> dimension_transform >> fact_transform

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOGGING_DATE_FORMAT,
    level=logging.INFO)

initial_to_raw()
