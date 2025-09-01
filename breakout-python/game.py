import tkinter as tk

class Game(tk.Frame):

    def __init__(self,master):
        super.__init__(master)
        #basic details of the canvas
        self.lives=3
        self.width=610
        self.height=400
        self.canvas=tk.Canvas(self,bg='#aaaaff',width=self.width,height=self.height) #Creating the canvas
        self.canvas.pack()
        self.pack()

    def setup_game(self):
        pass

    def game_loop(self):
        pass

    def start_game(self):
        pass

    def draw_text(self):
        pass

    def check_collisions(self):
        pass

    def update_lives(self):
        pass

    def add_brick(self):
        pass

    def add_ball(self):
        pass


class GameObject:

    def __init__(self,canvas,item):
        self.canvas=canvas
        self.item=item

    def get_position(self):
        return self.canvas.coords(self.item)
    
    def move(self,x,y):
        self.canvas.move(self.item,x,y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):

    def __init__(self, canvas, x,y):

        #Basic details of the ball
        self.radius=10
        self.direction=[1,-1]
        self.speed=10

        #creating the ball and at which position
        item=canvas.create_oval(x-self.radius,y-self.radius,x+self.radius,y+self.radius)
        super().__init__(canvas, item)

    def update(self):
        #update the position and direction of the ball according to the collisions
        pass

    def collide(self,game_objects):
        pass


class Paddle(GameObject):
    def __init__(self, canvas,x,y):
        self.width=80
        self.height=10
        self.ball=None
        item=self.canvas.create_rectangle(x-self.width/2,y-self.width/2,x+self.width/2,y+self.width/2,fill='blue')
        super().__init__(canvas, item)

    def set_ball(self):
        pass

    def move(self):
        pass


class Brick(GameObject):
    COLORS={1:'#999999', 2:'#555555', 3:'#222222'}

    def __init__(self, canvas, x,y,hits):
        #creates basic bricks depending on number of hits the brick has
        self.width=80
        self.height=20
        color=Brick.COLORS[hits]
        item=self.canvas.create_rectangle(x-self.width/2,y-self.width/2,x+self.width/2,y+self.width/2,fill=color,tags='brick')
        super().__init__(canvas, item)

    def hit(self):
        pass


root=tk.Tk()
root.title('Breakout')
game=Game(root)
game.mainloop()
