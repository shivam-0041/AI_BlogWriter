# 📝 Notes By AI: YouTube-to-Notes & Blog Generator

An intelligent web application that turns any YouTube video into concise, topic-by-topic study notes and blog articles using state-of-the-art AI. The system handles audio extraction, transcription, and contextual note generation within a secure, user-authenticated platform.

---

## 🚀 Key Features

*   📥 **YouTube Audio Extraction**: Downloads high-quality audio streams from any YouTube URL using `yt_dlp`.
*   🎙️ **High-Fidelity Transcription**: Leverages `AssemblyAI` with speaker-labeling support to create precise video transcripts.
*   🧠 **AI Note Generation**: Integrates Google’s `Gemini 1.5 Flash` (`google-generativeai`) to convert transcriptions into structured, study-friendly notes organized by topic.
*   🔐 **Secure User System**: Full authentication suite (Sign Up, Log In, Log Out) using Django's built-in User system, ensuring all generated notes remain private and personalized.
*   📂 **Saved History Database**: Store, review, and view details of all previously generated note posts using a relational database.
*   🎨 **Modern responsive UI**: Designed with Tailwind CSS (`django-tailwind`) and featuring custom loader animations (like a CSS pencil-sketch animation while notes are generating).

---

## 🛠️ Tech Stack & Requirements

### Backend
*   **Python 3.10+**
*   **Django 5.1.2** (Web Framework)
*   **PostgreSQL** (Neon Serverless PostgreSQL Database)

### Frontend
*   **Tailwind CSS** (via `django-tailwind`)
*   **HTML5 / ES6 JavaScript**
*   **django-browser-reload** (For hot reloading in development)

### Third-Party APIs & Libraries
*   `assemblyai` — Speech-to-Text Transcription API
*   `google-generativeai` — Google Gemini API for notes generation
*   `yt-dlp` — Extraction of audio from YouTube URLs
*   `ffmpeg` — Required by `yt_dlp` for post-processing audio extraction to `.mp3` format.

---

## 📂 Project Structure

```text
AI_BlogWriter/
│
├── main/                       # Core Django project settings
│   ├── settings.py             # App configurations, Neon database URL, and settings
│   ├── urls.py                 # Global routing configurations
│   └── ...
│
├── pages/                      # Application app containing views and models
│   ├── admin.py                # Admin register settings
│   ├── models.py               # BlogPost model storing user link, title, and content
│   ├── views.py                # Core logic for download, transcription, and Gemini AI query
│   └── ...
│
├── templates/                  # Frontend HTML templates
│   ├── base.html               # Base layout with Tailwind tags
│   ├── home.html               # Main dashboard with YouTube submit form & custom loader
│   ├── login.html              # User login screen
│   ├── signup.html             # User signup screen
│   ├── all_texts.html          # History list of all saved notes
│   └── text_details.html       # Detailed view of a single saved note
│
├── theme/                      # django-tailwind app directory containing Tailwind resources
│
├── manage.py                   # Django CLI utility
└── Readme.md                   # This project documentation
```

---

## ⚙️ Prerequisites & Setup

### 1. External Dependencies
Make sure you have **Node.js** (for compiling Tailwind CSS styles) and **FFmpeg** installed on your system.
*   **FFmpeg**: 
    *   *Linux*: `sudo apt install ffmpeg`
    *   *macOS*: `brew install ffmpeg`
    *   *Windows*: Download the builds and add `/bin` to your system Environment `PATH`.

### 2. Set Up a Virtual Environment
Navigate to your project folder and initialize a Python virtual environment:

```bash
# Initialize venv
python -m venv myvenv

# Activate venv (macOS/Linux)
source myvenv/bin/activate

# Activate venv (Windows PowerShell)
.\myvenv\Scripts\activate
```

### 3. Install Python Modules
Install the required packages using `pip`:

```bash
pip install django django-tailwind django-browser-reload assemblyai yt-dlp google-generativeai psycopg2-binary
```

### 4. Install & Configure Tailwind CSS
Install Tailwind's Node.js packages through Django:

```bash
python manage.py tailwind install
```

### 5. API Keys Configuration
Currently, API configurations are set inside `pages/views.py`. Set your respective keys at:
*   **AssemblyAI API Key** (around line 88 of [views.py](file:///run/media/test/Newfolder/Backend/temp/AI_BlogWriter/pages/views.py)):
    ```python
    aai.settings.api_key = "Your AssemblyAI api key here"
    ```
*   **Google Gemini API Key** (around line 100 of [views.py](file:///run/media/test/Newfolder/Backend/temp/AI_BlogWriter/pages/views.py)):
    ```python
    genai.configure(api_key="Your Gemini api key here")
    ```

*Note: For production, it is highly recommended to environment-variable load these configurations using `python-dotenv` or `django-environ`.*

### 6. Database Migrations
Configure your PostgreSQL configuration inside `main/settings.py`, then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🏃 Running the Application

To run the application locally, you will need two terminal windows:

### Terminal 1: Compile & Watch Tailwind CSS styles
```bash
# Make sure virtual environment is active
python manage.py tailwind start
```

### Terminal 2: Start the Django Server
```bash
# Make sure virtual environment is active
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 💡 How It Works under the Hood

1.  **Audio Extraction**: When a YouTube link is submitted, `yt_dlp` fetches the best quality audio stream and downloads it locally to the `/media` folder.
2.  **Transcription**: The application utilizes the `AssemblyAI` SDK to upload the audio file and transcribe speech to text.
3.  **Content Synthesis**: The raw text transcription is fed to `google-generativeai` (using `gemini-1.5-flash`) with a targeted prompt instructing it to create organized study notes.
4.  **Local Cleanup & Save**: The generated note is saved to the PostgreSQL database under `BlogPost` tied to the authenticated user. The temporary audio `.mp3` file is deleted from local storage to save space.
