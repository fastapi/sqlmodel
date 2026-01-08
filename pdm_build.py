import os
from typing import Any

from pdm.backend.hooks import Context

TIANGOLO_BUILD_PACKAGE = os.getenv("TIANGOLO_BUILD_PACKAGE", "sqlmodel")


def pdm_build_initialize(context: Context) -> None:
    metadata = context.config.metadata
    # Get custom config for the current package, from the env var
    config: dict[str, Any] = context.config.data["tool"]["tiangolo"][
        "_internal-slim-build"
    ]["packages"][TIANGOLO_BUILD_PACKAGE]
    project_config: dict[str, Any] = config["project"]
    # Get main optional dependencies, extras
    optional_dependencies: dict[str, list[str]] = metadata.get(
        "optional-dependencies", {}
    )
    # Get custom optional dependencies name to always include in this (non-slim) package
    include_optional_dependencies: list[str] = config.get(
        "include-optional-dependencies", []
    )
    # Override main [project] configs with custom configs for this package
    for key, value in project_config.items():
        metadata[key] = value
    # Get custom build config for the current package
    build_config: dict[str, Any] = (
        config.get("tool", {}).get("pdm", {}).get("build", {})
    )
    # Override PDM build config with custom build config for this package
    for key, value in build_config.items():
        context.config.build_config[key] = value
    # Get main dependencies
    dependencies: list[str] = metadata.get("dependencies", [])
    # Add optional dependencies to the default dependencies for this (non-slim) package
    for include_optional in include_optional_dependencies:
        optional_dependencies_group = optional_dependencies.get(include_optional, [])
        dependencies.extend(optional_dependencies_group)
