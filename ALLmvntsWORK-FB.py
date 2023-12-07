import pygame,random,sys,time#,numpy#,starter
###
# PyQt5
###
##global x
##x = starter.main()
##print(x)
###
# PyOpenGl
###
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def tryexcept(func):
    def x(*args, **kwargs):
        try: return(func(*args, **kwargs))
        except Exception as e: print(func.__name,":", "'{}'".format(e))
    return x



##print(dir(OpenGL.GLU))

clock = pygame.time.Clock()

vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    ]

edges = [
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    ]

surfaces = [
    (4,5,1,0),  # RIGHT
    (3,2,7,6),  # LEFT
    (4,0,3,6),  # BOTTOM
    (6,7,5,4),  # FRONT
    (1,5,7,2),  # TOP
    (0,1,2,3)   # BACK
    ]

colors = [               # colours
    (0,0,1),             # : 'BLUE',                 RIGHT
    (1,0,0),             # : 'RED',                  LEFT
    (0,1,0),             # : 'GREEN',                BOTTOM
    (1,1,1),             # : 'WHITE',                FRONT
    (1,0.64705882352,0), # : 'ORANGE'                TOP
    (1,1,0)              # : 'YELLOW',               BACK
    ]

colDict = {
    (0,0,1):'Blue',
    (1,0,0):'Red',
    (0,1,0):'Green',
    (1,1,1):'White',
    (1,0.64705882352,0):'Orange',
    (1,1,0):'Yellow'
    }

class Cublet():
    def __init__(self, index, x,y,z, gap=2.02):
        self.colors = [colDict[color] for color in colors]
        self.index = index
        self.cube_gap = 0.05+gap
        self.vertices = []
        self.x = x
        self.y = y
        self.z = z
        self.corner = True if x != 0 and y != 0 and z != 0 else False
        self.center = True if (x != 0 and (y == 0 and z == 0)) or (y != 0 and (x == 0 and z == 0)) or (z != 0 and (x == 0 and z == 0)) else False # distance 1 from 0,0,0
        self.edge = True if not(self.corner or self.center or (x == 0 and y == 0 and z == 0)) else False # not (corner, center, very center)

        
        for vertex in vertices:
            self.vertices.append([vertex[0] + x*self.cube_gap,
                                  vertex[1] + y*self.cube_gap,
                                  vertex[2] + z*self.cube_gap])


class Cubie():
    def __init__(self):
        # each cubie needs its own display
        pygame.init()
        pygame.display.set_caption('Rubix Cube')
        display = (800,600)
        
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        glEnable(GL_DEPTH_TEST) 
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        glTranslatef(0,0, -20) # from bottom left to top right = -2
        self.location = {}
        

    def draw(self, i,vertices, varcolors):
        rgbValues = self.getRGB(varcolors)
        
        glBegin(GL_QUADS)
        x = 0
        for surface in surfaces:
            glColor3fv(rgbValues[x])
            x += 1
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()

    def getRGB(self,x): return [list(colDict.keys())[list(colDict.values()).index(color)] for color in x]


