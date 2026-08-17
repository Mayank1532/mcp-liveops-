"""Evidence acquisition package."""

from nexus_shield.acquisition.api_models import (
    ExternalApiResponse,
    ExternalApiStatus,
)
from nexus_shield.acquisition.api_normalization import ExternalApiNormalizer
from nexus_shield.acquisition.external_api import ExternalApiAcquirer
from nexus_shield.acquisition.interface import EvidenceAcquirer
from nexus_shield.acquisition.local_text import LocalTextAcquirer
from nexus_shield.acquisition.models import (
    AcquisitionResult,
    AcquisitionStatus,
)
from nexus_shield.acquisition.normalization import WebSourceNormalizer
from nexus_shield.acquisition.web import WebAcquirer
from nexus_shield.acquisition.web_models import (
    WebAcquisitionResult,
    WebSource,
)

__all__ = [
    "AcquisitionResult",
    "AcquisitionStatus",
    "EvidenceAcquirer",
    "ExternalApiAcquirer",
    "ExternalApiNormalizer",
    "ExternalApiResponse",
    "ExternalApiStatus",
    "LocalTextAcquirer",
    "WebAcquirer",
    "WebAcquisitionResult",
    "WebSource",
    "WebSourceNormalizer",
]
