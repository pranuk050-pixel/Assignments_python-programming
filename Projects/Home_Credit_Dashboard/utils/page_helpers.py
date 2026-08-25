import pandas as pd
import streamlit as st

from utils.data_loader import load_data
from utils.filters import sidebar_filters
from utils.preprocessing import prepare_data


PAGE_HEADING_COLORS = {
    "Executive Overview": "#FFD700",
    "Sales Analysis": "#00C853",
    "Profit Analysis": "#FF7043",
    "Regional Analysis": "#00FFFF",
    "State Analysis": "#9C27B0",
    "City Analysis": "#00BFFF",
    "Category Analysis": "#C6FF00",
    "SubCategory Analysis": "#FF6EC7",
    "Product Analysis": "#C0C0C0",
    "Customer Analysis": "#D81B60",
    "Segment Analysis": "#00C853",
    "Order Analysis": "#FF7043",
    "Shipping Analysis": "#00BFFF",
    "Discount Analysis": "#FFD700",
    "Loss Analysis": "#FF6EC7",
    "Time Series": "#00FFFF",
    "Growth Analysis": "#C6FF00",
    "Sales vs Profit": "#9C27B0",
    "Top Bottom": "#D81B60",
    "Data Explorer": "#C0C0C0",
}

PAGE_ICONS = {
    "Executive Overview": "📊",
    "Sales Analysis": "💰",
    "Profit Analysis": "📈",
    "Regional Analysis": "🌍",
    "State Analysis": "🗺️",
    "City Analysis": "🏙️",
    "Category Analysis": "🗂️",
    "SubCategory Analysis": "📦",
    "Product Analysis": "🧾",
    "Customer Analysis": "👥",
    "Segment Analysis": "🎯",
    "Order Analysis": "🛒",
    "Shipping Analysis": "🚚",
    "Discount Analysis": "🏷️",
    "Loss Analysis": "⚠️",
    "Time Series": "🕒",
    "Growth Analysis": "📊",
    "Sales vs Profit": "💹",
    "Top Bottom": "🏆",
    "Data Explorer": "🔎",
}

SIDEBAR_PAGE_PATHS = {
    "Executive Overview": "pages/01_Executive_Overview.py",
    "Sales Analysis": "pages/02_Sales_Analysis.py",
    "Profit Analysis": "pages/03_Profit_Analysis.py",
    "Regional Analysis": "pages/04_Regional_Analysis.py",
    "State Analysis": "pages/05_State_Analysis.py",
    "City Analysis": "pages/06_City_Analysis.py",
    "Category Analysis": "pages/07_Category_Analysis.py",
    "SubCategory Analysis": "pages/08_SubCategory_Analysis.py",
    "Product Analysis": "pages/09_Product_Analysis.py",
    "Customer Analysis": "pages/10_Customer_Analysis.py",
    "Segment Analysis": "pages/11_Segment_Analysis.py",
    "Order Analysis": "pages/12_Order_Analysis.py",
    "Shipping Analysis": "pages/13_Shipping_Analysis.py",
    "Discount Analysis": "pages/14_Discount_Analysis.py",
    "Loss Analysis": "pages/15_Loss_Analysis.py",
    "Time Series": "pages/16_Time_Series.py",
    "Growth Analysis": "pages/17_Growth_Analysis.py",
    "Sales vs Profit": "pages/18_Sales_vs_Profit.py",
    "Top Bottom": "pages/19_Top_Bottom.py",
    "Data Explorer": "pages/20_Data_Explorer.py",
}


