import maya.cmds as maya
import random
groupcounters = {}

def checkGroupName(type, num):
    global groupcounters
    n = type + str(num)
    
    if maya.objExists(n):
        groupcounters[type] = num
        return checkGroupName(type, num+100)
    else:
        groupcounters[type] = num + 1
        return n

def makeGroup(lst, type = "group"):
    global groupcounters
    counter = groupcounters.get(type, 0)
    return maya.group(lst, name = checkGroupName(type, counter))
        

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
    def __init__(self, carType, train = None, x = 0, y = 0, z = 0):
        self.carType = carType
        self.train = train

        self.parts = self.build()   #list of components
        self.grp = makeGroup(self.parts, carType)     #maya group
        self.x = x
        self.y = y
        self.z = z
    
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
        active = self.simpleWindows()
        car.append(active)
        #roof
        '''Also lots of ways to do this.'''
        car.append(self.roof())
        maya.move(0,1.75,0)

        #doorway and stairs to go up to get in
        '''Most passenger cars have roofs that extend over the stairs, and the box just ends early. Put a
        door there and some windows on either side'''

        #texture and details

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
        for x in range(32, -35, -8):
            active = self.simpleWindow()
            row.append(active)
            maya.move(x/10, .6, -w)
            
        #seperators
        for x in range(28, -35, -8):
            active = maya.polyCube(w=.2,h=1.2,d=.05)[0]  
            row.append(active)
            maya.move(x/10, 1, -w+.05)
        row = makeGroup(row, "windowRow")
        windows.append(row)
        
        #other side's windows
        row = []

        for x in range(32, -35, -8):
            active = self.simpleWindow()
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x/10, .6, w-0.055)
            

        for x in range(28, -35, -8):
            active = maya.polyCube(w=.2,h=1.2,d=.05)[0]  
            row.append(active)
            maya.rotate(0,180,0)
            maya.move(x/10, 1, w-.05)
        row = makeGroup(row, "windowRow")
        windows.append(row)
        
        
        
        return makeGroup(windows, "simpleWindows")
        
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
        
    
    def roof(self):
        roof = []
        
        active = maya.polyCube(w=8.25, h = .2, d = 2.25)[0]
        roof.append(active)
        active = maya.polyCylinder(r=1.125, h = 8.25)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.1,0)
        maya.scale(.1,1,1)
        
        active = maya.polyCube(w=7.25, h = .2, d = 1.25)[0]
        roof.append(active)
        maya.move(0,.2, 0)
        
        active = maya.polyCylinder(r=.625, h = 7.25)[0]
        roof.append(active)
        maya.rotate(0,0,90)
        maya.move(0,.3,0)
        maya.scale(.125,1,1)
        
        return makeGroup(roof, "roof")



    def wheelSet(self, x = 0):
        wheels = []
        wheels.append(wheelPair(.25, .85,.5+x))
        wheels.append(wheelPair(.25, .85,-.5+x))
        wheelgroup = makeGroup(wheels, "wheelSet")
        #make a frame
        #make the connector
        #call wheel pair twice and properly arrange them
        #desired details
        return wheelgroup


class Train:
    def __init__(self, type = None, length = None, translate = (0,0,0), numcars = None):
        self.cars = []
        firstCar = Car("engine", self)
        self.carlist = CarList(obj = firstCar)
        self.cars.append(firstCar.grp)
        self.grp = makeGroup(self.cars, "train")
        if numcars == None:
            numcars = random.randint(1, 25)
        
        cars = ["passenger"]
        
        for car in range(numcars):
            type = random.choice(cars)
            self.addCar(type)
            length = len(self.cars)*9 -9

            maya.move(length, 0, 0, r=True)
            

    
    def addCar(self, new, x = 0, y= 0, z= 0):
        car = Car(new, self, x, y, z)
        self.cars.append(car)
        self.carlist.addNode(CarList(car))
        maya.select(car.parts)
        maya.parent(car.grp, self.grp)



myFirstTrain = Train(numcars = 2)


#working on fancy wheels

def wheelSet(x = 0):
        wheels = []
        wheels.append(wheelPair(.25, .85,.5+x))
        wheels.append(wheelPair(.25, .85,-.5+x))
        wheelgroup = makeGroup(wheels, "wheelSet")
        #make a frame
        #make the connector
        #call wheel pair twice and properly arrange them
        #desired details
        return wheelgroup

run = wheelSet()

for i in range(0,3):

active = maya.polyCube(w=.4 , h=.01, d=1.9)[0]
maya.move(0,-.3,0, r= True)   
active = maya.polyCube(w=.4 , h=.1, d=1.9)[0]
maya.move(0, -.11, 0, r = True)


maya.polyCube(w=1,h=.1,d=.2)
maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)
maya.move(.1, -.2, 0, r = True)
maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)
maya.move(-.1, -.2, 0, r = True)
maya.polyHelix( radius=.015, height=.2, coils=7, width=0.15)
maya.move(0, -.2, .1, r = True)

active = maya.polyCube(w=.1 , h=.1, d=.1)[0]



face = active+ ".f[3]"
maya.select(face)
maya.scale(.5)


















