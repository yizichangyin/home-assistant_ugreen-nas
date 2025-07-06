from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import logging
from token_refresher import TokenRefresher

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/token")
async def get_token(username: str = Query(...), password: str = Query(...)):
    refresher = TokenRefresher(
        username=username,
        password=password
    )

    success = await refresher.fetch_token_async()
    if success:
        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "msg": "success",
                "data": {
                    "token": refresher.token
                }
            }
        )
    else:
        raise HTTPException(
            status_code=401,
            content={ # type: ignore
                "code": 401,
                "msg": "Token refresh failed",
            }
        )