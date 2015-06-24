"""
Helper functions to generate table HTML markup
"""

__author__ = "Dean Oemcke"

def generate_table_header(header_list):

    html = "<html>"
    html += "<head>"
    html += "<style media=\"screen\" type=\"text/css\">"
    html += "table { font-family: sans-serif; font-size: 13px; border-spacing: 0px; border-collapse: collapse; }"
    html += "tr { max-height: 15px }"
    html += "td,th { border: 1px solid #ccc; }"
    html += "</style>"
    html += "</head>"

    html += "<body>"
    html += "<table cellpadding=\"8\" cellspacing=\"0\">"

    html += "<thead>"
    html += "<tr><th>"
    SEPARATOR = "</th><th>"
    html += SEPARATOR.join(header_list)
    html += "</th></tr>"
    html += "</thead>"

    html += "<tbody>"
    return html

def generate_table_row(row):

    html = "<tr><td>"

    SEPARATOR = "</td><td>"
    html += SEPARATOR.join(unicode(i).encode('utf8') for i in row)

    html += "</td></tr>"
    return html

def generate_table_footer():

    html = "</tbody>"
    html += "</table>"
    html += "</body>"
    html += "</html>"
    return html

