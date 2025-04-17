"""FastAPI application entry point."""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from secure import Secure
from http_.api_v1 import router as api_v1_router
from logutils import get_logger
from utils import get_env_var

logger = get_logger(__name__)
origins = get_env_var("ORIGINS", default="*").split(",")
secure_headers = Secure.with_default_headers()

app = FastAPI(
    title="Deku Enterprise API",
    description="",
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)
    return response


@app.exception_handler(HTTPException)
def http_exception_handler(_, exc: HTTPException):
    """
    Handle HTTP exceptions and return a structured error response.

    Args:
        exc (HTTPException): The HTTP exception raised.

    Returns:
        JSONResponse: A structured JSON response with error details.
    """
    logger.error("HTTPException: %s | Status Code: %d", exc.detail, exc.status_code)
    return JSONResponse(
        {"error": {"type": "HTTPException", "detail": exc.detail}},
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_, exc: RequestValidationError):
    """
    Handle validation errors and return a structured error response.

    Args:
        exc (RequestValidationError): The validation error raised.

    Returns:
        JSONResponse: A structured JSON response with error details.
    """
    first_error = exc.errors()[0]
    field = " -> ".join(str(loc) for loc in first_error["loc"])
    message = first_error.get("msg", "Invalid input")
    error_message = f"Field: {field}, Message: {message}"

    logger.error("Validation Error: %s", error_message)
    return JSONResponse(
        {"error": {"type": "ValidationError", "field": field, "message": message}},
        status_code=422,
    )


@app.exception_handler(Exception)
def internal_exception_handler(_, exc: Exception):
    """
    Handle unexpected exceptions and return a generic error response.

    Args:
        exc (Exception): The unexpected exception raised.

    Returns:
        JSONResponse: A structured JSON response with error details.
    """
    logger.exception("Unhandled Exception: %s", exc)
    return JSONResponse(
        {
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred. Please try again later.",
            }
        },
        status_code=500,
    )


app.include_router(api_v1_router)
