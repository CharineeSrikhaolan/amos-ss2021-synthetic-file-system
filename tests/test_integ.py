import pytest
import os
import subprocess
import unittest
import time

class TestIntegratedTool(unittest.TestCase):

    def setUp(self):
        print("Setting up docker...")
        # Add docker stop $(docker ps -aq), docker rm $(docker ps -aq)
        if not os.path.isfile('docker-compose.yml'):
                self.assertRaises(FileNotFoundError)
        process = subprocess.Popen(["docker-compose", "up"])
        time.sleep(30)
        print(process.pid)
        

    def test_container_files(self):
        process_run = subprocess.run(["docker", "container", "attach", "synthetic-file-system"])
        print("STDOUT: ", process_run.stdout)
        print("STDERR: ", process_run.stderr)
        process_exec_1 = subprocess.run(["docker", "container", "exec", "synthetic-file-system", "./mount.sh"], capture_output=True, shell=True)
        print("STDOUT: ", process_exec_1.stdout)
        print("STDERR: ", process_exec_1.stderr)
        process_exec_2 = subprocess.run(["docker", "container", "exec", "synthetic-file-system", "cd .."], capture_output=True)
        print("STDOUT: ", process_exec_2.stdout)
        print("STDERR: ", process_exec_2.stderr)
        process_exec_3 = subprocess.run(["docker", "container", "exec", "synthetic-file-system", "cd /fuse_mount"], capture_output=True)
        print("STDOUT: ", process_exec_3.stdout)
        print("STDERR: ", process_exec_3.stderr)
        process_exec_4 = subprocess.run(["docker", "container", "exec", "synthetic-file-system", "ls"], capture_output=True)
        print("STDOUT: ", process_exec_4.stdout)
        print("STDERR: ", process_exec_4.stderr)

    #def tearDown(self):
        #print("Turning off docker...")
        #docker_compose_return = subprocess.run(["docker-compose", "down"])
        # self.assertEqual(docker_compose_return, 0)
