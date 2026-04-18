from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.app.routers import books, llm, users

app = FastAPI(
    title="TheLibrary API",
    version="0.2.0",
)

@app.exception_handler(DomainError)
def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc)},
    )

# подключаем роуты
app.include_router(users.router)
app.include_router(books.router)
app.include_router(llm.router)


@app.get("/")
def root():
    return {"message": "API is running"}
