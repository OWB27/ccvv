from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "CCVV - AI Resume Analyzer API"
    API_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    ALLOWED_ORIGINS: list[str] = field(default_factory=lambda: ["http://localhost:5173"])


settings = Settings()
