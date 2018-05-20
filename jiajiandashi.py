import win32api,win32con
from PIL import ImageGrab
import config
import time
question=0
upichashmap={'0xc40c0c0c0c4f03':'1','0x24246464a7a7222':'2','0x425252527a7e2c':'3','0x8181838687e7e08':'4','0x72725252525c4c':'5','0x3c3c525252525c4c':'6','0x4040424e7e706040':'7','0xc7e7252525a7e2c':'8','0x30724a4a4a467c38':'9','0x1010103c3c101010':'+','0x808080808080808':'-',}
mutiupichashmap={'0x3c7e424242663c3c':'0','0x242427e7e020202':'1','0x24246464a7a7222':'2','0x425252527a7e2c':'3','0x8181838687e7e08':'4','0x72725252525c4c':'5','0x3c3c525252525c4c':'6','0x4040424e7e706040':'7','0xc7e7252525a7e2c':'8','0x327a4a4a4a6e3c38':'9','0x1010103c3c101010':'+','0x808080808080808':'-',}
dpichashmap={'0x1c3e224141223e1c':'0','0x121213f3f3f0101':'1','0x212323454d393901':'2','0x2223292929393616':'3','0x40c1c34243f3f04':'4','0x23b3929292b2e26':'5','0x1e3e2b29292b2e06':'6','0x2020232f3f302020':'7','0x16373929292d3616':'8','0x383b2121212a3e1c':'9','0x404040404040404':'-'}
threshold = 200
table = []
for i in range(256):
    if i > threshold:
        table.append(0)
    else:
        table.append(1)

picnum=0
def getsinglenum(img):
    global picnum
    width=img.size[0]
    height=img.size[1]
    bimg=img.point(table, '1')
    pix = bimg.load()
    white = False
    left = 0
    piclist=[]
    for x in range(width):
        white_flag = False
        for y in range(height):
            if pix[x, y] == 0:
                white_flag = True
                break
        if white:
            if not white_flag:
                pic = img.crop([left, 0, x, height])
                if config.save_debug:
                    if question>75:
                        pic.save('./pic/'+str(picnum)+'.jpg')
                piclist.append(pic)
                white = False
                picnum += 1
        else:
            if white_flag:
                left = x
                white = True
    return piclist
def getjunzhi(img):
    img=img.resize([8,8])
    width=img.size[0]
    height=img.size[1]
    pix=img.load()
    ave=0
    hashnum=0
    for x in range(width):
        for y in range(height):
            ave+=pix[x,y]
    ave=ave/64
    for x in range(width):
        for y in range(height):
            hashnum <<= 1
            if pix[x,y]>ave:
                hashnum|=0b1
    # print(hex(hashnum))
    return hashnum

def piccrop(img):
    width = img.size[0]
    height = img.size[1]
    # grayimg = img.point(table, '1')
    first=img.crop([0,0,width,height/2])
    second=img.crop([0,height/2,width,height])
    return first,second

def getupnum(pichash):
    # nine = nine.resize([17, 16])
    # width = nine.size[0]
    # height = nine.size[1]
    # pix = nine.load()
    # pichash = 0b0
    # for y in range(height):
    #     for x in range(1, width):
    #         pichash <<= 1
    #         if pix[x - 1, y] > pix[x, y]:
    #             pichash |= 0b01
    #         else:
    #             pichash |= 0b00
    # if config.hashdebug:
    #     print(hex(pichash))
    # if hex(pichash)=='0x0':
    #     return '-'
    hmlist=[]
    if question<76:
        length=len(upichashmap)
    else:
        length=len(mutiupichashmap)
    for i in range(0,length):
        hm=0
        if question<76:
            hdis=eval(list(upichashmap.keys())[i])^ pichash
        else:
            hdis = eval(list(mutiupichashmap.keys())[i]) ^ pichash
        while hdis!=0:
            if hdis&0x1:
                hm+=1
            else:
                hm+=0
            hdis>>=1
        hmlist.append(hm)
    num=0
    for i in range(1,length):
        if hmlist[i]<hmlist[num]:
            num=i
    if question<76:
        return upichashmap[list(upichashmap.keys())[num]]
    else:
        return mutiupichashmap[list(mutiupichashmap.keys())[num]]

def getdownnum(pichash):
    # nine = nine.resize([9, 8])
    # width = nine.size[0]
    # height = nine.size[1]
    # pix = nine.load()
    # pichash = 0b0
    # for y in range(height):
    #     for x in range(1, width):
    #         pichash <<= 1
    #         if pix[x - 1, y] > pix[x, y]:
    #             pichash |= 0b01
    #         else:
    #             pichash |= 0b00
    # if config.hashdebug:
    #     print(hex(pichash))
    hmlist=[]
    for i in range(0,11):
        hm=0
        hdis=eval(list(dpichashmap.keys())[i])^ pichash
        while hdis!=0:
            if hdis&0x1:
                hm+=1
            else:
                hm+=0
            hdis>>=1
        hmlist.append(hm)
    num=0
    for i in range(1,11):
        if hmlist[i]<hmlist[num]:
            num=i
    return dpichashmap[list(dpichashmap.keys())[num]]
if __name__ == '__main__':
    while True:
        time.sleep(0.4)
        up,down = piccrop(ImageGrab.grab([550, 280, 805, 415]).convert('L'))
        first=getsinglenum(up)
        second=getsinglenum(down)
        dengshi=''
        for i in first:
            dengshi+=getupnum(getjunzhi(i))

        dengshi+='=='
        for j in second[1:]:
            dengshi+=getdownnum(getjunzhi(j))

        if config.dengshi_debug:
            print(dengshi)
            print(eval(dengshi))
        if config.clickable:
            if eval(dengshi):
                win32api.SetCursorPos([590,583])
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP,0,0)
            else:
                win32api.SetCursorPos([775, 573])
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        if config.breakable:
            break
        question+=1
        print('题号: '+str(question))