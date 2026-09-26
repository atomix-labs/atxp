- [ ] The description says what changes, and why
{%- if "git-commits" in devset.profiles %}
- [ ] The title is a Conventional Commit: `type(scope): subject`
{%- endif %}
{%- if "just" in devset.profiles %}
- [ ] `just check` passes
{%- endif %}
{%- for layer in devset.layers if layer.profile == "project" and "breaking-changes" in layer.features %}
- [ ] A breaking change has its entry in `BREAKING-CHANGES.md`
{%- endfor %}
