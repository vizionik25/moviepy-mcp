import pytest
from unittest.mock import patch, MagicMock
from videoEditor_mcp.mcp_server import parse_args, main, mcp

def test_parse_args_defaults():
    args = parse_args([])
    assert args.transport == "http"
    assert args.host == "0.0.0.0"
    assert args.port == 8080

def test_parse_args_custom():
    args = parse_args(["--transport", "stdio", "--host", "127.0.0.1", "--port", "9000"])
    assert args.transport == "stdio"
    assert args.host == "127.0.0.1"
    assert args.port == 9000

@patch("videoEditor_mcp.mcp_server.mcp.run")
@patch("videoEditor_mcp.mcp_server.parse_args")
def test_main_http(mock_parse, mock_run):
    mock_args = MagicMock()
    mock_args.transport = "http"
    mock_args.host = "0.0.0.0"
    mock_args.port = 8080
    mock_parse.return_value = mock_args
    
    main()
    
    mock_run.assert_called_once_with(transport="http", host="0.0.0.0", port=8080)

@patch("videoEditor_mcp.mcp_server.mcp.run")
@patch("videoEditor_mcp.mcp_server.parse_args")
def test_main_stdio(mock_parse, mock_run):
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_parse.return_value = mock_args
    
    main()
    
    mock_run.assert_called_once_with(transport="stdio")

@patch("videoEditor_mcp.mcp_server.mcp.run")
@patch("videoEditor_mcp.mcp_server.parse_args")
def test_main_sse(mock_parse, mock_run):
    mock_args = MagicMock()
    mock_args.transport = "sse"
    mock_args.host = "1.2.3.4"
    mock_args.port = 1234
    mock_parse.return_value = mock_args
    
    main()
    
    mock_run.assert_called_once_with(transport="sse", host="1.2.3.4", port=1234)
