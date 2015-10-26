#@author Ben.Sebuufu 

#creates a collage on a canvas
def createCollage(imageLoc):
    #this is the canvas I place the pictures on
    canvas = makeEmptyPicture(694,946)
    
    #this is the picture I manipulate; image filepath is the 
    #input parameter to this function
    eagle = makePicture(imageLoc)
        
    #now placing the pictures on the canvas
	
    #rotate picture by 180, pixel it, and place it at (172,0)
    rotatedBy180 = rotate180R(eagle)
    pixelledFullPicture = pixelIt(rotatedBy180,15)
    copy(pixelledFullPicture,canvas,174,706)
    
    #another full picture at the top of the picture
    copy(eagle,canvas,174,0)
    
    #a black and white picture middle left
    BWPicture = brightBW(eagle)
    copy(BWPicture,canvas,0,352)
    
    #a full sepia image in the middle right ground
    sepiaLikePicture = sepiaLike(eagle)
    copy(sepiaLikePicture,canvas,347,352)
    
    #a picture on the top of the picture
    picHead = cropAnySize(eagle,0,0,174,245)
    lineDrawnHead = lineDraw(picHead)
    copy(lineDrawnHead,canvas,174,109)
	
    #back of the eagle on the top
    picTail = cropAnySize(eagle,173,0,174,245)
    redOnlyTail = leaveOnlyRed(picTail)
    copy(redOnlyTail,canvas,347,109)
    
    #no blue head in the bottom middle
    noBlueHead = eliminateBlue(picHead)
    copy(noBlueHead,canvas,174,597)
    
    #no green tail in the bottom middle
    noGreenTail = eliminateGreen(picTail)
    copy(noGreenTail,canvas,347,597)
    
    #the picture copied with out the background
    copyNoBackground(eagle,canvas,147,352)
    
    #a cross in the tail on top left
    crossHead = copyACross(picHead)
    redCrossHead = leaveOnlyRed(crossHead)
    copy(redCrossHead,canvas,0,0)
	
    #a cross in the tail on top right
    crossTail = copyACross(picTail)
    copy(crossTail,canvas,520,0)
    
    #a flipped cross tail in the bottom
    flippedTailCross = rotate180R(crossTail)
    copy(flippedTailCross,canvas,0,701)
	
    #a flipped cross head in the bottom
    flippedHeadCross = rotate180R(crossHead)
    redFlippedHeadCross = eliminateBlue(flippedHeadCross)
    copy(redFlippedHeadCross,canvas,520,701)
    
    #crop head eagle, place it in the next four
    eagleHead = cropAnySize(eagle,10,80,174,109)
	
    #place this eagle in two different places
    copy(eagleHead,canvas,520,245) #right; above sepia
    copy(eagleHead,canvas,0,597) #left; under black and white
	
    #make negative of eagle. use in two positions
    negated = makeNegative(eagleHead)
    copy(negated,canvas,0,245)
    copy(negated,canvas,520,597)
    
    show(canvas)
    return canvas
    
    
#copies onto canvas 
def copy(source, target, targX, targY):
  targetX = targX
  for sourceX in range(0,getWidth(source)):
    targetY = targY
    for sourceY in range(0, getHeight(source)):
      px = getPixel(source, sourceX, sourceY)
      tx = getPixel(target, targetX, targetY)
      setColor(tx, getColor(px))
      targetY = targetY + 1
    targetX = targetX + 1

#rotates the picture through 180 degrees 
def rotate180R(pic):
    rotated180 = duplicatePicture(pic)
    width = getWidth(rotated180)
    height = getHeight(rotated180)
    rotated = makeEmptyPicture(width, height)
    for col in range(0, width):
        for row in range(0, height):
            setColor(getPixel(rotated,width-col-1,height-row-1), getColor(getPixel(rotated180,col,row)))
    return rotated
	
