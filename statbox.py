# (C) 2015 Compose, an IBM company
# MIT Licensed

import pymongo
import unicornhat as unicorn
import sys,ssl,time

"mongodb://user:password@host1.example.com:port,host2.example.com:port2/admin?ssl=true"
client = pymongo.MongoClient(connecturl,ssl_ca_certs="./cacert.pem",ssl_cert_reqs=ssl.CERT_OPTIONAL)

red=[255,0,0]
green=[0,255,0]
blue=[0,0,255]
black=[0,0,0]
white=[255,255,255]

maxval=8

values=[ 0, 0, 0, 0, 0, 0, 0, 0 ]
colors=[ black, black, black, black, black, black, black, black]

unicorn.brightness(0.10)
#unicorn.rotation(90)

while True:
  conncounts = client["admin"].command({"serverStatus":1})["connections"]
  newval=conncounts["current"]

  oldval=values[7]
  if oldval==newval:
    newcol=blue
  elif oldval<newval:
    newcol=red
  elif oldval>newval:
    newcol=green

  if newval>maxval:
    while newval>maxval:
      maxval=maxval*2
      newcol=white
  elif maxval>8:
    midval=maxval/2
    scaledown=True
    for i in range(0,8):
      if values[i]>midval:
        scaledown=False
    if scaledown:
      maxval=midval
      newcol=white

  values.pop(0)
  colors.pop(0)

  values.append(newval)
  colors.append(newcol)

#  print(values)
#  print(colors)

  fudge=maxval/8

  for x in range(0,8):
    val=values[x]
    col=colors[x]
    adjval=int(val/fudge)
    for y in range(0,adjval):
      unicorn.set_pixel(x,y,col[0],col[1],col[2])
    if adjval<8:
      for y in range(adjval,8):
        unicorn.set_pixel(x,y,0,0,0)

  unicorn.show()
  time.sleep(5)
