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
                 data: pd.DataFrame,
                 filename: str = None,
                 output_directory: str = None,
                 chart_type: str = None,
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
        self.filename = filename
        if output_directory is None:
            self.output_directory = Path(".")
        else:
            self.output_directory = Path(output_directory)

        self.chart_type = chart_type

        self.output = {
            "template": {},
            "options": {},
            "selectedTemplate": {}
        }

        self.add_chart(chart_type=chart_type,
                       inverted=chart_inverted,
                       spacing_left=chart_spacing_left,
                       margin_right=chart_margin_right,
                       margin_bottom=chart_margin_bottom)
        self.add_plot_options()

        title_style = Style(font_family=chart_title_font_family,
                            font_size=chart_title_font_size,
                            color=chart_title_color)
        self.add_title(text_key="title", text=chart_title, style=title_style)
        self.add_title(text_key="subtitle", text=chart_subtitle)

        self.add_both_axis()
        self.add_plot_lines()
        self.add_legend()
        self.add_tooltip()
        self.add_credits()

        chart_style = Style(font_family="\"Akko W01 Regular\", \"Calibri Light\", sans-serif",
                            font_size="12px",
                            color="#000")
        self.add_chart(key="options",
                       style=chart_style,
                       height=450)

        self.write_to_file()

    def add_plot_lines(self, key="template", number_of_plot_lines=1):

        plot_lines = list()
        for cnt in range(number_of_plot_lines):
            plot_lines.append(PlotLine().serialize())

        self.output[key]["plotLines"] = plot_lines

    def add_both_axis(self, key="template"):
        """ Beide assen worden toegevoegd. Moet waarschijn plot type afhankelijk worden """

        # eerst de x as
        categories = Categories(series=self.data_df.index)

        style = Style(color="#000000")
        title = Text(align="high", style=style, use_html=True, rotation=0)
        label_style = Style(font_size="11px", color="#000000")
        labels = Text(style=label_style)
        self.add_axes(key=key,
                      axis_key="xAxis",
                      title=title,
                      labels=labels,
                      categories=categories,
                      )

        # nu de y as
        title = Text(use_html=True)
        label_style = Style(font_size="11px", color="#000000")
        labels = Text(style=label_style, enabled=True, auto_rotation=False)
        self.add_axes(key=key,
                      axis_key="yAxis",
                      title=title,
                      labels=labels,
                      grid_line_color="#666666",
                      grid_line_width=0.25,
                      start_on_tick=True,
                      end_on_tick=True,
                      line_width=0,
                      tick_length=9,
                      reversed_stacks=False)

    def add_chart(self,
                  key="template",
                  set_defaults=False,
                  chart_type=None,
                  inverted=None,
                  spacing_left=None,
                  margin_right=None,
                  margin_bottom=None,
                  height=None,
                  style=None,
                  animation=None,
                  polar=None,
                  events=None,
                  ):

        if set_defaults:
            # zet nu de waarden die alleen voor bepaalde types gezet worden
            if self.chart_type == "line":
                if margin_bottom is None:
                    margin_bottom = 180
            elif self.chart_type == "bar":
                if margin_right is None:
                    margin_right = 45
                if spacing_left is None:
                    spacing_left = 54
                if inverted is not None:
                    inverted = False
            elif self.chart_type == "column":
                if inverted is not None:
                    inverted = False

        chart = Chart(chart_type=chart_type,
                      inverted=inverted,
                      spacing_left=spacing_left,
                      margin_right=margin_right,
                      margin_bottom=margin_bottom,
                      height=height,
                      style=style,
                      animation=animation,
                      polar=polar,
                      events=events
                      )
        self.output[key]["chart"] = chart.serialize()

    def add_plot_options(self, key="template"):
        plot_options = PlotOptions(chart_type=self.chart_type)
        self.output[key]["plotOptions"] = plot_options.serialize()

    def add_title(self, key="template", text_key=" title", text=None, style=None):

        text = Text(text=text, style=style)

        self.output[key][text_key] = text.serialize()

    def add_tooltip(self, key="template"):

        tooltip = ToolTip()
        self.output[key]["tooltip"] = tooltip.serialize()

    def add_credits(self, key="template"):

        plot_credits = Credits()
        self.output[key]["credits"] = plot_credits.serialize()

    def add_legend(self,
                   key="template",
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
                   use_html=True
                   ):

        item_style = Style(font_weight="normal",
                           color="#000000",
                           font_size="12px")
        item_hidden_style = Style(color="#757575")
        legend = Legend(align=align,
                        reversed_legend=reversed_legend,
                        vertical_align=vertical_align,
                        y_shift=y_shift,
                        padding=padding,
                        symbol_radius=symbol_radius,
                        symbol_height=symbol_height,
                        symbol_width=symbol_width,
                        square_symbol=square_symbol,
                        symbol_padding=symbol_padding,
                        item_distance=item_distance,
                        item_margin_bottom=item_margin_bottom,
                        use_html=use_html,
                        item_style=item_style,
                        item_hidden_style=item_hidden_style)
        self.output[key]["legend"] = legend.serialize()

    def add_axes(self,
                 key="template",
                 axis_key="xAxis",
                 title=None,
                 labels=None,
                 categories=None,
                 grid_line_color=None,
                 grid_line_width=None,
                 start_on_tick=False,
                 end_on_tick=False,
                 line_width=1,
                 tick_length=0,
                 reversed_stacks=None):

        axis = Axis(categories=categories,
                    title=title,
                    labels=labels,
                    grid_line_color=grid_line_color,
                    grid_line_width=grid_line_width,
                    start_on_tick=start_on_tick,
                    end_on_tick=end_on_tick,
                    line_width=line_width,
                    tick_length=tick_length,
                    reversed_stacks=reversed_stacks,
                    )
        self.output[key][axis_key] = axis.serialize()
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
            stream.write(json.dumps(self.output, indent=json_indent, ensure_ascii=False))
