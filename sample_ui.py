import streamlit as st
import subprocess
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.image("ummi_ai.jpeg",width=400)
    st.title("Welcome to Ummi.ai")
    st.write("Select a service to continue")

    # Display images with buttons and spaces in between
    col1, space1, col2, space2, col3, space3, col4 = st.columns([20, 8, 20, 8, 20,8,20])
    img_width = 200  # Adjust this value as needed
    with col1:
        option_1_clicked = st.button("Plan your day.", st.image("scheduler1.png", width=img_width, caption=""))
    with space1:
        st.write("")
    with col2:
        option_2_clicked = st.button("Ask anything.", st.image("MaQuery1.png", width=img_width, caption=""))
    with space2:
        st.write("")
    with col3:
        option_3_clicked = st.button("Tell a story.", st.image("Stories1.png", width=img_width, caption=""))
    with col4:
        option_4_clicked = st.button("Sing or Play it.", st.image("Lullaby_Anytime1.png", width=img_width, caption=""))
    # Handle option clicks
    if option_1_clicked:
        run_option_1()
    elif option_2_clicked:
        run_option_2()
    elif option_3_clicked:
        run_option_3()
    elif option_4_clicked:
        run_option_4()

def run_option_1():
    st.title("Work Schedule Management")
    st.write("")
    # Add more content specific to Option 1

def run_option_2():
    st.title("Curated Content Access")
    subprocess.Popen(["streamlit", "run", "ummi_qa_bot.py"])
    st.write("")
    # Add more content specific to Option 2

def run_option_3():
    st.title("Bedtime story")  
    subprocess.Popen(["streamlit", "run", "generate_story.py"])
    st.write("")
    # Add more content specific to Option 3

def run_option_4():
    st.title("Find your lullaby.")
    subprocess.Popen(["streamlit", "run", "lyrics_selector.py"])
    st.write("")

if __name__ == "__main__":
    add_bg_from_local('App_selector_ page.jpeg')  # Add background image
    main()