class Cube():
    def __init__(self,size=3,rand=False):
        self.size = size
        self.cubie = Cubie()
        self.rand = rand

    def draw(self):
        Min = -(self.size//2)
        Max = self.size-abs(Min)
        self.cubies = []
        i = 0
        
        for x in range(Min,Max):
            for y in range(Min,Max):
                for z in range(Min,Max):
                    self.cubies.append(Cublet(i,x,y,z))
                    i += 1
                    
        if self.rand: self.randomize(self.rand)
        
    def matrixRotation(self,side,toDo,reverse,speed=4):
        if side == 'right' or side == 'left': xyz = (1,0,0) # rotation around the x axis
        elif side == 'top' or side == 'bottom': xyz = (0,1,0)
        elif side == 'front' or side == 'back': xyz = (0,0,1)
        else: print("OH SNAP",side)
        
        
        indexes = []
        for cube in self.cubies:
            if cube.x == toDo[0] or cube.y == toDo[1] or cube.z == toDo[2]:
                indexes.append(cube.index)

        loop = 1
        rotate = 90 if reverse else -90
        speed = speed # 0 = instant
        for i in range(speed):
            loop *= 2
            rotate /= 2

        glMatrixMode(GL_MODELVIEW)
        # animation loop 
        for i in range(loop):
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            
            if i != 0: glRotatef(-i*(rotate),xyz[0],xyz[1],xyz[2])
            
            for cube in self.cubies:
                if cube.index not in indexes: self.cubie.draw(cube.index,cube.vertices,cube.colors)

            if i == 0: glRotatef(rotate,xyz[0],xyz[1],xyz[2])
            else: glRotatef((i+1)*(rotate),xyz[0],xyz[1],xyz[2])

            for cube in self.cubies: # dictionary index
                if cube.index in indexes: self.cubie.draw(cube.index,cube.vertices,cube.colors)

            pygame.display.flip()

        for i in range(loop): glPopMatrix()



    def randomize(self,moves):

##        print(moves)

        catch = []
        list_moves = [6,3,4,1,7,9,0,'dot']
        opposites = {6:3, 4:1, 7:9, 0:'dot', 3:6, 1:4, 9:7, 'dot':0}
        for i in range(moves):
            x = random.randint(0,len(list_moves)-1)
            print(list_moves[x])
            self.move(list_moves[x])
            catch.append(list_moves[x])
            clock.tick(60)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            pygame.display.flip()
            

        catch.reverse()
        for i in catch:
            print(opposites[i])
            self.move(opposites[i])
            time.sleep(1)
            


    def move(self,direction):
               
        if direction == 6 or direction == 3: # R R'
            side = 'right'            
            toDo = [1,None,None]
            indexes = [0,1,5,2,3,4]
            reverse = True if direction == 3 else False

        elif direction == 4 or direction == 1: # L L'
            side = 'left'            
            toDo = [-1,None,None]
            indexes = [0,1,5,2,3,4]
            reverse = True if direction == 1 else False
            

        elif direction == 7 or direction == 9: # U U'
            side = 'top'
            toDo = [None,1,None]
            indexes = [5,3,2,0,4,1]
            reverse = True if direction == 9 else False


        elif direction == 0 or direction == 'dot': # D D'
            side = 'bottom'
            toDo = [None,-1,None]
            indexes = [5,3,2,0,4,1]
            reverse = True if direction == 'dot' else False

        elif direction == 'end' or direction == 'pgdn': # F F'
            side = 'front'
            toDo = [None,None,1]
            indexes = [4,2,0,3,1,5]
            reverse = True if direction == 'end' else False

        elif direction == 'home' or direction == 'pgup': # B B'
            side = 'back'
            toDo = [None,None,-1]
            indexes = [4,2,0,3,1,5]
            reverse = True if direction == 'home' else False
            
        else:
            return

        self.matrixRotation(side,toDo,reverse) # rotation animation
        
        bottom,top,left,right = self.getSides(toDo)
        
        for i in range(3 if reverse else 1):
            bottom,left,top,right = self.rotateList(bottom,top,left,right,indexes)
            
        self.appendNewColors(toDo,bottom,top,left,right)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def getSides(self,toDo):
        bottom,top,left,right = [],[],[],[]
        
        for cube in self.cubies:
            if cube.x == toDo[0]:
                if cube.y == -1 and len(bottom) <= 1: bottom.append(cube.colors)
                elif cube.z == 1 and len(left) <= 1: left.append(cube.colors)
                elif cube.z == -1 and len(right) <= 1: right.append(cube.colors)
                elif cube.y == 1 and len(top) <= 1: top.append(cube.colors)

            if cube.y == toDo[1]:
                if cube.z == -1 and len(top) <= 1: top.append(cube.colors)
                elif cube.x == 1 and len(right) <= 1: right.append(cube.colors)
                elif cube.x == -1 and len(left) <= 1: left.append(cube.colors)
                elif cube.z == 1 and len(bottom) <= 1: bottom.append(cube.colors)

            if cube.z == toDo[2]:
                if cube.y == -1 and len(bottom) <= 1: bottom.append(cube.colors)
                elif cube.x == -1 and len(left) <= 1: left.append(cube.colors)
                elif cube.y == 1 and len(top) <= 1: top.append(cube.colors)
                elif cube.x == 1 and len(right) <= 1: right.append(cube.colors)



        return(bottom,top,left,right)

    def rotateList(self,bottom,top,left,right,indexes):
        

        newb,newt,newl,newr = [],[],[],[]
        for x in bottom: newb.append([x[i] for i in indexes])
        for x in top: newt.append([x[i] for i in indexes])
        for x in left: newl.append([x[i] for i in indexes])
        for x in right: newr.append([x[i] for i in indexes])
        '''
        for 'U' rotation:

        bottom = [N,N,1] = 17,26
        left = [N,-1,N] = 7,8
        top = [N,N,-1] = 6,15
        right = [N,1,N] = 24,25


        right -> bottom = reverse order
        bottom -> left = same order
        left -> top = reverse order
        top -> right = same order
        
        '''
        return(newr[::-1],newb,newl[::-1],newt) # bottom,left,top,right

    def appendNewColors(self,toDo,bottom,top,left,right):#Min,Max=None):
        for cube in self.cubies:
            if cube.x == toDo[0]: # left right
                if cube.y == -1 and len(bottom) != 0: cube.colors = bottom.pop(0)
                elif cube.z == 1 and len(left) != 0: cube.colors = left.pop(0)
                elif cube.z == -1 and len(right) != 0: cube.colors = right.pop(0)
                elif cube.y == 1 and len(top) != 0: cube.colors = top.pop(0)

            if cube.y == toDo[1]: # top bottom
                if cube.z == -1 and len(top) != 0: cube.colors = top.pop(0)
                elif cube.x == 1 and len(right) != 0: cube.colors = right.pop(0)
                elif cube.x == -1 and len(left) != 0: cube.colors = left.pop(0)
                elif cube.z == 1 and len(bottom) != 0: cube.colors = bottom.pop(0)


            if cube.z == toDo[2]: # front back
                if cube.y == -1 and len(bottom) != 0: cube.colors = bottom.pop(0)
                elif cube.x == -1 and len(left) != 0: cube.colors = left.pop(0)
                elif cube.y == 1 and len(top) != 0: cube.colors = top.pop(0)
                elif cube.x == 1 and len(right) != 0: cube.colors = right.pop(0)

    def main(self):
        camera_sens = 3
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


            key = pygame.key.get_pressed()
            # camera keyboard rotation
            if key[pygame.K_UP]: glRotatef(camera_sens,-camera_sens,0,0)
            if key[pygame.K_DOWN]: glRotatef(camera_sens,camera_sens,0,0)
            if key[pygame.K_LEFT]: glRotatef(camera_sens,0,-camera_sens,0)
            if key[pygame.K_RIGHT]: glRotatef(camera_sens,0,camera_sens,0)

            # cube keyboard rotation
            if key[pygame.K_KP6]: self.move(6) # R
            if key[pygame.K_KP3]: self.move(3) # R'
            if key[pygame.K_KP4]: self.move(4) # L
            if key[pygame.K_KP1]: self.move(1) # L'
            if key[pygame.K_KP7]: self.move(7) # U
            if key[pygame.K_KP9]: self.move(9) # U'
            if key[pygame.K_KP0]: self.move(0) # D
            if key[pygame.K_KP_PERIOD]: self.move('dot') # D'
            if key[pygame.K_END]: self.move('end') # F
            if key[pygame.K_PAGEDOWN]: self.move('pgdn') # F'
            if key[pygame.K_HOME]: self.move('home') # B
            if key[pygame.K_PAGEUP]: self.move('pgup') # B'

            if key[pygame.K_SPACE]: self.randomize(20)
            
            if key[pygame.K_r]: self.draw() # reset cube

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


            for cube in self.cubies: # dictionary index
                self.cubie.draw(cube.index,cube.vertices,cube.colors)
                

            pygame.display.flip()
            
        ## out of while loop
        pygame.quit()

def main():
    try:
        rand = int(input("Enter number of random movements (0 for normal gameplay): "))
    except Exception as e:
        print("Please enter a number")
        raise e
    if rand == 0:
        cube = Cube()
    else:
        cube = Cube(rand=rand) #create a 3x3x3 cube
    
    cube.draw()
    cube.main()
main()
