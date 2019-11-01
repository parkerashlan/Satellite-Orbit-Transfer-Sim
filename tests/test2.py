#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 02:35:19 2019

@author: ashlan
"""
import SatteliteOrbitV1 as s
from numpy import linspace
import matplotlib.pyplot as plt

LEO = 6.7e6 #400km orbit
GPS = 2.67e7 #20,200km orbit (same as GPS satellites)
msat = 5443.11 #average mass of a satellite
mearth = 5.972e24

sat_LEO = s.Body(msat,LEO,0)
sat_GPS = s.Body(msat,GPS,0)
torb = s.HohmannTransfer(LEO,GPS)

LEO = s.Orbit(mearth, sat_LEO.r, sat_LEO.vel(mearth))
GEO = s.Orbit(mearth, sat_GPS.r, sat_GPS.vel(mearth))
transfer = s.Orbit(mearth, sat_LEO.r, torb.vel(mearth)[0])
    
t = linspace(0,86400,1000) #define time of orbit and how many steps you want it to take
t_transf = linspace(0,torb.TOF(mearth),1000)
    
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

print('Impulse needed at perigee:',torb.impulse(sat_LEO.vel(mearth),sat_GPS.vel(mearth))[0])
print('Impulse needed at apogee:',torb.impulse(sat_LEO.vel(mearth),sat_GPS.vel(mearth))[1])

ani1 = s.Animate.ani(xlim,ylim,x_LEO,y_LEO,f='b')

ani2 = s.Animate.ani(xlim,ylim,x_transf,y_transf,f='orange')

ani3 = s.Animate.ani(xlim,ylim,x_GEO, y_GEO,f='orange')

plt.plot(x_LEO,y_LEO,'b-')
plt.plot(x_GEO,y_GEO,'orange')
plt.plot(x_transf,y_transf,'orange')
plt.legend(['Orbit 1','Orbit 2'])