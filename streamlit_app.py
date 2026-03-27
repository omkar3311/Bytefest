import streamlit as st
from supabase import create_client
import smtplib
from email.message import EmailMessage
import pandas as pd

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

SMTP_EMAIL = st.secrets["SMTP_EMAIL"]
SMTP_PASSWORD = st.secrets["SMTP_PASSWORD"]
SMTP_SERVER = st.secrets["SMTP_SERVER"]
SMTP_PORT = int(st.secrets["SMTP_PORT"])

def send_email(subject, body, to):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

st.set_page_config(page_title="ByteFest Admin", layout="wide")

tab1, tab2, tab3, tab4 = st.tabs([
    "Approve Registrations",
    "QR Hunt Results",
    "Arrange Mode",
    "Debug Mode"
])


with tab1:

    st.title("Approve Registrations")

    users = (
        supabase
        .table("participant")
        .select("id,name,gmail,fee,auth")
        .order("id", desc=True)
        .execute()
        .data
    )

    for u in users:

        cols = st.columns([2,2,2,1,2])

        cols[0].write(u["name"])
        cols[1].write(u["gmail"])
        cols[2].markdown(f"[View Screenshot]({u['fee']})")

        if u["auth"]:
            cols[3].success("Approved")
        else:
            cols[3].warning("Pending")

            approve = cols[4].button("Approve", key=f"a{u['id']}")
            decline = cols[4].button("Decline", key=f"d{u['id']}")

            if approve:

                supabase.table("participant").update({
                    "auth": True
                }).eq("id", u["id"]).execute()

                send_email(
                    "ByteFest Registration Approved",
                    f"""Hello {u['name']},

Your registration for ByteFest has been approved.

Team ByteFest
""",
                    u["gmail"]
                )

                st.success("User approved and email sent")
                st.rerun()

            if decline:

                supabase.table("participant").delete().eq("id", u["id"]).execute()

                send_email(
                    "ByteFest Registration Update",
                    f"""Hello {u['name']},

Your registration could not be approved.

Please contact ByteFest team.

bytefest2026@gmail.com
""",
                    u["gmail"]
                )

                st.error("User declined and email sent")
                st.rerun()

        st.divider()

with tab2:

    st.title("QR Hunt Leaderboard")

    res = (
        supabase
        .table("participant")
        .select("name,gmail,r-time,round1")
        .eq("round1", False)
        .execute()
    )

    data = res.data

    if data:

        df = pd.DataFrame(data)
        df = df[df["r-time"].notna()]
        df["r-time"] = df["r-time"].astype(int)

        df = df.sort_values("r-time")

        df.insert(0, "Rank", range(1, len(df) + 1))

        df = df.rename(columns={
            "name": "Name",
            "gmail": "Email",
            "r-time": "Time (sec)"
        })

        st.dataframe(df, use_container_width=True)

        st.divider()

        top_n = st.number_input(
            "Select Top Players for Next Round",
            min_value=1,
            max_value=len(df),
            step=1
        )

        if st.button("Send Selection Email"):

            selected = df.head(top_n)

            for _, row in selected.iterrows():

                send_email(
                    "ByteFest Round 2 Selection",
                    f"""Hello {row['Name']},

Congratulations!

You have been selected for the next round of ByteFest.

Please report to the event coordinator for Round 2 instructions.

Best of luck!

Team ByteFest
""",
                    row["Email"]
                )

            st.success(f"Emails sent to top {top_n} participants")

    else:
        st.info("No players finished QR Hunt yet.")

with tab3:

    st.title("Arrange Mode Leaderboard")

    res = (
        supabase
        .table("participant")
        .select("name,gmail,B-score,B-time")
        .not_.is_("B-time", None)
        .execute()
    )

    data = res.data

    if data:

        df = pd.DataFrame(data)

        df["B-time"] = df["B-time"].astype(int)

        df = df.sort_values(
            by=["B-score","B-time"],
            ascending=[False,False]
        )

        df.insert(0,"Rank",range(1,len(df)+1))

        df = df.rename(columns={
            "name":"Name",
            "gmail":"Email",
            "B-score":"Score",
            "B-time":"Time"
        })

        st.dataframe(df,use_container_width=True)

        st.divider()

        default_value = min(3, len(df))

        top_n = st.number_input(
            "Select number of participants eligible for Round 3",
            min_value=1,
            max_value=len(df),
            value=default_value
        )

        if st.button("Send Eligibility Email"):

            selected = df.head(top_n)

            for _, row in selected.iterrows():

                send_email(
                    "ByteFest Round 3 Eligibility",
                    f"""Hello {row['Name']},

Congratulations!

Based on your performance in the Arrange Round,
you are eligible for the next round of ByteFest.

Please report to the event coordinator for further instructions.

Best of luck!

Team ByteFest
""",
                    row["Email"]
                )

            st.success(f"Emails sent to top {top_n} participants")

    else:
        st.info("No arrange submissions yet")

with tab4:

    st.title("Debug Mode Leaderboard")

    res = (
        supabase
        .table("participant")
        .select("name,gmail,D-score,D-time")
        .not_.is_("D-time", None)
        .execute()
    )

    data = res.data

    if data:

        df = pd.DataFrame(data)

        df["D-time"] = df["D-time"].astype(int)

        df = df.sort_values(
            by=["D-score","D-time"],
            ascending=[False,False]
        )

        df.insert(0,"Rank",range(1,len(df)+1))

        df = df.rename(columns={
            "name":"Name",
            "gmail":"Email",
            "D-score":"Score",
            "D-time":"Time"
        })

        st.dataframe(df,use_container_width=True)

    else:
        st.info("No debug submissions yet")
