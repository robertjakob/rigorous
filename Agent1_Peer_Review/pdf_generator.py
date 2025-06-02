import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.textlabels import Label
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os

class PDFReportGenerator:
    def __init__(self, executive_summary, quality_control, output_path):
        """Initialize the PDF generator with input and output paths."""
        self.executive_summary = executive_summary
        self.quality_control = quality_control
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def load_json(self, file_path):
        """Load and return JSON data from file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def setup_styles(self):
        """Setup custom styles for the PDF."""
        # Define colors
        self.colors = {
            'high_score': colors.HexColor('#4CAF50'),    # Green
            'medium_score': colors.HexColor('#FFC107'),  # Yellow
            'low_score': colors.HexColor('#F44336'),     # Red
            'header_bg': colors.HexColor('#2196F3'),     # Blue
            'header_text': colors.white,
            'footer_text': colors.grey,
            'table_header': colors.HexColor('#E3F2FD'),  # Light Blue
            'table_alt': colors.HexColor('#F5F5F5')      # Light Grey
        }
        
        # Modify existing styles
        self.styles['Heading1'].fontSize = 14
        self.styles['Heading1'].spaceAfter = 12
        self.styles['Heading1'].alignment = TA_LEFT
        self.styles['Heading1'].textColor = colors.black
        
        self.styles['Heading2'].fontSize = 12
        self.styles['Heading2'].spaceAfter = 10
        self.styles['Heading2'].alignment = TA_LEFT
        self.styles['Heading2'].textColor = colors.black
        
        self.styles['Normal'].fontSize = 11
        self.styles['Normal'].spaceAfter = 12
        self.styles['Normal'].alignment = TA_LEFT
        self.styles['Normal'].textColor = colors.black
        
        # Add new styles
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=self.colors['header_text']
        ))
        
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=self.colors['footer_text']
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=16,
            leading=20,
            spaceAfter=16,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            fontSize=13,
            leading=16,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            textColor=colors.black
        ))
        
        # Justified body text
        self.styles.add(ParagraphStyle(
            name='Justified',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Table cell style
        self.styles.add(ParagraphStyle(
            name='TableCell',
            fontSize=10,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=2
        ))
        
        self.styles.add(ParagraphStyle(
            name='SuggestionTableCell',
            fontSize=9,
            leading=11,
            alignment=TA_LEFT,
            spaceAfter=1,
            fontName='Helvetica',
        ))
    
    def get_score_color(self, score):
        """Return color based on score."""
        if score >= 4:
            return self.colors['high_score']
        elif score >= 2.5:
            return self.colors['medium_score']
        return self.colors['low_score']
    
    def create_header(self, canvas, doc):
        """Draw logo centered at the top of every page, just below the top margin."""
        canvas.saveState()
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            page_width, page_height = doc.pagesize
            logo_width = 1.2 * inch
            logo_height = 0.35 * inch
            # Center logo horizontally
            x = (page_width - logo_width) / 2
            y = page_height - doc.topMargin + 10  # 10 points below the top edge
            canvas.drawImage(logo_path, x, y, width=logo_width, height=logo_height, mask='auto')
        canvas.restoreState()
    
    def create_footer(self, canvas, doc):
        """Create footer with page number and date."""
        canvas.saveState()
        
        # Add page number and date
        canvas.setFillColor(self.colors['footer_text'])
        canvas.setFont('Helvetica', 8)
        
        # Page number
        page_text = f"Page {doc.page}"
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.bottomMargin/2, page_text)
        
        # Date
        date_text = datetime.now().strftime("%Y-%m-%d %H:%M")
        canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin/2, date_text)
        
        canvas.restoreState()
    
    def create_cover_page(self):
        """Create the cover page content."""
        elements = []
        
        # Add title
        elements.append(Paragraph("AI Review Report", self.styles['CoverTitle']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Add subtitle with manuscript title
        elements.append(Paragraph(
            "For the manuscript",
            ParagraphStyle(
                name='ManuscriptLabel',
                parent=self.styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=4,
                textColor=colors.black,
                fontName='Helvetica'
            )
        ))
        elements.append(Paragraph(
            self.executive_summary['manuscript_title'],
            ParagraphStyle(
                name='ManuscriptTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=24,
                textColor=colors.black,
                fontName='Helvetica-Bold'
            )
        ))
        
        elements.append(Paragraph(
            f"Publication Outlets: {self.executive_summary['publication_outlets']}",
            ParagraphStyle(
                name='PublicationOutlets',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=2,
                textColor=colors.black,
                fontName='Helvetica'
            )
        ))
        elements.append(Paragraph(
            f"Review Focus: {self.executive_summary['review_focus']}",
            ParagraphStyle(
                name='PublicationOutlets',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=2,
                textColor=colors.black,
                fontName='Helvetica'
            )
        ))
        elements.append(Spacer(1, 0.4*inch))
        
        # Add thank you note
        thank_you = """
        Thank you for using the Rigorous AI Reviewer!<br/><br/>
        We're dedicated to providing actionable, high-quality feedback that accelerates your revision process and boosts your chances of publication. To help us improve the system, please consider completing our short feedback survey. Your input directly contributes to making this tool more useful, accurate, and impactful for the research community. All responses are confidential and sincerely appreciated.<br/><br/>
        <b>Feedback Link:</b> <a href='https://docs.google.com/forms/d/1EhQvw-HdGRqfL01jZaayoaiTWLSydZTI4V0lJSvNpds/edit'><font color='#1976D2'><u>Feedback Form</u></font></a><br/><br/>
        <b>Important Note:</b> Like real human reviews, this AI-generated feedback may occasionally include hallucinations, overconfident statements, vague suggestions, or simply a false statement. Still, we hope you find it insightful and helpful in improving your manuscript for publication. This is very much an MVP (Minimum Viable Product) and is far from being the best version it can be. We are committed to making it truly excellent, and your feedback is essential to help us get there.
        """
        elements.append(Paragraph(thank_you, self.styles['Justified']))
        elements.append(Spacer(1, 0.3*inch))

        # Add CTAs as separate, left-aligned paragraphs
        cta_style = ParagraphStyle(
            name='CTA',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=6,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        link_style = ParagraphStyle(
            name='CTALink',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=2,
            textColor=colors.HexColor('#1976D2'),
            fontName='Helvetica',
        )
        note_style = ParagraphStyle(
            name='CTANote',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=12,
            textColor=colors.black,
            fontName='Helvetica',
        )
        # Website CTA
        elements.append(Paragraph("Want to submit more manuscripts for review?", cta_style))
        elements.append(Paragraph("<a href='https://www.rigorous.company'><u>https://www.rigorous.company</u></a>", link_style))
        elements.append(Paragraph("...We process new submissions for free upon receiving your feedback", note_style))
        # GitHub CTA
        elements.append(Paragraph("Want to help improve the AI Reviewer?", cta_style))
        elements.append(Paragraph("<a href='https://github.com/robertjakob/rigorous'><u>https://github.com/robertjakob/rigorous</u></a>", link_style))
        # Star CTA (single normal black sentence)
        elements.append(Paragraph("...Give us a Star to stay up to date on future improvements and new features of the AI Reviewer!", note_style))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_executive_summary_page(self):
        """Create the executive summary page content."""
        elements = []
        
        # Add executive summary
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(self.executive_summary['executive_summary'], self.styles['Justified']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Merge Section, Rigor, and Writing Scores into one grouped table with vertical spans
        merged_table_data = [["Category", "Sub-Category"]]
        spans = []
        row_idx = 1
        for cat_label, scores in [
            ("Section Assessment", self.quality_control['section_results']),
            ("Rigor Assessment", self.quality_control['rigor_results']),
            ("Writing Assessment", self.quality_control['writing_results'])
        ]:
            group_start = row_idx
            for i, (key, data) in enumerate(scores.items()):
                # Prepend code (key) to sub-category name
                subcat = f"{key} - {data['section_name']}"
                merged_table_data.append([
                    Paragraph(cat_label if i == 0 else "", self.styles['TableCell']),
                    Paragraph(subcat, self.styles['TableCell'])
                ])
                row_idx += 1
            # Add span for this group if more than one row
            if row_idx - group_start > 1:
                spans.append(('SPAN', (0, group_start), (0, row_idx - 1)))
        merged_table = Table(merged_table_data, colWidths=[1.7*inch, 4.2*inch], repeatRows=1)
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['header_bg']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('LINEBELOW', (0, 0), (-1, 0), 1.2, self.colors['header_bg']),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#E3F2FD')),
            ('BACKGROUND', (1, 1), (-1, -1), self.colors['table_alt']),
            ('ROWBACKGROUNDS', (1, 1), (-1, -1), [self.colors['table_alt'], colors.white]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
            ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#B0BEC5')),
            ('BOX', (0, 0), (-1, -1), 1.2, self.colors['header_bg']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        table_style.extend(spans)
        merged_table.setStyle(TableStyle(table_style))
        elements.append(merged_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def create_detailed_analysis_pages(self):
        """Create the detailed analysis pages content."""
        elements = []
        
        # Process section, rigor, and writing results
        for group in [
            self.quality_control['section_results'],
            self.quality_control['rigor_results'],
            self.quality_control['writing_results']
        ]:
            for section_id, section_data in group.items():
                elements.append(PageBreak())
                # Add code prefix to section header
                section_title = f"{section_id} - {section_data['section_name']}"
                elements.append(Paragraph(section_title, self.styles['SectionHeader']))
                # Add summary
                elements.append(Paragraph(section_data['summary'], self.styles['Justified']))
                elements.append(Spacer(1, 0.2*inch))
                # Add suggestions
                if 'suggestions' in section_data and section_data['suggestions']:
                    # Create table for suggestions
                    table_data = [['Remarks', 'Original', 'Improved', 'Explanation']]
                    for suggestion in section_data['suggestions']:
                        # Use small font for body cells
                        table_data.append([
                            Paragraph(suggestion.get('remarks', ''), self.styles['SuggestionTableCell']),
                            Paragraph(suggestion['original_text'], self.styles['SuggestionTableCell']),
                            Paragraph(suggestion['improved_version'], self.styles['SuggestionTableCell']),
                            Paragraph(suggestion['explanation'], self.styles['SuggestionTableCell'])
                        ])
                    # Create and style table
                    table = Table(table_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch, 1.8*inch], repeatRows=1)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.colors['header_bg']),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 11),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('LINEBELOW', (0, 0), (-1, 0), 1.2, self.colors['header_bg']),
                        ('BACKGROUND', (0, 1), (-1, -1), self.colors['table_alt']),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors['table_alt'], colors.white]),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                        ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#B0BEC5')),
                        ('BOX', (0, 0), (-1, -1), 1.2, self.colors['header_bg']),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    elements.append(table)
        
        return elements
    
    def generate_pdf(self):
        """Generate the complete PDF report."""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the document
        elements = []
        
        # Add cover page
        elements.extend(self.create_cover_page())
        elements.append(PageBreak())
        
        # Add executive summary page
        elements.extend(self.create_executive_summary_page())
        elements.append(PageBreak())
        
        # Add detailed analysis pages
        elements.extend(self.create_detailed_analysis_pages())
        
        # Build the PDF with headers and footers
        doc.build(elements, 
                 onFirstPage=lambda c, d: (self.create_header(c, d), self.create_footer(c, d)),
                 onLaterPages=lambda c, d: (self.create_header(c, d), self.create_footer(c, d)))

def generate_pdf(inputs):      
    # Generate PDF
    generator = PDFReportGenerator(inputs['executive_summary_results'], inputs['quality_control_results'], inputs['output_path'])
    generator.generate_pdf()
    print(f"PDF report generated successfully at: {inputs['output_path']}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(base_dir, 'results', 'executive_summary.json'), "r") as f:
        executive_summary = json.load(f)
        
    with open(os.path.join(base_dir, 'results', 'quality_control_results.json'), "r") as f:
        quality_control_results = json.load(f)    
    
    inputs = {
        'executive_summary_results': executive_summary,
        'quality_control_results': quality_control_results,
        'output_path': os.path.join(base_dir, 'reports', 'review_report.pdf')
    }
            
    generate_pdf(inputs)