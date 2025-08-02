from src.config import *
import pytest
from datetime import timedelta
from src.config import Config

def test_config_default(monkeypatch):
    monkeypatch.setenv('APP_URL', 'http://localhost:8188')
    config = Config.default()
    assert isinstance(config, Config)
    assert config.gpu_index == 0
    assert config.span_threshold == timedelta(minutes=10)
    assert config.heartbeat == timedelta(minutes=30)
    assert config.interval == timedelta(seconds=10)
    assert config.shutdown_interval == timedelta(seconds=30)
    assert config.app_url == 'http://localhost:8188'

def test_config_set_values():
    config = Config.default()
    config.gpu_index = 1
    config.span_threshold = timedelta(minutes=5)
    config.heartbeat = timedelta(minutes=15)
    config.interval = timedelta(seconds=5)
    config.shutdown_interval = timedelta(seconds=20)
    config.app_url = 'http://example.com'

    assert config.gpu_index == 1
    assert config.span_threshold == timedelta(minutes=5)
    assert config.heartbeat == timedelta(minutes=15)
    assert config.interval == timedelta(seconds=5)
    assert config.shutdown_interval == timedelta(seconds=20)
    assert config.app_url == 'http://example.com'

def test_config_missing_app_url_raises(monkeypatch):
    monkeypatch.setenv('APP_URL', '')
    with pytest.raises(ValueError) as ex:
        config = Config.default()
        config.verify()
    assert "app_url is not set" in str(ex.value)

def test_config_verify(monkeypatch):
    monkeypatch.setenv('APP_URL', 'http://localhost:8188')
    config = Config.default()
    config.verify()