#makes a picture with bright black and white hue
def brightBW(picture1):
    picture = duplicatePicture(picture1)
    for xpos in range(0,getWidth(picture)):
        for ypos in range(0,getHeight(picture)):
            pix = getPixel(picture,xpos,ypos)
            newRed = getRed(pix)*0.299
            newGreen = getGreen(pix)*0.587
            newBlue = getBlue(pix)*0.114
            color = 255 - (newRed+newGreen+newBlue)
            setColor(pix, makeColor(color,color,color))
    return picture
	
#makes sepia, but with a high value of red.
def sepiaLike(pic):
    sepiaTinted = duplicatePicture(pic)
    sepiaTinted = grayScale(sepiaTinted)
    for p in getPixels(sepiaTinted):
        red = getRed(p)
        blue = getBlue(p)
        #tint shadows
        if (red > 63):
            red = red*1.1
            blue = blue*1.9
        #tint midtones
        if (red>62 and red<192):
            red = red*1.15
            blue = blue*0.95
        #tint highlights
        if (red>191):
            red = red*1.08
        if (red>255):
            red = 255
            blue = blue*0.93
        #set the new color values
        setBlue(p,blue)
        setRed(p,red)
    return sepiaTinted

#crops a picture of any size starting any given point
def cropAnySize(source,startPointX,startPointY,newWidth,newHeight):
    source = duplicatePicture(source)
    newCanvas = makeEmptyPicture(newWidth,newHeight)
    target = newCanvas
    targetX = 0
    for sourceX in range(startPointX, getWidth(source)-(getWidth(source)+1-(startPointX+newWidth-1)-1)): 
        targetY = 0
        for sourceY in range(startPointY, getHeight(source)-(getHeight(source)+1-(startPointY+newHeight-1)-1)):
            px = getPixel(source, sourceX, sourceY)
            tx = getPixel(target, targetX, targetY)
            setColor(tx, getColor(px))
            targetY = targetY + 1
        targetX = targetX + 1
    return target

#makes a line sketch of a picture
def lineDraw(pic):
  lineDrawn = duplicatePicture(pic)
  for x in range(0,getWidth(pic)-1):
    for y in range(0,getHeight(pic)-1):
      here = getPixel(lineDrawn,x,y)
      down = getPixel(pic,x,y+1)
      right = getPixel(pic,x+1,y)
      hereL = (getRed(here)+getGreen(here)+getBlue(here))/3
      downL = (getRed(down)+getGreen(down)+getBlue(down))/3
      rightL = (getRed(right)+getGreen(right)+getBlue(right))/3
      if abs(hereL - downL)>10 and abs(hereL-rightL)>10:
        setColor(here,black)
      if abs(hereL - downL)<=10 and abs(hereL - rightL)<=10:
        setColor(here,white)
  return lineDrawn
  
#removes blue and green making the picture red 
def leaveOnlyRed(pic):
    redOnly = duplicatePicture(pic)
    for p in getPixels(redOnly):
          valueBlue = getBlue(p)
          valueGreen = getGreen(p)
          valueRed = getRed(p)
          setBlue(p,valueBlue*0.25)
          setGreen(p,valueGreen*0.25)
          setRed(p, valueRed*1.50)
    return redOnly

#sets all the green of a picture to zero
def eliminateGreen(pic):
    noGreenPic = duplicatePicture(pic)
    for p in getPixels(noGreenPic):
        value = getGreen(p)
        setGreen(p,value*0)
    return noGreenPic

#gets rid of blue from a picture
def eliminateBlue(pic):
    noBlue = duplicatePicture(pic)
    for p in getPixels(noBlue):
        value = getBlue(p)
        setBlue(p,value*0)
    return noBlue

#negates a picture
def makeNegative(pic):
    negativePic = duplicatePicture(pic)
    for px in getPixels(negativePic):
        red = getRed(px)
        green = getGreen(px)
        blue = getBlue(px)
        negColor = makeColor(255-red, 255-green, 255-blue)
        setColor(px,negColor)
    return negativePic
	
