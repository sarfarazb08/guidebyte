# GuideByte 🎮

GuideByte is an AI-powered micro-guide generator designed specifically for gamers. It provides fast, actionable tips for bosses, quests, and builds in your favorite games.

## Features

- **Game-Specific Guidance**: Get tailored advice for any game you're playing
- **Multiple Game Modes**: Support for various game modes and activities
- **Playstyle Customization**: Get tips based on your preferred playstyle
- **Difficulty-Based Strategies**: Receive advice appropriate for your chosen difficulty level
- **Retro 8-Bit UI**: Enjoy a nostalgic gaming-inspired interface
- **Real-time Research**: AI-powered research and strategy generation
- **Mobile Responsive**: Works seamlessly on both desktop and mobile devices

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Styling**: Custom CSS with retro gaming theme
- **Data Handling**: JSON for structured data management

## Prerequisites

- Python 3.7+
- Google Gemini API key
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/guidebyte.git
cd guidebyte
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key:
   - Get your API key from Google AI Studio
   - Replace the API key in the code or set it as an environment variable

## Usage

1. Run the application:
```bash
streamlit run guidebyte.py
```

2. Enter the game name you need help with
3. Specify your challenge (e.g., boss name, quest name)
4. Select the game mode, playstyle, and difficulty
5. Click "Generate Guide" to get your personalized strategy

## Features in Detail

### Game Options
- Dynamic game-specific options based on the game you enter
- Accurate game terminology and modes
- Verified difficulty levels and playstyles

### Guide Generation
- Research-backed strategies
- Difficulty-specific advice
- Common mistakes to avoid
- Required setup and prerequisites
- Key mechanics and patterns

### User Interface
- Retro 8-bit gaming theme
- Responsive design
- Intuitive layout
- Quick tips section
- Easy reset functionality


## Acknowledgments

- Google Gemini AI for powering the guide generation
- Streamlit for the web framework
- Various AI tools for code development (Chatgpt, Cursor, Claude)
- The gaming community for inspiration