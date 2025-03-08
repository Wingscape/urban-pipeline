import requests
import json

def fetch_data_from_api(api_url: str, params=None, headers=None) -> any:
    """Fetches data from the specified API URL.

    Args:
        api_url: The URL of the API endpoint.
        params (dict, optional): The query parameters to be sent with the request. Defaults to None.
        headers (dict, optional): The headers to be sent with the request. Defaults to None.
    Returns:
        any: The JSON response from the API.
    Raises:
        Exception: If the API is not available or the request fails.
        Exception: If the API response is not in JSON format.
    """
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception('API currently not available: {}'.format(e))
    except ValueError as e:
        raise Exception('API response not in JSON format: {}'.format(e))
    except Exception as e:
        raise Exception('API request failed: {}'.format(e))
    
    return response.json()

def set_api_to_query(response: any, data_source: dict) -> str:
    """Generates a SQL query to insert API response data into a database.

    Args:
        response: The API response data to be inserted.
        data_source: A dictionary containing the source, type, and context of the data.
    Returns:
        str: A SQL query string for inserting the data into the database.
    """
    response_replace_none = json.dumps(response).replace('None', 'NULL')

    raw_query = """
    INSERT INTO raw.public.data_source (name, type, context, raw_data)
    SELECT '{0}', '{1}', '{2}', PARSE_JSON('{3}');
    """.format(data_source['source'], data_source['type'], data_source['context'], response_replace_none)

    return raw_query
