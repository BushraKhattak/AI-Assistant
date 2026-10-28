import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for API Key
st.sidebar.title("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using Gemini Flash for fast, efficient performance
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.sidebar.warning("Please enter your Gemini API key to unlock the assistant.")

# Main Application Header
st.title("🤖 AI Personal Assistant")
st.markdown("Your all-in-one companion for answering questions, summarizing texts, managing tasks, and planning your day.")

if api_key:
    # Create Navigation Tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat & Q&A", "📄 Document Summarizer", "📅 Task & Day Planner"])
    
    # TAB 1: Chat & Q&A
    with tab1:
        st.header("Chat with Gemini Flash")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    # Format history for Gemini chat API
                    formatted_history = [
                        {"role": m["role"] if m["role"] != "assistant" else "model", "parts": [m["content"]]} 
                        for m in st.session_state.messages[:-1]
                    ]
                    chat = model.start_chat(history=formatted_history)
                    response = chat.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # TAB 2: Document Summarizer
    with tab2:
        st.header("Document Summarizer")
        doc_text = st.text_area("Paste your article, notes, or document text here:", height=200)
        
        if st.button("Summarize Document", type="primary"):
            if doc_text.strip():
                with st.spinner("Analyzing and summarizing..."):
                    try:
                        summary_prompt = f"Please provide a clear, concise, and structured summary of the following document, highlighting key takeaways:\n\n{doc_text}"
                        response = model.generate_content(summary_prompt)
                        st.subheader("Summary Result")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please paste some text first.")

    # TAB 3: Task & Day Planner
    with tab3:
        st.header("Task & Day Planner")
        tasks_input = st.text_area("List your tasks, goals, or schedule constraints for today:", height=150)
        
        if st.button("Generate Day Plan", type="primary"):
            if tasks_input.strip():
                with st.spinner("Structuring your day..."):
                    try:
                        planner_prompt = f"Act as an expert productivity coach. Create an optimized, realistic, time-blocked daily schedule and priority breakdown based on these goals/tasks:\n\n{tasks_input}"
                        response = model.generate_content(planner_prompt)
                        st.subheader("Your Optimized Schedule")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter your tasks or goals.")
else:
    st.info("👈 Please enter your Gemini API key in the sidebar to get started.")
