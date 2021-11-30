![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mknotebooks)
![PyPI](https://img.shields.io/pypi/v/mknotebooks)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mknotebooks)
![GitHub contributors](https://img.shields.io/github/contributors/timvink/mknotebooks)
![PyPI - License](https://img.shields.io/pypi/l/mknotebooks)

# mknotebooks

mknotebooks is a plugin for [MkDocs](https://mkdocs.org) enabling you to include [Jupyter](https://jupyter.org) notebooks directly in your project documentation.

## Install

`pip3 install mknotebooks`

## Usage

- Add `mknotebooks` to the plugin section of your `mkdocs.yml`
- Include any notebooks (`.ipynb` files) you want to use in the `docs/` directory just as you would `.md` files.

Example:

```yaml
# mkdocs.yml
nav:
  - your_notebook.ipynb

plugins:
  - mknotebooks
```

Any static images, plots, etc. will be extracted from the notebook and placed alongside the output HTML.

### Options

You can optionally execute the notebooks, by setting `execute: true` in the config. You can include a hidden preamble script, to be run before executing any cells using `preamble: "<path/to/your/script>"`. The default cell execution timeout can be overridden by setting `timeout: <timeout>`, where `<timeout>` is an integer number of seconds.

By default, execution will be aborted if any of the cells throws an error, but you can set `allow_errors: true` to continue execution and include the error message in the cell output.

Example:


```yaml
# mkdocs.yml
plugins:
  - mknotebooks
      execute: false
      timeout: 100
      preamble:  "<path/to/your/script>"
      allow_errors: false
```

### Styling

Mknotebooks applies default styling to improve the appearance of notebook input/output cells and pandas dataframes. If these interfere with any other CSS stylesheets that you're using, you can disable these via the following options.

```
# mkdocs.yml
- mknotebooks:
   enable_default_jupyter_cell_styling: false
   enable_default_pandas_dataframe_styling: false
```

### Syntax highlighting

In order to enable syntax highlighting for code blocks, `pygments` has to be installed and `codehilite` extension has to be enabled in `mkdocs.yml`.

1. Install pygments:

```
pip install Pygments
```

2. Enable `codehilite` extension in `mkdocs.yml`:

```
# mkdocs.yml
markdown_extensions:
    - codehilite
```

### Binder

You can also choose to have mknotebooks insert a [Binder](https://mybinder.org) link into each notebook.

``` mkdocs.yml
- mknotebooks:
      binder: true
      binder_service_name: "gh"
      binder_branch: "master"
      binder_ui: "lab"
```

If you are using GitLab, you will need to set `binder_service_name` to `"gl"`.

## Examples

See the [examples folder](examples/) for examples on the [use of a preamble](examples/execute_with_preamble) and [using Binder](examples/binder_logo). Try them out by running `pipenv install && pipenv run mkdocs serve`.

## Inspecting generated markdown

You can also export the generated markdown by setting `write_markdown: true` in your `mkdocs.yml`. This will write the generated markdown to a `.md.tmp` file alongside the original notebook.
