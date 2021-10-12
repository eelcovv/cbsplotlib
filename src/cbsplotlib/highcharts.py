import logging
import pandas as pd

_logger = logging.getLogger(__name__)

PLOT_TYPES = {"Line", "Area", "Column", "Bar", "Pie", "Polar", "Choropleth", "BubbleChart"}


class CBSHighChart:
    def __init__(self,
                 data: pd.DataFrame,
                 filename: str,
                 plot_type=None):
        self.data_df = data
        self.filename = filename
        _logger.debug(f"have data\n{data}")

        self.output = dict()
