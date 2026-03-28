import uvicorn
from main import app


def start():
    print("starting server")
    uvicorn.run(app, host='0.0.0.0', port=3010)
    print("server started")


if __name__ == "__main__":
    start()
