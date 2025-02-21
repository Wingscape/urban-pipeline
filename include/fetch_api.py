import requests
import json

def fetch_data_from_api(api_url, params=None, headers=None):
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

def set_api_to_query(response: list, data_source: list) -> str:
    response_replace_none = json.dumps(response).replace('None', 'NULL')

    raw_query = """
    INSERT INTO raw.public.data_source (name, type, context, raw_data)
    SELECT '{0}', '{1}', '{2}', PARSE_JSON('{3}');
    """.format(data_source['source'], data_source['type'], data_source['context'], response_replace_none)

    return raw_query
