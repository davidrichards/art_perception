from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class ColorSwatch(BaseModel):
    rgb: Tuple[int, int, int]
    hex: str
    proportion: float = Field(ge=0.0, le=1.0, default=1.0 / 6)
    label: Optional[str] = None


class Strategy(str, Enum):
    KMEANS = "kmeans"
    HISTOGRAM_PEAKS = "histogram_peaks"
    COLORFULLNESS = "colorfulness"
