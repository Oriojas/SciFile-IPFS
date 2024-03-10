import uvicorn
from ipfs import Ipfs
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.post('/load_data_ipfs/')
def load_data_ipfs(local_file: str, description: str):
    response = Ipfs().load_pdf(file=local_file, description=description)
    response = dict(response)

    json_response: object = jsonable_encoder(response)

    return json_response


@app.post('/load_review/')
def load_review(description: str, hash: str, name: str, review: str, n_rev: int):
    response_rev = Ipfs().load_rev(description=description,
                                   hash=hash,
                                   name=name,
                                   review=review,
                                   n_rev=n_rev)

    response_rev = dict(response_rev)

    json_response_rev: object = jsonable_encoder(response_rev)

    return json_response_rev


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
