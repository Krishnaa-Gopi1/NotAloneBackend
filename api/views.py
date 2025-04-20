from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup
from .news_scraper import scrape_cyber_news, validate_topic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse


class ScrapeNewsAPIView(APIView):
    def get(self, request):
        CYBER_NEWS_URL = "https://thehackernews.com/"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(CYBER_NEWS_URL, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = []

            for item in soup.find_all("div", class_="body-post clear"):
                title = item.find("h2", class_="home-title")
                link = item.find("a", class_="story-link")
                summary = item.find("div", class_="home-desc")

                if title and link:
                    articles.append({
                        "title": title.text.strip(),
                        "link": link.get("href"),
                        "summary": summary.text.strip() if summary else "No summary available"
                    })

            return Response({"articles": articles}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from Django!"})

def get_news(request, topic):
    topic = topic.strip()

    if not validate_topic(topic):
        return JsonResponse({"status": "error", "message": "Please enter a valid topic!"}, status=400)

    result = scrape_cyber_news(topic)
    return JsonResponse(result, safe=False)
