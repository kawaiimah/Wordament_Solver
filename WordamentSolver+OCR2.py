import pyautogui
import cv2
import pytesseract
import numpy as np

print('\nRunning OCR...\n')
try:
    hx, hy = pyautogui.locateCenterOnScreen('hint.png', confidence=0.9)
except:
    print('\nWordament screen not found!')
    import sys
    sys.exit()

# screengrab tile grid
# x,y = hintpoint
x = hx + 100
y = hy
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
# cv2.imwrite('tile0.png',tile[0])

# crop out the 16 scores from the tiles
score = []
score.append(img[2:22,5:35].copy())
score.append(img[2:22,78:108].copy())
score.append(img[2:22,155:185].copy())
score.append(img[2:22,230:260].copy())
score.append(img[77:97,5:35].copy())
score.append(img[77:97,78:108].copy())
score.append(img[77:97,155:185].copy())
score.append(img[77:97,230:260].copy())
score.append(img[153:173,5:35].copy())
score.append(img[153:173,78:108].copy())
score.append(img[153:173,155:185].copy())
score.append(img[153:173,230:260].copy())
score.append(img[228:248,5:35].copy())
score.append(img[228:248,78:108].copy())
score.append(img[228:248,155:185].copy())
score.append(img[228:248,230:260].copy())
# cv2.imwrite('score11.png',score[11])

# invoke tesseract for OCR
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
array = []
score_array = []
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

