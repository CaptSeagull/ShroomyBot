try:
    from .beta_config import setup_env
except ImportError:
    def setup_env():
        pass
