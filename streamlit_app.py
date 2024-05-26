import streamlit as st
import google.generativeai as genai
import os


def generate_content(prompts):
    try:
        # Configuration
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048
        }

        # Initialize Model
        model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

        # Combine prompts into a single prompt
        combined_prompt = " ".join(prompts)

        # Generate Content
        response = model.generate_content([combined_prompt])
        return response.text
    except Exception as e:
        return f"Error occurred during content generation: {str(e)}"

#streamlit UI
def app():
    st.header("Final Project in CCS 229 - Intelligent Systems")
    st.markdown("---")

    text = """
    **Windy C. Sabolbora**  
    **BSCS 3B AI**
    \nCS 229 - Intelligent Systems    
    College of Information and Communications Technology  
    West Visayas State University
    """
    st.markdown(text)
    st.title("Creative Text Recommendation")
    st.markdown("---")

    #initial prompt
    def get_initial_prompt():
        return "Welcome! What kind of creative text would you like to generate? (e.g., story, poem, article)"
    
    #follow up prompt
    def get_follow_up_prompt(choice):
        prompts = {
            "story": "Great choice! What genre of story are you interested in? (e.g., fantasy, mystery, sci-fi)",
            "poem": "Nice! What theme would you like the poem to have? (e.g., love, nature, adventure)",
            "article": "Interesting! What topic should the article be about? (e.g., technology, health, sports)"
        }
        return prompts.get(choice.lower(), "Sorry, I didn't understand that choice. Please choose story, poem, or article.")
    #step 1
    if 'step' not in st.session_state:
        st.session_state.step = 1

    if 'choice' not in st.session_state:
        st.session_state.choice = ""

    if st.session_state.step == 1:
        st.write(get_initial_prompt())
        choice = st.text_input("Please, choose your option:")
        if st.button("Next"):
            st.session_state.choice = choice
            st.session_state.step = 2
    #step 2
    elif st.session_state.step == 2:
        st.write(get_follow_up_prompt(st.session_state.choice))
        detail = st.text_input("Provide more details:")
        if st.button("Generate"):
            final_prompt = f"Create a {st.session_state.choice} about {detail}."
            generated_text = generate_content([final_prompt])
            st.write("Here is your generated text:")
            st.write(generated_text)
            st.session_state.step = 3
    #step3
    elif st.session_state.step == 3:
        if st.button("Start Over"):
            st.session_state.step = 1
            st.session_state.choice = ""

if __name__ == '__main__':
    app()
