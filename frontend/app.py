import streamlit as st

from services.api_client import (
    analyze_cv,
    generate_cv,
    match_job,
    mock_interview,
    prepare_interview,
)

st.set_page_config(page_title="CareerBridge UK", layout="wide")

st.title("CareerBridge UK")
st.subheader("AI Career Mentor")

cv_text = st.text_area("Paste your CV", height=180)
target_role = st.text_input("Target role", "Warehouse Operative")
location = st.text_input("Location", "Doncaster")
experience_level = st.selectbox(
    "Experience level",
    ["Entry-level", "Junior", "Mid-level", "Senior"],
)


def call_backend(action, payload, result_key):
    try:
        response = action(payload)
    except RuntimeError as exc:
        st.error(str(exc))
        return

    if result_key not in response:
        st.error(f"Unexpected backend response: {response}")
        return

    st.write(response[result_key])


base_payload = {
    "cv_text": cv_text,
    "target_role": target_role,
    "location": location,
    "experience_level": experience_level,
}

tab_cv, tab_jobs, tab_interview = st.tabs(["CV", "Jobs", "Interview"])

with tab_cv:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Analyze CV", use_container_width=True):
            if not cv_text.strip():
                st.warning("Paste your CV first.")
            else:
                st.subheader("CV Analysis")
                call_backend(analyze_cv, base_payload, "analysis")

    with col2:
        if st.button("Generate UK CV", use_container_width=True):
            if not cv_text.strip():
                st.warning("Paste your CV first.")
            else:
                st.subheader("Generated CV")
                call_backend(generate_cv, base_payload, "generated_cv")

with tab_jobs:
    job_description = st.text_area("Paste the job description", height=180)

    if st.button("Match Job", use_container_width=True):
        if not cv_text.strip() or not job_description.strip():
            st.warning("Paste both your CV and the job description.")
        else:
            payload = {
                **base_payload,
                "job_description": job_description,
            }
            st.subheader("Job Match")
            call_backend(match_job, payload, "match_result")

with tab_interview:
    interview_style = st.selectbox(
        "Interview style",
        ["Formal", "Conversational", "Competency-based"],
    )
    job_description = st.text_area(
        "Job description for interview prep",
        height=140,
        key="interview_job_description",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Prepare Interview", use_container_width=True):
            if not cv_text.strip():
                st.warning("Paste your CV first.")
            else:
                payload = {
                    **base_payload,
                    "job_description": job_description,
                    "interview_style": interview_style,
                }
                st.subheader("Interview Preparation")
                call_backend(prepare_interview, payload, "preparation")

    with col2:
        candidate_message = st.text_area(
            "Your latest mock interview answer",
            height=120,
            key="mock_message",
        )

        if st.button("Continue Mock Interview", use_container_width=True):
            if not cv_text.strip():
                st.warning("Paste your CV first.")
            else:
                payload = {
                    **base_payload,
                    "interview_style": interview_style,
                    "messages": [
                        {
                            "role": "candidate",
                            "content": candidate_message
                            or "I am ready to start the interview.",
                        }
                    ],
                }
                st.subheader("Mock Interview")
                call_backend(mock_interview, payload, "reply")