def hex_to_rgba(hex_color, alpha=1.0):
    """Convert a hex color to rgba CSS string."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = ''.join(ch * 2 for ch in hex_color)
    if len(hex_color) != 6:
        return f"rgba(255, 255, 255, {alpha})"

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def apply_dashboard_theme(page_title=None):
    """Apply page-specific background, heading, and selection accents."""

    heading_color = PAGE_HEADING_COLORS.get(page_title, "#2563EB")
    accent_soft = hex_to_rgba(heading_color, 0.18)
    accent_glow = hex_to_rgba(heading_color, 0.35)
    accent_lite = hex_to_rgba(heading_color, 0.12)

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Montserrat:wght@600;700;800;900&family=Nunito+Sans:wght@400;600;700;800&family=Poppins:wght@500;600;700;800&family=Roboto:wght@400;500;700&display=swap');

        :root {{
            --page-accent: {heading_color};
            --page-accent-soft: {accent_soft};
            --page-accent-glow: {accent_glow};
            --page-accent-lite: {accent_lite};
            --sidebar-bg: linear-gradient(180deg, #101828 0%, #0f172a 100%);
            --panel-bg: rgba(15, 23, 42, 0.78);
            --panel-border: rgba(148, 163, 184, 0.22);
            --page-bg-top: #f5fcff;
            --page-bg-mid: #e3f4fc;
            --page-bg-bottom: #c5e6f5;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            font-family: "Roboto", sans-serif;
            background: #eaf8ff !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background:
                linear-gradient(180deg, #d9f2ff 0%, #f3fbff 42%, #c8eaf7 100%) !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            min-height: 100vh;
            background:
                radial-gradient(circle at 15% 15%, rgba(255,255,255,0.86) 0%, transparent 18%),
                radial-gradient(circle at 85% 20%, rgba(255,255,255,0.68) 0%, transparent 14%),
                radial-gradient(circle at 50% 90%, rgba(255,255,255,0.52) 0%, transparent 20%),
                linear-gradient(135deg, var(--page-bg-top) 0%, var(--page-bg-mid) 44%, var(--page-bg-bottom) 100%) !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stAppViewContainer"] > .main .block-container {{
            background: linear-gradient(180deg, rgba(247, 253, 255, 0.78), rgba(205, 235, 248, 0.5));
            background-attachment: fixed;
            box-shadow: 0 0 55px rgba(76, 181, 230, 0.2);
        }}

        [data-testid="stAppViewContainer"] > .main::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background: linear-gradient(120deg, rgba(255,255,255,0.38), transparent 42%, rgba(125,211,252,0.14));
            z-index: 0;
        }}

        [data-testid="stAppViewContainer"] > .main > div {{
            position: relative;
            z-index: 1;
        }}

        [data-testid="stPlotlyChart"] {{
            margin: 0.45rem 0 1rem;
            padding: 0.35rem;
            border: 1px solid rgba(100, 116, 139, 0.48);
            border-radius: 14px;
            background: rgba(14, 17, 23, 0.22);
            box-shadow: 0 8px 22px rgba(13, 27, 42, 0.16), 0 0 12px rgba(0, 191, 255, 0.08);
            overflow: hidden;
        }}

        [data-testid="stHeader"] {{
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(8px);
        }}

        section[data-testid="stSidebar"] > div {{
            background:
                radial-gradient(circle at 20% 8%, rgba(255, 255, 255, 0.82) 0%, transparent 22%),
                linear-gradient(180deg, #FFFDE7 0%, #FFF8C9 52%, #F7E9A5 100%);
            padding-top: 0.35rem;
            border-right: 1px solid #E5C84A;
            box-shadow: inset -1px 0 0 rgba(255,255,255,0.82), 4px 0 22px rgba(202, 138, 4, 0.18);
        }}

        nav[data-testid="stSidebarNav"] {{
            padding: 1rem 0.35rem 1.25rem;
            display: none;
        }}

        .sidebar-nav-heading {{
            position: sticky;
            top: 0;
            z-index: 5;
            margin: 0.15rem 0.55rem 0.55rem;
            padding: 0.55rem 0.7rem;
            border-radius: 10px;
            background: linear-gradient(100deg, #FFF9C4, #FFF176);
            border: 1px solid #E5C84A;
            color: #0D1B2A !important;
            font-family: "Poppins", sans-serif;
            font-size: 0.92rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            text-shadow: 0 1px 0 rgba(255,255,255,0.75);
            box-shadow: 0 4px 14px rgba(202, 138, 4, 0.18);
        }}

        section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            min-height: 3rem;
            background: linear-gradient(100deg, #FFFDE7, #FFF59D) !important;
            border: 2px solid #C89B00 !important;
            border-radius: 12px !important;
            color: #0D1B2A !important;
            font-family: "Poppins", sans-serif !important;
            font-size: 0.98rem !important;
            font-weight: 800 !important;
            box-shadow: 0 5px 16px rgba(202, 138, 4, 0.2), 0 0 12px rgba(255, 245, 157, 0.52);
            transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
        }}

        section[data-testid="stSidebar"] [data-testid="stSelectbox"] {{
            position: sticky;
            top: 3.6rem;
            z-index: 4;
            margin: 0 0.25rem 0.8rem;
            padding: 0.18rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.4);
            box-shadow: 0 4px 14px rgba(202, 138, 4, 0.12);
        }}

        section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {{
            border-color: #FFAB91 !important;
            box-shadow: 0 7px 20px rgba(255, 171, 145, 0.32), 0 0 18px rgba(255, 245, 157, 0.8);
            transform: translateY(-1px);
        }}

        section[data-testid="stSidebar"] [role="listbox"],
        section[data-testid="stSidebar"] [role="option"] {{
            background: #FFFDE7 !important;
            color: #0D1B2A !important;
            font-family: "Poppins", sans-serif !important;
            font-weight: 700 !important;
        }}

        section[data-testid="stSidebar"] [role="option"]:hover,
        section[data-testid="stSidebar"] [aria-selected="true"] {{
            background: #FFF59D !important;
            color: #0D1B2A !important;
        }}

        nav[data-testid="stSidebarNav"]::before {{
            content: "Analysis Navigation";
            display: block;
            margin: 0 0.55rem 0.7rem;
            padding: 0.2rem 0.2rem 0.55rem;
            color: #FFF9C4;
            font-family: "Poppins", sans-serif;
            font-size: 1rem;
            font-weight: 900;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            text-shadow: 0 2px 0 #0D1B2A, 0 0 10px rgba(255, 249, 196, 0.42);
            border-bottom: 1px solid rgba(255, 249, 196, 0.28);
        }}

        nav[data-testid="stSidebarNav"] a {{
            position: relative;
            background: linear-gradient(100deg, rgba(255, 255, 255, 0.7), rgba(255, 241, 118, 0.24)) !important;
            border: 1px solid rgba(190, 150, 18, 0.24);
            border-left: 3px solid var(--nav-accent, #C89B00);
            border-radius: 12px;
            margin: 0.24rem 0.25rem;
            padding: 0.58rem 0.72rem;
            color: #0D1B2A !important;
            font-family: "Poppins", sans-serif;
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 0.015em;
            line-height: 1.25;
            text-shadow: 1px 1px 0 #0D1B2A, 2px 2px 0 #0D1B2A, 0 0 8px rgba(255, 241, 118, 0.46);
            box-shadow: 0 4px 12px rgba(111, 83, 0, 0.12), 0 0 14px rgba(255, 193, 7, 0.12);
            transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
            display: flex;
            align-items: center;
            gap: 11px;
            min-height: 2.55rem;
        }}

        nav[data-testid="stSidebarNav"] a::before {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.72rem;
            min-width: 1.72rem;
            height: 1.72rem;
            text-align: center;
            font-size: 1.02rem;
            line-height: 1;
            opacity: 1;
            border-radius: 8px;
            background: linear-gradient(145deg, var(--nav-icon, rgba(125, 211, 252, 0.28)), rgba(255,255,255,0.10));
            border: 1px solid rgba(255,255,255,0.24);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.18), 0 0 10px var(--nav-glow, rgba(125, 211, 252, 0.16));
            filter: drop-shadow(0 0 4px var(--nav-glow, rgba(125, 211, 252, 0.12)));
        }}

        nav[data-testid="stSidebarNav"] a:hover {{
            background: linear-gradient(100deg, #FFF176, #FFE082) !important;
            border-color: #C89B00;
            color: #FFFFFF !important;
            transform: translateX(4px);
            box-shadow: 0 8px 18px var(--nav-glow, rgba(14, 116, 144, 0.22)), 0 0 18px var(--nav-glow, rgba(125, 211, 252, 0.16));
        }}

        nav[data-testid="stSidebarNav"] a:hover span,
        nav[data-testid="stSidebarNav"] a:hover p {{
            color: #FFFFFF !important;
            text-shadow: 0 2px 0 #0D1B2A, 0 0 10px rgba(255, 255, 255, 0.64);
        }}

        nav[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: var(--nav-hover, linear-gradient(100deg, rgba(125, 211, 252, 0.30), rgba(96, 165, 250, 0.16)));
            border-color: var(--nav-accent, #67e8f9);
            border-left-color: var(--nav-accent, #67e8f9);
            box-shadow: 0 8px 22px var(--nav-glow, rgba(14, 116, 144, 0.2)), inset 0 0 0 1px rgba(255,255,255,0.24);
            color: #FFF176 !important;
            text-shadow: 0 2px 0 #0D1B2A, 1px 0 0 #0D1B2A, -1px 0 0 #0D1B2A, 0 0 12px rgba(255, 249, 196, 0.62);
        }}

        nav[data-testid="stSidebarNav"] a span,
        nav[data-testid="stSidebarNav"] a p {{
            color: #0D1B2A !important;
            font-weight: 800 !important;
            background: rgba(255, 241, 118, 0.72);
            border-radius: 6px;
            padding: 0.12rem 0.38rem;
            text-shadow: 1px 1px 0 #0D1B2A, 2px 2px 0 #0D1B2A, 0 0 8px rgba(255, 241, 118, 0.46);
        }}

        nav[data-testid="stSidebarNav"] a:hover span,
        nav[data-testid="stSidebarNav"] a:hover p {{
            color: #FFFFFF !important;
            background: rgba(13, 27, 42, 0.22);
            text-shadow: 0 1px 0 #0D1B2A, 0 0 9px rgba(255,255,255,0.68);
        }}

        nav[data-testid="stSidebarNav"] a[aria-current="page"]::before {{
            background: linear-gradient(145deg, #67e8f9, #60a5fa);
            border-color: rgba(255,255,255,0.55);
            box-shadow: 0 0 14px rgba(103, 232, 249, 0.35);
        }}

        nav[data-testid="stSidebarNav"] a[href$="/app"] {{ --nav-bg: linear-gradient(100deg, #dbeafe, #bfdbfe); --nav-hover: linear-gradient(100deg, #eff6ff, #bae6fd); --nav-accent: #2563eb; --nav-text: #0f172a; --nav-icon: #60a5fa; --nav-glow: rgba(96, 165, 250, 0.38); }}
        nav[data-testid="stSidebarNav"] a[href$="/Executive_Overview"] {{ --nav-bg: linear-gradient(100deg, #d1fae5, #a7f3d0); --nav-hover: linear-gradient(100deg, #ecfdf5, #86efac); --nav-accent: #059669; --nav-text: #064e3b; --nav-icon: #34d399; --nav-glow: rgba(52, 211, 153, 0.34); }}
        nav[data-testid="stSidebarNav"] a[href$="/Sales_Analysis"] {{ --nav-bg: linear-gradient(100deg, #fef3c7, #fde68a); --nav-hover: linear-gradient(100deg, #fffbeb, #fcd34d); --nav-accent: #d97706; --nav-text: #78350f; --nav-icon: #fbbf24; --nav-glow: rgba(251, 191, 36, 0.38); }}
        nav[data-testid="stSidebarNav"] a[href$="/Profit_Analysis"] {{ --nav-bg: linear-gradient(100deg, #fee2e2, #fecaca); --nav-hover: linear-gradient(100deg, #fff1f2, #fda4af); --nav-accent: #e11d48; --nav-text: #881337; --nav-icon: #fb7185; --nav-glow: rgba(251, 113, 133, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Regional_Analysis"] {{ --nav-bg: linear-gradient(100deg, #cffafe, #a5f3fc); --nav-hover: linear-gradient(100deg, #ecfeff, #67e8f9); --nav-accent: #0891b2; --nav-text: #164e63; --nav-icon: #22d3ee; --nav-glow: rgba(34, 211, 238, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/State_Analysis"] {{ --nav-bg: linear-gradient(100deg, #ede9fe, #ddd6fe); --nav-hover: linear-gradient(100deg, #f5f3ff, #c4b5fd); --nav-accent: #7c3aed; --nav-text: #4c1d95; --nav-icon: #a78bfa; --nav-glow: rgba(167, 139, 250, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/City_Analysis"] {{ --nav-bg: linear-gradient(100deg, #dbeafe, #bfdbfe); --nav-hover: linear-gradient(100deg, #eff6ff, #93c5fd); --nav-accent: #2563eb; --nav-text: #1e3a8a; --nav-icon: #60a5fa; --nav-glow: rgba(96, 165, 250, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Category_Analysis"] {{ --nav-bg: linear-gradient(100deg, #ffedd5, #fed7aa); --nav-hover: linear-gradient(100deg, #fff7ed, #fdba74); --nav-accent: #ea580c; --nav-text: #7c2d12; --nav-icon: #fb923c; --nav-glow: rgba(251, 146, 60, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/SubCategory_Analysis"] {{ --nav-bg: linear-gradient(100deg, #fce7f3, #fbcfe8); --nav-hover: linear-gradient(100deg, #fdf2f8, #f9a8d4); --nav-accent: #db2777; --nav-text: #831843; --nav-icon: #f472b6; --nav-glow: rgba(244, 114, 182, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Product_Analysis"] {{ --nav-bg: linear-gradient(100deg, #ccfbf1, #99f6e4); --nav-hover: linear-gradient(100deg, #f0fdfa, #5eead4); --nav-accent: #0f766e; --nav-text: #134e4a; --nav-icon: #2dd4bf; --nav-glow: rgba(45, 212, 191, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Customer_Analysis"] {{ --nav-bg: linear-gradient(100deg, #e0e7ff, #c7d2fe); --nav-hover: linear-gradient(100deg, #eef2ff, #a5b4fc); --nav-accent: #4f46e5; --nav-text: #312e81; --nav-icon: #818cf8; --nav-glow: rgba(129, 140, 248, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Segment_Analysis"] {{ --nav-bg: linear-gradient(100deg, #cffafe, #a7f3d0); --nav-hover: linear-gradient(100deg, #ecfeff, #6ee7b7); --nav-accent: #0d9488; --nav-text: #134e4a; --nav-icon: #2dd4bf; --nav-glow: rgba(45, 212, 191, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Order_Analysis"] {{ --nav-bg: linear-gradient(100deg, #ffe4e6, #fecdd3); --nav-hover: linear-gradient(100deg, #fff1f2, #fda4af); --nav-accent: #e11d48; --nav-text: #881337; --nav-icon: #fb7185; --nav-glow: rgba(251, 113, 133, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Shipping_Analysis"] {{ --nav-bg: linear-gradient(100deg, #dbeafe, #c7d2fe); --nav-hover: linear-gradient(100deg, #eff6ff, #a5b4fc); --nav-accent: #4f46e5; --nav-text: #312e81; --nav-icon: #818cf8; --nav-glow: rgba(129, 140, 248, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Discount_Analysis"] {{ --nav-bg: linear-gradient(100deg, #ffedd5, #fed7aa); --nav-hover: linear-gradient(100deg, #fff7ed, #fdba74); --nav-accent: #c2410c; --nav-text: #7c2d12; --nav-icon: #fb923c; --nav-glow: rgba(251, 146, 60, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Loss_Analysis"] {{ --nav-bg: linear-gradient(100deg, #fef2f2, #fecaca); --nav-hover: linear-gradient(100deg, #fff1f2, #f87171); --nav-accent: #dc2626; --nav-text: #7f1d1d; --nav-icon: #f87171; --nav-glow: rgba(248, 113, 113, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Time_Series"] {{ --nav-bg: linear-gradient(100deg, #e0f2fe, #bae6fd); --nav-hover: linear-gradient(100deg, #f0f9ff, #7dd3fc); --nav-accent: #0284c7; --nav-text: #0c4a6e; --nav-icon: #38bdf8; --nav-glow: rgba(56, 189, 248, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Growth_Analysis"] {{ --nav-bg: linear-gradient(100deg, #dcfce7, #bbf7d0); --nav-hover: linear-gradient(100deg, #f0fdf4, #86efac); --nav-accent: #16a34a; --nav-text: #14532d; --nav-icon: #4ade80; --nav-glow: rgba(74, 222, 128, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Sales_vs_Profit"] {{ --nav-bg: linear-gradient(100deg, #fae8ff, #f5d0fe); --nav-hover: linear-gradient(100deg, #fdf4ff, #e879f9); --nav-accent: #c026d3; --nav-text: #701a75; --nav-icon: #e879f9; --nav-glow: rgba(232, 121, 249, 0.36); }}
        nav[data-testid="stSidebarNav"] a[href$="/Top_Bottom"] {{ --nav-bg: linear-gradient(100deg, #fef9c3, #fde68a); --nav-hover: linear-gradient(100deg, #fffff0, #facc15); --nav-accent: #ca8a04; --nav-text: #713f12; --nav-icon: #facc15; --nav-glow: rgba(250, 204, 21, 0.38); }}
        nav[data-testid="stSidebarNav"] a[href$="/Data_Explorer"] {{ --nav-bg: linear-gradient(100deg, #e2e8f0, #cbd5e1); --nav-hover: linear-gradient(100deg, #f8fafc, #94a3b8); --nav-accent: #475569; --nav-text: #1e293b; --nav-icon: #94a3b8; --nav-glow: rgba(148, 163, 184, 0.34); }}

        /* Supplied dashboard palette: each route gets its own accent on the dark base. */
        nav[data-testid="stSidebarNav"] a[href$="/app"] {{ --nav-bg: linear-gradient(105deg, #00BFFF 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #38cfff 0%, #172333 92%); --nav-accent: #00BFFF; --nav-text: #ffffff; --nav-icon: #00BFFF; --nav-glow: rgba(0, 191, 255, 0.48); }}
        nav[data-testid="stSidebarNav"] a[href$="/Executive_Overview"] {{ --nav-bg: linear-gradient(105deg, #FFD700 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ffe34d 0%, #172333 92%); --nav-accent: #FFD700; --nav-text: #ffffff; --nav-icon: #FFD700; --nav-glow: rgba(255, 215, 0, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Sales_Analysis"] {{ --nav-bg: linear-gradient(105deg, #00C853 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #35df78 0%, #172333 92%); --nav-accent: #00C853; --nav-text: #ffffff; --nav-icon: #00C853; --nav-glow: rgba(0, 200, 83, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Profit_Analysis"] {{ --nav-bg: linear-gradient(105deg, #FF7043 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ff9878 0%, #172333 92%); --nav-accent: #FF7043; --nav-text: #ffffff; --nav-icon: #FF7043; --nav-glow: rgba(255, 112, 67, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Regional_Analysis"] {{ --nav-bg: linear-gradient(105deg, #00FFFF 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #54ffff 0%, #172333 92%); --nav-accent: #00FFFF; --nav-text: #ffffff; --nav-icon: #00FFFF; --nav-glow: rgba(0, 255, 255, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/State_Analysis"] {{ --nav-bg: linear-gradient(105deg, #9C27B0 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #bd55ce 0%, #172333 92%); --nav-accent: #9C27B0; --nav-text: #ffffff; --nav-icon: #9C27B0; --nav-glow: rgba(156, 39, 176, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/City_Analysis"] {{ --nav-bg: linear-gradient(105deg, #00BFFF 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #38cfff 0%, #172333 92%); --nav-accent: #00BFFF; --nav-text: #ffffff; --nav-icon: #00BFFF; --nav-glow: rgba(0, 191, 255, 0.48); }}
        nav[data-testid="stSidebarNav"] a[href$="/Category_Analysis"] {{ --nav-bg: linear-gradient(105deg, #C6FF00 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #d8ff4d 0%, #172333 92%); --nav-accent: #C6FF00; --nav-text: #ffffff; --nav-icon: #C6FF00; --nav-glow: rgba(198, 255, 0, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/SubCategory_Analysis"] {{ --nav-bg: linear-gradient(105deg, #FF6EC7 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ff9bdb 0%, #172333 92%); --nav-accent: #FF6EC7; --nav-text: #ffffff; --nav-icon: #FF6EC7; --nav-glow: rgba(255, 110, 199, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Product_Analysis"] {{ --nav-bg: linear-gradient(105deg, #C0C0C0 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #e0e0e0 0%, #172333 92%); --nav-accent: #C0C0C0; --nav-text: #ffffff; --nav-icon: #C0C0C0; --nav-glow: rgba(192, 192, 192, 0.42); }}
        nav[data-testid="stSidebarNav"] a[href$="/Customer_Analysis"] {{ --nav-bg: linear-gradient(105deg, #D81B60 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #e6538a 0%, #172333 92%); --nav-accent: #D81B60; --nav-text: #ffffff; --nav-icon: #D81B60; --nav-glow: rgba(216, 27, 96, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Segment_Analysis"] {{ --nav-bg: linear-gradient(105deg, #00C853 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #35df78 0%, #172333 92%); --nav-accent: #00C853; --nav-text: #ffffff; --nav-icon: #00C853; --nav-glow: rgba(0, 200, 83, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Order_Analysis"] {{ --nav-bg: linear-gradient(105deg, #FF7043 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ff9878 0%, #172333 92%); --nav-accent: #FF7043; --nav-text: #ffffff; --nav-icon: #FF7043; --nav-glow: rgba(255, 112, 67, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Shipping_Analysis"] {{ --nav-bg: linear-gradient(105deg, #00BFFF 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #38cfff 0%, #172333 92%); --nav-accent: #00BFFF; --nav-text: #ffffff; --nav-icon: #00BFFF; --nav-glow: rgba(0, 191, 255, 0.48); }}
        nav[data-testid="stSidebarNav"] a[href$="/Discount_Analysis"] {{ --nav-bg: linear-gradient(105deg, #FFD700 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ffe34d 0%, #172333 92%); --nav-accent: #FFD700; --nav-text: #ffffff; --nav-icon: #FFD700; --nav-glow: rgba(255, 215, 0, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Loss_Analysis"] {{ --nav-bg: linear-gradient(105deg, #FF6EC7 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #ff9bdb 0%, #172333 92%); --nav-accent: #FF6EC7; --nav-text: #ffffff; --nav-icon: #FF6EC7; --nav-glow: rgba(255, 110, 199, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Time_Series"] {{ --nav-bg: linear-gradient(105deg, #00FFFF 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #54ffff 0%, #172333 92%); --nav-accent: #00FFFF; --nav-text: #ffffff; --nav-icon: #00FFFF; --nav-glow: rgba(0, 255, 255, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Growth_Analysis"] {{ --nav-bg: linear-gradient(105deg, #C6FF00 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #d8ff4d 0%, #172333 92%); --nav-accent: #C6FF00; --nav-text: #ffffff; --nav-icon: #C6FF00; --nav-glow: rgba(198, 255, 0, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Sales_vs_Profit"] {{ --nav-bg: linear-gradient(105deg, #9C27B0 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #bd55ce 0%, #172333 92%); --nav-accent: #9C27B0; --nav-text: #ffffff; --nav-icon: #9C27B0; --nav-glow: rgba(156, 39, 176, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Top_Bottom"] {{ --nav-bg: linear-gradient(105deg, #D81B60 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #e6538a 0%, #172333 92%); --nav-accent: #D81B60; --nav-text: #ffffff; --nav-icon: #D81B60; --nav-glow: rgba(216, 27, 96, 0.45); }}
        nav[data-testid="stSidebarNav"] a[href$="/Data_Explorer"] {{ --nav-bg: linear-gradient(105deg, #C0C0C0 0%, #0E1117 88%); --nav-hover: linear-gradient(105deg, #e0e0e0 0%, #172333 92%); --nav-accent: #C0C0C0; --nav-text: #ffffff; --nav-icon: #C0C0C0; --nav-glow: rgba(192, 192, 192, 0.42); }}

        a[href$="/app"]::before {{ content: "🏠"; }}
        a[href$="/Executive_Overview"]::before {{ content: "📊"; }}
        a[href$="/Sales_Analysis"]::before {{ content: "💰"; }}
        a[href$="/Profit_Analysis"]::before {{ content: "📈"; }}
        a[href$="/Regional_Analysis"]::before {{ content: "🌍"; }}
        a[href$="/State_Analysis"]::before {{ content: "🗺️"; }}
        a[href$="/City_Analysis"]::before {{ content: "🏙️"; }}
        a[href$="/Category_Analysis"]::before {{ content: "🗂️"; }}
        a[href$="/SubCategory_Analysis"]::before {{ content: "📦"; }}
        a[href$="/Product_Analysis"]::before {{ content: "🧾"; }}
        a[href$="/Customer_Analysis"]::before {{ content: "👥"; }}
        a[href$="/Segment_Analysis"]::before {{ content: "🎯"; }}
        a[href$="/Order_Analysis"]::before {{ content: "🛒"; }}
        a[href$="/Shipping_Analysis"]::before {{ content: "🚚"; }}
        a[href$="/Discount_Analysis"]::before {{ content: "🏷️"; }}
        a[href$="/Loss_Analysis"]::before {{ content: "⚠️"; }}
        a[href$="/Time_Series"]::before {{ content: "🕒"; }}
        a[href$="/Growth_Analysis"]::before {{ content: "📊"; }}
        a[href$="/Sales_vs_Profit"]::before {{ content: "💹"; }}
        a[href$="/Top_Bottom"]::before {{ content: "🏆"; }}
        a[href$="/Data_Explorer"]::before {{ content: "🔎"; }}

        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"],
        label, p, small {{
            color: #18344d !important;
            font-family: "Nunito Sans", sans-serif;
            font-weight: 600;
            text-shadow: 0 1px 0 rgba(255,255,255,0.55);
        }}

        [data-testid="stCaptionContainer"] {{
            display: inline-block;
            max-width: 100%;
            margin: 0.18rem 0 0.72rem;
            padding: 0.34rem 0.62rem;
            border-left: 4px solid var(--page-accent);
            border-radius: 7px;
            background: rgba(255, 255, 255, 0.62);
            color: #12324d !important;
            font-size: 0.96rem;
            font-weight: 700;
            box-shadow: 0 3px 10px rgba(13, 27, 42, 0.1);
        }}

        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stHeading"] h1,
        [data-testid="stHeading"] h2,
        [data-testid="stHeading"] h3 {{
            text-shadow: 0 2px 0 rgba(255,255,255,0.68), 0 0 10px var(--page-accent-soft);
        }}

        [data-testid="stMetricValue"] {{
            color: #ffffff !important;
            font-family: "Inter", sans-serif;
            font-weight: 700 !important;
            font-size: 1.9rem !important;
            letter-spacing: 0.01em;
            line-height: 1.1 !important;
            margin-top: 0.4rem !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: #ebf3ff !important;
            font-family: "Inter", sans-serif;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 0.25rem 0.6rem;
            display: inline-block;
            border: 1px solid rgba(255,255,255,0.08);
            text-shadow: 0 1px 6px rgba(0, 191, 255, 0.28);
        }}

        .metric-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
            padding: 0.9rem 1rem 0.8rem;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            width: 100%;
        }}

        .metric-label-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ebf3ff;
            font-family: "Inter", sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 0.25rem 0.6rem;
            border: 1px solid rgba(255,255,255,0.08);
            width: fit-content;
            margin-bottom: 0.45rem;
            text-shadow: 0 1px 6px rgba(0, 191, 255, 0.28);
        }}

        .metric-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.3rem;
            height: 1.3rem;
            border-radius: 8px;
            background: rgba(255,255,255,0.08);
            font-size: 0.9rem;
        }}

        .metric-value {{
            color: #ffffff !important;
            font-family: "Inter", sans-serif;
            font-weight: 700 !important;
            font-size: 1.9rem !important;
            letter-spacing: 0.01em;
            line-height: 1.1 !important;
        }}

        .chart-insight {{
            margin: 0.35rem 0 0.9rem;
            padding: 0.7rem 0.9rem;
            border-left: 5px solid var(--page-accent);
            border-radius: 10px;
            background: linear-gradient(100deg, rgba(255, 241, 118, 0.92), rgba(255, 171, 145, 0.68));
            color: #0D1B2A !important;
            font-family: "Nunito Sans", sans-serif;
            font-size: 0.98rem;
            font-weight: 800;
            line-height: 1.45;
            text-shadow: 0 1px 0 rgba(255,255,255,0.72);
            box-shadow: 0 5px 16px rgba(13, 27, 42, 0.16), 0 0 14px var(--page-accent-soft);
        }}

        div[data-testid="stVerticalBlock"],
        div[data-testid="stHorizontalBlock"] > div {{
            background: rgba(15, 23, 42, 0.52);
            border: 1px solid var(--panel-border);
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
        }}

        div[data-testid="stDataFrame"],
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        input, textarea {{
            background: rgba(15, 23, 42, 0.9) !important;
            color: #f8fafc !important;
            border-color: rgba(148, 163, 184, 0.32) !important;
            font-family: "Roboto", sans-serif;
        }}

        input::placeholder, textarea::placeholder {{
            color: #94a3b8 !important;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 12px;
            overflow: hidden;
        }}

        h1, [data-testid="stHeading"] h1 {{
            color: {heading_color} !important;
            font-family: "Montserrat", sans-serif;
            font-weight: 900 !important;
            letter-spacing: 0.02em;
            font-size: clamp(2.3rem, 4vw, 5rem) !important;
            line-height: 1.05 !important;
            margin-top: 0.1rem !important;
            margin-bottom: 0.45rem !important;
            text-shadow: 0 2px 12px rgba(15, 23, 42, 0.18);
            background: linear-gradient(90deg, var(--page-accent) 0%, rgba(255,255,255,0.9) 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        h2, [data-testid="stHeading"] h2 {{
            color: #12324d !important;
            font-family: "Poppins", sans-serif;
            font-weight: 700 !important;
            letter-spacing: 0.01em;
            font-size: clamp(1.3rem, 2vw, 2rem) !important;
        }}

        .page-title-with-icon {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.4rem;
        }}

        .page-title-with-icon .title-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2.3rem;
            height: 2.3rem;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.08));
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.22);
            font-size: 1.25rem;
            line-height: 1;
            order: 2;
        }}

        .page-title-with-icon h1 {{
            order: 1;
            margin: 0;
        }}

        h3, [data-testid="stHeading"] h3 {{
            color: #123b5a !important;
            font-family: "Poppins", sans-serif;
            font-weight: 700 !important;
        }}

        h2, h3 {{
            border-left: 4px solid var(--page-accent);
            padding-left: 0.65rem;
            border-radius: 4px;
            background: linear-gradient(90deg, var(--page-accent-lite), transparent 80%);
        }}

        div[data-baseweb="select"]:focus-within,
        div[data-baseweb="input"]:focus-within,
        div[data-testid="stMultiSelect"]:focus-within {{
            border-color: var(--page-accent) !important;
            box-shadow: 0 0 0 1px var(--page-accent) !important;
        }}

        button:hover {{
            border-color: var(--page-accent) !important;
            color: var(--page-accent) !important;
        }}

        .stTable, table, th, td {{
            font-family: "Roboto", sans-serif;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    current_page = page_title or "Executive Overview"
    st.sidebar.markdown(
        '<div class="sidebar-nav-heading">Analysis Navigation</div>',
        unsafe_allow_html=True,
    )
    selected_page = st.sidebar.selectbox(
        "Select analysis",
        list(SIDEBAR_PAGE_PATHS),
        index=list(SIDEBAR_PAGE_PATHS).index(current_page),
        format_func=lambda name: f"{PAGE_ICONS.get(name, '📊')}  {name}",
        key="sidebar_analysis_navigation",
        label_visibility="collapsed",
    )
    if selected_page != current_page:
        st.switch_page(SIDEBAR_PAGE_PATHS[selected_page])


@st.cache_resource
def get_prepared_data():
    """
    Load and preprocess the dataset.
    """

    df = load_data()

    if df.empty:
        return df

    return prepare_data(df)


def style_dashboard_table(data, accent_color):
    """Apply dashboard colors to a dataframe before displaying it."""

    return (
        data.style
        .format(precision=2, thousands=",")
        .set_properties(
            **{
                "font-size": "1rem",
                "font-weight": "700",
                "color": "#10243e",
                "border": "1px solid rgba(30, 95, 145, 0.16)",
                "padding": "0.58rem 0.72rem",
            }
        )
        .background_gradient(
            subset=data.select_dtypes(include="number").columns,
            cmap="Blues",
            vmin=None,
            vmax=None,
        )
        .bar(
            subset=data.select_dtypes(include="number").columns,
            color=accent_color,
        )
        .set_table_styles([
            {
                "selector": "th.col_heading",
                "props": [
                    ("background-color", accent_color),
                    ("color", "#ffffff"),
                    ("font-size", "1rem"),
                    ("font-weight", "900"),
                    ("text-shadow", "0 1px 5px rgba(0,0,0,0.22)"),
                    ("border", "1px solid rgba(14, 17, 23, 0.22)"),
                    ("padding", "0.62rem 0.72rem"),
                ],
            },
            {
                "selector": "th.row_heading, th.index_name",
                "props": [
                    ("background-color", "rgba(0, 191, 255, 0.16)"),
                    ("color", "#0e3556"),
                    ("font-size", "1rem"),
                    ("font-weight", "900"),
                    ("border", "1px solid rgba(30, 95, 145, 0.16)"),
                    ("padding", "0.58rem 0.72rem"),
                ],
            },
            {
                "selector": "td.data",
                "props": [
                    ("color", "#10243e"),
                    ("font-size", "1rem"),
                    ("font-weight", "800"),
                ],
            },
            {
                "selector": "tbody tr:nth-child(even) td",
                "props": [("background-color", "rgba(0, 191, 255, 0.10)")],
            },
            {
                "selector": "tbody tr:hover",
                "props": [
                    ("background-color", "rgba(198, 255, 0, 0.24)"),
                    ("font-weight", "900"),
                ],
            },
        ])
    )


def categorical_chart_insight(grouped, dimension):
    """Summarize the strongest category signals shown in a chart."""

    largest = grouped.loc[grouped["Applications"].idxmax()]
    highest_risk = grouped.loc[grouped["Default_Rate"].idxmax()]
    return (
        f"Insight: {largest[dimension]} has the most applications "
        f"({int(largest['Applications']):,}), while {highest_risk[dimension]} "
        f"has the highest default rate ({highest_risk['Default_Rate']:.2f}%)."
    )


def numeric_chart_insight(data, dimension):
    """Summarize the distribution shown in a numeric chart."""

    values = data[dimension].dropna()
    if values.empty:
        return "Insight: No complete values are available for this chart."

    return (
        f"Insight: {dimension.replace('_', ' ').title()} ranges from "
        f"{values.min():,.2f} to {values.max():,.2f}, with a median of "
        f"{values.median():,.2f}."
    )


def three_d_chart_insight(data):
    """Summarize the 3D borrower profile without changing chart data."""

    default_rate = data["TARGET"].mean() * 100
    return (
        f"Insight: This 3D view contains {len(data):,} sampled applications; "
        f"the sampled default rate is {default_rate:.2f}%. Rotate the chart "
        "to compare income, credit, and age patterns."
    )


def show_chart_insight(text):
    """Render a visible highlighted insight callout."""

    st.markdown(
        f'<div class="chart-insight">{text}</div>', unsafe_allow_html=True)


def page_setup(
    title,
    description=""
):
    """
    Common page title and description.
    """

    st.title(title)

    if description:

        st.caption(
            description
        )


def show_missing_column(
    columns
):
    """
    Display warning when
    required columns are missing.
    """

    st.warning(
        "Required column(s) "
        "not available: "
        + ", ".join(columns)
    )

    st.stop()


def risk_summary(df):
    """
    Display default-rate KPI.
    """

    if "TARGET" not in df.columns:
        return

    if len(df) == 0:
        st.warning(
            "No records available."
        )
        return

    default_rate = (
        df["TARGET"].mean()
        * 100
    )

    st.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )


def page_specific_kpis(df, title, dimension):
    """Generate summary KPI cards that reflect the page's analysis focus."""
    if df.empty:
        return {
            "Applications": 0,
            "Default Rate": "0.00%",
            "Average Income": "0",
            "Average Credit": "0",
        }

    if dimension in df.columns:
        try:
            grouped = (
                df.groupby(dimension, dropna=False)
                .agg(
                    Applications=("TARGET", "size"),
                    Default_Rate=("TARGET", "mean"),
                    Avg_Income=("AMT_INCOME_TOTAL", "mean"),
                    Avg_Credit=("AMT_CREDIT", "mean"),
                )
                .reset_index()
            )
            if not grouped.empty:
                top_group = grouped.sort_values(
                    ["Applications", "Default_Rate"], ascending=[False, False]).iloc[0]
                return {
                    "Applications": int(top_group["Applications"]),
                    "Default Rate": f"{top_group['Default_Rate'] * 100:.2f}%",
                    "Average Income": f"{top_group['Avg_Income']:,.0f}",
                    "Average Credit": f"{top_group['Avg_Credit']:,.0f}",
                }
        except Exception:
            pass

    return {
        "Applications": len(df),
        "Default Rate": f"{df['TARGET'].mean() * 100:.2f}%" if "TARGET" in df.columns else "0.00%",
        "Average Income": f"{df['AMT_INCOME_TOTAL'].mean():,.0f}" if "AMT_INCOME_TOTAL" in df.columns else "0",
        "Average Credit": f"{df['AMT_CREDIT'].mean():,.0f}" if "AMT_CREDIT" in df.columns else "0",
    }


