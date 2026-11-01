# Rejie Rufin — Personal Portfolio

Static, dependency-free portfolio site for **Rejie Rufin** — Import & Export Logistics, Customs
Documentation, and Process Improvement.

Published with GitHub Pages straight from this repository (no build step, no framework).

```
index.html                       All page markup and content
assets/css/styles.css            Design system, layout, responsive and print styles
assets/js/main.js                Navigation, scroll spy, reveal, project dialog
assets/images/favicon.svg        Brand monogram favicon
assets/images/rejie-rufin-portrait.jpg   (add your photo here — see below)
assets/resume/rejie-rufin-resume.pdf     Resume served by every "Download Resume" button
tools/build_resume_pdf.py        Regenerates the resume PDF from the content above
```

## Preview locally

```bash
python3 -m http.server 3000
# open http://localhost:3000
```

Any static server works; there is nothing to compile or install.

## Portrait photo

The hero uses `profile-photo.jpg` at the project root, referenced as `/profile-photo.jpg`. The file
is served exactly as uploaded (1208 x 1801, unmodified) and is cropped by the existing frame
(`object-fit: cover`, 4:5 container). To change the photo later, replace that one file or update the
`src` on `.portrait__img` in `index.html`.

The image is cropped with `object-fit: cover` and positioned toward the upper part of the frame.

## Update the resume

Every "Download Resume" button points at `assets/resume/rejie-rufin-resume.pdf`. Replace that file
with any PDF using the same name and all buttons keep working.

The bundled PDF reproduces the attached resume — its profile summary, all five roles in their own
wording, education, and skills — and is **encrypted**: it opens only with the owner's password.
The password is never stored in this repository (the site is public). It is supplied at build time:

```bash
pip install reportlab
RESUME_PDF_PASSWORD='...' python3 tools/build_resume_pdf.py
```

Without `RESUME_PDF_PASSWORD` the build stops rather than producing an unprotected file. Printing
and copying are permitted to readers who have the password; editing and annotations are not.

The generated file omits the residential street address and mobile numbers so the public download
carries no more personal detail than the site itself.

All Download Resume buttons point directly at `/RUFIN_REJIE_RESUME.pdf` at the project root. That
file is the owner's own resume, reproduced page-for-page, encrypted with the owner's password
(AES-256). Content is unchanged by the encryption; only the lock is added. The unencrypted original
is kept locally and ignored by Git, so it is never published.

`assets/resume/rejie-rufin-resume.pdf` is no longer referenced by any button. To encrypt any PDF
(including this one) with the same password:

```bash
python3 -c "import pypdf,sys; r=pypdf.PdfReader('original.pdf'); w=pypdf.PdfWriter(); w.append(r); w.encrypt(sys.argv[1]); w.write('assets/resume/rejie-rufin-resume.pdf')" 'PASSWORD'
```

## Add a new project card

Copy one `<li class="card project-card reveal">` block in the Projects section and update:

| Where | What it feeds |
| --- | --- |
| `data-category` | Category line on the card and in the detail dialog |
| `data-title` | Card heading and dialog title |
| `data-desc` | Card description |
| `data-details` | Longer text shown inside the dialog |
| `data-tags` | Comma-separated tags, rendered as pills |
| `data-status` | Small note at the bottom of the dialog |

Then update the visible text inside the card to match. Nothing else is needed — the grid is
`auto-fit`, so new cards flow into the layout.

## Enable LinkedIn / GitHub icons

In the contact section, add a profile URL to `data-href` on the matching `.social` link. The icon
becomes a real, accessible link (opens in a new tab). Leaving `data-href` empty keeps the chip
disabled, so the site never ships a broken or placeholder URL.

## Content rules used on this site

Only supplied information is published: no invented metrics, certifications, awards, testimonials,
employers, or project outcomes. The three operational projects are labelled as personal
process-improvement concepts, not employer products.

## Brand palette

| Token | Value | Use |
| --- | --- | --- |
| Navy | `#0B2038` / `#071A2C` | Headings, primary buttons, dark bands |
| Teal | `#12A8A0` / `#2EC4BB` | Accents, links, active states |
| Background | `#F6F8FA` | Page background |
| Ink | `#141D28` / `#5B6B7A` | Body text / muted text |
| Border | `#E2E9EF` | Hairlines and card borders |
