{%- extends 'base/display_priority.j2' -%}
{% from 'base/celltags.j2' import celltags %}

{% block header %}
{{ super() }}
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
<script>
(function() {
  function addWidgetsRenderer() {
    var requireJsScript = document.createElement('script');
    requireJsScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js';

    var mimeElement = document.querySelector('script[type="application/vnd.jupyter.widget-view+json"]');
    var jupyterWidgetsScript = document.createElement('script');
    var widgetRendererSrc = 'https://unpkg.com/@jupyter-widgets/html-manager@*/dist/embed-amd.js';
    var widgetState;

    // Fallback for older version:
    try {
      widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);

      if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {
        widgetRendererSrc = '{{ resources.ipywidgets_base_url }}jupyter-js-widgets@*/dist/embed.js';
      }
    } catch(e) {}

    jupyterWidgetsScript.src = widgetRendererSrc;

    document.body.appendChild(requireJsScript);
    document.body.appendChild(jupyterWidgetsScript);
  }

  document.addEventListener('DOMContentLoaded', addWidgetsRenderer);
}());
</script>
{% endblock header %}


{% block codecell %}
<div class="cell border-box-sizing code_cell rendered{{ celltags(cell) }}" markdown="1">
{{ super() }}
</div>
{%- endblock codecell %}

{% block input_group -%}
<div class="input">
{{ super() }}
</div>
{% endblock input_group %}

{% block output_group %}
<div class="output_wrapper" markdown="1">
<div class="output" markdown="1">
{{ super() }}
</div>
</div>
{% endblock output_group %}

{#
  output_prompt doesn't do anything in HTML,
  because there is a prompt div in each output area (see output block)
#}
{% block output_prompt %}{% endblock output_prompt %}

{% block input %}
```
{%- if 'magics_language' in cell.metadata  -%}
    {{ cell.metadata.magics_language}}
{%- elif 'name' in nb.metadata.get('language_info', {}) -%}
    {{ nb.metadata.language_info.name }}
{%- endif %}
{{ cell.source}}
```
{% endblock input %}



{% block output %}
<div class="output_area" markdown="1">
{{ super() }}
</div>
{% endblock output %}

{% block markdowncell scoped %}
<div class="cell border-box-sizing text_cell rendered{{ celltags(cell) }}" markdown="1">
<div class="inner_cell" markdown="1">
<div class="text_cell_render border-box-sizing rendered_html" markdown="1">
{{ cell.source  }}
</div>
</div>
</div>
{%- endblock markdowncell %}

{% block unknowncell scoped %}
unknown type  {{ cell.type }}
{% endblock unknowncell %}

{% block execute_result -%}
{%- set extra_class="output_execute_result" -%}
{% block data_priority scoped %}
{{ super() }}
{% endblock data_priority %}
{%- set extra_class="" -%}
{%- endblock execute_result %}

{% block stream_stdout -%}
<div class="output_subarea output_stream output_stdout output_text">
<pre>
<code>
{{- output.text | ansi2html -}}
</code>
</pre>
</div>
{%- endblock stream_stdout %}

{% block stream_stderr -%}
<div class="output_subarea output_stream output_stderr output_text">
<pre>
<code>
{{- output.text | ansi2html -}}
</code>
</pre>
</div>
{%- endblock stream_stderr %}

{% block data_svg scoped -%}
<div class="output_svg output_subarea {{ extra_class }}">
{%- if output.svg_filename %}
<img src="{{ output.svg_filename | posix_path }}">
{%- else %}
{{ output.data['image/svg+xml'] }}
{%- endif %}
</div>
{%- endblock data_svg %}

{% block data_html scoped -%}
<div class="output_html rendered_html output_subarea {{ extra_class }}">
{{ output.data['text/html'] }}
</div>
{%- endblock data_html %}

{% block data_markdown scoped -%}
{{ output.data['text/markdown'] | markdown2html }}
{%- endblock data_markdown %}

{% block data_png scoped %}
<div class="output_png output_subarea {{ extra_class }}">
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/png'] | posix_path }}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/png') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/png') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/png') %}
class="unconfined"
{%- endif %}
{%- set alttext=(output | get_metadata('alt', 'image/png')) or (cell | get_metadata('alt')) -%}
{%- if alttext is not none %}
alt="{{ alttext }}"
{%- endif %}
>
</div>
{%- endblock data_png %}

{% block data_jpg scoped %}
<div class="output_jpeg output_subarea {{ extra_class }}">
{%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/jpeg'] | posix_path }}"
{%- else %}
<img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/jpeg') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/jpeg') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/jpeg') %}
class="unconfined"
{%- endif %}
{%- set alttext=(output | get_metadata('alt', 'image/jpeg')) or (cell | get_metadata('alt')) -%}
{%- if alttext is not none %}
alt="{{ alttext }}"
{%- endif %}
>
</div>
{%- endblock data_jpg %}

{% block data_latex scoped %}
<div class="output_latex output_subarea {{ extra_class }}">
{{ output.data['text/latex'] }}
</div>
{%- endblock data_latex %}

{% block error -%}
<div class="output_subarea output_text output_error">
<pre>
{{- super() -}}
</pre>
</div>
{%- endblock error %}

{%- block traceback_line %}
{{ line | ansi2html }}
{%- endblock traceback_line %}

{%- block data_text scoped %}
<div class="output_text output_subarea {{ extra_class }}">
<pre>
<code>
{{- output.data['text/plain'] | ansi2html -}}
</code>
</pre>
</div>
{%- endblock -%}

{%- block data_javascript scoped %}
{% set div_id = uuid4() %}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_javascript {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
{{ output.data['application/javascript'] }}
</script>
</div>
{%- endblock -%}

{%- block data_widget_state scoped %}
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_widget_state {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
</script>
<script type="{{ datatype }}">
{{ output.data[datatype] | json_dumps }}
</script>
</div>
{%- endblock data_widget_state -%}

{%- block data_widget_view scoped %}
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_widget_view {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
</script>
<script type="{{ datatype }}">
{{ output.data[datatype] | json_dumps }}
</script>
</div>
{%- endblock data_widget_view -%}

{%- block footer %}
{% set mimetype = 'application/vnd.jupyter.widget-state+json'%}
{% if mimetype in nb.metadata.get("widgets",{})%}
<script type="{{ mimetype }}">
{{ nb.metadata.widgets[mimetype] | json_dumps }}
</script>
{% endif %}
{{ super() }}
{%- endblock footer-%}
