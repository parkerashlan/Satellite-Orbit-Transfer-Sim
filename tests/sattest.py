#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:31:54 2019

@author: ashlan

All values based on calculation from 
https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/lecture-notes/MIT16_07F09_Lec17.pdf
"""

import SatteliteOrbitV1 as s
from numpy import linspace
import matplotlib.pyplot as plt

LEO = 6.7e6
GEO = 42.24e6
msat = 5443.11
mearth = 5.972e24
   
satellite_LEO = s.Body(msat,LEO,0)
satellite_GEO = s.Body(msat,GEO,0)
transferorb = s.HohmannTransfer(LEO,GEO)

LEO = s.Orbit(mearth, satellite_LEO.r, satellite_LEO.vel(mearth))
GEO = s.Orbit(mearth, satellite_GEO.r, satellite_GEO.vel(mearth))
transfer = s.Orbit(mearth, satellite_LEO.r, transferorb.vel(mearth)[0])
    
t = linspace(0,86400,1000) #define time of orbit and how many steps you want it to take
t_transf = linspace(0,transferorb.TOF(mearth),1000)
    
orbitpos_LEO = LEO.OrbitPos(LEO.rv,t,mearth)
orbitpos_GEO = GEO.OrbitPos(GEO.rv,t,mearth)
orbitpos_transfer = transfer.OrbitPos(transfer.rv, t_transf, mearth)
    
x_LEO = orbitpos_LEO[0]
y_LEO = orbitpos_LEO[1]
x_GEO = orbitpos_GEO[0]
y_GEO = orbitpos_GEO[1]
x_transf = orbitpos_transfer[0]
y_transf = orbitpos_transfer[1]
    
xlim = 5e7
ylim = 5e7

print('Impulse needed at perigee:',transferorb.impulse(satellite_LEO.vel(mearth),satellite_GEO.vel(mearth))[0])
print('Impulse needed at apogee:',transferorb.impulse(satellite_LEO.vel(mearth),satellite_GEO.vel(mearth))[1])

ani1 = s.Animate.ani(xlim,ylim,x_LEO,y_LEO,f='b')

ani2 = s.Animate.ani(xlim,ylim,x_transf,y_transf,f='orange')

ani3 = s.Animate.ani(xlim,ylim,x_GEO, y_GEO,f='orange')
plt.plot(x_GEO,y_GEO,'orange')
plt.plot(x_LEO,y_LEO,'b-')
plt.plot(x_transf,y_transf,'orange')