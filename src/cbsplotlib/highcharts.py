import logging
import json
import pandas as pd
from pathlib import Path

_logger = logging.getLogger(__name__)

PLOT_TYPES = {"line", "area", "column", "bar", "pie", "polar", "choropleth", "bubbleChart"}


class HCElement:
    def __init__(self, chart_type=None):
        self.chart_type = chart_type
        self._prop = {}

    def serialize(self):
        return self._prop


class Chart(HCElement):
    def __init__(self,
                 chart_type=None,
                 inverted=None,
                 spacing_left=None,
                 margin_right=None,
                 margin_bottom=None,
                 animation=False,
                 polar=False,
                 events={}
                 ):
        super().__init__(chart_type=chart_type)

        self.name: str = "chart"

        assert chart_type in ("line", "bar", "column")

        self.chart_type = chart_type

        # initieer de properties met het type plot
        self._prop["chart_type"] = chart_type

        # zet nu de waarden die alleen voor bepaalde types gezet worden
        if chart_type == "line":
            if margin_bottom is None:
                margin_bottom = 180
        elif chart_type == "bar":
            if margin_right is None:
                margin_right = 45
            if spacing_left is None:
                spacing_left = 54
            if inverted is not None:
                inverted = False
        elif chart_type == "column":
            if inverted is not None:
                inverted = False

        if inverted is not None:
            self._prop["inverted"] = inverted
        if spacing_left is not None:
            self._prop["spacingLeft"] = spacing_left
        if margin_right is not None:
            self._prop["marginRight"] = margin_right
        if margin_bottom is not None:
            self._prop["marginBottom"] = margin_bottom

        # nu de velden die altijd gegeven worden
        self._prop["polar"] = polar
        self._prop["animation"] = animation


class PlotOptions(HCElement):
    def __init__(self,
                 chart_type=None,
                 stacking=None,
                 point_placement=None,
                 events={},
                 max_point_width=60,
                 point_padding=None,
                 group_padding=None,
                 border_width=None,
                 line_width=None
                 ):
        super().__init__(chart_type=chart_type)
        series = {
                     "stacking": stacking,
                     "pointPlacement": point_placement,
                     "events": events,
                     "maxPointWidth": max_point_width
                 },
        self._prop["series"] = series

        if self.chart_type == "bar":
            if point_padding is None:
                point_padding = 0.04
            else:
                point_padding = point_padding
            if group_padding is None:
                group_padding = 0.08
            else:
                group_padding = group_padding
            if border_width is None:
                border_width = 1
            else:
                border_width = border_width
            bar = {
                "pointPadding": point_padding,
                "groupPadding": group_padding,
                "borderWidth": border_width
            }
            self._prop["bar"] = bar


class CBSHighChart:
    def __init__(self,
                 data: pd.DataFrame,
                 filename: str = None,
                 output_directory: str = None,
                 chart_type: str = None,
                 chart_inverted=None,
                 chart_spacing_left=None,
                 chart_margin_right=None,
                 chart_margin_bottom=None,
                 chart_animation=False,
                 chart_polar=False,
                 chart_events={}
                 ):
        self.chart_type = chart_type
        self.data_df = data
        self.filename = filename
        if output_directory is None:
            self.output_directory = Path(".")
        else:
            self.output_directory = Path(output_directory)
        self.chart_inverted = chart_inverted
        self.chart_spacing_left = chart_spacing_left
        self.chart_margin_right = chart_margin_right
        self.chart_margin_bottom = chart_margin_bottom
        self.chart_animation = chart_animation
        self.chart_polar = chart_polar
        self.chart_events = chart_events

        _logger.debug(f"have data\n{data}")

        self.output = {}

        self.add_template()
        self.add_options()

        self.write_to_file()

    def add_template(self):
        chart = Chart(chart_type=self.chart_type,
                      inverted=self.chart_inverted,
                      spacing_left=self.chart_spacing_left,
                      margin_right=self.chart_margin_right,
                      margin_bottom=self.chart_margin_bottom,
                      animation=self.chart_animation,
                      polar=self.chart_animation,
                      events=self.chart_events
                      )
        template = {}
        template["chart"] = chart.serialize()

        plot_options = PlotOptions(chart_type=self.chart_type)
        template["plotOptions"] = plot_options.serialize()

        self.output["template"] = template

    def add_options(self):
        options = {}
        self.output["options"] = options

    def write_to_file(self, json_indent=4):
        self.output_directory.mkdir(exist_ok=True)
        if self.filename is None:
            outfile = self.output_directory / Path("_".join(["highchart", self.chart_type, "plot"]) + ".json")
        else:
            outfile = self.output_directory / Path(self.filename)
        with open(outfile.as_posix(), "w") as stream:
            stream.write(json.dumps(self.output, indent=json_indent))
