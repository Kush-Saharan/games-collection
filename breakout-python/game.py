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
        self.add_ball()         #adds ball
        self.update_lives()     #adds default lives
        self.text=self.draw_text(300,200,'Press Space to start')    
        self.canvas.bind('<space>', lambda _:self.start_game())    #calls method starts game when space is clicked

    def game_loop(self):
        self.check_collisions()
        num_bricks=len(self.canvas.find_withtag('brick'))   #checks ho many bricks remain
        if num_bricks==0:                                   #if all bricks are gone, you win
            self.ball.speed=None
            self.draw_text(300,200,'You win!')

        elif self.ball.get_position()[3]>=self.height:      #if ball falls below paddle, reduce lives
            self.ball.speed=None
            self.lives-=1
            if self.lives<0:
                self.draw_text(300,200,"Game Over!")        #if lives end, end game
            else:
                self.after(1000,self.setup_game)          #if lives>0 setup game again
        else:
            self.ball.update()
            self.after(20, self.game_loop)                  #runs every 50 ms to check for collisions


    def start_game(self):
        self.canvas.unbind('<space>')   #so clicking space does nothing when the game starts
        self.canvas.delete(self.text)   #removes the text saying start game
        self.paddle.ball=None   #removes ball from the paddle or the ball moves when the paddle is moved
        self.game_loop()        #method that runs throughot the game which checks if game ended or not

    def draw_text(self,x,y,text,size='40'):
        font=('Helvetica',size)
        return self.canvas.create_text(x,y,text=text,font=font)     #canvas method of draing text on the screen

    def check_collisions(self):
        ball_coords=self.ball.get_position()
        items=self.canvas.find_overlapping(*ball_coords)    #canvas function that return which objects ids currently overlap the object
        objects=[self.items[x] for x in items if x in self.items]   #checks if the object returned exists in current items of the game
        self.ball.collide(objects)  #calls the collide method of the ball object

    def update_lives(self):
        text = "Lives: " + str(self.lives)      #to display remaining lives on the screen
        if self.hud is None:        #if there is no hu text, create one
            self.hud=self.draw_text(50,20,text,15)  
        else:   #If the HUD already exists, just update its text to the new value
            self.canvas.itemconfig(self.hud,text=text)

    def add_brick(self,x,y,hits):
        brick=Brick(self.canvas,x,y,hits)   #adds bricks on the screen with default hits and colors
        self.items[brick.item]=brick        #adds bricks to game items


    def add_ball(self):
        if self.ball is not None:           #deletes all balls that arent with paddle
            self.ball.delete()
        paddle_coords=self.paddle.get_position()    
        x=(paddle_coords[0]+paddle_coords[2])/2
        self.ball=Ball(self.canvas,x,310)        #creates a ball object just above paddle
        self.paddle.set_ball(self.ball)     #connects the ball to the paddle until it starts moving


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
        self.speed=3.5

        #creating the ball and at which position
        item=canvas.create_oval(x-self.radius,y-self.radius,x+self.radius,y+self.radius)
        super().__init__(canvas, item)

    def update(self):
        #update the position and direction of the ball according to the collisions
        coords=self.get_position()
        width=self.canvas.winfo_width()
        if coords[0]<=0 or coords[2]>=width:    # Check if the ball has hit the left or right wall
            self.direction[0] *= -1
        if coords[1]<=0:        # Check if the ball has hit the top wall
            self.direction[1] *= -1
        x=self.direction[0]*self.speed  # Move the ball in its current direction, scaled by speed
        y=self.direction[1]*self.speed
        self.move(x,y)          # actually update ball position on canvas

    def collide(self,game_objects):
        coords=self.get_position()
        x=(coords[0]+coords[2])*0.5
        if len(game_objects)>1:             # If the ball touches more than one object at the same time (e.g., paddle+brick, or 2 bricks)
            self.direction[1]*=-1           # simply bounce vertically
        elif len(game_objects)==1:          # If the ball touches exactly one object
            game_object=game_objects[0]     # the object it hit

            obj_coords=game_object.get_position()   
            if x>obj_coords[2]:             # hit the object's right side-bounce right, left side-bounce left
                self.direction[0]=1
            elif x<obj_coords[0]:
                self.direction[0]=-1
            else:
                self.direction[1]*=-1       # otherwise, bounce vertically (top/bottom hit)
        
        for game_object in game_objects:
            if isinstance(game_object,Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas,x,y):
        self.width=80
        self.height=10
        self.ball=None  #the ball isnt set yet
        item=canvas.create_rectangle(x-self.width/2,y-self.height/2,x+self.width/2,y+self.height/2,fill='blue')  #creates paddle
        super().__init__(canvas, item)

    def set_ball(self,ball):
        self.ball=ball

    def move(self,offset):
        coords=self.get_position()      #First get the position of the paddle
        width=self.canvas.winfo_width()
        if coords[0]+offset>=0 and coords[2]+offset<=width: #checks if the paddle is between the screen
            super().move(offset,0)
            if self.ball is not None:   #checks if the ball is not set yet
                self.ball.move(offset,0)


class Brick(GameObject):
    COLORS={1:'#999999', 2:'#555555', 3:'#222222'}

    def __init__(self, canvas, x,y,hits):
        #creates basic bricks
        self.width=75
        self.height=20
        self.hits=hits
        color=Brick.COLORS[hits]    #defines different colors for different hits
        item=canvas.create_rectangle(x-self.width/2,y-self.height/2,x+self.width/2,y+self.height/2,fill=color,tags='brick')
        super().__init__(canvas, item)

    def hit(self):
        self.hits-=1
        if self.hits==0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item,fill=Brick.COLORS[self.hits])

if __name__=='__main__':
    root=tk.Tk()
    root.title('Breakout')
    game=Game(root)
    game.mainloop()
