import maya.cmds as maya
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
    return maya.group(wheels)


#a doubly linked list meant for storing Car objects
class CarList:
    def __init__(self, obj, pre = None, next = None):
        self.obj = obj
        self.pre = pre
        self.next = next
        
    def remove(self):
        self.pre.next = self.next
        if self.next != None:
            self.next.pre = self.pre
    
    def addNode(self, new):
        if self.nxt == None:
            self.next = new
            new.pre = self
        else:
            self.next.addCar(new)
        




class Car: #builds and holds specified cars
    def __init__(self, carType, train = None, x = 0, y = 0, z = 0):
        self.carType = carType
        self.train = train

        self.parts = self.build()   #list of components
        self.group = maya.group(self.parts)     #maya group
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
        #roof
        '''Also lots of ways to do this.'''

        #doorway and stairs to go up to get in
        '''Most passenger cars have roofs that extend over the stairs, and the box just ends early. Put a
        door there and some windows on either side'''

        #texture and details

        return car


    #Component building functions
    def simpleWindows(self):
        windows = []
        '''These ones are just a bar on top, a bar on bottom, and blocks splitting the windows in between.'''

        return maya.group(windows)


    def wheelSet(self, x = 0):
        wheels = []
        wheels.append(wheelPair(.25, .85,.5+x))
        wheels.append(wheelPair(.25, .85,-.5+x))
        wheelgroup = maya.group(wheels)
        #make a frame
        #make the connector
        #call wheel pair twice and properly arrange them
        #desired details
        return wheelgroup


class Train:
    def __init__(self):
        self.cars = []
        firstCar = Car("engine", self)
        self.carlist = CarList(obj = firstCar)
        self.cars.append(firstCar)
    
    def addCar(self, new, x = 0, y= 0, z= 0):
        car = Car(new, self, x, y, z)
        self.cars.append(car)
        self.carlist.addNode(CarList(car))


car = Car("passenger")



    


#myFirstTrain = Train()
#print(myFirstTrain.cars)

#for reference only
#maya.polyCube(w=8,h=2.5,d=2)[0]
#car = []


#active = maya.polyCube(w=8,h=1,d=2)[0]
#car.append(active)
#maya.move(0, .1,0)
#active = maya.polyCube(w=8,h=.15,d=2)[0]  
#car.append(active)
#maya.move(0, 1.665, 0)


#leave buffer 1 tall for windows. They go here.
#active = maya.polyCube(w=8,h=1,d=2)[0]  
#car.append(active)
#maya.move(0, 1.1, 0)

#wheelPair(size, width, x: float = 0):
    


