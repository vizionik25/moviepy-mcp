from videoEditor_mcp.schemas import VideoRequest

def test_video_request_schema():
    data = {"text": "test", "duration": 5.0}
    request = VideoRequest(**data)
    assert request.text == "test"
    assert request.duration == 5.0

def test_video_request_defaults():
    data = {"text": "test"}
    request = VideoRequest(**data)
    assert request.text == "test"
    assert request.duration == 3.0
