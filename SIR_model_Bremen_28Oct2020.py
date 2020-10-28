# -*- coding: utf-8 -*-
#SIR_model.py for Germany

import numpy as np
#import scipy.optimize as opt

import matplotlib.pyplot as plt
#from pylab import *
#import matplotlib.colors as mcolors
#from scipy.optimize import curve_fit
#import math
#from scipy.stats import norm
#import matplotlib.mlab as mlab
#import scipy.special as sp
import datetime
import matplotlib.dates as mdates


# data:
data_file="./new_infections_Bremen.txt"
Binf = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

data_file="./new_deaths_Bremen.txt"
Bdead = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

data_file="./new_recovered_Bremen.txt"
Brec = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

data_file="./new_active_Bremen.txt"
Bact = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")


#data_file="./Krankenhausbetten_beatmet.txt"
#Betten_beatmet = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

#data_file="./Krankenhausbetten_normal.txt"
#Betten_normal = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

#timeax_beds=np.arange(27,35,1)

P=550000.0 # average population size between 1990 and 2018
P1=81800000.0
# parameters: constrained
b= 0.009019 * 1.0/360.0 # birth rate (per year) 
#theta= 0.003024 * 1.0/360.0 # immigration rate of susceptible (people per day)
theta=0.0 # due to closed borders
d= 0.010615 * 1.0/360.0 # death rate of healthy individuals (per year)



# parameters: unconstrained
# infection dynamics:
a= 0.03 # probability that the disease is transmitted upon contact
c= 3.0 # contact rate per susceptible individual

# recovery and mortality
#delta= 0.033 # death rate of infected individuals # based on Chinese data
delta= 0.0005 # death rate of infected individuals # based on GERMAN data


rho= 0.04 # recovery rate for infected individuals

# immunity or not?
sigma= 0.0 # rate of recovered individuals that become susceptible for reinfection

# initialization
tmax=20 # change duration of simulation to switch between parameter adjustment on the timescale of available data and future predictions for an entire year
#tmax=365
dt=1.0

base = datetime.datetime(2020, 10, 10)
timeax = np.array([base + datetime.timedelta(hours=(24 * i))
                  for i in range(tmax)])


S=np.zeros(tmax)
I=np.zeros(tmax)
R=np.zeros(tmax)
D=np.zeros(tmax)
time=np.arange(0,tmax,1)
DDt=np.zeros(tmax-1)
Rnull=np.zeros(tmax-1)


S[0]=P-731.0-2263.0-60.0
I[0]=731.0
R[0]=2263.0
D[0]=60.0

for i in range(tmax-1):
    # manual adjustment of parameter values due to changing human behaviour according to political restrictions or improved therapy
    
    
    # susceptible fraction of population
    dSdt=theta*S[i]+b*S[i]-d*S[i] - a*c*S[i]*I[i]/P + sigma*R[i]
    # infected fraction of population
    dIdt=a*c*S[i]*I[i]/P - delta*I[i] - rho*I[i]
    # recovered fraction of population
    dRdt=rho*I[i] - sigma*R[i] - d*R[i]
    
    S[i+1]=S[i]+dSdt*dt
    I[i+1]=I[i]+dIdt*dt
    R[i+1]=R[i]+dRdt*dt
    D[i+1]=D[i]+delta*I[i]*dt
    
    DDt[i]=np.log(2.0)/np.log(1.0+a*c*S[i])
    Rnull[i]=(a*c)/(rho)
    

print 'total fatalities=', D[tmax-1]


plt.figure(1)
#plt.plot(time,S,'b',label='susceptible')
plt.plot(time,I+R,'r',label='infected cumulative')
plt.plot(time,I,'m',label='infected active')
#plt.plot(time,I*0.12/0.02,'y',label='potentially infected') # potential to determine undetected cases by using the statistics of RKI on Pneumonia in comparison to Bremen data.
plt.plot(time,R,'g',label='recovered')
plt.plot(time,D,'c',label='dead')
#plt.plot(time,S+I+R,'k',label='total population')
plt.plot(Binf,'ro',label='infections')
plt.plot(Bdead,'bo',label='deaths')
plt.plot(Brec,'go',label='recovered')
plt.plot(Bact,'mo',label='active')
plt.xlabel('days after 10th of October 2020')
plt.ylabel('number of people')
plt.title('Covid Model for Bremen plus surrounding (assuming 0% unreported cases)')
plt.legend(loc=2)





plt.figure(3)
plt.plot(DDt,'b',label='doubling time')
plt.xlabel('days after 11th of March')
plt.ylabel('days')
plt.legend(loc=1)


plt.figure(4)
plt.plot(Rnull,'b',label='R0')
plt.xlabel('days after 11th of March')
plt.ylabel('days')
plt.legend(loc=1)
plt.title('Covid Model for Bremen (assuming 0% unreported cases)')


print 'Verdoppelungszeit=',DDt[7]
print 'Verdoppelungszeit=',DDt[tmax-2]


#trange=np.arange(0,tmax,1)
trange=timeax
years=mdates.YearLocator()
months=mdates.MonthLocator()
years_fmt=mdates.DateFormatter('%Y')
#Datum=dts.date(2020,3,18)

#print Datum


plt.figure(5)
#fig, ax = plt.subplots(constrained_layout=True)
#locator = mdates.AutoDateLocator()
#formatter = mdates.ConciseDateFormatter(locator)
#ax.xaxis.set_major_locator(locator)
#ax.xaxis.set_major_formatter(formatter)
plt.plot(trange, D+I+R, lw=3, color='green', label='Genesene')
plt.plot(trange,D+I, lw=3, color='red', label='Aktuell Erkrankte')
plt.plot(trange, D, lw=3, color='black', label='Verstorbene')
plt.fill_between(trange, D, D+I, color='red')
plt.fill_between(trange, D+I, D+I+R, color='green')
plt.fill_between(trange, 0, D, color='black')
plt.grid(True)
plt.legend(loc=2)
plt.title('Covid Model for Bremen plus surrounding (assuming 0% unreported cases)')




#lenBinf=len(Binf)
#doubletime=np.zeros(lenBinf-1)
#for j in range(lenBinf-1):
#    doubletime[j]=np.log(2.0)/np.log(1.0+(Binf[j+1]-Binf[j])/Binf[j])


#plt.figure(4)
#plt.plot(doubletime,'bo',label='Verdoppelungszeit Daten')
#plt.legend(loc=1)

print np.max(I)*0.0013
print np.max(I)*0.0002

print 'R0 =', (a*c)/(rho)

plt.figure(9)

#plt.plot(Binf,'ro',label='infections')
#plt.plot(Bdead,'bo',label='deaths')
#plt.plot(Brec,'go',label='recovered')
#plt.plot(Bact,'mo',label='active')

#plt.plot(trange,S,'b',label='susceptible')
plt.plot(trange,I+R,'r',label='infected cumulative')
plt.plot(trange,I,'m',label='infected active')
#plt.plot(time,I*0.12/0.02,'y',label='potentially infected') # potential to determine undetected cases by using the statistics of RKI on Pneumonia in comparison to Bremen data.
plt.plot(trange,R,'g',label='recovered')
plt.plot(trange,D,'c',label='dead')
#plt.plot(time,S+I+R,'k',label='total population')
#plt.xlabel('days after 10th of October 2020')
plt.ylabel('number of people')
plt.title('Covid Model for Bremen plus surrounding (assuming 0% unreported cases)')
plt.legend(loc=2)


plt.show()

