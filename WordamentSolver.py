# -*- coding: utf-8 -*-

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

# get 16 tiles from user
linein = input('Input tiles (space-delimited):\n')
array = linein.split(' ')

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
    mode = 5


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
for w in out:
    print(w, end=' ')