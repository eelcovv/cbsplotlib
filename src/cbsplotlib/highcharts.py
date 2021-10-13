import logging
import json
import pandas as pd
from decimal import Decimal, Rounded
from pathlib import Path
import functools
import cbsplotlib

_logger = logging.getLogger(__name__)


@functools.wraps(cbsplotlib.set_loglevel)
def set_loglevel(*args, **kwargs):
    return cbsplotlib.set_loglevel(*args, **kwargs)


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
                 height=None,
                 style=None,
                 animation=False,
                 polar=False,
                 events=None
                 ):
        super().__init__(chart_type=chart_type)

        self.name: str = "chart"

        # initieer de properties met het type plot
        if chart_type is not None:
            assert chart_type in ("line", "bar", "column")
            self._prop["type"] = chart_type

        if inverted is not None:
            self._prop["inverted"] = inverted
        if spacing_left is not None:
            self._prop["spacingLeft"] = spacing_left
        if margin_right is not None:
            self._prop["marginRight"] = margin_right
        if margin_bottom is not None:
            self._prop["marginBottom"] = margin_bottom
        if height is not None:
            self._prop["height"] = height
        if style is not None:
            self._prop["style"] = style.serialize()

        # nu de velden die altijd gegeven worden
        if polar is not None:
            self._prop["polar"] = polar
        if animation is not None:
            self._prop["animation"] = animation
        if events is not None:
            self._prop["events"] = events


class Categories(HCElement):
    def __init__(self,
                 chart_type=None,
                 series=None
                 ):
        super().__init__(chart_type=chart_type)

        self._prop["values"] = series.to_list()


