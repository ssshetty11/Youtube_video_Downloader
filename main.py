import streamlit as st
import yt_dlp
import os
import sys
import base64


# Function to convert an image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the path to your local image
local_image_path = "./favicon.ico"  # Update this to your local image path

# Convert the local image to base64
icon_base64 = image_to_base64(local_image_path)

# Set the page title and other configurations
st.set_page_config(page_title="YouTube Video Downloader", page_icon=f"data:image/png;base64,{icon_base64}")



# Set the page title and other configurations
# st.set_page_config(page_title="YouTube Video Downloader", page_icon="📥")

# Setting the overhead description 
st.title("Download Your Favorite YouTube Videos and Audio!")
st.write("Easily download videos and audio from YouTube for free! Whether it's a tutorial, shorts, music, or a funny clip, you can save it directly to your device.")
st.write("#### How to Use:")
st.write("1. **Paste the YouTube link** into the input box below.")
st.write("2. Click the **Download** button to get your video or audio.")
st.write("3. Choose between MP4 (video) and MP3 (audio) formats.")
st.write("Enjoy your downloads!")

# Custom input box style
input_style = """
<style>
input {
    width: 100%;
    background-color: rgba(31, 41, 55, 0.4); /* bg-gray-800 bg-opacity-40 */
    border: 1px solid #4F46E5; /* border-gray-700 */
    border-radius: 0.375rem; /* rounded */
    color: #D1D5DB; /* text-gray-100 */
    padding: 0.25rem 0.75rem; /* py-1 px-3 */
    transition: border-color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

input:focus {
    border-color: #4F46E5; /* focus:border-indigo-500 */
    outline: none; /* Remove default outline */
    background-color: transparent; /* focus:bg-transparent */
}
</style>
"""

# Apply the custom style
st.markdown(input_style, unsafe_allow_html=True)

# Input box 
video_link = st.text_input("Enter the Link here", "", key="video_link")

# Custom button style with margin
button_style = """
<style>
.custom-button {
    background-color: #4F46E5; /* bg-indigo-500 */
    color: white; /* Change text color to white */
    border: none; /* border-0 */
    padding: 10px 20px; /* py-2 px-8 */
    border-radius: 0.375rem; /* rounded */
    font-size: 1.125rem; /* text-lg */
    transition: background-color 0.2s ease-in-out;
    cursor: pointer; /* Pointer cursor on hover */
    text-decoration: none; /* Remove underline */
    margin-bottom: 10px; /* Add margin below the button */
}

.custom-button:hover {
    background-color: #4338CA; /* hover:bg-indigo-600 */

}

.stButton > button {
    background-color: #4F46E5; /* bg-indigo-500 */
    color: white; /* text-white */
    border: none; /* border-0 */
    padding: 10px 20px; /* py-2 px-8 */
    border-radius: 0.375rem; /* rounded */
    font-size: 1.125rem; /* text-lg */
    transition: background-color 0.2s ease-in-out;
}

.stButton > button:hover {
    background-color: #4338CA; /* hover:bg-indigo-600 */
</style>

"""

# Inject the custom style
st.markdown(button_style, unsafe_allow_html=True)

# Download button
if st.button("Continue"):
    if video_link:
        # Define the path to the Downloads folder
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Extract video information to get the title
        video_info = yt_dlp.YoutubeDL().extract_info(video_link, download=False)
        title = video_info.get('title', 'video').split()[:5]  # Get the first 5 words
        formatted_title = "_".join(title)  # Replace spaces with underscores

        # Define the output file path for video and audio
        output_file_path = os.path.join(downloads_path, f'{formatted_title}.%(ext)s')
        audio_output_path = os.path.join(downloads_path, f'{formatted_title}.mp3')

        with st.spinner("Downloading..."):
            # Download the video
            yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': output_file_path}).download([video_link])
            # Download the audio
            yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'outtmpl': audio_output_path}).download([video_link])

        # Check if the video file exists
        downloaded_file_name = yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': output_file_path}).prepare_filename(video_info)
        full_downloaded_path = os.path.join(downloads_path, downloaded_file_name)

        if os.path.exists(full_downloaded_path) and os.path.exists(audio_output_path):
            st.success(f"Your video is now downloaded at: {full_downloaded_path}")

            st.markdown("<br>", unsafe_allow_html=True) 
            
            # Add a download button for the MP4 file
            with open(full_downloaded_path, "rb") as file:
                st.markdown(f'<a href="data:video/mp4;base64,{base64.b64encode(file.read()).decode()}" class="custom-button" download="{formatted_title}.mp4" style="color: white; text-decoration: none;">Download MP4 File</a>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

            # Add a download button for the MP3 file
            with open(audio_output_path, "rb") as audio_file:
                st.markdown(f'<a href="data:audio/mp3;base64,{base64.b64encode(audio_file.read()).decode()}" class="custom-button" download="{formatted_title}.mp3" style="color: white; text-decoration: none;">Download MP3 File</a>', unsafe_allow_html=True)
        else:
            st.error("The video or audio could not be found.")
    else:
        st.error("Please enter a valid YouTube link.")





