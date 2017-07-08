#!/usr/bin/env python3
#
# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# BSD 3-Clause License (see LICENSE file)

import sys
import argparse

from .unit import AtreaUnitRD5

import logging
import logging.config
logger = logging.getLogger(__name__)


def configure_logging(level=logging.INFO):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            }
        }
    })


def construct_argparser():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
        prog='pytrea',
        description='Simple application for communicating with remote Atrea air ventilation unit over Modbus TCP.'
    )
    parser.add_argument(
        '-s',
        '--server',
        required=True,
        help='IP address of the Atrea unit.'
    )
    parser.add_argument(
        '-p',
        '--port',
        default=None,
        help='Port on which the Atrea unit server listens.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        default=False,
        action='store_true',
        help='Make the output more verbose.'
    )

    return parser


def main(cli_args=None):
    arg_parser = construct_argparser()
    # parse arguments passed on CLI
    cli_config = arg_parser.parse_args(cli_args)

    if cli_config.verbose:
        configure_logging(logging.DEBUG)
    else:
        configure_logging()

    unit = AtreaUnitRD5(cli_config.server)

    temp = unit.read_temperature_cp()
    logger.info("CP temp: %f", temp)

    unit.client.close()


if __name__ == '__main__':
    main(sys.argv[1:])
