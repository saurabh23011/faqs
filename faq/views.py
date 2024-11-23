from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache

from .models import FAQ
from .serializers import FAQSerializer
from groq import Groq

from django.conf import settings
client=Groq(api_key=settings.GROQ_API_KEY)


class FAQListView(APIView):
    def get(self,request):
        faqs=FAQ.objects.all()
        serializer=FAQSerializer(faqs,many=True)
        return Response(serializer.data)

class QueryView(APIView):
    def post(self,request):
        query=request.data.get('query','').lower()
        if not query:
            return Response({"error":"query is required"},status=400)
        
        #check cache
        cached_response=cache.get(query)
        if cached_response:
            return Response({"answer":cached_response})
        
        faqs=FAQ.objects.all()
        for faq in faqs:
            if query in faq.questions.lower():
                cache.set(query,faq.answer,timeout=3600)
                return Response({"answer":faq.answer})
            

        try:
            api_key=settings.GROQ_API_KEY
            response=client.chat.completions.create(
                messages=[
                    {
                        "role":"user",
                        "content":query
                    }
                ],
                model='llama3-8b-8192'

            )

            answer=response.choices[0].message.content
            cache.set(query,answer,timeout=3600)

            return Response({"answer":answer})
        
        except Exception as e:
            return Response({"error":f"the system is temporarily unavailable due to {e}"})
        
