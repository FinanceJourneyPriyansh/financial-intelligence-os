"""
Financial Intelligence OS
Generator Platform

Purpose
-------
The Generator Platform provides reusable generators
that create project components from the Financial
Intelligence OS blueprint and templates.

Available Generators
--------------------
- Folder Generator
- YAML Generator
- README Generator
- Engine Generator
- Domain Generator
- Product Generator
- Interface Generator
- Project Generator

This package is the foundation of the FIOS
code generation system.
"""

from .base_generator import BaseGenerator
from .folder_generator import FolderGenerator
from .yaml_generator import YAMLGenerator
from .readme_generator import ReadmeGenerator
from .engine_generator import EngineGenerator
from .domain_generator import DomainGenerator
from .product_generator import ProductGenerator
from .interface_generator import InterfaceGenerator
from .project_generator import ProjectGenerator
from .generator_manager import GeneratorManager

__all__ = [
    "BaseGenerator",
    "FolderGenerator",
    "YAMLGenerator",
    "ReadmeGenerator",
    "EngineGenerator",
    "DomainGenerator",
    "ProductGenerator",
    "InterfaceGenerator",
    "ProjectGenerator",
    "GeneratorManager",
]