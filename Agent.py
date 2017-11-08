# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
import numpy as np
from PIL import Image, ImageChops, ImageFilter
import time
from fractions import Fraction  

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

 

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        
        global img_names,figures,name, images
        name=problem.name
        print(problem.name)
        ts = time.time()


            
        if(problem.problemType=="3x3"):
            
            img_names=['A','B','C','D','E','F','G','H']
            figures=dict()
            images=dict()
                
            for i in img_names:
                figures[i]=(problem.figures[i])
                imagex=self.trimImage(Image.open(figures[i].visualFilename))
                images[i]=imagex
            
            #horizontal patterns
            pairsAB, notPaired=self.get_Pairs(figures['A'], figures['B'])
            pairsBC, notPaired=self.get_Pairs(figures['B'], figures['C'])
            pairsDE, notPaired=self.get_Pairs(figures['D'], figures['E'])
            pairsEF, notPaired=self.get_Pairs(figures['E'], figures['F'])
            pairsGH, notPaired=self.get_Pairs(figures['G'], figures['H'])

            #vertical patterns            
            pairsAD, notPaired=self.get_Pairs(figures['A'], figures['D'])
            pairsDG, notPaired=self.get_Pairs(figures['D'], figures['G'])
            pairsBE, notPaired=self.get_Pairs(figures['B'], figures['E'])
            pairsEH, notPaired=self.get_Pairs(figures['E'], figures['H'])
            pairsCF, notPaired=self.get_Pairs(figures['C'], figures['F'])


            transformations_horizontal=self.getTransformationPattern(['A','B','C','D','E','F', 'G', 'H'],[pairsAB,pairsBC,pairsDE,pairsEF,pairsGH], [pairsAD,pairsDG,pairsBE,pairsEH])
            transformations_vertical=self.getTransformationPattern(['A','D','G','B','E','H', 'C', 'F'],[pairsAD,pairsDG,pairsBE,pairsEH,pairsCF], [pairsAB,pairsBC,pairsDE,pairsEF])

            pairsAF, notPaired =self.get_Pairs(figures['A'], figures['F'])
            Ans_1= self.generate_Answer(transformations_vertical, pairsAD, pairsAF, notPaired, figures['F'])
            
            pairsAH, notPaired =self.get_Pairs(figures['A'], figures['H'])
            Ans_2= self.generate_Answer(transformations_horizontal, pairsAB, pairsAH, notPaired, figures['H'])
           
            #print(Ans_1)
            #print(Ans_2)
            Answer= self.test_Answer(['F', 'H'], ['C', 'G'],[Ans_1,Ans_2], problem, 8)
            print("Answer is",Answer)
            return Answer
        
        else:
            return -1

    
    def trimImage(self, Img):
        
        source = Img.split()
        mask = source[2].point(lambda i: i > 0)
        Img = Image.merge(Img.mode, source)
        
        return Img
        
    def getValue(self, dic,value):
        for name in dic:
            if dic[name] == value:
                return name
    
    def getEnum(self, dic, name):
        if(name in dic):
            return dic[name]
        else:
            return dic['unknown']
        
    def getTransformationPattern(self, letters, pairs, adjacents):
        if len(pairs)==1:
            return self.getTransformations(figures[letters[0]], figures[letters[1]], pairs[0])
        else:
            #transformation from A to B
            transform12_1=self.getTransformations(letters[0], letters[1], pairs[0])
            #transformation from B to C
            transform23_1=self.getTransformations(letters[1], letters[2], pairs[1])
            #transformation from D to E
            transform12_2=self.getTransformations(letters[3], letters[4], pairs[2])
            #transformation from E to F
            transform23_2=self.getTransformations(letters[4], letters[5], pairs[3])
            
            #transformation from G to H
            transform12_3=self.getTransformations(letters[6], letters[7], pairs[4])

            
            transformations=transform12_1
            
            #Check for row/column rotations
            transformations['rowRotation']=self.getRotation([letters[0],letters[1],letters[2], letters[3], letters[4], letters[5]])
            
            #Check for dark pixel ratio/contour/center of mass shifts
            transformations['darkPixelRatio']=(transform12_1['darkPixelRatio']+transform23_1['darkPixelRatio']+transform12_2['darkPixelRatio']+transform23_2['darkPixelRatio']+transform12_3['darkPixelRatio'])/5
            transformations['darkPixelRatioContour']=(transform12_1['darkPixelRatioContour']+transform23_1['darkPixelRatioContour']+transform12_2['darkPixelRatioContour']+transform23_2['darkPixelRatioContour']+transform12_3['darkPixelRatioContour'])/5
            transformations['shiftCOMX']=(transform12_1['shiftCOMX']+transform23_1['shiftCOMX']+transform12_2['shiftCOMX']+transform23_2['shiftCOMX']+transform12_3['shiftCOMX'])/5
            transformations['shiftCOMY']=(transform12_1['shiftCOMY']+transform23_1['shiftCOMY']+transform12_2['shiftCOMY']+transform23_2['shiftCOMY']+transform12_3['shiftCOMY'])/5
            transformations['shiftMOIX']=(transform12_1['shiftMOIX']+transform23_1['shiftMOIX']+transform12_2['shiftMOIX']+transform23_2['shiftMOIX']+transform12_3['shiftMOIX'])/5
            transformations['shiftMOIY']=(transform12_1['shiftMOIY']+transform23_1['shiftMOIY']+transform12_2['shiftMOIY']+transform23_2['shiftMOIY']+transform12_3['shiftMOIY'])/5
            
            
            #check for horizontal/
            transformations['flip_horiz']=transform23_2['flip_horiz']
            transformations['flip_vert']=transform23_2['flip_vert']
            transformations['changeNumObjects']=transform23_2['changeNumObjects']
            

            return transformations;


    def getRotation(self, arrLetters):
        i1, i2, i3=images[arrLetters[0]], images[arrLetters[1]], images[arrLetters[2]]
        i4, i5, i6=images[arrLetters[3]], images[arrLetters[4]], images[arrLetters[5]]
        totalDark1=self.getDP(i1)+self.getDP(i2)+self.getDP(i3)
        totalDark2=self.getDP(i4)+self.getDP(i5)+self.getDP(i6)
        diff=totalDark1-totalDark2
        if diff<5:
            return totalDark1
        else:
            return -1
            
    def isRowRotated(self, imgPrev, imgPrev2, imgCurrent, pixels):
        totalDark=self.getDP(imgPrev)+self.getDP(imgPrev2)+self.getDP(imgCurrent)
        diff=totalDark-pixels
        print(diff)
        if(diff<10):
            return True
        else:
            return False

        
    def getTransformations(self, name1, name2, pairs12):
        global shapesEnum, sizesEnum, fillEnum, relativePositionsEnum, alignmentEnum
        shapesEnum= {
            'unknown':'0',
            'square': '1',
            'circle': '2',
            'triangle' : '3',
            'rectangle' : '4',
            'pac-man' : '5',
            'right triangle' : '6',
            'octagon' : '7',
            'heart' :'8',
            'diamond' : '9',
            'star' : '10',
            'pentagon' : '11',
            'plus' : '12',
            'hexagon' : '13',
            'minus' :'14',
        }
        sizesEnum= {
            'unknown':'0',
            'huge': '6',
            'very large': '5',
            'large' :'4',
            'medium' : '3',
            'small' : '2',
            'very small' : '1'
        }
        fillEnum= {
            'unknown':0,
            'yes': 1,
            'no': -1,
            'right-half':2,
            'left-half':-2,
            'top-half':3,
            'bottom-half':-3,
        }
        relativePositionsEnum={
                'unknown':'0',
                "above":'2', 
                "below":'1',
                "inside":'3',
                "left-of":'4',
                "right-of":'5'
                }
        alignmentEnum={
                'unknown':[-10,-10],
                "bottom-left":[-1,-1],
                'bottom-right':[1,-1],
                'top-left':[-1,1],
                'top-right':[1,1],
                'top-center':[0,1],
                'bottom-center':[0,-1],
                'center-left':[-1,0],
                'center-right':[1,0]
                }
        
        transformations=dict()
        
        A=figures[name1]
        B=figures[name2]
        for key, value in pairs12.items():
            transformations[key]=dict()
            for attributeName in A.objects[key].attributes:
                if attributeName in B.objects[value].attributes:
                    if(attributeName=="shape"):
                        if A.objects[key].attributes['shape']==B.objects[value].attributes['shape']:
                            transformations[key]['shape']=0
                        else:
                            transformations[key]['shape']=shapesEnum[B.objects[value].attributes['shape']]
                    if(attributeName=="size"):
                        size1=A.objects[key].attributes['size']
                        size2=B.objects[value].attributes['size']
                        sizeDiff=int(sizesEnum[size2])-int(sizesEnum[size1])
                        transformations[key]['size']=sizeDiff
                    if(attributeName=="fill"):
                        fill1=A.objects[key].attributes['fill']
                        fill2=B.objects[value].attributes['fill']
                        fillDiff=int(fillEnum[fill2])-int(fillEnum[fill1])
                        transformations[key]['fill']=fillDiff
                    if(attributeName=="angle"):
                        angle1=A.objects[key].attributes['angle']
                        angle2=B.objects[value].attributes['angle']
                        angleDiff=int(angle1)-int(angle2)
                        transformations[key]['angle']=angleDiff
                    if(attributeName=="alignment"):
                        alignment1=self.getEnum(alignmentEnum,A.objects[key].attributes['alignment'])
                        alignment2=self.getEnum(alignmentEnum,B.objects[value].attributes['alignment'])
                        diffX=alignment2[0]-alignment1[0]
                        diffY=alignment2[1]-alignment1[1]
                        transformations[key]['translation']=[diffX,diffY]

        ###Check for vertical or horizontal flipping
        transformations['flip_horiz']=self.isFlipped(images[name1], images[name2], "horizontal")
        transformations['flip_vert']=self.isFlipped(images[name1],images[name2], "vertical")
        transformations['changeNumObjects']=len(B.objects)-len(A.objects)
        transformations['darkPixelRatio']=self.getDPR(images[name1], images[name2])
        transformations['darkPixelRatioContour']=self.getDPcontourR(images[name1], images[name2])
        deltax,deltay=self.getCOMchange(images[name1],images[name2])
        transformations['shiftCOMX']=deltax
        transformations['shiftCOMY']=deltay
        mdeltax,mdeltay=self.getMOIchange(images[name1],images[name2])
        transformations['shiftMOIX']=mdeltax
        transformations['shiftMOIY']=mdeltay

        return transformations 
     
    def getDPR(self, img1, img2):
        d1=self.getDP(img1)
        d2=self.getDP(img2)
        if(d1==0):
            d1=1
        dpr= d2/d1
        return dpr
    
    def getDP(self, img):
        img=img.convert("L")
        arr=np.array(img.getdata())
        dark=np.where(arr == 0)
        d=len(dark[0][:])
        return d
    
    def getCOM(self, img):
        img=img.convert("L")
        arr=np.array(img.getdata())
        arr.resize(img.height, img.width)
        darkx, darky=np.where(arr == 0)
        if(len(darkx)==0):
            comx=0
            comy=0
        else:
            comx=np.sum(darkx)/len(darkx)
            comy=np.sum(darky)/len(darky)
        return comx,comy
    
    def getCOMchange(self, img1, img2):
        x1,y1=self.getCOM(img1)
        x2,y2=self.getCOM(img2)
        delx=x2-x1
        dely=y2-y1
        return delx,dely
    
    def getMOI(self, img):
        img=img.convert("L")
        arr=np.array(img.getdata())
        arr.resize(img.height, img.width)
        darkx, darky=np.where(arr == 0)
        xsq=[x**2 for x in darkx.tolist()]
        ysq=[y**2 for y in darky.tolist()]
        if(len(darkx)==0):
            comx=0
            comy=0
        else:
            comx=np.sum(xsq)/len(xsq)
            comy=np.sum(ysq)/len(ysq)
        return comx,comy
    
    
    def getMOIchange(self, img1, img2):
        x1,y1=self.getMOI(img1)
        x2,y2=self.getMOI(img2)
        delx=x2-x1
        dely=y2-y1
        return delx,dely
    
    def getDPcontourR(self, img1, img2):
        d1=self.getDPcontour(img1)
        d2=self.getDPcontour(img2)
        if(d1==0):
            d1=1
        dpr= d2/d1
        return dpr
    
    def getDPcontour(self, img):
        img=img.convert("L")
        img = img.filter(ImageFilter.FIND_EDGES)
        arr=np.array(img.getdata())
        dark=np.where(arr == 0)
        d=len(dark[0][:])
        return d
        
        
    def isFlipped(self, img1, img2, direction):
        if(direction=="horizontal"):
            image_flipped = img1.transpose(Image.FLIP_LEFT_RIGHT)
            diff=ImageChops.difference(image_flipped, img2)
            if(self.isBlank(diff) or diff.getbbox() is None):
                return True
            else:
                return False
        else:
            image_flipped = img1.transpose(Image.FLIP_TOP_BOTTOM)
            diff=ImageChops.difference(image_flipped, img2)
            if(self.isBlank(diff) or diff.getbbox() is None):
                return True
            else:
                return False
        
        
    def isBlank(self, img):
        img = img.convert('L')
        numpy_array=np.array(img)
        whitepixels=0
        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                if numpy_array[i][j] >100:
                    whitepixels=whitepixels+1
        if(whitepixels==0):
            return True
        else:
            return False

    def get_Pairs(self, fig1, fig2):
         #Initialize a similarity matrix
        w=len(fig1.objects)
        h=len(fig2.objects)
        object_names1=[]
        object_names2=[]
        Matrix = np.zeros((w,h))
    
        i=0
        for objectName1 in fig1.objects:
            object_names1.append(objectName1)
            partner_name=""
            thisObject1=fig1.objects[objectName1]
            k=0
            for objectName2 in fig2.objects:
                object_names2.append(objectName2)
                score=0
                thisObject2 = fig2.objects[objectName2]
                # first check verbal data 
                for attributeName in thisObject1.attributes:
                    if(attributeName in thisObject2.attributes):
                        if(attributeName=="inside" or attributeName=="above" or attributeName=="below"):
                            if(len(thisObject1.attributes[attributeName])==len(thisObject2.attributes[attributeName])):
                                score=score+1
                        if(thisObject1.attributes[attributeName]==thisObject2.attributes[attributeName]):
                            score=score+1 
                Matrix[i][k]=score
                k=k+1
            i=i+1  
    #Create a dict to store pairs
        pairs=dict()
    #Go through similarity matrix to assign pairs and resolve ties
        if(Matrix.size>0):
            for n in range (0,w):
                max_score=np.max(Matrix)
                rows, cols = np.where(Matrix == max_score)
                x_val=rows[0]
                y_val=cols[0]
                for n in range(w):
                    Matrix[n][y_val]=0
                for n in range(h):
                    Matrix[x_val][n]=0
                pairs[object_names1[x_val]]=object_names2[y_val]

    
        
        notpaired=[]
        for objectName2 in fig2.objects:
            if objectName2 not in pairs.values():
                notpaired.append(objectName2)
        
        return pairs, notpaired
    
    def generate_Answer(self, transformations, pairsAB, pairsAC, notPaired, figurePrev):
        Ans=dict()
        C=figurePrev
        for key, value in pairsAB.items():
            if key in pairsAC:
                Cobject=pairsAC[key]
                Ans[Cobject]=[0 for x in range(10)]
                if('shape' in transformations[key]):
                    if(transformations[key]['shape']==0):
                        Ans[Cobject][0]=shapesEnum[C.objects[Cobject].attributes['shape']]
                if('size' in transformations[key]):
                    size1=C.objects[pairsAC[key]].attributes['size']
                    transform=int(transformations[key]['size'])
                    sizeNew=int(sizesEnum[size1])+transform
                    Ans[Cobject][1]=sizeNew
                if('fill' in transformations[key]):
                    fill1=C.objects[pairsAC[key]].attributes['fill']
                    transform=int(transformations[key]['fill'])
                    fillNew=int(fillEnum[fill1])+transform
                    Ans[Cobject][2]=fillNew
                if('angle' in transformations[key]):
                    angle1=int(C.objects[pairsAC[key]].attributes['angle'])
                    transform=int(transformations[key]['angle'])
                    angleNew=(angle1+transform)
                    Ans[Cobject][3]=angleNew
                if('translation' in transformations[key]):
                    oldalign=alignmentEnum[C.objects[pairsAC[key]].attributes['alignment']]
                    moved=transformations[key]['translation']
                    newX=int(oldalign[0])+int(moved[0])
                    newY=int(oldalign[1])+int(moved[1])
                    Ans[Cobject][6]=newX
                    Ans[Cobject][7]=newY
        if(transformations['flip_horiz']):
            Ans['flip_horizontal']=True
        else:
            Ans['flip_horizontal']=False
        if(transformations['flip_vert']):
            Ans['flip_vertical']=True
        else:
            Ans['flip_vertical']=False
        if(transformations['rowRotation']):
            Ans['rowRotation']=True
        Ans['numObjects']=len(C.objects)+transformations['changeNumObjects']
        Ans['darkPixels']=self.getDP(Image.open(C.visualFilename))*transformations['darkPixelRatio']
        Ans['darkPixelsContour']=self.getDPcontour(Image.open(C.visualFilename))*transformations['darkPixelRatioContour']
        oldx,oldy=self.getCOM(Image.open(C.visualFilename))
        newx=oldx+transformations['shiftCOMX']
        newy=oldy+transformations['shiftCOMY']
        Ans['COMX']=newx
        Ans['COMY']=newy
        oldx,oldy=self.getMOI(Image.open(C.visualFilename))
        newx=oldx+transformations['shiftMOIX']
        newy=oldy+transformations['shiftMOIY']
        Ans['MOIX']=newx
        Ans['MOIY']=newy
        return Ans
    
    def test_Answer(self, figPrev, figPrev2, possibleAnswers, problem, numSolutions):
        solutions = [[0 for x in range(numSolutions)] for p in range(2)] 
        i=0
        for D in possibleAnswers:
            C=figures[figPrev[i]]
            ImgC=images[figPrev[i]]
            for a in range (numSolutions):
                score=0
                sol=problem.figures[str(a+1)]
                imgSol=Image.open(sol.visualFilename)
                pairsCD,notPaired=self.get_Pairs(C,sol)   
                print("row rotation is:")
                print(D['rowRotation'])
                
                if(D['numObjects']==len(sol.objects)):
                    score=score+2                
                if(D['flip_horizontal'] and self.isFlipped(ImgC,imgSol,"horizontal")):
                    score=score+2
                if(D['flip_vertical'] and self.isFlipped(ImgC,imgSol,"vertical")):
                    score=score+2   
                if(D['rowRotation']>0) and self.isRowRotated(ImgC, images[figPrev2[i]], imgSol, D['rowRotation']):
                    score=score+2
                DPsol=self.getDP(imgSol)
                if(D['darkPixels']>0):
                    score=score-1.5*(abs(DPsol-D['darkPixels'])/D['darkPixels'])
                DPcontoursol=self.getDPcontour(imgSol)
                if(D['darkPixelsContour']>0):
                    score=score-0.6*(abs(DPcontoursol-D['darkPixelsContour'])/D['darkPixelsContour'])
                    
                solX,solY=self.getCOM(imgSol)
                score=score-(0.5*abs(solX-D['COMX'])/D['COMX'])
                score=score-(0.5*abs(solY-D['COMY'])/D['COMY'])
                
                solX,solY=self.getMOI(imgSol)
                score=score-(0.3*abs(solX-D['MOIX'])/D['MOIX'])
                score=score-(0.3*abs(solY-D['MOIY'])/D['MOIY'])
                
                for key, value in pairsCD.items():
                    if(key in D):
                        shape=str(D[key][0])
                        size=str(D[key][1])
                        fill=D[key][2]
                        angle=D[key][3]
                        alignment=[D[key][6],D[key][7]]
                        if('shape' in sol.objects[value].attributes and shape==shapesEnum[sol.objects[value].attributes['shape']]):
                            score=score+1
                        if('size' in sol.objects[value].attributes and size==sizesEnum[sol.objects[value].attributes['size']]):
                            score=score+1
                        if('fill' in sol.objects[value].attributes and fill==fillEnum[sol.objects[value].attributes['fill']]):                  
                            score=score+1
                        if('angle' in sol.objects[value].attributes and angle==(int(sol.objects[value].attributes['angle'])%360)):
                            score=score+1
                        if('alignment' in sol.objects[value].attributes and alignment==alignmentEnum[sol.objects[value].attributes['alignment']]):
                            score=score+1
                    #else:
                     #   score=score-2
                solutions[i][a]=score
            i=i+1
        solutions_combined=np.add(solutions[0],solutions[1])
        max_score=max(solutions_combined)
        max_index=solutions_combined.tolist().index(max_score)
        #print(solutions)
        return max_index +1