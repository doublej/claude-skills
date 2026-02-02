#!/usr/bin/env python3
import os
from maya1.api_v2 import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "9527"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
