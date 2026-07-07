from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ContentBrief:
    angle: str
    audience: str
    product: str
    cta: str
    channels: List[str]
    proof_point: Optional[str] = None
    link: Optional[str] = None
    customer_quote: Optional[str] = None
