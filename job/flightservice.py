from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkContext
from flask import Flask, request
from pyspark.ml import Pipeline, PipelineModel
from azure.storage.blob import BlockBlobService, PublicAccess
import os 
import pickle
import ast
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import Row
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import NaiveBayesModel
from pyspark.ml.feature import HashingTF,StopWordsRemover,IDF,Tokenizer
from pyspark.ml.feature import StringIndexer

app = Flask(__name__)
sc = SparkContext('local')
spark = SparkSession.builder.master("local").getOrCreate()

@app.route('/predict', methods=['POST'])  #can set first param to '/'
def predict():
    blob_account_name = os.environ.get('ds_blob_account')
    blob_account_key = os.environ.get('ds_blob_key')
    mycontainer = os.environ.get('ds_container')
    filename = os.environ.get('ds_model_filename')
    dirname = os.getcwd()
    dirname1 = "model/data"
    dirname2 = "model/metadata"
    filename1 = "part-00000-a1f9ca3a-3bec-4451-849f-546af11b14ab.snappy.parquet"
    filename2 = "part-00000"
    blobfilename = "HdiSamples/HdiSamples/sentimentfinal/stages/3_NaiveBayes_471fad31e436e6de3ade"

    blob_service = BlockBlobService(account_name=blob_account_name, account_key=blob_account_key, endpoint_suffix='core.usgovcloudapi.net')
    generator = blob_service.list_blobs(mycontainer)
    dirname = os.getcwd()
    if not os.path.exists(dirname + "/" + dirname1):
        os.makedirs(dirname + "/" + dirname1)
    if not os.path.exists(dirname + "/" + dirname2):
        os.makedirs(dirname + "/" + dirname2)

    blob_service.get_blob_to_path(mycontainer, blobfilename + "/data/" + filename1,
                                  dirname + "/" + dirname1 + "/" + filename1)
    blob_service.get_blob_to_path(mycontainer, blobfilename + "/metadata/" + filename2,
                                  dirname + "/" + dirname2 + "/" + filename2)
    localmodel = os.path.join(dirname, "model")
    model = NaiveBayesModel.load(localmodel)
    input = request.get_data().decode("utf-8")
    inputformat = ast.literal_eval(input)
    testrdd = sc.parallelize(inputformat)
    temp = testrdd.map(lambda x: Row(text=x))
    tempdf = spark.createDataFrame(temp)

    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    stopremover = StopWordsRemover().setInputCol("words").setOutputCol("removed").setCaseSensitive(False)
    newhashingTF = HashingTF(inputCol="removed", outputCol="features", numFeatures=2000)
    nb_pipeline = Pipeline(stages=[tokenizer, stopremover, newhashingTF])

    temp1df = nb_pipeline.fit(tempdf).transform(tempdf)

    testpred = model.transform(temp1df)
    return str(testpred.take(1))

print("hi")
if __name__ == '__main__':
    print("works1")
    app.run(host='0.0.0.0', port=8080)    #note set to 8080!
    print("works")

