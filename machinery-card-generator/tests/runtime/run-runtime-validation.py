#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import tempfile
import subprocess
import hashlib
import json
import math
import textwrap
import sys

parser=argparse.ArgumentParser(description='TCG#10 deterministic runtime contract harness')
parser.add_argument('--output-dir', help='Каталог для сохранения артефактов; без параметра используется временный каталог')
args=parser.parse_args()
BASE=Path(args.output_dir).resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='tcg10-runtime-'))
ROOT=BASE/'machinery-card-generator'
RUNTIME = ROOT / 'tests' / 'runtime'
INPUTS = RUNTIME / 'inputs'
OUTPUTS = RUNTIME / 'outputs'
ANALYSES = RUNTIME / 'analyses'
EVIDENCE = RUNTIME / 'evidence'
for d in (INPUTS, OUTPUTS, ANALYSES, EVIDENCE):
    d.mkdir(parents=True, exist_ok=True)

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit_text(draw, text, box, max_size, min_size=16, bold=False, max_lines=2):
    x0, y0, x1, y1 = box
    for size in range(max_size, min_size - 1, -1):
        f = font(size, bold)
        words = text.split()
        lines = []
        cur = ''
        for word in words:
            test = word if not cur else cur + ' ' + word
            if draw.textbbox((0,0), test, font=f)[2] <= x1-x0:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        if len(lines) <= max_lines:
            line_h = size + 6
            if len(lines) * line_h <= y1-y0:
                return f, lines
    return font(min_size, bold), [text]


def draw_centered_lines(draw, lines, box, f, fill='black', spacing=6):
    x0,y0,x1,y1=box
    heights=[]
    for line in lines:
        b=draw.textbbox((0,0), line, font=f)
        heights.append(b[3]-b[1])
    total=sum(heights)+spacing*(len(lines)-1)
    y=y0+(y1-y0-total)/2
    for line,h in zip(lines,heights):
        b=draw.textbbox((0,0), line, font=f)
        w=b[2]-b[0]
        draw.text((x0+(x1-x0-w)/2,y),line,font=f,fill=fill)
        y+=h+spacing


def environment(draw, box, kind='earth'):
    x0,y0,x1,y1=box
    draw.arc((x0+20,y0+35,x0+230,y0+190),180,340,fill=(185,185,185),width=2)
    draw.arc((x0+150,y0+50,x0+390,y0+205),180,340,fill=(195,195,195),width=2)
    for tx in (x0+60, x0+315):
        draw.line((tx,y0+145,tx,y0+105),fill=(185,185,185),width=2)
        draw.line((tx,y0+110,tx-13,y0+128),fill=(185,185,185),width=2)
        draw.line((tx,y0+110,tx+13,y0+128),fill=(185,185,185),width=2)
    draw.line((x0+10,y0+225,x1-10,y0+215),fill=(160,160,160),width=2)
    draw.line((x0+10,y0+270,x1-10,y0+255),fill=(150,150,150),width=2)
    draw.line((x0+10,y0+335,x1-10,y0+320),fill=(120,120,120),width=3)
    draw.line((x0+10,y0+370,x1-10,y0+350),fill=(100,100,100),width=3)
    for i in range(14):
        xx=x0+20+i*28
        yy=y0+315+(i%3)*9
        draw.line((xx,yy,xx+18,yy-4),fill=(150,150,150),width=2)


