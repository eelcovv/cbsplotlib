import codecs
import functools
import json
import logging
from pathlib import Path

import pandas as pd

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
                 defaults_file_name: str = None,
                 defaults_out_file: str = None,
                 chart_type: str = None,
                 csv_separator: str = ";",
                 decimal: str = ",",
                 index_col: int = 0,
                 y_format: str = None,
                 start: bool = False,
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

        if output_directory is None:
            self.output_directory = Path(".")
        else:
            self.output_directory = Path(output_directory)

        self.output_file_name = output_file_name

        self.modification_file_name = defaults_out_file

        # initieer de output dictionary
        self.output = {
            "template": {},
            "options": {},
            "selectedTemplate": {}
        }

        # hier worden alle defaults in de self.defaults attribute geladen
        self.defaults = self.read_the_defaults(chart_type=chart_type,
                                               defaults_directory=defaults_directory,
                                               defaults_file_name=defaults_file_name)

        if defaults_out_file is not None:
            # als we een default output file geven dan schrijven we alleen de huidige template naar
            # deze file
            self.write_to_file(output=self.defaults, output_file_name=defaults_out_file)
            _logger.info(
            """
            We hebben de defaults template geschreven om het *default_out_file* als argument gegeven
            was. Als je het plaatje met deze template wil maken, geef dan *defaults_out_file* mee 
            met het *defaults_file_name* argument. Script stop nu hier.
                """
            )
            return

        # get the data here, if take from the argument
        if data is None:
            _logger.info(f"Reading data from {input_file_name}")
            self.data_df = self.get_data(input_file_name, index_col=index_col,
                                         csv_separator=csv_separator, decimal=decimal)
        else:
            _logger.debug(f"Using dataframe")
            self.data_df = data

        # get the categories from the data
        self.categories = self.get_categories()

        _logger.debug(f"categories: {self.categories}")

        if start:
            # als de start optie meegeven is dan gaan we de highcharts file bouwen
            self.make_highcharts()
            _logger.info("Done with making highcharts")
        else:
            _logger.info("The data was successfully. To create the highcharts, call the "
                         "*make_highcharts()* method or pass the start=True argument")

    def make_highcharts(self):

        # now add all the items of the highcarts
        self.add_chart()
        self.add_plot_options()

        self.add_title(text_key="title")
        self.add_title(text_key="subtitle")

        self.add_axis(axis_key="xAxis", categories=self.categories)
        self.add_axis(axis_key="yAxis")
        self.add_legend()
        self.add_tooltip()
        self.add_credits()

        self.add_options()
        self.add_csv_data()
        self.add_series()
        self.add_axis(key="options", axis_key="xAxis", categories=self.categories)
        self.add_axis(key="options", axis_key="yAxis")

        self.add_selected_templated()

        # finally write the result to file
        self.write_to_file(output=self.output,
                           output_directory=self.output_directory,
                           output_file_name=self.output_file_name,
                           input_file_name=self.input_file_name,
                           chart_type=self.chart_type)

    @staticmethod
    def get_data(input_file_name, index_col=0, csv_separator=";", decimal=","):
        if input_file_name is None:
            raise TypeError("Both input data argument *data_df* and input filename "
                            "*input_file_name* are None. Please provide at least one.")
        else:
            _logger.debug(f"Reading {input_file_name}")
            data_df = pd.read_csv(input_file_name,
                                  sep=csv_separator,
                                  index_col=index_col,
                                  decimal=decimal)
        return data_df

    def get_categories(self):
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

        return categories

    @staticmethod
    def read_the_defaults(chart_type: str = None,
                          defaults_directory: str = None,
                          defaults_file_name: str = None,
                          cbs_hc_defaults: str = "cbs_hc_defaults"):
        """
        Lees de settings uit een default template json en overschrijf met de instellingen uit een modification json

        Parameters
        ----------
        chart_type: str of None
            Type plot die we maken (bar, column, line). De default template wordt gebaseerd hierop gemaakt
        defaults_directory: str of None
            Locatie waar de default template staat. Als niet gegeven en default file naam is niet mee gegeven, dan
            is dit <PACKAGELOCATIE>/Path(cbs_hc_defaults)
        defaults_file_name: str of None
            Naam van de defaults input file. Als niet gegeven wordt deze gebaseerd op *chart_type*
        cbs_hc_defaults: str
            Naam van de default directory in de package src.
        """

        if defaults_directory is None:
            if defaults_file_name is None:
                # er is geen default filenaam meegegeven. Ga ervan uit dat we de default uit de package folder halen
                defaults_directory = Path(__file__).parent / Path(cbs_hc_defaults)
        else:
            defaults_directory = Path(defaults_directory)

        if defaults_file_name is None:
            # alde default filename None is dan is default directory sowieso gezet
            defaults_file_name = defaults_directory / Path(chart_type + ".json")
        else:
            # default file naam was door de gebruiker meegegeven. Als ook de directory meegegeven was dan combineren
            # we de naam met de directory, anders nemen we direct de filenaam
            if defaults_directory is None:
                defaults_file_name = Path(defaults_file_name)
            else:
                defaults_file_name = defaults_directory / Path(defaults_file_name)

        _logger.info(f"Reading template {defaults_file_name}")
        with open(defaults_file_name, "r") as stream:
            defaults = json.load(stream)

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

    @staticmethod
    def write_to_file(output,
                      json_indent=2,
                      output_directory: Path = None,
                      output_file_name: str = None,
                      input_file_name: str = None,
                      chart_type=None):
        """
        Write the dictionary to an json output file
        Parameters
        ----------
        output: dict
            The settings dictionary to write
        json_indent: int
            Number of indenting spaces. If None is give, a compact json is written
        output_directory: Path of None
            Output directory
        output_file_name: str of None
            Naam van de output file
        input_file_name: str of None
            Naam van de input data file. Als we geen output filenaam geven zal de output file hierop gebaseerd worden.
        chart_type: str
            Type plot (bar, column, line). Als gegeven wordt dit in de filenaam verwerkt.

        """
        if output_directory is not None:
            output_directory.mkdir(exist_ok=True)
        if output_file_name is None:
            if input_file_name is None:
                if chart_type is None:
                    chart_label = ""
                else:
                    chart_label = chart_type
                default_file_name = Path("_".join(["highchart", chart_label, "plot"]) + ".json")
            else:
                file_stem = Path(input_file_name).stem
                default_file_name = Path(file_stem).with_suffix(".json")

            outfile = output_directory / default_file_name
        else:
            if output_directory is None:
                outfile = Path(output_file_name).with_suffix(".json")
            else:
                outfile = output_directory / Path(output_file_name).with_suffix(".json")
        _logger.info(f"Writing to {outfile}")
        with codecs.open(outfile.as_posix(), "w", encoding='utf-8') as stream:
            stream.write(json.dumps(output, indent=json_indent, ensure_ascii=False))
