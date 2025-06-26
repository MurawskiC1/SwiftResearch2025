
import pandas as pd
import os

'''https://www.zooniverse.org/projects/murawskic1/carter-project'''
#OPEN PANPOTRES AND FIND RIGHT PROJECT

count = 0 

class BurstChaser():
    def __init__(self, Burst_Name, BurstID, workflow, Verify = None):
        self.Burst_Name = Burst_Name
        self.BurstID = BurstID
        self.workflow = workflow
        self.Verify = Verify
        self.contributers = []
        


    
    @property
    def Burst_Name(self):
        return self._Burst_Name
    
    @Burst_Name.setter
    def Burst_Name(self, i):
        self._Burst_Name = i
    
    @property
    def BurstID(self):
        return self._BurstID
    
    @BurstID.setter
    def BurstID(self, i):
        self._BurstID = i
        
    @property
    def workflow(self):
        return self._workflow 
    
    @workflow.setter
    def workflow(self, i):
        self._workflow = i
    @property
    def contributers(self):
        return self._contributers 
    
    @contributers.setter
    def contributers(self, i):
        self._contributers = i
    @property
    def Verify(self):
        return self._Verify
    
    @Verify.setter
    def Verify(self, v):
        self._Verify = v
        
    def retire(self):
        global count
        if self.Verify != None:
            count += 1
           
            
            #workflow = Workflow.find(f"{self.workflow}")
            #workflow.retire_subjects(f"{self.BurstID}")
      

        
        
    def contributersAdd(self, c):
        self.contributers.append(c)
    
    @staticmethod
    def findPNG(name, path="BurstPhotos"):
        for filename in os.listdir(path):
            if name in filename and os.path.isfile(os.path.join(path, filename)):
                return filename #return path and file name os.path.join(path, filename)
        return "None"

            
    def __lt__(self, other):
        return self.BurstID < other.BurstID
   

#This Class will start to rank all the bursts and catagorize them by their 
class PulseShape(BurstChaser):
    def __init__(self, Burst_Name, BurstID, workflow):
        super().__init__(Burst_Name, BurstID, workflow)
        self.Follow = [0,0,0,0,0,0]
        self.Shape = [0,0,0,0]
    
    @property
    def Shape(self):
        return self._Shape
    
    @property
    def Follow(self):
        return self._Follow
    
    @Shape.setter
    def Shape(self, i):
        self._Shape = i 
    #The japanese wife that I met online and I are hitting it off pretty well and let me tell you, i am so in love with her. Im moving next week. WOW!
    
    
        
    @Follow.setter
    def Follow(self, f):
        self._Follow = f

    def __str__(self):
        #return f"{self.BurstID}:  Simple:{self.Shape[0]}  Ext:{self.Shape[1]}  Other:{self.Shape[2]} Follow Up:{self.Follow}"
        return f"{self.BurstID}:  Shape:{self.Shape}  Follow Up:{self.Follow} Verified:{self.Verify}"
    

    
    #code to add to definer array
    def FollowCount(self, j):
        if 'Pulses connected with underlying emission.' in j: 
            self.Follow[2] += 1
        if 'symmetrical structure' in j:
            self.Follow[0] += 1
        if "One or more pulses with the fast-rise and slow-decay shape." in j:
            self.Follow[1] += 1
        if 'Rapid Varying pulses' in j:
            self.Follow[3] += 1
        if "I don't see any of these" in j:
            self.Follow[4] += 1
        if "too noisy" in j:
            self.Follow[5] += 1

    def ShapeCount(self, shape):
        if "extended emission" in shape:
            self.Shape[1] += 1
        elif "simple pulse" in shape:
            self.Shape[0] += 1
        elif "Other." in shape:
            self.Shape[2] +=1
        elif "too noisy" in shape:
            self.Shape[3] +=1
        #Verify iif burst has met the requirements

       

            
    def export(name, pulse_list):
        pulse_list = sorted(pulse_list)
        data = {'Burst_Name': [i.Burst_Name for i in pulse_list],
                'Burst_PNG': [PulseShape.findPNG(i.Burst_Name) for i in pulse_list],
                'Simple': [i.Shape[0] for i in pulse_list],
                'Extended': [i.Shape[1] for i in pulse_list],
                'Other': [i.Shape[2] for i in pulse_list],
                'Too_Noisy': [i.Shape[3] for i in pulse_list],
                'Follow': [i.Follow for i in pulse_list]
                }
        df = pd.DataFrame(data)
        #creates data frame as csv file 
        df.to_csv(f'CSVExports/{name}.csv', index = False, header = True)


