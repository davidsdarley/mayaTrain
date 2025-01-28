import maya.cmds as maya

def wheel(radius):
    wheel = maya.polyCylinder(r= radius, h = .1)[0]
    maya.rotate(90,0,0)
    return wheel
    
def wheelPair(size, width, x = 0):
    height = -1+size
    wheels = []
    active = wheel(size)
    wheels.append(active)
    maya.move(x,height,-width, active)
        
    active = wheel(size)
    wheels.append(active)
    maya.move(x, height,width)
    return wheels



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
        




class Car:
    def __init__(self, carType, x = 0, y = 0, z = 0):
        self.carType = carType
        
        self.parts = self.build()
        self.x = x
        self.y = y
        self.z = z
    
    def build(self):
        if self.carType == "engine":
            return self.engine()
        else:
            return False

    def engine(self):
        engine = []
            
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
          for item in wheels:
              engine.append(item)
            
        size =.35   
        for x in range(2, 5):
            wheels = wheelPair(size, .85, -x+.5)
            for item in wheels:
                engine.append(item)
              
        #smokestack
        engine.append(maya.polyCylinder(r=.25, h = 1)[0])
        maya.move(-3,2,0)
    
        return engine





class Train:
    def __init__(self):
        self.cars = []
        firstCar = Car("engine")
        self.carlist = CarList(obj = firstCar)
        self.cars.append(firstCar)
    
    def addCar(self, new, x = 0, y= 0, z= 0):
        car = Car(new, x, y, z)
        self.cars.append(car)
        self.carlist.addNode(CarList(car))






    


myFirstTrain = Train()
print(myFirstTrain.cars)





