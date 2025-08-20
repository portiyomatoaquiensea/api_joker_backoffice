from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.routes import robot_statements
from app.core.database import engine_realtime, engine_dataplayer, BaseRealtime, BaseDataplayer
from app.schemas.response import ResponseDto

app = FastAPI(
    title="Multi-DB FastAPI Project",
    docs_url="/swagger",
    redoc_url="/redoc",
)

# ----------------------------
# Create tables if not exist
# ----------------------------
BaseRealtime.metadata.create_all(bind=engine_realtime)
BaseDataplayer.metadata.create_all(bind=engine_dataplayer)

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(robot_statements.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]  # get the first error
    field = first_error.get("loc")[-1]  # field name
    msg = first_error.get("msg")
    error_message = f"{field}: {msg}"

    return JSONResponse(
        status_code=200,
        content=ResponseDto.error(
            message=error_message,
            statusCode=422,
            data=[]
        ).dict()
    )

# Exception handler for HTTPException to always use ResponseDto
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        # Already a ResponseDto
        return JSONResponse(status_code=200, content=exc.detail)
    return JSONResponse(
        status_code=200,
        content=ResponseDto.error(message=str(exc.detail), statusCode=exc.status_code, data=[]).dict()
    )
# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "Multi-DB FastAPI Project is running!"}

