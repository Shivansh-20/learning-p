#This is a simple stock basic operation simulator to Learn about API basics and SQL implementation in the language
#while i was building this , I learnt about fastapi and cursor, then i explored REST,error handling and matplotlib plus pandas
#while Learning this, I also tried  plotting graphs using matplot and fetching stocks data in my google collab notebook
import sqlite3
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

# 1. CREATE FASTAPI APPLICATION
app = FastAPI()

# 2. MOCK STOCK PRICES 

prices = {
    "RELIANCE": 2900,
    "TCS":3900,
    "INFY":3000,
    "HCL":2800
}


#pydantic basemodel
class Trade(BaseModel):
    ticker: str
    quantity: int = Field(gt= 0)

#initiliaze database
def initialiaze_database():
    connection = sqlite3.connect("trading.db")
    cursor = connection.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio(
ticker TEXT PRIMARY KEY,
quantity INT,
average_buyprice REAL      -- like float , -- -> sql comment, #-> for python
)
"""
)
    connection.commit() #can use "with" statement for automatic resource free, but not good practise here 
    connection.close()

# Create database/table when program starts
initialiaze_database()

# 5. POST /trade
@app.post("/trade")
def trade_stock(trade:Trade):
    ticker = trade.ticker.upper()
    quantity = trade.quantity
    # Check whether stock exists in our mock prices
    if ticker not in prices: 
        raise HTTPException( 
            status_code=400, 
            detail="Unknown stock ticker" )
    # Get current mock price
    price = prices[ticker] #store the value in  variable price from dict prices of company passed as  ticker
    # Calculate trade value
    total = quantity * price 
    # Connect to database 
    connection = sqlite3.connect("trading.db")
    cursor = connection.cursor()

# Check whether we already own this stock
    cursor.execute(
        "Select quantity,average_buyprice from portfolio where ticker = ?",  #quantity at index 0 avg at 1
    (ticker,)
)
    row = cursor.fetchone()  #() are imp , to actually call the function
    # STOCK DOES NOT EXIST → INSERT
    if row is None:
        cursor.execute(
        """
            insert into portfolio (ticker,quantity,average_buyprice)
            values(?,?,?)
        """,
        (ticker,quantity,price)
        )
        # STOCK ALREADY EXISTS → UPDATE
    else:
        old_quantity = row[0]
        old_avg_price = row[1]  #average_buyprice
        new_quantity = old_quantity + quantity
        new_avg_price = (
    (old_quantity * old_avg_price)
    + (quantity * price)
) / new_quantity
        cursor.execute(
        """ 
             update portfolio
             set quantity = ?,  #comma says one more coming
             average_buyprice = ?
             where ticker = ?
        """,
        (new_quantity,new_avg_price,ticker)
        )
    connection.commit()
    connection.close()
    # Send  JSON response usind {}  for dict
    return {                            
        "ticker": ticker,
        "quantity_bought": quantity,
        "price":price,
        "total":total
    } 

# 6. GET /portfolio
@app.get("/portfolio")
def get_portfolio():
    connection = sqlite3.connect("trading.db")
    cursor = connection.cursor()
    # Get every row
    cursor.execute("select * from portfolio")
    rows = cursor.fetchall()
    connection.close()
    # Store formatted stocks
    stocks = []
    # Total portfolio value
    total_value = 0
    # Process every database row
    for row in rows:
        ticker,quantity,average_buyprice = row
        # Current mock market price
        current_price = prices[ticker]
        # Current value of this holding
        value = quantity * current_price

        stocks.append({
            "ticker":ticker,
            "quantity":quantity,
            "current_price":current_price,
            "value":value
        })
        total_value += value
    return {
        "stocks":stocks,
        "total_value":total_value
    }
#  we're calculating based on the current mock price, not avg_buy_price


