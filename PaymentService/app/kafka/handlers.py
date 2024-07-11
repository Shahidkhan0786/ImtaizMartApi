from app.proto import user_pb2
from app.proto import token_validation_pb2
import logging
import stripe
from app.proto.order_pb2 import Order
from app.proto.payment_pb2 import PaymentResponse
from app.core.config import settings
from app.kafka.producer import kafka_producer
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_info_store = {}
token_response_store = {}
# Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# validate token response consumer 
async def handle_validate_token_responses(msg):
    try:
        logger.info("Handling validate token response...")
        
         # Log the raw message content
        logger.debug(f"Raw message received: key {msg.key.decode()} value {msg.value}")
        print(f"Raw message received: {msg.value}")
        
        # Parse the message
        user_message = token_validation_pb2.ValidateTokenResponse()
        user_message.ParseFromString(msg.value)
        
        # Access parsed data
        validation_result = user_message.validation_result
        if validation_result.valid:
            user_data = validation_result.data
            user_info = user_data.user
            user_role = user_data.roles
            logger.info(f"Key is {msg.key.decode()}")
            logger.info(f"Valid token for user: id: {user_info.id} , {user_info.first_name} {user_info.last_name} ({user_info.email}) and role is {user_role}")
            token_response_store[msg.key.decode()] = {
                "id": user_info.id,
                "first_name": user_info.first_name,
                "last_name": user_info.last_name,
                "email": user_info.email,
                "roles": user_role,
                "token_valid": validation_result.valid,
                "token_message": validation_result.message,
            }
            return
        else:
            logger.warning(f"Token validation failed: {validation_result.message}")
            return False
    
    except Exception as e:
        logger.error(f"Failed to process message from topic {msg.topic}: {e}")
        return False

    

async def handle_user_response(msg):
    try:
        logger.info("Handle User response")
        user_message = user_pb2.UserDetailResponse()
        user_message.ParseFromString(msg.value)
        logger.debug(f"Parsed user message: {user_message}")
        
        user_info_store[user_message.id] = {
            "id": user_message.id,
            "first_name": user_message.user.first_name,
            "last_name": user_message.user.last_name,
            "email": user_message.user.email
        }
        
        logger.info(f"Processed user response message: {user_info_store[user_message.id]}")
    
    except Exception as e:
        logger.error(f"Error processing user response message: {e}")
        logger.debug(f"Failed message details: {msg}")

# async def handle_product_event(msg):
#     product_message = product_pb2.Product()
#     product_message.ParseFromString(msg.value)
#     logger.info(f"Processed product event message: {product_message}")

async def handle_payment_request(msg):
    try:
        logger.info("Handle payment request")

        # Parse the incoming order message
        order_message = Order()
        order_message.ParseFromString(msg.value)
        logger.debug(f"Parsed order message: {order_message}")

        # Extract order details
        order_id = order_message.order_id
        customer_email = order_message.customer_email
        total_amount = int(order_message.total_amount * 100)  # Convert to cents
        items = order_message.items
        logger.info(f"Order message {order_message}")
        logger.info(f"Items {order_message.items}")
        # Create Stripe checkout session
        line_items = [
            {
                'price_data': {
                    'currency': settings.CURRENCY,
                    'product_data': {'name': item.title},
                    'unit_amount': int(item.price * 100),
                },
                'quantity': item.quantity,
            } for item in items
        ]

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
                customer_email=customer_email,
            )
            logger.info(f"Created Stripe session id : {session.id}")
            logger.info(f"Created Stripe session url : {session.url}")
            # Create a payment response message
            payment_response = PaymentResponse(
                order_id=order_id,
                payment_url=session.url,
                session_id=session.id,
                status='created'
            )

            # Serialize and send the response message
            serialized_payment_response = payment_response.SerializeToString()
            await kafka_producer.send("payment_response_topic", key=str(order_id).encode(), value=serialized_payment_response)
            logger.info(f"Sent payment response for order ID {order_id}")

        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise e

    except Exception as e:
        logger.error(f"Error processing payment request message: {e}")
        logger.debug(f"Failed message details: {msg}")