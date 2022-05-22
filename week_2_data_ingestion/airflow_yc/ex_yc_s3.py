import boto3


session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")

# Creating a new bucket
s3.create_bucket(Bucket="afs-bucket-13")

# Uploading objects into a bucket

## From a string
s3.put_object(Bucket="afs-bucket-13", Key="object_name", Body="TEST", StorageClass="COLD")

## From a file
s3.upload_file("ex_yc_s3.py", "afs-bucket-13", "py_script.py")
s3.upload_file("ex_yc_s3.py", "afs-bucket-13", "script/py_script.py")

# Getting a list of objects in a bucket
for key in s3.list_objects(Bucket="afs-bucket-13")["Contents"]:
    print(key["Key"])

# Deleting multiple objects
forDeletion = [{"Key": "object_name"}, {"Key": "script/py_script.py"}]
response = s3.delete_objects(Bucket="afs-bucket-13", Delete={"Objects": forDeletion})

# Retrieving an object
get_object_response = s3.get_object(Bucket="afs-bucket-13", Key="py_script.py")
print(get_object_response["Body"].read())
