from pathlib import Path
import json,csv
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
R=Path(__file__).resolve().parents[1];data=R/'results/final'
pages=json.loads((data/'report_content.json').read_text(encoding='utf-8'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='TitleCustom',fontName='Helvetica-Bold',fontSize=23,leading=27,textColor=colors.HexColor('#153e44'),spaceAfter=13))
styles.add(ParagraphStyle(name='Section',fontName='Helvetica-Bold',fontSize=11,leading=14,textColor=colors.HexColor('#247d72'),spaceBefore=10,spaceAfter=4))
styles.add(ParagraphStyle(name='Copy',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=5))
styles.add(ParagraphStyle(name='CaptionCustom',fontName='Helvetica',fontSize=8,leading=11,textColor=colors.HexColor('#52626b'),spaceAfter=8))
story=[]
for i,p in enumerate(pages):
 if i:story.append(PageBreak())
 story.append(Paragraph(escape(p['title']),styles['TitleCustom']))
 if p.get('subtitle'):story.append(Paragraph(escape(p['subtitle']),styles['Section']))
 for title,body in p['sections']:
  story.extend([Paragraph(escape(title),styles['Section']),Paragraph(escape(body),styles['Copy'])])
 if p.get('figure'):
  from PIL import Image as PILImage
  im=PILImage.open(data/p['figure']);w,h=im.size
  story.extend([Spacer(1,9),Image(str(data/p['figure']),width=480,height=480*h/w),Paragraph(escape(p['caption']),styles['CaptionCustom'])])
 if p.get('table'):
  rows=[['Year','Rainfall (mm)','Mean temp. (C)','Days >10 mm']]
  for r in csv.DictReader((data/'annual_summary.csv').open()):rows.append([r['year'],f'{float(r["rainfall_mm"]):.2f}',f'{float(r["temperature_c"]):.2f}',r['heavy_rain_days_gt10mm']])
  table=Table(rows,colWidths=[80,135,135,130],rowHeights=18)
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#153e44')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(1,0),(-1,-1),'RIGHT'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#eef5f4'),colors.white]),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
  story.extend([Spacer(1,8),table])
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#cddbd8'));c.line(48,42,547,42);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#52626b'));c.drawString(48,29,'Musab Shahid | Monsoon Rainfall & Flood-Risk Analysis for Multan | Final release, November 2026');c.drawRightString(547,29,str(doc.page))
pdf=R/'docs/FINAL_REPORT.pdf';SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=55,title='Monsoon Rainfall & Flood-Risk Analysis for Multan: ERA5 2016-2025',author='Musab Shahid').build(story,onFirstPage=footer,onLaterPages=footer)
print(pdf)
