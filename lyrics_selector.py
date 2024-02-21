import os
import random
import streamlit as st
import base64
import json
from streamlit_player import st_player

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

def list_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return files

def read_lyrics(file_path):
    with open(file_path, 'r') as file:
        lyrics = file.read()
    return lyrics

def get_youtube_link(selected_file,lullabies_data):
    
    # Search for the selected lullaby in the loaded JSON data
    for lullaby in lullabies_data["lullabies"]:
        if lullaby["file"] == selected_file:
            return lullaby["link"]
    return None

def recommend_filename(selected_tags, lullabies_data):
    matching_files_links = []

    # Iterate through each lullaby
    for lullaby in lullabies_data:
        # Count how many tags match
        matching_tags = sum(1 for tag in selected_tags.values() if tag in (lullaby["Type"], lullaby["Mood"], lullaby["Audience"]))

        # Add the filename and its corresponding link if it matches either 3 out of 3 or 2 out of 3 tags
        if matching_tags >= 2:
            matching_files_links.append((lullaby["file"]))

    # Randomly select a lullaby file and its corresponding link from the matching files
    if matching_files_links:
        selected_file = random.choice(matching_files_links)
        return selected_file
    else:
        return None, None

def display_lyrics_and_player(folder_path, selected_file, lullabies_data):
        file_path = os.path.join(folder_path, selected_file)

        if os.path.exists(file_path):
            lyrics = read_lyrics(file_path)
            st.markdown(f"<p style='font-weight: bold; color: black;'>{lyrics}</p>", unsafe_allow_html=True)
            #st.write(f"{lyrics}")
            # Get the YouTube link for the selected lullaby
            youtube_link =get_youtube_link(selected_file,lullabies_data)
            if youtube_link:
                #st.write("Play me:")
                st_player(youtube_link)  # Embed the player using streamlit_player
            else:
                pass#display embedded player only if found
                #st.warning("Oops! Link not found.")
        else:
            pass#only show lyrics if found
            #st.error(f"\nError: File '{selected_file}' not found.")

def main():
    st.image("Lullaby_Anytime1.png", width=200)
    # st.title("Lullaby Anytime!")

    folder_path = 'lyrics'  # Change this to the actual path of your 'lyrics' folder

    if not os.path.exists(folder_path):
        st.error(f"The folder '{folder_path}' does not exist.")
        return

    files = list_files(folder_path)
    # Extract file names without the .txt extension
    file_names_without_extension = [os.path.splitext(file)[0] for file in files]
    # Load JSON data from lyrics_catg.json
    json_file_path = os.path.join("lyrics_catg.json")
    with open(json_file_path, 'r') as json_file:
        lullabies_data = json.load(json_file)

    st.write("Select by category")

        # Extracting available tags for Type, Mood, and Audience
    available_tags = {
        "Type": [],
        "Mood": [],
        "Audience": []
    }
    for lullaby in lullabies_data["lullabies"]:
        for category in available_tags.keys():
            available_tags[category].append(str(lullaby.get(category, [])))

    for lullaby in lullabies_data["lullabies"]:
        for category in available_tags.keys():
            available_tags[category]=set(available_tags[category]) #filter out duplicates

    #print(available_tags)
    # Displaying the tags for Type, Mood, and Audience
    selected_tags = {}

    # Create a column for each category title and its tags
    for category, tags in available_tags.items():
        col_title, col_tags = st.columns([1, 4])  # Adjust width ratios as needed

        # Display the category title
        col_title.write(f"### {category}")

        # Display the tags in the respective column
        selected_tags[category] = col_tags.radio("s", options=tags, label_visibility='hidden')

    # Button to trigger search
    apply_button = st.button("Apply")
    if apply_button:
        match = recommend_filename(selected_tags, lullabies_data["lullabies"])
        st.write(f"### Found A Match! '{match[:-4]}'")
        if match:
            display_lyrics_and_player(folder_path, match, lullabies_data)            
        else:
            pass

    st.write("### OR")

    selected_file_index = st.selectbox("Choose From Classics", range(len(files)), format_func=lambda i: file_names_without_extension[i])
    search_button = st.button("Search",key="2")
    #wait for usr to select and click search button
    if search_button:
        selected_file = files[selected_file_index]
        display_lyrics_and_player(folder_path, selected_file, lullabies_data)

if __name__ == "__main__":
    add_bg_from_local('lulaby_bg.jpeg')  # Add background image
    main()
