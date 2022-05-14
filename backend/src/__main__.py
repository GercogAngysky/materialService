import uvicorn


from settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
# uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload