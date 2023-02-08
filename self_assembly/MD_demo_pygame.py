# coding=utf-8
import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import math
import time


# parameter
mySystem = {"type1": {"number": 50, "La": 5, "Lb": 5}}   # tune parameters here! La+Lb=10
aa = 0.5  # sigma_A / sigma_B
La = mySystem["type1"]["La"]   # 5
Lb = mySystem["type1"]["Lb"]   # 5
bb = La / Lb

sigma_A = 1
sigma_B = sigma_A / aa
rcutoff = 2.5
eps_AA = 5*1  # kT  # k=1 T=1
eps_BB = 5*1  # kT
eps_AB = 1*1  # kT
Lbox = 40
kspring = 0.1

dxMax = 0.2
nSample = 500
typeA_size = 5
typeB_size = int(typeA_size*aa)

number_of_particles = 500
number_of_polymers = mySystem["type1"]["number"]
number_of_bead_typeA = La
number_of_bead_typeB = Lb
my_particles = []

background_colour = (255,255,255)
width, height = 400, 400

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def get_beed_distance(Beed_i, Beed_j):
    x_distance = abs(Beed_i.x-Beed_j.x)
    y_distance = abs(Beed_i.y-Beed_j.y)
    beed_distance = math.sqrt(x_distance*x_distance + y_distance*y_distance)
    return beed_distance


def get_beed_sigma(Beed_i, Beed_j):
    sigma = (sigma_A + sigma_B)/2
    if Beed_i.type == 'A' and Beed_j.type == 'A':
        sigma = sigma_A
    elif Beed_i.type == 'B' and Beed_j.type == 'B':
        sigma = sigma_B
    return sigma


def get_beed_epsilon(Beed_i, Beed_j):
    epsilon = eps_AB
    if Beed_i.type == 'A' and Beed_j.type == 'A':
        epsilon = eps_AA
    elif Beed_i.type == 'B' and Beed_j.type == 'B':
        epsilon = eps_BB
    return epsilon


def check_beed_connected(Beed_i,Beed_j):
    if get_beed_distance(Beed_i,Beed_j) == (Beed_i.size + Beed_j.size):
        #print("Beed",Beed_i.index," Beed",Beed_j.index, "is connected!!!")
        return True
    return False

def Eharmonic(Beed_i,Beed_j):
    #  Eharmonic will be zero if i and j are not bonded together
    if check_beed_connected(Beed_i,Beed_j) is False:
        return 0
    beed_distance = get_beed_distance(Beed_i,Beed_j)
    EH = 0.5 * kspring * beed_distance * beed_distance
    #print("EH:",EH)
    return EH

def ELJ(Beed_i,Beed_j):
    beed_distance = get_beed_distance(Beed_i, Beed_j)
    sigma = get_beed_sigma(Beed_i, Beed_j)
    if beed_distance > rcutoff * sigma:
        return 0
    epsilon = get_beed_epsilon(Beed_i, Beed_j)
    elj_value = 4 * epsilon * ( math.pow(sigma/beed_distance, 12) - math.pow(sigma/beed_distance, 6) )
    #print("ELJ:",elj_value)
    return elj_value

def CalcBeedEnergy(Beed_i,Beed_j):
    return Eharmonic(Beed_i,Beed_j) + ELJ(Beed_i,Beed_j)

def BeedEnery(old_beed, Beed_i):
    bead_nergy = 0
    for i,particle in enumerate(my_particles):
        if Beed_i.index == particle.index:
            continue
        if old_beed.index == particle.index:
            continue
        bead_nergy += CalcBeedEnergy(Beed_i, particle)
    #print(Beed_i.index," nergy:",bead_nergy)
    return bead_nergy

def GetSystemEnery():
    energy = 0
    for i,particle in enumerate(my_particles):
        for particle2 in my_particles[i+1:]:
            add_energy = CalcBeedEnergy(particle, particle2)
            #print("add_energy:",add_energy)
            energy += add_energy
    return energy

