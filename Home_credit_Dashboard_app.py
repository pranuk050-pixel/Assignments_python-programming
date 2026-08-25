import streamlit as st
from utils.charts import bar_chart, histogram, scatter_3d_chart
from utils.features import default_rate, group_default
from utils.filters import sidebar_filters
from utils.kpis import overview_kpis
from utils.page_helpers import (
    PAGE_HEADING_COLORS,
    apply_dashboard_theme,
    get_prepared_data,
    show_chart_insight,
    three_d_chart_insight,
    style_dashboard_table,
)

st.set_page_config(
    page_title="Home Credit Dashboard 🏦",
    page_icon="🤝",
    layout="wide",
)

apply_dashboard_theme()

st.markdown(
    """
    <style>
    .dashboard-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 0 0 8px 0;
        padding: 0.2rem 0;
        flex-wrap: nowrap;
    }
    .dashboard-header .title-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 56px;
        height: 56px;
        min-width: 56px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(255,255,255,0.05));
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.16);
        font-size: 2.2rem;
        line-height: 1;
        filter: drop-shadow(0 8px 16px rgba(0,0,0,0.12));
    }
    .dashboard-header .title-icon.bank {
        font-size: 2.1rem;
        width: 52px;
        height: 52px;
    }
    .dashboard-header h1 {
        margin: 0;
        font-family: "Montserrat", sans-serif;
        font-size: clamp(2.6rem, 4vw, 5.5rem);
        font-weight: 900;
        line-height: 1.02;
        letter-spacing: 0.02em;
        color: #DCE9FF;
        text-shadow: 0 8px 18px rgba(30,42,120,0.28);
        white-space: nowrap;
    }
    @media (max-width: 900px) {
        .dashboard-header {
            gap: 10px;
            flex-wrap: wrap;
        }
        .dashboard-header h1 {
            white-space: normal;
        }
    }
    </style>
    <div class="dashboard-header">
        <span class="title-icon">🤝</span>
        <h1>Home Credit Dashboard</h1>
        <span class="title-icon bank">🏦</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Explore application volume, borrower characteristics, and default risk.")

if st.button("🔄 Reload Data"):
    st.rerun()

df = get_prepared_data()
if df.empty:
    st.error("No data was found at data/application_train.csv.")
    st.stop()

filtered_df = sidebar_filters(df)
metrics = overview_kpis(filtered_df)

metric_items = [
    ("Applications", "📊", f"{metrics['applications']:,}"),
    ("Default Rate", "📉", f"{metrics['default_rate']:.2f}%"),
    ("Average Income", "💵", f"{metrics['avg_income']:,.0f}"),
    ("Average Credit", "🏦", f"{metrics['avg_credit']:,.0f}"),
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

st.subheader("Risk by borrower profile")
group_column = st.selectbox(
    "Group results by",
    ["NAME_CONTRACT_TYPE", "NAME_EDUCATION_TYPE", "NAME_INCOME_TYPE"],
)
grouped = group_default(filtered_df, group_column)
if grouped.empty:
    st.info("The selected filters do not produce a usable breakdown.")
else:
    st.plotly_chart(
        bar_chart(grouped, group_column, "default_rate",
                  "Default rate by group"),
        width="stretch",
    )
    show_chart_insight(
        f"Insight: {grouped.loc[grouped['default_rate'].idxmax(), group_column]} "
        f"has the highest default rate at "
        f"{grouped['default_rate'].max():.2f}%."
    )

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            histogram(filtered_df, "AMT_INCOME_TOTAL",
                      title="Income distribution"),
            width="stretch",
        )
        show_chart_insight(
            f"Insight: Income has a median of "
            f"{filtered_df['AMT_INCOME_TOTAL'].median():,.0f} "
            "within the current filters."
        )
    with right:
        st.dataframe(
            style_dashboard_table(
                grouped,
                PAGE_HEADING_COLORS.get("Executive Overview", "#FFD700"),
            ),
            width="stretch",
            hide_index=True,
        )

st.subheader("3D borrower risk profile")
three_d_columns = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AGE_YEARS", "TARGET"]
if all(column in filtered_df.columns for column in three_d_columns):
    three_d_data = filtered_df[three_d_columns].dropna()
    if not three_d_data.empty:
        three_d_data = three_d_data.sample(
            n=min(len(three_d_data), 3500),
            random_state=42,
        )
        st.plotly_chart(
            scatter_3d_chart(
                three_d_data,
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AGE_YEARS",
                color="TARGET",
                title="Income, credit, age and default risk",
            ),
            width="stretch",
        )
        show_chart_insight(three_d_chart_insight(three_d_data))
    else:
        st.info("The selected filters do not produce enough complete 3D records.")
