# ChatSensei Lite

An intelligent messaging assistant prototype built with FastAPI for an NLP course project.

## Project Overview

ChatSensei Lite is a messaging assistant prototype that:
- Analyzes chat message tone (question/positive/negative/neutral)
- Generates reply suggestions in three different styles:
  - 🎩 **Polite Style**: Formal, respectful, and courteous
  - 😄 **Funny Style**: Casual, humorous, with emojis
  - 💬 **Straightforward Style**: Concise, clear, and direct
- Learns user preferences through feedback (simple reinforcement learning/bandit algorithm)
- Supports both OpenAI API and pure heuristic methods (no external dependencies required)

## Features

- ✅ Simple and intuitive web interface
- ✅ Real-time tone analysis
- ✅ Multi-style reply generation
- ✅ User preference learning (contextual bandit)
- ✅ Dual-mode support: online (OpenAI) and offline (heuristic)
- ✅ Responsive design with mobile support

## Tech Stack

- **Backend**: Python 3.8+, FastAPI, Uvicorn
- **Frontend**: HTML5, Vanilla JavaScript, Pico.css
- **Template Engine**: Jinja2
- **AI**: OpenAI API (optional)

## Installation

### 1. Clone or Download the Project

```bash
cd chatsensei_lite
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration (Optional)

### Using OpenAI API

To use OpenAI's GPT models for more intelligent suggestions, set your API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Note**: 
- The application works without an API key! It will automatically use built-in heuristic methods.
- You can obtain an API key at [OpenAI Platform](https://platform.openai.com/api-keys).

## Running the Application

### Start the Server

```bash
uvicorn app:app --reload
```

Or run directly:

```bash
python app.py
```

### Access the Application

Open in your browser:

```
http://127.0.0.1:8000/
```

## Usage Instructions

1. **Paste Chat Messages**
   - Paste your received chat messages into the text area
   - Works with WhatsApp, WeChat, Discord, or any chat platform

2. **Analyze & Generate Suggestions**
   - Click the "Analyze & Generate Suggestions" button
   - The system detects tone and generates three style variations

3. **Select and Provide Feedback**
   - Each suggestion has two buttons:
     - **Use 👍**: Indicates you like this style (increases style weight)
     - **Bad 👎**: Indicates you dislike it (decreases style weight)

4. **View Preferences**
   - The bottom panel shows your style preference weights
   - Higher weights indicate stronger preference for that style

## Project Structure

```
chatsensei_lite/
├── app.py                 # FastAPI main application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main page template
└── static/
    ├── script.js         # Frontend JavaScript logic
    └── styles.css        # Custom CSS styles
```

## API Endpoints

### GET /
Returns the main page (HTML)

### POST /suggest
Analyzes chat content and generates suggestions

**Request Body:**
```json
{
  "chat": "Hi, are you free this weekend?"
}
```

**Response:**
```json
{
  "tone": "question",
  "suggestions": {
    "polite": "Thank you for the invitation! Let me think about it and get back to you.",
    "funny": "Haha, let me think about it and get back to you. 😂",
    "straightforward": "Let me think about it and get back to you."
  },
  "preferences": {
    "polite": 1.0,
    "funny": 1.0,
    "straightforward": 1.0
  }
}
```

### POST /feedback
Submits user feedback

**Request Body:**
```json
{
  "chosen_style": "polite",
  "good": true
}
```

**Response:**
```json
{
  "preferences": {
    "polite": 2.0,
    "funny": 1.0,
    "straightforward": 1.0
  }
}
```

## Reinforcement Learning Mechanism

This project uses a simple **Contextual Bandit** algorithm:

- Each style maintains a weight value (initially 1.0)
- Clicking "Use 👍" increases weight by +1.0
- Clicking "Bad 👎" decreases weight by -0.5 (minimum remains 1.0)
- Weights reflect user preference for each style

This is a simplified RL implementation suitable for course projects, demonstrating basic preference learning concepts.

## Development Notes

### Heuristic Mode (No API)

When `OPENAI_API_KEY` is not set, the application uses the following rules:

**Tone Detection:**
- Ends with `?` or `？` → question
- Contains positive keywords (thanks, great, awesome...) → positive
- Contains negative keywords (hate, bad, terrible...) → negative
- Otherwise → neutral

**Suggestion Generation:**
- Selects base responses based on detected tone
- Wraps with style-appropriate phrasing

### OpenAI Mode

Uses the `gpt-4o-mini` model with carefully designed prompts to generate natural, diverse suggestions.

## Troubleshooting

### Issue: Module Not Found Error

Ensure you've activated the virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: OpenAI API Call Fails

- Check if API key is correctly set
- Verify network connection
- Application will automatically fall back to heuristic mode without crashing

### Issue: Port 8000 Already in Use

Use a different port:
```bash
uvicorn app:app --reload --port 8001
```

## Future Improvements

- [ ] Add user account system
- [ ] Persist preference data (database)
- [ ] Support more languages
- [ ] More sophisticated RL algorithms (e.g., Thompson Sampling)
- [ ] Context-aware suggestion generation
- [ ] Batch processing of multiple messages

## License

This project is for educational purposes only (NLP course project).

## Authors

NLP Course Project Team

## Feedback

For questions or suggestions, please submit an Issue or contact me: tianluoboding@gmail.
