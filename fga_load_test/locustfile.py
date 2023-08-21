import subprocess

from fga_load_test import read_http, write_http, read_grpc


write_file_http = write_http.__file__
read_file_http = read_http.__file__
read_file_rpc = read_grpc.__file__


def write_http():
    subprocess.run(f"locust -f {write_file_http} --html report.html", shell=True)


def read_http():
    subprocess.run(f"locust -f {read_file_http} --html report.html", shell=True)


def read_rpc():
    subprocess.run(f"locust -f {read_file_rpc} --html report.html", shell=True)
