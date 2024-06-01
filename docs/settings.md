
`Helix-py-api` will work fine without any additonal configuration. If you need or wish to change some of the default behavior, simply set the values in the API settings file [helixapi/utils/settings.yaml](helixapi/utils/settings.yaml).

```yaml
log_level: DEBUG
midi:
  targets:
    - "Line 6 Helix 9"
standards:
  setlist:
    casing: UPPERCASE
    replacements:
      " ":
        - "_"
      
  preset:
    casing: UPPERCASE
    replacements:
      " ":
        - "_"
      "Preset":
        - "New Preset"

  snapshot:
    casing: UPPERCASE
    replacements:
      " ":
        - "_"
      "Solo":
        - "lead"
```

For example, if you plan to use MIDI (i.e. have the API send commands to a Helix or other MIDI device), you will need to configure the "midi" section.