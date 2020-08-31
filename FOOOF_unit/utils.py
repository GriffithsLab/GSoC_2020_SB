""" Function to load common frequency bands (brain waves): theta, alpha, beta and gamma """

def common_fr_bands(range):
  if (range =='theta'):
    bands = {'theta' : [4, 8]}
  elif (range =='alpha'):
    bands = {'alpha' : [8, 13]} 
  elif (range =='beta'):
    bands = {'beta' : [13, 30]} 
  elif (range =='gamma'):
    bands = {'gamma' : [30, 50]}    
  else:
    bands = {'theta' : [4, 8], 'alpha' : [8, 13], 'beta' : [13, 30], 'gamma' : [30, 50]}
  return bands
