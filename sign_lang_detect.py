"""
╔══════════════════════════════════════════════════════════════╗
║   ASL Sign Language Detector — Full A-Z + Common Phrases    ║
║   INSTALL: pip install opencv-python==4.8.1.78              ║
║            pip install mediapipe==0.10.9 numpy==1.26.4      ║
║   RUN:     python sign_lang_detect.py                        ║
║   KEYS:    Q=Quit  C=Clear  Backspace=Delete  H=CheatSheet  ║
╚══════════════════════════════════════════════════════════════╝
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque

mp_hands  = mp.solutions.hands
mp_draw   = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

WRIST=0
THUMB_CMC=1;THUMB_MCP=2;THUMB_IP=3;THUMB_TIP=4
INDEX_MCP=5;INDEX_PIP=6;INDEX_DIP=7;INDEX_TIP=8
MID_MCP=9;MID_PIP=10;MID_DIP=11;MID_TIP=12
RING_MCP=13;RING_PIP=14;RING_DIP=15;RING_TIP=16
PINK_MCP=17;PINK_PIP=18;PINK_DIP=19;PINK_TIP=20

def lm(lms,i):
    p=lms.landmark[i]; return np.array([p.x,p.y,p.z])
def up(lms,tip_i,pip_i):
    return lm(lms,tip_i)[1]<lm(lms,pip_i)[1]
def down(lms,tip_i,pip_i):
    return lm(lms,tip_i)[1]>lm(lms,pip_i)[1]
def d(lms,a,b):
    return float(np.linalg.norm(lm(lms,a)-lm(lms,b)))
def thumb_ext(lms,hand):
    t=lm(lms,THUMB_TIP);ip=lm(lms,THUMB_IP)
    return t[0]<ip[0] if hand=="Right" else t[0]>ip[0]
def thumb_down(lms):
    return lm(lms,THUMB_TIP)[1]>lm(lms,WRIST)[1]+0.05
def spread(lms):
    return d(lms,INDEX_TIP,MID_TIP)>0.06 and d(lms,MID_TIP,RING_TIP)>0.06
def all_curled(lms):
    return (down(lms,INDEX_TIP,INDEX_PIP) and down(lms,MID_TIP,MID_PIP)
            and down(lms,RING_TIP,RING_PIP) and down(lms,PINK_TIP,PINK_PIP))

def classify(lms, hand):
    T=thumb_ext(lms,hand)
    I=up(lms,INDEX_TIP,INDEX_PIP)
    M=up(lms,MID_TIP,MID_PIP)
    R=up(lms,RING_TIP,RING_PIP)
    P=up(lms,PINK_TIP,PINK_PIP)

    ti=d(lms,THUMB_TIP,INDEX_TIP)
    tm=d(lms,THUMB_TIP,MID_TIP)
    tr=d(lms,THUMB_TIP,RING_TIP)
    tp=d(lms,THUMB_TIP,PINK_TIP)
    im=d(lms,INDEX_TIP,MID_TIP)
    mr=d(lms,MID_TIP,RING_TIP)

    wy=lm(lms,WRIST)[1]
    iy=lm(lms,INDEX_TIP)[1]
    ix=lm(lms,INDEX_TIP)[0]
    imx=lm(lms,INDEX_MCP)[0]

    # ── PHRASES (priority) ───────────────────────────────────
    if T and I and not M and not R and P:           return "I LOVE YOU"
    if T and I and M and R and P and spread(lms):   return "HELLO"
    if T and not I and not M and not R and not P:
        return "BAD" if thumb_down(lms) else "GOOD"
    if ti<0.05 and not I and M and R and P:         return "OK"
    if T and I and M and R and P and not spread(lms): return "STOP"
    if all_curled(lms) and not T and ti<0.08:       return "YES"
    if I and M and not R and not P and not T and im<0.03 and abs(ix-imx)>0.08:
                                                     return "NO"
    if ti<0.05 and not I and not M and not R and not P: return "MORE"
    if all_curled(lms) and not T:                   return "SORRY"
    if ti<0.06 and tm<0.06 and not R and not P:     return "EAT"
    if not T and I and M and R and not P:           return "WATER"
    if T and I and M and R and not P:               return "HELP"
    if T and not I and not M and not R and P:       return "WHY"
    if I and not M and not R and not P and not T and iy<wy-0.1: return "WHERE"

    # ── LETTERS A–Z ──────────────────────────────────────────
    # A — fist + thumb alongside
    if not I and not M and not R and not P and T:   return "A"

    # B — 4 fingers up, thumb folded
    if not T and I and M and R and P:               return "B"

    # C — curved partial close
    if not I and not M and not R and not P and not T:
        if 0.06<ti<0.15 and 0.06<tm<0.15:          return "C"

    # D — index up, thumb touches middle
    if I and not M and not R and not P and tm<0.06 and not T: return "D"

    # E — claw, all curled touching thumb
    if not I and not M and not R and not P and not T:
        if ti<0.07 and tm<0.08:                     return "E"

    # F — index+thumb circle, 3 fingers up
    if ti<0.05 and not I and M and R and P:         return "F"

    # G — index pointing sideways
    if I and not M and not R and not P and not T:
        if abs(ix-imx)>0.09:                        return "G"

    # H — index+middle sideways together
    if I and M and not R and not P and not T:
        if im<0.04 and abs(ix-imx)>0.07:            return "H"

    # I — pinky only
    if not I and not M and not R and P and not T:   return "I"

    # K — index+middle up, thumb between
    if I and M and not R and not P and T and im<0.07: return "K"

    # L — index up + thumb out
    if I and not M and not R and not P and T and not thumb_down(lms): return "L"

    # M — 3 fingers over thumb
    if not I and not M and not R and not P and not T and ti<0.05: return "M"

    # N — 2 fingers over thumb
    if not I and not M and not R and not P and not T and ti<0.07 and tm<0.07: return "N"

    # O — O shape
    if not I and not M and not R and not P and not T and 0.04<ti<0.09: return "O"

    # P — like K but pointing down
    if I and M and not R and not P and T and iy>wy: return "P"

    # Q — index down + not thumb
    if I and not M and not R and not P and not T and iy>wy: return "Q"

    # R — index+middle crossed (very close)
    if I and M and not R and not P and not T and im<0.025: return "R"

    # S — plain fist
    if not I and not M and not R and not P and not T: return "S"

    # T — thumb between index+middle
    if not I and not M and not R and not P and T and ti<0.07: return "T"

    # U — index+middle up, held together
    if I and M and not R and not P and not T and im<0.04: return "U"

    # V — peace sign, spread
    if I and M and not R and not P and not T and im>=0.04: return "V"

    # W — index+middle+ring up
    if not T and I and M and R and not P:           return "W"

    # X — index hooked
    if not M and not R and not P and not T:
        xt=lm(lms,INDEX_TIP)[1]; xp=lm(lms,INDEX_PIP)[1]; xm=lm(lms,INDEX_MCP)[1]
        if xt>xp and xp<xm:                         return "X"

    # Y — thumb+pinky out
    if T and not I and not M and not R and P:       return "Y"

    # Z — index horizontal (pointing side)
    if I and not M and not R and not P and not T and abs(ix-imx)>0.05: return "Z"

    return None


class SentenceBuilder:
    WORDS={"HELLO","I LOVE YOU","GOOD","BAD","OK","STOP","YES","NO",
           "MORE","SORRY","EAT","WATER","HELP","WHERE","WHAT","WHY","MY","YOU"}

    def __init__(self,hold=20,lgap=1.8,wgap=3.5):
        self.hold=hold;self.lgap=lgap;self.wgap=wgap
        self.sentence=[];self.word=[];self.last=None;self.count=0;self.t=time.time()

    def update(self,sign):
        now=time.time();gap=now-self.t
        if sign is None:
            self.count=0
            if gap>self.wgap and self.word:
                self.sentence.append("".join(self.word));self.word=[]
            return
        self.count=self.count+1 if sign==self.last else 1
        self.last=sign
        if self.count==self.hold:
            self.t=now;self.count=0
            if sign in self.WORDS:
                if self.word: self.sentence.append("".join(self.word));self.word=[]
                self.sentence.append(sign)
            else: self.word.append(sign)

    @property
    def text(self):
        p=list(self.sentence)
        if self.word: p.append("".join(self.word))
        return " ".join(p)

    @property
    def stability(self): return min(self.count/max(self.hold,1),1.0)

    def clear(self): self.sentence.clear();self.word.clear();self.last=None;self.count=0
    def backspace(self):
        if self.word: self.word.pop()
        elif self.sentence: self.word=list(self.sentence.pop())
    def space(self):
        if self.word: self.sentence.append("".join(self.word));self.word=[]


CHEAT=[
    "A=fist+thumb    B=4fingers     C=curved       D=index+tmid",
    "E=claw          F=circle+3up   G=gun-sideways H=2-sideways",
    "I=pinky         K=2+thumb      L=L-shape      M=3overThumb",
    "N=2overThumb    O=O-circle     P=K-down       Q=index-down",
    "R=2-crossed     S=plain fist   T=thumbBetween U=2-together",
    "V=peace-spread  W=3-up         X=hook-index   Y=thumb+pink",
    "Z=index-horiz   ---PHRASES---",
    "HELLO=open+sprd GOOD=thumbUp   BAD=thumbDown  OK=circle+3",
    "STOP=palm-flat  YES=fist       NO=2-sideways  MORE=pinch",
    "SORRY=fist-rot  EAT=fingersPinch WATER=W      HELP=T+flat",
    "I_LOVE_YOU=Y+I  WHERE=indexHi  WHY=Y-shape",
]

def blend(img,x1,y1,x2,y2,col,alpha=0.75):
    ov=img.copy();cv2.rectangle(ov,(x1,y1),(x2,y2),col,-1)
    cv2.addWeighted(ov,alpha,img,1-alpha,0,img)

def draw_ui(frame,sign,b,fps,cheat):
    h,w=frame.shape[:2]
    blend(frame,0,0,w,118,(15,15,15))
    cv2.putText(frame,f"FPS {fps:.0f}",(w-115,26),cv2.FONT_HERSHEY_SIMPLEX,0.58,(100,100,100),1)
    sc=(50,220,100) if sign else (100,100,100)
    cv2.putText(frame,"SIGN:",(14,36),cv2.FONT_HERSHEY_SIMPLEX,0.65,(130,130,130),1)
    cv2.putText(frame,sign or "—",(94,36),cv2.FONT_HERSHEY_SIMPLEX,0.95,sc,2)
    cv2.putText(frame,"WORD:",(14,73),cv2.FONT_HERSHEY_SIMPLEX,0.6,(130,130,130),1)
    cv2.putText(frame,"".join(b.word)+"_",(94,73),cv2.FONT_HERSHEY_SIMPLEX,0.8,(50,210,255),2)
    bw=int(250*b.stability)
    cv2.rectangle(frame,(14,88),(264,103),(40,40,40),-1)
    if bw: cv2.rectangle(frame,(14,88),(14+bw,103),(255,190,0),-1)
    cv2.putText(frame,"Stability",(270,102),cv2.FONT_HERSHEY_SIMPLEX,0.4,(100,100,100),1)
    blend(frame,0,h-82,w,h,(15,15,15))
    cv2.putText(frame,"SENTENCE:",(14,h-56),cv2.FONT_HERSHEY_SIMPLEX,0.48,(100,100,100),1)
    txt=b.text;txt=("…"+txt[-59:]) if len(txt)>60 else txt
    cv2.putText(frame,txt,(14,h-22),cv2.FONT_HERSHEY_SIMPLEX,0.88,(240,240,240),2)
    cv2.putText(frame,"Q:Quit C:Clear Bksp:Del Spc:Space H:Signs",(w-440,h-8),
                cv2.FONT_HERSHEY_SIMPLEX,0.4,(90,90,90),1)
    if cheat:
        cx,cy=10,125;cw=w-20;ch=len(CHEAT)*22+28
        blend(frame,cx,cy,cx+cw,cy+ch,(20,20,20),0.88)
        cv2.rectangle(frame,(cx,cy),(cx+cw,cy+ch),(80,80,80),1)
        cv2.putText(frame,"SIGN CHEAT SHEET  (press H to hide)",(cx+10,cy+20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.55,(200,200,50),1)
        for i,line in enumerate(CHEAT):
            cv2.putText(frame,line,(cx+8,cy+42+i*22),
                        cv2.FONT_HERSHEY_SIMPLEX,0.42,(170,230,170),1)
    return frame


def main():
    print("\n"+"═"*58)
    print("  ASL Detector — Full A-Z + 20 Phrases")
    print("  Hold each sign ~0.7s to register it")
    print("  Press H in the window for cheat sheet")
    print("═"*58+"\n")
    cap=cv2.VideoCapture(0)
    if not cap.isOpened(): print("❌ Cannot open webcam"); return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    builder=SentenceBuilder();fps_buf=deque(maxlen=30);prev=time.time();cheat=False

    with mp_hands.Hands(max_num_hands=1,
                        min_detection_confidence=0.75,
                        min_tracking_confidence=0.65) as hands:
        while True:
            ret,frame=cap.read()
            if not ret: break
            frame=cv2.flip(frame,1)
            rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            res=hands.process(rgb)
            sign=None
            if res.multi_hand_landmarks:
                for hlms,hinfo in zip(res.multi_hand_landmarks,res.multi_handedness):
                    mp_draw.draw_landmarks(frame,hlms,mp_hands.HAND_CONNECTIONS,
                        mp_styles.get_default_hand_landmarks_style(),
                        mp_styles.get_default_hand_connections_style())
                    sign=classify(hlms,hinfo.classification[0].label)
            builder.update(sign)
            now=time.time();fps_buf.append(now-prev);prev=now
            fps=1.0/(sum(fps_buf)/len(fps_buf)) if fps_buf else 0
            frame=draw_ui(frame,sign,builder,fps,cheat)
            cv2.imshow("ASL Sign Language Detector",frame)
            key=cv2.waitKey(1)&0xFF
            if   key==ord('q'):   break
            elif key==ord('c'):   builder.clear()
            elif key in(8,127):   builder.backspace()
            elif key==ord(' '):   builder.space()
            elif key==ord('h'):   cheat=not cheat

    print(f'\n✅ Final sentence: "{builder.text}"')
    cap.release();cv2.destroyAllWindows()

if __name__=="__main__":
    main()