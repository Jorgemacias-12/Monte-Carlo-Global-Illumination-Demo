from OpenGL.GL import *
import math

class Shapes:
    def cube(self):
        glPushMatrix()
        vertices = [(0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
                    (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5)]
        triangles = [0, 2, 3, 0, 3, 1, 8, 4, 5, 8, 5, 9, 10, 6, 7, 10, 7, 11, 12,
                     13, 14, 12, 14, 15, 16, 17, 18, 16, 18, 19, 20, 21, 22, 20, 22, 23]

        for t in range(len(triangles) - 3):
            glBegin(GL_LINES)
            glVertex3fv(vertices[triangles[t]])
            glVertex3fv(vertices[triangles[t + 1]])
            glVertex3fv(vertices[triangles[t + 2]])
            glEnd()
            t += 3
            
        glPopMatrix()

    def draw_scene(self):
        glPushMatrix()
        # glLoadIdentity()
        glTranslatef(0.0, 2.5, -4)

        num_segments = 1000
        radius = 1

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)

        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
            
        glEnd()
        glPopMatrix()

        # Draw cube
        glPushMatrix()
        # glLoadIdentity()
        glTranslatef(2.0, 0.0, 0.0) 
        glBegin(GL_QUADS)

        glColor3f(0, 34.0, 100.0)
        glVertex3f(-1, -1,  1)
        glVertex3f( 1, -1,  1)
        glVertex3f( 1,  1,  1)
        glVertex3f(-1,  1,  1)

        glColor3f(0, 34.0, 100.0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1,  1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f( 1, -1, -1)
        
        glColor3f(0, 34.0, 100.0)
        glVertex3f(-1,  1, -1)
        glVertex3f(-1,  1,  1)
        glVertex3f( 1,  1,  1)
        glVertex3f( 1,  1, -1)
        
        glColor3f(0, 34.0, 100.0)
        glVertex3f(-1, -1, -1)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1, -1,  1)
        glVertex3f(-1, -1,  1)
        
        glColor3f(0, 34.0, 100.0)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f( 1,  1,  1)
        glVertex3f( 1, -1,  1)
        
        glColor3f(0, 34.0, 100.0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1,  1)
        glVertex3f(-1,  1,  1)
        glVertex3f(-1,  1, -1)
        
        glEnd()
        glPopMatrix()
 

