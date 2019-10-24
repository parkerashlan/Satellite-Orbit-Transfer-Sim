#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:31:54 2019

@author: ashlan
"""

import SatteliteOrbitV1 as s
from numpy import linspace
import matplotlib.pyplot as plt

LEO = 6.37e6+2e6
GEO = 6.37e6+3.578e6
msat = 5443.11
mearth = 5.872e24
    
satellite_LEO = s.Body(msat,LEO,0)
satellite_GEO = s.Body(msat,-GEO,0)
transferorb = s.HohmannTransfer(LEO,GEO)
    
LEO = s.Orbit(mearth, satellite_LEO.r, satellite_LEO.vel(mearth))
GEO = s.Orbit(mearth, satellite_GEO.r, satellite_GEO.vel(mearth))
transfer = s.Orbit(mearth, satellite_LEO.r, transferorb.vel(mearth)[0])
    
t = linspace(0,10000,900)
t_transf = linspace(0,transferorb.TOF(mearth),900)
    
orbitpos_LEO = LEO.OrbitPos(LEO.rv,t,mearth)
orbitpos_GEO = GEO.OrbitPos(GEO.rv,t,mearth)
orbitpos_transfer = transfer.OrbitPos(transfer.rv, t_transf, mearth)
    
x_LEO = orbitpos_LEO[0]
y_LEO = orbitpos_LEO[1]
x_GEO = orbitpos_GEO[0]
y_GEO = orbitpos_GEO[1]
x_transf = orbitpos_transfer[0]
y_transf = orbitpos_transfer[1]
    
xlim = 2e7
ylim = 2e7
    
ani1 = s.Animate.ani(xlim,ylim,x_LEO,y_LEO)

ani2 = s.Animate.ani(xlim,ylim,x_transf,y_transf)
    
ani3 = s.Animate.ani(xlim,ylim,x_GEO, y_GEO)
    
plt.show(ani1)
