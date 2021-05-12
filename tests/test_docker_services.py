import subprocess
import mock

import pytest
from plugin import (
    DockerComposeExecutor,
    Services,
    get_docker_services,
    get_cleanup_command,
)


def test_docker_services():
    """Automatic teardown of all services."""

    with mock.patch("subprocess.check_output") as check_output:
        check_output.side_effect = [b"", b"0.0.0.0:32770", b""]
        check_output.returncode = 0

        assert check_output.call_count == 0

        # The fixture is a context-manager.
        with get_docker_services(
            "docker-compose.yml",
            docker_compose_project_name="sfs",
            docker_cleanup=get_cleanup_command(),
        ) as services:
            assert isinstance(services, Services)

            assert check_output.call_count == 1

            # Can request port for services.
            port = services.port_for("synthetic-file-system", 123)
            assert port == 32770

            assert check_output.call_count == 2

            # 2nd request for same service should hit the cache.
            port = services.port_for("synthetic-file-system", 123)
            assert port == 32770

            assert check_output.call_count == 2

        assert check_output.call_count == 3

    # Both should have been called.
    assert check_output.call_args_list == [
        mock.call(
            'docker-compose -f "docker-compose.yml" -p "sfs" up --build -d',
            stderr=subprocess.STDOUT,
            shell=True,
        ),
        mock.call(
            'docker-compose -f "docker-compose.yml" -p "sfs" port synthetic-file-system 123',
            stderr=subprocess.STDOUT,
            shell=True,
        ),
        mock.call(
            'docker-compose -f "docker-compose.yml" -p "sfs" down -v',
            stderr=subprocess.STDOUT,
            shell=True,
        ),
    ]
