import mkdocs, pathlib, os
from mkdocs.structure.files import Files
from traitlets.config import Config
from nbconvert import MarkdownExporter
import nbformat


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
        ("preamble", mkdocs.config.config_options.FilesystemObject()),
        ("timeout", mkdocs.config.config_options.Type(int)),
    )

    def on_config(self, config):
        c = Config()
        if self.config["execute"]:
            if self.config["preamble"]:
                default_preprocessors = MarkdownExporter.default_preprocessors.default_args[
                    0
                ]
                default_preprocessors.insert(
                    default_preprocessors.index(
                        "nbconvert.preprocessors.ExecutePreprocessor"
                    ),
                    "nbconvert_utils.ExecuteWithPreamble",
                )
                c.default_preprocessors = default_preprocessors
                c.ExecutePreprocessor.timeout = self.config["timeout"]
                c.ExecuteWithPreamble.enabled = True
                c.ExecuteWithPreamble.preamble_scripts = [self.config["preamble"]]
            else:
                c.Executor.enabled = True
        config["notebook_exporter"] = MarkdownExporter(config=c)
        return config

    def on_files(self, files, config):
        files = Files(
            [
                NotebookFile(f, **config)
                if str(f.abs_src_path).endswith("ipynb")
                else f
                for f in files
            ]
        )
        return files

    def on_page_read_source(self, _, page, config):
        print(page)
        if str(page.file.abs_src_path).endswith("ipynb"):
            with open(page.file.abs_src_path) as nbin:
                nb = nbformat.read(nbin, 4)

            exporter = config["notebook_exporter"]
            body, resources = exporter.from_notebook_node(nb)

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
