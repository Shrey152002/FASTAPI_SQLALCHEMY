from fastapi import Depends, HTTPException, FastAPI, status ,Request
from pydantic import BaseModel
from typing import Annotated
import models
from fastapi import Request
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import logging


logging.basicConfig(level=logging.DEBUG)

app = FastAPI(debug=True)
models.Base.metadata.create_all(bind=engine)

class MovieBase(BaseModel):
    title: str
    description: str
    rating: int  

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: int
    username: str
    email: str

class BookingBase(BaseModel):
    id: int
    user_id: int
    movie_title: str
    seats: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Booking API"}

@app.post("/")
async def dialogflow_webhook(request: Request, db: Session = Depends(get_db)):
    req_json = await request.json()
    intent_name = req_json['queryResult']['intent']['displayName']
    parameters = req_json['queryResult']['parameters']
    contexts = req_json['queryResult']['outputContexts']
    
    logging.debug(f"Intent Name: {intent_name}")
    logging.debug(f"Parameters: {parameters}")
    logging.debug(f"Contexts: {contexts}")

    context_params = {}
    for context in contexts:
        if 'parameters' in context:
            context_params.update(context['parameters'])

    logging.debug(f"Context Parameters: {context_params}")

    if intent_name == 'Get Movie List Intent':
        movies = db.query(models.Movie).all()
        if not movies:
            fulfillment_text = "No movies available currently."
        else:
            movie_list = ", ".join([movie.title for movie in movies])
            fulfillment_text = f"Here are the available movies: {movie_list}. Which movie would you like to book?"

        return {
            "fulfillmentText": fulfillment_text,
            "outputContexts": [
                {
                    "name": f"{req_json['session']}/contexts/awaiting_movie_selection",
                    "lifespanCount": 30,
                }
            ]
        }

    elif intent_name == 'Book Ticket Intent':
        movie_title = parameters.get('movie_title')
        if not movie_title:
            fulfillment_text = "Please specify a movie title to book a ticket."
        else:
            movie = db.query(models.Movie).filter(models.Movie.title == movie_title).first()
            if not movie:
                fulfillment_text = f"Sorry, the movie '{movie_title}' is not available."
            else:
                fulfillment_text = f"You chose {movie_title}. How many seats would you like to book?"

        return {
            "fulfillmentText": fulfillment_text,
            "outputContexts": [
                {
                    "name": f"{req_json['session']}/contexts/awaiting_seats",
                    "lifespanCount": 30,
                    "parameters": {
                        "movie_title": movie_title
                    }
                }
            ]
        }

    elif intent_name == 'Collect Seats Intent':
        seats = parameters.get('seats')
        movie_title = context_params.get('movie_title')

        fulfillment_text = f"ok {seats} selected for {movie_title}, Please provide your user ID to proceed with the booking."
        return {
           "fulfillmentText": fulfillment_text,
           "outputContexts": [
                {
                    "name": f"{req_json['session']}/contexts/awaiting_user_id",
                    "lifespanCount": 30,
                    "parameters": {
                        "movie_title": movie_title,
                        "seats": seats
                    }
                }
            ]
        }

    elif intent_name == 'Collect User ID Intent':
        user_id = parameters.get('userid')
        movie_title = context_params.get('movie_title')
        seats = context_params.get('seats')

        fulfillment_text = f"Thank you user id: {user_id}. Please confirm your booking: {seats} seats for the movie '{movie_title}'?"
        return {
            "fulfillmentText": fulfillment_text,
            "outputContexts": [
                {
                    "name": f"{req_json['session']}/contexts/awaiting_confirmation",
                    "lifespanCount": 30,
                    "parameters": {
                        "movie_title": movie_title,
                        "seats": seats,
                        "userid": user_id
                    }
                }
            ]
        }

    elif intent_name == 'Confirm Booking Intent':
        user_id = context_params.get('userid')
        movie_title = context_params.get('movie_title')
        seats = context_params.get('seats')

        logging.debug(f"User ID: {user_id}, Movie Title: {movie_title}, Seats: {seats}")
        users = db.query(models.User).all()
        user_ids = [user.id for user in users]
        if not user_id or not movie_title or not seats:
            fulfillment_text = "Missing required parameters. Please provide user ID, movie title, and seats."
        elif user_id in user_ids:
            booking = models.Booking(user_id=user_id, movie_title=movie_title, seats=seats)
            db.add(booking)
            db.commit()
            db.refresh(booking)

            fulfillment_text = f"Booking confirmed for {seats} seats for the movie '{movie_title}'. Your booking ID is {booking.id}. Enjoy your movie!"
        else:
            fulfillment_text = f"Login first pls"
        return {
            "fulfillmentText": fulfillment_text
        }

    return {
        "fulfillmentText": "Intent not handled."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)   