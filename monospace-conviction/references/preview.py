#!/usr/bin/env python3
"""
monospace-conviction preview — block elements, braille, powerline, half-block AA
Run: python3 preview.py
"""
import math, re

def rgb(r,g,b): return f'\033[38;2;{r};{g};{b}m'
def fg(n):      return f'\033[38;5;{n}m'
def bg(n):      return f'\033[48;5;{n}m'
N='\033[0m'; B='\033[1m'

HC_L=''; HC_R=''; PL=''  # U+E0B6, U+E0B4, U+E0B0

vis = lambda s: len(re.sub(r'\033\[[^m]*m','',s))
pad = lambda s,w: s+' '*max(0,w-vis(s))

# ── arc: quarter-circle with ▀▄ boundary anti-aliasing ──────────────────────
# key formula: pixel_x=col/2, pixel_y=row (not row*2 — that breaks aspect ratio)
# physical: 2R cols × R rows × 2 units/row = square → circle looks round
def make_arc(R=9):
    rows=[]
    for dy in range(R):
        row=''
        for px in range(R*2):
            x=px/2.0; yt=float(dy); yb=dy+0.5
            dt=math.sqrt(x*x+yt*yt); db=math.sqrt(x*x+yb*yb)
            it=dt<R-.05; ib=db<R-.05
            def c(d):
                t=min(d,R)/R
                return int(30+t*60),int(80+t*100),int(220-t*90)
            if it and ib: r,g2,b=c((yt+yb)/2); row+=rgb(r,g2,b)+'█'+N
            elif it:      r,g2,b=c(yt);         row+=rgb(r,g2,b)+'▀'+N
            elif ib:      r,g2,b=c(yb);         row+=rgb(r,g2,b)+'▄'+N
            else:         row+=' '
        rows.append(row)
    return rows  # 18w × 9h

# ── gem: diamond with per-pixel radial diffuse + specular lighting ───────────
def make_gem(SZ=9):
    W=SZ+1; rows=[]
    for dy in range(W):
        row=''
        for px in range(W*2):
            def ind(px,py): return abs(px-SZ)+abs(py-SZ)<=SZ
            def col(px,py):
                cx=(px-SZ)/float(SZ); cy=(py-SZ)/float(SZ)
                r2=math.sqrt(cx*cx+cy*cy)
                nx=cx/r2 if r2>.01 else 0; ny=cy/r2 if r2>.01 else 0
                diff=max(0,-(nx*.7+ny*.7))
                spec=max(0,-(nx*.8+ny*.8))**12
                edge=max(0,1-r2)**.4
                ang=math.atan2(cy,cx); fac=math.sin(ang*4)*.5+.5
                br=30+int(fac*40); bg2=60+int(fac*30); bb=180+int(fac*40)
                t=diff*.7+edge*.3
                return (min(255,int(br+t*160+spec*255)),
                        min(255,int(bg2+t*100+spec*220)),
                        min(255,int(bb+t*40+spec*255)))
            pt=dy*2; pb=dy*2+1
            tp=ind(px,pt); bt=ind(px,pb)
            if tp and bt: r,g2,b=col(px,pt); row+=rgb(r,g2,b)+'█'+N
            elif tp:      r,g2,b=col(px,pt); row+=rgb(r,g2,b)+'▀'+N
            elif bt:      r,g2,b=col(px,pb); row+=rgb(r,g2,b)+'▄'+N
            else:         row+=' '
        rows.append(row)
    return rows  # 20w × 10h