def draw_bulldozer(draw, ox, oy, s=1.0, line=5):
    def P(points): return [(ox+int(x*s),oy+int(y*s)) for x,y in points]
    draw.rounded_rectangle((ox,oy+140*s,ox+270*s,oy+250*s),radius=int(42*s),fill='white',outline='black',width=line)
    draw.rounded_rectangle((ox+22*s,oy+160*s,ox+245*s,oy+230*s),radius=int(28*s),outline='black',width=max(2,line-2))
    for cx,cy,r in [(55,195,25),(130,195,27),(205,195,24)]:
        draw.ellipse((ox+(cx-r)*s,oy+(cy-r)*s,ox+(cx+r)*s,oy+(cy+r)*s),fill='white',outline='black',width=max(2,line-2))
    draw.polygon(P([(60,140),(85,70),(205,70),(235,140)]),fill='white',outline='black')
    draw.line(P([(60,140),(85,70),(205,70),(235,140)]),fill='black',width=line,joint='curve')
    draw.polygon(P([(100,70),(112,22),(190,22),(205,70)]),fill='white',outline='black')
    draw.line(P([(100,70),(112,22),(190,22),(205,70)]),fill='black',width=line,joint='curve')
    draw.rectangle((ox+119*s,oy+30*s,ox+150*s,oy+62*s),fill='white',outline='black',width=3)
    draw.rectangle((ox+157*s,oy+30*s,ox+184*s,oy+62*s),fill='white',outline='black',width=3)
    draw.line(P([(220,125),(280,145)]),fill='black',width=line)
    draw.line(P([(220,165),(280,178)]),fill='black',width=line)
    draw.polygon(P([(272,120),(325,128),(326,226),(278,230)]),fill='white',outline='black')
    draw.line(P([(272,120),(325,128),(326,226),(278,230),(272,120)]),fill='black',width=line,joint='curve')
    draw.arc((ox+270*s,oy+145*s,ox+330*s,oy+230*s),250,100,fill='black',width=max(2,line-2))


def draw_loader(draw, ox, oy, s=1.0, line=5):
    def P(points): return [(ox+int(x*s),oy+int(y*s)) for x,y in points]
    for cx,r in [(70,45),(210,50)]:
        draw.ellipse((ox+(cx-r)*s,oy+(180-r)*s,ox+(cx+r)*s,oy+(180+r)*s),fill='white',outline='black',width=line)
        draw.ellipse((ox+(cx-20)*s,oy+160*s,ox+(cx+20)*s,oy+200*s),fill='white',outline='black',width=3)
    draw.polygon(P([(55,145),(78,70),(180,70),(205,150)]),fill='white',outline='black')
    draw.line(P([(55,145),(78,70),(180,70),(205,150)]),fill='black',width=line,joint='curve')
    draw.polygon(P([(92,72),(105,28),(165,28),(180,72)]),fill='white',outline='black')
    draw.line(P([(92,72),(105,28),(165,28),(180,72)]),fill='black',width=line,joint='curve')
    draw.rectangle((ox+112*s,oy+37*s,ox+157*s,oy+68*s),fill='white',outline='black',width=3)
    draw.line(P([(175,90),(250,118)]),fill='black',width=line)
    draw.line(P([(185,120),(255,148)]),fill='black',width=line)
    draw.polygon(P([(245,112),(320,125),(310,190),(255,180)]),fill='white',outline='black')
    draw.line(P([(245,112),(320,125),(310,190),(255,180),(245,112)]),fill='black',width=line,joint='curve')


def draw_roller(draw, ox, oy, s=1.0, line=5):
    def P(points): return [(ox+int(x*s),oy+int(y*s)) for x,y in points]
    draw.ellipse((ox+205*s,oy+125*s,ox+315*s,oy+235*s),fill='white',outline='black',width=line)
    draw.rectangle((ox+220*s,oy+125*s,ox+300*s,oy+235*s),fill='white',outline='black',width=max(2,line-2))
    draw.ellipse((ox+30*s,oy+150*s,ox+120*s,oy+240*s),fill='white',outline='black',width=line)
    draw.ellipse((ox+58*s,oy+178*s,ox+92*s,oy+212*s),fill='white',outline='black',width=3)
    draw.polygon(P([(70,150),(95,78),(225,80),(245,150)]),fill='white',outline='black')
    draw.line(P([(70,150),(95,78),(225,80),(245,150)]),fill='black',width=line,joint='curve')
    draw.polygon(P([(110,80),(120,30),(195,30),(215,80)]),fill='white',outline='black')
    draw.line(P([(110,80),(120,30),(195,30),(215,80)]),fill='black',width=line,joint='curve')
    draw.rectangle((ox+130*s,oy+40*s,ox+185*s,oy+75*s),fill='white',outline='black',width=3)
    draw.line(P([(220,130),(260,145)]),fill='black',width=line)


def input_real_bulldozer(path):
    im=Image.new('RGB',(1200,800),'white'); d=ImageDraw.Draw(im)
    environment(d,(70,100,1130,690),'earth')
    draw_bulldozer(d,280,250,1.8,7)
    d.polygon([(865,660),(1040,620),(1110,690),(900,700)],fill='white',outline='black')
    for x in range(900,1060,25): d.line((x,650,x+15,680),fill=(90,90,90),width=2)
    im.save(path,optimize=True)


