import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from googleapiclient.discovery import build
from selenium import webdriver
# --- Job Search Section ---


def job_search_section(job_query=None):
    st.header("🔍 Sarkari Job Search")
    
    if not job_query:
        st.info("Please enter a job keyword above to start searching.")
        return

    try:
        url = "https://www.sarkariresult.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Send request to Sarkari Result
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Define sections to search
        sections = [
            ('latestjobs', 'div', 'latestjobs'),
            ('resultblock', 'div', 'resultblock'),
            ('post', 'div', 'post'),
            ('menu', 'div', 'menu'),
            ('posttitle', 'div', 'posttitle'),
            ('headline', 'div', 'headline')
        ]

        results = []
        for section_id, tag, class_name in sections:
            section = soup.find(tag, id=section_id) or soup.find(tag, class_=class_name)
            if section:
                links = section.find_all('a', href=True)
                for a in links:
                    link_text = re.sub(r'\s+', ' ', a.text).strip()
                    if (job_query.lower() in link_text.lower() and
                        not any(x in link_text.lower() for x in ['answer key', 'admit card', 'syllabus']) and
                        len(link_text) > 5):
                        results.append({
                            'text': link_text,
                            'url': a['href'] if a['href'].startswith('http') else f"https://www.sarkariresult.com{a['href']}"
                        })

        # Remove duplicates
        unique_results = []
        seen_urls = set()
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        # Display results
        if unique_results:
            st.success(f"✅ Found {len(unique_results)} matching jobs:")
            for result in unique_results[:10]:  # show top 10 results
                st.markdown(f"- [{result['text']}]({result['url']})")
        else:
            st.warning("No matching jobs found. Try different keywords.")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to connect to Sarkari Result. Error: {str(e)}")
    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {str(e)}")

