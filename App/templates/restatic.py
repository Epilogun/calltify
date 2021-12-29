import codecs
import sys
import os
from bs4 import BeautifulSoup as Soup

def parse_html(file_name, output_file, framework="flask", supported_tags=["link", "script", "img", "video"]):
    framework = framework.lower()

    def parse_tags(tag):
        def parse_doc(doc):
            if doc == None:
                return doc
            else:
                if framework == "flask":
                    doc = "{{ url_for('static', filename = '" + doc + "') }}"
                elif framework == "django":
                    doc = "{% static '" + doc + "' %}"
                else:
                    print("Unknown framework {} passed".format(framework))
                return doc

        try:
            if tag.name == "link":
                doc_link = tag["href"]
            elif tag.name in ["script", "img", "video"]:
                doc_link = tag["src"]
            else:
                doc_link = None
        except:
            doc_link = None

        if doc_link == None:
            return str(tag)
        else:
            return str(tag).replace(doc_link, parse_doc(doc_link))

    html = open(file_name, "r").read()
    html_soup = Soup(html, "html.parser")

    for i in html_soup.find_all(supported_tags):
        i.replace_with(Soup(parse_tags(i), "html.parser"))

    clean_html = html_soup.prettify()
    if framework == "django":
        clean_html = "{% load static %}\n\n" + clean_html

    codecs.open(output_file, "w", "utf-8").write(clean_html)
    print("Successfully formatted '{}' to {} template".format(file_name, framework))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""python restatic.py <file.html> <flask|django>""")
        print("""python restatic.py . <flask|django>""")
        print("""python restatic.py <file.html> <flask|django> <output.html>""")
    else:
        if sys.argv[1] == ".":
            all_html = [file for file in os.listdir(".") if file.split(".")[-1] == "html"]
            for html in all_html:
                parse_html(html, html, sys.argv[2])
        else:
            try:
                output_file = sys.argv[3]
            except:
                output_file = sys.argv[1]
            parse_html(sys.argv[1], output_file, sys.argv[2])
