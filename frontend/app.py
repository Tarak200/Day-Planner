import streamlit as st
import requests

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []  # Chat history
    # Initialize the conversation by adding the System's greeting
    st.session_state.messages.append({"author": "System", "text": "Hi, how are you?"})

if "step" not in st.session_state:
    st.session_state.step = 0  # Tracks the conversation step
if "user_input" not in st.session_state:
    st.session_state.user_input = {}  # Tracks user-provided data like city, date, etc.

def add_message(author, text):
    """Add a message to the chat."""
    st.session_state.messages.append({"author": author, "text": text})

def display_chat():
    """Display all chat messages."""
    for idx, message in enumerate(st.session_state.messages):
        if message["author"] == "User":
            st.text_area(
                "You",
                value=message["text"],
                height=100,
                disabled=True,
                key=f"user_msg_{idx}"
            )
        else:
            st.markdown(f"**System**: {message['text']}")

def query_llm(all_interactions, query):
    """Send conversation history and query to the LLM."""
    payload = {
        "conversation": all_interactions,
        "query": query
    }
    try:
        response = requests.post(
            "http://localhost:8000/api/llm",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from model.")
        else:
            error_details = f"Status Code: {response.status_code}, Response Text: {response.text}"
            st.error(f"Failed to get a response from the LLM. Details: {error_details}")
            return None
    except requests.RequestException as e:
        st.error(f"RequestException: {e}")
        return None

def handle_interaction(user_input):
    """Process user input and update the conversation."""
    step = st.session_state.step

    # Save user input for the current step
    st.session_state.user_input[f"step_{step}"] = user_input

    # Add user's message to the conversation
    add_message("User", user_input)

    # Handle each step
    if step == 0:
        # Step 0: Respond to greeting
        add_message("System", "I'm doing great, thank you! Let's plan your one-day tour. Which city are you interested in visiting?")
        st.session_state.step += 1

    elif step == 1:
        # Step 1: Collect city
        st.session_state.user_input["city"] = user_input
        add_message("System", "What date are you planning for your visit?")
        st.session_state.step += 1

    elif step == 2:
        # Step 2: Collect date
        st.session_state.user_input["date"] = user_input
        add_message("System", "What are your interests? For example: Culture, Food, Historical Sites, etc.")
        st.session_state.step += 1

    elif step == 3:
        # Step 3: Collect interests
        st.session_state.user_input["interests"] = user_input.split(", ") if user_input else []
        add_message("System", "What is your budget for the day?")
        st.session_state.step += 1

    elif step == 4:
        # Step 4: Collect budget and call backend API
        try:
            st.session_state.user_input["budget"] = str(user_input)
            add_message("System", "Got it! Planning your itinerary. Please wait...")

            # Construct the conversation history
            all_interactions = [
                {"role": "System", "content": message["text"]} if message["author"] == "System" else
                {"role": "User", "content": message["text"]}
                for message in st.session_state.messages
            ]

            # Call the backend API with the collected data
            with st.spinner('Planning your itinerary...'):
                itinerary_data = query_llm(all_interactions, user_input)
                if itinerary_data:
                    add_message("System", f"Here’s your planned itinerary:\n\n{itinerary_data}")
                else:
                    add_message("System", "Failed to retrieve itinerary. Please check your inputs and try again.")
        except ValueError:
            add_message("System", "Please enter a valid budget.")
        st.session_state.step += 1

    else:
        # Conversation end
        add_message("System", "Thank you! If you want to start a new conversation, please refresh the page.")
        st.session_state.step = 0  # Reset for a new conversation

# Title of the app
st.title("One-Day Tour Planning Assistant with LLM")

# Display the chat
display_chat()

# User input field
if st.session_state.step == 0:
    user_message = st.text_input("You:", key="greeting_input")
elif st.session_state.step == 1:
    user_message = st.text_input("Enter the city you want to visit:", key="city_input")
elif st.session_state.step == 2:
    user_message = st.text_input("Enter the date of your visit (YYYY-MM-DD):", key="date_input")
elif st.session_state.step == 3:
    user_message = st.text_input("Enter your interests (comma-separated):", key="interests_input")
elif st.session_state.step == 4:
    user_message = st.text_input("Enter your budget:", key="budget_input")
else:
    user_message = None

# Handle user input
if st.button("Send") and user_message:
    handle_interaction(user_message)
