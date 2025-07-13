from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError
from .notes_endpoint import notes_router as notes_router
from .tags_endpoint import tags_router as tags_router
app = FastAPI()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized", "detail": exc.detail}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(JWTError)
async def jwt_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid token", "custom_message": "JWT error handled globally"},
    )



app.include_router(notes_router)
app.include_router(tags_router)