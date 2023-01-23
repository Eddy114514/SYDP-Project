import os

from pylatex import Document, PageStyle, Head, Foot, MiniPage, \
    StandAloneGraphic, MultiColumn, Tabu, LongTabu, LargeText, MediumText, \
    LineBreak, NewPage, Tabularx, TextColor, simple_page_number
from pylatex.utils import bold, NoEscape


def generate_unique():
    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)

    # Generating first page style
    first_page = PageStyle("firstpage")

    # Header image
    with first_page.create(Head("L")) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                         pos='c')) as logo_wrapper:

            logo_wrapper.append(StandAloneGraphic(image_options="width=120px",
                                filename="C:\SYDP-Project\asset\Picture\MSA_logo.png"))

    # Add document title
    with first_page.create(Head("R")) as right_header:
        with right_header.create(MiniPage(width=NoEscape(r"0.49\textwidth"),
                                 pos='c', align='r')) as title_wrapper:
            title_wrapper.append(LargeText(bold("Bank Account Statement")))
            title_wrapper.append(LineBreak())
            title_wrapper.append(MediumText(bold("Date")))

    # Add footer
    with first_page.create(Foot("C")) as footer:
        message = "Important message please read"
        with footer.create(Tabularx(
                "X X X X",
                width_argument=NoEscape(r"\textwidth"))) as footer_table:

            footer_table.add_row(
                [MultiColumn(4, align='l', data=TextColor("blue", message))])
            footer_table.add_hline(color="blue")
            footer_table.add_empty_row()

            branch_address = MiniPage(
                width=NoEscape(r"0.25\textwidth"),
                pos='t')
            branch_address.append("960 - 22nd street east")
            branch_address.append("\n")
            branch_address.append("Saskatoon, SK")

            document_details = MiniPage(width=NoEscape(r"0.25\textwidth"),
                                        pos='t', align='r')
            document_details.append("1000")
            document_details.append(LineBreak())
            document_details.append(simple_page_number())

            footer_table.add_row([branch_address, branch_address,
                                  branch_address, document_details])

    doc.preamble.append(first_page)
    # End first page style



    doc.append(NewPage())
    doc.append("Hello World")

    doc.generate_tex("complex_report")

generate_unique()