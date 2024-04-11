from typing import TypeVar, Generic, Optional, List, Union, Any
from pydantic import BaseModel, ValidationError, create_model
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

T = TypeVar('T')

class ApiResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None


def response_model(message: str = "", errors: List[dict] = None, status: str = "success", data=None):
    model = ApiResponse(status=status, message=message, data=data, errors=errors)
    logging.debug(model)
    return model
