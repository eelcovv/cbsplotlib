import logging
import pandas as pd
import io
from cbsplotlib.highcharts import CBSHighChart

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

csv_data = """
dim_gk,2016,2017,2018,2019
2 tot 10 werkzame personen,32,37,43,44
10 tot 50 werkzame personen,54,61,69,65
50 tot 250 werkzame personen,82,83,89,89
250 of meer werkzame personen,94,94,98,98
"""
#data_df = pd.read_csv(io.StringIO(csv_data))

data_df = pd.read_csv("cbs_hc_bar.csv")

logger.info(data_df)

hc = CBSHighChart(data_df, chart_type="bar")
print("Done")
