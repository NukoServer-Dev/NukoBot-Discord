from dataclasses import dataclass

@dataclass
class MCJavaVersion:
    id: str
    type: str
    url: str
    time: str
    releaseTime: str
    sha1: str
    complianceLevel: int
