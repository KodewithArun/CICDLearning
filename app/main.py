from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.calculator import add, divide, multiply, subtract

app = FastAPI(
    title="Simple Calculator API",
    description="A simple calculator API built with FastAPI for learning CI/CD",
    version="1.0.0",
)


class OperationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationRequest(BaseModel):
    operation: OperationType
    a: float
    b: float


class CalculationResponse(BaseModel):
    operation: str
    a: float
    b: float
    result: float


@app.get("/")
def root():
    return {
        "message": "Welcome to the Calculator API!",
        "docs_url": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/calculate", response_model=CalculationResponse)
def calculate(req: CalculationRequest):
    try:
        if req.operation == OperationType.ADD:
            res = add(req.a, req.b)
        elif req.operation == OperationType.SUBTRACT:
            res = subtract(req.a, req.b)
        elif req.operation == OperationType.MULTIPLY:
            res = multiply(req.a, req.b)
        elif req.operation == OperationType.DIVIDE:
            res = divide(req.a, req.b)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        return CalculationResponse(operation=req.operation.value, a=req.a, b=req.b, result=res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