# ── sparklines: ▁▂▃▄▅▆▇█ eighths, 4 channels ────────────────────────────────
def make_sparks(W=54):
    bars='▁▂▃▄▅▆▇█'
    chs=[
        ('cpu',lambda x:math.sin(x*3.7)*.5+math.sin(x*11)*.3+.4,  60,200,80),
        ('mem',lambda x:.3+x*.35+math.sin(x*7)*.08,                90,130,255),
        ('net',lambda x:max(0,math.sin(x*5)**3)*.9+math.sin(x*17)*.08, 255,130,50),
        ('lat',lambda x:abs(math.sin(x*6))*.4+math.sin(x*13)*.15+.1,  200,70,190),
    ]
    rows=[]
    for lbl,fn,cr,cg,cb in chs:
        row=fg(245)+lbl+N+' '
        for i in range(W):
            t=i/W; v=max(0,min(1,fn(t))); iv=.4+v*.6
            row+=rgb(int(cr*iv),int(cg*iv),int(cb*iv))+bars[int(v*7.99)]+N
        rows.append(row)
    return rows

# ── braille: 8-dot density gradient, U+2800 range ───────────────────────────
def make_braille(W=58):
    masks=[0x00,0x01,0x09,0x19,0x59,0xD9,0xFB,0xFF]
    pals=[((20,80,200),(60,200,140)),((180,50,90),(80,90,230))]
    rows=[]
    for (r1,g1,b1),(r2,g2,b2) in pals:
        row=''
        for i in range(W):
            t=i/(W-1); lvl=int(t*7)
            r=int(r1+t*(r2-r1)); g=int(g1+t*(g2-g1)); b=int(b1+t*(b2-b1))
            row+=rgb(r,g,b)+chr(0x2800+masks[lvl])+N
        rows.append(row)
    return rows

# ── shading: ░▒▓█ + truecolor gradient ──────────────────────────────────────
def make_shading(W=58):
    sh='░▒▓█'
    row=''
    for i in range(W):
        t=i/(W-1)
        row+=rgb(int(20+t*200),int(20+t*60),int(180-t*100))+sh[int(t*3.99)]+N
    return row

# ─────────────────────────────────────────────────────────────────────────────

def main():
    AR=make_arc(9); GE=make_gem(9)
    SP=make_sparks(54); BR=make_braille(58); SH=make_shading(58)

    print()

    # powerline title bar
    segs=[(57,255,' monospace·conviction '),
          (237,141,' nerd fonts · block art '),
          (239,245,' ▀▄ aa · gem · sparklines ')]
    line='  '; prev=None
    for i,(bgn,fgn,txt) in enumerate(segs):
        if i==0: line+=fg(bgn)+HC_L+N
        else:    line+=bg(bgn)+fg(prev)+PL+N
        line+=bg(bgn)+fg(fgn)+B+txt+N; prev=bgn
    print(line+fg(prev)+HC_R+N)
    print()

    # arc + gem side by side
    AW=18; GAP=6
    print('  '+pad(fg(245)+'arc — ▀▄ boundary aa, R=9'+N, AW+GAP+2)+fg(245)+'gem — radial diffuse + specular'+N)
    for i in range(max(len(AR),len(GE))):
        ar=AR[i] if i<len(AR) else ''
        gr=GE[i] if i<len(GE) else ''
        print('  '+pad(ar,AW)+'  '+' '*GAP+gr)

    print()
    print('  '+fg(245)+'sparklines — ▁▂▃▄▅▆▇█ eighths'+N)
    for row in SP: print('  '+row)

    print()
    print('  '+fg(245)+'braille density — U+2800 8-dot cells'+N)
    for row in BR: print('  '+row)

    print()
    print('  '+fg(245)+'shading depth — ░▒▓█ + truecolor gradient'+N)
    print('  '+SH)

    print()
    print('  '+fg(245)+'borders — light · heavy · rounded'+N)
    specs=[('┌┐└┘─│',250,'light'),('┏┓┗┛━┃',75,' heavy'),('╭╮╰╯─│',141,' round')]
    W3=12; top=mid=bot=''
    for ch,col,lbl in specs:
        tl,tr,bl,br,h,v=ch
        top+=fg(col)+tl+h*(W3-2)+tr+N+'  '
        mid+=fg(col)+v+N+f' {lbl:<{W3-4}} '+fg(col)+v+N+'  '
        bot+=fg(col)+bl+h*(W3-2)+br+N+'  '
    print('  '+top); print('  '+mid); print('  '+bot)
    print()

if __name__=='__main__':
    main()
