from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from datetime import datetime, timezone

# Create your views here.

@api_view(http_method_names=["get"])
def gender_list(request):
    name = request.GET.get("name")
    if not name:
        return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "Missing or empty name parameter"})

    if not name.isalpha():
        return Response(
            {"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "message": "'name' must be a string"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    try:
        response = requests.get("https://api.genderize.io/", params={"name": name}, timeout=5)
        data = response.json()
    except requests.exceptions.RequestException:
        return Response({"status": status.HTTP_502_BAD_GATEWAY, "message": "Upstream or server failure"})
    except ValueError:
        return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Internal Server Error"})

    response = requests.get("https://api.genderize.io/", params={"name": name})
    data = response.json()

    data["sample_size"] = data.pop("count")
    data["is_confident"] = data["probability"] >= 0.7 and data["sample_size"] >= 100
    data["processed_at"] = datetime.now(timezone.utc).isoformat()

    if data["gender"] not in ["male", "female"] or data["sample_size"] == 0:
            return Response({"status": "null", "message": "No prediction available for the provided name"})
    return Response(data)
