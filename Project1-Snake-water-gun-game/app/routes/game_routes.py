from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..core.game import play_game
import random

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


#Route to homepage
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {'request':request})

# Route for game play (When user submits the form)
@router.post("/play", response_class=HTMLResponse)
def playing(request:Request, game : str=Form(...,)):    # Form(...) - Reads the HTML form input properly
    
    # Mapping user input
    move = {"snake":'S', "water":"W", "gun":"G"}
    player_move = move[game.lower()]  # Here we are converting the input to lower case as values in html is in lower and form is capital
    
    # Computer randomly selecting the move
    comp = random.choice(['S', 'W', 'G'])
    
    # Getting result from the game.py
    result = play_game(player_move, comp)
    
    ''' Sending all the inputs back to frontend to display '''
    # Sends result back to HTML
    return templates.TemplateResponse('index.html', 
                                      {
                                          "request":request,
                                          "player_move":player_move,
                                          "comp":comp,
                                          "result":result
                                      })