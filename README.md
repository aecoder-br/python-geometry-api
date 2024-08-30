# Python Geometry API

This project provides a simple API built with FastAPI that takes a list of 2D points and generates a concave hull (alpha shape) based on a given alpha value. The API returns the coordinates of the shape's edges, which is useful for creating boundary shapes around scattered points.

## Features

- **2D Concave Hull Calculation**: Uses the [`alphashape`](https://pypi.org/project/alphashape/) library to compute the concave hull (alpha shape) of a given set of points.
- **FastAPI**: Provides a fast and interactive API with automatic documentation via Swagger UI.
- **Simple Token Verification**: Includes a verification token for secure ~~at least a little bit the~~ access to the API.
- **Python 3.12**: Built and deployed using Python 3.12.

## Endpoints

- **POST /2d_concave_hull/**: Receives a JSON payload containing a list of 2D points and a verification token, and returns the alpha shape edges.

### Request

```curl
POST /2d_concave_hull/?token=your_verification_token&alpha=0
{
  "points": [
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0]
  ]
}
```

### Response

```json
{
  "edges": [
    [[0.0, 0.0], [1.0, 0.0]],
    [[1.0, 0.0], [1.0, 1.0]],
    [[1.0, 1.0], [0.0, 1.0]],
    [[0.0, 1.0], [0.0, 0.0]]
  ]
}
```

Example of a request using python (inside Dynamo):

```python
import urllib2
import json
def get_concave_hull(points2D, token, alpha = 0.0):
	base_url = "http://127.0.0.1:8000/" # Change the base URL when you deploy to production
	endpoint = "2d_concave_hull/"
	# Encode token to avoid errors
	my_token = urllib2.quote(token)
	parameters = "?token=" + my_token + "&alpha=" + str(alpha).replace(",", ".")
	url = base_url + endpoint + parameters
	headers = {'Content-type': 'application/json', "accept": "application/json"}
	data = json.dumps(dict(points=points2D))
	request = urllib2.Request(url, data, headers)
	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as e:
		raise Exception("The request was not successful.\n" + e.read())
	return response.read()
```

## Local Development

### Prerequisites

- Python 3.12
- [Virtualenv](https://pypi.org/project/virtualenv/)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/aecoder-br/python-geometry-api.git
   cd python-geometry-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   Alternatively, on Windows, you can use:
   ```bash
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of the project and add your verification token:
   ```
   VERIFICATION_TOKEN=your_verification_token
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

6. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
