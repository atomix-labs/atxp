# `{{ name or devset.target }}`

<!-- >>> devset: project >>> -->
<!-- <<< devset: project <<< -->

One paragraph: what the project is, and why someone would use it.

## Quick Start

The fewest steps from nothing to the project at work.

## Documentation

Where to read more.
{%- if "contributing" in devset.features %}

## Contributing

Issues and pull requests are welcome: read [CONTRIBUTING.md](CONTRIBUTING.md)
first.
{%- endif %}
{%- if "license" in devset.features %}

## License
{% if license == "MIT OR Apache-2.0" %}
Either [the MIT License](LICENSE-MIT) or
[the Apache License, Version 2.0](LICENSE-APACHE), at your option.
{%- elif license == "MIT" %}
[The MIT License](LICENSE).
{%- elif license == "Apache-2.0" %}
[The Apache License, Version 2.0](LICENSE).
{%- else %}
`{{ license }}`.
{%- endif %}
{%- endif %}
