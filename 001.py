import numpy as np
import math,wave

sRate = 44100
nSamples = sRate * 5 # 5 seconds
x=np.arange(nSamples)/float(sRate)
print(x)
vals=np.sin(2*math.pi*220.0*x)
print(vals)
data = np.array(vals*32767,dtype=np.int16).tostring()
file = wave.open('sine220.wav','w')
file.setparams((1,2,sRate,nSamples, 'NONE', 'not compressed'))
file.writeframes(data)
file.close()

