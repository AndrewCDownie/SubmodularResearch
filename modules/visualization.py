import pygame


class visualization():
    def __init__(self,dims,scale,cap = ""):
        pygame.init()
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0) 
        self.PURPLE =(153,  50, 204)
        self.YELLOW =(255, 255,   0)
        self.scale = scale

        self.colours = {
            "BLACK" :(  0,   0,   0),
            "WHITE" :(255, 255, 255),
            "BLUE" : (  0,   0, 255),
            "GREEN" : (  0, 255,   0),
            "RED" : (255,   0,   0) ,
            "PURPLE" : (153,  50, 204),
            "YELLOW" : (255, 255,   0)
        }
        
        #get size of the space to work with
        self.displaySize = (self.scale*dims[0],self.scale*dims[1])
        self.display = pygame.display.set_mode(self.displaySize)
        
        #set the title
        pygame.display.set_caption(cap)

        #whip the screen initally
        self.display.fill(self.WHITE)
        self.clock = pygame.time.Clock()

    def draw_circles(self,points,r,colour,cc = None):
        if cc is not None:
            for p in points:
                pygame.draw.circle(self.display, cc, (self.scale*round(p[0]),self.scale*round(p[1])),self.scale*r)
            return
        for p in points:
            pygame.draw.circle(self.display, self.colours[colour], (self.scale*round(p[0]),self.scale*round(p[1])),self.scale*r)

    def draw_circles_dict(self,points,colour):
        for p in points:
            pygame.draw.circle(self.display, self.colours[colour], (self.scale*round(p["x"]),self.scale*round(p["y"])),self.scale*int(p['r']))


    def update(self):
        pygame.display.update(pygame.Rect(0, 0, 10000, 10000))

    def draw(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

def main():
    vis = visualization((100,100),5)
    vis.draw_cirles([(25,25)],10,"BLUE")
    vis.draw_cirles([(25,15)],1,"BLACK")
    vis.draw_cirles([(40,10)],10,"GREEN")
    vis.draw_cirles([(60,35)],10,"RED")
    vis.draw_cirles([(25,25)],1,"BLACK")
    vis.draw_cirles([(40,10)],1,"BLACK")
    vis.draw_cirles([(37,25)],1,"BLACK")
    vis.draw_cirles([(60,30)],1,"BLACK")
    vis.draw_cirles([(60,35)],1,"BLACK")

    vis.update()
    running = True
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


if __name__ == "__main__":
    main()
