from fastapi import FastAPI

from api.app.routers import books, llm, users

app = FastAPI(
    title="TheLibrary API",
    version="0.1.0",
)

# подключаем роуты
app.include_router(users.router)
app.include_router(books.router)
app.include_router(llm.router)


@app.get("/")
def root():
    return {"message": "API is running"}
