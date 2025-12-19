from .server import app
import uvicorn
from dotenv import load_dotenv

load_dotenv()

def main():
    uvicorn.run(app, port=8000, host="127.0.0.1")

main()