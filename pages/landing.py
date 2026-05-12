import streamlit as st

HERO_IMG   = "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=700&q=80"
APPT_IMG   = "https://images.unsplash.com/photo-1584515933487-779824d29309?w=600&q=80"
NURSE_IMG  = "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=600&q=80"
PRICE_IMG  = "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=600&q=80"
BLOG_IMG_1 = "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=500&q=80"
BLOG_IMG_2 = "https://images.unsplash.com/photo-1530026405186-ed1f139313f3?w=500&q=80"
BLOG_IMG_3 = "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=500&q=80"


def show():
    st.markdown("""
    <style>
    *, *::before, *::after { box-sizing: border-box; }
    .block-container, .stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }

    /* HERO */
    .hero-section {
        background: linear-gradient(150deg, #063d34 0%, #0a8a74 45%, #0fbfa0 100%);
        padding: 2.5rem 1.2rem 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 6px 28px rgba(10,138,116,0.22);
        margin-bottom: 1.5rem;
        min-height: 70vh;
        align-items: center;
        justify-content: center;
    }
    .hero-text { width: 100%; order: 2; }
    .hero-img-wrap { width: 100%; order: 1; }
    .hero-img-wrap img {
        width: 100%; height: 220px; object-fit: cover;
        object-position: top center; border-radius: 16px;
        box-shadow: 0 10px 32px rgba(0,0,0,0.22); display: block;
    }
    .hero-badge {
        background: rgba(255,255,255,0.22); color: #fff;
        border-radius: 20px; padding: 5px 16px; font-size: 0.75rem;
        font-weight: 700; display: inline-block; margin-bottom: 0.9rem;
        letter-spacing: 1.2px; border: 1px solid rgba(255,255,255,0.3);
    }
    .hero-text h1 {
        font-size: 1.75rem; font-weight: 800; color: #fff;
        line-height: 1.25; margin: 0 0 0.9rem 0;
    }
    .hero-text p {
        font-size: 0.92rem; color: rgba(255,255,255,0.85);
        line-height: 1.7; margin-bottom: 1.4rem;
    }
    .hero-btns { display: flex; flex-wrap: wrap; gap: 0.75rem; }
    .hero-btn {
        background: #fff; color: #0a8a74; border-radius: 30px;
        padding: 11px 26px; font-size: 0.9rem; font-weight: 700;
        text-decoration: none; display: inline-block;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12); transition: all 0.2s;
        white-space: nowrap;
    }
    .hero-btn:hover { background: #e6faf6; transform: translateY(-2px); }
    .hero-btn-outline {
        background: rgba(255,255,255,0.12); color: #fff;
        border: 2px solid rgba(255,255,255,0.6); border-radius: 30px;
        padding: 9px 22px; font-size: 0.9rem; font-weight: 600;
        text-decoration: none; display: inline-block; transition: all 0.2s;
        white-space: nowrap;
    }
    .hero-stats { display: flex; flex-wrap: wrap; gap: 1.2rem; margin-top: 1.5rem; }
    .hero-stat span { font-size: 1.35rem; font-weight: 800; color: #fff; display: block; }
    .hero-stat p    { font-size: 0.72rem; color: rgba(255,255,255,0.72); margin: 0; }

    /* SECTION LABELS */
    .section-tag {
        color: #0a8a74; font-size: 0.72rem; font-weight: 700;
        letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 0.4rem;
    }
    .section-title {
        font-size: 1.55rem; font-weight: 800; color: #1a2e2b;
        margin: 0 0 0.6rem 0; line-height: 1.3;
    }
    .section-sub { font-size: 0.9rem; color: #6b7b78; margin-bottom: 1.4rem; line-height: 1.65; }

    /* FEATURE ROW */
    .feat-row {
        display: flex; flex-direction: column; gap: 1.5rem;
        padding: 2rem 1.2rem; background: #fff;
        border-radius: 20px; box-shadow: 0 2px 18px rgba(0,0,0,0.06); margin: 1rem 0;
        min-height: 70vh;
        align-items: center;
        justify-content: center;
    }
    .feat-row.reverse { background: #f4fdf9; }
    .feat-img img {
        width: 100%; height: 220px; object-fit: cover;
        border-radius: 14px; box-shadow: 0 6px 20px rgba(0,0,0,0.10); display: block;
    }
    .feat-content ul { padding-left: 0; list-style: none; margin: 0; }
    .feat-content ul li {
        padding: 0.4rem 0; font-size: 0.9rem; color: #3a4a47;
        display: flex; align-items: flex-start; gap: 0.6rem;
    }
    .feat-content ul li::before {
        content: "\2714"; color: #0a8a74; font-weight: 700; flex-shrink: 0; margin-top: 1px;
    }

    /* 4-CARD GRID */
    .cards-grid { display: grid; grid-template-columns: 1fr; gap: 0.9rem; margin-top: 1rem; }
    @media (min-width: 480px) { .cards-grid { grid-template-columns: 1fr 1fr; } }
    .mini-card {
        background: #fff; border-radius: 14px; padding: 1rem 1.1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06); border-left: 4px solid #0a8a74;
    }
    .mini-card .icon  { font-size: 1.3rem; margin-bottom: 0.4rem; display: block; }
    .mini-card h4     { font-size: 0.88rem; font-weight: 700; color: #1a2e2b; margin: 0 0 0.35rem 0; }
    .mini-card p      { font-size: 0.78rem; color: #6b7b78; margin: 0; line-height: 1.5; }

    /* BLOG */
    .blog-section-header { text-align: center; margin: 2rem 0 1.2rem; padding: 0 1.2rem; }
    .blog-section-wrapper { display: flex; flex-direction: column; justify-content: center; padding: 2rem 0; }
    .blog-grid { display: grid; grid-template-columns: 1fr; gap: 1.2rem; padding: 0 1.2rem; }
    .blog-card {
        background: #fff; border-radius: 16px; overflow: hidden;
        box-shadow: 0 2px 14px rgba(0,0,0,0.07); transition: transform 0.2s, box-shadow 0.2s;
    }
    .blog-card:hover { transform: translateY(-4px); box-shadow: 0 8px 28px rgba(0,0,0,0.12); }
    .blog-card img { width: 100%; height: 180px; object-fit: cover; display: block; }
    .blog-card-body { padding: 1.1rem; }
    .blog-tag {
        color: #0a8a74; font-size: 0.68rem; font-weight: 700;
        letter-spacing: 1.8px; text-transform: uppercase;
    }
    .blog-card-body h4 {
        font-size: 0.96rem; font-weight: 700; color: #1a2e2b;
        margin: 0.4rem 0 0.5rem; line-height: 1.4;
    }
    .blog-card-body p  { font-size: 0.82rem; color: #6b7b78; line-height: 1.6; margin-bottom: 0.8rem; }
    .read-more { color: #0a8a74; font-size: 0.82rem; font-weight: 700; text-decoration: none; }
    .read-more:hover { text-decoration: underline; }

    /* CTA STRIP */
    .cta-strip {
        background: linear-gradient(135deg, #063d34, #0a8a74 60%, #0fbfa0);
        border-radius: 20px; padding: 2rem 1.5rem; text-align: center;
        margin: 2rem 1.2rem 1rem; box-shadow: 0 8px 28px rgba(10,138,116,0.22);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .cta-strip h2 { color: #fff; font-size: 1.35rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.3; }
    .cta-strip p  { color: rgba(255,255,255,0.82); font-size: 0.9rem; margin-bottom: 0; }

    /* FOOTER */
    .site-footer {
        text-align: center; padding: 1.5rem 1rem; color: #aaa;
        font-size: 0.78rem; border-top: 1px solid #e8f5f2; margin-top: 1.5rem;
    }

    /* TABLET >= 640px */
    @media (min-width: 640px) {
        .hero-section { padding: 3rem 2.5rem 2.5rem; flex-direction: row; align-items: center; gap: 2rem; }
        .hero-text { order: 1; flex: 1.2; }
        .hero-img-wrap { order: 2; flex: 1; }
        .hero-img-wrap img { height: 300px; }
        .hero-text h1 { font-size: 2.1rem; }
        .feat-row { flex-direction: row; align-items: center; padding: 2.5rem 2rem; gap: 2.5rem; min-height: 60vh; }
        .feat-row.reverse { flex-direction: row-reverse; }
        .feat-content { flex: 1.3; }
        .feat-img { flex: 1; }
        .feat-img img { height: 260px; }
        .blog-grid { grid-template-columns: 1fr 1fr; padding: 0 1.5rem; }
        .blog-section-header { padding: 0 1.5rem; }
        .section-title { font-size: 1.8rem; }
        .cta-strip { padding: 2.5rem 3rem; margin: 2rem 1.5rem 1rem; }
        .cta-strip h2 { font-size: 1.65rem; }
        .block-container, .stMainBlockContainer { padding: 0 1rem !important; }
    }

    /* DESKTOP >= 1024px */
    @media (min-width: 1024px) {
        .block-container, .stMainBlockContainer { max-width: 1440px !important; width: 100% !important; margin: 0 auto !important; padding: 0 2rem !important; }
        .hero-section { padding: 4rem 3.5rem 3.5rem; border-radius: 0 0 32px 32px; gap: 3rem; min-height: 85vh; }
        .hero-img-wrap img { height: 380px; max-width: 420px; }
        .hero-text h1 { font-size: 2.75rem; }
        .hero-text p  { font-size: 1.05rem; }
        .feat-row { gap: 3.5rem; padding: 3rem 2.5rem; min-height: 75vh; }
        .feat-img img { height: 300px; }
        .section-title { font-size: 2.1rem; }
        .blog-grid { grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; padding: 0 2rem; }
        .blog-section-header { margin: 3rem 0 1.5rem; padding: 0 2rem; }
        .cta-strip { margin: 3rem 0 1.5rem; padding: 3rem 4rem; }
        .cta-strip h2 { font-size: 1.9rem; }
    }

    #MainMenu, footer, header { visibility: hidden; }
    div[data-testid="stVerticalBlock"] > div > div > div > button { display: none; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-text">
            <div class="hero-badge">AI-POWERED HEALTHCARE</div>
            <h1>Early Kidney Disease Detection &amp; Management</h1>
            <p>MLPKD leverages state-of-the-art machine learning to help clinicians
            detect chronic kidney disease early, track patient health trends, and
            make confident, data-driven decisions — all in one unified platform.</p>
            <div class="hero-btns">
                <a class="hero-btn" href="?page=signin">Get Started Free</a>
                <a class="hero-btn-outline" href="?page=about">Learn More</a>
            </div>
            <div class="hero-stats">
                <div class="hero-stat"><span>97%</span><p>Model Accuracy</p></div>
                <div class="hero-stat"><span>4</span><p>User Roles</p></div>
                <div class="hero-stat"><span>Real-Time</span><p>Predictions</p></div>
            </div>
        </div>
        <div class="hero-img-wrap">
            <img src="{HERO_IMG}" alt="Doctor"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _b1, _b2, _b3 = st.columns([2, 1, 1])
    with _b2:
        if st.button("Sign In", use_container_width=True, type="primary"):
            st.session_state.page = "signin"
            st.rerun()
    with _b3:
        if st.button("Register", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

    st.markdown(f"""
    <div class="feat-row">
        <div class="feat-content">
            <div class="section-tag">WHY MLPKD</div>
            <h2 class="section-title">Smart Clinical Decision Support</h2>
            <p class="section-sub">Our platform combines the precision of AI with clinical
            expertise to deliver fast, reliable predictions at the point of care.</p>
            <ul>
                <li>Instant CKD risk scoring from lab values &amp; vitals</li>
                <li>99% uptime with real-time processing</li>
                <li>Secure, role-based patient record management</li>
                <li>Visual trend analytics for longitudinal care</li>
            </ul>
        </div>
        <div class="feat-img"><img src="{APPT_IMG}" alt="Clinical team"/></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feat-row reverse">
        <div class="feat-img"><img src="{NURSE_IMG}" alt="Nurse"/></div>
        <div style="flex:1.4">
            <div class="section-tag">PLATFORM FEATURES</div>
            <h2 class="section-title">Everything Your Clinical Team Needs</h2>
            <div class="cards-grid">
                <div class="mini-card"><span class="icon">&#128300;</span><h4>ML Predictions</h4><p>XGBoost-powered CKD risk with confidence scores.</p></div>
                <div class="mini-card"><span class="icon">&#128202;</span><h4>Rich Analytics</h4><p>Population-level charts, trends and outcome tracking.</p></div>
                <div class="mini-card"><span class="icon">&#128101;</span><h4>Multi-Role Access</h4><p>Portals for doctors, nurses, lab techs &amp; patients.</p></div>
                <div class="mini-card"><span class="icon">&#128274;</span><h4>Secure &amp; Compliant</h4><p>Role-based access with session-level data isolation.</p></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feat-row">
        <div class="feat-content">
            <div class="section-tag">OPEN ACCESS</div>
            <h2 class="section-title">Accessible for Every Healthcare Setting</h2>
            <p class="section-sub">Deployable in community clinics, district hospitals and
            large teaching centres. No expensive hardware required.</p>
            <ul>
                <li>Runs on any device with a browser</li>
                <li>Lightweight — no GPU required for inference</li>
                <li>Easy onboarding for new staff in under 5 minutes</li>
            </ul>
        </div>
        <div class="feat-img"><img src="{PRICE_IMG}" alt="Doctor"/></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="blog-section-wrapper">
        <div class="blog-section-header">
            <div class="section-tag" style="display:inline-block">HEALTH KNOWLEDGE</div>
            <h2 class="section-title">Clinical Tips &amp; Insights</h2>
            <p class="section-sub" style="max-width:520px;margin:0 auto">
                Evidence-based guidance for kidney health management.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="blog-grid">
        <div class="blog-card">
            <img src="{BLOG_IMG_1}" alt="Prevention"/>
            <div class="blog-card-body">
                <div class="blog-tag">Prevention</div>
                <h4>Early Signs of Kidney Disease You Shouldn't Ignore</h4>
                <p>Fatigue, swelling and changes in urination can be early indicators.</p>
                <a class="read-more" href="#">Read more &#8594;</a>
            </div>
        </div>
        <div class="blog-card">
            <img src="{BLOG_IMG_2}" alt="Nutrition"/>
            <div class="blog-card-body">
                <div class="blog-tag">Nutrition</div>
                <h4>Dietary Recommendations for CKD Patients</h4>
                <p>Managing protein, potassium and sodium intake slows CKD progression.</p>
                <a class="read-more" href="#">Read more &#8594;</a>
            </div>
        </div>
        <div class="blog-card">
            <img src="{BLOG_IMG_3}" alt="Technology"/>
            <div class="blog-card-body">
                <div class="blog-tag">Technology</div>
                <h4>How AI is Transforming Nephrology Care</h4>
                <p>ML is reshaping how clinicians approach kidney disease management.</p>
                <a class="read-more" href="#">Read more &#8594;</a>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-strip">
        <h2>Ready to Transform Your Clinical Workflow?</h2>
        <p>Join MLPKD today — free for all healthcare professionals.</p>
    </div>
    """, unsafe_allow_html=True)

    _c1, _c2, _c3 = st.columns([1.5, 1, 1])
    with _c2:
        if st.button("Sign In Now", use_container_width=True, type="primary"):
            st.session_state.page = "signin"
            st.rerun()
    with _c3:
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

    st.markdown("""
    <div class="site-footer">
        &copy; 2026 MLPKD &nbsp;&middot;&nbsp; ML-Powered Kidney Disease Platform
        &nbsp;&middot;&nbsp; Built with Streamlit &amp; scikit-learn
    </div>
    """, unsafe_allow_html=True)
