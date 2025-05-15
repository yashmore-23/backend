import logging
from logging.config import dictConfig
import os

# Define your log file path
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app_logs.log")

# Ensure the logs directory exists
log_dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def setup_logging():
    # Logging configuration for local file
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': LOG_FILE_PATH,  # Log file path
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    })

