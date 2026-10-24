import streamlit as st

# Page Configuration
st.set_page_config(page_title="SkillBridge - Micro-Internships", page_icon="💼", layout="wide")

# Initialize Session State to store tasks dynamically so they don't disappear
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Design a Minimalist Logo", "company": "EcoCafe Startup", "stipend": "$50", "category": "Design", "status": "Open"},
        {"id": 2, "title": "Write 3 SEO Blog Posts on Tech", "company": "CodePulse Media", "stipend": "$80", "category": "Writing", "status": "Open"},
        {"id": 3, "title": "Fix Python Bug in Automation Script", "company": "DataFlow Analytics", "stipend": "$120", "category": "Coding", "status": "Open"}
    ]

if "applications" not in st.session_state:
    st.session_state.applications = []

# App Header
st.title("💼 SkillBridge: Micro-Internship & Task Portal")
st.markdown("Connecting ambitious students with startups and local businesses for bite-sized projects and real-world experience.")

# --- LOGIN & ROLE SELECTION GATE ---
st.sidebar.title("🔐 Access Portal")
user_role = st.sidebar.selectbox("Select Your Role", ["Select Role", "Student", "Employer"])

if user_role == "Select Role":
    st.info("👈 Please select your role (**Student** or **Employer**) from the sidebar to continue exploring the platform.")

elif user_role == "Student":
    st.sidebar.markdown("---")
    student_nav = st.sidebar.radio("Student Menu", ["Browse & Apply for Tasks", "View My Applications"])
    
    if student_nav == "Browse & Apply for Tasks":
        st.header("🔍 Student Portal: Explore Open Micro-Tasks")
        
        # Filter by category
        category_filter = st.selectbox("Filter by Category", ["All", "Design", "Writing", "Coding"])
        
        for task in st.session_state.tasks:
            if category_filter == "All" or task["category"] == category_filter:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(task["title"])
                        st.write(f"**Company:** {task['company']} | **Category:** {task['category']}")
                        st.write(f"💰 **Stipend:** {task['stipend']}")
                    with col2:
                        st.write("") # spacing
                        if st.button("Apply Now", key=f"apply_{task['id']}"):
                            st.session_state.current_applying_task = task["title"]
                    st.markdown("---")

        # Application form area if user clicked apply
        if "current_applying_task" in st.session_state and st.session_state.current_applying_task:
            st.subheader(f"📝 Apply for: {st.session_state.current_applying_task}")
            with st.form("application_form"):
                student_name = st.text_input("Your Full Name")
                student_email = st.text_input("Your Student Email")
                cover_note = st.text_area("Why are you a good fit for this task?")
                submitted = st.form_submit_button("Submit Application")
                
                if submitted:
                    if student_name and student_email:
                        st.session_state.applications.append({
                            "task": st.session_state.current_applying_task,
                            "name": student_name,
                            "email": student_email,
                            "note": cover_note,
                            "status": "⏳ Pending Review"
                        })
                        st.success("🎉 Application submitted successfully!")
                        st.session_state.current_applying_task = None
                    else:
                        st.error("Please fill in your name and email.")

    else:
        st.header("📋 My Submitted Applications & Notifications")
        if len(st.session_state.applications) == 0:
            st.info("You haven't applied to any tasks yet. Go to 'Browse & Apply' to find a task!")
        else:
            for app in st.session_state.applications:
                status_color = "green" if "Accepted" in app['status'] else "orange"
                
                st.markdown(f"""
                - **Task:** {app['task']}
                - **Applicant:** {app['name']} ({app['email']})
                - **Why I'm a good fit:** {app['note']}
                - **Status:** :{status_color}[**{app['status']}**]
                """)
                st.markdown("---")

elif user_role == "Employer":
    st.sidebar.markdown("---")
    employer_nav = st.sidebar.radio("Employer Menu", ["Post a New Task", "View Student Applications"])
    
    if employer_nav == "Post a New Task":
        st.header("🏢 Employer Dashboard: Post a Micro-Task")
        st.write("Welcome, employer! Post your project below so students can apply.")
        
        with st.form("post_task_form"):
            task_title = st.text_input("Task Title (e.g., Social Media Banner Design)")
            company_name = st.text_input("Company / Organization Name")
            category = st.selectbox("Category", ["Design", "Writing", "Coding", "Marketing"])
            stipend = st.text_input("Proposed Stipend / Reward (e.g., $60)")
            
            post_submitted = st.form_submit_button("Publish Task")
            
            if post_submitted:
                if task_title and company_name:
                    new_id = len(st.session_state.tasks) + 1
                    st.session_state.tasks.append({
                        "id": new_id,
                        "title": task_title,
                        "company": company_name,
                        "stipend": stipend,
                        "category": category,
                        "status": "Open"
                    })
                    st.success("🚀 Task posted live successfully! Students will now see it on the browse page.")
                else:
                    st.error("Please fill out the task title and company name.")
                    
    else:
        st.header("📥 Student Applications Received")
        st.write("Review candidates who have applied for your tasks below:")
        
        if len(st.session_state.applications) == 0:
            st.info("No student applications received yet.")
        else:
            for idx, app in enumerate(st.session_state.applications):
                with st.container():
                    st.markdown(f"### 🎯 Applied For: {app['task']}")
                    st.write(f"**Candidate Name:** {app['name']}")
                    st.write(f"**Contact Email:** {app['email']}")
                    st.write(f"**Cover Pitch:** {app['note']}")
                    st.write(f"**Current Status:** {app['status']}")
                    
                    # Accept application button updates student feed notification directly
                    if app['status'] != "🎉 Accepted!":
                        if st.button("Accept Application", key=f"accept_{idx}"):
                            st.session_state.applications[idx]['status'] = "🎉 Accepted!"
                            st.rerun()
                    else:
                        st.success("Candidate Accepted")
                    st.markdown("---")