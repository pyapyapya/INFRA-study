import time
import os
import shutil

def write_file(src_path, dest_path):
    shutil.copy(src_path, dest_path)

def read_file(dest_path):
    with open(dest_path, 'r') as file:
        return file.read()

def main():
    src_path = './submission.csv'
    dest_path = '/mnt/efs/submission.csv'
    num_iterations = 100
    write_times = []
    read_times = []

    # 파일 쓰기 및 읽기 100번 반복
    for _ in range(num_iterations):
        start = time.time()
        write_file(src_path, dest_path)
        end = time.time()
        write_times.append(end - start)

        start = time.time()
        read_file(dest_path)
        end = time.time()
        read_times.append(end - start)

    # 평균 시간 계산
    avg_write_time = sum(write_times) / num_iterations
    avg_read_time = sum(read_times) / num_iterations

    print(f"Average write time: {avg_write_time:.5f} seconds")
    print(f"Average read time: {avg_read_time:.5f} seconds")

if __name__ == '__main__':
    main()