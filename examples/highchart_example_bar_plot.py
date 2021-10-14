import logging
from pathlib import Path

from cbsplotlib.highcharts import CBSHighChart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_directory = "out"
data_input_directory = Path("../data/highcharts_examples")

# create bar plot (met horizontale balken)
input_file_name = data_input_directory / Path("cbs_hc_bar.csv")
# eerste keer runnen we alleen om de defaults template uit de package directory naar onze eigen script folder te
# schrijven
hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  chart_type="bar",
                  output_directory=output_directory,
                  output_file_name="cbs_hc_bar_plot",
                  defaults_out_file=input_file_name.stem)

# pas nu de template aan en run nogmaals zonder defaults_out_file om de highcharts met onze data te maken
# als je niks aan de template aanpast kan je ook direct de output highcharts maken.
hc = CBSHighChart(input_file_name=input_file_name.as_posix(),
                  defaults_file_name=input_file_name.stem + ".json",
                  chart_type="bar",
                  output_directory=output_directory,
                  output_file_name="cbs_hc_bar_plot", start=True)


logger.info("Done")