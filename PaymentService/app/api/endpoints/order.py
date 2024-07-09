from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import  Order , OrderItem , ShippingAddress
from app.schemas.order import OrderCreate ,OrderItemRead , OrderRead
from app.schemas.auth import TokenResponse
from app.enums.status_enum import StatusEnum
from app.api.deps import role_check
from typing import Annotated , Union

router = APIRouter()


# Create Order with Shipping Address and Order Items
@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: Session = Depends(get_session), current_user: Annotated[Union[TokenResponse, None], Depends(role_check(['customer', 'admin']))] = None):
    try:
        # Create shipping address
        db_shipping_address = ShippingAddress(
            user_id=current_user["id"], 
            address=order.shipping_address.address,
            company_name=order.shipping_address.company_name,
            city=order.shipping_address.city,
            state=order.shipping_address.state,
            postal_code=order.shipping_address.postal_code,
            country=order.shipping_address.country,
            phone_number=order.shipping_address.phone_number,
            is_default=order.shipping_address.is_default
        )
        db.add(db_shipping_address)
        db.commit()
        db.refresh(db_shipping_address)

        # Create order
        db_order = Order(
            customer_id=current_user["id"], 
            shipping_address_id=db_shipping_address.id,
            customer_name=current_user["first_name"],
            customer_email=current_user["email"],  
            # customer_name=order.customer_name,
            # customer_email=order.customer_email,
            description=order.description,
            total_amount=order.total_amount,
            payment_type=order.payment_type,
            order_status=order.order_status
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Create order items
        db_order_items = []
        for item in order.items:
            db_order_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                title=item.title,
                quantity=item.quantity,
                item_price=item.item_price,
                total_amount= (item.item_price * item.quantity)
            )
            db_order_items.append(db_order_item)
            db.add(db_order_item)
        db.commit()

        return db_order
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order creation failed")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

