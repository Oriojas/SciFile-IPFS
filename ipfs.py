import os
from lighthouseweb3 import Lighthouse


class Ipfs:

    def __init__(self):
        self.lh = Lighthouse(token=os.environ['KEY'])

    def load_pdf(self, file, tag="pdf_test", tagged_source_file_path="pdf_data/"):
        """
        this function load ipfs file in lighthouse
        :param file: file name to load
        :param tag: tag for identify file class
        :param tagged_source_file_path: local folder
        :return:
        """
        upload_with_tag = self.lh.upload(source=f'{tagged_source_file_path}{file}', tag=tag)
        metadata = upload_with_tag.get('data')
        print("File Upload with Tag Successful!")
        print(metadata)

        return metadata


if __name__ == "__main__":
    Ipfs().load_pdf(file='test.pdf')

