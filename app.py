import streamlit as st
import mysql.connector
import hashlib
from streamlit_option_menu import option_menu

# ------------------ Hàm kết nối MySQL ------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="220905",   
        database="school_management"
    )

# ------------------ Mã hóa mật khẩu ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ Xử lý đăng nhập ------------------
def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    query = "SELECT role FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, hashed_pwd))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# ------------------ Đăng ký người dùng ------------------
def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_pwd = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_pwd, role.lower()))
        conn.commit()
        st.success("🎉 Registered successfully!")
    except mysql.connector.errors.IntegrityError:
        st.error("⚠️ Username already exists.")
    finally:
        cursor.close()
        conn.close()

# ------------------ Giao diện chính ------------------
def main():
    st.set_page_config(page_title="School Management System", layout="centered", page_icon="🏫")
    st.markdown("<h1 style='text-align: center; color: navy;'>🏫 School Management System</h1>", unsafe_allow_html=True)
    st.write("##")

    selected = option_menu(
        menu_title=None,
        options=["Login", "Register"],
        icons=["box-arrow-in-right", "person-plus"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "blue", "font-size": "18px"},
            "nav-link": {"font-size": "18px", "text-align": "center", "margin": "2px"},
            "nav-link-selected": {"background-color": "#3399ff", "color": "white"},
        }
    )

    st.write("")

    if selected == "Login":
        st.subheader("🔐 Login to your account")
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                role = login_user(username, password)
                if role:
                    st.success(f"✅ Welcome **{username}**! You are logged in as **{role.title()}**.")
                    # Role-based navigation (placeholder)
                    dashboards = {
                        "student": "📚 Student Dashboard (to be implemented)",
                        "homeroom_teacher": "👩‍🏫 Homeroom Teacher Dashboard (to be implemented)",
                        "subject_teacher": "📘 Subject Teacher Dashboard (to be implemented)",
                        "vice_principal": "🧑‍💼 Vice Principal Dashboard (to be implemented)",
                        "principal": "🎓 Principal Dashboard (to be implemented)",
                    }
                    st.info(dashboards.get(role, "Dashboard under construction."))
                else:
                    st.error("❌ Invalid username or password.")

    elif selected == "Register":
        st.subheader("📝 Create a new account")
        with st.form("register_form"):
            username = st.text_input("👤 Choose a Username")
            password = st.text_input("🔐 Choose a Password", type="password")
            role = st.selectbox("🎭 Select Role", [
                "Student", "Homeroom Teacher", "Subject Teacher", "Vice Principal", "Principal"
            ])
            submitted = st.form_submit_button("Register")
            if submitted:
                register_user(username, password, role)

if __name__ == "__main__":
    main()
