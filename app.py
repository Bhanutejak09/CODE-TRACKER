
import json
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CodeTrack",
    page_icon="💻",
    layout="wide"
)


def load_problems():
    try:
        with open("problems.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_problems(problems):
    with open("problems.json", "w") as file:
        json.dump(problems, file, indent=4)


problems = load_problems()

total = len(problems)
solved = sum(1 for problem in problems if problem.get("solved", False))
unsolved = total - solved
completion = solved / total * 100 if total > 0 else 0

easy = sum(
    1 for problem in problems
    if problem["difficulty"].strip().lower() == "easy"
)
medium = sum(
    1 for problem in problems
    if problem["difficulty"].strip().lower() == "medium"
)
hard = sum(
    1 for problem in problems
    if problem["difficulty"].strip().lower() == "hard"
)

st.sidebar.title("💻 CodeTrack")
st.sidebar.caption("Your Coding Companion")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Problems", "Analytics"]
)

st.title(f"💻 {page}")

if page == "Dashboard":
    st.subheader("Welcome back, Developer! 👋")
    st.write("Your coding journey, all in one place.")
    st.caption("Keep solving. Keep learning. Keep growing.")

    st.divider()
    st.divider()
    st.subheader("📊 Your Coding Progress")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Problems", total)
    col2.metric("Solved", solved)
    col3.metric("Unsolved", unsolved)
    col4.metric("Completion", f"{completion:.1f}%")
    if completion == 100:
        st.success("Amazing! You've solved every tracked problem.")
    elif solved > 0:
        st.info(f"Great progress! You've solved {solved} out of {total} problems.")
    else:
        st.info("Start solving problems to build your coding streak!")
    st.progress(completion / 100)
    st.caption(f"You have completed {completion:.1f}% of your coding goals.")
    st.divider()
    st.subheader("🕒 Recent Problems")

    if problems:
        recent_problems = problems[-5:][::-1]

        for problem in recent_problems:
            status = "✅ Solved" if problem.get("solved", False) else "⏳ Unsolved"
            st.write(
                f"**{problem.get('name', 'Untitled')}** — "
                f"{problem.get('platform', 'Unknown')} | {status}"
            )
    else:
        st.info("No problems added yet. Go to the Problems page to add one.")
    st.progress(completion / 100)

    st.divider()
    st.subheader("Recent Problems")

    if problems:
        recent_problems = []

        for problem in reversed(problems[-5:]):
            recent_problems.append({
                "Problem": problem["name"],
                "Platform": problem["platform"],
                "Difficulty": problem["difficulty"],
                "Status": (
                    "Solved"
                    if problem.get("solved", False)
                    else "Unsolved"
                )
            })

        st.dataframe(
            recent_problems,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Add your first coding problem in the Problems page.")

elif page == "Problems":
    st.write("Add, search, filter, update, and delete your problems.")

    st.divider()
    st.subheader("Add a New Problem")

    with st.form("add_problem_form"):
        name = st.text_input("Problem Name")
        platform = st.text_input(
            "Platform",
            placeholder="e.g. LeetCode"
        )
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Arrays"
        )
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        submitted = st.form_submit_button("Save Problem")

    if submitted:
        if not name.strip():
            st.error("Problem name cannot be empty.")
        else:
            new_problem = {
                "name": name.strip(),
                "platform": platform.strip(),
                "topic": topic.strip(),
                "difficulty": difficulty,
                "solved": False
            }

            problems.append(new_problem)
            save_problems(problems)

            st.success("Problem saved successfully!")
            st.rerun()

    st.divider()
    st.subheader("Your Problems")

    search_text = st.text_input(
        "Search Problems",
        placeholder="Enter a problem name..."
    )

    if problems:
        topics = sorted(
            set(
                problem["topic"].strip().title() or "Unspecified"
                for problem in problems
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_topic = st.selectbox(
                "Filter by Topic",
                ["All"] + topics
            )

        with col2:
            selected_difficulty = st.selectbox(
                "Filter by Difficulty",
                ["All", "Easy", "Medium", "Hard"]
            )

        with col3:
            selected_status = st.selectbox(
                "Filter by Status",
                ["All", "Solved", "Not solved"]
            )

        filtered_problems = []

        for problem in problems:
            if search_text.lower() not in problem["name"].lower():
                continue

            topic = problem["topic"].strip().title() or "Unspecified"
            difficulty_value = problem["difficulty"].strip().title()
            status = (
                "Solved"
                if problem.get("solved", False)
                else "Not solved"
            )

            if selected_topic != "All" and topic != selected_topic:
                continue

            if (
                selected_difficulty != "All"
                and difficulty_value != selected_difficulty
            ):
                continue

            if selected_status != "All" and status != selected_status:
                continue

            filtered_problems.append({
                "Problem": problem["name"],
                "Platform": problem["platform"],
                "Topic": topic,
                "Difficulty": difficulty_value,
                "Status": status
            })

        if filtered_problems:
            st.dataframe(
                filtered_problems,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No problems match your selected filters.")

        st.caption(
            f"Showing {len(filtered_problems)} of {total} problems."
        )

        st.divider()
        st.subheader("Update Solved Status")

        problem_options = {
            f"{i + 1}. {problem['name']} ({problem['platform']})": i
            for i, problem in enumerate(problems)
        }

        selected_problem = st.selectbox(
            "Choose a problem",
            list(problem_options.keys()),
            key="selected_problem"
        )

        problem_index = problem_options[selected_problem]
        current_status = problems[problem_index].get("solved", False)

        mark_solved = st.checkbox(
            "Solved",
            value=current_status,
            key=f"solved_{problem_index}"
        )

        if mark_solved != current_status:
            problems[problem_index]["solved"] = mark_solved
            save_problems(problems)
            st.rerun()

        st.divider()
        st.subheader("Delete a Problem")

        delete_options = {
            f"{i + 1}. {problem['name']} ({problem['platform']})": i
            for i, problem in enumerate(problems)
        }

        selected_delete = st.selectbox(
            "Choose a problem to delete",
            list(delete_options.keys()),
            key="delete_problem"
        )

        if st.button("Delete Problem"):
            delete_index = delete_options[selected_delete]
            deleted_name = problems[delete_index]["name"]

            problems.pop(delete_index)
            save_problems(problems)

            st.success(f"Deleted: {deleted_name}")
            st.rerun()

        st.divider()
        st.subheader("Export Your Problems")

        export_data = []

        for problem in problems:
            export_data.append({
                "Problem": problem["name"],
                "Platform": problem["platform"],
                "Topic": problem["topic"],
                "Difficulty": problem["difficulty"],
                "Status": (
                    "Solved"
                    if problem.get("solved", False)
                    else "Unsolved"
                )
            })

        df = pd.DataFrame(export_data)

        st.download_button(
            label="Download Problems as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="codetrack_problems.csv",
            mime="text/csv"
        )

    else:
        st.info("No problems recorded yet. Add your first problem above!")

elif page == "Analytics":
    st.write("Analyze your coding practice.")

    st.divider()
    st.subheader("Difficulty Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Easy", easy)
    col2.metric("Medium", medium)
    col3.metric("Hard", hard)

    st.subheader("Difficulty Distribution")

    if problems:
        difficulty_counts = {
            "Easy": easy,
            "Medium": medium,
            "Hard": hard
        }

        st.bar_chart(difficulty_counts)

        st.subheader("Solved vs Unsolved")

        status_counts = {
            "Solved": solved,
            "Unsolved": unsolved
        }

        st.bar_chart(status_counts)

        st.subheader("Topic Statistics")

        topic_counts = {}

        for problem in problems:
            topic = problem["topic"].strip().title() or "Unspecified"
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        st.bar_chart(topic_counts)

    else:
        st.info("Add problems to see your analytics.")
