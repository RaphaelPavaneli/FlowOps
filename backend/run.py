import os
from pathlib import Path

import uvicorn


if __name__ == "__main__":
    backend_directory = Path(__file__).resolve().parent
    os.chdir(backend_directory)

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
