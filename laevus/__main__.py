#!/usr/bin/env python

"""laevus main script."""

import argparse
import logging
import signal
import sys

from chaussette.server import make_server as make_chaussette_server

from laevus import create_app, init_logging, read_config


def command_line_options():
    """Define command-line options and parse them."""
    parser = argparse.ArgumentParser(description=(
        'Wild life observations around roads'
    ))
    parser.add_argument('--config', '-c', default=None,
                        help='Path to the laevus configuration file')
    parser.add_argument('--chaussette-fd', '-f', type=int, default=None,
                        help='File descriptor of the socket to bind to with chaussette')
    return parser.parse_args()


def start_app():
    """Start the laevus Flask application.

    Use chaussette as a backend WSGI server.
    """
    args = command_line_options()
    config = read_config(args.config)
    app = create_app(config)
    init_logging(app.config['LOG_LEVEL'], app.config['LOG_FILENAME'])
    logging.info('Starting laevus...')
    if args.chaussette_fd is not None:
        srv = make_chaussette_server(app, host='fd://{0}'.format(args.chaussette_fd))
    else:
        strs = app.config['SERVER_NAME'].split(':')
        host, port = strs if len(strs) == 2 else (strs.pop(), '')
        port = int(port) if port.isdigit() else 5000
        srv = make_chaussette_server(app, host=host, port=port)
    signal.signal(signal.SIGINT, stop_app)
    signal.signal(signal.SIGTERM, stop_app)
    srv.serve_forever()


def stop_app(signal, frame):
    """Hook called when quitting application to cleanup before exiting."""
    logging.info('laevus stopped.')
    sys.exit(0)


main = start_app


if __name__ == '__main__':
    main()
