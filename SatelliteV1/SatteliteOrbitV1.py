"""
Created on Tue Sep 17 17:54:18 2019

@author: ashlan

Orbit Transfer Simulator

Goal: Simulate and animate the transfer of a sattelite from one orbit to
another.
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib import animation

class Body:
    
    G = 6.678e-11
    
    def __init__(self,m,x,y,z=0,r=0):
        """ Create a new body instance.
        
        m: mass of the body
        x,y,z: x,y,z positions of body
        r: radial distance of the body from the origin
        """
        self.m = m
        self.x = x
        self.y = y
        self.z = z
        self.r = np.sqrt(x**2+y**2)

        
    def reldist(self,xrel = 0,yrel =0):
        """Finds the relative radial distance. If no values inputted for xrel and yrel
        then finds distance from the origin.
        
        xrel: x position of point which you want to find the distance from
        yrel: y position of point which you want to find the distance from       
        """
        self.r = np.sqrt((self.x-xrel)**2+(self.y-yrel)**2)
        
        return self.r
    
    def vel(self,M):
        """Finds the velocity of the body in orbit.
        
        M: mass of the body which is being orbited
        """
        v = np.sqrt((M*Body.G)/self.r)
        
        return v


class HohmannTransfer:
    
    G = 6.678e-11
    
    def __init__(self,r1,r2):
        """Creates a new instance to calculate Hohmann transfer orbit.
        
        r1: radius of orbit 1
        r2: radius of orbit 2
        a: semi-major axis of the transfer orbit
        """
        self.r1 = r1
        self.r2 = r2
        self.a = (r1+r2)/2
        
        
    def vel(self,M):
        """Finds the velocities at the perihelion and aphelion of the
        transfer orbit which are the transfer points of the orbit.
        
        M: mass of body exerting gravitational force on the sattelite
        """
        v_peri = np.sqrt((HohmannTransfer.G*M)*((2/self.r1)-(2/(self.r1+self.r2))))
        
        v_aphe = np.sqrt((HohmannTransfer.G*M)*((2/self.r2)-(2/(self.r1+self.r2))))
        
        return v_peri, v_aphe
    
    def impulse(self,v1,v2):
        """Finds the impulse needed to switch orbits.
        
        v1: velocity of body in orbit 1
        v2: velocity of body in orbit 2
        """
        dv_peri = self.v_peri - v1
        
        dv_aphe = self.v_peri - v2
        
        return dv_peri, dv_aphe
    
    def TOF(self,M):
        """Finds the time of flight in the transfer orbit.
        
        M: mass of the body being orbited
        """
        
        T = np.pi*np.sqrt(self.a**3/(HohmannTransfer.G*M))
        
        return T
        

class Orbit:
     
     
     G = 6.67e-11
     
     def __init__(self, m,r,v):
         """ Creates an orbit instance.
         
         m: mass of the body being orbited
         r: radius of the orbit
         v: velocity of the body orbiting
         """
         self.m = m
         self.r = r
         self.v = v
         self.rv = np.array([-r,0,0,-v])
         
     
     def OrbitPos(self, rv, t, m): 
         """Takes a timespan and an array of an initial position and initial velocity and
         uses them to calculate the orbit of the body. 
         
         rv: array of initial position and initial velocity
         t: a timespan in the form of an array or range of numbers.
            An example would be np.linspace(1,100,99)
         m: mass of the body being orbited
         """
         
         params = np.array(rv)
         params = params.flatten()
         
         def GravityODE(rv,t):
             G = 6.67e-11
             m = 5.972e24
             x = rv[0]
             y = rv[1]
             vx = rv[2]
             vy = rv[3]
             
             dvydt = -((G*m*y)/((x**2+y**2)**(3/2)))
             dvxdt = -((G*m*x)/((x**2+y**2)**(3/2)))
             dxdt = vx
             dydt = vy

             pos_derivs = np.array([dxdt,dydt])
             v_deriv = np.array([dvxdt,dvydt])
             derivs = np.hstack((pos_derivs,v_deriv))
        
             return derivs  
         
         satellite_orbit = integrate.odeint(GravityODE,params,t)
         
         return satellite_orbit[:,0],satellite_orbit[:,1]
        
        
class Animate:
    """Class used to animate the path of the satellite."""
    
    fig = plt.figure()
    
    @staticmethod
    def ani(xlim,ylim,xvals,yvals):
        """Animates the orbit of the satellite using an array of x and y
        positions.
        
        xlim: The x-limit of the graph.
        ylim: The y-limit of the graph.
        xvals: The array of x-values.
        yvals: The array of y-values.
        """
        
        ax = plt.axes(xlim=(-xlim,xlim),ylim=(-ylim,ylim))
        line, = ax.plot([], [], lw=2)
        
        def init():
            line.set_data([], [])
            return line,
        
        def animate(i):
            x = xvals
            y = yvals
            line.set_data(x[:i],y[:i])
            return line,
        
        anim = animation.FuncAnimation(Animate.fig, animate, init_func=init, frames = int(np.size(xvals)),
                                       interval = 1)
        return anim
     
if __name__ == '__main__':
"""Example of a transfer between a low Earth orbit and a Geosynchronous orbit."""

    LEO = 6.37e6+2e6
    GEO = 6.37e6+3.578e6
    msat = 5443.11
    mearth = 5.872e24
    
    satellite_LEO = Body(msat,LEO,0)
    satellite_GEO = Body(msat,-GEO,0)
    transferorb = HohmannTransfer(LEO,GEO)
    
    LEO = Orbit(mearth, satellite_LEO.r, satellite_LEO.vel(mearth))
    GEO = Orbit(mearth, satellite_GEO.r, satellite_GEO.vel(mearth))
    transfer = Orbit(mearth, -satellite_LEO.r, -transferorb.vel(mearth)[0])
    
    t = np.linspace(0,10000,900)
    t_transf = np.linspace(0,transferorb.TOF(mearth),300)
    
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
    
    ani1 = Animate.ani(xlim,ylim,x_LEO,y_LEO)
    
    ani2 = Animate.ani(xlim,ylim,x_transf,y_transf)
    
    ani3 = Animate.ani(xlim,ylim,x_GEO, y_GEO)
    
    plt.show(ani1)
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