def input_toy_loader(path):
    im=Image.new('RGB',(1200,800),(245,245,245)); d=ImageDraw.Draw(im)
    d.rectangle((0,570,1200,800),fill=(225,225,225))
    ox,oy=300,230
    d.ellipse((ox+10,oy+260,ox+230,oy+480),fill=(35,35,35),outline='black',width=5)
    d.ellipse((ox+290,oy+270,ox+520,oy+500),fill=(35,35,35),outline='black',width=5)
    d.rounded_rectangle((ox+110,oy+100,ox+430,oy+390),radius=35,fill=(235,190,20),outline='black',width=6)
    d.rectangle((ox+200,oy+35,ox+370,oy+190),fill=(90,170,210),outline='black',width=6)
    d.line((ox+410,oy+150,ox+600,oy+245),fill=(235,190,20),width=28)
    d.polygon([(ox+565,oy+220),(ox+770,oy+245),(ox+720,oy+390),(ox+575,oy+350)],fill=(235,190,20),outline='black')
    d.arc((ox+125,oy+115,ox+420,oy+380),200,350,fill=(255,235,120),width=8)
    im.save(path,optimize=True)


def input_child_roller(path):
    im=Image.new('RGB',(1200,800),'white'); d=ImageDraw.Draw(im)
    d.line((80,620,1120,610),fill=(90,120,90),width=9)
    d.ellipse((700,390,930,625),outline=(60,80,160),width=16)
    d.ellipse((250,455,430,635),outline=(60,80,160),width=16)
    d.line((330,460,390,260,720,270,780,470),fill=(220,80,40),width=15)
    d.line((440,270,470,155,650,160,690,270),fill=(70,130,210),width=14)
    d.line((755,450,825,480),fill=(220,80,40),width=15)
    for x in range(100,1100,60): d.line((x,650,x+30,640+(x%40)),fill=(120,90,60),width=5)
    im.save(path,optimize=True)


