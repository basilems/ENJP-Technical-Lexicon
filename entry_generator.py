import regex as re

import streamlit as st
import glob as gl
from io import open

def create_tags(tag_list):
    md_start = """---
tags:
"""
    md_middle = [f"""  - {tag}""" for tag in tag_list]
    md_end = """
---"""

    return md_start + '\n'.join(tag for tag in md_middle) + md_end

def assign_category(category):
    return f"docs/{category}"

def get_categories():
    dirs = gl.glob("docs/*/")
    dirs = [text[5:-1] for text in dirs]
    return dirs

def create_mermaid_graph(eng, kanji, kana, romaji, multiple,*eng2):
    graph_start = """``` mermaid
graph LR"""

    if not multiple:
        graph_eng = f"""
  A((=)) --> B([{eng}]);"""
    else:
        graph_eng = f"""
  A((=)) --> B((English Transcription));
  B --> F([{eng}]);
  B --> G([{eng2}]);"""

    graph_jp = f"""
  A --> C([{kanji}]);
  C --> D([{kana}]);
  C --> E([{romaji}]);
```"""

    return graph_start + graph_eng + graph_jp

def create_caution(caution_list):
    caution_start = """> [!CAUTION]
> May be confused with:
"""

    caution_content = [f"""> - [[{item}]]""" for item in caution_list]

    return caution_start + "\n".join(item for item in caution_content)

def create_note(note_list, roots):
    intro_text = ["Used in", "Derived from"]

    note_start = f"""> [!Note]
> {intro_text[int(roots)]}:
"""

    note_content = [f"""> - [[{item}]]""" for item in note_list]

    return note_start + "\n".join(item for item in note_content)

def create_tip(link_list):
    note_start = f"""> [!tip]
> See more:
"""
    if isinstance(link_list, dict):
        note_content = [f"""> - ({item['title']})[{item['link']}]""" for item in link_list]
    else:
        note_content = [f"""> - ({item})[{item}]""" for item in link_list]

    return note_start + "\n".join(item for item in note_content)


if __name__ == "__main__":
    t = create_tags(["ML", "Neural Networks", "Statistics"])
    f = create_mermaid_graph("Distribution", "分布", "ぶんぷ", "bunpu", False)
    g = create_caution(["Distribution - 分布"])
    h = create_note(["Test ref 1"], True)
    i = create_tip([{"title":"Wiki", "link": "https://wikipedia.org/"}])
    print(t)
    print(f)
    print(g)
    print(h)
    print(i)

    print(get_categories())

    st.title("Lexicon Entry Generator")
    st.text("This web app allows for an easy and fast workflow when "
            "adding new entries to the project")

    category = st.selectbox("Please select the main category of the entry",
                            get_categories())

    tags = st.text_input("Add tags", placeholder="Please separate with commas")

    tags_list = re.split(", *", tags)

    st.caption(tags_list)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("English")

        eng = st.text_input("English translation")
        eng2 = None
        multiple_translation = st.checkbox("Multiple translations")

        if multiple_translation:
            eng2 = st.text_input("Additional english translations")

        st.caption(eng2)

    with col2:
        st.subheader("Japanese")

        jp = st.text_input("Kanji transcription")

        kana = st.text_input("Furigana transcription")

        romaji = st.text_input("Romaji transcription")

    st.header("Optional fields")

    entries = gl.glob("docs/*/*.md")
    print(entries)
    info_name = map(lambda x: re.search(r"\\.*\\(?P<name>.*).md", x).group("name"), entries)
    caution_name = map(lambda x: re.search(r"\\.*\\(?P<name>.*).md", x).group("name"), entries)

    c1, c2, c3 = st.columns(3)

    with c1:
        info = st.toggle("Linked to other entries")

        if info:
            info_list = st.multiselect("Add reference", info_name, key="info")
    with c2:
        caution = st.toggle("Can be confused with other entries")

        if caution:
            caution_list = st.multiselect("Add reference", caution_name, key="caution")
    with c3:
        tip = st.toggle("Add references")

        if tip:
            links = st.text_area("Paste the link of reference",
                                 placeholder="Please separate with commas")

            link_list = re.split(",|, |,\\n", links)
            st.caption(link_list)

    st.divider()

    if eng and jp and kana and romaji:
        if 'processed' not in st.session_state:
            st.session_state.processed = {}

        if st.button("Generate file"):
            with st.spinner("Generating"):
                st.write("Creating file")
                with open(f"docs/{category}/{eng} - {jp}.md", "x", encoding="utf-8") as md:
                    st.write("Adding tags")
                    md.write(create_tags(tags_list))
                    md.write("\n")
                    md.write(f"# {eng} - {jp}")
                    md.write("\n")

                    st.write("Adding translations")
                    md.write(create_mermaid_graph(eng, jp, kana, romaji, multiple_translation, eng2))
                    md.write("\n")

                    if tip or caution or info:
                        st.write("Adding additional information")
                        if info:
                            md.write(create_note(info_list, True))
                            md.write("\n")
                        if caution:
                            md.write(create_caution(caution_list))
                            md.write("\n")
                        if tip:
                            md.write(create_tip(link_list))
                            md.write("\n")
            st.session_state.processed["created"] = f"{eng} - {jp}"

        if "created" in st.session_state.processed:
            st.subheader(f"File '{st.session_state.processed['created']}' has been successfully generated")