#class for the Pulse or noise
class PulseNoise(BurstChaser):
    def __init__(self, Burst_Name, BurstID, workflow):
        super().__init__(Burst_Name, BurstID, workflow)
        self.classification = [0,0,0,0]
        
  
    @property
    def classification(self):
        return self._classification

        
    @classification.setter
    def classification(self, i):
        self._classification = i
        
    def classCount(self, a):
        if "This is a pulse." in a:
            self.classification[0] += 1
            
        elif "This is noise." in a:
            self.classification[1] += 1
        elif "It's hard to tell." in a: 
            self.classification[2] += 1
        else:
            self.classification[3] += 1
    
    def __str__(self):
        return f"{self.BurstID}: Classification: {self.classification}"
    
    def export( name, pulse_list):
        pulse_list = sorted(pulse_list)
        data = {'Burst Name': [i.Burst_Name for i in pulse_list],
                'Burst ID': [i.BurstID for i in pulse_list],
                'Pulse': [i.classification[0] for i in pulse_list],
                "Noise": [i.classification[1] for i in pulse_list],
                'Cant Tell': [i.classification[2] for i in pulse_list],
                'No Response': [i.classification[3] for i in pulse_list]
                }
        df = pd.DataFrame(data)
        #creates data frame as csv file 
        df.to_csv(f'CSVExports/{name}.csv', index = True, header = True)


class PulseLocation(BurstChaser):
    def __init__(self, Burst_Name, BurstID, workflow):
        super().__init__(Burst_Name, BurstID, workflow)
        self.locations =  []

        self.count = 0 

    @property
    def count(self):
        return self._count
    
    @count.setter
    def count(self ,i):
        self._count = i
    
    @property
    def locations(self):
        return self._locations

        
    @locations.setter
    def locations(self, i):
        self._locations = i

            
    

        
        
    def read(self, a):
        a = a.split(' which is automatically determined by a computer algorithm.","value":[')[1]
        self._count += 1
        if '},{' in a:
            a = a.split('},{')
        else:
            a = [a]
        for i in a:
            cata = i.split(",")
            if len(cata) >4:
                loc = Location(float(cata[0].split(":")[1]),float(cata[1].split(":")[1]), float(cata[4].split(":")[1]),float(cata[5].split(":")[1]))
                self.locations.append(loc)
 
        

    def findGRB(self, sid):
        file = pd.read_csv("GRB_IDS_Names.csv")
        file.set_index('Subject_ID', inplace=True)

        return file.loc[sid,'GRB_Names']
               
            
            
    def export(name, pulse_list):
        Burst_Name = []
        BurstID =[]
        x = []
        y = []
        h = [] 
        w = []
        
        for i in sorted(pulse_list):
            if len(i.locations) != 0:
                Burst_Name.append(i.Burst_Name)
                BurstID.append(i.BurstID)
                tempx = []
                tempy = []
                temph = []
                tempw = []
                for j in i.locations:
                    tempx.append(j.x)
                    tempy.append(j.y)
                    tempw.append(j.width)
                    temph.append(j.height)
                x.append(tempx)
                y.append(tempy)
                h.append(temph)
                w.append(tempw)



        print(len(x))
        print(len(Burst_Name))
        
        data = {'Burst Name': Burst_Name,
            
                'X_Locations': x,
                'Y_Locations': y,
                'Heights': h,
                'Widths': w
                }
        df = pd.DataFrame(data)
        #creates data frame as csv file 
        df.to_csv(f'CSVExports/{name}.csv', index = True, header = True)
        

                    


        


class Location():
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @x.setter
    def x(self, i):
        self._x = i
    
    @y.setter
    def y(self, i):
        self._y = i
        
    @width.setter
    def width(self, i):
        self._width = i
    
    @height.setter
    def height(self, i):
        self._height = i
