import os
from lighthouseweb3 import Lighthouse

lh = Lighthouse(token=os.environ['KEY'])

tagged_source_file_path = "pdf_data/"
file = 'test.pdf'
tag = "pdf_test"
upload_with_tag = lh.upload(source=f'{tagged_source_file_path}{file}', tag=tag)
print("File Upload with Tag Successful!")

print(upload_with_tag.get('data'))
