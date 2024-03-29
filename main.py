import uvicorn
import json
from ipfs import Ipfs
import save_postgres as sp
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Header

app = FastAPI()

origins = ['*']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                   allow_headers=["*"], )


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Guardar el archivo en local con formato PDF
        with open(f"pdf_data/{file.filename}", "wb") as output_file:
            output_file.write(contents)

        return JSONResponse(content={"filename": file.filename, "content_length": len(contents)}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/upload_meta_article/")
async def upload_meta_article(json_data: dict, x_token: str = Header(...)):
    try:

        print(json_data)
        print("Token recibido:", x_token)

        response = JSONResponse(content={"status": "success", "message": "JSON data received successfully"},
                                status_code=200)
        print(response)

        sp.DB().upload_data(name=json_data.get('name'),
                            review=json_data.get('description'),
                            n_rev=0,
                            metadata=f'{json_data}')

        return json_data

    except Exception as e:
        response = JSONResponse(content={"error": str(e)}, status_code=500)
        print(response)
        json_data = {}
        return json_data


@app.post('/load_review/')
async def load_review(description: str, hash: str, name: str, review: str, n_rev: int):
    response_rev = Ipfs().load_rev(description=description,
                                   hash=hash,
                                   name=name,
                                   review=review,
                                   n_rev=n_rev)

    response_rev = dict(response_rev)

    json_response_rev: object = jsonable_encoder(response_rev)

    sp.DB().upload_data(name=name,
                        review=review,
                        n_rev=n_rev,
                        metadata=f'{json_response_rev}')

    return json_response_rev


@app.post('/hola_mundo/')
async def hola_mundo():
    return 'Hola mundo BENDER'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
