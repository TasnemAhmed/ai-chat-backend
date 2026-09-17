import streamlit as st
import requests


# =========================================================
# CONFIG
# =========================================================

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Color Vision Assistant",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
   COLOR SYSTEM
   ===================================================== */

        :root {
            --navy: #102A43;
            --navy-dark: #0B1F33;
            --navy-light: #243B53;

            /* ألوان أكثر وضوحاً وتباين مع النص الأبيض */
            --blue: #005A9C;         /* أزرق واضح ومريح لعمى الألوان */
            --blue-dark: #003A66;
            --cyan: #7FDBDA;

            --background: #F5F7FA;
            --surface: #FFFFFF;

            --border: #829AB1;       /* تغميق الحدود لتحديد الحقول بوضوح */
            --border-dark: #627D98;

            --text: #102A43;
            --muted: #486581;

            --danger: #B42318;
        }



    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background: var(--background);
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

        /* 1. إظهار الهيدر */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 999999 !important;
    }

    /* 2. إجبار الزرار وكل الأيقونات والعناصر اللي جواه إنها تفضل ظاهرة 100% */
    header[data-testid="stHeader"] button,
    button[data-testid="stHeaderNavStateButton"],
    button[aria-label="Expand sidebar"],
    button[aria-label="Collapse sidebar"],
    button[data-testid="stHeaderNavStateButton"] * {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
    }

    /* 3. تصميم الزرار بحيث يبان كـ Icon واضح جداً لخلفية فاتحة */
    header[data-testid="stHeader"] button {
        background-color: #102A43 !important; /* خلفية كحلي غمق */
        border-radius: 8px !important;
        padding: 6px !important;
        margin: 8px !important;
    }

    /* 4. تغيير لون الأيقونة السهم نفسها للون الأبيض عشان تظهر بوضوح */
    header[data-testid="stHeader"] button svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
        width: 20px !important;
        height: 20px !important;
    }

    /* عند الوقوف على الزرار بالماوس */
    header[data-testid="stHeader"] button:hover {
        background-color: #005A9C !important;
    }

           
    h1,
    h2,
    h3,
    h4 {
        color: var(--text) !important;
        letter-spacing: -0.025em;
    }

    p {
        color: var(--muted);
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    .stTextInput label,
    .stTextArea label,
    .stFileUploader label {
        color: var(--text) !important;
        font-weight: 700 !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #FFFFFF !important;
        color: var(--text) !important;

        border: 1px solid var(--border-dark) !important;
        border-radius: 10px !important;

        min-height: 44px;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--blue) !important;

        box-shadow:
            0 0 0 3px rgba(0, 124, 145, 0.10) !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */
        .stButton > button {
            min-height: 48px !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            font-size: 16px !important;
            border: 2px solid transparent !important;
            transition: all 0.16s ease !important;
        }

        /* إجبار النص وجميع المكونات داخل الزر على الظهور باللون الأبيض الناصع */
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 16px !important;
        }

        /* الزر الأساسي (Primary Button) */
        .stButton > button[kind="primary"],
        .stButton > button {
            background-color: var(--blue) !important;
            color: #FFFFFF !important;
            border-color: var(--blue) !important;
        }

        .stButton > button:hover {
            background-color: var(--blue-dark) !important;
            border-color: var(--blue-dark) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }

        /* الزر الثانوي */
        .stButton > button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: var(--navy) !important;
            border: 2px solid var(--navy) !important;
        }

        .stButton > button[kind="secondary"] p,
        .stButton > button[kind="secondary"] span {
            color: var(--navy) !important;
        }

    /* =====================================================
       AUTH PAGES
       ===================================================== */

    .auth-container {
        max-width: 440px;
        margin: 3.5rem auto 0 auto;
    }

    .auth-brand {
        text-align: center;
        margin-bottom: 2.2rem;
    }

    .auth-icon {
        width: 64px;
        height: 64px;

        margin: 0 auto 18px auto;

        border-radius: 18px;

        background: var(--navy);

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 30px;

        box-shadow:
            0 12px 28px rgba(16, 42, 67, 0.18);
    }

    .auth-title {
        color: var(--text);
        font-size: 30px;
        font-weight: 750;
        letter-spacing: -0.03em;
        margin-bottom: 7px;
    }

    .auth-subtitle {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.6;
    }

    .auth-note {
        text-align: center;
        color: var(--muted);
        font-size: 13px;
        margin-top: 15px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: var(--navy-dark);

        border-right:
            1px solid #203B52;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.1rem;
    }

    section[data-testid="stSidebar"] * {
        color: #F7FAFC;
    }

    .sidebar-brand {
        padding:
            5px 7px 22px 7px;
    }

    .sidebar-title {
        font-size: 17px;
        font-weight: 750;
        color: white;
    }

    .sidebar-subtitle {
        font-size: 11px;
        color: #9FB3C8;
        margin-top: 3px;
    }

    .sidebar-section {
        color: #829AB1;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 0.12em;

        margin:
            22px 7px 8px 7px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;

        min-height: 40px;

        background: transparent;

        border:
            1px solid transparent;

        border-radius: 9px;

        color: #D9E2EC;

        text-align: left;

        transition:
            background-color 0.16s ease,
            border-color 0.16s ease,
            transform 0.16s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #173A55;

        border-color: #2E526D;

        transform: translateX(2px);
    }


    /* New conversation */

    .new-chat-button button {
        background: var(--blue) !important;

        border-color: var(--blue) !important;

        color: white !important;

        font-weight: 700 !important;
    }

    .new-chat-button button:hover {
        background: var(--blue-dark) !important;
        border-color: var(--blue-dark) !important;
    }


    /* =====================================================
       CHAT
       ===================================================== */

    [data-testid="stChatMessage"] {
        border:
            1px solid var(--border);

        border-radius: 14px;

        padding:
            0.8rem 1rem;

        margin-bottom: 0.7rem;

        animation:
            messageIn 0.2s ease-out;
    }

    @keyframes messageIn {

        from {
            opacity: 0;
            transform: translateY(5px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    /* =====================================================
       EMPTY CHAT
       ===================================================== */

    .empty-space {
        height: 120px;
    }


    /* =====================================================
       SETTINGS
       ===================================================== */

    .settings-divider {
        margin:
            1.5rem 0;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        background: white;

        border:
            1px solid var(--border);

        border-radius: 12px;

        padding: 0.25rem;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding: 1rem;
        }

        .auth-container {
            margin-top: 2rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "signup",
    "token": None,
    "user": None,
    "conversation_id": None,
    "conversations": [],
    "messages": [],
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================

def get_headers():

    return {
        "Authorization":
            f"Bearer {st.session_state.token}"
    }


def get_error_message(response, fallback):

    try:

        return response.json().get(
            "detail",
            fallback
        )

    except Exception:

        return fallback


def load_user():

    response = requests.get(
        f"{API_BASE_URL}/users/me",
        headers=get_headers(),
    )

    if response.status_code == 200:

        st.session_state.user = response.json()

        return True

    return False


def load_conversations():

    user_id = st.session_state.user["id"]

    response = requests.get(
        f"{API_BASE_URL}/users/{user_id}/conversations",
        headers=get_headers(),
    )

    if response.status_code == 200:

        st.session_state.conversations = response.json()

        return True

    return False


def create_new_conversation(title="New conversation"):

    user_id = st.session_state.user["id"]

    response = requests.post(
        f"{API_BASE_URL}/users/{user_id}/conversations",
        headers=get_headers(),
        json={
            "title": title
        },
    )

    if response.status_code == 200:

        conversation = response.json()

        st.session_state.conversation_id = (
            conversation["id"]
        )

        st.session_state.messages = []

        load_conversations()

        return True

    st.error(
        get_error_message(
            response,
            "Could not create a new conversation."
        )
    )

    return False


def load_messages(conversation_id):

    response = requests.get(
        f"{API_BASE_URL}/conversations/{conversation_id}/messages",
        headers=get_headers(),
    )

    if response.status_code == 200:

        st.session_state.messages = (
            response.json()
        )

        st.session_state.conversation_id = (
            conversation_id
        )

        return True

    st.error(
        get_error_message(
            response,
            "Could not load this conversation."
        )
    )

    return False


def logout():

    st.session_state.token = None
    st.session_state.user = None
    st.session_state.conversation_id = None
    st.session_state.conversations = []
    st.session_state.messages = []

    st.session_state.page = "login"


def login_successfully():

    if not load_user():
        st.error("Could not load your account.")
        return False

    # جلب محادثات المستخدم السابقة
    load_conversations()

    # لو عنده محادثات نفتح أحدث واحدة، لو معندوش نترك المعرف خالي ليتم إنشاؤها عند أول رسالة
    if st.session_state.conversations:
        latest_conv = st.session_state.conversations[-1]
        load_messages(latest_conv["id"])
    else:
        st.session_state.conversation_id = None
        st.session_state.messages = []

    st.session_state.page = "main"

    return True


# =========================================================
# SIGN UP
# =========================================================

if st.session_state.page == "signup":

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown(
            '<div class="auth-container">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-brand">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-icon">🎨</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-title">'
            'Color Vision Assistant'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-subtitle">'
            'A smarter way to understand visual information.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

        st.subheader("Create your account")

        name = st.text_input(
            "Name",
            placeholder="Enter your name",
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
        )

        if st.button(
            "Create account",
            type="primary",
            use_container_width=True,
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill in all fields."
                )

            else:

                response = requests.post(
                    f"{API_BASE_URL}/users",
                    json={
                        "name": name,
                        "email": email,
                        "password": password,
                    },
                )

                if response.status_code == 200:

                    st.success(
                        "Account created successfully."
                    )

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    st.error(
                        get_error_message(
                            response,
                            "Could not create your account."
                        )
                    )

        st.markdown(
            '<div class="auth-note">'
            'Already have an account?'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Sign in",
            use_container_width=True,
        ):

            st.session_state.page = "login"

            st.rerun()


# =========================================================
# LOGIN
# =========================================================

elif st.session_state.page == "login":

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown(
            '<div class="auth-container">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-brand">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-icon">🎨</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-title">'
            'Welcome back'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="auth-subtitle">'
            'Sign in to continue your visual conversations.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

        st.subheader("Sign in")

        email = st.text_input(
            "Email",
            placeholder="you@example.com",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        if st.button(
            "Sign in",
            type="primary",
            use_container_width=True,
        ):

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                response = requests.post(
                    f"{API_BASE_URL}/login",
                    json={
                        "email": email,
                        "password": password,
                    },
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.token = (
                        data["access_token"]
                    )

                    if login_successfully():

                        st.rerun()

                else:

                    st.error(
                        get_error_message(
                            response,
                            "Invalid email or password."
                        )
                    )

        st.markdown(
            '<div class="auth-note">'
            "Don't have an account?"
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Create account",
            use_container_width=True,
        ):

            st.session_state.page = "signup"

            st.rerun()


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "settings":

    st.title("Settings")

    st.caption(
        "Manage your profile and account."
    )

    st.divider()

    user = st.session_state.user

    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    st.subheader("Profile")

    st.caption(
        "Update the information associated with your account."
    )

    new_name = st.text_input(
        "Name",
        value=user["name"],
    )

    new_email = st.text_input(
        "Email",
        value=user["email"],
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your current password",
    )

    st.caption(
        "Enter your current password to save profile changes."
    )

    if st.button(
        "Save changes",
        type="primary",
        use_container_width=True,
    ):

        if not new_name or not new_email or not password:

            st.warning(
                "Name, email, and password are required."
            )

        else:

            user_id = user["id"]

            response = requests.put(
                f"{API_BASE_URL}/users/{user_id}",
                headers=get_headers(),
                json={
                    "name": new_name,
                    "email": new_email,
                    "password": password,
                },
            )

            if response.status_code == 200:

                st.session_state.user = (
                    response.json()
                )

                st.success(
                    "Your profile has been updated."
                )

                st.rerun()

            else:

                st.error(
                    get_error_message(
                        response,
                        "Could not update your profile."
                    )
                )

    st.divider()

    # -----------------------------------------------------
    # DELETE ACCOUNT
    # -----------------------------------------------------

    st.subheader("Delete account")

    st.caption(
        "Permanently delete your account and its data."
    )

    st.warning(
        "This action cannot be undone."
    )

    confirm_delete = st.checkbox(
        "I understand that deleting my account is permanent."
    )

    if st.button(
        "Delete my account",
        use_container_width=True,
    ):

        if not confirm_delete:

            st.warning(
                "Please confirm the deletion first."
            )

        else:

            user_id = st.session_state.user["id"]

            response = requests.delete(
                f"{API_BASE_URL}/users/{user_id}",
                headers=get_headers(),
            )

            if response.status_code == 200:

                logout()

                st.success(
                    "Your account has been deleted."
                )

                st.rerun()

            else:

                st.error(
                    get_error_message(
                        response,
                        "Could not delete your account."
                    )
                )

    st.divider()

    if st.button(
        "← Back to chat",
        use_container_width=True,
    ):

        st.session_state.page = "main"

        st.rerun()


# =========================================================
# MAIN CHAT
# =========================================================

elif st.session_state.page == "main":

    user = st.session_state.user

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-brand">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-title">'
            '🎨 Color Vision'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-subtitle">'
            'AI Assistant'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="new-chat-button">',
            unsafe_allow_html=True,
        )

        new_chat = st.button(
            "＋  New conversation",
            use_container_width=True,
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

        if new_chat:

            # لا ننشئ Conversation في قاعدة البيانات بمجرد الضغط على
            # "New conversation". ننتظر أول رسالة ثم ننشئها بعنوان الرسالة.
            st.session_state.conversation_id = None
            st.session_state.messages = []

            st.rerun()

        st.markdown(
            '<div class="sidebar-section">'
            'CONVERSATIONS'
            '</div>',
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # Conversations
        # -------------------------------------------------

        if not st.session_state.conversations:

            st.caption(
                "No conversations yet."
            )

        else:

            for conversation in reversed(
                st.session_state.conversations
            ):

                conversation_id = conversation["id"]

                title = conversation.get(
                    "title",
                    "Conversation",
                )

                # المحادثات القديمة التي اتعملت تلقائياً بعنوان
                # "New conversation" ممكن تكون Conversations فاضية من
                # النسخة القديمة من الواجهة، لذلك لا نعرضها في الـ sidebar.
                if not title or title == "New conversation":
                    continue

                is_current = (
                    conversation_id
                    == st.session_state.conversation_id
                )

                if is_current:

                    label = f"●  {title}"

                else:

                    label = f"   {title}"

                if st.button(
                    label,
                    key=f"conversation_{conversation_id}",
                    use_container_width=True,
                ):

                    if load_messages(
                        conversation_id
                    ):

                        st.rerun()

        # -------------------------------------------------
        # Bottom Navigation
        # -------------------------------------------------

        st.markdown(
            "<div style='height: 120px;'></div>",
            unsafe_allow_html=True,
        )

        st.divider()

        if st.button(
            "⚙  Settings",
            use_container_width=True,
        ):

            st.session_state.page = "settings"

            st.rerun()

        if st.button(
            "↪  Sign out",
            use_container_width=True,
        ):

            logout()

            st.rerun()


    # =====================================================
    # HEADER
    # =====================================================

    st.title("Color Vision Assistant")

    st.caption(
        f"Welcome back, {user['name']}"
    )

    st.divider()


    # =====================================================
    # EMPTY STATE
    # =====================================================

    if not st.session_state.messages:

        st.markdown(
            "<div class='empty-space'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "### What can I help you with?"
        )

        st.caption(
            "Ask a question, describe something you see, "
            "or upload an image for visual analysis."
        )


    # =====================================================
    # MESSAGES
    # =====================================================

    for message in st.session_state.messages:

        role = message["role"]

        content = message["content"]

        if role == "user":

            with st.chat_message(
                "user",
                avatar="👤",
            ):

                st.write(content)

        else:

            with st.chat_message(
                "assistant",
                avatar="🎨",
            ):

                st.write(content)


    # =====================================================
    # IMAGE
    # =====================================================

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
        ],
        help=(
            "Upload an image when you want "
            "the assistant to analyze it."
        ),
    )

    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Image ready to send",
            width=400,
        )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Message your assistant..."
    )

    if prompt:
        if st.session_state.conversation_id is None:
                generated_title = prompt[:30] + ("..." if len(prompt) > 30 else "")
                
                if not create_new_conversation(title=generated_title):
                    st.stop()
        with st.chat_message(
            "user",
            avatar="👤",
        ):

            st.write(prompt)

            if uploaded_image is not None:

                st.image(
                    uploaded_image,
                    width=400,
                )

        # -------------------------------------------------
        # Prepare image
        # -------------------------------------------------

        files = None

        if uploaded_image is not None:

            files = {
                "image": (
                    uploaded_image.name,
                    uploaded_image.getvalue(),
                    uploaded_image.type,
                )
            }

        # -------------------------------------------------
        # Send request
        # -------------------------------------------------

        response = requests.post(
            f"{API_BASE_URL}/conversations/"
            f"{st.session_state.conversation_id}/chat",

            headers=get_headers(),

            data={
                "message": prompt
            },

            files=files,
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        if response.status_code == 200:

            data = response.json()

            ai_response = data["ai_response"]

            with st.chat_message(
                "assistant",
                avatar="🎨",
            ):

                st.write(ai_response)

            load_messages(
                st.session_state.conversation_id
            )

            load_conversations()

            st.rerun()

        else:

            st.error(
                get_error_message(
                    response,
                    "Something went wrong while contacting the assistant."
                )
            )
            #streamlit run frontend/streamlit_app.py