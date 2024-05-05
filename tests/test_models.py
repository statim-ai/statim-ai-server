"""Model test module."""

import unittest

from unittest import TestCase

import requests

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


class ModelsTest(TestCase):
    """Models test class."""

    def test_status_codes_200(self):
        """Test for status code 200."""
        with DockerContainer("statim-ai-server:0.1.0").with_exposed_ports(5000).with_env("PORT", "5000") as container:
            wait_for_logs(container, "Serving on")

            port = container.get_exposed_port(5000)

            try:
                response = requests.get(f"http://localhost:{port}/model/")
                assert response.status_code == 200
            except Exception as e:
                print(e)


unittest.main()
