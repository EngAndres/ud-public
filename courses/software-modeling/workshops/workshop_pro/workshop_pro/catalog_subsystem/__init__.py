"""Exposes classes for the Catalog sub-system."""

from .catalog import CatalogConcrete as Catalog
from .decorator import TimePerformanceDecorator as TimeDecorator
# change for linux or windows depending of the OS you are working on
from .decorator import MemoryPerformanceDecoratorWindows as MemoryDecorator
