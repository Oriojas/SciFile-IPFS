import ast
import uvicorn
import pandas as pd
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

        with open(f"pdf_data/{file.filename}", "wb") as output_file:
            output_file.write(contents)

        print(file.filename)

        response = Ipfs().load_pdf(file=file.filename)

        print(JSONResponse(content={"filename": file.filename, "content_length": len(contents)}, status_code=200))

        json_output = jsonable_encoder(response)

        sp.DB().upload_data(name=file.filename,
                            review='upload',
                            n_rev=0,
                            metadata=f'{json_output}')

        return JSONResponse(content=json_output)

    except Exception as e:

        print(JSONResponse(content={"error": str(e)}, status_code=500))
        response = {}

        return JSONResponse(response)


@app.post("/upload_meta_article/")
async def upload_meta_article(json_data: dict, x_token: str = Header(...)):
    try:

        print(json_data)
        print("Token recibido:", x_token)

        response = JSONResponse(content={"status": "success", "message": "JSON data received successfully"},
                                status_code=200)
        print(response)

        response_rev = Ipfs().load_rev(description=json_data.get('description'),
                                       hash='0000',
                                       name=json_data.get('name'),
                                       review=json_data.get('description'),
                                       n_rev=0)

        sp.DB().upload_data(name=json_data.get('name'),
                            review=json_data.get('description'),
                            n_rev=1,
                            metadata=f'{response_rev}')

        json_output = jsonable_encoder(response_rev)

        return JSONResponse(content=json_output)

    except Exception as e:
        response = JSONResponse(content={"error": str(e)}, status_code=500)
        print(response)
        json_data = {}
        return JSONResponse(json_data)


@app.post("/upload_meta_review/")
async def upload_meta_review(json_data: dict, x_token: str = Header(...)):
    try:

        print(json_data)
        print("Token recibido:", x_token)

        response = JSONResponse(content={"status": "success", "message": "JSON data received successfully"},
                                status_code=200)
        print(response)

        response_rev = Ipfs().load_rev(description=json_data.get('review'),
                                       hash='0000',
                                       name=json_data.get('name'),
                                       review=json_data.get('review'),
                                       n_rev=0)

        sp.DB().upload_data(name=json_data.get('name'),
                            review=json_data.get('review'),
                            n_rev=1,
                            metadata=f'{response_rev}')

        json_output = jsonable_encoder(response_rev)

        return JSONResponse(content=json_output)

    except Exception as e:
        response = JSONResponse(content={"error": str(e)}, status_code=500)
        print(response)
        json_data = {}
        return JSONResponse(json_data)


@app.get("/query/")
async def query():
    df = pd.DataFrame(sp.DB().query_article())

    list_df = []
    for col in range(len(df)):
        print(df['metadata'].loc[col])
        list_df.append(ast.literal_eval(df['metadata'].loc[col]))

    json_output = jsonable_encoder(list_df)

    return JSONResponse(content=json_output)


@app.post('/hola_mundo/')
async def hola_mundo():
    return 'Hola mundo BENDER'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
