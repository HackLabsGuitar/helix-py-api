<p align="center"><font size="6">Helix Py API</font></p>
<p align="center">Unofficial API for managing Line 6 Helix files and related devices</p>

<p align="center">
<a href="https://github.com/HackLabsGuitar/helix-py-api"><img alt="Source Code" src="https://img.shields.io/badge/ource-code-blue?style=flat-square&logoColor=fff&color=0e7acf"/></a>
<a href="https://github.com/HackLabsGuitar/helix-py-api/issues"><img alt="Issues" src="https://img.shields.io/badge/issue-tracker-blue?style=flat-square&logoColor=fff&color=0e7acf"/></a>
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&style=flat-square&logoColor=fff&color=0e7acf"/>
<img alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?logo=windows&style=flat-square&logoColor=fff&color=0e7acf"/>
<a href="https://github.com/HackLabsGuitar/helix-py-api/tree/main/LICENSE"><img alt="BSD 3-Clause " src="https://img.shields.io/badge/license-BSD%203--Clause-blue.svg?style=flat-square&logoColor=fff&color=0e7acf"/></a>
<a href="https://github.com/sponsors/hacklabsguitar"><img alt="Sponsor" src="https://img.shields.io/static/v1?style=flat-square&label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86"/></a>
</p>

## Overview

`Helix-py-api` is the unofficial API for managing Line 6 Helix files and related devices. It includes features for editing, standardizing, importing/exporting, renaming, reordering, and cloning bundles, setlists, presets, and snapshots. You can easily build setlists and presets from separate files as well as breakup bundles and setlists into individual setlist and preset files. It also includes simplified MIDI control (i.e. no MIDI message format/value knowledge needed) for Helix hardware and software (Helix Native) as well as direct MIDI control for other Line 6 (ex. FBV) and 3rd party devices. 

`Helix-py-api` will open up a new world of possibilities. Here are a few ideas to get you started:
<table border=0>
<tr>
<td width=25% style="vertical-align: middle;"><img src="https://hacklabsguitar.github.io/helix-py-api/assets/images/idea.png"></td>
<td style="font-size:medium">
<ul>
<li>Automatically change to a specific setlist, preset, and or snapshot with one click (i.e. script, button, etc)
<ol style="list-style-type: circle">
<li>ex. Change on your Helix, your co-guitarist, your bass player, or all at once
</li>
</ol>
<li>Cleanup all your setlist, preset and snapshot names:
<ol style="list-style-type: circle">
<li>ex. Uppercase, no special characters, etc</li>
<li>ex. Change "Lead" to "Solo", "New Preset" to ""</li>
</ol>
<li>Standardize snapshot colors (for every preset in every setlist) to your desired criteria (ex. SOLO=red, CLEAN=WHITE, etc)</li>
<li>Easily mass import a ton of presets into a single setlist
<ol style="list-style-type: circle">
<li>ex. After you downloaded bunch of presets from CustomTone</li>
</ol>
</li>
<li>Individually backup all your presets to Github</li></ul></td>
</tr></table>

## Current Limitations
Until time, knowledge, and desire permits to add new features, below are some notable limitations. 

### Helix

* Reading state/changes directly from the Helix
* Importing/exporting files to/from the Helix
* Anything not exposed in the API (ex. blocks, IRs, favorites, etc)

### Helix Native

* Controlling Helix Native requires a virtual MIDI cable: https://springbeats.com/2016/12/10/springbeats-free-virtual-midi-cable/
* Helix Native midi control through VST's is severely limited as stated in the Helix Native product manual:
    *AU and AAX Plugin Formats Only: At this time, remote MIDI control of setlist and preset changes is supported only with the AU (Mac) and Pro Tools AAX (Mac and Windows) Helix Native plugin formats. It is not supported for the VST2 or VST3 Helix Native plugin formats on Mac or Windows.*

## Support the Project
If you find this project useful, please consider supporting it to help with ongoing development and maintenance:

[![](https://img.shields.io/static/v1?style=flat-square&label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/hacklabsguitar)

Your contributions are greatly appreciated!

## Getting Started

Download and install the API

```bash
git clone https://github.com/HackLabsGuitar/`Helix-py-api`.git
cd `Helix-py-api`
pip install -r requirements.txt
```

Optionally change any default [settings](https://hacklabsguitar.github.io/helix-py-api/settings/).

Create an API instance.

```python
import helixapi

helix = Helix()
```

This will load a default empty bundle template. You can instead load your own bundle:

```python
import helixapi

helix = Helix(file_path="/path/to/bundle.hlb")
```

## Usage Examples

The full API of this library can be found in the [API reference](https://hacklabsguitar.github.io/helix-py-api/helix/).

```python
# Example: Import/export files
helix.setlists[1].import_setlist(file_path="/path/to/setlist.hls")
helix.bundle.export_bundle(file_path="/path/to/bundle.hlb")
```

```python
# Example: Import multiple/export to individual files
helix.setlists[4].presets.import_presets(file_paths=["/path/to/preset1.hlx", "/path/to/preset2.hlx"])
helix.setlists.export_setlists(file_path="/path/to/setlists")
```

```python
# Example: Change properties of a setlist, preset, or snapshot
helix.setlists[0].name = "Setlist 1"
helix.setlists[1].presets[0]. = "Set2-Pres1"
helix.setlists[0].presets[0].snapshots[0].name = "Snapshot 1"

import helixapi.snapshot.LEDColor as LEDColor
helix.setlists[0].presets[0].snapshots[0].ledcolor = LEDColor.RED
```

```python
# Example: loop through items
for setlist in helix.setlists:
    print(setlist.name)
    
    for preset in setlist.presets:
        print(preset.name)

        for snapshot in preset.snapshots:
            print(snapshot.name)
```

```python
# Example: standardize setlists, presets, and snapshots
helix.setlists.standardize()
for setlist in helix.setlists:      
    setlist.presets.standardize()
    for preset in setlist.presets:
        preset.snapshots.standardize()
```

## Licensing

Copyright 2024 Hack Labs Guitar

Licensed under the BSD 3-Clause License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

https://opensource.org/licenses/BSD-3-Clause

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

A copy of the license is available in the repository's [LICENSE](LICENSE) file.