try:
    for i in range(16):
        tscore = pytesseract.image_to_string(score[i], lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')[:-2]
        if tscore.isnumeric():
            score_array.append(int(tscore))
        else:
            score_array.append(5)
except:
    pass

# screengrab tasks (target length)
x = hx - 160
y = hy - 152
img_raw = pyautogui.screenshot(region=(x,y, 11, 16))
# convert to grayscale then black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
# cv2.imwrite('img.png',img)
# invoke tesseract
task_len = 0
try:
    task_len = int(pytesseract.image_to_string(img, lang='eng', config='--psm 10 -c tessedit_char_whitelist=3456')[:-2])
except:
    pass

# screengrab tasks (num of words)
x = hx - 160
y = hy - 131
img_raw = pyautogui.screenshot(region=(x,y, 100, 22))
# convert to grayscale then black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
# cv2.imwrite('img.png',img)
# invoke tesseract
task_lennum = 0
try:
    task_lennum = int(pytesseract.image_to_string(img, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789/')[:-2].split('/')[-1])
except:
    pass
print('...extracting puzzle tasks')

# screengrab tasks (num of points)
x = hx - 15
y = hy - 131
img_raw = pyautogui.screenshot(region=(x,y, 110, 22))
# convert to grayscale then black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
# cv2.imwrite('img.png',img)
# invoke tesseract
task_points = 0
try:
    task_points = int(pytesseract.image_to_string(img, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789/')[:-2].split('/')[-1])
except:
    pass

# screengrab tasks (num of special words)
x = hx + 140
y = hy - 132
img_raw = pyautogui.screenshot(region=(x,y, 100, 22))
# convert to grayscale then black and white
img_gray = cv2.cvtColor(np.array(img_raw), cv2.COLOR_RGB2GRAY)
(thresh, img) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
img = cv2.bitwise_not(img)
# cv2.imwrite('img.png',img)
# invoke tesseract
task_special = 11
try:
    task_special = int(pytesseract.image_to_string(img, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789/')[:-2].split('/')[-1])
except:
    pass

# show detected tiles and scores
print('\nOCR detected the following letters:')
for i in range(4):
    print(array[i*4:i*4+4])
print('\nOCR detected the following scores:')
for i in range(4):
    print(score_array[i*4:i*4+4])

# show detected tasks
print('\nOCR detected the following tasks:')
print('Number of {}-letter words needed: {}'.format(task_len,task_lennum))
print('Number of points needed: {}'.format(task_points))
print('Number of specials needed: {}'.format(task_special))

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

# define function for calculating word scores
def calc_score(wordlength,flagarray,scorearray):
    wordscore=0
    for i in range(16):
        if flagarray[i]==1:
            wordscore += scorearray[i]
    if wordlength==5:
        wordscore *= 1.5
    elif wordlength==6 or wordlength==7:
        wordscore *= 2
    elif wordlength>=8:
        wordscore *= 2.5
    if wordscore>200:
        wordscore = 200
    return(int(wordscore))

# default mode = 0, i.e. long word mode
mode=0
px1=0
px2=4
py1=0
py2=4
minz=3
maxz=15

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
    mode = 5

# prep output list
out = []
out1 = [] # subset of word length = task_len
out2 = [] # subset of digram, corner or either/or words
auto = []

if mode == 2: # mode 2 = suffix mode
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in rev_trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    # prioritise special words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_special or len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # top up if not enough special words
    if len(auto)<task_special:
        for wordtuple in out:
            if len(auto)>=task_special:
                break
            if wordtuple not in auto:
                auto.append(wordtuple)
    
    # switch back to default mode for second pass
    mode=0
    px1=0
    px2=4
    py1=0
    py2=4
    minz=task_len
    maxz=15
    for y in range(py1,py2):
        for x in range(px1,px2):
            if x==ex and y==ey: continue
            print('Pathing tile {},{}...'.format(x,y))
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            fary[ey*4+ex]=2 # no longer need to add suffix to path/score
            chunk = [[array[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    out.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    # check if enough words of length = task_len
    cnum = 0
    for wordtuple in auto:
        if len(wordtuple[0])==task_len:
            cnum += 1
    for wordtuple in out1:
        if cnum>=task_lennum:
            break
        if wordtuple not in auto:
            auto.append(wordtuple)
            cnum += 1
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]

elif mode == 1: # mode 1 = prefix
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    # prioritise special words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_special or len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # top up if not enough special words
    if len(auto)<task_special:
        for wordtuple in out:
            if len(auto)>=task_special:
                break
            if wordtuple not in auto:
                auto.append(wordtuple)

    # switch back to default mode for second pass
    mode=0
    px1=0
    px2=4
    py1=0
    py2=4
    minz=task_len
    maxz=15
    for y in range(py1,py2):
        for x in range(px1,px2):
            # skip special tile
            if x==ex and y==ey: continue
            print('Pathing tile {},{}...'.format(x,y))
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            fary[ey*4+ex]=2 # no longer need to add prefix to path/score
            chunk = [[array[y*4+x],x,y,fary]]
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    out.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    # check if enough words of length = task_len
    cnum = 0
    for wordtuple in auto:
        if len(wordtuple[0])==task_len:
            cnum += 1
    for wordtuple in out1:
        if cnum>=task_lennum:
            break
        if wordtuple not in auto:
            auto.append(wordtuple)
            cnum += 1
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]

elif mode == 0: # mode 0 = long word mode
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    # prioritise words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]
    
elif mode == 3: # mode 3 = digram mode
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            # and to append to out2 as well if digram tile is used
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                    if e[3][ey*4+ex]==1:
                        out2.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing special words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out2.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out2 if len(wordtuple[0])==task_len]
    # prioritise special words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_special or len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # top up if not enough special words
    if len(auto)<task_special:
        for wordtuple in out2:
            if len(auto)>=task_special:
                break
            if wordtuple not in auto:
                auto.append(wordtuple)
    # check if enough words of length = task_len
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    cnum = 0
    for wordtuple in auto:
        if len(wordtuple[0])==task_len:
            cnum += 1
    for wordtuple in out1:
        if cnum>=task_lennum:
            break
        if wordtuple not in auto:
            auto.append(wordtuple)
            cnum += 1
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]

elif mode == 5: # mode 5 = corners
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            # and to append to out2 as well if corner tile is used
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                    if (e[3][0]==1 or e[3][3]==1 or e[3][12]==1 or e[3][15]==1):
                        out2.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing special words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out2.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out2 if len(wordtuple[0])==task_len]
    # prioritise special words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_special or len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # top up if not enough special words
    if len(auto)<task_special:
        for wordtuple in out2:
            if len(auto)>=task_special:
                break
            if wordtuple not in auto:
                auto.append(wordtuple)
    # check if enough words of length = task_len
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    cnum = 0
    for wordtuple in auto:
        if len(wordtuple[0])==task_len:
            cnum += 1
    for wordtuple in out1:
        if cnum>=task_lennum:
            break
        if wordtuple not in auto:
            auto.append(wordtuple)
            cnum += 1
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]

else: # mode 4 = either/or mode
    print('Pass 1 ({}):'.format(char1))
    for y in range(py1,py2):
        for x in range(px1,px2):
            print('Pathing tile {},{}...'.format(x,y))
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array1[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            # and to append to out2 as well if either/or tile is used
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                    if e[3][ey*4+ex]==1:
                        out2.append(wordtuple)
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
            # initiate a chunk of 1 letter at position x,y
            fary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            fary[y*4+x]=1
            chunk = [[array2[y*4+x],x,y,fary]]
            # loop to add letters one by one to chunks
            # append to out as a tuple of (word, score)
            # if identified as proper word
            # and to append to out2 as well if either/or tile is used
            while len(chunk)>0:
                e = chunk.pop(0)
                wordtuple = (e[0],calc_score(len(e[0]), e[3], score_array))
                if len(e[0])>minz-1 and e[0] in words and wordtuple not in out:
                    out.append(wordtuple)
                    if e[3][ey*4+ex]==1:
                        out2.append(wordtuple)
                if len(e[0])<maxz:
                    if len(e[0])>2:
                        if e[0] not in trunc[len(e[0])-3]:
                            continue
                    ee = add_letter(e[0],e[1],e[2],e[3],array2,mode)
                    if len(ee)>0:
                        for eee in ee:
                            chunk.append(eee)
    # sort identified words by score value
    # create out1 containing special words of length = task_len
    out.sort(key = lambda x: x[1], reverse=True)
    out2.sort(key = lambda x: x[1], reverse=True)
    out1 = [wordtuple for wordtuple in out2 if len(wordtuple[0])==task_len]
    # prioritise special words of length = task_len
    for wordtuple in out1:
        if len(auto)>=task_special or len(auto)>=task_lennum:
            break
        else:
            auto.append(wordtuple)
    # top up if not enough special words
    if len(auto)<task_special:
        for wordtuple in out2:
            if len(auto)>=task_special:
                break
            if wordtuple not in auto:
                auto.append(wordtuple)
    # check if enough words of length = task_len
    out1 = [wordtuple for wordtuple in out if len(wordtuple[0])==task_len]
    cnum = 0
    for wordtuple in auto:
        if len(wordtuple[0])==task_len:
            cnum += 1
    for wordtuple in out1:
        if cnum>=task_lennum:
            break
        if wordtuple not in auto:
            auto.append(wordtuple)
            cnum += 1
    # now to keep adding high value words till task_points is reached
    ctotal = 0
    for wordtuple in auto:
        ctotal += wordtuple[1]
    for wordtuple in out:
        if ctotal>=task_points:
            break
        elif wordtuple not in auto:
            auto.append(wordtuple)
            ctotal += wordtuple[1]

# show auto word list
print('')
for wordtuple in auto:
    print(wordtuple)