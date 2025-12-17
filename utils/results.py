# utils/results.py

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class BenchmarkResult:
    """
    Unified result schema for all benchmarks.
    Wraps raw runner output with structured fields and parsed metrics.
    """
    tool: str
    cmd: str
    return_code: int
    stdout: str
    stderr: str
    params: Dict[str, Any]
    sysinfo: Dict[str, Any]
    metrics: Dict[str, Any] = field(default_factory=dict)
    scenario: str = "single-node"
    node: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
