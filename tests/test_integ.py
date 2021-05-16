import pytest
import os
import subprocess
import unittest

class TestIntegratedTool(unittest.TestCase):

    def setUp(self):
        docker_compose_return = subprocess.run(["docker-compose", "up"])
        # self.assertEqual(docker_compose_return, 0)
        if docker_compose_return != 0:
            if not os.path.isfile('docker-compose.yml'):
                self.assertRaises(FileNotFoundError)

    def test_container_files:
        subprocess.run(["cd app", "ls"])

    def tearDown(self):
        docker_compose_return = subprocess.run(["docker-compose", "down"])
        # self.assertEqual(docker_compose_return, 0)