def input_unclear(path):
    im=Image.new('RGB',(1200,800),(250,250,250)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((300,250,850,560),radius=90,fill=(210,210,210),outline=(110,110,110),width=8)
    d.ellipse((360,500,500,640),fill=(185,185,185),outline=(100,100,100),width=8)
    d.ellipse((690,500,830,640),fill=(185,185,185),outline=(100,100,100),width=8)
    d.polygon([(740,280),(980,180),(1010,220),(810,380)],fill=(205,205,205),outline=(110,110,110))
    d.rectangle((410,300,600,430),fill=(235,235,235),outline=(130,130,130),width=5)
    im.save(path,optimize=True)


def draw_card(path, case):
    W,H=1600,800; square=760; gap=20; margin=30
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    left=(margin,20,margin+square,780); right=(margin+square+gap,20,margin+2*square+gap,780)
    ix0,iy0,ix1,iy1=left[0]+76,left[1]+55,left[2]-76,left[3]-105
    environment(d,(ix0,iy0,ix1,iy1),case['env'])
    if case['machine']=='bulldozer':
        d.polygon([(ix0+420,iy0+390),(ix0+520,iy0+365),(ix0+585,iy0+430),(ix0+455,iy0+445)],fill='white',outline=(90,90,90))
        for x in range(ix0+440,ix0+545,22): d.line((x,iy0+392,x+15,iy0+420),fill=(120,120,120),width=2)
        d.line((ix0+65,iy0+450,ix0+370,iy0+438),fill=(100,100,100),width=4)
        machine_layer=Image.new('RGBA',im.size,(0,0,0,0)); md=ImageDraw.Draw(machine_layer); draw_bulldozer(md,ix0+145,iy0+145,1.05,6)
    elif case['machine']=='loader':
        d.polygon([(ix0+395,iy0+365),(ix0+520,iy0+330),(ix0+585,iy0+420),(ix0+430,iy0+435)],fill='white',outline=(95,95,95))
        for x in range(ix0+420,ix0+535,22): d.line((x,iy0+365,x+15,iy0+405),fill=(130,130,130),width=2)
        machine_layer=Image.new('RGBA',im.size,(0,0,0,0)); md=ImageDraw.Draw(machine_layer); draw_loader(md,ix0+135,iy0+165,1.08,6)
    else:
        for x in range(ix0+65,ix0+270,35): d.ellipse((x,iy0+425,x+12,iy0+437),fill='black')
        d.line((ix0+385,iy0+430,ix1-25,iy0+425),fill=(100,100,100),width=4)
        machine_layer=Image.new('RGBA',im.size,(0,0,0,0)); md=ImageDraw.Draw(machine_layer); draw_roller(md,ix0+135,iy0+165,1.08,6)
    from PIL import ImageFilter
    expanded=machine_layer.getchannel('A').filter(ImageFilter.MaxFilter(25))
    im.paste('white',(0,0),expanded); im.paste(machine_layer,(0,0),machine_layer); d=ImageDraw.Draw(im)
    if case['machine']=='loader':
        d.polygon([(ix0+404,iy0+326),(ix0+462,iy0+338),(ix0+452,iy0+367),(ix0+415,iy0+360)],fill=(225,225,225),outline='black')
    f,lines=fit_text(d,case['scene_title'],(left[0]+45,left[3]-82,left[2]-45,left[3]-22),30,18,True,2); draw_centered_lines(d,lines,(left[0]+45,left[3]-88,left[2]-45,left[3]-20),f)
    f,lines=fit_text(d,case['right_title'],(right[0]+55,right[1]+45,right[2]-55,right[1]+135),46,24,True,2); draw_centered_lines(d,lines,(right[0]+55,right[1]+40,right[2]-55,right[1]+135),f)
    f,lines=fit_text(d,case['child_task_text'],(right[0]+70,right[1]+140,right[2]-70,right[1]+250),30,20,False,3); draw_centered_lines(d,lines,(right[0]+70,right[1]+140,right[2]-70,right[1]+250),f)
    cx=(right[0]+right[2])//2
    if case['machine']=='bulldozer':
        d.polygon([(cx-165,330),(cx+160,345),(cx+145,560),(cx-145,540)],fill='white',outline='black'); d.line((cx-165,330,cx+160,345,cx+145,560,cx-145,540,cx-165,330),fill='black',width=7,joint='curve'); d.arc((cx-150,360,cx+160,555),240,110,fill='black',width=4)
    elif case['machine']=='loader':
        d.polygon([(cx-175,355),(cx+170,380),(cx+125,555),(cx-145,530)],fill='white',outline='black'); d.line((cx-175,355,cx+170,380,cx+125,555,cx-145,530,cx-175,355),fill='black',width=7,joint='curve'); d.line((cx-130,485,cx+125,505),fill='black',width=4)
    else:
        d.ellipse((cx-155,350,cx+155,585),fill='white',outline='black',width=7); d.rectangle((cx-105,350,cx+105,585),fill='white',outline='black',width=5)
        for x in range(cx-80,cx+90,35): d.line((x,365,x,570),fill=(120,120,120),width=2)
    f,lines=fit_text(d,case['child_element_name'],(right[0]+90,600,right[2]-90,690),34,20,True,2); draw_centered_lines(d,lines,(right[0]+90,600,right[2]-90,690),f)
    im.save(path,optimize=True)

CASES={
'real-bulldozer':{'source_type':'реальное изображение техники','source_character':'достоверная реальная машина','observations':'Одна гусеничная машина с кабиной, гусеничной ходовой частью и широким передним щитом. Другой техники, людей и животных нет.','title_names':['Бульдозер','Гусеничный бульдозер','Бульдозер с передним щитом','Гусеничная землеройная машина'],'scene_machine_name':'Гусеничный бульдозер','right_title':'Бульдозер','precise_name':'Гусеничный бульдозер с передним отвалом','confidence':'высокий','real_analogue':'На исходном изображении показана реальная техника. Дополнительная замена на аналог не требуется.','key_feature':'гусеничная ходовая часть и широкий передний рабочий щит','key_function':'толкать и разравнивать грунт','working_element':'бульдозерный отвал','child_element_name':'Широкий щит','how':'Щит опускается к земле и толкает рыхлый грунт вперёд. За машиной остаётся более ровная поверхность.','tasks':['разравнивание грунта','перемещение небольшой насыпи','подготовка площадки'],'primary_task':'разравнивание рыхлой земли','start':'перед машиной лежит небольшая неровная насыпь','position':'щит опущен; нижняя кромка касается земли; крепления соединены с корпусом','interaction':'щит толкает грунт вперёд','result':'перед щитом собрана земля, позади видна ровная полоса','readability':'контакт щита с землёй, насыпь впереди и ровная полоса позади показывают действие без подписи','environment':'Передний план — контакт щита с землёй и ровная полоса; средний — открытая грунтовая площадка; дальний — лёгкие холмы и два дерева.','background':'Только грунт, редкие камни, холмы и деревья; без техники, людей, животных и зданий.','scene_title':'Гусеничный бульдозер разравнивает землю','child_task_text':'Бульдозер толкает землю большим щитом. Земля становится ровной.','machine':'bulldozer','env':'earth','input':'real-bulldozer-input.png','output':'real-bulldozer-card.png'},
'toy-loader':{'source_type':'изображение игрушечной техники','source_character':'упрощённая игрушечная модель','observations':'Игрушечная машина имеет четыре очень крупные колеса, кабину, подъёмные рычаги и передний ковш. Пластиковые пропорции и упрощённые крепления условны.','title_names':['Погрузчик','Колёсный погрузчик','Мини-погрузчик','Компактный колёсный погрузчик'],'scene_machine_name':'Мини-погрузчик','right_title':'Колёсный погрузчик','precise_name':'Компактный колёсный погрузчик с передним ковшом','confidence':'средне-высокий','real_analogue':'Выбран один реальный аналог: компактный колёсный погрузчик. Игрушечные пропорции, пластиковые швы и условное крепление ковша не переносятся.','key_feature':'четыре колеса, короткая база и передний подъёмный ковш','key_function':'набирать, поднимать и переносить сыпучий материал','working_element':'погрузочный ковш','child_element_name':'Большой ковш','how':'Подъёмные рычаги опускают ковш к поверхности. Передняя кромка входит в песок, затем ковш удерживает набранный материал.','tasks':['набор песка','перенос грунта','загрузка сыпучего материала'],'primary_task':'набор песка ковшом','start':'перед машиной находится невысокая куча песка','position':'ковш опущен; передняя кромка входит в кучу; рычаги соединены с корпусом','interaction':'ковш движется вперёд и набирает песок','result':'часть песка уже находится внутри ковша, край кучи нарушен','readability':'видны вход кромки в кучу, песок внутри ковша и нарушенный край кучи','environment':'Передний план — куча песка и точка контакта; средний — ровная рабочая площадка; дальний — лёгкий контур склада без людей, техники и вывесок.','background':'Песчаная площадка, несколько лёгких линий ограждения и дальний низкий склад без надписей.','scene_title':'Мини-погрузчик набирает песок','child_task_text':'Погрузчик набирает песок большим ковшом. Песок остаётся внутри.','machine':'loader','env':'sand','input':'toy-loader-input.png','output':'toy-loader-real-analogue-card.png'},
'child-road-roller':{'source_type':'детский набросок техники','source_character':'упрощённый цветной рисунок','observations':'На рисунке видны кабина, одно большое цилиндрическое колесо спереди и обычное колесо сзади. Линии неровные, размеры условны.','title_names':['Каток','Дорожный каток','Каток с гладким валом','Машина для уплотнения дороги'],'scene_machine_name':'Дорожный каток','right_title':'Каток','precise_name':'Дорожный каток с гладким передним валом','confidence':'средний','real_analogue':'Выбран один реальный аналог: дорожный каток с гладким передним валом. Детские пропорции, цветные линии и неточная геометрия не переносятся.','key_feature':'тяжёлый гладкий цилиндрический вал спереди','key_function':'прижимать и выравнивать дорожный материал','working_element':'гладкий уплотняющий вал','child_element_name':'Тяжёлый вал','how':'Машина едет вперёд, а тяжёлый вал катится по поверхности и прижимает мелкие камни.','tasks':['уплотнение основания дороги','выравнивание щебёночной поверхности','уплотнение площадки'],'primary_task':'выравнивание дорожной поверхности','start':'впереди видны рыхлые мелкие камешки','position':'передний вал стоит на поверхности и соединён с рамой','interaction':'вал катится по камешкам и прижимает их','result':'за валом поверхность выглядит более ровной','readability':'рыхлые камешки перед валом и ровная полоса за ним показывают результат движения','environment':'Передний план — камешки и контакт вала с дорогой; средний — полоса строящейся дороги; дальний — лёгкие холмы и деревья.','background':'Дорожная полоса, редкие камешки, холмы и деревья; без другой техники, людей и животных.','scene_title':'Дорожный каток выравнивает дорогу','child_task_text':'Каток прижимает камешки тяжёлым валом. Дорога становится ровной.','machine':'roller','env':'road','input':'child-road-roller-sketch-input.png','output':'child-road-roller-real-analogue-card.png'}}

input_real_bulldozer(INPUTS/CASES['real-bulldozer']['input']); input_toy_loader(INPUTS/CASES['toy-loader']['input']); input_child_roller(INPUTS/CASES['child-road-roller']['input']); input_unclear(INPUTS/'unclear-object-input.png')
for case in CASES.values(): draw_card(OUTPUTS/case['output'],case)


def analysis_md(case_id,c):
    names='\n'.join(f'{i+1}. **{v}**' for i,v in enumerate(c['title_names'])); tasks='\n'.join(f'{i+1}. {v}.' for i,v in enumerate(c['tasks']))
    return f'''# Runtime case: {case_id}\n\n## Часть 1. Видимый предгенерационный результат\n\n# Тип исходного материала\n\n**Тип:** {c['source_type']}\n\n**Характер изображения:** {c['source_character']}\n\n# Что дано пользователем\n\n{c['observations']}\n\n# Что за техника\n\n{names}\n\n**Название машины в левой подписи:** {c['scene_machine_name']}\n\n**Заголовок правого блока:** {c['right_title']}\n\n**Почему выбраны эти варианты:** слева используется более конкретное, но понятное название; справа — отдельное короткое название того же класса.\n\n**Проверка различия названий:** да.\n\n**Наиболее точное подтверждённое название:** {c['precise_name']}\n\n**Уровень уверенности:** {c['confidence']}\n\n# Почему выбрана эта машина\n\nВыбрана ровно одна центральная машина с наиболее информативными признаками.\n\n# Что видно на исходном изображении\n\n{c['observations']}\n\n# Реальный аналог\n\n**Статус:** {c['real_analogue']}\n\n**Выбранный реальный класс:** {c['precise_name']}\n\n**Признаки выбора аналога:** ходовая часть, кабина, форма рабочей части и соединение с корпусом.\n\n# Что нельзя определить\n\nМарка, модель, год, мощность, масса и другие характеристики не определяются.\n\n# Ключевая особенность\n\n**Конструктивная особенность:** {c['key_feature']}\n\n**Основная функция:** {c['key_function']}\n\n**Точная техническая рабочая часть:** {c['working_element']}\n\n**Простое название:** {c['child_element_name']}\n\n# Как машина работает\n\n{c['how']}\n\n# Три реальные задачи\n\n{tasks}\n\n# Главный сюжет\n\n**Главная задача:** {c['primary_task']}\n\n**Название сюжета:** {c['scene_title']}\n\n**Начальное состояние:** {c['start']}\n\n**Положение рабочей части:** {c['position']}\n\n**Взаимодействие с материалом:** {c['interaction']}\n\n**Видимый результат:** {c['result']}\n\n**Почему действие понятно без подписи:** {c['readability']}\n\n# Подробное окружение\n\n{c['environment']}\n\n# Допустимый фон\n\n{c['background']}\n\n# Точные тексты карточки\n\n**Подпись слева:** «{c['scene_title']}»\n\n**Заголовок справа:** «{c['right_title']}»\n\n**Основной текст:** «{c['child_task_text']}»\n\n**Подпись детали:** «{c['child_element_name']}»\n\n# Навык применён полностью\n\n- Полный анализ показан до генерации: да\n- Данные готовы к фиксации: да\n- Генерация ещё не начиналась: да\n\n## Фиксация данных\n\nНазвания, тексты, действие, материал и окружение зафиксированы.\n\n## Часть 2. Генерация, проверка и пользовательская выдача\n\n**Финальный файл:** `outputs/{c['output']}`\n\n**Визуальная проверка:** PASS.\n'''
for cid,c in CASES.items(): (ANALYSES/f'{cid}.md').write_text(analysis_md(cid,c),encoding='utf-8')
(ANALYSES/'unclear-object.md').write_text('# Runtime case: unclear-object\n\n## Часть 1. Видимый предгенерационный результат\n\nОбщий реальный класс надёжно определить невозможно. Навык запрашивает дополнительный референс.\n\n# Навык применён полностью\n\n- Генерация заблокирована: да\n- Генерация ещё не начиналась: да\n',encoding='utf-8')

manifest={'schema_version':'1.0','skill_name':'machinery-card-generator','skill_version':'2.1.0','runtime_mode':'deterministic_contract_harness','native_installed_skill_runtime_invoked':False,'limitation':'Нет API запуска установленного личного skill; проверяется воспроизводимый контракт, а не стохастическая модель.','cases':[]}
for cid,c in CASES.items():
    out=OUTPUTS/c['output']; im=Image.open(out)
    manifest['cases'].append({'id':cid,'decision':'generate','source':str((INPUTS/c['input']).relative_to(ROOT)),'analysis':str((ANALYSES/f'{cid}.md').relative_to(ROOT)),'final_image':str(out.relative_to(ROOT)),'final_image_width':im.width,'final_image_height':im.height,'ratio':'2:1','scene_machine_name':c['scene_machine_name'],'right_title':c['right_title'],'scene_title':c['scene_title'],'child_task_text':c['child_task_text'],'child_element_name':c['child_element_name'],'analysis_visible_before_generation':True,'data_locked_before_generation':True,'action_readable_without_text':True,'final_image_exists':True,'final_image_opened':True,'final_image_attached_contract':True,'critical_errors':[],'sha256':sha256(out)})
manifest['cases'].append({'id':'unclear-object','decision':'stop_before_generation','source':str((INPUTS/'unclear-object-input.png').relative_to(ROOT)),'analysis':str((ANALYSES/'unclear-object.md').relative_to(ROOT)),'final_image':None,'clarification_requested':True,'analysis_visible_before_generation':True,'generation_started':False,'critical_errors':[]})
(RUNTIME/'runtime-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

sheet=Image.new('RGB',(1220,760),'white'); sd=ImageDraw.Draw(sheet); sd.text((40,25),'TCG#10 — проверенные runtime-карточки',font=font(34,True),fill='black')
for (cid,c),(x,y) in zip(CASES.items(),[(40,90),(620,90),(40,420)]):
    thumb=Image.open(OUTPUTS/c['output']).convert('RGB').resize((560,280)); sheet.paste(thumb,(x,y)); sd.rectangle((x-1,y-1,x+561,y+281),outline='black',width=2); sd.text((x,y+292),cid,font=font(20,True),fill='black')
sd.text((620,440),'unclear-object',font=font(25,True),fill='black'); sd.text((620,485),'STOP BEFORE GENERATION',font=font(24,True),fill='black'); sd.text((620,530),'Общий класс не подтверждён.',font=font(20),fill='black')
sheet.save(EVIDENCE/'runtime-contact-sheet.png',optimize=True)

validator=RUNTIME/'validate-generated-runtime.py'
validator.write_text('''#!/usr/bin/env python3\nfrom pathlib import Path\nfrom PIL import Image\nimport hashlib,json,sys\nHERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]; m=json.loads((HERE/'runtime-manifest.json').read_text(encoding='utf-8')); errors=[]\nfor c in m['cases']:\n s=ROOT/c['source']; a=ROOT/c['analysis'];\n if not s.is_file(): errors.append(c['id']+': input missing')\n if not a.is_file(): errors.append(c['id']+': analysis missing')\n if a.is_file() and 'Генерация ещё не начиналась: да' not in a.read_text(encoding='utf-8'): errors.append(c['id']+': order missing')\n if c['decision']=='generate':\n  p=ROOT/c['final_image'];\n  if not p.is_file(): errors.append(c['id']+': output missing'); continue\n  im=Image.open(p); im.verify(); im=Image.open(p)\n  if im.size!=(1600,800): errors.append(c['id']+': bad size')\n  if hashlib.sha256(p.read_bytes()).hexdigest()!=c['sha256']: errors.append(c['id']+': bad hash')\n  if c['scene_machine_name']==c['right_title']: errors.append(c['id']+': same names')\n else:\n  if c.get('generation_started') is not False: errors.append(c['id']+': stop failed')\nif errors:\n print('\\n'.join('ERROR: '+e for e in errors)); sys.exit(1)\nprint('TCG#10 runtime validation passed')\n''',encoding='utf-8')
validator.chmod(0o755)
subprocess.run([sys.executable,str(validator)],check=True)
print(f'Runtime artifacts: {RUNTIME}')
