import boto3
import time

session = boto3.Session(profile_name='HASANAccess-854407906105')

s3_client = boto3.client('s3')
bucket_name = 'hasan-assignment'
file_name = 'submission.csv'
object_name = 'taehyeon/submission.csv'

def upload_to_s3(bucket, object_name, file_name):
    with open(file_name, 'rb') as file:
        s3_client.upload_fileobj(file, bucket, object_name)

def download_from_s3(bucket, object_name, file_name):
    with open(file_name, 'wb') as file:
        s3_client.download_fileobj(bucket, object_name, file)

def main():
    num_iterations = 100
    write_times = []
    read_times = []

    # S3에 업로드 및 다운로드 100번 반복
    for _ in range(num_iterations):
        start = time.time()
        try:
            upload_to_s3(bucket_name, object_name, file_name)
            end = time.time()
            write_times.append(end - start)
        except Exception as e:
            print(e)


        start = time.time()
        try:
            download_from_s3(bucket_name, object_name, file_name)
            end = time.time()
            read_times.append(end - start)
        except Exception as e:
            print(e)

    avg_write_time = sum(write_times) / num_iterations
    avg_read_time = sum(read_times) / num_iterations

    print(f"Average S3 upload time: {avg_write_time:.5f} seconds")
    print(f"Average S3 download time: {avg_read_time:.5f} seconds")

if __name__ == '__main__':
    main()