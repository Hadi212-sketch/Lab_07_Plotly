import json
import os
from pathlib import Path

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"


def save_figure(fig, out_dir: Path, stem: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    save_html = os.getenv("LAB07_SAVE_HTML", "0") == "1"
    html_path = out_dir / f"{stem}.html"
    png_path = out_dir / f"{stem}.png"
    if save_html:
        fig.write_html(str(html_path), include_plotlyjs="cdn")
    try:
        fig.write_image(str(png_path), width=1400, height=900, scale=2)
    except Exception as exc:
        note_path = out_dir / f"{stem}.image_export_error.txt"
        note_path.write_text(
            "PNG export failed.\n"
            f"Error: {exc}\n",
            encoding="utf-8",
        )


def build_100_dataviz() -> None:
    out_dir = OUT / "100_dataviz"

    # 1) Lollipop chart
    regions = [
        "Nordic", "Baltic", "Iberia", "Benelux", "Alpine",
        "Balkan", "Adriatic", "Aegean", "Baltic Sea", "Atlantic",
    ]
    values = [82, 76, 69, 91, 85, 58, 63, 71, 67, 88]

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=values,
            y=regions,
            mode="markers",
            marker=dict(size=16, color="#0f4c5c", line=dict(color="#e36414", width=2)),
            name="Score",
        )
    )
    for y, x in zip(regions, values):
        fig1.add_shape(type="line", x0=0, y0=y, x1=x, y1=y, line=dict(color="#9a031e", width=3))
    fig1.update_layout(
        title="Recreation 01: Lollipop Ranking",
        xaxis_title="Index",
        yaxis_title="Region",
        template="plotly_white",
        paper_bgcolor="#f8f4e3",
        plot_bgcolor="#f8f4e3",
    )
    save_figure(fig1, out_dir, "01_lollipop_ranking")

    # 2) Dumbbell chart
    countries = ["Belgium", "Netherlands", "Germany", "France", "Spain", "Italy"]
    baseline = [63, 58, 61, 55, 49, 53]
    followup = [72, 75, 70, 68, 62, 64]

    fig2 = go.Figure()
    for c, b, f in zip(countries, baseline, followup):
        fig2.add_shape(type="line", x0=b, y0=c, x1=f, y1=c, line=dict(color="#adb5bd", width=3))
    fig2.add_trace(go.Scatter(x=baseline, y=countries, mode="markers", marker=dict(size=14, color="#264653"), name="Baseline"))
    fig2.add_trace(go.Scatter(x=followup, y=countries, mode="markers", marker=dict(size=14, color="#e76f51"), name="Follow-up"))
    fig2.update_layout(
        title="Recreation 02: Dumbbell Comparison",
        xaxis_title="Mobility score",
        yaxis_title="Country",
        template="plotly_white",
        paper_bgcolor="#fff7f0",
        plot_bgcolor="#fff7f0",
    )
    save_figure(fig2, out_dir, "02_dumbbell_comparison")

    # 3) Waffle chart using heatmap
    cats = ["Therapy", "Assessment", "Training", "Admin"]
    pct = [45, 25, 20, 10]
    color_map = {
        "Therapy": "#1d3557",
        "Assessment": "#457b9d",
        "Training": "#a8dadc",
        "Admin": "#e63946",
    }
    waffle = []
    cat_cells = []
    for cat, p in zip(cats, pct):
        cat_cells.extend([cat] * p)
    for r in range(10):
        row = cat_cells[r * 10 : (r + 1) * 10]
        waffle.append(row)
    z = [[cats.index(c) for c in row] for row in waffle]
    colorscale = [
        [0.00, color_map["Therapy"]],
        [0.24, color_map["Therapy"]],
        [0.25, color_map["Assessment"]],
        [0.49, color_map["Assessment"]],
        [0.50, color_map["Training"]],
        [0.74, color_map["Training"]],
        [0.75, color_map["Admin"]],
        [1.00, color_map["Admin"]],
    ]
    fig3 = go.Figure(
        data=[
            go.Heatmap(
                z=z,
                colorscale=colorscale,
                showscale=False,
                xgap=2,
                ygap=2,
                hoverinfo="skip",
            )
        ]
    )
    fig3.update_yaxes(autorange="reversed", showticklabels=False)
    fig3.update_xaxes(showticklabels=False)
    fig3.update_layout(
        title="Recreation 03: Waffle Composition (100 cells)",
        paper_bgcolor="#f1faee",
        plot_bgcolor="#f1faee",
        template="plotly_white",
    )
    save_figure(fig3, out_dir, "03_waffle_composition")

    # 4) Radial bars
    skills = ["Grip", "Reach", "Stability", "Accuracy", "Speed", "Balance"]
    score = [78, 64, 82, 71, 60, 74]
    fig4 = go.Figure(
        go.Barpolar(
            r=score,
            theta=skills,
            marker_color=["#003049", "#d62828", "#f77f00", "#fcbf49", "#669bbc", "#2a9d8f"],
            marker_line_color="#111111",
            marker_line_width=1.5,
            opacity=0.9,
        )
    )
    fig4.update_layout(
        title="Recreation 04: Radial Skill Profile",
        template="plotly_white",
        paper_bgcolor="#fcf6e8",
        polar=dict(radialaxis=dict(range=[0, 100], ticksuffix="")),
    )
    save_figure(fig4, out_dir, "04_radial_profile")

    # 5) Stacked area / stream style
    x = list(range(1, 13))
    a = [10, 14, 17, 20, 22, 24, 23, 21, 19, 17, 13, 11]
    b = [8, 10, 12, 15, 16, 16, 15, 14, 12, 10, 9, 8]
    c = [5, 7, 8, 10, 12, 13, 12, 11, 9, 8, 7, 6]

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=x, y=a, stackgroup="one", mode="lines", line=dict(width=0.5, color="#0b3c49"), name="Cognitive"))
    fig5.add_trace(go.Scatter(x=x, y=b, stackgroup="one", mode="lines", line=dict(width=0.5, color="#3b8ea5"), name="Motor"))
    fig5.add_trace(go.Scatter(x=x, y=c, stackgroup="one", mode="lines", line=dict(width=0.5, color="#f46036"), name="Visual"))
    fig5.update_layout(
        title="Recreation 05: Stream-style Stacked Area",
        xaxis_title="Month",
        yaxis_title="Session load",
        template="plotly_white",
        paper_bgcolor="#fdf0d5",
        plot_bgcolor="#fdf0d5",
    )
    save_figure(fig5, out_dir, "05_stream_area")


