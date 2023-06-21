import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://cosmosdbapp5.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'qmwxWIdka0a5k592YWFMZNWA0Gu7ZzBAllWpCv7yJfeBgIao7ebteqtcpX04Ao4r552lDyU45flcACDbV3qiZA=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'PurviewMetadata'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}