# --- Dashboard Page ---
def dashboard():
    st.markdown(
        "<h3 style='color:#007ACC; font-weight:bold;'>🎓 Welcome to <span style='color:#FFD700;'>Prem Mohan</span>'s Learning Platform!</h3>",
        unsafe_allow_html=True
    )
    st.title(f"\U0001F389 Welcome! \U0001F44B!")

    st.subheader("\U0001F4DA 12th Complete? Now What to Do?")
    stream_choice = st.selectbox("🎓Dear Student Select Your Stream", [
        "Select",
        "Arts Stream",
        "Biology Stream",
        "Mathematics Stream",
        "Government Jobs Opportunities",
        "Government Jobs Opportunities After 12th"])

    if stream_choice == "Arts Stream":
        st.write("### Arts Stream (12th Arts) Options:")
        st.markdown("""
        ## 🎨 Career Options After 12th - Arts Stream

        ---

        ### 1. 📘 **BA (Bachelor of Arts)**
        - **Specializations:** History, Political Science, Psychology, Sociology, Economics, etc.  
        - **Duration:** 3 years  
        - **Career:** Civil Services, Teaching, Research, NGOs, Content Writing

        ---

        ### 2. 🎨 **BFA (Bachelor of Fine Arts)**
        - **Focus:** Visual and performing arts like painting, sculpture, animation  
        - **Duration:** 3–4 years  
        - **Career:** Artist, Illustrator, Animator, Art Director, Designer

        ---

        ### 3. 📰 **Journalism & Mass Communication**
        - **Focus:** Media, reporting, content creation, public relations  
        - **Duration:** 3 years  
        - **Career:** Journalist, News Anchor, Editor, Media Planner, Content Creator

        ---

        ### 4. ⚖️ **Law (5-Year Integrated Course)**
        - **Focus:** Legal studies, Indian constitution, criminal/civil law  
        - **Duration:** 5 years  
        - **Career:** Lawyer, Judge, Legal Advisor, Public Prosecutor

        ---

        ### 5. 🏨 **Hotel Management, Event Management, Travel & Tourism**
        - **Focus:** Hospitality services, event planning, travel business  
        - **Duration:** 3–4 years  
        - **Career:** Hotel Manager, Event Planner, Travel Consultant, Tour Manager

        ---
        """)

    elif stream_choice == "Biology Stream":
        st.write("### Biology Stream (12th Biology) Options:")
        st.markdown("""
            ## 🧬 Career Options After 12th - Biology Stream

            ---

            ### 1. 🩺 **NEET (National Eligibility Entrance Test)**
            - **Purpose:** Admission to MBBS, BDS, BAMS, BHMS, BPT, BSc Nursing  
            - **Duration:** - MBBS: 5.5 years  
            - BDS: 5 years  
            - BAMS/BHMS: 5.5 years  
            - BPT/Nursing: 4 years  
            - **Focus:** Doctor, Dentist, Physiotherapist, Nurse, Ayurvedic/ Homeopathy Specialist

            ---

            ### 2. 🌿 **BAMS (Bachelor of Ayurvedic Medicine & Surgery)**
            - **Focus:** Ayurvedic medicine and treatment  
            - **Duration:** 5.5 years  
            - **Career:** Ayurvedic doctor, practitioner, or researcher

            ---

            ### 3. 🧘 **BPT (Bachelor of Physiotherapy)**
            - **Focus:** Physical therapy, rehabilitation, and fitness recovery  
            - **Duration:** 4 years  
            - **Career:** Physiotherapist, Sports Rehab Expert, Fitness Therapist

            ---

            ### 4. 🔬 **Biotechnology, Bioinformatics, Genetics**
            - **Focus:** Research and development in life sciences  
            - **Duration:** 3 years  
            - **Career:** Lab Scientist, Geneticist, Biotech Engineer, R&D Specialist

            ---
            """)

    elif stream_choice == "Mathematics Stream":
        st.write("### Mathematics Stream (12th Mathematics) Options:")
        st.markdown("""
        ## 📐 Career Options After 12th - Mathematics Stream

        ---

        ### 1. 🧮 **JEE (Joint Entrance Examination)**
        - **Purpose:** Admission to BTech/BE programs in top engineering institutes (IITs, NITs, IIITs)  
        - **Duration:** 4 years  
        - **Focus:** Engineering fields like Computer Science, Mechanical, Electrical, Civil, etc.

        ---

        ### 2. 💻 **BCA (Bachelor of Computer Applications)**
        - **Focus:** Computer Science, software development, web & app programming  
        - **Duration:** 3 years  
        - **Career:** Software Developer, Web Developer, App Programmer, IT Consultant

        ---

        ### 3. 🔢 **BSc Mathematics**
        - **Focus:** Advanced math concepts, theories, and real-world problem-solving  
        - **Duration:** 3 years  
        - **Career:** Mathematician, Statistician, Data Analyst, Educator

        ---

        ### 4. 📊 **Data Science & Analytics**
        - **Focus:** Statistical analysis, big data, AI/ML models  
        - **Duration:** 3 years (Bachelor's) or via specialized certifications  
        - **Career:** Data Scientist, Analyst, Business Intelligence Expert

        ---

        ### 5. 🧾 **Actuarial Science**
        - **Focus:** Risk analysis, finance, insurance mathematics  
        - **Duration:** No fixed duration (depends on passing actuarial exams)  
        - **Career:** Actuary, Financial Risk Manager, Insurance Analyst

        ---
        """)

    elif stream_choice == "Government Jobs Opportunities":
        st.write("### Government Jobs Opportunities for you :")
        st.markdown("""
        ## 🔍 Top 10 Government Job Opportunities After 12th

        ---

        ### 1. 🏢 **SSC (Staff Selection Commission)**
        - **Role:** LDC, DEO, Junior Assistant, etc.  
        - **Eligibility:** 12th pass  
        - **Exam:** SSC CHSL  
        - **Salary:** ₹19,900 – ₹63,200  
        - **Age Limit:** 18–27 years  
        - **Type:** Central Government Jobs  

        ---

        ### 2. 🏦 **Bank Jobs**
        - **Role:** Clerk, Assistant, PO, Specialist Officer  
        - **Eligibility:** 12th pass (Clerk), Graduation (PO)  
        - **Exam:** SBI/IBPS Clerk & PO  
        - **Salary:** ₹20,000 – ₹45,000  
        - **Age Limit:** 20–30 years  
        - **Type:** Public Sector Banks  

        ---

        ### 3. 🚆 **Railway (RRB) Jobs**
        - **Role:** ASM, Ticket Collector, Group D, etc.  
        - **Eligibility:** 12th pass  
        - **Exam:** RRB NTPC, Group D, ALP  
        - **Salary:** ₹18,000 – ₹35,000  
        - **Age Limit:** 18–33 years  
        - **Type:** Indian Railways  

        ---

        ### 4. 🚓 **Police Jobs**
        - **Role:** Constable, Sub-Inspector (SI)  
        - **Eligibility:** 12th pass (Constable), Graduation (SI)  
        - **Exam:** SSC GD, State Police, UPSC CPO  
        - **Salary:** ₹21,700 – ₹1,12,400  
        - **Age Limit:** 18–25 (Constable), 20–25 (SI)  
        - **Type:** State & Central Police Forces  

        ---

        ### 5. 🪖 **Defence Jobs (Army/Navy/Air Force)**
        - **Role:** Soldier, Airmen, Sailor  
        - **Eligibility:** 12th pass (with specific subjects for technical roles)  
        - **Exam:** NDA, other recruitment exams  
        - **Salary:** ₹21,000 – ₹50,000+  
        - **Age Limit:** 16.5–23 years  
        - **Type:** Indian Armed Forces  

        ---

        ### 6. 👩‍🏫 **Teaching Jobs**
        - **Role:** Primary Teacher, TGT, PGT  
        - **Eligibility:** 12th + Diploma (Primary), Graduation for others  
        - **Exam:** CTET, State TET  
        - **Salary:** ₹25,000 – ₹60,000+  
        - **Age Limit:** 18–40 years  
        - **Type:** Government Schools  

        ---

        ### 7. 🎖️ **NDA (National Defence Academy)**
        - **Role:** Officer (Army/Navy/Air Force)  
        - **Eligibility:** 12th pass (PCM for tech roles)  
        - **Exam:** NDA  
        - **Salary:** ₹56,100 – ₹1,77,500+  
        - **Age Limit:** 16.5–19.5 years  
        - **Type:** Armed Forces Officer  

        ---

        ### 8. 📮 **Post Office Jobs**
        - **Role:** Postal Assistant, Sorting Assistant, MTS  
        - **Eligibility:** 12th pass  
        - **Exam:** India Post Exams  
        - **Salary:** ₹18,000 – ₹40,000+  
        - **Age Limit:** 18–27 years  
        - **Type:** India Post (Central Government)  

        ---

        ### 9. ✈️ **Air India Jobs**
        - **Role:** Cabin Crew, Ground Staff  
        - **Eligibility:** 12th pass  
        - **Exam:** Air India recruitment  
        - **Salary:** ₹25,000 – ₹50,000  
        - **Age Limit:** 18–27 years  
        - **Type:** Public Sector (Air India)  

        ---

        ### 10. 🏛️ **UPSC (Civil Services & Forest Services)**
        - **Role:** IAS, IPS, IFS  
        - **Eligibility:** Graduation for others  
        - **Exam:** UPSC Civil Services, IFS  
        - **Salary:** ₹56,100 – ₹2,50,000  
        - **Age Limit:** 21–32 years  
        - **Type:** Central Government Services  

        ---
        """)
    elif stream_choice == "Government Jobs Opportunities After 12th":
        st.write("### 🔍Government Jobs Opportunities After 12th:")
        user_query = st.text_input('🎯 After 12th: Search Government Jobs & More Opportunities:')
        if user_query:
            job_search_section(user_query)

