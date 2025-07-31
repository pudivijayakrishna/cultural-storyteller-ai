# The Cultural Storyteller and Poet--AI

A full-stack web application that generates creative poems and stories in multiple Indian languages using AI, with text-to-speech capabilities.

## Features

- **Multi-language Support**: Hindi, Tamil, Bengali, and Telugu
- **Content Types**: Poems and Stories
- **AI-Powered Generation**: Uses Sarvam AI for creative content
- **Text-to-Speech**: Converts generated text to audio
- **Beautiful UI**: Modern, responsive design
- **Real-time Generation**: Instant content creation

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Sarvam AI API
- **Deployment**: Vercel

## Local Development

### Prerequisites

- Python 3.9+
- Node.js (for running the frontend server)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd The-Cultural-Storyteller-and-Poet--AI
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```
   SARVAM_API_KEY=your_sarvam_api_key_here
   ```

5. **Run the application**
   ```bash
   python run_all.py
   ```

   This will start both:
   - Backend server at `http://localhost:5000`
   - Frontend server at `http://localhost:8000`

## Deployment to Vercel

### Prerequisites

- Vercel account
- Sarvam AI API key

### Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Set up environment variables in Vercel**
   - Go to your Vercel dashboard
   - Navigate to your project settings
   - Add environment variable:
     - Name: `SARVAM_API_KEY`
     - Value: Your Sarvam AI API key

4. **Deploy to Vercel**
   ```bash
   vercel
   ```

   Or for production:
   ```bash
   vercel --prod
   ```

### Vercel Configuration

The project includes a `vercel.json` file that configures:
- Python runtime for the backend
- Static file serving for the frontend
- API route handling (`/api/*` routes to backend)
- Static file routes (all other routes to frontend)

## API Endpoints

### POST `/api/generate_content`

Generates creative content based on user input.

**Request Body:**
```json
{
  "prompt": "Write about a brave king",
  "language": "hi-IN",
  "content_type": "story"
}
```

**Response:**
```json
{
  "generated_text": "Generated content...",
  "audio_base64": "base64_encoded_audio_data"
}
```

**Supported Languages:**
- `hi-IN`: Hindi
- `ta-IN`: Tamil
- `bn-IN`: Bengali
- `te-IN`: Telugu

**Content Types:**
- `poem`: Generate poems
- `story`: Generate stories

## Project Structure

```
├── backend/
│   ├── app.py              # Flask backend
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── style.css          # Styles
│   └── app.js             # Frontend JavaScript
├── vercel.json            # Vercel configuration
└── README.md              # This file
```

## Environment Variables

- `SARVAM_API_KEY`: Your Sarvam AI API key (required)

## Troubleshooting

### Common Issues

1. **CORS Errors**: The backend is configured to accept requests from any origin in production
2. **API Key Issues**: Ensure your Sarvam AI API key is correctly set in Vercel environment variables
3. **Audio Generation**: The app uses pydub for audio processing, which requires ffmpeg

### Local Development Issues

- Make sure both backend and frontend are running
- Check that the API key is set in the `.env` file
- Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub. 