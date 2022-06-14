import csv
import json

from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.views import APIView

from sky.serializers import PlanetSerializer, AsteroidSerializer
from tools.core import Planet, Asteroid
from requests_oauthlib import OAuth2Session

from tools.database import Database
from tools.oauth import oauth_required


class AsteroidsView(APIView):
    @swagger_auto_schema(responses={200: AsteroidSerializer})
    @oauth_required
    def get(self, request: Request) -> HttpResponse:
        db = Database.get()
        venus = next((planet for planet in db.planets if planet.name == "Venus"))
        if not venus:
            raise APIException("Venus not found, cannot proceed")

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="asteroids.csv"'},
        )

        csv_writer = csv.DictWriter(response, fieldnames=Asteroid.csv_fields())
        for asteroid in db.asteroids:
            if asteroid.mass and asteroid.mass > venus.mass:
                csv_writer.writerow(asteroid.csv_row())

        return response


class PlanetsView(APIView):
    @swagger_auto_schema(responses={200: PlanetSerializer})
    @oauth_required
    def get(self, request: Request) -> HttpResponse:
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="planets.csv"'},
        )

        csv_writer = csv.DictWriter(response, fieldnames=Planet.csv_fields())
        csv_writer.writeheader()
        for planet in Database.get().planets:
            csv_writer.writerow(planet.csv_row())

        return response


class LoginView(APIView):
    def get(self, request: HttpRequest) -> HttpResponse:
        credentials = json.loads(
            (settings.BASE_DIR / "rhim" / "credentials.json").open("r").read()
        )
        client_id = credentials["web"]["client_id"]
        client_secret = credentials["web"]["client_secret"]
        redirect_uri = "http://localhost:8000/oauth_redirect"

        authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        token_url = "https://www.googleapis.com/oauth2/v4/token"
        scope = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

        google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        authorization_url, state = google.authorization_url(
            authorization_base_url, access_type="offline", prompt="select_account"
        )

        return render(
            request, "login.jinja2", context={"oauth_login_url": authorization_url}
        )


class OAuthRedirectView(APIView):
    def get(self, request: HttpRequest):
        import os

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        credentials = json.loads(
            (settings.BASE_DIR / "rhim" / "credentials.json").open("r").read()
        )
        client_id = credentials["web"]["client_id"]
        client_secret = credentials["web"]["client_secret"]
        redirect_uri = "http://localhost:8000/oauth_redirect"
        token_url = "https://www.googleapis.com/oauth2/v4/token"

        scope = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

        google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        google.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.get_full_path(),
        )
        r = google.get("https://www.googleapis.com/oauth2/v1/userinfo")

        given_name = json.loads(r.content)["given_name"]
        request.session["user"] = json.loads(r.content)["given_name"]

        return HttpResponse(f"Hi {given_name}")
