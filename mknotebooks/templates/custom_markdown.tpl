{#
   This template extends the standard nbconvert markdown template in
   such a way that input and output cells are wrapped in custom <div>
   tags which are marked with the CSS classes "jupyterInputCell" and
   "jupyterOutputCell". This allows us to use our own custom styling
   for input and output cells. Note that this works because it is
   valid to use raw HTML in markdown.

   When converted to markdown, input cells are formatted using code
   blocks that use triple backticks, and these can be wrapped directly
   in a <div>.

   By contrast, output cells are by default formatted using simply
   an indented block (rather than triple backticks). Such an indented
   block cannot directly be wrapped in a <div> without losing the
   formatting. Therefore we first apply a custom Jinja filter to
   each line of the output cell which removes the indentation, and
   then surround the result with triple backticks and finally wrap
   this in the custom <div>.
#}

{% extends "markdown.tpl" %}

{% block input_group %}
<div class='jupyterInputCell'>
{{ super() }}
</div>
{% endblock input_group %}

{% block output_group %}
<div class='jupyterOutputCell'>
```
{{ super().split('\n') | map('remove_leading_indentation') | join('\n') }}
```
</div>
{% endblock output_group %}
