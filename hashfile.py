from PIL import Image
upichashmap={'0xc40c0c0c0c4f03':'1','0x18267313072e0401':'2','0x5827711b33511722':'3','0x252b225430208':'4','0x13013e1511240':'5','0x7481615761638716':'6','0x142464c580854':'7','0x682721ab33712a2a':'8','0x5c226b6b89893698':'9','0x180c6dcc0c2400':'+','0x43440000':'-',}
dpichashmap={'0x4e73e96163375d':'0','0xd4544444440f43':'1','0xc678b06073011':'2','0x4d71118699634d':'3','0x2471637991317':'4','0x81113e318121cd':'5','0x1297340763311336':'6','0x8111060d481c18':'7','0xc7131b771334c':'8','0xe37713189779e':'9','0x180018000':'=','0xa0030000':'-'}
nine=Image.open('3.jpg')
nine.show()
nine=nine.resize([9,8])
width=nine.size[0]
height=nine.size[1]
pix=nine.load()
pichash=0b0
print(width,height)
for y in range(height):
    for x in range(1,width):
        pichash<<=1
        if pix[x-1,y]>pix[x,y]:
            pichash|=0b01
        else:
            pichash|=0b00
print(hex(pichash))
hmlist=[]
for i in range(0,12):
    hm=0
    hdis=eval(list(dpichashmap.keys())[i])^ pichash
    while hdis!=0:
        if hdis&0x1:
            hm+=1
        else:
            hm+=0
        hdis>>=1
    hmlist.append(hm)
print(hmlist)



