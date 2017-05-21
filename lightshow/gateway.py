import urllib2
import json
import time
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

TECTHULU_ENDPOINT = 'http://TecthulhuFF.local/portals/Tecthulhu05.json'
# can also be status/faction, status/health

USB_ENABLED = False
USB_ENDPOINT = '/dev/tty.usbmodem1411'


logging.config.dictConfig(LOG_SETTINGS)

def main():
    """
    gateway entrypoint
    """
    logger = logging.getLogger('lightshow')
    running = True
    logger.info("Starting gateway, press C-c to exit")

    # set up usb
    if USB_ENABLED:
        usb = serial.Serial(USB_ENDPOINT)

    # state variables
    prev_states = []

    while running:

        try:

            # fetch data from tecthulu
            raw_response = urllib2.urlopen(
                urllib2.Request(TECTHULU_ENDPOINT)
            ).read()

            resp = json.loads(raw_response)['externalApiPortal']

            print 'request made'

            # load into previous state, hold up to last 10
            if len(prev_states) == 0:
                print 'first state'
                print resp
                prev_states.append(resp)    # first time double load

            prev_states.append(resp)
            prev_states = prev_states[-10:]

            # for now, just get current and previous state
            current_state = prev_states[-1]
            before_state = prev_states[-2]




            # health change
            health_change = 'same'

            if current_state['health'] < before_state['health']:
                print 'health decreased'
                health_change = 'weaker'

            elif current_state['health'] > before_state['health']:
                print 'health increased'
                health_change = 'stronger'

            if current_state['resonators'] != before_state['resonators']:
                print 'reso state change'


            final_command = ' '.join([
                current_state['controllingFaction'],
                str(int(current_state['health'])),
                health_change
            ])

            if USB_ENABLED:
                usb.write(final_command + '\n')
            else:
                print final_command

            # sleep between polls
            time.sleep(3)


    # deserialize json

    # return line format

    #event loop
        #raise NotImplementedError("Not Implemented")

            except KeyboardInterrupt:
                logger.info("exiting")
                if USB_ENABLED:
                    usb.close()
            except Exception as e:
                print raw_response
                logger.error(str(e))
                continue

if __name__ == "__main__":
    main()
