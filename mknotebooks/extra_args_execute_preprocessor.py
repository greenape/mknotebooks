from nbconvert.preprocessors import ExecutePreprocessor
from traitlets import List, Unicode


class ExtraArgsExecutePreprocessor(ExecutePreprocessor):
    extra_arguments = List(Unicode()).tag(config=True)
