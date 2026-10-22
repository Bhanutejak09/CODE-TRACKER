import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CodeTrack",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).parent / "problems.json"
TODAY = date.today()
GREEN = "#00E68A"

st.markdown(
    """
    <style>
    .stApp {
        background: #0B0F0E;
        color: #F2FFF8;
    }
    [data-testid="stSidebar"] {
        background: #101713;
        border-right: 1px solid #26372E;
    }
    h1, h2, h3 {
        color: #F2FFF8;
        letter-spacing: -0.025em;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #141D18, #0F1512);
        border: 1px solid #26372E;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 112px;
    }
    [data-testid="stMetricLabel"] {
        color: #A8B9AE !important;
    }
    [data-testid="stMetricValue"] {
        color: #00E68A !important;
    }
    [data-testid="stProgressBar"] > div > div {
        background: #00E68A !important;
    }
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {
        background: #00E68A;
        color: #06110B;
        border: 1px solid #00E68A;
        border-radius: 10px;
        font-weight: 750;
        min-height: 2.55rem;
    }
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover {
        background: #7DFFC4;
        color: #06110B;
        border-color: #7DFFC4;
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background: #111915;
        border-color: #304137;
        border-radius: 9px;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #26372E;
        border-radius: 12px;
        overflow: hidden;
    }
    [data-testid="stAlert"] {
        border-radius: 10px;
    }
    hr {
        border-color: #26372E;
    }
    .ct-eyebrow {
        color: #00E68A;
        text-transform: uppercase;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .14em;
        margin-bottom: .35rem;
    }
    .ct-subtitle {
        color: #A8B9AE;
        margin-top: -.35rem;
    }
    .ct-panel {
        background: linear-gradient(145deg, #141D18, #0F1512);
        border: 1px solid #26372E;
        border-radius: 16px;
        padding: 20px 22px;
        margin: 8px 0 16px 0;
    }
    .ct-panel-title {
        color: #F2FFF8;
        font-weight: 750;
        font-size: 1.05rem;
    }
    .ct-panel-text {
        color: #A8B9AE;
        font-size: .92rem;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_problems():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
            st.error("Your problems.json file should contain a list of problems.")
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        st.error("Your problems.json file contains invalid JSON. It has not been changed.")
        return []


def save_problems(problems):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(problems, file, indent=4, ensure_ascii=False)


def get_difficulty(problem):
    value = str(problem.get("difficulty", "Easy")).strip().title()
    return value if value in {"Easy", "Medium", "Hard"} else "Easy"


def get_topic(problem):
    return str(problem.get("topic", "")).strip().title() or "Unspecified"


def get_name(problem):
    return str(problem.get("name", "Untitled")).strip() or "Untitled"


def get_platform(problem):
    return str(problem.get("platform", "Unknown")).strip() or "Unknown"


def parse_activity_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def activity_dates(problems):
    dates = set()

    for problem in problems:
        if problem.get("solved", False):
            solved_date = parse_activity_date(
                problem.get("solved_date")
            )
            if solved_date:
                dates.add(solved_date)

    return dates


def calculate_streaks(days):
    if not days:
        return 0, 0

    sorted_days = sorted(days)
    longest = 1
    current_run = 1

    for previous, current in zip(
        sorted_days, sorted_days[1:]
    ):
        if current == previous + timedelta(days=1):
            current_run += 1
        else:
            current_run = 1

        longest = max(longest, current_run)

    if TODAY in days:
        cursor = TODAY
    elif TODAY - timedelta(days=1) in days:
        cursor = TODAY - timedelta(days=1)
    else:
        return 0, longest

    current = 0

    while cursor in days:
        current += 1
        cursor -= timedelta(days=1)

    return current, longest


def record_solved(problem, solved_status):
    problem["solved"] = solved_status

    if solved_status:
        problem["solved_date"] = TODAY.isoformat()
    else:
        problem.pop("solved_date", None)


problems = load_problems()

total = len(problems)
solved = sum(
    1 for problem in problems
    if problem.get("solved", False)
)
unsolved = total - solved
completion = solved / total * 100 if total else 0

easy = sum(
    1 for problem in problems
    if get_difficulty(problem) == "Easy"
)
medium = sum(
    1 for problem in problems
    if get_difficulty(problem) == "Medium"
)
hard = sum(
    1 for problem in problems
    if get_difficulty(problem) == "Hard"
)

days_active = activity_dates(problems)
current_streak, longest_streak = calculate_streaks(
    days_active
)

st.sidebar.markdown(
    """
    <div style="padding: 8px 0 18px 0;">
        <div style="font-size: 1.7rem; font-weight: 850; color: #F2FFF8;">
            💻 CodeTrack
        </div>
        <div style="color: #A8B9AE; font-size: .9rem;">
            Your coding companion
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Problems", "Analytics", "Streak Tracker"],
)

