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


class Categories(HCElement):
    def __init__(self,
                 chart_type=None,
                 values=None
                 ):
        super().__init__(chart_type=chart_type)

        categories = values
        self._prop["categories"] = values


class Axis(HCElement):
    def __init__(self,
                 chart_type=None,
                 draw_horizontal_borders=False,
                 line_color="#666666",
                 line_width=1,
                 tick_color="#C6C6C6",
                 tick_length=0,
                 title=None,
                 categories=None,
                 labels=None,
                 tickmark_placement="between",
                 start_on_tick=False,
                 show_first_label=False,
                 end_on_tick=False,
                 show_last_label=False,
                 ):
        super().__init__(chart_type=chart_type)

        axis = {
            "drawHorizontalBorders": draw_horizontal_borders,
            "lineColor": line_color,
            "lineWidth": line_width,
            "tickColor": tick_color,
            "tickLength": tick_length,
        }
        if title is not None:
            axis["title"] = title
        if labels is not None:
            axis["labels"] = labels

        axis["tickmarkPlacement"] = tickmark_placement
        axis["startOnTick"] = start_on_tick
        axis["showFirstLabel"] = show_first_label
        axis["endOnTick"] = end_on_tick
        axis["showLastLabel"] = show_last_label

        if categories is not None:
            axis["categories"] = categories

        for key, value in axis.items():
            self._prop[key] = value


class Style(HCElement):
    def __init__(self,
                 chart_type=None,
                 font_family=None,
                 font_size=None,
                 color=None,
                 ):

        super().__init__(chart_type=chart_type)

        style = {}
        if font_family is not None:
            style["fontFamily"] = font_family
        if font_size is not None:
            style["fontSize"] = font_size
        if color is not None:
            style["color"] = color

        for key, value in style.items():
            self._prop[key] = value


class Title(HCElement):
    def __init__(self,
                 chart_type=None,
                 style=None,
                 align="left",
                 x_shift=None,
                 use_html=None,
                 rotation=None,
                 ):
        super().__init__(chart_type=chart_type)

        title = {
            "align": align,
        }
        if style is not None:
            title["style"] = style
        if x_shift is not None:
            title["x"] = x_shift
        if use_html is not None:
            title["useHTML"] = use_html
        if rotation is not None:
            title["rotation"] = rotation

        for key, value in title.items():
            self._prop[key] = value


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
                 chart_title: str = None,
                 chart_subtitle: str = None,
                 chart_inverted=None,
                 chart_spacing_left=None,
                 chart_margin_right=None,
                 chart_margin_bottom=None,
                 chart_animation=False,
                 chart_polar=False,
                 chart_events={}
                 ):
        self.data_df = data
        self.filename = filename
        if output_directory is None:
            self.output_directory = Path(".")
        else:
            self.output_directory = Path(output_directory)

        self.chart_type = chart_type
        self.chart_title = chart_title
        self.chart_subtitle = chart_subtitle
        self.chart_inverted = chart_inverted
        self.chart_spacing_left = chart_spacing_left
        self.chart_margin_right = chart_margin_right
        self.chart_margin_bottom = chart_margin_bottom
        self.chart_animation = chart_animation
        self.chart_polar = chart_polar
        self.chart_events = chart_events

        _logger.debug(f"have data\n{data}")

        self.template = {}
        self.output = {}

        self.add_template_chart()
        self.add_template_plot_options()
        self.add_template_title()
        self.add_template_title(title_key="subtitle")
        self.add_template_axis()

        self.output["template"] = self.template

        self.add_options()

        self.write_to_file()

    def add_template_chart(self):
        chart = Chart(chart_type=self.chart_type,
                      inverted=self.chart_inverted,
                      spacing_left=self.chart_spacing_left,
                      margin_right=self.chart_margin_right,
                      margin_bottom=self.chart_margin_bottom,
                      animation=self.chart_animation,
                      polar=self.chart_animation,
                      events=self.chart_events
                      )
        self.template["chart"] = chart.serialize()

    def add_template_plot_options(self):
        plot_options = PlotOptions(chart_type=self.chart_type)
        self.template["plotOptions"] = plot_options.serialize()

    def add_template_title(self, title_key=" title"):

        if self.chart_title is not None:
            style = Style(font_family="\"Soho W01 Medium\", \"Cambria\", sans-serif",
                          font_size="17px",
                          color="#000")
            title = Title(style=style.serialize())
        else:
            title = Title()

        self.template[title_key] = title.serialize()

    def add_template_axis(self, axis_key="xAxis"):

        categories = Categories(self.data_df.index)

        style = Style()
        title = Title(align="high", style=style.serialize(), use_html=True, rotation=0)

        label_style = Style(font_size="11px", color="#000000")
        labels = Title(style=label_style.serialize())

        axis = Axis(categories=categories.serialize(),
                    title=title.serialize(),
                    labels=labels.serialize())
        self.template[axis_key] = axis.serialize()
        _logger.debug("axis: {axis}")

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
