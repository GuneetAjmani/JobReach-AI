from django.shortcuts import render, get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from datetime import datetime
from openai import OpenAI
from django.http import JsonResponse
from groq import Groq
import httpx

def home(request):
    """Home page with job search filters"""
    # Get initial set of cities for dropdown
    cities = [
        'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 
        'Chennai', 'Pune', 'Kolkata', 'Ahmedabad'
    ]
    
    # Get current date for date picker default
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get search parameters if they exist
    designation = request.GET.get('designation', '')
    selected_city = request.GET.get('city', '')
    date = request.GET.get('date', today)
    
    context = {
        'cities': cities,
        'today': today,
        'designation': designation,
        'selected_city': selected_city,
        'date': date,
        'jobs': []  # Empty list for initial page load
    }
    return render(request, 'jobs/home.html', context)

def job_list(request):
    """View to display filtered job listings"""
    # Get filter parameters
    designation = request.GET.get('designation', '')
    city = request.GET.get('city', '')
    date = request.GET.get('date', '')

    # Prepare the search query
    query_parts = []
    if designation:
        query_parts.append(designation)
    if city:
        query_parts.append(f"in {city}")
    query = " ".join(query_parts) if query_parts else "jobs in India"

    try:
        # Call the JSearch API
        url = f'https://jsearch.p.rapidapi.com/search'
        params = {
            'query': query,
            'page': '1',
            'num_pages': '1',
            'country': 'in',
            'date_posted': 'all'
        }
        
        headers = {
            'x-rapidapi-key': '2c6da7808emsh3b0aa0a485666f8p199780jsn74db3c33500b',
            'x-rapidapi-host': 'jsearch.p.rapidapi.com'
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Get the list of cities for the dropdown
        cities = [
            'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 
            'Chennai', 'Pune', 'Kolkata', 'Ahmedabad'
        ]

        context = {
            'jobs': data.get('data', []),
            'cities': cities,
            'today': datetime.now().strftime('%Y-%m-%d'),
            'designation': designation,
            'selected_city': city,
            'date': date
        }
        return render(request, 'jobs/job_list.html', context)

    except requests.RequestException as e:
        # If there's an error, return to home page with error message
        context = {
            'cities': [
                'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 
                'Chennai', 'Pune', 'Kolkata', 'Ahmedabad'
            ],
            'today': datetime.now().strftime('%Y-%m-%d'),
            'error': 'Failed to fetch jobs. Please try again.',
            'designation': designation,
            'selected_city': city,
            'date': date
        }
        return render(request, 'jobs/home.html', context)

@api_view(['GET'])
def search_jobs(request):
    try:
        query = request.GET.get('query', '')
        page = request.GET.get('page', '1')
        num_pages = request.GET.get('num_pages', '1')
        country = request.GET.get('country', 'in')
        date_posted = request.GET.get('date_posted', 'all')

        url = f'https://jsearch.p.rapidapi.com/search'
        params = {
            'query': query,
            'page': page,
            'num_pages': num_pages,
            'country': country,
            'date_posted': date_posted
        }
        
        headers = {
            'x-rapidapi-key': settings.JSEARCH_API_KEY,
            'x-rapidapi-host': settings.JSEARCH_API_HOST
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        return Response(response.json())
    except requests.RequestException as e:
        return Response(
            {'error': 'Failed to fetch jobs'},
            status=500
        )

def generate_cold_mail(request, job_id):
    try:
        # Fetch job details from JSearch API
        url = f'https://jsearch.p.rapidapi.com/job-details'
        params = {
            'job_id': job_id,
            'country': 'in'
        }
        
        headers = {
            'x-rapidapi-key': '2c6da7808emsh3b0aa0a485666f8p199780jsn74db3c33500b',
            'x-rapidapi-host': 'jsearch.p.rapidapi.com'
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('data'):
            raise ValueError('Job not found')
            
        job = data['data'][0]  # Get the first job from the response

        # Compose prompt for ChatGPT
        prompt = f"Write a professional cold email to apply for the following job:\n\nTitle: {job['job_title']}\nCompany: {job['employer_name']}\nLocation: {job['job_location']}\nDescription: {job['job_description']}\n\nThe email should be concise, polite, and highlight relevant skills."

        # Initialize Groq client
        try:
            # Create a custom HTTP client without proxy settings
            http_client = httpx.Client(
                timeout=30.0,
                verify=True
            )
            
            client = Groq(
                api_key='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',
                http_client=http_client
            )

            response = client.chat.completions.create(
            model="llama3-70b-8192",  # This is Groq's official model ID for LLaMA 3 70B
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional email writer who creates compelling cold emails for job applications."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=512
        )

            # To access the generated message:
            reply = response.choices[0].message.content
            print(reply)
            # Render the template with the cold email and job details
            return render(request, 'jobs/generate_cold_mail.html', {
                'cold_email': reply,
                'job': job
            })
        except Exception as e:
            print(f"Error with Groq client: {str(e)}")
            raise
        
    except (requests.RequestException, ValueError) as e:
        # If there's an error, return to home page with error message
        context = {
            'cities': [
                'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 
                'Chennai', 'Pune', 'Kolkata', 'Ahmedabad'
            ],
            'today': datetime.now().strftime('%Y-%m-%d'),
            'error': 'Failed to generate cold email. Please try again.',
        }
        return render(request, 'jobs/home.html', context) 