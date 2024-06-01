@echo off
cd /d %~dp0
cd ..
cd ..
pip install black
pip install mkdocs
pip install mkdocs-material
pip install pymdown-extensions
pip install mkdocstrings
pip install mkdocstrings[python]
pip install markdown-callouts
pip install markdown-exec[ansi]
pip install mkdocs-include-markdown-plugin
