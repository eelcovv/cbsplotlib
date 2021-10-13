import logging
import pandas as pd
from pathlib import Path

import cbsplotlib
from cbsplotlib.highcharts import CBSHighChart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_directory = "out"
data_input_directory = Path("../data/highcharts_examples")

input_file_name = data_input_directory / Path("cbs_hc_bar.csv")
data_df = pd.read_csv(input_file_name, sep=';', index_col=0, decimal=",")

logger.info(data_df)

hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  chart_type="bar",
                  output_directory=output_directory,
                  output_file_name="cbs_hc_bar_plot",
                  y_format="{:.1f}")

input_file_name = data_input_directory / Path("cbs_hc_column.csv")
data_df = pd.read_csv(input_file_name, sep=';', index_col=0, decimal=",")

logger.info(data_df)

hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  chart_type="bar",
                  output_directory=output_directory,
                  output_file_name="cbs_hc_bar_plot",
                  y_format="{:.1f}")
print("Done")
