from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# Define models
class Order(BaseModel):
    client_id: str
    quantity: int

# Define global variables
orders = []
baristas = 10
clients_per_group = 150
brewing_time = 45  # seconds
delusional_ddoser_ip = "192.168.1.100"

# Routes
@app.post("/order/")
async def place_order(order: Order):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    # Add the order to the global orders list
    orders.append(order)

    # Simulate processing time based on quantity
    processing_time = brewing_time * order.quantity
    time.sleep(processing_time)

    return {"message": f"Order received for {order.quantity} americano(s)"}

@app.get("/start/")
async def start_preparing_orders():
    if len(orders) == 0:
        return {"message": "No orders to prepare"}

    # Pick orders to prepare based on available baristas
    orders_to_prepare = orders[:baristas]
    orders[:] = orders[baristas:]

    return {"message": "Started preparing orders", "orders": orders_to_prepare}

@app.post("/finish/")
async def finish_preparing_orders(finished_orders: List[Order]):
    for order in finished_orders:
        print(f"Order for client {order.client_id} is ready")

    return {"message": "Orders finished"}

# Middleware to defend against the delusional DDoSer
@app.middleware("http")
async def defend_against_ddos(request: Request, call_next):
    if request.client.host == delusional_ddoser_ip:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    response = await call_next(request)
    return response

# Additional Setup
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
