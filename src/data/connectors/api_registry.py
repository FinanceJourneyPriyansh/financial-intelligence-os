"""
Financial Intelligence OS
API Registry

Defines all supported data providers.
"""

API_REGISTRY = {

    "world_bank": {

        "name": "World Bank",

        "base_url": "https://api.worldbank.org/v2",

        "format": "json",

        "timeout": 30,

        "endpoints": {

            "countries": "/country",

            "indicators": "/indicator",

            "economy": "/country/{country}/indicator/{indicator}",

        },

    },

}