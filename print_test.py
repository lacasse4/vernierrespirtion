
# Python program to demonstrate 
# object printing 
  
  
# Defining a class 
class Test:  
    def __init__(self, a, b):  
        self.a = a  
        self.b = b  
      
    def __repr__(self):  
        # return "Test a:% s b:% s" % (self.a, self.b)
        return str(vars(self))
    
    def __str__(self):  
        return "From str method of Test: a is % s, b is % s" % (self.a, self.b)  
  
# Driver Code          
t = Test(1234, 5678)  
  
# This calls __str__()  
print(t)  
  
# This calls __repr__()  
print([t]) 
