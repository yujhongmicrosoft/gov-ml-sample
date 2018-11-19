from azure.storage.blob import BlockBlobService, PublicAccess
import os
import pickle
import ast

blob_account = "mltesting"
blob_key = "bimLRHGBR84SUHLQupWAoYZ+EyPQZxllWZXHT+30sR/2Dwx0Lmuqwq4OvKTt+pxh4jPS9j/oFX4Y6LuxJlMS4g=="
mycontainer = "ml-testing-2018-01-02t14-56-28-539z"
dirname1 = "model/data"
dirname2 = "model/metadata"
filename1 = "part-00000-a1f9ca3a-3bec-4451-849f-546af11b14ab.snappy.parquet"
filename2 = "part-00000"
blobfilename = "HdiSamples/HdiSamples/sentimentfinal/stages/3_NaiveBayes_471fad31e436e6de3ade"
if __name__ == '__main__':
    print("works1")
    blob_service = BlockBlobService(account_name=blob_account, account_key=blob_key, endpoint_suffix='core.usgovcloudapi.net')
    generator = blob_service.list_blobs(mycontainer)
    dirname = os.getcwd()
    os.makedirs(dirname + "/" + dirname1)
    os.makedirs(dirname + "/" + dirname2)
    print(filename1)

    #python figure out how to create a file in python not folder
    #for blob in generator:
    #    if filename in blob.name:
    #os.makedirs(dirname + "/" + "model" + "/" + filename)
    blob_service.get_blob_to_path(mycontainer, blobfilename + "/data/" + filename1, dirname + "/" + dirname1 + "/" + filename1)
    blob_service.get_blob_to_path(mycontainer, blobfilename + "/metadata/" + filename2, dirname + "/" + dirname2 + "/" + filename2)
