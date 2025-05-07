import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image

# --- Initialize session state ---
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

# --- Login function ---
def log_fun(email, password):
    if email in st.session_state.users_db and st.session_state.users_db[email]['password'] == password:
        return st.session_state.users_db[email]
    return None

# --- Registration function ---
def reg_fun(name, email, mobile, password):
    if email not in st.session_state.users_db:
        st.session_state.users_db[email] = {"name": name, "email": email, "mobile": mobile, "password": password}
        return "done"
    return "User already exists."

# --- Dashboard function ---
def dashboard():
    user_email = st.session_state.user
    if user_email in st.session_state.users_db:
        user = st.session_state.users_db[user_email]
        st.title(f"🎉 Welcome, {user['name']}!")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Mobile:** {user['mobile']}")
    else:
        st.error("User data not found. Please login again.")

    st.subheader("📚 12th Complete? Now What to Do?")
    stream_choice = st.selectbox("Dear Student Select Your Stream", [
        "Select", "Arts Stream", "Biology Stream", "Mathematics Stream", "Government Jobs Opportunities After 12th"
    ])

    st.subheader("Search Latest Government Job Opportunities etc.")
    user_query = st.text_input('🎯 After 12th: Search Government Jobs & More Opportunities:')
    if st.button("Search Job"):
        if user_query:
            try:
                url = "https://www.sarkariresult.com/"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)

                filtered_links = [link for link in links if re.search(user_query.lower(), link.text.lower(), re.IGNORECASE)]
                if filtered_links:
                    st.success(f"Results for '{user_query}':")
                    for link in filtered_links:
                        link_text = link.text.strip()
                        link_url = link['href']
                        if not link_url.startswith('http'):
                            link_url = "https://www.sarkariresult.com/" + link_url
                        st.markdown(f"- [{link_text}]({link_url})")
                else:
                    st.warning(f"No results found for '{user_query}'")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Sidebar Content ---
def learn_more_sidebar():
    st.sidebar.title("Start Your Preparation with Prem Mohan NextGen 📚")
    st.sidebar.title('🚀 Boost Your Knowledge')

    st.sidebar.subheader("🎥 Prem Mohan's YouTube Channel")
    if st.sidebar.button("Go to YouTube Channel"):
        st.sidebar.markdown("[👉 Click Here Dear](https://www.youtube.com/@PremMohanofficial)")

    yt_search_query = st.sidebar.text_input("Search inside Channel:")
    if yt_search_query:
        videos = search_youtube_videos(yt_search_query, "AIzaSyA0rrzp3VznxIswQnmfzrIy9bb4PygmP38")
        if videos:
            st.sidebar.success(f"Results found for '{yt_search_query}':")
            for video in videos:
                if video['id'].get('kind') == 'youtube#video':
                    title = video['snippet']['title']
                    video_id = video['id'].get('videoId')
                    thumbnail = video['snippet']['thumbnails']['default']['url']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    st.sidebar.image(thumbnail, width=120)
                    st.sidebar.markdown(f"[{title}]({video_url})", unsafe_allow_html=True)
        else:
            st.sidebar.warning(f"Sorry! No videos found for '{yt_search_query}'")

    st.sidebar.subheader("Recommended Book 📖")
    book = {
        "title": "Prem Mohan NextGen Book",
        "image": "Prem Mohan NextGen Book.png",
        "link": "https://wa.me/p/7601838773250384/918174083966"
    }

    st.sidebar.subheader("Mock Test Options 📋")
    search_test_query = st.sidebar.text_input("Search Mock Tests:", placeholder="Enter test name/subject")
    if search_test_query:
        search_url = f"https://testbook.com/online-test-series?q={search_test_query.replace(' ', '+')}"
        st.sidebar.markdown(f"🔍 Searching for: **{search_test_query}**")
        st.sidebar.markdown(f"[✨ Congratulations! Your Searched Mock Test is Here!]({search_url})")

    if st.sidebar.button("Take Mock Test"):
        st.sidebar.markdown("[👉 Click here to take a Mock Test](https://testbook.com/online-test-series)")

    st.sidebar.subheader("Navigation 🔗")
    if st.sidebar.button("Go to Dashboard"):
        st.session_state.page = "dashboard"

    if st.sidebar.button("About"):
        st.session_state.page = "about"

    if st.sidebar.button("Logout ❌"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.success("Logged out successfully!")
        st.rerun()

# --- YouTube Video Search ---
def search_youtube_videos(query, api_key):
    channel_id = "UCyvboRO_Z2rza0IOeJ85UxA"
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&q={query}&channelId={channel_id}&maxResults=5&key={api_key}"
    )
    response = requests.get(url)
    results = response.json()
    return results.get("items", [])

# --- Footer ---
def footer():
    st.markdown("""
    <style>
        .footer {
            padding: 20px;
            background-color: #f0f0f5;
            text-align: center;
            font-size: 14px;
            color: #333;
            border-top: 1px solid #ddd;
        }
        .footer h4 {
            font-size: 16px;
            margin-bottom: 10px;
        }
        .footer p {
            margin: 5px 0;
        }
    </style>
    <div class="footer">
        <h4>👨‍💼 Provider: Prem Mohan</h4>
        <p>📞 Contact: 8174083966</p>
        <p>🏠 Address: Kanpur, Sanjaynagar, CTI Chauraha</p>
        <p>📧 Email: premmohan966@gmail.com</p>
        <p>🎂 DOB: 20th Oct, 2003</p>
        <p>🏡 Permanent Address: Gram & Post- Khaspur, Tanda, Dist- Ambedkar Nagar, Uttar Pradesh, 224190</p>
        <p>🔧 Hobbies: Explorer of New Technologies, Learning</p>
        <p>💻 Skills: Python, MySQL, HTML, Data Analysis, Machine Learning</p>
        <h4>🏅 Certifications:</h4>
        <p><strong>ADCA (12 Months)</strong><br>
        📅 November 2023 - November 2024<br>
        Skills: MS Office, Python, HTML, MySQL, Photoshop, Data Analysis, Communication</p>
        <p><strong>CCC (3 Months)</strong><br>
        📅 September 2024 - December 2024<br>
        Skills: Internet & Web Browsing, Basic Programming, Cloud Storage, Computer Operations</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main App ---
def main():
    st.title("Welcome to Learning Platform")
    st.subheader('🎓 Prem Mohan NextGen')

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "home"

    menu = ["Home", "About", "Login", "Registration"]
    choice = st.sidebar.selectbox(" Dear Student Choose Page", menu)

    if choice == "Home":
        st.write("Welcome to the home page of the learning platform.")
    elif choice == "About":
        footer()
    elif choice == "Login":
        st.subheader("🔐 Login")
        email = st.text_input("Enter Email", key="login_email")
        password = st.text_input("Enter Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            user = log_fun(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = email
                st.success(f"Welcome back, {user['name']}!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid Credentials. Try again.")
    elif choice == "Registration":
        st.subheader("📝 Registration Form")
        name = st.text_input("Enter Name", key="reg_name")
        email = st.text_input("Enter Email", key="reg_email")
        mobile = st.text_input("Enter Mobile No.", key="reg_mobile")
        password = st.text_input("Enter Password", type="password", key="reg_password")
        if st.button("Submit", key="reg_submit"):
            status = reg_fun(name, email, mobile, password)
            if status == "done":
                st.success("Registration Successful. Please Login!")
            else:
                st.error(f"Registration Failed: {status}")

    if st.session_state.logged_in:
        learn_more_sidebar()
        if st.session_state.page == "dashboard":
            dashboard()

if __name__ == "__main__":
    main()
