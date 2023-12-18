# ENJP Technical Lexicon

This repository gives a mkdocs baseline for the English-Japanese Technical Lexicon available [here](https://basilems.github.io/ENJP-Technical-Lexicon/)


## Quick start

When accessing the website, you will find entries either by searching the top search bar or by filtering through the topics on the left side.

![](MainPage.png)

## Installation

When cloning the project, there are some install requirements:
```
pip install mkdocs
pip install mkdocs-materials
pip install mkdocs-roamlinks-plugin
pip install mkdocs-mermaid2-plugin
pip install mkdocs-callouts
```

## Add entries

### By using the (Template)[Template.md]

You can use the template file to create new entries.
Add related information into the appropriate fields and delete unneeded ones.

### By unsing (Streamlit)[entry_generator.py]

Streamlit allows for an interactive protal to create automatically new entries. You will need to install the following:
```
pip install streamlit
```
After installing the library, please execute the following command:
```
streamlit run entry_generator.py
```
This will direct you to an easy-to-use web app to add new entries to the project.

## Contribute

If you want to contribute to this repository, you can duplicate the [Template.md](Template.md) in the root directory of the project. This preserves the same layout for all entries in the lexicon for a better experience.

After adding new entries, please commit changes and send a pull request.