# --- YouTube Video Search ---
def search_youtube_videos(query, api_key):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=5,
            channelId="UCyvboRO_Z2rza0IOeJ85UxA"
        )
        response = request.execute()
        return response.get("items", [])
    except Exception as e:
        st.sidebar.error(f"Error fetching YouTube videos: {e}")
        return []

# --- Sidebar Learning Resources ---
def learn_more_sidebar():
    st.sidebar.title("Start Your Preparation with Prem Mohan NextGen \U0001F4DA")
    st.sidebar.title('\U0001F680 Boost Your Knowledge')

    st.sidebar.subheader("\U0001F4FA Prem Mohan's YouTube Channel")
    if st.sidebar.button("Go to YouTube Channel"):
        st.sidebar.markdown("[🎥 Hey Dear! Click Here to Visit My Channel 😊](https://www.youtube.com/@PremMohanofficial)")

    yt_search_query = st.sidebar.text_input("Search inside Channel:")
    if yt_search_query:
        videos = search_youtube_videos(
            yt_search_query,
            "AIzaSyA0rrzp3VznxIswQnmfzrIy9bb4PygmP38"
        )
        if videos:
            st.sidebar.success(f"🎉 Congratulations! Your video title was found. 👉 [Click Here] to watch. '{yt_search_query}':")
            for video in videos:
                if video['id'].get('kind') == 'youtube#video':
                    title = video['snippet']['title']
                    video_id = video['id'].get('videoId')
                    thumbnail = video['snippet']['thumbnails']['default']['url']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    st.sidebar.image(thumbnail, width=120)
                    st.sidebar.markdown(f"[{title}]({video_url})", unsafe_allow_html=True)
        else:
            st.sidebar.warning(f"😢 Sorry Dear! No videos found for your search query.'{yt_search_query}'")

    st.sidebar.subheader("Mock Test Options \U0001F4CB")
    search_test_query = st.sidebar.text_input("Search Mock Tests:", placeholder="Enter test name/subject")
    if search_test_query:
        search_url = f"https://testbook.com/online-test-series?q={search_test_query.replace(' ', '+')}"
        st.sidebar.markdown(f"\U0001F50D Searching for: **{search_test_query}**")
        st.sidebar.markdown(f"[\u2728 Congratulations! Your Searched Mock Test is Here!]({search_url})")

    if st.sidebar.button("Take Mock Test"):
        st.sidebar.markdown("[👉 Click here to take a Mock Test](https://testbook.com/online-test-series)")

    st.sidebar.subheader("\U0001F4CD Navigation")
    if st.sidebar.button("\U0001F3E0 Home"):
        st.session_state.page = "home"
        st.rerun()
    if st.sidebar.button("\u2139\uFE0F About"):
        st.session_state.page = "about"
        st.rerun()
    if st.sidebar.button("\U0001F4CA Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


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
        .success {
            font-size: 16px;
            color: #2E8B57;
            margin: 20px 0;
        }
    </style>

    <div class="footer">
        <div class="success">
            <h3>🎓 AI Programming Assistant Certified</h3>
            <p><strong>Congratulations!</strong> I've officially completed the <strong>Artificial Intelligence Programming Assistant (AIPA)</strong> course.</p>
            <p>You are now equipped to build intelligent applications using AI, Python, and data analysis techniques.</p>
            <p style="color: #4CAF50; font-weight: bold;">🔥 Future Innovator in the World of AI & Smart Tech!</p>
            <hr>
        </div>
        <h4>👨‍💼 Provider: Prem Mohan</h4>
        <p>📞 Contact: 8174083966</p>
        <p>🏠 Address: Gram & Post- Khaspur, Tanda, Dist- Ambedkar Nagar, Uttar Pradesh</p>
        <p>📧 Email: premmohan966@gmail.com</p>
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
           <p><strong>AIPA (Artificial Intelligence Programming Assistant)</strong><br>
        📅 Completed<br>
        Skills: AI Programming, Python, Data Analysis, Machine Learning, Deep Learning, AI Application Development, Data Visualization, Neural Networks, NLP</p>
    </div>        
    """, unsafe_allow_html=True)

# --- Main Function ---
def main():
    st.set_page_config(page_title="Learning Platform", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    learn_more_sidebar()
    if st.session_state.page == "dashboard":
        st.image("nextgen education.jpg.jpg", use_container_width=300)
        dashboard()
    elif st.session_state.page == "home":
        st.title("🏠 Home Page")
        st.image("nextgen education.jpg.jpg", use_container_width=300)
        st.markdown(
            "<h3 style='color:#009688; font-weight:bold;'>🎓 Welcome to <span style='color:#FF7043;'>Prem Mohan</span>'s Learning Platform!</h3>",
            unsafe_allow_html=True
        )

        st.markdown("""
        # 💼 Prem Mohan NextGen – Your Learning & Career Guide

        **Finished 12th and unsure what's next?**
        You're in the right place!

        **Prem Mohan NextGen** is a student-first platform built to guide your **career journey after 12th**.

        Whether you're from **Arts**, **Biology**, **Maths**, or aiming for **Government Jobs**, we provide the tools and knowledge to move ahead confidently.

        ---

        ### 🚀 What You Can Do Here

        ✅ **Explore Career Options**
        → Find courses, degrees, and career paths based on your stream.

        ✅ **Search Government Job Opportunities**
        → Stay updated with the latest **Sarkari Naukri** after 12th.

        ✅ **Learn from YouTube Videos**
        → Watch career tips, study tricks, and motivation from *Prem Mohan's Official Channel*.

        ✅ **Practice Mock Tests**
        → Get free test series to prep for exams.

        ✅ **Get Book Recommendations**
        → Access handpicked books and study materials for your goals.

        ---

        ### 👥 Who Is This For?

        * Students in or just completed **Class 12**
        * Aspirants preparing for **government or competitive exams**
        * Learners seeking **career advice and motivation**
        * Youth from **rural and small-town backgrounds** needing direction

        ---

        **Start today and shape a smarter, confident, and successful future with us!**
        """)
    elif st.session_state.page == "about":
        st.markdown(
            "<h3 style='color:#6A1B9A; font-weight:bold;'>🎓 Welcome to <span style='color:#00B8D4;'>Prem Mohan</span>'s Learning Platform!</h3>",
            unsafe_allow_html=True
        )
        st.header("👨‍💼About Prem Mohan NextGen")
        st.markdown("""
        *Prem Mohan NextGen* is a student-focused learning and career guidance platform dedicated to helping young minds shape their future after completing *12th grade*.

        We understand this stage of life can be \*confusing, \**overwhelming*, and full of questions like:

        * What should I do after 12th?
        * Which course or career is right for me?
        * How can I prepare for government jobs or competitive exams?
        * Where can I find the right study materials?

        🔍 Our platform is designed to answer \*all these questions in one place—with \**simplicity, clarity, and continuous support*.

        ---

        ### 🎯 Our Vision

        To \*empower students from every background—especially those in \**rural and semi-urban areas*—with accessible, reliable, and practical career guidance.

        We believe that \*talent is everywhere, but it needs the \**right direction and tools* to shine.

        ---

        ### 📚 What We Offer

        ✅ *Career Guidance Based on Your Stream*
        → Choose Arts, Biology, Mathematics, or Government Job stream and explore suitable career options, courses, and exams.

        ✅ *Latest Government Job Updates*
        → Stay updated with recent job notifications, eligibility criteria, and direct application links.

        ✅ *Free Mock Tests*
        → Test your knowledge with free online test series and exam simulations.

        ✅ *Video Learning from YouTube*
        → Watch career tips, study techniques, and motivational content from Prem Mohan's official YouTube channel.

        ✅ *Recommended Books*
        → Get handpicked books and materials tailored to your career goal and study needs.

        ✅ *Student-Friendly Interface*
        → Clean, simple, and mobile-friendly design to help you start learning anytime, anywhere.

        ---

        ### 👨‍🏫 Why Choose Us?

        * 🧑‍🎓 *Built by learners, for learners*
        * 🌐 *Completely online and easy to access*
        * 💡 *Focus on both academic and career development*
        * 🆓 *Most resources are free and community-driven*
        * 📞 *Personalized support and easy contact options*

        ---

        At \*Prem Mohan NextGen, we're not just building a platform—we're building a \**community of future leaders, dreamers, and achievers*.

        🚀 *Let's walk this journey together. Your future starts now!*
        """, unsafe_allow_html=True)
        footer()
    return

  

if __name__ == "__main__":
    main()
