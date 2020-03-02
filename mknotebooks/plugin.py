import logging
import os
import pathlib
import re
from binascii import a2b_base64

import markdown
import mkdocs
import nbconvert
import nbformat
from mkdocs.config.base import Config as MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page, _RelativePathExtension
from mkdocs.structure.toc import get_toc
from nbconvert import HTMLExporter, MarkdownExporter
from traitlets.config import Config

from mknotebooks.extra_args_execute_preprocessor import ExtraArgsExecutePreprocessor

log = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))


class NotebookFile(mkdocs.structure.files.File):
    """
    Wraps a regular File object to make ipynb files appear as
    valid documentation files.
    """

    def __init__(self, file, use_directory_urls, site_dir, **kwargs):
        self.file = file
        self.dest_path = self._get_dest_path(use_directory_urls)
        self.abs_dest_path = os.path.normpath(os.path.join(site_dir, self.dest_path))
        self.url = self._get_url(use_directory_urls)

    def __getattr__(self, item):
        return self.file.__getattribute__(item)

    def is_documentation_page(self):
        return True


class Plugin(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ("execute", mkdocs.config.config_options.Type(bool, default=False)),
        ("allow_errors", mkdocs.config.config_options.Type(bool, default=False)),
        ("preamble", mkdocs.config.config_options.FilesystemObject()),
        ("timeout", mkdocs.config.config_options.Type(int)),
        ("write_markdown", mkdocs.config.config_options.Type(bool, default=False)),
        (
            "enable_default_jupyter_cell_styling",
            mkdocs.config.config_options.Type(bool, default=True),
        ),
        (
            "enable_default_pandas_dataframe_styling",
            mkdocs.config.config_options.Type(bool, default=True),
        ),
    )

    def on_config(self, config: MkDocsConfig):
        exporter_config = Config()
        if self.config["execute"]:
            default_preprocessors = MarkdownExporter.default_preprocessors.default_args[
                0
            ]
            try:
                default_preprocessors[
                    default_preprocessors.index(
                        "nbconvert.preprocessors.ExecutePreprocessor"
                    )
                ] = ExtraArgsExecutePreprocessor
            except ValueError:
                pass
            exporter_config.default_preprocessors = default_preprocessors
            exporter_config.ExecutePreprocessor.timeout = self.config["timeout"]
            exporter_config.ExecutePreprocessor.allow_errors = self.config[
                "allow_errors"
            ]
            exporter_config.ExtraArgsExecutePreprocessor.enabled = True
            exporter_config.ExtractOutputPreprocessor.enabled = True
            preamble = [os.path.join(here, "pandas_output_formatter.py")]

            exporter_config.file_extension = ".md"
            if self.config["preamble"]:
                preamble.append(self.config["preamble"])
            exporter_config.ExtraArgsExecutePreprocessor.extra_arguments = [
                f"--InteractiveShellApp.exec_files={preamble}",
            ]

        template_file = os.path.join(here, "templates", "custom_markdown.tpl")
        built_in_templates = os.path.join(
            os.path.dirname(nbconvert.__file__), "templates"
        )
        exporter_config.NbConvertBase.display_data_priority = [
            "application/vnd.jupyter.widget-state+json",
            "application/vnd.jupyter.widget-view+json",
            "application/javascript",
            "text/markdown",
            "text/html",
            "image/svg+xml",
            "text/latex",
            "image/png",
            "image/jpeg",
            "text/plain",
        ]
        exporter = HTMLExporter(
            config=exporter_config,
            template_file=template_file,
            template_path=[
                os.path.join(here, "templates"),
                built_in_templates,
                os.path.join(built_in_templates, "html"),
                os.path.join(built_in_templates, "skeleton"),
            ],
        )

        config["notebook_exporter"] = exporter
        config["extra_css"].append(os.path.join("css", "ansi-colours.css"))
        if self.config["enable_default_jupyter_cell_styling"]:
            config["extra_css"].append(os.path.join("css", "jupyter-cells.css"))
        if self.config["enable_default_pandas_dataframe_styling"]:
            config["extra_css"].append(os.path.join("css", "pandas-dataframe.css"))
        return config

    def on_files(self, files, config):
        templates_dir = os.path.join(here, "templates")
        css_dest_dir = os.path.join(config["site_dir"], "css")
        ansi_colours_css = File(
            path="ansi-colours.css",
            src_dir=templates_dir,
            dest_dir=css_dest_dir,
            use_directory_urls=False,
        )
        pandas_dataframe_css = File(
            path="pandas-dataframe.css",
            src_dir=templates_dir,
            dest_dir=css_dest_dir,
            use_directory_urls=False,
        )
        jupyter_cells_css = File(
            path="jupyter-cells.css",
            src_dir=templates_dir,
            dest_dir=css_dest_dir,
            use_directory_urls=False,
        )
        files = Files(
            [
                NotebookFile(f, **config)
                if str(f.abs_src_path).endswith("ipynb")
                else f
                for f in files
            ]
            + [ansi_colours_css, pandas_dataframe_css, jupyter_cells_css]
        )
        return files

    def on_page_read_source(self, page, config):
        if str(page.file.abs_src_path).endswith("ipynb"):
            with open(page.file.abs_src_path) as nbin:
                nb = nbformat.read(nbin, 4)

            exporter = config["notebook_exporter"]
            # Extract attachments, because mkdocs' markdown renderer doesn't cope with them
            for cell in nb["cells"]:
                attachments = cell.get("attachments", {})
                for attachment_name, attachment in attachments.items():
                    pathlib.Path(page.file.abs_dest_path).parent.mkdir(
                        parents=True, exist_ok=True
                    )
                    with open(
                        pathlib.Path(page.file.abs_dest_path).parent / attachment_name,
                        "wb",
                    ) as fout:
                        for mimetype, data in attachment.items():
                            fout.write(a2b_base64(data))
            body, resources = exporter.from_notebook_node(nb)

            # nbconvert uses the anchor-link class, convert it to the mkdocs convention
            body = body.replace('class="anchor-link"', 'class="headerlink"')
            body = re.compile("\(attachment:([a-z_\-A-Z0-9]+\.(png|jpg|svg))\)").sub(
                r"(\1)", body
            )

            if self.config["write_markdown"]:
                pathlib.Path(page.file.abs_dest_path).parent.mkdir(
                    parents=True, exist_ok=True
                )
                with open(
                    pathlib.Path(page.file.abs_src_path).with_suffix(".md.tmp"), "w"
                ) as fout:
                    fout.write(body)
            if hasattr(resources["outputs"], "items"):
                for fname, content in resources["outputs"].items():
                    pathlib.Path(page.file.abs_dest_path).parent.mkdir(
                        parents=True, exist_ok=True
                    )
                    with open(
                        pathlib.Path(page.file.abs_dest_path).parent / fname, "wb"
                    ) as fout:
                        fout.write(content)
            return body
        return None

    def on_page_content(
        self, html: str, page: Page, config: MkDocsConfig, files: Files
    ):
        if str(page.file.abs_src_path).endswith("ipynb") and not (
            "markdown.extensions.md_in_html" in config["markdown_extensions"]
            or "markdown.extensions.extra" in config["markdown_extensions"]
        ):
            log.debug(f"Re-rendering page with markdown in divs: {page}")
            extensions = [
                _RelativePathExtension(page.file, files),
                "markdown.extensions.md_in_html",
            ] + config["markdown_extensions"]
            md = markdown.Markdown(
                extensions=extensions, extension_configs=config["mdx_configs"] or {}
            )
            html = md.convert(page.markdown)
            page.toc = get_toc(getattr(md, "toc_tokens", []))

        return html
