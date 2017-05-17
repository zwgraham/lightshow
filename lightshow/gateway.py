import urllib2
import json
import serial
import logging
import logging.config

LOG_SETTINGS = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'simple',
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': logging.DEBUG,
            'formatter': 'detailed',
            'filename': 'gateway.log',
        }
    },
    'formatters': {
        'detailed': {
            'format': ('%(asctime)s %(module)-8s line:%(lineno)-4d '
                       '%(levelname)s %(message)s'),
        },
        'simple': {
            'format': '%(asctime)-8s %(levelname)s %(message)s',
        },
    },
    'loggers': {
        'lightshow': {
            'level': logging.DEBUG,
            'handlers': ['console', 'fileHandler'],
        },
    },
}
logging.config.dictConfig(LOG_SETTINGS)

def main():
    """
    gateway entrypoint
    """
    logger = logging.getLogger('lightshow')
    running = True
    logger.info("Starting gateway, press C-c to exit")
    logger.debug("SDLFKJSDLFKJSDF")
    try:
        while running:
        #event loop
            raise NotImplementedError("Not Implemented")

    except KeyboardInterrupt:
        logger.info("exiting")
    except Exception as e:
        logger.error(str(e))

if __name__ == "__main__":
    main()