def build_hemianopsia() -> None:
    out_dir = OUT / "hemianopsia"

    data = {
        "time": 1709550269540,
        "id": "Hemianopsia-396373",
        "fakePercent": 0,
        "fixationPercent": 100,
        "unSeenPoints": [{"z": 55.138145446777344, "x": -20.06864356994629, "y": -6.167179107666016}],
        "reactionTimes": [
            682.6985473632812, 391.7491760253906, 362.61138916015625, 306.4205017089844,
            291.9778137207031, 265.0105895996094, 374.3802795410156, 343.149169921875,
            334.63824462890625, 290.0105895996094, 321.00054931640625, 320.3567199707031,
            306.8519287109375, 347.7110900878906, 320.556640625, 292.5042419433594,
            583.4418334960938, 376.8360595703125, 457.558837890625,
        ],
        "seenPoints": [
            {"y": -19.20852279663086, "z": 54.938087463378906, "x": -9.687067985534668},
            {"y": -6.167180061340332, "z": 57.78535842895508, "x": 10.189117431640625},
            {"x": -10.168876647949219, "z": 57.67055892944336, "y": 7.1902923583984375},
            {"x": 10.168876647949219, "z": 57.67055892944336, "y": 7.1902923583984375},
            {"y": -6.167180061340332, "z": 57.78535842895508, "x": -10.189117431640625},
            {"y": -6.167180061340332, "z": 58.67679214477539, "x": 0},
            {"z": 55.02861022949219, "x": 20.028778076171875, "y": 7.190291404724121},
            {"y": 20.17919158935547, "z": 54.599578857421875, "x": -9.627378463745117},
            {"z": 55.441864013671875, "y": 20.179189682006836, "x": 0},
            {"y": 7.190291881561279, "z": 58.56022262573242, "x": 0},
            {"y": -19.20852279663086, "x": 9.687067985534668, "z": 54.938087463378906},
            {"z": 52.42131042480469, "y": -19.20852279663086, "x": 19.079801559448242},
            {"y": 7.190291404724121, "z": 55.02861022949219, "x": -20.028778076171875},
            {"y": 20.17919158935547, "z": 54.599578857421875, "x": 9.627378463745117},
            {"z": 55.138145446777344, "y": -6.167179107666016, "x": 20.06864356994629},
            {"x": -19.079801559448242, "y": -19.20852279663086, "z": 52.42131042480469},
            {"z": 52.09830856323242, "y": 20.179189682006836, "x": 18.96223258972168},
            {"z": 52.09830856323242, "y": 20.179189682006836, "x": -18.96223258972168},
            {"x": 0, "z": 55.78559494018555, "y": -19.208520889282227},
        ],
        "settings": {
            "speed": 2,
            "stimuliCount": 10,
            "fakeChance": 0.20000000298023224,
            "verticalFOV": 40,
            "delay": 1,
            "horizontalFOV": 40,
        },
    }

    seen = data["seenPoints"]
    unseen = data["unSeenPoints"]
    rt = data["reactionTimes"]
    settings = data["settings"]

    x_half_range = settings["horizontalFOV"] / 2
    y_half_range = settings["verticalFOV"] / 2
    z_min = min(sz for sz in [p["z"] for p in seen + unseen]) - 2
    z_max = max(sz for sz in [p["z"] for p in seen + unseen]) + 2

    sx = [p["x"] for p in seen]
    sy = [p["y"] for p in seen]
    sz = [p["z"] for p in seen]
    ux = [p["x"] for p in unseen]
    uy = [p["y"] for p in unseen]
    uz = [p["z"] for p in unseen]

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "xy"}]],
        subplot_titles=("Stimuli Map in 3D", "Reaction Time per Seen Stimulus"),
    )

    fig.add_trace(
        go.Scatter3d(
            x=sx,
            y=sy,
            z=sz,
            mode="markers+lines",
            marker=dict(size=6, color=rt, colorscale="Viridis", colorbar=dict(title="ms")),
            line=dict(color="#1d3557", width=3),
            name="Seen points",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter3d(
            x=ux,
            y=uy,
            z=uz,
            mode="markers",
            marker=dict(size=9, color="#e63946", symbol="x"),
            name="Unseen points",
        ),
        row=1,
        col=1,
    )

    idx = list(range(1, len(rt) + 1))
    fig.add_trace(
        go.Scatter(x=idx, y=rt, mode="lines+markers", line=dict(color="#457b9d", width=3), marker=dict(size=7), name="Reaction time"),
        row=1,
        col=2,
    )

    fig.update_layout(
        title="Hemianopsia: Visual Field Stimuli and Reaction Times",
        template="plotly_white",
        paper_bgcolor="#f1faee",
        annotations=[
            dict(
                x=0.01,
                y=1.13,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="left",
                text=(
                    f"ID: {data['id']} | Fixation: {data['fixationPercent']}% | "
                    f"FOV: {settings['horizontalFOV']}x{settings['verticalFOV']} deg | "
                    f"StimuliCount setting: {settings['stimuliCount']}"
                ),
                font=dict(size=12),
            )
        ],
        scene=dict(
            xaxis_title="X (deg)",
            yaxis_title="Y (deg)",
            zaxis_title="Depth",
            aspectmode="cube",
            xaxis=dict(range=[-x_half_range, x_half_range]),
            yaxis=dict(range=[-y_half_range, y_half_range]),
            zaxis=dict(range=[z_min, z_max]),
        ),
        xaxis_title="Stimulus order",
        yaxis_title="Reaction time (ms)",
    )

    save_figure(fig, out_dir, "hemianopsia_3d")

    # Dedicated rendition that mirrors the lab example style: only seen vs unseen in one 3D plot.
    fig_example = go.Figure()
    fig_example.add_trace(
        go.Scatter3d(
            x=sx,
            y=sy,
            z=sz,
            mode="markers",
            marker=dict(size=5, color="#3b4ddb"),
            name="Seen Points",
        )
    )
    fig_example.add_trace(
        go.Scatter3d(
            x=ux,
            y=uy,
            z=uz,
            mode="markers",
            marker=dict(size=6, color="#e53935"),
            name="Unseen Points",
        )
    )
    fig_example.update_layout(
        title="3D Scatterplot of Seen and Unseen Points",
        template="plotly",
        paper_bgcolor="#e5e7eb",
        scene=dict(
            xaxis_title="X (Left/Right)",
            yaxis_title="Y (Up/Down)",
            zaxis_title="Z (Depth)",
            xaxis=dict(range=[-x_half_range, x_half_range]),
            yaxis=dict(range=[-y_half_range, y_half_range]),
            zaxis=dict(range=[z_min, z_max]),
            camera=dict(eye=dict(x=1.5, y=1.4, z=1.2)),
        ),
        legend=dict(x=1.02, y=0.95),
        annotations=[
            dict(
                x=0.5,
                y=1.04,
                xref="paper",
                yref="paper",
                showarrow=False,
                text=f"{data['id']} | Fixation {data['fixationPercent']}% | FOV {settings['horizontalFOV']}x{settings['verticalFOV']} deg",
                font=dict(size=12),
            )
        ],
    )
    save_figure(fig_example, out_dir, "hemianopsia_example_rendition")


def _extract_hand_payload(item):
    hand = item.get("hand", "UNKNOWN")
    horiz = item.get("horizontalCoordinates", [])
    vert = item.get("verticalCoordinates", [])
    return hand, horiz, vert


def _span(values):
    if not values:
        return 0.0
    return max(values) - min(values)


def build_motor_amplification() -> None:
    out_dir = OUT / "motor_amplification"

    files = [ROOT / "005774.json", ROOT / "479379.json", ROOT / "926818.json"]
    summary_rows = []

    for fpath in files:
        payload = json.loads(fpath.read_text(encoding="utf-8"))
        pid = payload.get("id", fpath.stem)

        actual_by_hand = {h.get("hand", "UNKNOWN"): h for h in payload.get("handData", [])}
        adapted_by_hand = {h.get("hand", "UNKNOWN"): h for h in payload.get("adaptedHandData", [])}

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                "Horizontal ROM (x-z plane)",
                "Vertical ROM (y-z plane)",
            ),
        )

        for hand in ["LEFT", "RIGHT"]:
            actual = actual_by_hand.get(hand, {})
            adapted = adapted_by_hand.get(hand, {})

            ah = actual.get("horizontalCoordinates", [])
            av = actual.get("verticalCoordinates", [])
            dh = adapted.get("horizontalCoordinates", [])
            dv = adapted.get("verticalCoordinates", [])

            if ah:
                fig.add_trace(
                    go.Scatter(
                        x=[p["x"] for p in ah],
                        y=[p["z"] for p in ah],
                        mode="lines+markers",
                        line=dict(width=3),
                        marker=dict(size=4),
                        name=f"{hand} actual",
                    ),
                    row=1,
                    col=1,
                )

            if dh:
                fig.add_trace(
                    go.Scatter(
                        x=[p["x"] for p in dh],
                        y=[p["z"] for p in dh],
                        mode="lines",
                        line=dict(width=2, dash="dot"),
                        name=f"{hand} adapted",
                    ),
                    row=1,
                    col=1,
                )

            if av:
                fig.add_trace(
                    go.Scatter(
                        x=[p["y"] for p in av],
                        y=[p["z"] for p in av],
                        mode="lines+markers",
                        line=dict(width=3),
                        marker=dict(size=4),
                        name=f"{hand} actual",
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )

            if dv:
                fig.add_trace(
                    go.Scatter(
                        x=[p["y"] for p in dv],
                        y=[p["z"] for p in dv],
                        mode="lines",
                        line=dict(width=2, dash="dot"),
                        name=f"{hand} adapted",
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )

            summary_rows.append(
                {
                    "id": pid,
                    "hand": hand,
                    "h_actual": _span([p.get("x", 0.0) for p in ah]),
                    "h_adapted": _span([p.get("x", 0.0) for p in dh]),
                    "v_actual": _span([p.get("y", 0.0) for p in av]),
                    "v_adapted": _span([p.get("y", 0.0) for p in dv]),
                }
            )

        fig.update_layout(
            title=f"Motor Amplification ROM: {pid}",
            template="plotly_white",
            paper_bgcolor="#f8f9fa",
            plot_bgcolor="#f8f9fa",
        )
        fig.update_xaxes(title_text="X", row=1, col=1)
        fig.update_yaxes(title_text="Z", row=1, col=1)
        fig.update_xaxes(title_text="Y", row=1, col=2)
        fig.update_yaxes(title_text="Z", row=1, col=2)

        save_figure(fig, out_dir, f"{pid}_trajectories")

    labels = [f"{r['id']} {r['hand']}" for r in summary_rows]
    fig_sum = go.Figure()
    fig_sum.add_trace(go.Bar(x=labels, y=[r["h_actual"] for r in summary_rows], name="Horizontal actual", marker_color="#1d3557"))
    fig_sum.add_trace(go.Bar(x=labels, y=[r["h_adapted"] for r in summary_rows], name="Horizontal adapted", marker_color="#457b9d"))
    fig_sum.add_trace(go.Bar(x=labels, y=[r["v_actual"] for r in summary_rows], name="Vertical actual", marker_color="#e76f51"))
    fig_sum.add_trace(go.Bar(x=labels, y=[r["v_adapted"] for r in summary_rows], name="Vertical adapted", marker_color="#f4a261"))
    fig_sum.update_layout(
        barmode="group",
        title="Motor Amplification: Actual vs Adapted ROM Span",
        xaxis_title="Session + hand",
        yaxis_title="Range of motion span",
        template="plotly_white",
        paper_bgcolor="#fffaf3",
        plot_bgcolor="#fffaf3",
    )
    save_figure(fig_sum, out_dir, "motor_rom_summary")


def build_optional_first_demo_screenshot() -> None:
    out_dir = OUT / "optional"
    df = px.data.gapminder()
    fig = px.bar(
        df[df["country"] == "Belgium"],
        x="year",
        y="pop",
        title="Optional: First Demo Screenshot (Belgium Population)",
        height=500,
    )
    fig.update_layout(template="plotly_white", paper_bgcolor="#f7f7f7", plot_bgcolor="#f7f7f7")
    save_figure(fig, out_dir, "first_demo_screenshot")


def build_optional_star_cancellation_experiment() -> None:
    out_dir = OUT / "star_cancellation"

    star_json_path = ROOT / "341980.json"
    if not star_json_path.exists():
        fig = go.Figure()
        fig.add_annotation(
            text="341980.json not found. Place it in workspace root to render data-driven star cancellation.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16),
        )
        fig.update_layout(title="Optional Star Cancellation Experiment", template="plotly_white")
        save_figure(fig, out_dir, "star_cancellation_experiment")
        return

    payload = json.loads(star_json_path.read_text(encoding="utf-8"))
    objects = payload.get("objects", [])

    big = [o for o in objects if o.get("cancellationObjectType") == "BIG_STAR"]
    small = [o for o in objects if o.get("cancellationObjectType") == "SMALL_STAR"]
    words = [o for o in objects if o.get("cancellationObjectType") == "WORD"]

    selected_small = [o for o in small if o.get("selected")]
    unselected_small = [o for o in small if not o.get("selected")]
    selected_path = sorted(
        [o for o in selected_small if isinstance(o.get("sequencePosition"), int) and o.get("sequencePosition") > 0],
        key=lambda o: o.get("sequencePosition"),
    )

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Star Board Selection Experiment", "Case Summary Metrics"),
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        column_widths=[0.65, 0.35],
    )

    fig.add_trace(
        go.Scatter(
            x=[o["coordinate"]["x"] for o in big],
            y=[o["coordinate"]["y"] for o in big],
            mode="markers",
            marker=dict(symbol="star", size=16, color="#111111", line=dict(width=1, color="#111111")),
            name="Big stars",
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=[o["coordinate"]["x"] for o in unselected_small],
            y=[o["coordinate"]["y"] for o in unselected_small],
            mode="markers",
            marker=dict(symbol="star", size=10, color="#9ca3af"),
            name="Small stars (unselected)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=[o["coordinate"]["x"] for o in selected_small],
            y=[o["coordinate"]["y"] for o in selected_small],
            mode="markers",
            marker=dict(symbol="star", size=11, color="#84cc16"),
            name="Small stars (selected)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=[o["coordinate"]["x"] for o in selected_path],
            y=[o["coordinate"]["y"] for o in selected_path],
            mode="lines+markers",
            line=dict(color="#1d4ed8", width=3),
            marker=dict(symbol="star", size=10, color="#84cc16"),
            name="Selection sequence",
        ),
        row=1,
        col=1,
    )

    # Use metadata fields from the real file.
    object_stats = payload.get("objectStats", [])
    head_stats = payload.get("headMovementBoundaries", [])

    def _pick_stat(direction: str, field: str, default: int = 0) -> int:
        for item in object_stats:
            if item.get("direction") == direction and item.get("cancellationObjectType") == "SMALL_STAR":
                return int(item.get(field, default))
        return default

    def _pick_head(direction: str) -> int:
        for item in head_stats:
            if item.get("direction") == direction:
                return int(item.get("timesReachedBoundary", 0))
        return 0

    metric_names = ["Small stars left", "Small stars right", "Selected left", "Selected right", "Head left", "Head right"]
    metric_values = [
        _pick_stat("LEFT", "totalAmountOfObjects"),
        _pick_stat("RIGHT", "totalAmountOfObjects"),
        _pick_stat("LEFT", "selectedAmountOfObjects"),
        _pick_stat("RIGHT", "selectedAmountOfObjects"),
        _pick_head("LEFT"),
        _pick_head("RIGHT"),
    ]

    fig.add_trace(
        go.Bar(
            x=metric_values,
            y=metric_names,
            orientation="h",
            marker=dict(color=["#334155", "#475569", "#16a34a", "#15803d", "#f59e0b", "#d97706"]),
            name="Metrics",
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="Count", row=1, col=2)
    fig.update_yaxes(title_text="", row=1, col=2)

    fig.update_layout(
        title="Optional Star Cancellation Experiment (Board + Sequence + Stats)",
        template="plotly_white",
        paper_bgcolor="#f5f5f5",
        plot_bgcolor="#f5f5f5",
        showlegend=True,
    )

    save_figure(fig, out_dir, "star_cancellation_experiment")

    # Additional 3D coordinate view using the real object positions.
    fig3d = go.Figure()
    fig3d.add_trace(
        go.Scatter3d(
            x=[o["coordinate"]["x"] for o in big],
            y=[o["coordinate"]["y"] for o in big],
            z=[o["coordinate"]["z"] for o in big],
            mode="markers",
            marker=dict(size=5, color="#111111", symbol="circle"),
            name="Big stars",
        )
    )
    fig3d.add_trace(
        go.Scatter3d(
            x=[o["coordinate"]["x"] for o in small],
            y=[o["coordinate"]["y"] for o in small],
            z=[o["coordinate"]["z"] for o in small],
            mode="markers",
            marker=dict(size=4, color=["#84cc16" if o.get("selected") else "#9ca3af" for o in small]),
            name="Small stars",
        )
    )
    fig3d.add_trace(
        go.Scatter3d(
            x=[o["coordinate"]["x"] for o in selected_path],
            y=[o["coordinate"]["y"] for o in selected_path],
            z=[o["coordinate"]["z"] for o in selected_path],
            mode="lines+markers",
            line=dict(color="#1d4ed8", width=6),
            marker=dict(size=3, color="#22c55e"),
            name="Selection path",
        )
    )
    fig3d.update_layout(
        title="Star Cancellation 3D Coordinates (from 341980.json)",
        template="plotly_white",
        paper_bgcolor="#f5f5f5",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
    )
    save_figure(fig3d, out_dir, "star_cancellation_3d")


def main() -> None:
    build_100_dataviz()
    build_hemianopsia()
    build_motor_amplification()
    build_optional_first_demo_screenshot()
    build_optional_star_cancellation_experiment()
    print("Done. Outputs generated in ./outputs")


if __name__ == "__main__":
    main()
