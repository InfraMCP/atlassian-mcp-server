"""Module manager for handling enabled/disabled modules."""

import os
from typing import Dict, List
from mcp.server import Server
from .modules import JiraModule, ConfluenceModule, ServiceDeskModule
from .modules.base import BaseModule


class ModuleManager:
    """Manages which modules are enabled and registers their tools/resources."""

    def __init__(self, client):
        """Initialize the module manager."""
        self.client = client
        self.available_modules = {
            "jira": JiraModule,
            "confluence": ConfluenceModule,
            "service_desk": ServiceDeskModule
        }
        self.enabled_modules: Dict[str, BaseModule] = {}
        self._load_enabled_modules()

    def _load_enabled_modules(self) -> None:
        """Load enabled modules based on environment variable."""
        # Get enabled modules from environment variable
        modules_env = os.getenv("ATLASSIAN_MODULES", "").strip()

        if not modules_env:
            # Default: enable all modules
            enabled_names = set(self.available_modules.keys())
        else:
            # Parse comma-separated list
            enabled_names = {
                name.strip().lower()
                for name in modules_env.split(",")
                if name.strip()
            }

        # Validate module names
        invalid_modules = enabled_names - set(self.available_modules.keys())
        if invalid_modules:
            raise ValueError(
                f"Invalid module names: {invalid_modules}. "
                f"Available modules: {list(self.available_modules.keys())}"
            )

        # Initialize enabled modules
        for name in enabled_names:
            module_class = self.available_modules[name]
            self.enabled_modules[name] = module_class(self.client)

    def get_enabled_modules(self) -> Dict[str, BaseModule]:
        """Get all enabled modules."""
        return self.enabled_modules

    def is_module_enabled(self, name: str) -> bool:
        """Check if a specific module is enabled."""
        return name in self.enabled_modules

    def get_required_scopes(self) -> List[str]:
        """Get all required OAuth scopes for enabled modules."""
        scopes = set()
        for module in self.enabled_modules.values():
            scopes.update(module.required_scopes)
        return list(scopes)

    def register_all(self, server: Server) -> None:
        """Register tools and resources for all enabled modules."""
        for name, module in self.enabled_modules.items():
            if module.is_available():
                print(f"Registering {name} module...")
                module.register_tools(server)
                module.register_resources(server)
            else:
                print(f"Skipping {name} module (not available)")

    def get_status(self) -> Dict[str, Dict[str, any]]:
        """Get status of all modules."""
        status = {}
        for name, module_class in self.available_modules.items():
            is_enabled = name in self.enabled_modules
            is_available = False
            if is_enabled:
                is_available = self.enabled_modules[name].is_available()

            status[name] = {
                "enabled": is_enabled,
                "available": is_available,
                "required_scopes": module_class(None).required_scopes
            }
        return status
