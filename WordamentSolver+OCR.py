import pyautogui
import cv2
import pytesseract
import numpy as np

print('\nRunning OCR...\n')
try:
    x, y = pyautogui.locateCenterOnScreen('hint.png', confidence=0.9)
except:
    print('Wordament screen not found!')
    import sys
    sys.exit()

# screengrab tile grid
# x,y = hintpoint
x += 100
img_raw = pyautogui.screenshot(region=(x,y, 300, 300))
# img_raw = pyautogui.screenshot('grid.png',region=(x,y, 300, 300))

# check for P's
pflag = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for xx,yy,hh,ww in pyautogui.locateAllOnScreen('p.png', region=(x,y, 300, 300), confidence=0.9):
    cox = (xx-x)/270
    coy = (yy-y)/270
    if cox<0.25:
        cox = 0
    elif cox<0.5:
        cox = 1
    elif cox<0.75:
        cox = 2
    else:
        cox = 3
    if coy<0.25:
        coy = 0
    elif coy<0.5:
        coy = 1
    elif coy<0.75:
        coy = 2
    else:
        coy = 3
    pflag[coy*4+cox] = 1

# convert to grayscale then black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

# func for image processing contrast, resize, blur, sharpen
def img_proc(image):
    image = cv2.equalizeHist(image)
    image = cv2.resize(image, (90,60))
    image = cv2.GaussianBlur(image,(5,5),0)
    filt = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, filt)
    return(image)

# crop out the 16 tiles from the tile grid screengrab
tile = []
tile.append(img_proc(img[17:59,10:70].copy()))
tile.append(img_proc(img[17:59,80:140].copy()))
tile.append(img_proc(img[17:59,160:220].copy()))
tile.append(img_proc(img[17:59,235:295].copy()))
tile.append(img_proc(img[93:135,10:70].copy()))
tile.append(img_proc(img[93:135,80:140].copy()))
tile.append(img_proc(img[93:135,160:220].copy()))
tile.append(img_proc(img[93:135,235:295].copy()))
tile.append(img_proc(img[171:213,10:70].copy()))
tile.append(img_proc(img[171:213,80:140].copy()))
tile.append(img_proc(img[171:213,160:220].copy()))
tile.append(img_proc(img[171:213,235:295].copy()))
tile.append(img_proc(img[247:289,10:70].copy()))
tile.append(img_proc(img[247:289,80:140].copy()))
tile.append(img_proc(img[247:289,160:220].copy()))
tile.append(img_proc(img[247:289,235:295].copy()))
# cv2.imwrite('tile8.png',tile[8])

