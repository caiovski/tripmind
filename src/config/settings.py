import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Carrega o arquivo .env a partir do caminho absoluto da raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH, override=True)
else:
    load_dotenv()


def _clean_env_val(val: Optional[str], default: str = "") -> str:
    """Higieniza valores de variáveis de ambiente removendo aspas, espaços e quebras de linha."""
    if not val:
        return default
    cleaned = str(val).strip().strip('"').strip("'").strip()
    return cleaned if cleaned else default


@dataclass(frozen=True)
class Settings:
    """Configurações centrais do sistema com sanitização robusta de variáveis."""

    # Provedor e Modelos
    model_provider: str = _clean_env_val(os.getenv("MODEL_PROVIDER"), "gemini").lower()
    gemini_model_id: str = _clean_env_val(os.getenv("GEMINI_MODEL_ID"), "gemini-3.6-flash")
    groq_model_id: str = _clean_env_val(os.getenv("GROQ_MODEL_ID"), "openai/gpt-oss-120b")

    # Chaves de API
    gemini_api_key: str = _clean_env_val(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    groq_api_key: str = _clean_env_val(os.getenv("GROQ_API_KEY"))
    tavily_api_key: str = _clean_env_val(os.getenv("TAVILY_API_KEY"))

    # Parâmetros de execução
    debug_mode: bool = _clean_env_val(os.getenv("DEBUG_MODE"), "false").lower() == "true"
    request_timeout: int = int(_clean_env_val(os.getenv("REQUEST_TIMEOUT"), "10"))

    def __post_init__(self):
        # Sincroniza GOOGLE_API_KEY no os.environ para compatibilidade nativa com o SDK do Google e Agno
        if self.gemini_api_key:
            os.environ["GOOGLE_API_KEY"] = self.gemini_api_key
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key
        if self.groq_api_key:
            os.environ["GROQ_API_KEY"] = self.groq_api_key
        if self.tavily_api_key:
            os.environ["TAVILY_API_KEY"] = self.tavily_api_key

    @property
    def has_gemini(self) -> bool:
        """Verifica se a chave Gemini está configurada."""
        return bool(self.gemini_api_key)

    @property
    def has_groq(self) -> bool:
        """Verifica se a chave Groq está configurada."""
        return bool(self.groq_api_key)

    @property
    def has_tavily(self) -> bool:
        """Verifica se a chave Tavily está configurada."""
        return bool(self.tavily_api_key)


def get_settings() -> Settings:
    """Retorna uma instância das configurações da aplicação."""
    return Settings()