def render_analysis_page(title, description, dimension):
    """Render a consistent analysis page for the Home Credit dataset."""

    apply_dashboard_theme(title)
    icon = PAGE_ICONS.get(title, "📊")
    st.markdown(
        f"""
        <div class="page-title-with-icon">
            <h1>{title}</h1>
            <span class="title-badge">{icon}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(description)

    df = get_prepared_data()
    if df.empty:
        st.error("No application data is available.")
        st.stop()

    filtered_df = sidebar_filters(df)
    if filtered_df.empty:
        st.warning("The selected filters do not produce any records.")
        st.stop()

    metrics = page_specific_kpis(filtered_df, title, dimension)
    metric_items = [
        ("Applications", "📊", metrics["Applications"]),
        ("Default Rate", "📉", metrics["Default Rate"]),
        ("Average Income", "💵", metrics["Average Income"]),
        ("Average Credit", "🏦", metrics["Average Credit"]),
    ]
    columns = st.columns(4)
    for column, (label, icon, value) in zip(columns, metric_items):
        column.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label-row"><span class="metric-icon">{icon}</span>{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if dimension not in filtered_df.columns:
        st.error(f"Column `{dimension}` is not available in the dataset.")
        st.stop()

    from utils.charts import bar_chart, histogram, pie_chart, scatter_3d_chart

    chart_icon = PAGE_ICONS.get(title, "📊")
    st.markdown(
        f"<h3 style='display:flex; align-items:center; gap:10px; margin:1.2rem 0 0.7rem 0; justify-content:flex-start;'>"
        f"<span>Risk by {dimension.replace('_', ' ').title()}</span>"
        f"<span style='display:inline-flex; align-items:center; justify-content:center; width:1.8rem; height:1.8rem; border-radius:10px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.14);'>{chart_icon}</span>"
        f"</h3>",
        unsafe_allow_html=True,
    )
    if not pd.api.types.is_numeric_dtype(filtered_df[dimension]):
        grouped = (
            filtered_df.groupby(dimension, dropna=False)
            .agg(Applications=("TARGET", "size"), Default_Rate=("TARGET", "mean"))
            .reset_index()
        )
        grouped["Default_Rate"] *= 100
        st.plotly_chart(
            bar_chart(grouped, dimension, "Default_Rate",
                      "Default rate by group"),
            width="stretch",
        )
        show_chart_insight(categorical_chart_insight(grouped, dimension))
        left, right = st.columns(2)
        with left:
            st.plotly_chart(
                pie_chart(
                    grouped,
                    dimension,
                    "Applications",
                    f"Application share by {dimension.replace('_', ' ').title()}",
                ),
                width="stretch",
            )
            show_chart_insight(
                f"Insight: The pie chart shows application share across "
                f"{grouped[dimension].nunique()} {dimension.replace('_', ' ').lower()} groups."
            )
        with right:
            st.dataframe(
                style_dashboard_table(
                    grouped, PAGE_HEADING_COLORS.get(title, "#00BFFF")),
                width="stretch",
                hide_index=True,
            )
    else:
        st.plotly_chart(
            histogram(filtered_df, dimension,
                      title=f"{dimension.replace('_', ' ').title()} distribution"),
            width="stretch",
        )
        show_chart_insight(numeric_chart_insight(filtered_df, dimension))
        summary_columns = [dimension] if dimension == "TARGET" else [
            dimension, "TARGET"]
        summary = filtered_df[summary_columns].describe()
        st.dataframe(
            style_dashboard_table(
                summary, PAGE_HEADING_COLORS.get(title, "#00BFFF")),
            width="stretch",
        )

    # Add 3D analysis only when the selected dimension and supporting fields are numeric.
    if title not in {"Profit Analysis", "Loss Analysis"} and dimension != "TARGET":
        try:
            if pd.api.types.is_numeric_dtype(filtered_df[dimension]):
                if dimension == "AMT_CREDIT":
                    secondary_axis = "AMT_INCOME_TOTAL"
                else:
                    secondary_axis = "AMT_CREDIT"

                if dimension == "AGE_YEARS":
                    vertical_axis = "EMPLOYMENT_YEARS"
                else:
                    vertical_axis = "AGE_YEARS"

                three_d_columns = [dimension,
                                   secondary_axis, vertical_axis, "TARGET"]
                if (
                    len(set(three_d_columns)) == len(three_d_columns)
                    and all(column in filtered_df.columns for column in three_d_columns)
                ):
                    three_d_data = filtered_df[three_d_columns].dropna()
                    if not three_d_data.empty:
                        three_d_data = three_d_data.sample(
                            n=min(len(three_d_data), 3500),
                            random_state=42,
                        )
                        st.plotly_chart(
                            scatter_3d_chart(
                                three_d_data,
                                dimension,
                                secondary_axis,
                                vertical_axis,
                                color="TARGET",
                                title=(
                                    f"3D {dimension.replace('_', ' ').title()} analysis"
                                ),
                            ),
                            width="stretch",
                        )
                        show_chart_insight(three_d_chart_insight(three_d_data))
        except (KeyError, TypeError, ValueError):
            pass
