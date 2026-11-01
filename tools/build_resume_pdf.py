#!/usr/bin/env python3
"""Build the downloadable resume PDF.

The content below mirrors the attached resume (RUFIN, REJIE_RESUME.pdf) — same
sections, roles, wording and skills — so the file served by the site is that
resume. Replace assets/resume/rejie-rufin-resume.pdf with the original PDF at
any time; every "Download Resume" button points at that exact path.

Two deliberate omissions for public publishing:
  * residential street address (per the portfolio brief)
  * mobile numbers (two different numbers appear in the source; omitted rather
    than publishing a possibly outdated one)

Typos in the source ("shioment", "custom brokers", "Adaptibility",
"Continuos") are corrected.

The output is always encrypted. The password is read from the environment and is
never stored in this repository:

    RESUME_PDF_PASSWORD='...' python3 tools/build_resume_pdf.py

"""

import os
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

NAVY = colors.HexColor("#0B2038")
TEAL = colors.HexColor("#0D8F8A")
INK = colors.HexColor("#22303D")
MUTED = colors.HexColor("#5B6B7A")
RULE = colors.HexColor("#D8E2EA")

OUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "resume" / "rejie-rufin-resume.pdf"

NAME = "REJIE RUFIN"
HEADLINE = "Import &amp; Export Logistics &amp; Documentation Specialist"
CONTACT = "Bacoor City, Cavite, Philippines&nbsp;&nbsp;&bull;&nbsp;&nbsp;rejierufinxxvii@gmail.com"

PROFILE = (
    "Results-driven logistics and customs documentation professional with experience in import customs "
    "manifest processing, freight forwarding operations, airfreight documentation, import-export "
    "coordination, government liaison services, and administrative support. Demonstrated expertise in "
    "preparing and validating shipping documentation, ensuring regulatory compliance, coordinating with "
    "global stakeholders, and managing time-sensitive operational processes. Proven ability to maintain "
    "high accuracy, meet strict deadlines, and support business continuity in fast-paced environments."
)

EXPERIENCE = [
    {
        "role": "Import Customs Manifest Specialist",
        "org": "Maersk Global Service Centre &ndash; Philippines",
        "dates": "2023 &ndash; Present",
        "bullets": [
            "Responsible for ensuring the timely, accurate and compliant preparation and submission of import customs manifest for shipments arriving in Vietnam and Cambodia.",
            "Maintained high accuracy and timely completion of customs manifest reports.",
        ],
    },
    {
        "role": "Senior Documentation Officer / IMPEX Coordinator",
        "org": "ATR International Freight Inc. &ndash; Port Area, Manila",
        "dates": "2017 &ndash; 2023",
        "bullets": [
            "Managed end-to-end import air &amp; sea manifest processing and submission through the e-Trade/e2m Customs System.",
            "Ensured timely and accurate filing of cargo manifest for import air &amp; sea shipments, maintaining compliance with Philippine customs regulations.",
            "Coordinated with international agents, airlines, shipping lines and customs brokers to resolve documentation discrepancies and prevent cargo clearance delays.",
            "Processed manifest amendments, cargo updates and shipment exceptions while meeting operational deadlines.",
            "Maintained high levels of accuracy in shipment data, supporting efficient customs processing and import operations.",
            "Coordinated end-to-end air export shipments from booking to cargo uplift.",
            "Prepared and reviewed export shipping documents, including MAWB, HAWB, commercial invoices, packing list, export declarations, and shipping instructions.",
        ],
    },
    {
        "role": "Administrative Staff",
        "org": "Municipal Treasurer&rsquo;s Office &ndash; Municipality of Isabel",
        "dates": "February 2016 &ndash; May 2016",
        "bullets": [
            "Assisted in the posting and recording of daily disbursement transactions, ensuring accurate financial documentation and record keeping.",
            "Supported payroll administration by preparing payslips and maintaining employee compensation records.",
            "Managed the uploading and maintenance of employee BIR records and tax-related information.",
            "Performed data entry, report generation, and administrative support functions for treasury operations.",
            "Maintained confidentiality and accuracy of financial and employee records.",
        ],
    },
    {
        "role": "Liaison Officer",
        "org": "Inspira Prime International Corp. &ndash; Quezon City",
        "dates": "2013 &ndash; 2015",
        "bullets": [
            "Managed permit processing and regulatory compliance requirements with BIR, LGUs, Barangay Offices and other government agencies.",
            "Facilitated business permit applications, renewals, registrations, and documentary submissions.",
            "Maintained strong working relationships with government offices, banks, and external stakeholders.",
        ],
    },
    {
        "role": "Census Area Supervisor",
        "org": "Philippine Statistics Authority &ndash; Tacloban City, Leyte",
        "dates": "2013 &ndash; 2015",
        "bullets": [
            "Supervised field operations to ensure accurate data collection and adherence to protocols.",
            "Trained and mentored enumerators on data gathering techniques and best practices.",
            "Coordinated logistics for census activities, optimizing resource allocation and efficiency.",
            "Reviewed collected data for consistency, identifying discrepancies for timely resolution.",
        ],
    },
]

EDUCATION = {
    "degree": "Bachelor of Science in Shipping Management",
    "school": "Palompon Institute of Technology",
    "dates": "June 2011 &ndash; March 2015",
}

