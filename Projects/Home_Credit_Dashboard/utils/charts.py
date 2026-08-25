import plotly.express as px


TRENDING_CATEGORICAL_COLORS = [
    "#2563EB",  # blue
    "#14B8A6",  # teal
    "#F59E0B",  # amber
    "#F97316",  # orange
    "#E11D48",  # rose
    "#7C3AED",  # violet
    "#0891B2",  # cyan
    "#65A30D",  # lime
]
IMPACT_COLOR_SCALE = ["#0EA5E9", "#14B8A6", "#F59E0B", "#F97316", "#E11D48"]


def apply_dark_chart_theme(figure):
    """Keep Plotly charts readable on the dashboard's black canvas."""

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#111923",
        font={"color": "#F8FAFC", "family": "Roboto, sans-serif"},
        margin={"l": 56, "r": 30, "t": 62, "b": 54},
        separators=".,",
        legend={
            "bgcolor": "rgba(14, 17, 23, 0.94)",
            "bordercolor": "rgba(0, 191, 255, 0.72)",
            "borderwidth": 1,
            "font": {
                "color": "#FFFFFF",
                "size": 13,
                "family": "Roboto, sans-serif",
            },
            "title": {
                "font": {
                    "color": "#00FFFF",
                    "size": 14,
                    "family": "Roboto, sans-serif",
                },
            },
        },
        xaxis={
            "gridcolor": "#334155",
            "zerolinecolor": "#475569",
            "showline": True,
            "linecolor": "#64748B",
            "linewidth": 1,
            "mirror": True,
        },
        yaxis={
            "gridcolor": "#334155",
            "zerolinecolor": "#475569",
            "showline": True,
            "linecolor": "#64748B",
            "linewidth": 1,
            "mirror": True,
        },
    )
    figure.update_coloraxes(
        colorbar={
            "bgcolor": "rgba(14, 17, 23, 0.94)",
            "bordercolor": "rgba(0, 191, 255, 0.72)",
            "borderwidth": 1,
            "tickfont": {
                "color": "#FFFFFF",
                "size": 13,
                "family": "Roboto, sans-serif",
            },
            "title": {
                "font": {
                    "color": "#00FFFF",
                    "size": 14,
                    "family": "Roboto, sans-serif",
                },
            },
        }
    )
    return figure


def bar_chart(
    data,
    x,
    y,
    title,
    text=None
):
    """
    Create a bar chart.
    """

    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        text=text,
        color=x,
        color_discrete_sequence=TRENDING_CATEGORICAL_COLORS,
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        showlegend=False,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    fig.update_traces(
        texttemplate="%{y:.2f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
    )
    apply_dark_chart_theme(fig)

    return fig


def line_chart(
    data,
    x,
    y,
    title,
    color=None,
):
    """
    Create a line chart.
    """

    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=TRENDING_CATEGORICAL_COLORS,
    )

    fig.update_traces(
        mode="lines+markers",
        line={"width": 3},
        marker={"size": 7},
        hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
    )
    fig.update_layout(
        hovermode="x unified",
        legend_title_text="",
    )
    apply_dark_chart_theme(fig)

    return fig


def pie_chart(
    data,
    names,
    values,
    title,
):
    """Create a categorical share chart."""

    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        hole=0.42,
        color_discrete_sequence=TRENDING_CATEGORICAL_COLORS,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Applications: %{value:,}<extra></extra>",
    )
    fig.update_layout(showlegend=True, legend_title_text="")
    apply_dark_chart_theme(fig)

    return fig


def scatter_chart(
    data,
    x,
    y,
    color=None,
    title=""
):
    """
    Create a scatter plot.
    """

    scatter_color = color
    color_scale = None
    if color is None and y in data.columns and data[y].dtype.kind in "ifu":
        scatter_color = y
        color_scale = IMPACT_COLOR_SCALE

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=scatter_color,
        title=title,
        opacity=0.72,
        color_discrete_sequence=TRENDING_CATEGORICAL_COLORS,
        color_continuous_scale=color_scale,
    )

    fig.update_traces(
        marker={"size": 9, "line": {"width": 1, "color": "#FFFFFF"}},
        hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
    )
    fig.update_layout(legend_title_text="")
    apply_dark_chart_theme(fig)

    return fig


def scatter_3d_chart(
    data,
    x,
    y,
    z,
    color=None,
    title="",
):
    """Create an interactive 3D scatter chart."""

    x_label = x.replace("_", " ").title()
    y_label = y.replace("_", " ").title()
    z_label = z.replace("_", " ").title()

    fig = px.scatter_3d(
        data,
        x=x,
        y=y,
        z=z,
        color=color,
        title=title,
        opacity=0.72,
        color_continuous_scale=IMPACT_COLOR_SCALE,
    )
    fig.update_traces(
        marker={"size": 4, "line": {"width": 0.4, "color": "#FFFFFF"}},
        hovertemplate=(
            f"<b>{x_label}:</b> %{{x:,.2f}}<br>"
            f"<b>{y_label}:</b> %{{y:,.2f}}<br>"
            f"<b>{z_label}:</b> %{{z:,.2f}}<br>"
            "<b>Default:</b> %{marker.color}<extra></extra>"
        ),
    )
    fig.update_layout(
        legend_title_text="",
        scene={
            "xaxis": {"title": x_label, "showline": True, "linecolor": "#64748B", "gridcolor": "#334155", "backgroundcolor": "#111923"},
            "yaxis": {"title": y_label, "showline": True, "linecolor": "#64748B", "gridcolor": "#334155", "backgroundcolor": "#111923"},
            "zaxis": {"title": z_label, "showline": True, "linecolor": "#64748B", "gridcolor": "#334155", "backgroundcolor": "#111923"},
            "bgcolor": "#111923",
        },
    )
    apply_dark_chart_theme(fig)

    return fig


def histogram(
    data,
    x,
    color=None,
    title=""
):
    """
    Create a histogram.
    """

    fig = px.histogram(
        data,
        x=x,
        color=color,
        title=title,
        marginal="box",
        color_discrete_sequence=TRENDING_CATEGORICAL_COLORS,
    )
    apply_dark_chart_theme(fig)

    return fig
