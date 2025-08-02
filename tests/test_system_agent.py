import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from system_agent import SystemAgent

@pytest.mark.asyncio
@patch("os.system")
async def test_shutdown_windows(mock_os_system):
    agent = SystemAgent()
    agent._post_message = AsyncMock()
    agent._config = MagicMock()
    agent._config.shutdown_interval.total_seconds.return_value = 0

    with patch("os.name", "nt"):
        await agent.shutdown()

    agent._post_message.assert_awaited_with('Shutting down..')
    mock_os_system.assert_called_once_with('shutdown /s /t 1')

@pytest.mark.asyncio
@patch("os.system")
async def test_shutdown_unix(mock_os_system):
    agent = SystemAgent()
    agent._post_message = AsyncMock()
    agent._config = MagicMock()
    agent._config.shutdown_interval.total_seconds.return_value = 0

    with patch("os.name", "posix"):
        await agent.shutdown()

    agent._post_message.assert_awaited_with('Shutting down..')
    mock_os_system.assert_called_once_with('sudo shutdown now')