import streamlit as st
import google.generativeai as genai

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TravelGuideAI",
    page_icon="✈️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main background */
.stApp {
    background-color: #f5efe6;
}

/* Header styling */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #1a1208 !important;
    font-size: 2.5rem !important;
}

/* Subheader */
.subtitle {
    color: #7a6e60;
    font-weight: 300;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

/* Input labels */
label {
    font-weight: 500 !important;
    color: #4a5c3a !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.8rem !important;
}

/* Buttons */
.stButton > button {
    background-color: #c96d3f !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background-color: #b85d32 !important;
}

/* Text area */
.stTextArea textarea {
    background-color: #f5efe6 !important;
    border: 1.5px solid #e8e0d5 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    color: #2d2417 !important;
    line-height: 1.8 !important;
}

/* Badge */
.badge {
    display: inline-block;
    background: #c96d3f;
    color: white;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

.divider {
    text-align: center;
    color: #d4a847;
    font-size: 1.1rem;
    margin: 1rem 0;
}

/* Info box */
.info-box {
    background: #fffbf0;
    border: 1px solid rgba(212,168,71,0.4);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.85rem;
    color: #7a6030;
    margin-bottom: 1.2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: generate itinerary ─────────────────────────────────────────────────
def generate_itinerary(destination: str, days: int, nights: int) -> str:
    """Call Gemini and return the itinerary text."""
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"write me a travel itinerary to {destination} for {days} days and {nights} nights",
                ],
            }
        ]
    )

    response = chat_session.send_message(
        f"Create a detailed travel itinerary for {days} days and {nights} nights in {destination}. "
        "Include a catchy title, day-by-day breakdown with morning/afternoon/evening activities, "
        "local dining recommendations, key attractions, hidden gems, and practical travel tips."
    )

    return response.text


# ── Main UI ────────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown('<div class="badge">✦ AI-Powered Travel Planning</div>', unsafe_allow_html=True)
    st.title("Travel Itinerary Generator")
    st.markdown(
        '<p class="subtitle">Generate personalized travel itineraries in seconds — '
        "tailored to your destination, duration, and style.</p>",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="divider">✦</div>', unsafe_allow_html=True)

    # API key input
    st.markdown(
        '<div class="info-box">'
        "<strong>Gemini API Key required.</strong> Enter your key below — it is only used for this session. "
        'Get a free key at <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#c96d3f;">Google AI Studio</a>.'
        "</div>",
        unsafe_allow_html=True,
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
    )

    st.markdown('<div class="divider">✦</div>', unsafe_allow_html=True)

    # Trip details
    destination = st.text_input(
        "Enter your desired destination:",
        placeholder="e.g. Kedarnath, Bali, Paris…",
    )

    col1, col2 = st.columns(2)
    with col1:
        days = st.number_input("Enter the number of days:", min_value=1, value=5)
    with col2:
        nights = st.number_input("Enter the number of nights:", min_value=0, value=4)

    # Generate button
    if st.button("✈ Generate Itinerary"):

        # Validate inputs
        if not api_key.strip():
            st.error("Please enter your Gemini API key.")
        elif not destination.strip():
            st.error("Please enter your desired destination.")
        elif days < 1:
            st.error("Number of days must be at least 1.")
        else:
            try:
                genai.configure(api_key=api_key.strip())

                with st.spinner("Crafting your personalized itinerary…"):
                    itinerary = generate_itinerary(destination.strip(), int(days), int(nights))

                st.success("Your itinerary is ready!")
                st.text_area(
                    "Generated Itinerary:",
                    value=itinerary,
                    height=500,
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

        if not destination.strip() and not api_key.strip():
            st.error("Please make sure all inputs are provided and valid.")


if __name__ == "__main__":
    main()
