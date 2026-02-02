# Video Generation Service API Documentation

## 1. Overview

Welcome to the Video Generation Service API! This API allows for powerful, programmatic creation and manipulation of video and audio content using simple HTTP requests. It's built on FastAPI and uses the MoviePy library for all media processing.

**Base URL**: `http://localhost:8000` (for local development)

**API Version**: 1.0.0

**Live Documentation**: For a complete, interactive API specification (Swagger UI), please run the server and visit `http://localhost:8000/docs`.

## 2. Authentication

Currently, the API does not require authentication. All endpoints are open and accessible on the network where the service is deployed.

## 3. Endpoints

The API is organized into four main categories: Video Generation, Video Editing, Audio Processing, and Compositing.

---

### **Video Generation**

#### Generate Video
**Method**: `POST`
**Path**: `/video/generate`
**Description**: Creates a simple video with specified text on a default background.

**Request Body**:
```json
{
  "text": "Hello, World!",
  "duration": 5.0
}
```

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| text | string | Yes | The text content to display in the video. | "Welcome!" |
| duration | float | No | The duration of the video in seconds. | 10.0 |

**Response**:
- **Status Code**: `200 OK`
```json
{
  "status": "success",
  "file_path": "/path/to/your/project/video_... .mp4"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/video/generate" \
-H "Content-Type: application/json" \
-d '{
  "text": "API-Generated Video",
  "duration": 3
}'
```

---

### **Video Editing**

#### Cut Video
**Method**: `POST`
**Path**: `/video-edits/cut`
**Description**: Trims a video to a specified time range.

**Request Body**:
```json
{
  "video_path": "/path/to/input.mp4",
  "start_time": 10.0,
  "end_time": 25.5,
  "output_path": "/path/to/output_cut.mp4"
}
```

**Response**:
- **Status Code**: `200 OK`
```json
{
  "status": "success",
  "output_path": "/path/to/output_cut.mp4"
}
```
*Note: The structure for other video editing endpoints (`/concatenate`, `/resize`, `/speed`, etc.) follows a similar pattern. Please refer to the [Data Models](#4-data-models--schemas) section for the specific request body of each endpoint.*

---

### **Audio Processing**

#### Adjust Volume
**Method**: `POST`
**Path**: `/audio/volume`
**Description**: Adjusts the volume of a video's audio track by a multiplier.

**Request Body**:
```json
{
  "video_path": "/path/to/input.mp4",
  "factor": 0.5,
  "output_path": "/path/to/output_quiet.mp4"
}
```

**Response**:
- **Status Code**: `200 OK`
```json
{
  "status": "success",
  "output_path": "/path/to/output_quiet.mp4"
}
```

#### Extract Audio
**Method**: `POST`
**Path**: `/audio/extract`
**Description**: Extracts the audio from a video file into a separate audio file.

**Request Body**:
```json
{
  "video_path": "/path/to/input.mp4",
  "output_audio_path": "/path/to/output_audio.mp3"
}
```
---

### **Compositing**

#### Overlay Text
**Method**: `POST`
**Path**: `/compositing/text-overlay`
**Description**: Adds a text overlay to a video.

**Request Body**:
```json
{
  "video_path": "/path/to/input.mp4",
  "text": "Important Message",
  "fontsize": 70,
  "color": "yellow",
  "position": "center",
  "start_time": 2.0,
  "duration": 5.0
}
```

#### Composite Videos
**Method**: `POST`
**Path**: `/compositing/composite`
**Description**: Combines multiple videos into a single frame using a 'stack' or 'grid' layout.

**Request Body**:
```json
{
  "video_paths": ["/path/to/vid1.mp4", "/path/to/vid2.mp4"],
  "method": "stack"
}
```

## 4. Data Models / Schemas

These are the Pydantic models used for request validation. Optional fields can be omitted.

```typescript
// General response for most editing operations
interface ResponseModel {
  status: string;
  output_path: string;
  details?: string;
}

// Base request for most operations
interface ClipRequest {
  video_path: string;
  output_path?: string;
}

// /video-edits/cut
interface CutRequest extends ClipRequest {
  start_time: number;
  end_time: number;
}

// /video-edits/concatenate
interface ConcatenateRequest {
  video_paths: string[];
  output_path?: string;
  method: 'compose' | 'chain';
}

// /video-edits/resize
interface ResizeRequest extends ClipRequest {
  width?: number;
  height?: number;
  scale?: number;
}

// /video-edits/speed
interface SpeedRequest extends ClipRequest {
  factor: number;
}

// /compositing/text-overlay
interface TextOverlayRequest extends ClipRequest {
  text: string;
  fontsize?: number;
  color?: string;
  position?: 'center' | 'top' | 'bottom' | [number, number];
  duration?: number;
  start_time?: number;
}

// /compositing/image-overlay
interface ImageOverlayRequest extends ClipRequest {
  image_path: string;
  position?: 'center' | 'top' | 'bottom' | [number, number];
  scale?: number;
  opacity?: number;
  duration?: number;
  start_time?: number;
}

// /audio/volume
interface VolumeRequest extends ClipRequest {
  factor: number;
}

// ... and so on for all other request types.
```

## 5. Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request.

- **`200 OK`**: The request was successful.
- **`404 Not Found`**: The requested resource (e.g., an input `video_path`) could not be found.
- **`422 Unprocessable Entity`**: The request body is malformed or missing required fields. The response body will contain details about the validation error.
- **`500 Internal Server Error`**: An unexpected error occurred on the server, likely during video processing. The response body will contain a `detail` key with information about the error.

**Example Error Response (`422`)**:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        "start_time"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 6. Code Examples

### cURL
```bash
# Resize a video to 50% of its original size
curl -X POST "http://localhost:8000/video-edits/resize" \
-H "Content-Type: application/json" \
-d '{
  "video_path": "my_input_video.mp4",
  "scale": 0.5
}'
```

### Python (`requests`)
```python
import requests

api_url = "http://localhost:8000"

def resize_video(input_path: str, scale: float):
    endpoint = f"{api_url}/video-edits/resize"
    payload = {
        "video_path": input_path,
        "scale": scale
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    result = resize_video("my_input_video.mp4", 0.5)
    if result:
        print("Success!", result)
```

## 7. Rate Limiting, Pagination, & More

The current version of the API does not implement rate limiting, pagination, filtering, or webhooks. These features may be considered for future releases.

## 8. Changelog

-   **v1.0.0** (Current)
    -   Initial release of the Video Generation Service.
    -   Includes endpoints for video generation, editing, audio processing, and compositing.
    -   Includes an MCP server for agent-based interaction.
