from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

import utils
from services.ZeroSSLService import ZeroSSLService
from services.AccountService import AccountService

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

account_service = AccountService()
url = "http://localhost:8000" if utils.is_dev() else "https://api.quelenis.com/zerossl/get_cert"


class GetCert(BaseModel):
    email: str
    domain: str


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/get_cert")
async def get_cert(payload: GetCert = list) -> JSONResponse:
    try:
        random_email = account_service.generate_random_email()

        zerossl_service = ZeroSSLService()
        zerossl_service.get_cert(payload.email, random_email, payload.domain)
        zerossl_service.close()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Le certificat a été récupéré avec succès.",
                "url": f"{url}/static/{zerossl_service.get_path_image()}"
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur est survenue lors de la récupération du certificat. Veuillez réessayer ultérieurement."
        )
