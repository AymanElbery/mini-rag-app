from fastapi import FastAPI

from routes import base_router, data_router

app = FastAPI()

app.include_router(base_router)
app.include_router(data_router)

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
# else:
#     print("Running in production")