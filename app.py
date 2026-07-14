import streamlit as st
import subprocess
import json
import os
from datetime import datetime


# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI Research Crew",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Custom CSS Olive Theme
# -----------------------------

st.markdown("""
<style>

body {
    background-color:#101810;
}

.main {
    background: linear-gradient(
        135deg,
        #101810,
        #243324
    );
}

h1,h2,h3 {
    color:#D4D9B0;
}


.card {

    background: linear-gradient(
        145deg,
        #283828,
        #182518
    );

    padding:20px;
    border-radius:20px;
    border:1px solid #65743A;
    margin-bottom:20px;

}


.stButton button {

    background: linear-gradient(
        90deg,
        #556B2F,
        #8A9A5B
    );

    color:white;
    border-radius:15px;
    height:3em;
    width:100%;
    font-size:18px;

}


</style>

""", unsafe_allow_html=True)



# -----------------------------
# History Functions
# -----------------------------

HISTORY_FILE = "history.json"


def load_history():

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE,"r") as f:
            return json.load(f)

    return []



def save_history(topic, report):

    history = load_history()

    history.append({

        "topic": topic,
        "date": str(datetime.now()),
        "report": report

    })


    with open(HISTORY_FILE,"w") as f:
        json.dump(history,f,indent=4)



# -----------------------------
# Sidebar
# -----------------------------


with st.sidebar:


    st.title("🤖 AI Research Crew")

    st.markdown(
    """
    ---
    **Powered by CrewAI**

    🧠 Research Agent  
    📊 Analyst Agent  
    📝 Report Generator

    ---
    """
    )


    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📚 History",
            "ℹ️ About"
        ]
    )




# -----------------------------
# HOME
# -----------------------------


if page == "🏠 Home":


    st.title("🤖 AI Research Crew")

    st.write(
        "Generate professional research reports using collaborative AI Agents"
    )


    topic = st.text_input(
        "📚 Research Topic",
        placeholder="Example: Artificial Intelligence in Healthcare"
    )



    col1,col2,col3 = st.columns(3)


    with col1:

        st.markdown(
        """
        <div class="card">

        🧠 <b>Researcher Agent</b>

        <br>
        Collects information and insights.

        </div>
        """,
        unsafe_allow_html=True
        )



    with col2:

        st.markdown(
        """
        <div class="card">

        📊 <b>Analyst Agent</b>

        <br>
        Creates structured reports.

        </div>
        """,
        unsafe_allow_html=True
        )


    with col3:

        st.markdown(
        """
        <div class="card">

        📝 <b>Output</b>

        <br>
        Markdown Report

        </div>
        """,
        unsafe_allow_html=True
        )



    if st.button("🚀 Generate Report"):


        if topic:


            progress = st.progress(0)


            status = st.empty()


            status.info(
                "🔍 Research Agent is working..."
            )

            progress.progress(30)



            try:


                subprocess.run(
                    [
                        "crewai",
                        "run"
                    ],
                    check=True
                )


                progress.progress(80)


                status.info(
                    "📊 Analyst Agent creating report..."
                )



                report_path="output/report.md"



                if os.path.exists(report_path):

                    with open(report_path,"r") as f:

                        report=f.read()



                    save_history(
                        topic,
                        report
                    )


                    progress.progress(100)


                    st.success(
                        "✅ Report Generated Successfully"
                    )



                    st.markdown(
                        report
                    )


                    st.download_button(

                        "⬇️ Download Report",

                        report,

                        file_name="report.md"

                    )



            except Exception as e:


                st.error(e)


        else:

            st.warning(
                "Please enter a topic"
            )



# -----------------------------
# HISTORY
# -----------------------------


elif page=="📚 History":


    st.title("📚 Previous Reports")


    history=load_history()



    if history:


        for item in reversed(history):


            with st.expander(
                f"📄 {item['topic']} - {item['date']}"
            ):

                st.markdown(
                    item["report"]
                )


    else:

        st.info(
            "No reports yet"
        )




# -----------------------------
# ABOUT
# -----------------------------


else:


    st.title("ℹ️ About")

    st.write(
    """
    This application uses CrewAI agents:

    - Research Agent
    - Analyst Agent

    to generate AI-powered reports.
    """
    )