from decimal import Decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.bank import BankAccount, CardBlockError, InsufficientFundsError,InvalidPINError

app = FastAPI(title = "Banking & Core Agent API")

mock_account = BankAccount(
    account_id= 100,                     #int 
    owner_name= "Daksh",                 #string
    initial_balance= Decimal("1000.00"), # Decimal
    plaintext_pin= "1290"                # string
)

class WithdrawRequest(BaseModel): # its a json form of this class good for payload representation
    account_id: int
    pin: str
    amount : float

@app.get("/health")
async def health_check():
    return{"status": "online", 
           "system": "Banking Core API"}

@app.post("/withdraw")
async def withdraw_funds(payload:WithdrawRequest): # payload must be in the form of the class WithdrawRequest
    if payload.account_id != mock_account.account_id:
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        mock_account.withdraw(Decimal(str(payload.amount)), payload.pin)
        return{
            "status": "success",
            "account_id": mock_account.account_id,
            "new_balance": float(mock_account.balance)
        }
    except InvalidPINError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except CardBlockError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    