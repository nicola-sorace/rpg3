from math import *

def add(a,b):		#Vector add
	return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def sub(a,b):		#Vector subtract
	return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def fac(n,x):		#Multiply vector by a factor
	return (n*x[0], n*x[1], n*x[2])
def mag(x):			#Return magnitude
	return sqrt(x[0]**2 + x[1]**2 + x[2]**2)
def arg(x):			#Return argument (2D, degrees)
	if x[0] > 0: return degrees(atan(x[1]/x[0]))+90
	if x[0] == 0:
		if x[1]<0: return 0
		return 180
	return degrees(atan(x[1]/x[0]))+270
def uni(x):			#Return unit-vector
	if(mag(x)==0): return (0,0,0)
	return fac(1/mag(x), x)
def polToVec(m,d):	#Generate 2D vector from magnitude and direction
	#return fac( m, uni(math.atan(math.radians(d)),1) ) #UNTESTED
	t = d-90
	if t<0: t = t+360
	r = radians(d-90)

	return fac(m, (cos(r), sin(r), 0) )
def setMag(m,x):	#Set vector's magnitude
	return fac(m, uni(x))
