import maya.cmds as maya
import random
groupcounters = {}
trainReference = 0
while maya.objExists("train"+str(trainReference)):
    trainReference += 10000
        

def makeGroup(lst, type = "group"):
    global groupcounters
    global trainReference
    counter = groupcounters.get(str(type), 0)
    groupcounters[str(type)] = counter + 1
    n = str(type) + str(counter + trainReference)
    return maya.group(lst, name = n)
        
def fltrng(num1, num2 = None, inc = 1):
    if num2 == None:
        min = 0
        max = num1
    else:
        min = num1
        max = num2
        
    lst = []
    num = min
    while num < max:
        lst.append(num)
        num += inc
    return lst

# creates a wheel and returns a reference to it. For the moment it's just a disc but I hope to replace it soon with something better
def wheel(radius):    
    wheel = maya.polyCylinder(r= radius, h = .1)[0]
    maya.rotate(90,0,0)
    return wheel

#creates a par of wheels touching the 'ground' at y = -1. the size and width are given. you can optionally specify a position x to place them at.
def wheelPair(size, width, x: float = 0):
    height = -1+size
    wheels = []
    active = wheel(size)
    wheels.append(active)
    maya.move(x,height,-width, active)
        
    active = wheel(size)
    wheels.append(active)
    maya.move(x, height,width)
    return makeGroup(wheels, "wheelPair")
    

def metalSheet():
    #each will be .5 wide, with rivets going up and down
    metal = []
    metal.append(maya.polyCube(w=.45, h = .8, d =.1)[0])
    
    
    for x in [.175, -.175]:
       
        rivet = maya.polyCylinder(r=.015,h =.125)[0]
        metal.append(rivet)
        maya.rotate(90, 0,0)
        maya.move(x, .35, 0, r= True)
        for i in fltrng(.07, .78, .08):
            metal.append(maya.duplicate(rivet)[0])
            maya.select(metal[-1])
            maya.move(0, -i, 0, r= True)
    
    metal = makeGroup(metal, "metal")
    maya.move(0,.05,0,r = True)
    return metal


def archwindow():
    win = []
    dim = .055
#1 wide, .66 tall base and .33 tall arch.

#left and right squares
    for x in [0.25, -0.25]:
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #bottom
        maya.move(x, 0,x/10)
        win.append(active)  
        active = maya.polyCube(w=dim,h=.66,d=dim)[0]  #left
        win.append(active)  
        maya.move(.275+x, .3026,x/10)
        active = maya.polyCube(w=dim,h=.66,d=dim)[0]  #right
        win.append(active)  
        maya.move(-.275+x, .3026,x/10)
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #top
        win.append(active)  
        maya.move(x,0.6051,x/10)
    
        #top arch
    active = maya.polyCube(w=1.11, h = .33, d= dim*2)[0]
    win.append(active)
    maya.move(0, .797, .025)
    maya.select([active+".e[7]", active + ".e[6]"])
    maya.polyBevel(fraction = 1, segments = 10, offsetAsFraction = True)
            
    return makeGroup(win, "window")

#a doubly linked list meant for storing Car objects
class CarList:
    def __init__(self, obj, pre = None, next = None):
        self.obj = obj
        self.pre = pre
        self.next = next
        self.index = 0
        if pre != None:
            self.index = pre.index + 1
        
    def remove(self):
        self.pre.next = self.next
        if self.next != None:
            self.next.pre = self.pre
    
    def addNode(self, new):
        if self.next == None:
            self.next = new
            new.pre = self
        else:
            self.next.addNode(new)
            
    def getGroup(groupName = None, index = None):
        if index != None:
            if self.index == index:
                return self.obj.grp
            else:
                return self.next.getGroup(groupName, index)
                
        elif groupName !=None:
            if groupName == self.obj.grp:
                return self.obj.grp
            else:
                return self.next.getGroup(groupName, index)
                
        else:
            return self.obj.grp
        




