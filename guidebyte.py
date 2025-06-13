import streamlit as st
import google.generativeai as genai
import os
import json

# Set page config first
st.set_page_config(
    page_title="GuideByte",
    page_icon="🎮",
    layout="wide"
)

# Set your Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Custom CSS for retro 8-bit theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Main theme colors */
    :root {
        --primary-color: #00ff00;
        --secondary-color: #ff00ff;
        --background-color: #000000;
        --text-color: #ffffff;
        --accent-color: #ffff00;
        --border-color: #00ff00;
        --shadow-offset: 4px;
        --border-width: 3px;
        --base-font-size: 14px;
        --spacing-unit: 1.5rem;
    }

    /* Global font and background */
    .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: var(--base-font-size) !important;
        line-height: 1.8 !important;
    }

    /* Remove default streamlit padding and set consistent spacing */
    .main .block-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--spacing-unit);
    }

    /* Global text styling - ensure all text uses pixel font */
    * {
        font-family: 'Press Start 2P', cursive !important;
    }

    /* Main title styling */
    h1 {
        color: var(--primary-color) !important;
        font-size: 2rem !important;
        text-align: center;
        text-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        margin: var(--spacing-unit) 0 calc(var(--spacing-unit) * 2) 0 !important;
        letter-spacing: 2px;
        line-height: 1.4 !important;
    }

    /* Subtitle/description text - CENTERED */
    .stApp > div:first-child p {
        text-align: center !important;
        color: var(--accent-color);
        font-size: var(--base-font-size);
        margin-bottom: calc(var(--spacing-unit) * 2);
    }

    /* Additional selector for subtitle text to ensure centering */
    .main .block-container > div:first-child > div:first-child > div:nth-child(2) p {
        text-align: center !important;
        color: var(--accent-color) !important;
        font-size: var(--base-font-size) !important;
        margin-bottom: calc(var(--spacing-unit) * 2) !important;
    }

    /* Section headers */
    h3 {
        color: var(--accent-color) !important;
        font-size: calc(var(--base-font-size) + 2px) !important;
        border-bottom: var(--border-width) solid var(--accent-color);
        padding-bottom: calc(var(--spacing-unit) / 2);
        margin: calc(var(--spacing-unit) * 2) 0 var(--spacing-unit) 0 !important;
        text-shadow: 2px 2px 0px var(--background-color);
    }

    /* Input field labels */
    .stTextInput > label,
    .stSelectbox > label {
        color: var(--text-color) !important;
        font-size: var(--base-font-size) !important;
        margin-bottom: calc(var(--spacing-unit) / 2) !important;
        display: block;
        text-shadow: 1px 1px 0px var(--background-color);
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        border: var(--border-width) solid var(--border-color) !important;
        border-radius: 0 !important;
        font-size: var(--base-font-size) !important;
        padding: calc(var(--spacing-unit) / 2) !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        margin-bottom: var(--spacing-unit) !important;
        transition: all 0.1s ease;
        min-height: 48px !important;
        line-height: 1.4 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color) !important;
        outline: none !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--accent-color);
    }

    .stTextInput > div > div > input::placeholder {
        color: #666666;
        font-size: calc(var(--base-font-size) - 1px);
        font-family: 'Press Start 2P', cursive !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: var(--background-color) !important;
        border: var(--border-width) solid var(--border-color) !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        margin-bottom: var(--spacing-unit) !important;
        min-height: 48px !important;
    }

    .stSelectbox > div > div > div {
        color: var(--text-color) !important;
        font-size: var(--base-font-size) !important;
        padding: calc(var(--spacing-unit) / 2) !important;
        line-height: 1.4 !important;
        min-height: 24px !important;
    }

    /* Dropdown menu styling */
    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        border: var(--border-width) solid var(--border-color) !important;
        border-radius: 0 !important;
        font-size: var(--base-font-size) !important;
        min-height: 48px !important;
        padding: calc(var(--spacing-unit) / 2) !important;
    }

    /* Dropdown options container */
    [data-baseweb="popover"] {
        background-color: var(--background-color) !important;
        border: var(--border-width) solid var(--border-color) !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        z-index: 9999 !important;
    }

    /* Individual dropdown options */
    [data-baseweb="menu"] > ul > li {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        font-size: var(--base-font-size) !important;
        padding: calc(var(--spacing-unit) / 2) !important;
        line-height: 1.4 !important;
        min-height: 36px !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    [data-baseweb="menu"] > ul > li:hover {
        background-color: var(--primary-color) !important;
        color: var(--background-color) !important;
    }

    [data-baseweb="menu"] > ul > li:last-child {
        border-bottom: none !important;
    }

    /* Selected option styling */
    .stSelectbox > div > div > div[data-baseweb="select"] span {
        color: var(--text-color) !important;
        font-size: var(--base-font-size) !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--primary-color) !important;
        color: var(--background-color) !important;
        border: var(--border-width) solid var(--border-color) !important;
        border-radius: 0 !important;
        font-size: calc(var(--base-font-size) + 1px) !important;
        padding: calc(var(--spacing-unit) / 2) var(--spacing-unit) !important;
        text-transform: uppercase;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        transition: all 0.1s ease;
        margin: var(--spacing-unit) 0 !important;
        width: 100%;
        font-weight: normal !important;
    }

    .stButton > button:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px var(--secondary-color);
        background-color: var(--accent-color) !important;
    }

    .stButton > button:active {
        transform: translate(var(--shadow-offset), var(--shadow-offset));
        box-shadow: none;
    }

    /* Reset button specific styling */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: var(--secondary-color) !important;
        color: var(--background-color) !important;
        border-color: var(--secondary-color) !important;
    }

    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #ff4444 !important;
        border-color: #ff4444 !important;
    }

    /* Success message styling */
    .stSuccess {
        background-color: var(--background-color) !important;
        color: var(--primary-color) !important;
        border: var(--border-width) solid var(--primary-color) !important;
        border-radius: 0 !important;
        padding: var(--spacing-unit) !important;
        margin: var(--spacing-unit) 0 !important;
        font-size: var(--base-font-size) !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
        text-align: center !important;
    }

    .stSuccess > div {
        font-size: var(--base-font-size) !important;
        text-align: center !important;
    }

    /* Info message styling */
    .stInfo {
        background-color: var(--background-color) !important;
        color: var(--accent-color) !important;
        border: var(--border-width) solid var(--accent-color) !important;
        border-radius: 0 !important;
        padding: var(--spacing-unit) !important;
        margin: var(--spacing-unit) 0 !important;
        font-size: var(--base-font-size) !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
    }

    .stInfo > div {
        font-size: var(--base-font-size) !important;
    }

    /* Error message styling */
    .stError {
        background-color: var(--background-color) !important;
        color: #ff0000 !important;
        border: var(--border-width) solid #ff0000 !important;
        border-radius: 0 !important;
        padding: var(--spacing-unit) !important;
        margin: var(--spacing-unit) 0 !important;
        font-size: var(--base-font-size) !important;
        box-shadow: var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color);
    }

    /* Markdown content styling - CENTERED GUIDE */
    .stMarkdown {
        color: var(--text-color) !important;
        line-height: 2 !important;
    }

    .stMarkdown p {
        font-size: var(--base-font-size) !important;
        margin: calc(var(--spacing-unit) / 2) 0 !important;
        color: var(--text-color) !important;
    }

    /* CENTER THE GENERATED GUIDE - WIDER CONTAINER */
    .stMarkdown:has(h2),
    .stMarkdown:has(strong) {
        text-align: center !important;
        max-width: 1000px !important;
        width: 95% !important;
        margin: calc(var(--spacing-unit) * 2) auto !important;
        padding: calc(var(--spacing-unit) * 2) !important;
        background-color: rgba(0, 255, 0, 0.05) !important;
        border: var(--border-width) solid var(--primary-color) !important;
        box-shadow: calc(var(--shadow-offset) + 2px) calc(var(--shadow-offset) + 2px) 0px var(--secondary-color) !important;
        border-radius: 0 !important;
        position: relative !important;
    }

    /* Add a subtle inner glow to the guide container */
    .stMarkdown:has(h2)::before,
    .stMarkdown:has(strong)::before {
        content: '';
        position: absolute;
        top: var(--border-width);
        left: var(--border-width);
        right: var(--border-width);
        bottom: var(--border-width);
        border: 1px solid rgba(0, 255, 0, 0.2);
        pointer-events: none;
    }

    /* Markdown headers */
    .stMarkdown h1 {
        color: var(--primary-color) !important;
        font-size: calc(var(--base-font-size) + 4px) !important;
        margin: calc(var(--spacing-unit) * 2) 0 var(--spacing-unit) 0 !important;
        text-shadow: 2px 2px 0px var(--secondary-color);
        text-align: center !important;
    }

    .stMarkdown h2 {
        color: var(--accent-color) !important;
        font-size: calc(var(--base-font-size) + 2px) !important;
        border-bottom: var(--border-width) solid var(--accent-color);
        padding-bottom: calc(var(--spacing-unit) / 2);
        margin: calc(var(--spacing-unit) * 1.5) 0 var(--spacing-unit) 0 !important;
        text-shadow: 2px 2px 0px var(--background-color);
        text-align: center !important;
    }

    .stMarkdown h3 {
        color: var(--primary-color) !important;
        font-size: calc(var(--base-font-size) + 1px) !important;
        margin: var(--spacing-unit) 0 calc(var(--spacing-unit) / 2) 0 !important;
        text-align: center !important;
    }

    /* Markdown lists - keep left-aligned but center the container */
    .stMarkdown ul {
        margin: var(--spacing-unit) 0 !important;
        padding-left: calc(var(--spacing-unit) * 2) !important;
        text-align: left !important;
        display: inline-block !important;
    }

    .stMarkdown ul li {
        margin: calc(var(--spacing-unit) / 2) 0 !important;
        color: var(--text-color) !important;
        font-size: var(--base-font-size) !important;
        line-height: 1.8 !important;
        text-align: left !important;
    }

    .stMarkdown ul li::marker {
        color: var(--primary-color);
    }

    /* Strong/bold text in markdown */
    .stMarkdown strong {
        color: var(--accent-color) !important;
        font-weight: normal !important;
        text-shadow: 1px 1px 0px var(--background-color);
    }

    /* Spinner styling */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }

    /* Column styling */
    .stColumn {
        padding: 0 calc(var(--spacing-unit) / 2) !important;
    }

    /* Remove streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Add subtle scanlines effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 50%,
            rgba(0, 255, 0, 0.02) 50%
        );
        background-size: 100% 3px;
        pointer-events: none;
        z-index: 1000;
        opacity: 0.5;
    }

    /* Add slight glow effect to interactive elements */
    .stTextInput > div > div > input:focus,
    .stButton > button:hover {
        box-shadow: 
            var(--shadow-offset) var(--shadow-offset) 0px var(--secondary-color),
            0 0 10px rgba(0, 255, 0, 0.3);
    }

    /* Consistent spacing for all form elements */
    .stTextInput,
    .stSelectbox,
    .stButton {
        margin-bottom: var(--spacing-unit) !important;
    }

    /* Quick Tips section styling */
    .stColumn:last-child .stMarkdown {
        background-color: rgba(0, 255, 0, 0.05);
        border: 2px solid var(--primary-color);
        padding: var(--spacing-unit);
        box-shadow: 4px 4px 0px var(--secondary-color);
        margin-top: calc(var(--spacing-unit) * 2);
        text-align: left !important;
        max-width: none !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        :root {
            --base-font-size: 12px;
            --spacing-unit: 1rem;
            --shadow-offset: 3px;
        }
        
        h1 {
            font-size: 1.5rem !important;
            letter-spacing: 1px;
        }
        
        .main .block-container {
            padding: calc(var(--spacing-unit) / 2);
        }

        /* Ensure mobile dropdown visibility */
        .stSelectbox > div > div {
            min-height: 44px !important;
        }

        [data-baseweb="menu"] > ul > li {
            min-height: 32px !important;
            font-size: calc(var(--base-font-size) - 1px) !important;
        }

        /* Adjust centered guide for mobile */
        .stMarkdown:has(h2),
        .stMarkdown:has(strong) {
            max-width: 98% !important;
            width: 98% !important;
            padding: var(--spacing-unit) !important;
            margin: var(--spacing-unit) auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("GuideByte – AI Micro-Guide Generator for Gamers")
st.write("Get fast, actionable tips for bosses, quests, and builds.")

# Initialize session state for game options
if 'game_options' not in st.session_state:
    st.session_state.game_options = None
if 'current_game' not in st.session_state:
    st.session_state.current_game = None
if 'reset_inputs' not in st.session_state:
    st.session_state.reset_inputs = False

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # Game selection
    game = st.text_input("Game Name", placeholder="e.g. The Witcher 3", 
                        value="" if st.session_state.reset_inputs else None,
                        key="game_input")

# Reset the flag after processing
if st.session_state.reset_inputs:
    st.session_state.reset_inputs = False

# Fetch game-specific options
if game and game != st.session_state.current_game:
    st.session_state.current_game = game
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        game_options_prompt = f"""
        For the game "{game}", provide a JSON object with EXACT game terminology:
        {{
            "modes": ["list of actual game modes/activities as they appear in the game's menu or UI"],
            "playstyles": ["list of actual character builds or playstyles that are commonly used and recognized in the game"],
            "difficulties": ["list of exact difficulty levels as they appear in the game's menu"]
        }}

        Requirements:
        1. For difficulties: Use EXACT names from the game's menu (e.g. for The Witcher 3: "Just the Story!", "Story and Sword!", etc.)
        2. For modes: Use EXACT names of game activities (e.g. "Main Quest", "Side Quest", "Contracts", etc.)
        3. For playstyles: Use EXACT names of character builds or approaches (e.g. "Signs Build", "Combat Build", etc.)
        4. Double-check all names against official game sources
        5. If unsure about any option, omit it rather than guessing
        6. Return ONLY the JSON object, nothing else
        """
        response = model.generate_content(game_options_prompt)
        raw = response.text.strip().removeprefix('```json').removesuffix('```').strip()
        options = json.loads(raw)

        # Validate and clean options
        def clean_options(option_list, default_list):
            if not isinstance(option_list, list):
                return default_list
            # Remove duplicates while preserving order
            seen = set()
            return [x for x in option_list if x and not (x in seen or seen.add(x))]

        st.session_state.game_options = {
            "modes": clean_options(options.get("modes", []), ["Main Quest", "Side Quest"]),
            "playstyles": clean_options(options.get("playstyles", []), ["Balanced", "Magic"]),
            "difficulties": clean_options(options.get("difficulties", []), ["Easy", "Normal", "Hard"])
        }

    except:
        st.session_state.game_options = {
            "modes": ["Main Quest", "Side Quest"],
            "playstyles": ["Balanced", "Magic"],
            "difficulties": ["Easy", "Normal", "Hard"]
        }

# Show additional options if available
if st.session_state.game_options:
    with col1:
        challenge = st.text_input("Challenge", placeholder="e.g. Defeating Eredin",
                                value="" if st.session_state.reset_inputs else None,
                                key="challenge_input")
        mode = st.selectbox("Mode", st.session_state.game_options["modes"],
                          index=0 if st.session_state.reset_inputs else None,
                          key="mode_select")
        playstyle = st.selectbox("Playstyle", st.session_state.game_options["playstyles"],
                               index=0 if st.session_state.reset_inputs else None,
                               key="playstyle_select")
        difficulty = st.selectbox("Difficulty", st.session_state.game_options["difficulties"],
                                index=0 if st.session_state.reset_inputs else None,
                                key="difficulty_select")

        # Create two columns for buttons
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            generate_guide = st.button("Generate Guide", use_container_width=True)
            
        with btn_col2:
            if st.button("Reset", use_container_width=True, key="reset_button_main"):
                # Clear session state
                st.session_state.game_options = None
                st.session_state.current_game = None
                st.session_state.reset_inputs = True
                # Rerun to refresh the interface
                st.rerun()

    with col2:
        st.markdown("### Quick Tips")
        st.markdown("""
        - Be specific with your challenge
        - Include boss names or quest names
        - Mention any specific requirements
        - Specify if you're stuck at a particular point
        """)

# Handle guide generation outside of columns for full-width display
if st.session_state.game_options and generate_guide:
    st.session_state.reset_inputs = False  # Reset the flag
    with st.spinner("Researching and generating guide..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Research prompt
            research_prompt = f"""
            Research this:
            Game: {game}
            Challenge: {challenge}
            Mode: {mode}
            Playstyle: {playstyle}
            Difficulty: {difficulty}

            Provide JSON only:
            {{
                "mechanics": [{{"description": ..., "sources": [...], "confidence": "high/medium/low"}}],
                "strategies": [{{"description": ..., "sources": [...], "confidence": ..., "difficulty_specific": true/false}}],
                "setup": [{{"requirement": ..., "sources": [...], "confidence": ...}}],
                "common_mistakes": [{{"description": ..., "sources": [...], "confidence": ...}}]
            }}
            """

            research_response = model.generate_content(research_prompt)
            research_json = research_response.text.strip().removeprefix('```json').removesuffix('```').strip()
            research_data = json.loads(research_json)

            # Guide generation prompt
            guide_prompt = f"""
You are a tactical assistant generating video game strategy guides using ONLY the structured, verified research provided below.
Do NOT invent or assume any content. If something is missing or not verified, explicitly say so.
If a section is empty, write: "No verified information available."
If confidence is "low", ignore the item unless no other data exists.

This is the structured research:
{json.dumps(research_data, indent=2)}

Write a clean, markdown-formatted guide in this structure:

**Key Mechanics**
- List reliable mechanics and patterns.
- Use exact game terms.
- Note dangerous mechanics.

**Effective Strategies**
- Prioritize high-confidence strategies.
- Mention confirmation for difficulty: {difficulty}.
- Flag failed or unverified strategies.

**Required Setup**
- List exact requirements: level, gear, quest prereqs.
- State which are verified or not for difficulty: {difficulty}.

**Common Mistakes**
- Only verified ones.
- State "No verified mistakes documented" if empty.
            """

            guide_response = model.generate_content(guide_prompt)
            st.success("Guide generated!")
            st.markdown(guide_response.text)

        except Exception as e:
            st.error(f"Error: {e}")
        
else:
    if not st.session_state.game_options:
        st.info("Please enter a game name to get started.")