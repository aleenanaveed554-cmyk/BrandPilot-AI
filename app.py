import streamlit as st
from groq import Groq
import re

# =========================================================
# BRANDPILOT AI
# =========================================================

st.set_page_config(
    page_title="BrandPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CONFIGURATION
# =========================================================

MODEL = "openai/gpt-oss-20b"

APP_NAME = "BrandPilot AI"
TAGLINE = "Your AI-Powered Marketing Assistant"


# =========================================================
# PREMIUM UI
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(104, 55, 170, 0.20),
            transparent 35%
        ),
        radial-gradient(
            circle at 0% 30%,
            rgba(76, 32, 125, 0.15),
            transparent 30%
        ),
        #09060f;
    color: white;
}

.block-container {
    max-width: 1450px;
    padding: 2rem 3rem 4rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #10091b 0%,
        #0b0711 100%
    );
    border-right: 1px solid rgba(216, 178, 76, 0.18);
}

section[data-testid="stSidebar"] * {
    color: #f6f2ff;
}

/* BRAND */

.brand-logo {
    font-family: "Space Grotesk", sans-serif;
    font-size: 27px;
    font-weight: 700;
    letter-spacing: -1px;
}

.gold {
    color: #d8b24c;
}

.tagline {
    color: #a9a2b5;
    font-size: 13px;
    margin-top: -6px;
}

/* HERO */

.hero {
    padding: 32px;
    border: 1px solid rgba(216, 178, 76, 0.20);
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(70, 31, 105, 0.60),
            rgba(18, 10, 29, 0.90)
        );

    box-shadow:
        0 20px 60px rgba(0,0,0,0.25);
}

.hero h1 {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(36px, 5vw, 60px);
    line-height: 1;
    margin: 0;
    color: white;
}

.hero p {
    color: #bdb6c9;
    max-width: 780px;
    font-size: 16px;
    margin-top: 15px;
}

/* SECTION */

.section-title {
    font-family: "Space Grotesk", sans-serif;
    color: white;
    font-size: 23px;
    font-weight: 700;
    margin: 30px 0 15px;
}

/* FEATURE CARDS */

.feature-card {
    min-height: 145px;
    padding: 20px;

    border: 1px solid rgba(216, 178, 76, 0.13);
    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(39, 20, 58, 0.90),
            rgba(17, 10, 25, 0.95)
        );

    box-shadow:
        0 12px 35px rgba(0,0,0,0.18);
}

.feature-icon {
    font-size: 25px;
}

.feature-title {
    color: white;
    font-weight: 700;
    font-size: 16px;
    margin-top: 9px;
}

.feature-desc {
    color: #9e97aa;
    font-size: 12px;
    margin-top: 5px;
}

/* RESULT CARD */

.result-card {
    padding: 24px;
    margin: 15px 0;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            #21122f,
            #120b19
        );

    border: 1px solid rgba(216, 178, 76, 0.18);
}

.result-card h3 {
    color: #d8b24c;
}

.result-text {
    color: #f1edf5;
    line-height: 1.7;
    white-space: pre-wrap;
}

