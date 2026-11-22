"""Generate native, editable PowerPoint plus PDF with the same slide content.

Usage: .venv/bin/python scripts/build_presentation.py
All financial values are computed from the committed Sample Superstore CSV.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation"
ART = OUT / "assets"
ART.mkdir(parents=True, exist_ok=True)
CSV = ROOT / "data/raw/Sample_Superstore.csv"
d = pd.read_csv(CSV,encoding="utf-8-sig")
d.columns=[c.lower().replace(" ","_").replace("-","_") for c in d.columns]
d["order_date"] = pd.to_datetime(d["order_date"],format="%Y-%m-%d")
d["year"] = d.order_date.dt.year

def grp(k):
    t=d.groupby(k,observed=True).agg(sales=("sales","sum"),profit=("profit","sum")).reset_index()
    t["margin"]=100*t.profit/t.sales
    return t

years=grp("year")
cats=grp("category").sort_values("margin",ascending=False)
subs=grp("sub_category").sort_values("profit")
states=grp("state").sort_values("profit")
d["discount_band"]=pd.cut(d.discount,[-.001,0,.2,.4,1],labels=["0%",">0–20%",">20–40%",">40%"],include_lowest=True)
discounts=grp("discount_band")

NAVY="#13253A"
INK="#152B45"
TEAL="#007F85"
RED="#C05455"
BLUE="#337EA5"
LIGHT="#EDF3F5"
MUTED="#657789"
WHITE="#FFFFFF"
GOLD="#F0B85C"

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.titleweight":"bold"})
def save(fig,name):
    fig.savefig(ART/name,bbox_inches="tight",dpi=200,facecolor="white")
    plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(10.5,4.05))
for ax,col,title,color in [(axs[0],"sales","Revenue",BLUE),(axs[1],"profit","Profit",TEAL)]:
    vals=years[col]/1000
    ax.bar([str(x) for x in years.year],vals,color=color,width=.58)
    ax.set_ylim(bottom=0)
    for i,v in enumerate(vals):ax.text(i,v+max(vals)*.02,"$%.0fk"%v,ha="center")
    ax.set_title(title);ax.set_ylabel("USD thousands")
    ax.grid(axis="y",alpha=.15)
    ax.spines[["right","top"]].set_visible(False)
fig.tight_layout(w_pad=2)
save(fig,"yearly.png")

fig,ax=plt.subplots(figsize=(8.5,4.1))
colors=[TEAL,BLUE,RED]
ax.barh(cats.category,cats.margin,color=colors,height=.55)
ax.invert_yaxis();ax.set_xlim(left=0,right=22)
for i,row in enumerate(cats.itertuples()):ax.text(row.margin+.4,i,"%.1f%%"%row.margin,va="center",weight="bold")
ax.set_xlabel("Weighted margin (%)");ax.spines[["right","top","left"]].set_visible(False)
ax.grid(axis="x",alpha=.15);fig.tight_layout()
save(fig,"categories.png")

fig,ax=plt.subplots(figsize=(8.7,4.25))
labels=discounts.discount_band.astype(str).tolist()
vals=discounts.profit.to_numpy()/1000
ax.bar(labels,vals,color=[TEAL if v>0 else RED for v in vals],width=.6)
ax.axhline(0,color=INK,lw=1);ax.set_ylabel("Total profit (USD thousands)")
for i,v in enumerate(vals):
    ax.text(i,v+(10 if v>0 else -20),("%s$%.0fk"%("+" if v>=0 else "−",abs(v))),ha="center",weight="bold")
ax.set_ylim(-140,365);ax.grid(axis="y",alpha=.1);ax.spines[["right","top"]].set_visible(False)
fig.tight_layout();save(fig,"discounts.png")

losers=states.head(6).iloc[::-1]
fig,ax=plt.subplots(figsize=(9,4.1))
vals=abs(losers.profit.to_numpy())/1000
ax.barh(losers.state,vals,color=RED,height=.55)
for i,v in enumerate(vals):ax.text(v+.5,i,"−$%.1fk"%v,va="center")
ax.set_xlim(left=0,right=30);ax.set_xlabel("Total loss magnitude (USD thousands)")
ax.spines[["right","top","left"]].set_visible(False);ax.grid(axis="x",alpha=.15)
fig.tight_layout();save(fig,"states.png")

W,H=13.333,7.5
slides=[]
def new(background=WHITE):
    ob={"background":background,"items":[]}
    slides.append(ob)
    return ob
def rect(s,x,y,w,h,color=LIGHT,radius=.0):
    s["items"].append(("rect",x,y,w,h,color,radius))
def txt(s,value,x,y,w,h,size=17,color=INK,bold=False):
    s["items"].append(("text",str(value),x,y,w,h,size,color,bold))
def img(s,name,x,y,w,h):
    s["items"].append(("image",str(ART/name),x,y,w,h))
def foundation(chapter,title,number,subtitle=None):
    s=new()
    rect(s,0,0,.12,H,TEAL)
    txt(s,chapter.upper(),.6,.3,11,.25,11,TEAL,True)
    txt(s,title,.6,.7,12.05,.75,26,NAVY,True)
    if subtitle:txt(s,subtitle,.6,1.55,11.9,.52,14,MUTED)
    rect(s,.6,7.07,12,.012,"#D7E0E8")
    txt(s,"SAMPLE SUPERSTORE  •  2015–2018  •  EXECUTIVE INSIGHTS",.63,7.14,10,.17,8,MUTED)
    txt(s,"%02d / 10"%number,12.04,7.14,1,.19,8,MUTED)
    return s
def stat(s,value,label,x,y,w):
    rect(s,x,y,w,1.12,LIGHT,.10)
    txt(s,value,x+.18,y+.12,w-.30,.51,25,NAVY,True)
    txt(s,label,x+.18,y+.71,w-.32,.27,12,MUTED)

s=new(NAVY)
rect(s,.66,.78,1.5,.08,GOLD)
txt(s,"DATABASE KNOWLEDGE EXTRACTION",.66,1.09,10,.35,16,GOLD,True)
txt(s,"THE COST OF\nDISCOUNTING",.66,1.68,11.2,2.15,43,WHITE,True)
txt(s,"Why strong retail revenue does not guarantee healthy profitability",.66,4.13,10.6,1.02,22,WHITE)
rect(s,.66,5.57,11.85,.018,MUTED)
txt(s,"9,994 order lines  •  2015–2018  •  US retail sample",.66,5.82,11,.36,16,WHITE)
txt(s,"Juan Manuel Sánchez Hernández  ·  2302084     |     Seir Mendoza Vidal  ·  2302072\nJosé Rodrigo de la Cruz Chim  ·  2302089     |     Marco Antonio Caamal Chi  ·  2302075\nFifth member: [name and student ID pending]",.66,6.02,12.0,1.10,13,GOLD)

s=foundation("01 / Setup","The leadership question",2,"How can revenue grow while some regions and product lines lose money?")
rect(s,.85,2.16,7,3.66,LIGHT,.12)
txt(s,"ARE WE SELLING PROFITABLY?",1.17,2.6,6.26,.75,27,NAVY,True)
txt(s,"Explore the relationship between sales, net profit, discounts, location and product mix.",1.17,3.74,6.23,1.24,20,INK)
rect(s,8.15,2.16,4.25,3.66,NAVY,.12)
txt(s,"KEY DECISION",8.55,2.53,3.4,.4,14,GOLD,True)
txt(s,"Where should the company review pricing, promotions and category strategy?",8.55,3.14,3.32,2.2,21,WHITE,True)

s=foundation("01 / Setup","One dataset, several business lenses",3,"Historical training data, not audited financial statements.")
stat(s,"9,994","Order lines",.72,2.23,2.84)
stat(s,"5,009","Unique orders",3.72,2.23,2.84)
stat(s,"793","Customers",6.72,2.23,2.84)
stat(s,"4","Years",9.72,2.23,2.84)
txt(s,"SOURCE   →   CLEAN   →   ANALYZE   →   VISUALIZE   →   RECOMMEND",.96,4.02,11.5,.5,19,TEAL,True)
txt(s,"Data checks: valid dates and financial fields; missing postal codes treated as unknown.\nOne row represents one order line; distinct orders counted separately.",.98,5.04,11.2,1.22,18,INK)

s=foundation("01 / Setup","Sales growth is not the whole story",4,"Revenues increased between 2015 and 2018, but margins vary by product line.")
img(s,"yearly.png",.78,2.04,11.82,4.35)
txt(s,"2018 sales: $733K   |   2018 profit: $93K   |   margin: 12.74%",1,6.44,11.4,.4,15,TEAL,True)

s=foundation("02 / Insight","Furniture is the profitability outlier",5,"Weighted margin = SUM(profit) / SUM(sales) within each category.")
img(s,"categories.png",.87,2.12,8.55,4.34)
rect(s,9.57,2.27,3.00,3.58,LIGHT,.12)
txt(s,"$742K",9.9,2.58,2.43,.72,29,NAVY,True)
txt(s,"Furniture sales",9.9,3.30,2.43,.36,13,MUTED)
txt(s,"2.49%",9.9,4.20,2.4,.70,29,RED,True)
txt(s,"Furniture margin",9.9,4.92,2.4,.42,13,MUTED)

s=foundation("02 / Insight","Two subcategories lose money",6,"Investigate price, costs and promotions at product level.")
rect(s,.85,2.25,5.66,3.52,LIGHT,.12)
txt(s,"TABLES",1.19,2.58,4.8,.4,16,MUTED,True)
txt(s,"−$17,725",1.19,3.17,4.8,.85,33,RED,True)
txt(s,"Profit across $206,966 in sales",1.19,4.30,4.8,.9,18,INK)
rect(s,6.76,2.25,5.66,3.52,LIGHT,.12)
txt(s,"BOOKCASES",7.09,2.58,4.8,.4,16,MUTED,True)
txt(s,"−$3,473",7.09,3.17,4.8,.85,33,RED,True)
txt(s,"Profit across $114,880 in sales",7.09,4.30,4.8,.9,18,INK)
txt(s,"These totals indicate where to investigate, not the causal reason for the loss.",.97,6.18,11.9,.7,16,TEAL,True)

s=foundation("02 / Insight","Large discounts coincide with losses",7,"Discount bands greater than 20% have negative aggregate profit.")
img(s,"discounts.png",.85,2.17,8.61,4.26)
rect(s,9.63,2.31,2.9,3.35,LIGHT,.12)
txt(s,"−$135K",9.91,2.76,2.45,.75,29,RED,True)
txt(s,"Combined net profit from discount bands above 20%",9.91,3.61,2.28,1.5,17,INK)
txt(s,"Correlation is not causation: test proposed policy changes.",.92,6.52,11.6,.35,14,MUTED)

s=foundation("02 / Insight","Losses concentrate in specific states",8,"Six states with the largest accumulated net losses.")
img(s,"states.png",1.0,2.13,10.63,4.28)
txt(s,"Texas: ~$170K in sales, but a ~$25.7K aggregate loss.",1.0,6.49,11.5,.38,15,RED,True)

s=foundation("03 / Resolution","Three practical actions to test",9,"Propose experiments, measure results and review before changing policy company-wide.")
cards=[
    (.72,"1  PROMOTIONS","Pilot approval controls for discounts above 20%. Measure margin and conversion."),
    (4.87,"2  FURNITURE","Review Tables and Bookcases unit economics, procurement and product mix."),
    (9.02,"3  GEOGRAPHY","Investigate Texas, Ohio, Pennsylvania and Illinois; segment by category."),
]
for x,head,body in cards:
    rect(s,x,2.28,3.58,3.58,LIGHT,.12)
    txt(s,head,x+.23,2.68,3.1,.53,17,TEAL,True)
    txt(s,body,x+.23,3.45,3.13,1.9,18,INK)
txt(s,"Track: total profit • weighted margin • sales • discount intensity • geographic profitability",.88,6.33,11.8,.6,15,NAVY,True)

s=new(NAVY)
rect(s,.72,.86,1.35,.08,GOLD)
txt(s,"EXECUTIVE TAKEAWAY",.72,1.19,10.5,.4,16,GOLD,True)
txt(s,"OPTIMIZE PROFIT,\nNOT REVENUE ALONE.",.72,1.91,11.3,1.95,38,WHITE,True)
txt(s,"Combine sales, profit margin, product mix, discounts and geography before making decisions.",.72,4.40,11.3,1.16,21,WHITE)
txt(s,"Descriptive analytics • Educational sample • No causal guarantees",.72,5.91,11.25,.4,13,GOLD)
txt(s,"Source: github.com/mikemooreviz/superstore (Sample Superstore)",.72,6.76,11.3,.3,11,WHITE)

assert len(slides)==10
prs=Presentation()
prs.slide_width=Inches(W);prs.slide_height=Inches(H)
layout=prs.slide_layouts[6]
pdf=Canvas(str(OUT/"Superstore_Executive_Story.pdf"),pagesize=(W*72,H*72))
for slide in slides:
    p=prs.slides.add_slide(layout)
    p.background.fill.solid()
    p.background.fill.fore_color.rgb=RGBColor.from_string(slide["background"].lstrip("#"))
    pdf.setFillColor(HexColor(slide["background"]))
    pdf.rect(0,0,W*72,H*72,stroke=0,fill=1)
    for item in slide["items"]:
        kind=item[0]
        if kind=="rect":
            _,x,y,w,h,color,radius=item
            sh=p.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                  Inches(x),Inches(y),Inches(w),Inches(h))
            sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(color.lstrip("#"))
            sh.line.fill.background()
            pdf.setFillColor(HexColor(color))
            if radius:pdf.roundRect(x*72,(H-y-h)*72,w*72,h*72,radius*72,stroke=0,fill=1)
            else:pdf.rect(x*72,(H-y-h)*72,w*72,h*72,stroke=0,fill=1)
        elif kind=="text":
            _,value,x,y,w,h,sz,color,bold=item
            box=p.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
            frame=box.text_frame;frame.clear();frame.word_wrap=True
            frame.margin_left=Inches(.01);frame.margin_right=Inches(.01)
            frame.margin_top=Inches(.01);frame.margin_bottom=Inches(0)
            for i,line in enumerate(value.split("\n")):
                pp=frame.paragraphs[0] if i==0 else frame.add_paragraph()
                pp.text=line;pp.font.name="Aptos";pp.font.size=Pt(sz);pp.font.bold=bold
                pp.font.color.rgb=RGBColor.from_string(color.lstrip("#"))
                pp.space_after=Pt(1);pp.line_spacing=1.05
            font="Helvetica-Bold" if bold else "Helvetica"
            pdf.setFillColor(HexColor(color));pdf.setFont(font,sz)
            curr=0
            for line in value.split("\n"):
                for part in simpleSplit(line,font,sz,max(1,w*72-4)):
                    if (curr+1)*sz*1.18>h*72+4:break
                    pdf.drawString(x*72+1,(H-y)*72-sz-(curr)*sz*1.18,part)
                    curr+=1
        elif kind=="image":
            _,path,x,y,w,h=item
            p.shapes.add_picture(path,Inches(x),Inches(y),width=Inches(w),height=Inches(h))
            pdf.drawImage(ImageReader(path),x*72,(H-y-h)*72,width=w*72,height=h*72,preserveAspectRatio=True,anchor="c",mask="auto")
    pdf.showPage()
prs.save(OUT/"Superstore_Executive_Story.pptx")
pdf.save()
print("Generated",len(slides),"slides in both PPTX and PDF.")
print(OUT/"Superstore_Executive_Story.pptx")
print(OUT/"Superstore_Executive_Story.pdf")
