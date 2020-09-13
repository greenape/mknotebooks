# mknotebooks

mknotebooks is a plugin for [MkDocs](https://mkdocs.org), which makes it more convenient to include [Jupyter](https://jupyter.org) notebooks in your project documentation.

## Install

`pip install mknotebooks`

## Usage

Simply include any notebooks you want to use in the docs source directory, and add mknotebooks to the plugin section of your `mkdocs.yml`.

You can optionally execute the notebooks, by setting `execute: true` in the config, and include a hidden preamble script, to be run before executing any cells using `preamble: "<path/to/your/script>"`.

Any static images, plots, etc. will be extracted from the notebook and placed alongside the output HTML.