class Axis(HCElement):
    def __init__(self,
                 chart_type=None,
                 draw_horizontal_borders=False,
                 line_color="#666666",
                 line_width=1,
                 tick_color="#C6C6C6",
                 tick_length=0,
                 grid_line_color=None,
                 grid_line_width=None,
                 grid_line_interpolation=None,
                 title=None,
                 categories=None,
                 labels=None,
                 tickmark_placement="between",
                 start_on_tick=False,
                 show_first_label=True,
                 end_on_tick=False,
                 show_last_label=True,
                 reversed_stacks=None,
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
            axis["title"] = title.serialize()

        if labels is not None:
            axis["labels"] = labels.serialize()

        axis["tickmarkPlacement"] = tickmark_placement
        axis["startOnTick"] = start_on_tick
        axis["showFirstLabel"] = show_first_label
        axis["endOnTick"] = end_on_tick
        axis["showLastLabel"] = show_last_label

        if grid_line_color is not None:
            axis["gridLineColor"] = grid_line_color

        if grid_line_width is not None:
            axis["gridLineWidth"] = grid_line_width

        if reversed_stacks is not None:
            axis["reversedStacks"] = reversed_stacks

        axis["gridLineInterpolation"] = grid_line_interpolation

        if categories is not None:
            axis["categories"] = categories.serialize()['values']

        for key, value in axis.items():
            self._prop[key] = value


class PlotLine(HCElement):
    def __init__(self):
        super().__init__()
        plot_line = {
            "value": "0",
            "width": 2,
            "color": "#666666",
            "zIndex": 4
        }
        for key, value in plot_line.items():
            self._prop[key] = value


class Credits(HCElement):

    def __init__(self,
                 enabled=False,
                 ):
        super().__init__()

        plot_credits = {
            "enabled": enabled
        }
        for key, value in plot_credits.items():
            self._prop[key] = value


class ToolTip(HCElement):

    def __init__(self,
                 shared=True,
                 follow_pointer=True,
                 use_html=True
                 ):
        super().__init__()

        tooltip = {}

        if shared is not None:
            tooltip["shared"] = shared
        if follow_pointer is not None:
            tooltip["followPointer"] = follow_pointer
        if use_html is not None:
            tooltip["useHTML"] = use_html

        for key, value in tooltip.items():
            self._prop[key] = value


class Legend(HCElement):
    def __init__(self,
                 align="left",
                 reversed_legend=False,
                 vertical_align="bottom",
                 y_shift=-40,
                 padding=0,
                 symbol_radius=0,
                 symbol_height=10,
                 symbol_width=25,
                 square_symbol=False,
                 symbol_padding=10,
                 item_distance=25,
                 item_margin_bottom=6,
                 use_html=True,
                 item_style=None,
                 item_hidden_style=None,
                 ):
        super().__init__()
        legend = {}
        if align is not None:
            legend["align"] = align
        if reversed_legend is not None:
            legend["reversed"] = reversed_legend
        if vertical_align is not None:
            legend["verticalAlign"] = vertical_align
        if y_shift is not None:
            legend["y"] = y_shift
        if padding is not None:
            legend["padding"] = padding
        if symbol_radius is not None:
            legend["symbolRadius"] = symbol_radius
        if symbol_height is not None:
            legend["symbolHeight"] = symbol_height
        if symbol_width is not None:
            legend["symbolWidth"] = symbol_width
        if square_symbol is not None:
            legend["squareSymbol"] = square_symbol
        if item_style is not None:
            legend["itemStyle"] = item_style.serialize()
        if item_hidden_style is not None:
            legend["itemHiddenStyle"] = item_hidden_style.serialize()
        if symbol_padding is not None:
            legend["symbolPadding"] = symbol_padding
        if item_distance is not None:
            legend["symbolDistance"] = item_distance
        if item_margin_bottom is not None:
            legend["symbolMarginBottom"] = item_margin_bottom
        if use_html is not None:
            legend["useHTML"] = use_html

        for key, value in legend.items():
            self._prop[key] = value


class Style(HCElement):
    def __init__(self,
                 chart_type=None,
                 font_weight=None,
                 font_family=None,
                 font_size=None,
                 color=None,
                 ):

        super().__init__(chart_type=chart_type)

        style = {}
        if font_weight is not None:
            style["fontWeight"] = font_weight
        if font_family is not None:
            style["fontFamily"] = font_family
        if font_size is not None:
            style["fontSize"] = font_size
        if color is not None:
            style["color"] = color

        for key, value in style.items():
            self._prop[key] = value


class Text(HCElement):
    def __init__(self,
                 chart_type=None,
                 text=None,
                 style=None,
                 align=None,
                 x_shift=None,
                 use_html=None,
                 rotation=None,
                 enabled=None,
                 auto_rotation=None,
                 ):
        super().__init__(chart_type=chart_type)

        text = {
            "text": text,
        }
        if align is not None:
            text["align"] = align
        if style is not None:
            text["style"] = style.serialize()
        if x_shift is not None:
            text["x"] = x_shift
        if use_html is not None:
            text["useHTML"] = use_html
        if rotation is not None:
            text["rotation"] = rotation
        if auto_rotation is not None:
            text["auto_rotation"] = auto_rotation
        if enabled is not None:
            text["enabled"] = enabled

        for key, value in text.items():
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
                 data: pd.DataFrame = None,
                 input_file_name: str = None,
                 output_file_name: str = None,
                 output_directory: str = None,
                 defaults_directory: str = None,
                 defaults_filename: str = None,
                 modifications_filename: str = None,
                 chart_type: str = None,
                 csv_separator: str = ";",
                 decimal: str = ",",
                 index_col: int = 0,
                 y_format: str = None,
                 chart_title: str = None,
                 chart_subtitle: str = None,
                 chart_title_font_family="\"Soho W01 Medium\", \"Cambria\", sans-serif",
                 chart_title_font_size="17px",
                 chart_title_color="#000",
                 chart_inverted=None,
                 chart_spacing_left=None,
                 chart_margin_right=None,
                 chart_margin_bottom=None,
                 chart_animation=False,
                 chart_polar=False,
                 chart_events=None
                 ):
        self.data_df = data
        self.input_file_name = input_file_name
        self.csv_separator = csv_separator
        self.decimal = decimal
        self.index_col = index_col
        if self.data_df is None:
            if self.input_file_name is None:
                raise TypeError("Both input data argument *data_df* and input filename "
                                "*input_file_name* are None. Please provide at least one.")
            else:
                _logger.info(f"Reading {input_file_name}")
                self.data_df = pd.read_csv(input_file_name,
                                           sep=self.csv_separator,
                                           index_col=self.index_col,
                                           decimal=self.decimal)

        self.y_format = y_format
        if chart_type is None:
            # defaults chart type is a bar plot
            self.chart_type = "bar"
        else:
            self.chart_type = chart_type

        self.output_filename = output_file_name
        self.output = {
            "template": {},
            "options": {},
            "selectedTemplate": {}
        }

        if output_directory is None:
            self.output_directory = Path(".")
        else:
            self.output_directory = Path(output_directory)

        # hier worden alle defaults in de self.defaults attribute geladen
        self.defaults = self.read_the_defaults(chart_type=chart_type,
                                               defaults_directory=defaults_directory,
                                               defaults_filename=defaults_filename,
                                               modifications_filename=modifications_filename)

        self.add_chart()
        self.add_plot_options()

        self.add_title(text_key="title")
        self.add_title(text_key="subtitle")

        self.add_axis(axis_key="xAxis", categories=self.data_df.index.to_list())
        self.add_axis(axis_key="yAxis")
        self.add_legend()
        self.add_tooltip()
        self.add_credits()

        self.add_options()
        self.add_csv_data()
        self.add_series()
        self.add_axis(key="options", axis_key="xAxis", categories=self.data_df.index.to_list())
        self.add_axis(key="options", axis_key="yAxis")

        self.add_selected_templated()

        self.write_to_file()

    @staticmethod
    def read_the_defaults(chart_type=None,
                          defaults_directory=None,
                          defaults_filename=None,
                          modifications_filename=None):

        def modify_the_defaults(mod_defaults, mods):

            for chapter_key, chapter_prop in mods:
                for section_key, section_prop in chapter_prop:
                    if isinstance(section_prop, dict):
                        for subsection_key, subsection_prop in section_prop:
                            mod_defaults[chapter_key][section_key][subsection_key] = subsection_prop
                    else:
                        mod_defaults[chapter_key][section_key] = section_prop
            return mod_defaults

        if defaults_directory is None:
            defaults_directory = Path(__file__).parent / Path("cbs_hc_defaults")
        else:
            defaults_directory = Path(defaults_directory)

        if defaults_filename is None:
            defaults_filename = defaults_directory / Path(chart_type + ".json")
        else:
            defaults_filename = defaults_directory / Path(defaults_filename)

        if modifications_filename is not None:
            modifications_filename = Path(modifications_filename)

        with open(defaults_filename, "r") as stream:
            defaults = json.load(stream)

        if modifications_filename is not None:
            with open(modifications_filename, "r") as stream:
                modifications = json.load(stream)
            defaults = modify_the_defaults(defaults, modifications)

        return defaults

    def add_plot_lines(self, key="template"):

        self.output[key]["plotLines"] = self.defaults[key]["plotLines"]

    def add_chart(self, key="template"):

        self.output[key]["chart"] = self.defaults[key]["chart"]

    def add_plot_options(self, key="template"):
        self.output[key]["plotOptions"] = self.defaults[key]["plotOptions"]

    def add_title(self, key="template", text_key="title"):

        self.output[key][text_key] = self.defaults[key][text_key]

    def add_tooltip(self, key="template"):

        self.output[key]["tooltip"] = self.defaults[key]["tooltip"]

    def add_credits(self, key="template"):

        self.output[key]["credits"] = self.defaults[key]["credits"]

    def add_legend(self, key="template"):

        self.output[key]["legend"] = self.defaults[key]["legend"]

    def add_axis(self,
                 key="template",
                 axis_key="xAxis",
                 categories=None,
                 ):

        self.output[key][axis_key] = self.defaults[key][axis_key]

        if categories is not None:
            for ax in self.output[key][axis_key]:
                ax["categories"] = categories

    def add_options(self):
        self.output["options"] = self.defaults["options"]

    def add_csv_data(self, key="options", settings_keys="settings"):

        csv = self.data_df.to_csv(sep=self.csv_separator, decimal=self.decimal, float_format="%g")
        self.output[key][settings_keys]["csvData"] = csv.rstrip()

    def add_series(self, key="options", series_key="series"):

        if self.y_format is None:
            self.y_format = "{:g}"

        series = list()
        for col_name in self.data_df.columns:
            item = {
                "name": col_name,
                "isSerie": True,
                "borderColor": "#FFFFFF",
                "data": list()
            }
            for index, row in self.data_df[[col_name]].iterrows():
                value = row.values[0]
                y_string = self.y_format.format(value)
                entry = {
                    "y": value,
                    "yString": y_string,
                    "name": index
                }
                item["data"].append(entry)

            series.append(item)

        self.output[key][series_key] = series

    def add_selected_templated(self, key="selectedTemplate"):
        self.output[key] = self.defaults[key]

    def write_to_file(self, json_indent=2):
        self.output_directory.mkdir(exist_ok=True)
        if self.output_filename is None:
            if self.input_file_name is None:
                default_file_name = Path("_".join(["highchart", self.chart_type, "plot"]) + ".json")
            else:
                file_stem = Path(self.input_file_name).stem
                default_file_name = Path(file_stem).with_suffix(".json")

            outfile = self.output_directory / default_file_name
        else:
            outfile = self.output_directory / Path(self.output_filename).with_suffix(".json")
        _logger.info(f"Writing to {outfile}")
        with open(outfile.as_posix(), "w") as stream:
            stream.write(json.dumps(self.output, indent=json_indent, ensure_ascii=False))
