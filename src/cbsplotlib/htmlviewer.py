import argparse
import logging


_logger = logging.getLogger(__name__)

def _parse_arguments():

    parser = argparse.ArgumentParser(description="Tool om een highcharts html naar een rendered plaatje te converteren")

    parsed_args = parser.parse_args()

    return parsed_args
