import enum


class DataSourceType:
    CSV = 'csv'
    URL = 'url'
    DOCX = 'docx'
    PDF = 'pdf'
    NOTIONPAGES = 'notionpages'
    


class SourceStatus:
    TRAINED = 'Trained'
    FAILED = 'Failed'
    PROCESSING = 'Processing'
    
    
ALLOWED_FILE_TYPES = ["pdf", "csv", "docx"]

FILES_AND_URL = ['pdf', 'csv', 'docx', 'url']