class Car: #builds and holds specified cars
    def __init__(self, carType, train = None, length = 8):
        self.carType = carType
        self.train = train
        self.length = length

        self.parts = self.build()   #list of components
        self.grp = makeGroup(self.parts, carType)     #maya group
        
    
    def build(self):
        if self.carType == "engine":
            return self.engine()
        elif self.carType == "passenger":
            return self.passenger()
        else:
            return False
            
    def getCar(self):
        return self.group

    def engine(self): #makes my basic engine.
        engine = [] #holds the components
            
        active = maya.polyCube(w=8,h=.5,d=2)[0]
        engine.append(active)
        active = maya.polyCube(w=8,h=.5,d=1.5)[0]
        engine.append(active)
        maya.move(0,-.35,0)                

    
        
        active = maya.polyCube(w=2,h=1.5,d=2)[0]
        engine.append(active)
        maya.move(3,1,0)
        active = maya.polyCube(w=2.5,h=.1,d=2.25)[0]
        engine.append(active)
        maya.move(3.125,1.8,0)
        active = maya.polyCube(w=1.25,h=.1,d=1.75)[0]
        engine.append(active)
        maya.move(3,1.9,0)
        active = maya.polyCube(w=4.5,h=.1,d=2.25)[0]
        engine.append(active)
        maya.move(2.25,0,0)
        
        active = maya.polyCylinder(r=.9, h = 6)[0]
        engine.append(active)
        maya.rotate(0,0,90)
        maya.move(-1,.75,0)
        
        size =.45
        for x in [0,2]:
          wheels = wheelPair(size, 1.1, x)
          engine.append(wheels)
            
        size =.35   
        for x in range(2, 5):
            wheels = wheelPair(size, .85, -x+.5)
            engine.append(wheels)
              
        #smokestack
        engine.append(maya.polyCylinder(r=.25, h = 1)[0])
        maya.move(-3,2,0)

        return engine

    def passenger(self):
        car = []
        #base and mechanical bits
        '''little metal hang-y bits and the metal frame the box rests on.
                - diagonal metal bars drooping down and meeting at the middle
                - maybe some machinery?'''

        # wheels
        '''
        Most boxcar type cars had two sets of 4 wheels: one in the front, one in the back.
        they would be held together in a frame with some simple suspension and sit right underneath
        the car.
        Probably be smart to make a function to make one of these and then just call it any time I need boxcar type
        wheels.
        '''
        car.append(self.wheelSet(3))
        car.append(self.wheelSet(-3))
        #Long box for the passengers to go into
        """make a box that only goes about halfway up, leave a gap for windows to go into, then put a rectangle
        cap on top for the roof to go onto. Also make"""

        active = maya.polyCube(w=8,h=1,d=2)[0]
        car.append(active)
        maya.move(0, .1,0)
        active = maya.polyCube(w=8,h=.15,d=2)[0]  
        car.append(active)
        maya.move(0, 1.665, 0)



        #windows running along the midpoint
        '''Lots of types of windows. This might be an oportunity to make different functions for different window
        types'''
        windows = random.randint(1, 2)
        if windows == 1:
            car.append(self.simpleWindows())  
        else:
            car.append(self.archwindows())
        
        #roof
        '''Also lots of ways to do this.'''
        roof = random.randint(1, 4)
        if roof == 1:
            car.append(self.basicroof())  
        elif roof == 2:
            car.append(self.ventroof())
        elif roof == 3:
            car.append(self.curvedroof())
        else:
            car.append(self.railingroof())
        maya.move(0,1.75,0)

        #doorway and stairs to go up to get in
        '''Most passenger cars have roofs that extend over the stairs, and the box just ends early. Put a
        door there and some windows on either side'''

        #texture and details
        siding = random.randint(1, 2)
        if siding == 1:
            car.append(self.woodSiding())  
        else:
            car.append(self.metalSiding())

        return car


    #Component building functions
    def simpleWindows(self):
        windows = []
        '''These ones are just a bar on top, a bar on bottom, and blocks splitting the windows in between.'''
        length = 8
        width = 2
        l = length/2
        w = width/2
        #baseboard
        active = maya.polyCube(w=length+.1,h=.1,d=.1)[0]  
        windows.append(active)
        maya.move(0, .51, -w)
        active = maya.polyCube(w=length +.1,h=.1,d=.1)[0]  
        windows.append(active)
        maya.move(0, .51, w)
          
        #car ends
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(l-.25,1.1,w-.05)
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(-l+.25,1.1,w-.05)
                
                
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(l-.25,1.1,-w+.05)
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(-l+.25,1.1,-w+.05)
        
        row = []
        #make an actual window
        
        start = -length/2+.8
        end = length/2-.5-.61/2
        winspace = length-1
        numwindows = (length-.8)//.81
        inc = (end-start)/numwindows
        for x in fltrng(start, end, inc):
            active = self.simpleWindow()
            row.append(active)
            maya.move(x, .6, -w)
        numsep = int(numwindows-1)
        width = (length-1-(.61*numwindows))/numsep
        start = start+.56-width/2
            #seperators
        for x in fltrng(start, end+.1, inc):
            active = maya.polyCube(w=width,h=1.2,d=.05)[0]  
            row.append(active)
            maya.move(x, 1.05, -w+.05)
        row = makeGroup(row, "windowRow")
        windows.append(row)
        
        #other side's windows
        
        
        row = []
        
        start = -length/2+.8
        end = length/2-.5-.61/2
        winspace = length-1
        numwindows = (length-.8)//.81
        inc = (end-start)/numwindows
        for x in fltrng(start, end, inc):
            active = self.simpleWindow()
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x, .6, w-0.055)
        numsep = int(numwindows-1)
        width = (length-1-(.61*numwindows))/numsep
        start = start+.56-width/2
            #seperators
        for x in fltrng(start, end+.1, inc):
            active = maya.polyCube(w=width,h=1.2,d=.05)[0]  
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x, 1.05, w-.05)
        row = makeGroup(row, "windowRow")
        windows.append(row)
        
        return makeGroup(windows, "simpleWindows")
        


    def archwindows(self, length = 8, width = 2):
    
        windows = []
        l = length/2
        w = width/2
            #baseboard
        active = maya.polyCube(w=8,h=.1,d=.1)[0]  
        windows.append(active)
        maya.move(0, .51, -w)
        active = maya.polyCube(w=8,h=.1,d=.1)[0]  
        windows.append(active)
        maya.move(0, .51, w)
            #car ends
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(l-.25,1.1,w-.05)
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(-l+.25,1.1,w-.05)
        
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(l-.25,1.1,-w+.05)
        active = maya.polyCube(w=.5,h=1,d=.1)[0]  
        windows.append(active)
        maya.move(-l+.25,1.1,-w+.05)
         
        row = []
            #make an actual window
        for x in range(32, -28, -12):
            active = archwindow()
            row.append(active)
            maya.move(x/8-1, .6, -w)
            #seperators
        for x in range(20, -28, -12):
            active = maya.polyCube(w=.45,h=1.2, d=.05)[0]  
            row.append(active)
            maya.move(x/8-.25, 1, -w+.05)
        active = maya.polyCube(w=8,h=.3, d=.05)[0]  
        row.append(active)
        maya.move(0, 1.42, -w+.05)
        row = makeGroup(row, "windowRow")
        maya.move(0, .029, 0, r= True)
        windows.append(row)
            
            #other side's windows
        row = []
    
        for x in range(32, -28, -12):
            active = archwindow()
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x/8-1, .6, w-0.055)
            
    
        for x in range(20, -28, -12):
            active = maya.polyCube(w=.45,h=1.2, d=.05)[0]  
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x/8-.25, 1, w-.05)
        active = maya.polyCube(w=8,h=.3, d=.05)[0]  
        row.append(active)
        maya.move(0, 1.42, w-.05)
        row = makeGroup(row, "windowRow")
        maya.move(0, .029, 0.025, r= True)
        windows.append(row)
        
        return makeGroup(windows, "archWindows")
        
    def simpleWindow(self):
        win = []
        dim = .055
        #outer frame
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #bottom
        win.append(active)  
        active = maya.polyCube(w=dim,h=1.08,d=dim)[0]  #left
        win.append(active)  
        maya.move(.275, .513,0)
        active = maya.polyCube(w=dim,h=1.08,d=dim)[0]  #right
        win.append(active)  
        maya.move(-.275, .513,0)
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #top
        win.append(active)  
        maya.move(0,1.0255,0)
        #inner slidey bit
        dim = .04
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #top
        win.append(active)  
        maya.move(0,.95,0.055)
        active = maya.polyCube(w=.5,h=dim,d=dim)[0]    #bottom
        win.append(active)  
        maya.move(0,.7,0.055)
        for x in [-.25, 0, .25]:
            active = maya.polyCube(w=dim,h=.25,d=dim)[0]
            win.append(active)  
            maya.move(x,.825,0.055)
            
        return makeGroup(win, "window")
        
        
    
        
    
    def basicroof(self):
        roof = []
        length = self.length +.25
        active = maya.polyCube(w=length, h = .2, d = 2.25)[0]
        roof.append(active)
        active = maya.polyCylinder(r=1.125, h = length)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.1,0)
        maya.scale(.1,1,1)
        
        active = maya.polyCube(w=length-1, h = .2, d = 1.25)[0]
        roof.append(active)
        maya.move(0,.2, 0)
        
        active = maya.polyCylinder(r=.625, h = length-1)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.3,0)
        maya.scale(.125,1,1)
        
        return makeGroup(roof, "roof")



    def railingroof(self):
        roof = []
        #base
        length = self.length+.25
        active = maya.polyCube(w=length, h = .2, d = 2.25)[0]
        roof.append(active)
        active = maya.polyCylinder(r=1.125, h = length)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.1,0)
        maya.scale(.1,1,1)
        
        #top parts
        width = self.length/2 -1.5
        for x in [width, -width]:
            active = maya.polyCube(w= .6, h = .2, d = .6)[0]
            roof.append(active)
            maya.move(x,.3, 0)
            active = maya.polyCube(w = .85, h = .1, d = .85)[0]
            roof.append(active)
            maya.move(x,.4,0)
        
        
        #railing 1
        
        for w in [.9, -.9]:
            roof.append(maya.polyCylinder(r=.05, h = length-1)[0])
            maya.rotate(0,0,90)
            maya.move(0, .3, w)
            max = self.length/2
            min = -max+1
            for x in fltrng(min, max):
                roof.append(maya.polyCylinder(r=.02, h = .2)[0])
                maya.move(x, .2, w)
                
        
        
        return makeGroup(roof, "roof")
    

    
    def ventroof(self):
        roof = []
        #base
        length = self.length +.25
        active = maya.polyCube(w= length, h = .2, d = 2.25)[0]
        roof.append(active)
        active = maya.polyCylinder(r=1.125, h = length)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.1,0)
        maya.scale(.1,1,1)
        
        #top part
        width = self.length/2-1.5
        for x in [width, -width]:
            dim = 1.5
            active = maya.polyCube(w= dim, h = .15, d = dim)[0]
            roof.append(active)
            maya.move(x,.4, 0)
            dim = 1
            active = maya.polyCube(w= dim, h = .3, d = dim)[0]
            roof.append(active)
            maya.move(x,.2, 0)
                
        return makeGroup(roof, "roof")


    def curvedroof(self):
        roof = []
        #base
        length = self.length+.25
        active = maya.polyCube(w= length, h = .2, d = 2.25)[0]
        roof.append(active)
        active = maya.polyCylinder(r=1.125, h = length)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.1,0)
        maya.scale(.1,1,1)
        
        #canopy thing
        roof.append(maya.polyCube(w=length-.25, h = .15, d = 1.25)[0])
        maya.move(0,.2,0)
        active = maya.polyCube(w=self.length-.25, h = .25, d = 1.25)[0]
        roof.append(active)
        maya.move(0,.4,0)
        maya.select([active+ ".e[6]", active+ ".e[7]"])
        maya.polyBevel(fraction = 1, segments = 10, offsetAsFraction = True)
        
        for d in [.5, -.5]:
            active = maya.polyCube(w=length, h = .45, d = .25)[0]
            roof.append(active)
            maya.move(0,.4, d)
            maya.select([active+ ".e[6]", active+ ".e[7]"])
            maya.polyBevel(fraction = 1, segments = 10, offsetAsFraction = True)
            
        
        for d in [.65, -.65]:
            active = maya.polyCube(w = length - .5, h = .25, d = .25)[0]
            roof.append(active)
            maya.move(0,.3, d)
            maya.select([active+ ".e[6]", active+ ".e[7]"])
            maya.polyBevel(fraction = 1, segments = 10, offsetAsFraction = True)
        
        return makeGroup(roof, "Canopy")

    def wheelSet(self, x = 0):
        wheels = []
        wheels.append(wheelPair(.25, .85,.5+x))
        wheels.append(wheelPair(.25, .85,-.5+x))
            #long connectors
        active = maya.polyCube(w=.4 , h=.01, d=1.9)[0]
        wheels.append(active)
        maya.move(0+x,-.9,0, r= True)   
        active = maya.polyCube(w=.4 , h=.1, d=1.9)[0]
        wheels.append(active)
        maya.move(0+x, -.71, 0, r = True)
        
            #brakes and springs
        d = -.85
        active = maya.polyCube(w=1.19,h=.1,d=.2)[0]
        wheels.append(active)
        maya.move(0+x,-.6,d,r=True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(.1+x, -.8, d, r = True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(-.1+x, -.8, d, r = True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(0+x, -.8, .1+d, r = True)
    
        active = maya.polyCube(w=.1 , h=.1, d=.1)[0]
        wheels.append(active)
        face = active+ ".f[3]"
        maya.select(face)
        maya.scale(.5)
        maya.select(active)
        maya.scale(1,2,1)
        maya.move(.55+x, -.7, d-.05, r=True)
        
        
        active = maya.polyCube(w=.1 , h=.1, d=.1)[0]
        wheels.append(active)
        face = active+ ".f[3]"
        maya.select(face)
        maya.scale(.5)
        maya.select(active)
        maya.scale(1,2,1)
        maya.move(-.55+x, -.7, d-.05, r=True)
        
        #other side
        d = +.85
        active = maya.polyCube(w=1.19,h=.1,d=.2)[0]
        wheels.append(active)
        maya.move(0+x,-.6,d,r=True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(.1+x, -.8, d, r = True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(-.1+x, -.8, d, r = True)
        active = maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)[0]
        wheels.append(active)
        maya.move(0+x, -.8, -.1+d, r = True)
    
        active = maya.polyCube(w=.1 , h=.1, d=.1)[0]
        wheels.append(active)
        face = active+ ".f[3]"
        maya.select(face)
        maya.scale(.5)
        maya.select(active)
        maya.scale(1,2,1)
        maya.move(.55+x, -.7, d+.05, r=True)
        
        
        active = maya.polyCube(w=.1 , h=.1, d=.1)[0]
        wheels.append(active)
        face = active+ ".f[3]"
        maya.select(face)
        maya.scale(.5)
        maya.select(active)
        maya.scale(1,2,1)
        maya.move(-.55+x, -.7, d+.05, r=True)
    
        wheelgroup = makeGroup(wheels, "wheelSet")
            
        return wheelgroup
        
        
    def woodSiding(self, length = 8, width = 2):
        #make a board
        #lets make each pair of sticky-outy and not sticky-outy boards take up .5 squares for easy repition
        #move into position
        #repeat
        wood = []
        for depth in [-width/2, width/2]:
            siding = []
            for i in range(0, length*2):
                i = (i-length)/2+.25
                siding.append(maya.polyCube(w=.25,h= 1, d=.1)[0])
                maya.move(-.25/2+i, 0,.025, r=True)
                siding.append(maya.polyCube(w=.25, h=1, d=.1)[0])
                maya.move(+.25/2+i, 0,-0.025, r=True)
                
            grp = makeGroup(siding, "siding")
            maya.move(0, 0 ,depth, r = True)
            wood.append(grp)
        
        return makeGroup(wood, "woodSiding")
        
    def metalSiding(self, length = 8, width = 2):
        metal = []
        for depth in [-width/2, width/2]:
            siding = []
            for i in range(0, length*2):
                siding 
                i = (i-length)/2+.25
                
                
                siding.append(metalSheet())
                maya.move(i, 0, 0, r=True)
                
                
            grp = makeGroup(siding, "siding")
            maya.move(0, 0 ,depth, r = True)
            metal.append(grp)
            
    
        
        return makeGroup(metal, "metalSiding")



class Train:
    def __init__(self, type = None, length = None, translate = (0,0,0), numcars = None):
        self.cars = []
        firstCar = Car("engine", self)
        self.carlist = CarList(obj = firstCar)
        self.cars.append(firstCar.grp);
        self.length = firstCar.length/2+1

        self.grp = makeGroup(self.cars, "train")
        if numcars == None:
            numcars = random.randint(1, 25)
        
        cars = ["passenger"]
        
        for car in range(numcars):
            type = random.choice(cars)
            self.addCar(type)
            

    #self, carType, train = None, length = 8
    def addCar(self, new, length = 8):
        car = Car(new, self, length)
        self.cars.append(car)
        self.carlist.addNode(CarList(car))
        maya.select(car.parts)
        maya.parent(car.grp, self.grp)
        maya.move(self.length+car.length/2, 0, 0, r=True)
        self.length+= car.length +1




myFirstTrain = Train(numcars = 5)





        
#car = Car("Passenger")

#making a flatbed car

length = 8
width = 2

car =[]
car.append(maya.polyCube(w= length, h = .25, d = width)[0])

base =[]
offset = .05
for x in fltrng(-length/2+.25/2, length/2+.01, .25):
    base.append(maya.polyCube(w = .25, h = .1, d = width+.15)[0])
    maya.move(x, .25/2, offset)
    offset *=-1
    





car.append(makeGroup(base, "platform")


    

 
