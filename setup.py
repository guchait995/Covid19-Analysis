import os
import sys
import subprocess

def execute_bash(command):
        subprocess.run(command, shell=True)
 
commands=["requests","numpy","pandas","matplotlib","pmdarima"]

def setup_env():
    for package in commands:
        execute_bash("pip3 install {}".format(package))


if __name__ == "__main__":
    setup_env()