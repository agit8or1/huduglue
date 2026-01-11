"""
Import services for IT Glue, Hudu, and MagicPlan
"""
from .base import BaseImportService
from .itglue import ITGlueImportService
from .hudu import HuduImportService
from .magicplan import MagicPlanImportService


def get_import_service(import_job):
    """
    Get the appropriate import service for an import job.

    Args:
        import_job: ImportJob instance

    Returns:
        Service instance (ITGlueImportService, HuduImportService, or MagicPlanImportService)

    Raises:
        ValueError: If source_type is unknown
    """
    if import_job.source_type == 'itglue':
        return ITGlueImportService(import_job)
    elif import_job.source_type == 'hudu':
        return HuduImportService(import_job)
    elif import_job.source_type == 'magicplan':
        return MagicPlanImportService(import_job)
    else:
        raise ValueError(f"Unknown source type: {import_job.source_type}")


__all__ = [
    'BaseImportService',
    'ITGlueImportService',
    'HuduImportService',
    'MagicPlanImportService',
    'get_import_service',
]
