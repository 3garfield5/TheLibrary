from fastapi import FastAPI

from api.app.routers import users, books

app = FastAPI(
    title="TheLibrary API",
    version="0.1.0",
)

# подключаем роуты
app.include_router(users.router)
app.include_router(books.router)


@app.get("/")
def root():
    return {"message": "API is running"}
