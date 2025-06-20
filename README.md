# JobReach-AI

JobReach-AI is a web-based job search platform that leverages real-time job data and AI-powered tools to help users efficiently discover and apply for jobs. The application integrates with the JSearch API to fetch up-to-date job listings and uses Groq/OpenAI (Llama 3) to generate personalized cold emails for job applications.

## Features

- **Real-Time Job Search:**  
  Search and filter jobs by designation, city, and posting date using live data from the JSearch API.

- **AI-Powered Cold Email Generator:**  
  Automatically generate professional, personalized cold emails for job applications using Groq/OpenAI Llama 3.

- **User-Friendly Interface:**  
  Simple and intuitive UI for searching jobs, viewing details, and generating emails.

- **Responsive Design:**  
  Accessible across devices with a clean, modern layout.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** Django Templates, HTML, CSS
- **APIs:** JSearch API (job data), Groq/OpenAI (AI email generation)
- **Other:** Requests, HTTPX

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Django

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/jobreach-ai.git
   cd jobreach-ai
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Add your JSearch API key and Groq/OpenAI API key to a `.env` file or your Django settings.

4. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Start the development server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- Enter your desired job designation, select a city, and pick a posting date to search for jobs.
- Browse the job listings and click on a job to view details.
- Use the "Generate Cold Email" feature to create a personalized application email for any job.

## Project Structure

```
project 4/
├── project 3/
│   ├── jobs/
│   │   ├── templates/
│   │   ├── views.py
│   │   └── ...
│   └── ...
├── requirements.txt
├── README.md
└── ...
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/)
- [Groq](https://console.groq.com/docs) / [OpenAI](https://platform.openai.com/docs/)
- Django Software Foundation
