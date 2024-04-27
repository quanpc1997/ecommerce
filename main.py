import uvicorn

from app.app import create_app


def main():
    app = create_app()
    uvicorn.run(app, host="localhost", port=15000)


if __name__ == "__main__":
    main()
