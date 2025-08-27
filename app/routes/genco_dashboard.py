from fastapi import APIRouter, Depends, status, HTTPException, Request
from typing import List, Annotated, Any, Union
from models import Create, Message, Update, ShowOrder, Order, Trades
from sqlmodel import Session
from db.db import get_db
import uuid
from utils.utils import authenticate_and_get_user

SessionInit = Annotated[Session, Depends(get_db)]
router = APIRouter(prefix="/Genco-Dashboard", tags=["Genco Dashboard"])


@router.get("/get_offer", response_model=List[ShowOrder])
def all_offer(
    *,
    session: SessionInit,
    request: Request) -> Any:

    user_details = authenticate_and_get_user(request)
    user_id = user_details.get("user_id")
    if user_details:
        try:
            offer = session.query(Order).filter(Order.trader_id == user_id).all()
            return offer
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))



@router.get("/Trades/{Seller_id}")
def get_trades(*, session: SessionInit, seller_id: str) -> Any:
    try:
        trade = session.query(Trades).filter(Trades.seller_id == seller_id).all()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found or has been deleted")
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    

@router.post("/create_offer", response_model=Union[Message,ShowOrder], status_code=status.HTTP_201_CREATED)
def create_offer(
                *,
                session: SessionInit,
                offer_in: List[Create],
                request: Request) -> Any:
    
    create_offer = []
    try:
        user_details = authenticate_and_get_user(request)
        user_id = user_details.get("user_id")

        for offer in offer_in:
            order_data = offer.dict()
            order_data["trader_id"] = str(user_id)
            order_data = Order.model_validate(order_data)
            session.add(order_data)
            session.commit()
            session.refresh(order_data)
        create_offer.append(order_data)
        return  Message(message="Offer submitted successfully")
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    

@router.put("/update_offer/{id}", response_model=Union[ShowOrder,Message], status_code=status.HTTP_200_OK)
def update_offer(*,
                 id: uuid.UUID, 
                 offer_in: Update,
                 session: SessionInit,
                 request: Request
                 ) -> Any:
    """Update an Offer."""
    user_details = authenticate_and_get_user(request)
    user_id = user_details.get("user_id")
    if user_details:
        try:
            offer = session.get(Order, id)
            if not offer:
                raise HTTPException(status_code=404, detail="Offer not found")
            
            if offer.trader_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this offer")
            else: 
                update_offer = offer_in.model_dump(exclude_unset=True)
                offer.sqlmodel_update(update_offer)
                session.add(offer)
                session.commit()
                session.refresh(offer)
                return Message(message="Offer updated successfully")
        except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("/delete_offer/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_offer(
            *, 
            id: uuid.UUID,
            session: SessionInit,
            request: Request
            ) -> Any:
    """Delete an Offer."""

    user_details = authenticate_and_get_user(request)
    if user_details:
        offer = session.get(Order, id)
        if not offer:
            raise HTTPException(status_code=404, detail="offer not found")
        session.delete(offer)
        session.commit()
        return Message(message="offer deleted successfully")