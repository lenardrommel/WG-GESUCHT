import secondary

param = True
flags = secondary.wrapper_function(param)
if not param:
    print('this works')

def wrapper_function(param):
   myparam = param #get parameters
   print('wrapper called')