def check_collide(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = np.hypot(dx, dy)
    if dist < (p1.size + p2.size):
        return True
    return False


def check_particle_collide_in_my_particles(index, particle):
    collide_or_out = False
    size = particle.size
    if (particle.x < size) or (particle.x > (width - size)):
        collide_or_out = True  # out
    elif (particle.y < size) or (particle.y > (height - size)):
        collide_or_out = True  # out

    for i,particle2 in enumerate(my_particles):
        if i!=index and (check_collide(particle, particle2) is True):
            collide_or_out = True # collide

    return collide_or_out

def decide_particle_to_move(particle, new_particle): # to be implement
    to_move = False
    delta = BeedEnery(particle,new_particle) - BeedEnery(particle,particle)
    #print("delta:",delta,"type:",particle.type)
    if delta<=0:
        to_move = True
    else:
        x = random.random()
        a = math.exp(-delta)  # a = exp( - DE / kT )
        #print("x:",x,"a:",a)
        if x < a:
            to_move = True
        #else:
        #   print("decide not to move!!!!!!")
    return to_move


class Particle():
    def __init__(self,index,x,y,size,type):
        self.index = index
        self.x = x
        self.y = y
        self.size = size
        self.type = type
        self.colour = BLUE
        self.thickness = 1

    def display(self):
        if self.type == 'B':
            self.colour = RED
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def printinfo(self):
        print("Position：", self.x, self.y)

    def move_interval(self,direction,interval):
        if direction == 0:
            self.x += interval
        elif direction == 1:
            self.y += interval

def generate_fixed_polymers():
    for n in range(number_of_polymers):
        index = 0
        if n < 25:
            x = random.randint(10, 110)
            y = 10 + 15*n
        else:
            x = random.randint(190, 300)
            y= 30 + 15*(n-25)

        x_bead = x
        for m in range(number_of_bead_typeA):
            particle = Particle(index,x_bead, y, typeA_size, 'A')
            index +=1
            x_bead += typeA_size*2
            my_particles.append(particle)

        x_bead -= typeA_size - typeB_size
        for m in range(number_of_bead_typeB):
            particle = Particle(index,x_bead, y, typeB_size, 'B')
            index += 1
            x_bead += typeB_size*2
            my_particles.append(particle)

#logfile = open('energy_log.txt','w+')
heatfile = open('heat_log.txt','a+')
generate_fixed_polymers()
ori_energy = GetSystemEnery()
energy_sum = ori_energy
energy_number = 1
energy_list = []
print("Original Energy:",ori_energy)
energy_list.append(ori_energy)
heatfile.write(str(aa)+'    ')
heatfile.write(str(bb)+'    ')
#logfile.write(str(ori_energy)+'\n')
running = True
nfilp=0
screen = pygame.display.set_mode((width, height))

while running:
    nfilp += 1
    #print nfilp
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(background_colour)

    particle_index = random.randint(0, len(my_particles) - 1)
    interval = random.randint(-dxMax * 10, dxMax * 10)
    direction = random.randint(0, 1)
    particle = my_particles[particle_index]

    move_x = particle.x
    move_y = particle.y
    if direction == 0:
        move_x += interval
    elif direction == 1:
        move_y += interval
    new_particle = Particle(-1,(move_x,move_y),particle.size,particle.type)

    has_collide = check_particle_collide_in_my_particles(particle_index, new_particle)
    if has_collide is False:
        decide_to_move = decide_particle_to_move(particle, new_particle)
        if decide_to_move is True:
            particle.move_interval(direction,interval)
        #else:
        #    print("new_particle not decide to move,type:", new_particle.type)
    #else:
        #print("new_particle has collide,type:",new_particle.type)

    for i, particle2 in enumerate(my_particles):
        particle2.display()

    pygame.display.flip()

    if nfilp%nSample == 0:
        system_energy = GetSystemEnery()
        energy_list.append(system_energy)
        energy_number+=1
        #print("System Energy:",system_energy)
        #logfile.write(str(system_energy)+'\n')

energy_average = energy_sum/energy_number
print("Average System Energy:",energy_average)
heatfile.write(str(energy_average)+'\n')
#logfile.flush()
#logfile.close()
heatfile.flush()
heatfile.close()
pygame.quit()

x_values = range(energy_number)
avg_values = [energy_average]*energy_number
plt.plot(x_values,energy_list,'o-',linewidth=5)
plt.plot(x_values,avg_values,'--',label="Average Energy",color='red',linewidth=3)
plt.title("System Energy in nSteps",fontsize = 24)
plt.xlabel("nSteps",fontsize = 14)
plt.ylabel("System Energy",fontsize = 14)
plt.tick_params(axis='both',labelsize = 14)
plt.legend(loc='upper right')
plt.show()
