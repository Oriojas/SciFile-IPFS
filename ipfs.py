import os
import json
from lighthouseweb3 import Lighthouse


class Ipfs:

    def __init__(self):
        self.lh = Lighthouse(token=os.environ['KEY'])

    def load_pdf(self, file: str, description: str, tag="pdf_test", file_path="pdf_data/"):
        """
        this function load ipfs file in lighthouse
        :param description: description article
        :param file: file name to load
        :param tag: tag for identify file class
        :param file_path: local folder
        :return:
        """
        upload_with_tag = self.lh.upload(source=f'{file_path}{file}', tag=tag)
        metadata = upload_with_tag.get('data')
        print("File Upload with Tag Successful!")
        print(metadata)

        # {'Name': 'test.pdf', 'Hash': 'QmaEmcgUBVSKtVHbtNZRr18dWK1vWsPSzEiUNTpkAiNe7Z', 'Size': '9028'}

        nft_metadata = {"description": description,
                        "hash": metadata.get('Hash'),
                        "name": metadata.get('Name'),
                        "review": "Initial review",
                        "n_rev": 0}

        with open(f'{os.environ["ROOT_FOLDER"]}/json_data/nft_metadata.json', 'w') as jf:
            json.dump(nft_metadata, jf)

        upload_with_tag = self.lh.upload(source=f'json_data/nft_metadata.json', tag=tag)
        nft_metadata = upload_with_tag.get('data')

        print("File Upload with Tag Successful!")
        print(nft_metadata)

        return nft_metadata

    def load_rev(self, description: str, hash: str, name: str, review: str, n_rev: int):

        json_data_review = {"description": description,
                            "hash": hash,
                            "name": name,
                            "review": review,
                            "n_rev": n_rev}

        with open(f'{os.environ["ROOT_FOLDER"]}/json_data/review_metadata.json', 'w') as jf:
            json.dump(json_data_review, jf)

        upload_dict_tag = self.lh.upload(source='json_data/review_metadata.json')
        json_metadata = upload_dict_tag.get('data')
        print("File Upload with Tag Successful!")
        print(json_metadata)

        return json_metadata


if __name__ == "__main__":
    Ipfs().load_pdf(file='test.pdf', description='Test file')
    # Ipfs().load_rev(description="Test file",
    #                 hash="QmaEmcgUBVSKtVHbtNZRr18dWK1vWsPSzEiUNTpkAiNe7Z",
    #                 name="test.pdf",
    #                 review="Test large review XDXDXDXDXDXDXD",
    #                 n_rev=1)
