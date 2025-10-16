# This directory will contain PDF versions of the deliverables

To generate PDFs from the Markdown files:

## Using Pandoc (recommended)

```bash
pandoc cahier_des_charges.md -o pdf/cahier_des_charges.pdf --pdf-engine=xelatex -V geometry:margin=1in
pandoc synthese_commerciale.md -o pdf/synthese_commerciale.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

## Using online converters

- [Markdown to PDF](https://www.markdowntopdf.com/)
- [Dillinger](https://dillinger.io/)
- [HackMD](https://hackmd.io/)

## Using print to PDF

1. Open the Markdown file in VS Code preview
2. Use browser print function
3. Save as PDF
