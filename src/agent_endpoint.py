import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from decimal import Decimal

from src.bank import BankAccount,CardBlockError,InsufficientFundsError,InvalidPINError

app = FastAPI(title="AI Agent Orchestration API")

mock_account = BankAccount(
    account_id= 100,                     #int 
    owner_name= "Daksh",                 #string
    initial_balance= Decimal("1000.00"), # Decimal
    plaintext_pin= "1290"                # string
)

# 1. Structured Output Contract: Enforces strict data extraction from user prompt
class AgentActionSchema(BaseModel):
    action: str = Field(description="Actions that can be performed 'Balance' or 'withdraw'")
    amount: float = Field(default = 0.0, description="Amount involved in the transaction")
    pin: str = Field(description="User PIN provided in natural language")

"""
2. Preventing "Network Congestion" (Real-Time Transmission)
In the LLM script you shared, yield solves a major user experience problem. 
If an AI takes 10 seconds to generate a full 500-word paragraph, waiting for a traditional return means the user stares at a blank, frozen screen for 10 seconds.
By using yield:The LLM generates Word 1 → yield pushes it down the network pipe immediately.
The client's browser renders Word 1 instantly.The server generates Word 2 → yield pushes it down.
This creates the classic "typing" effect seen in ChatGPT. 
The network pipe is never overwhelmed by a massive, sudden dump of data, and the user experiences zero perceived delay.
"""

async def simulate_llm_stream(prompt:str):
    yield "data: [Agent Thinks]: Analyzing user request..\n"
    await asyncio.sleep(0.5) # Simulate network/inference latency

    yield f"data: [Agent Thinks]: Parsing intent from prompt: '{prompt}'\n\n"
    await asyncio.sleep(0.5)

    yield "data: [Agent Execution]: Executing BankAccount engine verification...\n\n"
    await asyncio.sleep(0.5)

@app.get("/agent/stream")
async def stream_agent_execution(prompt:str):
    """
    Simulates streaming AI reasoning steps to the client via Server-Sent Events (SSE).
    """
    return StreamingResponse(
        simulate_llm_stream(prompt),
        media_type="text/event-stream"
    )

@app.post("/agent/execute")
async def execute_extracted_action(payload: AgentActionSchema):
    """
    Takes structured output (JSON extracted from prompt) and conducts 
    the underlying BankAccount state machine safely.
    """
    if payload.action.lower() == "withdraw":
        try:
            mock_account.withdraw(Decimal(str(payload.amount)), payload.pin)
            return {
                "status": "success",
                "message": f"Successfully withdrew ₹{payload.amount}",
                "remaining_balance": float(mock_account.balance)
            }
        except (InvalidPINError, CardBlockError, InsufficientFundsError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    elif payload.action.lower() == "balance":
        return {"status": "success", "balance": float(mock_account.balance)}
    
    raise HTTPException(status_code=422, detail="Unsupported agent action")