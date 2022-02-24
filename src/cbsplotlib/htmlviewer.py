import argparse
import logging
import sys
import webbrowser
from pathlib import Path
from typing import Union

from cbsplotlib import (HC_DEFAULTS_DIRECTORY, HC_HTML_VIEW_TEMPLATE)
from cbsplotlib import __version__

_logger = logging.getLogger(__name__)


class HtmlViewer:
    def __init__(self, filename: Union[str, Path],
                 output_html_file: Union[str, Path] = None,
                 output_directory: Union[str, Path] = None,
                 view_template: Union[str, Path] = None,
                 view_template_directory: Union[str, Path] = None,
                 show: bool = False
                 ):
        self.filename = Path(filename)

        if output_directory is None:
            self.output_directory = self.filename.parent
        else:
            self.output_directory = Path(output_directory)

        if output_html_file is None:
            out_file_base = self.filename.stem + self.filename.suffix
        else:
            out_file_base = Path(output_html_file)

        self.output_html_file = self.output_directory / out_file_base

        self.view_template = view_template
        self.view_template_directory = view_template_directory

        html_contents = self.make_html_template()

        _logger.info(f"Writing to {output_html_file}")
        with open(self.output_html_file, "w") as fp:
            fp.write(html_contents)

        if show:
            self.show()

    def make_html_template(self):
        if self.view_template_directory is not None:
            defaults_directory = self.view_template_directory
        else:
            defaults_directory = Path(__file__).parent / Path(HC_DEFAULTS_DIRECTORY)

        if self.view_template is not None:
            html_view_template = self.view_template
        else:
            html_view_template = HC_HTML_VIEW_TEMPLATE

        html_template_file = defaults_directory / html_view_template

        with open(html_template_file) as fp:
            html_template = fp.read()

        _logger.info(f"Reading  {self.filename}")
        with open(self.filename) as stream:
            highchart_script = stream.read()

        new_html = html_template.replace("HIGHCHARTS_SCRIPT", highchart_script)

        return new_html

    def show(self):

        url = "file://" + self.output_html_file

        webbrowser.open(url)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Tool om latex tabulars in xls files om te zetten")
    parser.add_argument(
        "--version",
        action="version",
        version="tabular2xls {ver}".format(ver=__version__),
    )
    parser.add_argument("filename", help="Tabular file name", metavar="FILENAME")
    parser.add_argument("--output_filename",
                        help="Naam van de xls output file. Moet extensie .xlsx "
                             "hebben", metavar="OUTPUT_FILENAME")
    parser.add_argument("--output_directory",
                        help="Naam van de output directory. Als niet gegeven wordt het"
                             "door de output filenaam bepaald", metavar="OUTPUT_DIRECTORY")
    parser.add_argument("--search_and_replace",
                        help="Search en Replace patterns als je nog string wilt veranderen."
                             "Default worden cdots en ast naar resp . en * vervangen",
                        nargs="*", action="append")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "--multi_index",
        help="Forceer een multiindex dataframe",
        action="store_true",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formated message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    filename = Path(args.filename)

    if args.output_filename is None:
        html_outfile = filename.with_suffix(".xlsx")
    else:
        html_outfile = Path(args.output_filename)

    if args.output_directory is not None:
        output_directory = Path(args.output_directory)
        html_out_base = html_outfile.stem + html_outfile.suffix
        html_outfile = output_directory / Path(html_out_base)

    if ".html" not in html_outfile.suffix:
        raise ValueError("Output filename does not have .html extension. Please correct")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