st.sidebar.divider()
st.sidebar.markdown("**YOUR PROGRESS**")
st.sidebar.progress(completion / 100)
st.sidebar.caption(f"{solved} of {total} problems solved")
st.sidebar.caption(f"🔥 Current streak: {current_streak} day(s)")

st.markdown(
    '<div class="ct-eyebrow">Your personal coding workspace</div>',
    unsafe_allow_html=True,
)

page_titles = {
    "Dashboard": "💻 Dashboard",
    "Problems": "🧩 Problems",
    "Analytics": "📈 Analytics",
    "Streak Tracker": "🔥 Streak Tracker",
}

st.title(page_titles[page])


if page == "Dashboard":
    st.markdown("## Welcome back, Developer 👋")

    st.markdown(
        '<div class="ct-subtitle">'
        'Small, consistent practice builds strong coding skills.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Problems", total)
    col2.metric("Solved", solved)
    col3.metric("Remaining", unsolved)
    col4.metric("Completion", f"{completion:.1f}%")

    if total and solved == total:
        message_title = "🏆 Excellent work — all problems solved!"
        message_text = (
            f"You have solved all {total} tracked problems."
        )
    elif total:
        message_title = "🌱 Keep building your momentum"
        message_text = (
            f"You have solved {solved} out of {total} "
            "tracked problems."
        )
    else:
        message_title = "🌱 Start your coding journey"
        message_text = (
            "Add your first coding problem to start "
            "tracking your progress."
        )

    st.markdown(
        f"""
        <div class="ct-panel">
            <div class="ct-panel-title">{message_title}</div>
            <div class="ct-panel-text">{message_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(completion / 100)
    st.caption(
        f"{completion:.1f}% of your tracked problems are solved."
    )

    st.divider()
    st.subheader("🔥 Practice Streak")

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Streak", f"{current_streak} 🔥")
    col2.metric("Longest Streak", f"{longest_streak} 🏆")
    col3.metric("Active Days", len(days_active))

    if not days_active:
        st.info(
            "Your streak starts when you mark a problem as solved. "
            "Existing solved problems without dates cannot count "
            "toward historical streaks."
        )

    st.divider()
    st.subheader("🕒 Recent Problems")

    if problems:
        recent = []

        for problem in reversed(problems[-5:]):
            recent.append({
                "Problem": get_name(problem),
                "Platform": get_platform(problem),
                "Topic": get_topic(problem),
                "Difficulty": get_difficulty(problem),
                "Status": (
                    "Solved"
                    if problem.get("solved", False)
                    else "Unsolved"
                ),
            })

        st.dataframe(
            pd.DataFrame(recent),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.markdown(
            '<div class="ct-panel">'
            '<div class="ct-panel-title">No problems yet</div>'
            '<div class="ct-panel-text">'
            'Open the Problems page to add your first challenge.'
            '</div></div>',
            unsafe_allow_html=True,
        )


elif page == "Problems":
    st.markdown(
        '<div class="ct-subtitle">'
        'Add, search, filter, update, and remove coding challenges.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("➕ Add a New Problem")

    with st.form("add_problem_form", clear_on_submit=True):
        name = st.text_input(
            "Problem Name",
            placeholder="e.g. Two Sum",
        )

        col1, col2 = st.columns(2)

        with col1:
            platform = st.text_input(
                "Platform",
                placeholder="e.g. LeetCode",
            )
            topic = st.text_input(
                "Topic",
                placeholder="e.g. Arrays",
            )

        with col2:
            difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
            )
            problem_url = st.text_input(
                "Problem URL (optional)",
                placeholder="https://...",
            )

        submitted = st.form_submit_button(
            "Save Problem",
            use_container_width=True,
        )

    if submitted:
        if not name.strip():
            st.error("Problem name cannot be empty.")
        else:
            new_problem = {
                "name": name.strip(),
                "platform": platform.strip() or "Unspecified",
                "topic": topic.strip(),
                "difficulty": difficulty,
                "solved": False,
            }

            if problem_url.strip():
                new_problem["url"] = problem_url.strip()

            problems.append(new_problem)
            save_problems(problems)
            st.success("Problem saved successfully.")
            st.rerun()

    st.divider()
    st.subheader("🔎 Your Problems")

    search_text = st.text_input(
        "Search by problem name",
        placeholder="Type a problem name...",
    )

    if problems:
        topics = sorted({
            get_topic(problem) for problem in problems
        })

        col1, col2, col3 = st.columns(3)

        with col1:
            selected_topic = st.selectbox(
                "Filter by Topic",
                ["All"] + topics,
            )

        with col2:
            selected_difficulty = st.selectbox(
                "Filter by Difficulty",
                ["All", "Easy", "Medium", "Hard"],
            )

        with col3:
            selected_status = st.selectbox(
                "Filter by Status",
                ["All", "Solved", "Not solved"],
            )

        filtered = []

        for problem in problems:
            if search_text.lower() not in get_name(problem).lower():
                continue

            if (
                selected_topic != "All"
                and get_topic(problem) != selected_topic
            ):
                continue

            if (
                selected_difficulty != "All"
                and get_difficulty(problem) != selected_difficulty
            ):
                continue

            status = (
                "Solved"
                if problem.get("solved", False)
                else "Not solved"
            )

            if (
                selected_status != "All"
                and status != selected_status
            ):
                continue

            filtered.append(problem)

        if filtered:
            table_rows = []

            for problem in filtered:
                row = {
                    "Problem": get_name(problem),
                    "Platform": get_platform(problem),
                    "Topic": get_topic(problem),
                    "Difficulty": get_difficulty(problem),
                    "Status": (
                        "Solved"
                        if problem.get("solved", False)
                        else "Unsolved"
                    ),
                }

                if problem.get("url"):
                    row["URL"] = problem["url"]

                table_rows.append(row)

            st.dataframe(
                pd.DataFrame(table_rows),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No problems match these filters.")

        st.caption(f"Showing {len(filtered)} of {total} problems.")

        st.divider()
        st.subheader("✅ Update Solved Status")

        problem_options = {
            f"{i + 1}. {get_name(problem)} ({get_platform(problem)})": i
            for i, problem in enumerate(problems)
        }

        selected_problem = st.selectbox(
            "Choose a problem to update",
            list(problem_options.keys()),
            key="selected_problem",
        )

        problem_index = problem_options[selected_problem]
        current_status = bool(
            problems[problem_index].get("solved", False)
        )

        mark_solved = st.checkbox(
            "Mark as solved",
            value=current_status,
            key=f"solved_{problem_index}_{current_status}",
        )

        if mark_solved != current_status:
            record_solved(
                problems[problem_index],
                mark_solved,
            )
            save_problems(problems)
            st.rerun()

        st.divider()
        st.subheader("🗑️ Delete a Problem")

        selected_delete = st.selectbox(
            "Choose a problem to delete",
            list(problem_options.keys()),
            key="delete_problem",
        )

        if st.button("Delete Selected Problem", type="primary"):
            delete_index = problem_options[selected_delete]
            deleted_name = get_name(problems[delete_index])

            problems.pop(delete_index)
            save_problems(problems)

            st.success(f"Deleted: {deleted_name}")
            st.rerun()

        st.divider()
        st.subheader("📤 Export")

        export_rows = []

        for problem in problems:
            export_rows.append({
                "Problem": get_name(problem),
                "Platform": get_platform(problem),
                "Topic": get_topic(problem),
                "Difficulty": get_difficulty(problem),
                "Status": (
                    "Solved"
                    if problem.get("solved", False)
                    else "Unsolved"
                ),
                "Solved Date": problem.get("solved_date", ""),
                "URL": problem.get("url", ""),
            })

        export_df = pd.DataFrame(
            export_rows,
            columns=[
                "Problem",
                "Platform",
                "Topic",
                "Difficulty",
                "Status",
                "Solved Date",
                "URL",
            ],
        )

        st.download_button(
            "Download Problems as CSV",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="codetrack_problems.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:
        st.info(
            "No problems recorded yet. Add your first problem above."
        )


elif page == "Analytics":
    st.markdown(
        '<div class="ct-subtitle">'
        'Understand your practice and identify where to focus next.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Easy", easy)
    col2.metric("Medium", medium)
    col3.metric("Hard", hard)

    if problems:
        st.divider()
        st.subheader("Difficulty Distribution")

        difficulty_df = pd.DataFrame(
            {"Problems": [easy, medium, hard]},
            index=["Easy", "Medium", "Hard"],
        )

        st.bar_chart(difficulty_df, color=GREEN)

        st.subheader("Solved vs Unsolved")

        status_df = pd.DataFrame(
            {"Problems": [solved, unsolved]},
            index=["Solved", "Unsolved"],
        )

        st.bar_chart(status_df, color=GREEN)

        st.subheader("Problems by Topic")

        topic_counts = Counter(
            get_topic(problem) for problem in problems
        )

        topic_df = pd.DataFrame(
            {"Problems": list(topic_counts.values())},
            index=list(topic_counts.keys()),
        )

        st.bar_chart(topic_df, color=GREEN)

        st.divider()
        st.subheader("Practice Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Topics Practised", len(topic_counts))
        col2.metric(
            "Platforms Used",
            len({get_platform(problem) for problem in problems}),
        )
        col3.metric("Recorded Active Days", len(days_active))

    else:
        st.info("Add coding problems to see your analytics.")


elif page == "Streak Tracker":
    st.markdown(
        '<div class="ct-subtitle">'
        'Build consistency by solving at least one problem each day.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Current Streak", f"{current_streak} days 🔥")
    col2.metric("Longest Streak", f"{longest_streak} days 🏆")
    col3.metric("Active Days", len(days_active))

    if TODAY in days_active:
        st.success(
            "You have recorded a solved problem today. "
            "Keep the momentum going!"
        )
    else:
        st.info(
            "Today's activity is not recorded yet. Mark a problem "
            "as solved on the Problems page to log today's practice."
        )

    st.subheader("Last 30 Days")

    calendar_start = TODAY - timedelta(days=29)
    calendar_rows = []

    for week_start_offset in range(0, 30, 7):
        row = {}

        for day_offset in range(
            week_start_offset,
            min(week_start_offset + 7, 30),
        ):
            calendar_day = calendar_start + timedelta(days=day_offset)
            status = "🟩" if calendar_day in days_active else "⬛"
            row[calendar_day.strftime("%a %d %b")] = status

        calendar_rows.append(row)

    st.dataframe(
        pd.DataFrame(calendar_rows).fillna(""),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "🟩 At least one solved problem has a recorded date. "
        "⬛ No recorded activity."
    )

    st.divider()
    st.subheader("How Streaks Work")

    st.markdown(
        "- A day counts when at least one problem is marked as solved that day.\n"
        "- Your current streak continues through today, or yesterday "
        "if you have not logged today's activity yet.\n"
        "- Existing solved problems without a `solved_date` cannot "
        "be counted as historical activity because their dates are unknown."
    )