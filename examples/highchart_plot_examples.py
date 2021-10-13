import logging
import pandas as pd
from pathlib import Path

import cbsplotlib
from cbsplotlib.highcharts import CBSHighChart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_directory = "out"
data_input_directory = Path("../data/highcharts_examples")

csv_data = """
dim_gk,2016,2017,2018,2019
2 tot 10 werkzame personen,32,37,43,44
10 tot 50 werkzame personen,54,61,69,65
50 tot 250 werkzame personen,82,83,89,89
250 of meer werkzame personen,94,94,98,98
"""
# data_df = pd.read_csv(io.StringIO(csv_data))

input_file_name = data_input_directory / Path("cbs_hc_bar.csv")
data_df = pd.read_csv(input_file_name, sep=';', index_col=0, decimal=",")

logger.info(data_df)

hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  chart_type="bar",
                  output_directory=output_directory)
print("Done")
