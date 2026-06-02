from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Application starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down...")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query_parameter": q
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )