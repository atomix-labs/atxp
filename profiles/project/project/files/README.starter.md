<!-- >>> devset: project >>> -->
<!-- <<< devset: project <<< -->
{%- if "vhs" in devset.profiles %}

<!-- dprint-ignore-start -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/src/media/demo-dark.gif">
    <img alt="What the demo shows, in one sentence" src="docs/src/media/demo-light.gif" width="720">
  </picture>
</p>

<!-- dprint-ignore-end -->
{%- endif %}

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