#obtains a cross from the picture; sets other areas white
def copyACross(source1):
    source = source1
    for xpixel in range(0,getWidth(source)):
        for ypixel in range(0,getHeight(source)):
            if xpixel<44 and ypixel<62:
                whiteThis = getPixel(source,xpixel,ypixel)
                setColor(whiteThis,white)
            if 130<xpixel<(getWidth(source)+1) and ypixel<62:
                whiteThis = getPixel(source,xpixel,ypixel)
                setColor(whiteThis,white)
            if xpixel<44 and 183<ypixel<getHeight(source):
                whiteThis = getPixel(source,xpixel,ypixel)
                setColor(whiteThis,white)
            elif 130<xpixel<(getWidth(source)+1) and 183<ypixel<getHeight(source):
                whiteThis = getPixel(source,xpixel,ypixel)
                setColor(whiteThis,white)
    return source

#copies without blue background
def copyNoBackground(source, target, targX, targY):
  targetX = targX
  for sourceX in range(0,getWidth(source)):
    targetY = targY
    for sourceY in range(0, getHeight(source)):
      px = getPixel(source, sourceX, sourceY)
      tx = getPixel(target, targetX, targetY)
      if getBlue(px)>100 and getRed(px)<100:
        setColor(tx, getColor(tx))              
      else:
        setColor(tx, getColor(px))
      targetY = targetY + 1
    targetX = targetX + 1
  return target

#turns a picture into shades of gray
def grayScale(pic):
    negated = duplicatePicture(pic)
    #sums the colors in a picture and paints the picture the average 
    for p in getPixels(negated):
        intensity = (getRed(p)+getGreen(p)+getBlue(p))/3
        setColor(p,makeColor(intensity, intensity,intensity)) 
    return negated 
  
#requires cropItCenter(pic) to work            
#pixelizes a picture
def pixelIt(picture,ps):

    #getting rid of excess lengths and cropping pic
    xRemainder = getWidth(picture)%ps
    yRemainder = getHeight(picture)%ps
    pic = cropItCenter(picture,getWidth(picture)-xRemainder,getHeight(picture)-yRemainder)
    
    for xpos in range (0,getWidth(pic),ps):
        for ypos in range(0,getHeight(pic),ps):
            redColor = 0
            blueColor = 0
            greenColor = 0
            for px in range(xpos,xpos+ps):
                for py in range(ypos,ypos+ps):
                    pix = getPixel(pic,xpos,ypos)
                    redColor = redColor + getRed(pix)
                    greenColor = greenColor + getGreen(pix)
                    blueColor = blueColor + getBlue(pix)                    
            #colors used to calculate the average 
            newRed = redColor/ps**2
            newGreen = greenColor/ps**2
            newBlue = blueColor/ps**2
            newColor = makeColor(newRed,newGreen,newBlue)
            
            for px in range(xpos,xpos+ps):
                for py in range(ypos,ypos+ps):
               
                    blockPixel = getPixel(pic,px,py)
                    setColor(blockPixel,newColor)
    return(pic)   
    
#crops the center of the picture
def cropItCenter(picture,newWidth,newHeight):
    newPicture = makeEmptyPicture(newWidth,newHeight)
    xtarget = 0
    for xpos in range((getWidth(picture)-newWidth)/2,(getWidth(picture)+newWidth)/2):
        ytarget= 0
        for ypos in range((getHeight(picture)-newHeight)/2, (getHeight(picture)+newHeight)/2):
            pixelToCopy = getPixel(picture,xpos,ypos)
            colorToCopy = getColor(pixelToCopy)
            setColor(getPixel(newPicture,xtarget,ytarget), colorToCopy)
            ytarget = ytarget+1
        xtarget = xtarget+1
    return newPicture
    

#direct execution; insert (string) location of the 'input_Eagle.jpg' below
createCollage()
