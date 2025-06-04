#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Cisco Systems
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
name: nxos_dme
short_description: Use NX-OS DME API to run commands on Cisco NX-OS devices
description:
  - This httpapi plugin provides DME API capabilities for Cisco NX-OS devices
  - Supports authentication, session management, and RESTful operations
  - Maintains compatibility with cisco.nxos collection structure
version_added: "1.0.0"
author:
  - Ansible Networking Team
options:
  become:
    type: boolean
    description: Enable privilege escalation
    default: false
    vars:
      - name: ansible_become
  become_method:
    description: Privilege escalation method
    default: enable
    vars:
      - name: ansible_become_method
"""

import json
import time
from ansible.module_utils.basic import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.plugins.httpapi import HttpApiBase
from ansible.utils.display import Display

display = Display()


class DmeApi(HttpApiBase):
    """NX-OS DME HttpApi plugin"""

    def __init__(self, connection):
        super(DmeApi, self).__init__(connection)
        self._auth_token = None
        self._device_info = {}
        # self.plugin_type = "httpapi"

    def login(self, username, password):
        """Login to NX-OS device using DME API"""
        if username and password:
            auth_data = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}

            login_path = "/api/aaaLogin.json"
            try:
                response = self.send_request(method="POST", path=login_path, data=auth_data)

                # Parse authentication response
                if isinstance(response, str):
                    result = json.loads(response)
                else:
                    result = response

                # Extract token from response
                if "imdata" in result and result["imdata"]:
                    token_data = result["imdata"][0]
                    if "aaaLogin" in token_data:
                        self._auth_token = token_data["aaaLogin"]["attributes"]["token"]
                        display.vvv(
                            f"DME authentication successful",
                            host=self.connection.get_option("host"),
                        )
                        return

                # Check for error messages
                if "error" in result:
                    error_msg = result["error"]["text"]
                    raise ConnectionError(f"Authentication failed: {error_msg}")
                else:
                    raise ConnectionError("Authentication failed: Invalid response format")

            except ConnectionError:
                raise
            except Exception as e:
                raise ConnectionError(f"Authentication failed: {to_text(e)}")
        else:
            raise ConnectionError("Username and password are required for authentication")

    def logout(self):
        """Logout from NX-OS device"""
        if self._auth_token:
            logout_path = "/api/aaaLogout.json"
            try:
                # Set authentication header for logout
                self.connection.set_option("headers", {"Cookie": f"APIC-cookie={self._auth_token}"})
                self.send_request(method="POST", path=logout_path)
                display.vvv("DME logout successful", host=self.connection.get_option("host"))
            except Exception as e:
                display.vvv(f"Logout failed: {to_text(e)}", host=self.connection.get_option("host"))
            finally:
                self._auth_token = None

    def send_request(self, method="GET", path="/", data=None, headers=None, **kwargs):
        """Send request to DME API"""
        # Prepare headers
        if headers is None:
            headers = {}

        # Add authentication if available
        if self._auth_token and "Cookie" not in headers:
            headers["Cookie"] = f"APIC-cookie={self._auth_token}"

        headers.setdefault("Content-Type", "application/json")
        headers.setdefault("Accept", "application/json")

        # Prepare data
        if data is not None and not isinstance(data, str):
            data = json.dumps(data)

        try:
            response = self.connection.send(
                path=path, data=data, method=method.upper(), headers=headers, **kwargs
            )

            # Handle token expiration
            if hasattr(response, "status") and response.status in [401, 403]:
                display.vvv(
                    "Token expired, attempting to refresh", host=self.connection.get_option("host")
                )
                self._refresh_token()

                # Retry with new token
                if self._auth_token:
                    headers["Cookie"] = f"APIC-cookie={self._auth_token}"
                    response = self.connection.send(
                        path=path, data=data, method=method.upper(), headers=headers, **kwargs
                    )

            return response

        except Exception as e:
            raise ConnectionError(f"Request failed: {to_text(e)}")

    def _refresh_token(self):
        """Refresh authentication token"""
        if not self._auth_token:
            return

        refresh_path = "/api/aaaRefresh.json"
        try:
            headers = {"Cookie": f"APIC-cookie={self._auth_token}"}
            response = self.connection.send(path=refresh_path, method="POST", headers=headers)

            # Parse refresh response
            if isinstance(response, str):
                result = json.loads(response)
            else:
                result = response

            if "imdata" in result and result["imdata"]:
                token_data = result["imdata"][0]
                if "aaaRefresh" in token_data:
                    self._auth_token = token_data["aaaRefresh"]["attributes"]["token"]
                    display.vvv(
                        "Token refreshed successfully", host=self.connection.get_option("host")
                    )
                    return

        except Exception as e:
            display.vvv(
                f"Token refresh failed: {to_text(e)}", host=self.connection.get_option("host")
            )

        # If refresh fails, clear token to force re-authentication
        self._auth_token = None

    def get_device_info(self):
        """Get device information via DME API"""
        if not self._device_info:
            try:
                # Query system information
                response = self.send_request(method="GET", path="/api/node/class/topSystem.json")

                if isinstance(response, str):
                    result = json.loads(response)
                else:
                    result = response

                if "imdata" in result and result["imdata"]:
                    sys_info = result["imdata"][0]["topSystem"]["attributes"]
                    self._device_info = {
                        "network_os": "nxos",
                        "network_os_version": sys_info.get("version", "unknown"),
                        "network_os_model": sys_info.get("model", "unknown"),
                        "network_os_hostname": sys_info.get("name", "unknown"),
                        "network_os_image": sys_info.get("systemUpTime", "unknown"),
                    }

            except Exception as e:
                display.vvv(
                    f"Failed to get device info: {to_text(e)}",
                    host=self.connection.get_option("host"),
                )
                self._device_info = {
                    "network_os": "nxos",
                    "network_os_version": "unknown",
                    "network_os_model": "unknown",
                    "network_os_hostname": "unknown",
                }

        return self._device_info

    def get_device_operations(self):
        """Return supported device operations"""
        return {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": False,
            "supports_configure_session": False,
            "supports_multiline_delimiter": False,
            "supports_diff_match": False,
            "supports_diff_ignore_lines": False,
            "supports_generate_diff": False,
            "supports_replace": False,
        }

    def get_capabilities(self):
        """Return httpapi capabilities"""
        result = {}
        result["rpc"] = self.get_base_rpc()
        result["device_info"] = self.get_device_info()
        result["device_operations"] = self.get_device_operations()
        result.update(
            {
                "network_api": "dme",
                "has_message_delimiter": False,
                "supports_async": False,
            }
        )
        return json.dumps(result)

    def get_base_rpc(self):
        """Return base RPC methods"""
        return [
            "get_config",
            "edit_config",
            "get",
            "get_capabilities",
            "commit",
            "discard_changes",
            "get_diff",
        ]

    # RPC method implementations
    def get_config(self, source="running", format="json", filter=None):
        """Get configuration via DME API"""
        if source not in ["running", "startup"]:
            raise ConnectionError(f"Unsupported config source: {source}")

        # Map to appropriate DME endpoint
        if source == "running":
            path = "/api/node/mo/sys.json?query-target=subtree&target-subtree-class=*"
        else:
            path = "/api/node/mo/sys/startup.json?query-target=subtree&target-subtree-class=*"

        if filter:
            path += f"&rsp-subtree-filter={filter}"

        return self.send_request(method="GET", path=path)

    def edit_config(self, config, format="json", target="running"):
        """Edit configuration via DME API"""
        if target != "running":
            raise ConnectionError(f"Unsupported config target: {target}")

        # Convert config to DME format if needed
        if isinstance(config, str):
            try:
                config_data = json.loads(config)
            except json.JSONDecodeError:
                raise ConnectionError("Invalid JSON configuration")
        else:
            config_data = config

        # Post configuration to DME
        return self.send_request(method="POST", path="/api/node/mo/.json", data=config_data)

    def get(self, path, **kwargs):
        """Generic GET operation"""
        return self.send_request(method="GET", path=path, **kwargs)

    def post(self, path, data=None, **kwargs):
        """Generic POST operation"""
        return self.send_request(method="POST", path=path, data=data, **kwargs)

    def put(self, path, data=None, **kwargs):
        """Generic PUT operation"""
        return self.send_request(method="PUT", path=path, data=data, **kwargs)

    def delete(self, path, **kwargs):
        """Generic DELETE operation"""
        return self.send_request(method="DELETE", path=path, **kwargs)

    def commit(self, comment=None):
        """Commit changes - NX-OS commits automatically via DME"""
        return {"status": "success", "message": "Configuration committed automatically"}

    def discard_changes(self):
        """Discard changes - not applicable for DME API"""
        return {"status": "success", "message": "No pending changes to discard"}

    def get_diff(self, candidate=None, running=None, **kwargs):
        """Get configuration diff - basic implementation"""
        return {"diff": "Diff not supported via DME API"}
