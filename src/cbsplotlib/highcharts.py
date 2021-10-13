import codecs
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
        else:
            _logger.debug(f"Using dataframe")

        self.add_chart()
        self.add_plot_options()

        self.add_title(text_key="title")
        self.add_title(text_key="subtitle")

        if self.data_df.index.nlevels == 1:
            categories = self.data_df.index.to_list()
        elif self.data_df.index.nlevels == 2:
            categories = list()
            for first_level_key, df in self.data_df.groupby(level=0):
                group_categories = {"name": str(first_level_key),
                                    "categories": df.index.get_level_values(1).to_list()}
                categories.append(group_categories)
        else:
            raise TypeError("Multilevel with more than 2 levels not implemented")

        self.add_axis(axis_key="xAxis", categories=categories)
        self.add_axis(axis_key="yAxis")
        self.add_legend()
        self.add_tooltip()
        self.add_credits()

        self.add_options()
        self.add_csv_data()
        self.add_series()
        self.add_axis(key="options", axis_key="xAxis", categories=categories)
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
            if modifications_filename.exists():
                _logger.info(f"Reading modification settings from {modifications_filename} ")
                with open(modifications_filename, "r") as stream:
                    modifications = json.load(stream)
                defaults = modify_the_defaults(defaults, modifications)
            else:
                _logger.info(f"Creating new modification settings file {modifications_filename}")
                with codecs.open(modifications_filename.as_posix(), "w", encoding='utf-8') as fp:
                    fp.write(json.dumps(defaults, indent=2, ensure_ascii=False))

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
                }
                if isinstance(index, str):
                    entry["name"] = index
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
        with codecs.open(outfile.as_posix(), "w", encoding='utf-8') as stream:
            stream.write(json.dumps(self.output, indent=json_indent, ensure_ascii=False))
