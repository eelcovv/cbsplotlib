import logging
from pathlib import Path

from cbsplotlib.highcharts import CBSHighChart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_directory = "out"
data_input_directory = Path("../data/highcharts_examples")

# create bar plot (met horizontale balken)
input_file_name = data_input_directory / Path("cbs_hc_bar.csv")
hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  chart_type="bar",
                  output_directory=output_directory,
                  output_file_name="cbs_hc_bar_plot")

logger.info("Done")