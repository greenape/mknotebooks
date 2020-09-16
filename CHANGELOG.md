# Changelog
All notable changes to mknotebooks will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- You can now remove cells using both nbconvert's built in options, but also the [cell tag and regex remove preprocessors](https://nbconvert.readthedocs.io/en/latest/removing_cells.html). [#36](https://github.com/greenape/mknotebooks/issues/36)
- Now works with nbconvert 6.x [#46](https://github.com/greenape/mknotebooks/issues/46)

### Changed


### Fixed


### Removed
- No longer supports nbconvert < 6.x [#46](https://github.com/greenape/mknotebooks/issues/46)

## [0.5.0]
### Added
- You can now add a per-notebook Binder link [#44](https://github.com/greenape/mknotebooks/pull/44) (thanks to [@ericmjl](https://github.com/ericmjl))

### Changed
- Readme now nicer! [#40](https://github.com/greenape/mknotebooks/pull/40) (thanks to [@timvink](https://github.com/timvink))

## [0.4.1]
### Fixed
- When using `enable_default_pandas_dataframe_styling: true` with mkdocs-material dark mode now renders correctly [#35](https://github.com/greenape/mknotebooks/issues/35) (thanks to [@timvink](https://github.com/timvink))

## [0.4.0]
### Changed
- stdout, stderr and text/plain outputs are now wrapped in a `<code></code>` (thanks to [@lgeiger](https://github.com/lgeiger))

## [0.3.6]
### Fixed
- Fixed errors when running with older nbconvert releases by requiring >=  5.6.1 (thanks to [@theolvs](https://github.com/theolvs))

## [0.3.5]
### Fixed
- Fixed duped display of widgets when there's more than one

## [0.3.4]
### Fixed
- Widgets should now display properly

## [0.3.3]
### Fixed
- Images in markdown cells are now extract as well
- Re-refixed pandas tables (hopefully)

## [0.3.2]
### Fixed
- Fixed pandas tables not being parsed

## [0.3.1]
### Fixed
- Fixed the toc extension not adding a table of contents

## [0.3.0]
### Added

- Added default CSS stylesheets for nicer styling of notebook input/output cells and pandas dataframes,
  as well as two options (`enable_default_jupyter_cell_styling`, `enable_default_pandas_dataframe_styling`)
  to enable or disable them [#13](https://github.com/greenape/mknotebooks/pull/13)  (thanks to [@maxalbert](https://github.com/maxalbert))

## [0.2.0]

### Fixed
- Compatibility with mkdocs 1.1. [#14](https://github.com/greenape/mknotebooks/pull/14) (thanks to [@lgeiger](https://github.com/lgeiger))
- Set the correct class on headerlink. [#16](https://github.com/greenape/mknotebooks/pull/16) (thanks to [@lgeiger](https://github.com/lgeiger))

[Unreleased]: https://github.com/greenape/mktheapidocs/compare/0.5.0...master
[0.5.0]: https://github.com/greenape/mktheapidocs/compare/0.4.1...0.5.0
[0.4.1]: https://github.com/greenape/mktheapidocs/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/greenape/mktheapidocs/compare/0.3.6...0.4.0
[0.3.6]: https://github.com/greenape/mktheapidocs/compare/0.3.5...0.3.6
[0.3.5]: https://github.com/greenape/mktheapidocs/compare/0.3.4...0.3.5
[0.3.4]: https://github.com/greenape/mktheapidocs/compare/0.3.3...0.3.4
[0.3.3]: https://github.com/greenape/mktheapidocs/compare/0.3.2...0.3.3
[0.3.2]: https://github.com/greenape/mktheapidocs/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/greenape/mktheapidocs/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/greenape/mktheapidocs/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/greenape/mktheapidocs/compare/0.1.16...0.2.0
