#! /usr/bin/env python3
"""FastAPI Server"""


from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import Pyro4
from server import engine, Session

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Initialize the Pyro4 server and register it with a name server
server = Pyro4.Proxy("PYRONAME:AuctionServer")

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        

@app.on_event('shutdown')
def shutdown():
    engine.dispose()


@app.get('/', response_class=HTMLResponse)
async def home(request: Request ):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/user')
def create_user(username: str):
    user = server.create_user(name=username)
    return user

@app.post("/auction")
def create_auction(item_name: str, initial_price: float):
    auction_id = server.create_auction(item_name, initial_price)
    return {"auction_id": auction_id}

@app.post("/bid/{auction_id}")
def place_bid(auction_id: int, bidder_id: int, bid_amount: float):
    success = server.place_bid(auction_id, bidder_id, bid_amount)
    return {"success": success}

@app.get("/auction/{auction_id}")
def get_auction_info(auction_id: int):
    auction = server.get_auction_info(auction_id)
    return {"auction": auction}

@app.get("/auctions")
def get_auctions( skip: int, limit: int, db: Session = Depends(get_db), ):
    auctions =  server.fetch_auctions(skip, limit)
    return {"auctions": auctions}
