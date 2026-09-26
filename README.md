# Demografix — Gender Classification API

A simple Django REST Framework API that predicts the likely gender of a person based on their first name, using the [Genderize.io](https://genderize.io/) API.

## Live Demo

```
https://demografix-c63625879fc2.herokuapp.com/api/classify/?name=sam
```

## Endpoint

### `GET /api/classify/`

Returns gender prediction data for a given name.

**Query Parameters**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|---------------------------------------|
| `name`    | string | Yes      | The first name to classify (letters only) |

**Example Request**

```
GET /api/classify/?name=sam
```

**Example Response — `200 OK`**

```json
{
    "name": "sam",
    "gender": "male",
    "probability": 0.9,
    "sample_size": 647976,
    "is_confident": true,
    "processed_at": "2026-09-26T01:43:56.913721+00:00"
}
```

**Response Fields**

| Field          | Type    | Description                                                        |
|----------------|---------|----------------------------------------------------------------------|
| `name`         | string  | The name that was classified                                       |
| `gender`       | string  | Predicted gender (`male`, `female`, or `null` if unknown)          |
| `probability`  | float   | Confidence score from Genderize (0–1)                              |
| `sample_size`  | integer | Number of data points Genderize used for the prediction            |
| `is_confident` | boolean | `true` only if `probability >= 0.7` **and** `sample_size >= 100`   |
| `processed_at` | string  | UTC timestamp (ISO 8601) of when the request was processed         |

## Error Responses

| Status | Condition                              |
|--------|------------------------------------------|
| `400`  | Missing or empty `name` parameter       |
| `422`  | `name` contains non-alphabetic characters |
| `502`  | Upstream (Genderize) service unavailable or returned an error |
| `500`  | Upstream returned an invalid/non-JSON response |

**Example Error Response**

```json
{
    "status": 400,
    "message": "Missing or empty name parameter"
}
```

## Tech Stack

- Python
- Django
- Django REST Framework
- `requests` (for calling the Genderize API)
- `django-cors-headers` (CORS enabled for all origins)
- Gunicorn (production WSGI server)
- Deployed on Heroku

## Local Setup

Clone the repo:

```bash
git clone https://github.com/musbahughassan/stage0task.git
cd stage0task
```

Install dependencies with Pipenv:

```bash
pipenv install
pipenv shell
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/api/classify/?name=sam
```

## Environment Variables

| Variable     | Description                          |
|--------------|----------------------------------------|
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG`      | Set to `True` for local dev, `False` in production |

## Deployment (Heroku)

```bash
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
```

## License

This project was built as part of the HNG Backend Internship, Stage 0 task.
