from fastapi import APIRouter, Depends, status, HTTPException, Request
from typing import List, Annotated, Any, Union
from models import  Create, Order, Message, Update, ShowOrder, Trades
from sqlmodel import Session
from db.db import get_db
import uuid
from utils.utils import authenticate_and_get_user

SessionInit = Annotated[Session,  Depends(get_db)]
router = APIRouter(prefix="/Disco-Dashboard",tags=["Disco Dashboard"])


@router.get("/get_bid", response_model=List[ShowOrder])
def all_bid(
     *, 
     session: SessionInit, 
     request: Request) ->  Any:
    
    user_details = authenticate_and_get_user(request)
    user_id = user_details.get("user_id")
    if user_details:
        try:
            bid = session.query(Order).filter(Order.created_by == user_id).all()
            return bid
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.get("/Trades/{Buyer_id}")
def get_trades(*, session: SessionInit, buyer_id: str ) -> Any:
    try:
        trade = session.query(Trades).filter(Trades.buyer_id == buyer_id).all()
        if not trade:
              raise HTTPException(status_code=404, detail="trade not found or has been deleted")
        return trade
    except Exception as error:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))
    


@router.post("/create_bid", response_model=Union[ShowOrder,Message], status_code=status.HTTP_201_CREATED)
def create_bid(
            *, 
            session: SessionInit,
            bid_in: List[Create],
            request: Request) -> Any:
    create_bid = []
    try:
        user_details = authenticate_and_get_user(request)
        user_id = user_details.get("user_id")

        for bid in bid_in:
            order_data = bid.dict()
            order_data["created_by"] = str(user_id)
            order_data = Order.model_validate(order_data)
            session.add(order_data)
            session.commit()
            session.refresh(order_data)
        create_bid.append(order_data)
        return Message(
            message="bid submitted successfully")
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.put("/update_bid/{id}", response_model=Union[ShowOrder,Message], status_code=status.HTTP_200_OK)
def update_bid(*,
                 id: uuid.UUID, 
                 bid_in: Update,
                 session: SessionInit,
                 request: Request) -> Any:
    """Update a Bid."""
    user_details = authenticate_and_get_user(request)
    user_id = user_details.get("user_id")
    if user_details:
        try:
            bid = session.get(Order, id)
            if not bid:
                raise HTTPException(status_code=404, detail="Order not found")
            if bid.created_by != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this bid")
            else:
                update_bid = bid_in.model_dump(exclude_unset=True)
                bid.sqlmodel_update(update_bid)
                session.add(bid)
                session.commit()
                session.refresh(bid)
                return Message(
                        message="Bid updated successfully")
        
        except Exception as error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(error))


@router.delete("/delete_bid/{id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_bid(
            *,
            id: uuid.UUID,
            session: SessionInit,
            request: Request) -> Any:
    """
    Delete an Order.
    """
    user_details = authenticate_and_get_user(request)
    if user_details:
        bid = session.get(Order, id)
        if not bid:
            raise HTTPException(status_code=404, detail="Bid not found")
        session.delete(bid)
        session.commit()
        return Message(
                message="Bid deleted successfully")