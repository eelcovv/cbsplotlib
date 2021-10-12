import logging
import json
import pandas as pd

_logger = logging.getLogger(__name__)

PLOT_TYPES = {"line", "area", "column", "bar", "pie", "polar", "choropleth", "bubbleChart"}


class Chart:
    def __init__(self,
                 chart_type="bar",
                 inverted=True,
                 spacingLeft=54,
                 marginRight=45,
                 animation=False,
                 polar=False,
                 events={}):
        self.name: str = "chart"
        self._prop = {
            "type": chart_type,
            "inverted": inverted,
            "spacingLeft": spacingLeft,
            "marginRight": marginRight,
            "animation": animation,
            "polar": polar,
            "events": events
        }

    def serialize(self):
        return self._prop


class CBSHighChart:
    def __init__(self,
                 data: pd.DataFrame,
                 filename: str = None,
                 plot_type: str = None):
        self.data_df = data
        self.filename = filename
        _logger.debug(f"have data\n{data}")

        self.chart = None
        self.output = {}

        self.add_template()
        self.add_options()

        self.write_to_file()

    def add_template(self):
        self.chart = Chart()
        template = {}
        template[self.chart.name] = self.chart.serialize()
        self.output["template"] = template

    def add_options(self):
        options = {}
        self.output["options"] = options

    def write_to_file(self, json_indent=4):
        if self.filename is None:
            outfile = self.chart.name + ".json"
        else:
            outfile = self.filename
        with open(outfile, "w") as stream:
            stream.write(json.dumps(self.output, indent=json_indent))
