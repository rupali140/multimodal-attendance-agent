
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Multimodal Attendance & Engagement Agent",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Multimodal Attendance & Engagement Agent")
st.caption("Classroom attendance and session analytics")

st.info(
    "Project foundation is ready. "
    "Vision, audio, and engagement analysis will be added in later Epics."
)

# Demo attendance data
attendance = pd.DataFrame(
    {
        "Student ID": ["ST001", "ST002", "ST003", "ST004"],
        "Student": ["Student A", "Student B", "Student C", "Student D"],
        "Status": ["Present", "Present", "Absent", "Present"],
    }
)

total_students = len(attendance)
present_count = int((attendance["Status"] == "Present").sum())
absent_count = total_students - present_count
attendance_rate = present_count / total_students * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", total_students)
col2.metric("Present", present_count)
col3.metric("Attendance Rate", f"{attendance_rate:.1f}%")

st.subheader("Attendance Records")
st.dataframe(attendance, use_container_width=True, hide_index=True)

st.subheader("Attendance Overview")

chart_data = attendance["Status"].value_counts().rename_axis(
    "Status"
).reset_index(name="Students")

fig = px.bar(
    chart_data,
    x="Status",
    y="Students",
    title="Present vs Absent",
    text="Students",
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "The displayed records are fictional demonstration data, "
    "not real student attendance."
)

st.divider()
st.header("Vision & Audio Analysis")

st.write(
    "Run analysis on a test classroom image and audio file. "
    "These results are technical measurements, not proof of attendance or engagement."
)

if st.button("Run Sample Analysis"):
    try:
        from modules.pipeline import analyze_classroom
        from modules.analytics import summarize_classroom

        result = analyze_classroom(
            "data/classroom_test.jpg",
            "data/audio_test.wav",
        )
        summary = summarize_classroom(result)

        col1, col2, col3 = st.columns(3)
        col1.metric("Detected Faces", summary["face_count"])
        col2.metric("Audio Intervals", summary["audio_interval_count"])
        col3.metric("Average RMS", summary["average_rms"])

        st.write("**Sound intensity:**", summary["sound_intensity"])
        st.caption(summary["interpretation"])

        st.subheader("Audio RMS by Interval")
        audio_chart_data = pd.DataFrame(result["audio"]["intervals"])

        if not audio_chart_data.empty:
            st.line_chart(
                audio_chart_data.set_index("start_seconds")["rms"]
            )
        else:
            st.info("No audio intervals were found.")

    except FileNotFoundError as error:
        st.error(f"Test file missing: {error}")
    except (ValueError, KeyError) as error:
        st.error(f"Analysis could not be completed: {error}")
