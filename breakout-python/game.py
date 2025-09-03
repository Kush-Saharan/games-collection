import tkinter as tk

class Game(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        #basic details of the canvas
        self.lives=3
        self.width=610
        self.height=400
        self.canvas=tk.Canvas(self,bg='#aaaaff',width=self.width,height=self.height) #Creating the canvas
        self.canvas.pack()
        self.pack()

        self.items={}   #to keep track of items which will be needed for collisions
        self.ball=None  
        self.paddle=Paddle(self.canvas,self.width/2,326)    #creates the paddle object
        self.items[self.paddle.item]=self.paddle    #adds paddle to the items of the game

        for x in range(5,self.width-5,75):  #creates bricks for the game
            self.add_brick(x+37.7,50,2)
            self.add_brick(x+37.5,70,1)
            self.add_brick(x+37.5,90,1)

        self.hud=None
        self.setup_game()
        self.canvas.focus_set() #makes sure your Canvas is the active widget for keyboard input
        self.canvas.bind('<Left>',
                         lambda _:self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _:self.paddle.move(10))

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

    def add_brick(self,x,y,hits):
        brick=Brick(self.canvas,x,y,hits)   #adds bricks on the screen with default hits and colors
        self.items[brick.item]=brick        #adds bricks to game items


    def add_ball(self):
        if self.ball is not None:   #deletes all balls that arent with paddle
            self.ball=ball
        paddle_coords=self.paddle.get_position()    
        x=(paddle_coords[0]+paddle_coords[2])/2
        ball=Ball(self.canvas,x,310)    #creates a ball object just above paddle
        self.paddle.set_ball(self.ball) #connects the ball to the paddle until it starts moving


class GameObject:

    def __init__(self,canvas,item):
        self.canvas=canvas
        self.item=item

    def get_position(self):
        return self.canvas.coords(self.item)    #used to get positions of game objects
    
    def move(self,x,y):
        self.canvas.move(self.item,x,y) #used to move game objects

    def delete(self):
        self.canvas.delete(self.item)   #used to delete game objects


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
        self.ball=None  #the ball isnt set yet
        item=self.canvas.create_rectangle(x-self.width/2,y-self.width/2,x+self.width/2,y+self.width/2,fill='blue')  #creates paddle
        super().__init__(canvas, item)

    def set_ball(self,ball):
        self.ball=ball

    def move(self,offset):
        coords=self.get_position()  #First get the position of the paddle
        width=self.canvas.winfo_width()
        if coords[0]+offset>=0 and coords[2]+offset<=0: #checks if the paddle is between the screen
            super().move(offset,0)
            if self.ball is not None:   #checks if the ball is not set yet
                self.ball.move(offset,0)


class Brick(GameObject):
    COLORS={1:'#999999', 2:'#555555', 3:'#222222'}

    def __init__(self, canvas, x,y,hits):
        #creates basic bricks
        self.width=80
        self.height=20
        color=Brick.COLORS[hits]    #defines different colors for different hits
        item=self.canvas.create_rectangle(x-self.width/2,y-self.width/2,x+self.width/2,y+self.width/2,fill=color,tags='brick')
        super().__init__(canvas, item)

    def hit(self):
        pass

if __name__=='__main__':
    root=tk.Tk()
    root.title('Breakout')
    game=Game(root)
    game.mainloop()