# invoke tesseract for OCR
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
array = []
try:
    for i in range(16):
        if pflag[i]==0:
            array.append(pytesseract.image_to_string(tile[i], lang='eng', config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-/')[:-2].lower())
        else:
            array.append('p')
            # print('--Hardcoded a P')
except:
    pass

# dealing with I, R and under-
for i in range(16):
    if array[i]=='':
        # array[i] = pytesseract.image_to_string(tile[i], lang='eng', config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ-/')[:-2].lower()
        # print('-Replaced a null with single char detection')
        if array[i]=='':
            counter = 0
            current = 1
            for j in range(10,80):
                if current==1 and tile[i][40,j]<127:
                    counter += 1
                    current = 0
                elif current==0 and tile[i][40,j]>127:
                    counter += 1
                    current = 1
            if counter==2:
                array[i] = 'i'
                # print('--Replaced a null with I')
            else:
                array[i] = 'r'
                # print('--Replaced a null with R')
    elif array[i]=='under':
        array[i] = 'under-'

# show detected tiles
print('OCR detected the following letters:')
for i in range(4):
    print(array[i*4:i*4+4])

# check whether to proceed with manual entry instead
zz = input('Press enter to proceed, or\n' + 
            'any other key for manual entry:\n')
if zz != '':
    linein = input('Input tiles (space-delimited):\n')
    array = linein.split(' ')

# read in word list
print('\nLoading word list...')
with open('word_list.txt') as f:
    words = set(f.read().split())

# set up truncated sets for checking if further pathing is needed
trunc = []
for i in range(3,15):
    temp = [w[:i] for w in words if len(w)>i]
    trunc.append(temp)

rev_trunc = []
for i in range(3,15):
    temp = [w[-i:] for w in words if len(w)>i]
    rev_trunc.append(temp)

# define functions for adding letters in the 8 possible directions
def right(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1+1
    tcy=cy*1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def downright(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1+1
    tcy=cy*1+1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def down(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1
    tcy=cy*1+1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def downleft(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1-1
    tcy=cy*1+1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def left(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1-1
    tcy=cy*1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def upleft(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1-1
    tcy=cy*1-1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def up(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1
    tcy=cy*1-1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def upright(word,cx,cy,cary,ary,m):
    tcary=cary*1
    tcx=cx*1+1
    tcy=cy*1-1
    if tcary[tcy*4+tcx]==0:
        if m==2: # suffix mode
            tword=ary[tcy*4+tcx]+word
        else:
            tword=word+ary[tcy*4+tcx]
        tcary[tcy*4+tcx]=1
        return([tword,tcx,tcy,tcary])
    else:
        return('')

def add_letter(word,cx,cy,cary,ary,m):
    ans = []
    if cx==0 and cy==0:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(downright(word,cx,cy,cary,ary,m))>0: ans.append(downright(word,cx,cy,cary,ary,m))
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
    elif cx>0 and cx<3 and cy==0:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(downright(word,cx,cy,cary,ary,m))>0: ans.append(downright(word,cx,cy,cary,ary,m))
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
        if len(downleft(word,cx,cy,cary,ary,m))>0: ans.append(downleft(word,cx,cy,cary,ary,m))
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
    elif cx==3 and cy==0:
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
        if len(downleft(word,cx,cy,cary,ary,m))>0: ans.append(downleft(word,cx,cy,cary,ary,m))
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
    elif cx==0 and cy>0 and cy<3:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(downright(word,cx,cy,cary,ary,m))>0: ans.append(downright(word,cx,cy,cary,ary,m))
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))
        if len(upright(word,cx,cy,cary,ary,m))>0: ans.append(upright(word,cx,cy,cary,ary,m))
    elif cx>0 and cx<3 and cy>0 and cy<3:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(downright(word,cx,cy,cary,ary,m))>0: ans.append(downright(word,cx,cy,cary,ary,m))
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
        if len(downleft(word,cx,cy,cary,ary,m))>0: ans.append(downleft(word,cx,cy,cary,ary,m))
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
        if len(upleft(word,cx,cy,cary,ary,m))>0: ans.append(upleft(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))
        if len(upright(word,cx,cy,cary,ary,m))>0: ans.append(upright(word,cx,cy,cary,ary,m))
    elif cx==3 and cy>0 and cy<3:
        if len(down(word,cx,cy,cary,ary,m))>0: ans.append(down(word,cx,cy,cary,ary,m))
        if len(downleft(word,cx,cy,cary,ary,m))>0: ans.append(downleft(word,cx,cy,cary,ary,m))
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
        if len(upleft(word,cx,cy,cary,ary,m))>0: ans.append(upleft(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))
    elif cx==0 and cy==3:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))
        if len(upright(word,cx,cy,cary,ary,m))>0: ans.append(upright(word,cx,cy,cary,ary,m))
    elif cx>0 and cx<3 and cy==3:
        if len(right(word,cx,cy,cary,ary,m))>0: ans.append(right(word,cx,cy,cary,ary,m))
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
        if len(upleft(word,cx,cy,cary,ary,m))>0: ans.append(upleft(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))
        if len(upright(word,cx,cy,cary,ary,m))>0: ans.append(upright(word,cx,cy,cary,ary,m))
    elif cx==3 and cy==3:
        if len(left(word,cx,cy,cary,ary,m))>0: ans.append(left(word,cx,cy,cary,ary,m))
        if len(upleft(word,cx,cy,cary,ary,m))>0: ans.append(upleft(word,cx,cy,cary,ary,m))
        if len(up(word,cx,cy,cary,ary,m))>0: ans.append(up(word,cx,cy,cary,ary,m))

    return(ans)

# default mode = 0, i.e. path all tiles to all word lengths
mode=0
px1=0
px2=4
py1=0
py2=4

# auto-detect modes using '-' at prefix or suffix,
# or digram, or '/' for either/or, or whether corner letters identical
for i in range(4):
    for j in range(4):
        if len(array[i*4+j])>1:
            ex=j
            ey=i
            if array[i*4+j][0]=='-': # mode 2 = suffix mode
                array[i*4+j]=array[i*4+j][1:]
                mode = 2
                py1=i*1
                py2=py1+1
                px1=j*1
                px2=px1+1
            elif array[i*4+j][-1]=='-': # mode 1 = prefix mode
                array[i*4+j]=array[i*4+j][:-1]
                mode = 1
                py1=i*1
                py2=py1+1
                px1=j*1
                px2=px1+1
            elif array[i*4+j][1]=='/': # mode 4 = either/or mode
                char1=array[i*4+j][0]
                char2=array[i*4+j][-1]
                array1 = array * 1
                array1[ey*4+ex] = char1
                array2 = array * 1
                array2[ey*4+ex] = char2
                mode = 4
            else:
                digram = array[i*4+j] # mode 3 = digram mode
                mode = 3
if array[0]==array[3] and array[0]==array[12] and array[0]==array[15]:
    mode = 5 # mode 5 = corner mode

# check if searching for specific word length
# if so, assume not focusing only on special tile
pz=''
if mode==0:
    pz = input('Input target word length, or\n' + 
                'null to search all lengths:\n')
elif mode==1:
    pz = input('Input target word length, or\n' +
                '"x" to search all words, or\n' +
                'null to search prefix words only:\n')
elif mode==2:
    pz = input('Input target word length, or\n' +
                '"x" to search all words, or\n' +
                'null to search suffix words only:\n')
elif mode==3:
    pz = input('Input target word length, or\n' +
                '"x" to search all words, or\n' +
                'null to search digram only:\n')
    if pz!='': mode=0
elif mode==4:
    pz = input('Input target word length, or\n' +
                '"x" to search all words, or\n' +
                'null to search either/or only:\n')
elif mode==5:
    pz = input('Input target word length, or\n' +
                '"x" to search all words, or\n' +
                'null to search corners only:\n')
    if pz!='': mode=0

if pz=='' or pz=='x':
    minz=3
    maxz=15
else:
    minz=int(pz)
    maxz=minz

# prep output list
out = []

if mode == 2: # mode 2 = suffix mode
    for y in range(py1,py2):
        for x in range(px1,px2):
            
            print('Pathing tile {},{}...'.format(x,y))
            
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1

            chunk = [[array[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                    out.append(e[0])
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in rev_trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    if pz!='':
        mode=0 # switch back to default mode for this pass
        px1=0
        px2=4
        py1=0
        py2=4
        for y in range(py1,py2):
            for x in range(px1,px2):
                
                if x==ex and y==ey: continue
                
                print('Pathing tile {},{}...'.format(x,y))
                
                fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                fary[y*4+x]=1
                fary[ey*4+ex]=1 # no longer need to add suffix to path
        
                chunk = [[array[y*4+x],x,y,fary]]
                while len(chunk)>0:
                    e = chunk.pop(0)
                    if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                        out.append(e[0])
                    if len(e[0])<maxz:
                        if len(e[0])>2:
                            if e[0] not in trunc[len(e[0])-3]:
                                continue
                        ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                        if len(ee)>0:
                            for eee in ee:
                                chunk.append(eee)

elif mode != 4: # mode 0 = auto, mode 1 = prefix, mode 3 = digram, mode 5 = corners
    for y in range(py1,py2):
        for x in range(px1,px2):
            
            print('Pathing tile {},{}...'.format(x,y))
            
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
    
            chunk = [[array[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                    if (mode==0 
                        or mode==1 
                        or minz==maxz
                        or (mode==3 and e[3][ey*4+ex]==1) # check if looking for digram or corner words only
                        or (mode==5 and (e[3][0]==1 or e[3][3]==1 or e[3][12]==1 or e[3][15]==1))):
                        if len(e[0])<=maxz: out.append(e[0])
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)

    if pz!='' and mode==1:
        px1=0
        px2=4
        py1=0
        py2=4
        for y in range(py1,py2):
            for x in range(px1,px2):
                
                if (mode==1 or mode==3) and x==ex and y==ey: continue
                
                print('Pathing tile {},{}...'.format(x,y))
                
                fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                fary[y*4+x]=1
                fary[ey*4+ex]=1 # no longer need to add prefix to path
        
                chunk = [[array[y*4+x],x,y,fary]]
                while len(chunk)>0:
                    e = chunk.pop(0)
                    if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                        out.append(e[0])
                    if len(e[0])<maxz:
                        if len(e[0])>2:
                            if e[0] not in trunc[len(e[0])-3]:
                                continue
                        ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                        if len(ee)>0:
                            for eee in ee:
                                chunk.append(eee)

else: # mode 4 = either/or mode, unless target word length is set
    print('Pass 1 ({}):'.format(char1))
    for y in range(py1,py2):
        for x in range(px1,px2):
            
            print('Pathing tile {},{}...'.format(x,y))
            
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
    
            chunk = [[array1[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                    if pz!='' or e[3][ey*4+ex]==1:
                        out.append(e[0])
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array1,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    print('Pass 2 ({}):'.format(char2))
    for y in range(py1,py2):
        for x in range(px1,px2):
            
            print('Pathing tile {},{}...'.format(x,y))
            
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
    
            chunk = [[array2[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                if len(e[0])>minz-1 and e[0] in words and e[0] not in out:
                    if pz!='' or e[3][ey*4+ex]==1:
                        out.append(e[0])
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array2,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)

out.sort(key=len)
print('')
if len(out)<1:
    print('No words match criteria!')
else:
    for w in out:
        print(w, end=' ')