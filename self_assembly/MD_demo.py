import numpy as np
import random as rd
import copy as cp
import math as math
import matplotlib.pyplot as plt

mySystem={'type1':{'number':int(input('number of monomers=')),'La':int(input('La=')),'Lb':int(input('Lb=')),}}
Lbox=int(input('Lbox='))
k=1.38*(10**(-23))#Boltzmann
sigma_A=1
sigma_B=float(input('sigma_B='))
T=int(input('temperature='))
eps_AA=eps_BB=5*k*T
eps_AB=k*T
para=mySystem['type1']
bb=para['La']/para['Lb']
aa=sigma_A/sigma_B
sigma_AB=(sigma_A+sigma_B)/2
No=range(para['number'])
dxMax=0.2*sigma_A
ks=1
counter=0
Etot=0
ending=int(input('end='))
a=int(para['number']*para['La']/(para['La']+para['Lb']))
b=int(para['number']*para['Lb']/(para['La']+para['Lb']))
ini=np.random.uniform(0,Lbox,((para['number']),2))#random initial position
L=Lbox/(para['La']+para['Lb']) #length of cell
fig,ax=plt.subplots()

#information of particle
def particle(x):
    k=['a']*a+['b']*b
    rd.shuffle(k) #reshuffle
    for i in k:
        info=[x,[int(x[0]//L),int(x[1]//L)],i] #determine cell position
    return info
con=[]
for i in No:
    con.append([i,[]])#连接信息
infolist=[] #空列表防止迭代错误
infolist1=[]
for i in ini:
    infolist.append(particle(i)) 
k_=list(zip(infolist,con))
infolist.clear()
for i in k_:
    infolist.append(list(i))#imformation of particles, [[position,[cellx,celly],type],[number,[connect1,connect2]]

def cellconfirm(x,y):
    celly=np.array(y[0][1])
    hr=np.array([1,0])
    vr=np.array([0,1])
    if list(celly+1)==x[0][1]:
        return True
    elif list(celly-1)==x[0][1]:
        return True
    elif list(celly+hr)==x[0][1]:
        return True
    elif list(celly-hr)==x[0][1]:
        return True
    elif list(celly+vr)==x[0][1]:
        return True
    elif list(celly-vr)==x[0][1]:
        return True
    else:
        return False
        
def Ep(x,y):
    Px,Py=x[0][0],y[0][0]
    Tx,Ty=x[0][2],y[0][2]
    if Tx=='a' and Ty=='a':
        epsilon,sigma=eps_AA,sigma_A
    elif Tx=='a' and Ty=='b':
        epsilon,sigma=eps_AB,sigma_AB
    elif Tx=='b' and Ty=='b':
        epsilon,sigma=eps_BB,sigma_B
    elif Tx=='b' and Ty=='a':
        epsilon,sigma=eps_AB,sigma_AB
    r,rcutoff=np.linalg.norm(Px-Py),2.5*sigma
    if r>rcutoff:
        E=0
    else:
        E=4*epsilon*((sigma/abs(r))**12-(sigma/abs(r))**6)
    return E

def connection(x):
    if len(x[1][1])!=2:
        return True

def Eb(x,y):
    if connection(x)==connection(y)==True:
       Px,Py=x[0][0],y[0][0]
       Tx,Ty=x[0][2],y[0][2]
       if Tx=='a' and Ty=='a':
           epsilon,sigma=eps_AA,sigma_A
       elif Tx=='a' and Ty=='b':
           epsilon,sigma=eps_AB,sigma_AB
       elif Tx=='b' and Ty=='b':
           epsilon,sigma=eps_BB,sigma_B
       elif Tx=='b' and Ty=='a':
           epsilon,sigma=eps_AB,sigma_AB
       r=np.linalg.norm(Px-Py)
       if r<sigma:
           Eh=0.5*ks*abs(r)**2
           xx=x[1][0]
           yy=y[1][0]
           x[1][1].append(yy)
           y[1][1].append(xx)
       else:
            Eh=0
    else:
        Eh=0
    return Eh

def plot():
    plt.title('MC SIM')
    f1=plt.subplot(1,2,1)
    f2=plt.subplot(1,2,2)
    plt.sca(f1)
    plt.xlim(xmax=Lbox,xmin=0)
    plt.ylim(ymax=Lbox,ymin=0)
    plt.grid(linestyle = ':')
    for i in infolist:
        if i[0][2]=='a':
            plt.scatter(i[0][0][0],i[0][0][1],color='r',s=10*sigma_A)
        else:
            plt.scatter(i[0][0][0],i[0][0][1],color='b',s=10*sigma_B)
    END=ending
    plt.sca(f2)
    EEE=0
    plt.ion()
    xs=[0,0]
    ys=[1,1]
    for x in range(END):
        y=EEE
        xs[0]=xs[1]
        ys[0]=ys[1]
        xs[1]=x
        ys[1]=y
        plt.plot(xs,ys)
    plt.show()

def Line(x):
    if len(x[1][1])!=0:
        for i in x[1][1]:
            AA=0
            AA=plt.plot([infolist[x[1][0]][0][0][0],infolist[i][0][0][0]],[infolist[x[1][0]][0][0][1],infolist[i][0][0][1]],color='black')
    
def rm():
    pro=rd.choice(No)
    V=(np.random.random(2)-0.5)*(dxMax*T/(293.15*0.5))
    PV=cp.copy(infolist[pro][0][0])
    plt.arrow(PV[0],PV[1],10*V[0],10*V[1],length_includes_head = True,head_width = 0.6,color='black')
    PV+=V
    while list(PV-np.array([Lbox,Lbox])) and False:
        V=(np.random.random(2)-0.5)*(dxMax/0.5)
        PV=cp.copy(infolist[pro][0][0])
        PV+=V
    else:
        infolist[pro][0][0]=PV


def MC(x):
    plot()
    for i in infolist:
        Line(i)
    Ehar=x[0]
    ELJ=x[1]
    rm()
    
    for i in No:
        if i+1 in No:
            for x in No[i+1:]:
                if cellconfirm(infolist[i],infolist[x])==True:
                    ELJ+=Ep(infolist[i],infolist[x])
                if connection(infolist[i])==True and connection(infolist[x])==True:
                    Ehar+=Eb(infolist[i],infolist[x])
    return [Ehar,ELJ]

E_=[]
E_ini=[]
Etot=sum(MC([0,0]))
EEE=Etot
for i in range(ending):
    infolist1=cp.copy(infolist)
    E_.append(sum(MC([0,0])))
    DE=sum(E_)-Etot
    if DE<0:
        Etot=sum(E_)
    else:
        Ka=math.exp(-DE/(k*T))
        X=rd.uniform(0,1)
        if X<Ka:
            Etot=sum(E_)
        else:
            infolist=cp.copy(infolist1)
            Etot=Etot
            E_ini.append(Etot)
        
print(f"Total Energy is {Etot}")
plot()
