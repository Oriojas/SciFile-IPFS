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
def load_data_ipfs(local_file: str):
    response = Ipfs().load_pdf(file=local_file)
    response = dict(response)

    json_response: object = jsonable_encoder(response)

    return json_response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