SYSTEMS = [
    "Microsoft Excel",
    "Microsoft Word",
    "Process Flows",
    "Microsoft Teams",
    "e2m / e-Trade System",
    "Microsoft Outlook",
]

PROFESSIONAL_SKILLS = [
    "Attention to Detail",
    "Time Management",
    "Process Ownership",
    "Communication Skills",
    "Adaptability and Flexibility",
    "Continuous Improvement",
]


def build_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["name"] = ParagraphStyle(
        "name", parent=base["Title"], fontName="Helvetica-Bold", fontSize=21,
        leading=24, textColor=NAVY, alignment=TA_LEFT, spaceAfter=2,
    )
    styles["headline"] = ParagraphStyle(
        "headline", fontName="Helvetica-Bold", fontSize=9.4, leading=12.4,
        textColor=TEAL, spaceAfter=2,
    )
    styles["contact"] = ParagraphStyle(
        "contact", fontName="Helvetica", fontSize=8.4, leading=12, textColor=MUTED,
    )
    styles["section"] = ParagraphStyle(
        "section", fontName="Helvetica-Bold", fontSize=9.4, leading=12,
        textColor=NAVY, spaceBefore=9, spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=8.9, leading=12.6, textColor=INK,
    )
    styles["role"] = ParagraphStyle(
        "role", fontName="Helvetica-Bold", fontSize=9.9, leading=12.4, textColor=NAVY,
    )
    styles["org"] = ParagraphStyle(
        "org", fontName="Helvetica-Oblique", fontSize=8.7, leading=11.4, textColor=MUTED,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=styles["body"], leftIndent=9, bulletIndent=1,
        spaceBefore=1.2, bulletFontName="Helvetica", bulletFontSize=8.9,
    )
    return styles


class ResumeDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        frame = Frame(
            self.leftMargin, self.bottomMargin, self.width, self.height, id="main",
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        )
        self.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=self._footer)])

    def _footer(self, canvas, _doc):
        canvas.saveState()
        width, _ = A4
        y = 14 * mm
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(self.leftMargin, y + 9, width - self.rightMargin, y + 9)
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, y, "Rejie Rufin  |  Import & Export Logistics & Documentation Specialist")
        canvas.drawRightString(width - self.rightMargin, y, "Page %d" % canvas.getPageNumber())
        canvas.restoreState()


def section_title(text):
    return Paragraph(text.upper(), STYLES["section"])


def encryption():
    """Password protection for the downloadable resume.

    The password comes from RESUME_PDF_PASSWORD so it never lands in the repo
    (this project is published publicly on GitHub Pages). Printing and copying
    are allowed; editing and annotations are not.
    """
    password = os.environ.get("RESUME_PDF_PASSWORD", "")
    if not password:
        sys.exit(
            "RESUME_PDF_PASSWORD is not set. The resume must be encrypted before it is\n"
            "published. Re-run with:  RESUME_PDF_PASSWORD='...' python3 tools/build_resume_pdf.py"
        )
    return StandardEncryption(
        userPassword=password,
        ownerPassword=password,
        canPrint=1,
        canModify=0,
        canCopy=1,
        canAnnotate=0,
        strength=128,
    )


def build():
    doc = ResumeDoc(
        str(OUT_PATH), pagesize=A4,
        leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm, bottomMargin=20 * mm,
        title="Rejie Rufin - Resume",
        author="Rejie Rufin",
        subject="Import & Export Logistics & Documentation Specialist",
        encrypt=encryption(),
    )

    story = [
        Paragraph(NAME, STYLES["name"]),
        Paragraph(HEADLINE, STYLES["headline"]),
        Paragraph(CONTACT, STYLES["contact"]),
        Spacer(1, 7),
        section_title("Profile Summary"),
        Paragraph(PROFILE, STYLES["body"]),
        section_title("Work Experience"),
    ]

    for index, job in enumerate(EXPERIENCE):
        block = [
            Paragraph(job["role"], STYLES["role"]),
            Paragraph("%s &nbsp;&bull;&nbsp; %s" % (job["org"], job["dates"]), STYLES["org"]),
            Spacer(1, 3),
        ]
        block += [Paragraph(b, STYLES["bullet"], bulletText="•") for b in job["bullets"]]
        if index < len(EXPERIENCE) - 1:
            block.append(Spacer(1, 7))
        story.append(KeepTogether(block))

    story.append(
        KeepTogether([
            section_title("Education"),
            Paragraph(EDUCATION["degree"], STYLES["role"]),
            Paragraph(
                "%s &nbsp;&bull;&nbsp; %s" % (EDUCATION["school"], EDUCATION["dates"]),
                STYLES["org"],
            ),
        ])
    )

    story.append(
        KeepTogether([
            section_title("Skills"),
            Paragraph(" &nbsp;&bull;&nbsp; ".join(SYSTEMS), STYLES["body"]),
        ])
    )
    story.append(
        KeepTogether([
            section_title("Professional Skills"),
            Paragraph(" &nbsp;&bull;&nbsp; ".join(PROFESSIONAL_SKILLS), STYLES["body"]),
        ])
    )

    doc.build(story)


STYLES = build_styles()

if __name__ == "__main__":
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    build()
    print("Wrote %s (%d bytes, encrypted)" % (OUT_PATH, OUT_PATH.stat().st_size))