/* INPUTS */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {

    background: #160d20 !important;
    color: white !important;

    border: 1px solid #3d2850 !important;

    border-radius: 12px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {

    background: #160d20 !important;
    color: white !important;

    border: 1px solid #3d2850 !important;

    border-radius: 12px !important;
}

/* LABELS */

label,
.stMarkdown p,
.stMarkdown li {
    color: #ddd6e6 !important;
}

/* BUTTONS */

.stButton > button {

    border-radius: 11px;

    border: 1px solid #d8b24c;

    background:
        linear-gradient(
            135deg,
            #d8b24c,
            #b88b25
        );

    color: #120b18 !important;

    font-weight: 700;

    min-height: 43px;

    transition: 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 10px 25px rgba(216,178,76,0.18);
}

/* DIVIDER */

hr {
    border-color: rgba(216,178,76,0.12);
}

/* HIDE FOOTER */

footer {
    visibility: hidden;
}

/* MOBILE */

@media (max-width: 900px) {

    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        padding: 22px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# API FUNCTIONS
# =========================================================

def get_api_key():

    try:
        return st.secrets["GROQ_API_KEY"]

    except Exception:
        return None


def get_client():

    api_key = get_api_key()

    if not api_key:
        return None

    return Groq(api_key=api_key)


def clean_output(text):

    if not text:
        return ""

    text = re.sub(
        r"^```(?:json|text)?\s*",
        "",
        text.strip(),
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def generate_ai(prompt, max_tokens=1800):

    client = get_client()

    if not client:

        st.error(
            "Groq API key missing. Please add GROQ_API_KEY "
            "inside .streamlit/secrets.toml"
        )

        return None

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role": "system",
                    "content": """
You are BrandPilot AI,
a professional marketing strategist,
copywriter and social media expert.

Create high-quality,
practical and professional marketing content.

Use clear headings,
structured sections,
short paragraphs,
and useful marketing language.

Avoid generic filler.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.7,

            max_completion_tokens=max_tokens
        )

        result = response.choices[0].message.content

        if not result:

            st.error("AI returned an empty response.")

            return None

        return clean_output(result)

    except Exception as e:

        error = str(e).lower()

        if "429" in error or "rate" in error:

            st.error(
                "Groq rate limit reached. "
                "Please wait a moment and try again."
            )

        elif "401" in error or "authentication" in error:

            st.error(
                "Groq authentication failed. "
                "Please check your API key."
            )

        elif "404" in error or "model" in error:

            st.error(
                f"The model '{MODEL}' is unavailable. "
                "Change the MODEL variable at the top of app.py."
            )

        else:

            st.error(
                "AI request failed. "
                "Please check your API key, model and internet connection."
            )

        return None


# =========================================================
# BRAND CONTEXT
# =========================================================

def brand_context():

    return f"""

Brand Name:
{st.session_state.get("brand_name", "")}

Product / Service:
{st.session_state.get("product", "")}

Business Description:
{st.session_state.get("business_desc", "")}

Target Audience:
{st.session_state.get("audience", "")}

Industry:
{st.session_state.get("industry", "")}

Brand Tone:
{st.session_state.get("tone", "Professional")}

Main Goal:
{st.session_state.get("goal", "")}

Platform:
{st.session_state.get("platform", "Instagram")}

"""


# =========================================================
# VALIDATION
# =========================================================

def require(value):

    if not value or not str(value).strip():

        st.warning(
            "Please enter the required information first."
        )

        return False

    return True


# =========================================================
# DOWNLOAD
# =========================================================

def download_text(filename, content):

    st.download_button(
        label="⬇️ Download",
        data=content,
        file_name=filename,
        mime="text/plain"
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-logo">
            Brand<span class="gold">Pilot</span> AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="tagline">
            Your AI-Powered Marketing Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    pages = [

        "🏠 Dashboard",

        "✍️ Caption Generator",

        "📢 Ad Copy",

        "💡 Content Ideas",

        "#️⃣ Hashtags",

        "📅 Content Calendar",

        "📝 Product Description",

        "🚀 Marketing Strategy"

    ]

    page = st.radio(
        "Navigation",
        pages,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### AI Marketing Studio")

    st.caption(
        "Create. Grow. Market Smarter."
    )

    st.caption(
        f"AI Model: {MODEL}"
    )


# =========================================================
# BRAND INFORMATION PANEL
# =========================================================

def brand_panel():

    with st.expander(
        "⚙️ Brand Information",
        expanded=False
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.session_state.brand_name = st.text_input(
                "Brand / Business Name",
                value=st.session_state.get(
                    "brand_name",
                    ""
                )
            )

            st.session_state.product = st.text_input(
                "Product or Service",
                value=st.session_state.get(
                    "product",
                    ""
                )
            )

            st.session_state.industry = st.text_input(
                "Industry",
                value=st.session_state.get(
                    "industry",
                    ""
                )
            )

        with col2:

            st.session_state.audience = st.text_input(
                "Target Audience",
                value=st.session_state.get(
                    "audience",
                    ""
                )
            )

            tones = [
                "Professional",
                "Friendly",
                "Luxury",
                "Creative",
                "Casual",
                "Minimal",
                "Persuasive"
            ]

            current_tone = st.session_state.get(
                "tone",
                "Professional"
            )

            st.session_state.tone = st.selectbox(
                "Brand Tone",
                tones,
                index=tones.index(current_tone)
            )

            st.session_state.goal = st.text_input(
                "Main Goal",
                value=st.session_state.get(
                    "goal",
                    "Increase engagement"
                )
            )

        st.session_state.business_desc = st.text_area(
            "Business Description",
            value=st.session_state.get(
                "business_desc",
                ""
            ),
            height=90
        )

        platforms = [
            "Instagram",
            "Facebook",
            "TikTok",
            "LinkedIn",
            "YouTube"
        ]

        current_platform = st.session_state.get(
            "platform",
            "Instagram"
        )

        st.session_state.platform = st.selectbox(
            "Platform",
            platforms,
            index=platforms.index(current_platform)
        )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">

            <div class="gold"
                 style="font-weight:700;letter-spacing:1px;">

                AI MARKETING STUDIO

            </div>

            <h1>
                BrandPilot AI
            </h1>

            <p>
                Your AI-Powered Marketing Assistant —
                create smarter marketing content,
                social posts, advertisements and
                content strategies in minutes.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            Everything you need to market smarter
        </div>
        """,
        unsafe_allow_html=True
    )

    cards = [

        (
            "✍️",
            "AI Caption Generator",
            "Create hooks, captions, CTAs and hashtags."
        ),

        (
            "📢",
            "Ad Copy Generator",
            "Write persuasive ads for multiple platforms."
        ),

        (
            "💡",
            "Content Ideas",
            "Turn your business into fresh content ideas."
        ),

        (
            "#️⃣",
            "Hashtag Generator",
            "Build popular, niche and branded hashtags."
        ),

        (
            "📅",
            "Content Calendar",
            "Plan consistent content with AI."
        ),

        (
            "🎨",
            "Social Media Content",
            "Generate platform-ready content."
        ),

        (
            "📝",
            "Product Description",
            "Create polished product descriptions."
        ),

        (
            "🚀",
            "Marketing Strategy",
            "Build practical marketing plans."
        )

    ]

    columns = st.columns(4)

    for i, (icon, title, desc) in enumerate(cards):

        with columns[i % 4]:

            st.markdown(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-desc">
                        {desc}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if (i + 1) % 4 == 0:

            st.markdown(
                "<div style='height:14px'></div>",
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="section-title">
            Quick Start
        </div>
        """,
        unsafe_allow_html=True
    )

    brand_panel()


# =========================================================
# CAPTION GENERATOR
# =========================================================

elif page == "✍️ Caption Generator":

    st.markdown("## ✍️ AI Caption Generator")

    st.caption(
        "Create professional captions with hooks, CTAs and hashtags."
    )

    brand_panel()

    topic = st.text_input(
        "Topic / Product",
        placeholder="e.g. New luxury skincare collection"
    )

    if st.button(
        "✨ Generate Content",
        use_container_width=True
    ):

        if require(topic):

            prompt = f"""

{brand_context()}

Topic:
{topic}

Create a professional social media caption.

Return exactly:

HOOK

CAPTION

CALL-TO-ACTION

HASHTAGS

Adapt the content to the selected platform.

Use appropriate emojis where useful.
"""

            result = generate_ai(
                prompt,
                1300
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_caption.txt",
                    result
                )


# =========================================================
# AD COPY
# =========================================================

elif page == "📢 Ad Copy":

    st.markdown("## 📢 AI Ad Copy Generator")

    st.caption(
        "Create persuasive advertising content for your business."
    )

    brand_panel()

    product = st.text_input(
        "Product / Offer",
        placeholder="e.g. Premium handmade handbags"
    )

    style = st.selectbox(
        "Ad Style",
        [
            "Professional",
            "Emotional",
            "Luxury",
            "Promotional",
            "Attention-grabbing"
        ]
    )

    if st.button(
        "🚀 Generate Ad Copy",
        use_container_width=True
    ):

        if require(product):

            prompt = f"""

{brand_context()}

Product / Offer:
{product}

Advertising Style:
{style}

Create professional advertising copy.

Include:

AD HEADLINE

PRIMARY TEXT

SHORT DESCRIPTION

CALL-TO-ACTION

TARGET AUDIENCE SUGGESTION

"""

            result = generate_ai(
                prompt,
                1400
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_ad_copy.txt",
                    result
                )


# =========================================================
# CONTENT IDEAS
# =========================================================

elif page == "💡 Content Ideas":

    st.markdown("## 💡 Content Ideas Generator")

    st.caption(
        "Generate unique social media content ideas for your business."
    )

    brand_panel()

    count = st.number_input(
        "Number of Ideas",
        min_value=3,
        max_value=15,
        value=8
    )

    if st.button(
        "💡 Generate Ideas",
        use_container_width=True
    ):

        if (
            require(
                st.session_state.get("brand_name")
            )
            and
            require(
                st.session_state.get("product")
            )
        ):

            prompt = f"""

{brand_context()}

Generate {count} unique social media content ideas.

For every idea include:

CONTENT TITLE

CONTENT TYPE

SHORT CONCEPT

SUGGESTED PLATFORM

SUGGESTED CTA

Keep every idea different,
creative and practical.

"""

            result = generate_ai(
                prompt,
                1800
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_content_ideas.txt",
                    result
                )


# =========================================================
# HASHTAGS
# =========================================================

elif page == "#️⃣ Hashtags":

    st.markdown("## #️⃣ Hashtag Generator")

    st.caption(
        "Generate relevant hashtags for reach, niche discovery and branding."
    )

    brand_panel()

    keyword = st.text_input(
        "Brand / Product / Keyword",
        placeholder="e.g. handmade jewelry"
    )

    if st.button(
        "🔎 Generate Hashtags",
        use_container_width=True
    ):

        if require(keyword):

            prompt = f"""

{brand_context()}

Keyword:
{keyword}

Generate relevant hashtags.

Separate them into:

POPULAR

NICHE

BRANDED

Give 10 hashtags for each category.

Avoid irrelevant and spammy hashtags.

"""

            result = generate_ai(
                prompt,
                1200
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_hashtags.txt",
                    result
                )


# =========================================================
# CONTENT CALENDAR
# =========================================================

elif page == "📅 Content Calendar":

    st.markdown("## 📅 AI Content Calendar")

    st.caption(
        "Create a structured publishing plan for your selected platform."
    )

    brand_panel()

    col1, col2 = st.columns(2)

    with col1:

        days = st.number_input(
            "Number of Days",
            min_value=3,
            max_value=30,
            value=7
        )

    with col2:

        calendar_goal = st.selectbox(
            "Content Goal",
            [
                "Engagement",
                "Awareness",
                "Leads",
                "Sales",
                "Community Growth"
            ]
        )

    if st.button(
        "📅 Generate Calendar",
        use_container_width=True
    ):

        if (
            require(
                st.session_state.get("brand_name")
            )
            and
            require(
                st.session_state.get("product")
            )
        ):

            prompt = f"""

{brand_context()}

Create a {days}-day content calendar.

Content Goal:
{calendar_goal}

For every day include:

DAY

POST TOPIC

CONTENT TYPE

CAPTION IDEA

CTA

HASHTAGS

Keep the plan varied,
realistic and platform-specific.

"""

            result = generate_ai(
                prompt,
                2200
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_content_calendar.txt",
                    result
                )


# =========================================================
# PRODUCT DESCRIPTION
# =========================================================

elif page == "📝 Product Description":

    st.markdown("## 📝 Product Description Generator")

    st.caption(
        "Turn product information into professional sales copy."
    )

    brand_panel()

    product_name = st.text_input(
        "Product Name"
    )

    features = st.text_area(
        "Product Details / Features",
        height=150,
        placeholder="""
Materials, size, benefits,
special features, price range,
unique selling points...
"""
    )

    if st.button(
        "📝 Generate Description",
        use_container_width=True
    ):

        if require(product_name) and require(features):

            prompt = f"""

{brand_context()}

Product Name:
{product_name}

Product Details:
{features}

Generate:

SHORT PRODUCT DESCRIPTION

PROFESSIONAL PRODUCT DESCRIPTION

E-COMMERCE DESCRIPTION

SOCIAL MEDIA DESCRIPTION

KEY SELLING POINTS

Do not invent technical facts
that were not provided.

"""

            result = generate_ai(
                prompt,
                1700
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_product_description.txt",
                    result
                )


# =========================================================
# MARKETING STRATEGY
# =========================================================

elif page == "🚀 Marketing Strategy":

    st.markdown("## 🚀 AI Marketing Strategy")

    st.caption(
        "Build a focused marketing roadmap for your business."
    )

    brand_panel()

    plan_length = st.radio(
        "Plan Length",
        [
            "7-Day Plan",
            "30-Day Plan"
        ],
        horizontal=True
    )

    if st.button(
        "🚀 Generate Marketing Strategy",
        use_container_width=True
    ):

        if (
            require(
                st.session_state.get("brand_name")
            )
            and
            require(
                st.session_state.get("product")
            )
        ):

            prompt = f"""

{brand_context()}

Create a {plan_length} marketing strategy.

Include:

1. TARGET AUDIENCE

2. MARKETING GOALS

3. CONTENT PILLARS

4. RECOMMENDED PLATFORMS

5. CONTENT STRATEGY

6. ENGAGEMENT STRATEGY

7. CALL-TO-ACTION STRATEGY

8. {plan_length.upper()} CONTENT PLAN

Make the strategy practical
for a small business or creator.

Align everything with the
business goal and selected platform.

"""

            result = generate_ai(
                prompt,
                2400
            )

            if result:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-text">
                            {result}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                download_text(
                    "brandpilot_marketing_strategy.txt",
                    result
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    "<br><hr>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#81798c;
        font-size:12px;
    ">
        BrandPilot AI • Create. Grow. Market Smarter.
    </div>
    """,
    unsafe_allow_html=True
)
