import streamlit as st
import os
import instaloader
from pathlib import Path
import shutil  # For folder deletion

# Function to download Instagram reel
def download_reel(url):
    # Create Instaloader instance
    loader = instaloader.Instaloader(save_metadata=False, download_comments=False)
    
    # Extract shortcode from the URL
    shortcode = url.split("/")[-2]
    download_dir = f"./{shortcode}"  # Instaloader creates a folder with this name
    download_path = os.path.join(download_dir, f"{shortcode}.mp4")
    
    try:
        # Download reel
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=shortcode)
        
        # Find and return the video file
        for file in os.listdir(download_dir):
            if file.endswith(".mp4"):
                return os.path.join(download_dir, file)
    except Exception as e:
        return str(e)

# Streamlit UI for the additional page
def reel_download():
    st.write("Enter the Instagram Reel URL below and click the button to download it.")

    # Input and Button
    reel_url = st.text_input("Reel URL", placeholder="https://www.instagram.com/reel/shortcode/")
    if st.button("Download Reel"):
        if reel_url:
            # Process download
            with st.spinner("Downloading the reel..."):
                file_path = download_reel(reel_url)
                
                if os.path.exists(file_path):
                    # Provide file for user to download
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Click to Download Reel",
                            data=file,
                            file_name="instagram_reel.mp4",
                            mime="video/mp4"
                        )
                    
                    # Cleanup: Remove the entire download folder
                    folder_path = os.path.dirname(file_path)
                    shutil.rmtree(folder_path)
                else:
                    st.error(f"Failed to download the reel. Error: {file_path}")
        else:
            st.warning("Please enter a valid Instagram Reel URL.")
