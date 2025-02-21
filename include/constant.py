# Logging configuration
LOGGING_FORMAT = '(%(asctime)s) [%(levelname)s] %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

FILENAME = 'world_bank_temp.sql'

WORLD_BANK_SOURCES = [
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'total population',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/SP.POP.TOTL',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'total urban population',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/SP.URB.TOTL',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'total rural population',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/SP.RUR.TOTL',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'largest city population',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/EN.URB.LCTY',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'urban population percentage',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/SP.URB.TOTL.IN.ZS',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'rural population percentage',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/SP.RUR.TOTL.ZS',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'largest city population percentage',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/EN.URB.LCTY.UR.ZS',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    },
    {
        'source': 'world bank',
        'type': 'API',
        'context': 'air pollution mean annual exposure',
        'endpoint': 'https://api.worldbank.org/v2/country/IDN/indicator/EN.ATM.PM25.MC.M3',
        'params': {'format': 'json', 'date': '1999:2023'},
        'headers': None
    }
]
