import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Yetitrader 4-Pillar Framework",
    page_icon="📊",
    layout="wide"
)

# Create the app header
st.title("Yetitrader 4-Pillar Framework Analyzer")
st.markdown("*This app analyzes trading setups based on the Yetitrader 4-Pillar Framework*")

# Initialize session state for pivot values if not already set
if 'pivot_initialized' not in st.session_state:
    st.session_state.pivot_initialized = False
    st.session_state.r3 = 535.00
    st.session_state.r2 = 533.50
    st.session_state.r1 = 532.00
    st.session_state.pivot = 530.50
    st.session_state.s1 = 529.47
    st.session_state.s2 = 528.38
    st.session_state.s3 = 527.00
    st.session_state.price = 530.00
    st.session_state.broken_levels = []

# Two-tab system: Setup and Analysis
tab1, tab2 = st.tabs(["Setup Pivot Levels", "Trade Analysis"])

# Tab 1: Setup Pivot Levels
with tab1:
    st.header("Daily Pivot Levels Setup")
    st.markdown("Enter pivot levels once for the trading day. These values will be saved for all your analysis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input fields for resistance levels
        st.subheader("Resistance Levels")
        r3 = st.number_input("R3", value=st.session_state.r3, format="%.2f", step=0.01, key="r3_input")
        r2 = st.number_input("R2", value=st.session_state.r2, format="%.2f", step=0.01, key="r2_input")
        r1 = st.number_input("R1", value=st.session_state.r1, format="%.2f", step=0.01, key="r1_input")
    
    with col2:
        # Input fields for support levels
        st.subheader("Support Levels")
        s1 = st.number_input("S1", value=st.session_state.s1, format="%.2f", step=0.01, key="s1_input")
        s2 = st.number_input("S2", value=st.session_state.s2, format="%.2f", step=0.01, key="s2_input")
        s3 = st.number_input("S3", value=st.session_state.s3, format="%.2f", step=0.01, key="s3_input")
    
    # Pivot point
    st.subheader("Central Pivot")
    pivot = st.number_input("Pivot", value=st.session_state.pivot, format="%.2f", step=0.01, key="pivot_input")
    
    # Broken levels section
    st.subheader("Broken Levels (Optional)")
    st.markdown("Select any levels that have been recently broken:")
    
    # Create broken levels checkboxes
    col1, col2 = st.columns(2)
    
    with col1:
        broken_r3 = st.checkbox("R3 Broken", key="broken_r3")
        broken_r2 = st.checkbox("R2 Broken", key="broken_r2")
        broken_r1 = st.checkbox("R1 Broken", key="broken_r1")
        broken_pivot = st.checkbox("Pivot Broken", key="broken_pivot")
    
    with col2:
        broken_s1 = st.checkbox("S1 Broken", key="broken_s1")
        broken_s2 = st.checkbox("S2 Broken", key="broken_s2")
        broken_s3 = st.checkbox("S3 Broken", key="broken_s3")
    
    # Button to save pivot levels
    if st.button("Save Pivot Levels", type="primary"):
        # Store all pivot values in session state
        st.session_state.r3 = r3
        st.session_state.r2 = r2
        st.session_state.r1 = r1
        st.session_state.pivot = pivot
        st.session_state.s1 = s1
        st.session_state.s2 = s2
        st.session_state.s3 = s3
        
        # Store broken levels
        broken_levels = []
        if broken_r3: broken_levels.append(("R3", r3))
        if broken_r2: broken_levels.append(("R2", r2))
        if broken_r1: broken_levels.append(("R1", r1))
        if broken_pivot: broken_levels.append(("Pivot", pivot))
        if broken_s1: broken_levels.append(("S1", s1))
        if broken_s2: broken_levels.append(("S2", s2))
        if broken_s3: broken_levels.append(("S3", s3))
        st.session_state.broken_levels = broken_levels
        
        st.session_state.pivot_initialized = True
        st.success("Pivot levels and broken levels saved successfully! You can now switch to the Trade Analysis tab.")
    
    # Visualize pivot levels
    if st.checkbox("Show Pivot Levels Visualization", value=True):
        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Price range
        price_range = [s3, s2, s1, pivot, r1, r2, r3]
        labels = ["S3", "S2", "S1", "Pivot", "R1", "R2", "R3"]
        
        # Create horizontal lines for each level with broken levels shown differently
        for i, (price_level, label) in enumerate(zip(price_range, labels)):
            # Check if this level is in broken_levels
            is_broken = False
            for blevel in st.session_state.broken_levels:
                if blevel[0] == label:
                    is_broken = True
                    break
            
            if is_broken:
                # Use dashed line for broken levels
                ax.axhline(y=price_level, color='orange', linestyle='--', alpha=0.9, linewidth=2)
                ax.text(0.02, price_level, f"{label}: {price_level:.2f} (BROKEN)", verticalalignment='center', fontweight='bold', color='orange')
            else:
                # Use normal colors
                if label.startswith("R"):
                    color = "green"
                elif label.startswith("S"):
                    color = "red"
                else:
                    color = "purple"
                ax.axhline(y=price_level, color=color, linestyle='-', alpha=0.7, linewidth=2)
                ax.text(0.02, price_level, f"{label}: {price_level:.2f}", verticalalignment='center', fontweight='bold', color=color)
        
        # Set the y-limits to be slightly outside the range of values
        y_min = min(price_range) - 2
        y_max = max(price_range) + 2
        ax.set_ylim(y_min, y_max)
        
        # Remove x-axis ticks and labels
        ax.set_xticks([])
        ax.set_xticklabels([])
        
        # Set title and labels
        ax.set_title("SPY Pivot Levels")
        ax.set_ylabel("Price")
        
        # Display the plot
        st.pyplot(fig)

# Tab 2: Trade Analysis
with tab2:
    # Create sidebar for inputs
    st.sidebar.header("Input Values")

    # Current price (for analysis tab)
    current_price = st.sidebar.number_input(
        "Current Price",
        value=st.session_state.price,
        format="%.2f",
        step=0.01,
        key="current_price_analysis"
    )
    
    # SPY EMAs
    st.sidebar.header("SPY EMAs")
    spy_ema8 = st.sidebar.number_input("SPY 8 EMA", value=530.87, format="%.2f", step=0.01)
    spy_ema21 = st.sidebar.number_input("SPY 21 EMA", value=531.40, format="%.2f", step=0.01)

    # CALL EMAs
    st.sidebar.header("CALL EMAs")
    call_ema8 = st.sidebar.number_input("CALL 8 EMA", value=6.27, format="%.2f", step=0.01)
    call_ema21 = st.sidebar.number_input("CALL 21 EMA", value=6.97, format="%.2f", step=0.01)

    # PUT EMAs
    st.sidebar.header("PUT EMAs")
    put_ema8 = st.sidebar.number_input("PUT 8 EMA", value=1.78, format="%.2f", step=0.01)
    put_ema21 = st.sidebar.number_input("PUT 21 EMA", value=1.59, format="%.2f", step=0.01)
    
    # Function to determine nearest support and resistance
    def find_nearest_levels(price):
        # Get all pivot levels
        levels = {
            "R3": st.session_state.r3,
            "R2": st.session_state.r2,
            "R1": st.session_state.r1,
            "Pivot": st.session_state.pivot,
            "S1": st.session_state.s1,
            "S2": st.session_state.s2,
            "S3": st.session_state.s3
        }
        
        # Separate into resistance and support
        resistance_levels = {k: v for k, v in levels.items() if v > price}
        support_levels = {k: v for k, v in levels.items() if v < price}
        
        # Find nearest resistance
        if resistance_levels:
            nearest_resistance_name = min(resistance_levels, key=lambda k: abs(levels[k] - price))
            nearest_resistance = levels[nearest_resistance_name]
        else:
            nearest_resistance_name = "None"
            nearest_resistance = price + 5  # Default if no resistance found
        
        # Find nearest support
        if support_levels:
            nearest_support_name = min(support_levels, key=lambda k: abs(levels[k] - price))
            nearest_support = levels[nearest_support_name]
        else:
            nearest_support_name = "None"
            nearest_support = price - 5  # Default if no support found
        
        return {
            "nearest_resistance": nearest_resistance,
            "nearest_resistance_name": nearest_resistance_name,
            "nearest_support": nearest_support,
            "nearest_support_name": nearest_support_name
        }

    # Get nearest levels
    nearest_levels = find_nearest_levels(current_price)
    
    # Display nearest levels
    st.sidebar.markdown(f"**Nearest Resistance:** ${nearest_levels['nearest_resistance']:.2f} ({nearest_levels['nearest_resistance_name']})")
    st.sidebar.markdown(f"**Nearest Support:** ${nearest_levels['nearest_support']:.2f} ({nearest_levels['nearest_support_name']})")
    
    # Function to automatically determine pivot zone context
    def determine_pivot_context(price, resistance, resistance_name, support, support_name, trend, broken_levels):
        # Calculate threshold for "near" (using 0.3% of price as threshold)
        near_threshold = price * 0.003
        
        # Check if any levels have been broken
        if broken_levels:
            return "Broken support/resistance", f"Recently broken: {', '.join([level[0] for level in broken_levels])}"
        
        # Check distance to nearest levels
        distance_to_resistance = resistance - price
        distance_to_support = price - support
        
        if trend == "UPTREND":
            if distance_to_resistance < near_threshold:
                return "Near bounce zones or reversal levels", f"Price near resistance ({resistance_name}: ${resistance:.2f})"
            elif distance_to_support < near_threshold:
                return "PUTs near resistance or CALLs near support", f"CALLs near support ({support_name}: ${support:.2f})"
            else:
                return "Mid-range", f"Price in middle zone between {support_name} and {resistance_name}"
        
        elif trend == "DOWNTREND":
            if distance_to_support < near_threshold:
                return "Near bounce zones or reversal levels", f"Price near support ({support_name}: ${support:.2f})"
            elif distance_to_resistance < near_threshold:
                return "PUTs near resistance or CALLs near support", f"PUTs near resistance ({resistance_name}: ${resistance:.2f})"
            else:
                return "Mid-range", f"Price in middle zone between {support_name} and {resistance_name}"
        
        else:  # NEUTRAL
            if distance_to_resistance < near_threshold or distance_to_support < near_threshold:
                return "Near bounce zones or reversal levels", f"Price near pivot level in neutral trend"
            else:
                return "Mid-range", f"Price in middle zone in neutral trend"

    # Calculate results button
    calculate_button = st.sidebar.button("Calculate Score & Recommendation", type="primary")

    # Function to determine SPY trend
    def determine_spy_trend(ema8, ema21):
        if ema8 > ema21:
            return "UPTREND", 25, "Uptrend detected (8 EMA > 21 EMA)"
        elif ema8 < ema21:
            return "DOWNTREND", 25, "Downtrend detected (8 EMA < 21 EMA)"
        else:
            return "NEUTRAL", 0, "Neutral trend (8 EMA = 21 EMA)"

    # Function to analyze option chart confirmation
    def analyze_option_confirmation(trend, call_ema8, call_ema21, put_ema8, put_ema21):
        if trend == "UPTREND":
            call_aligned = call_ema8 > call_ema21
            put_aligned = put_ema8 < put_ema21
            call_message = "CALL chart aligned ✓" if call_aligned else "CALL chart not aligned ✗"
            put_message = "PUT chart aligned ✓" if put_aligned else "PUT chart not aligned ✗"
            
            if call_aligned and put_aligned:
                return 25, f"{call_message}, {put_message} - Perfect alignment for UPTREND"
            elif call_aligned:
                return 15, f"{call_message}, {put_message} - Partial alignment for UPTREND"
            else:
                return 0, f"{call_message}, {put_message} - Poor alignment for UPTREND"
        
        elif trend == "DOWNTREND":
            call_aligned = call_ema8 < call_ema21
            put_aligned = put_ema8 > put_ema21
            call_message = "CALL chart aligned ✓" if call_aligned else "CALL chart not aligned ✗"
            put_message = "PUT chart aligned ✓" if put_aligned else "PUT chart not aligned ✗"
            
            if call_aligned and put_aligned:
                return 25, f"{call_message}, {put_message} - Perfect alignment for DOWNTREND"
            elif put_aligned:
                return 15, f"{put_message}, {call_message} - Partial alignment for DOWNTREND"
            else:
                return 0, f"{call_message}, {put_message} - Poor alignment for DOWNTREND"
        
        else:  # NEUTRAL
            return 0, "Neutral SPY trend - Option chart alignment not applicable"

    # Function to analyze opposing option divergence
    def analyze_opposing_option(trend, call_ema8, call_ema21, put_ema8, put_ema21):
        if trend == "UPTREND":
            # In uptrend, PUT should be weak (8 EMA < 21 EMA)
            if put_ema8 < put_ema21:
                return 15, "PUT options weak as expected in uptrend ✓"
            elif put_ema8 == put_ema21:
                return 7.5, "PUT options neutral in uptrend (partial credit) ⚠️"
            else:
                return 0, "PUT options strong in uptrend (contradicting signal) ✗"
        
        elif trend == "DOWNTREND":
            # In downtrend, CALL should be weak (8 EMA < 21 EMA)
            if call_ema8 < call_ema21:
                return 15, "CALL options weak as expected in downtrend ✓"
            elif call_ema8 == call_ema21:
                return 7.5, "CALL options neutral in downtrend (partial credit) ⚠️"
            else:
                return 0, "CALL options strong in downtrend (contradicting signal) ✗"
        
        else:  # NEUTRAL
            return 0, "Neutral SPY trend - Opposing option analysis not applicable"

    # Function to analyze EMA gap
    def analyze_ema_gap(ema8, ema21):
        gap = abs(ema8 - ema21)
        
        if 0.5 <= gap <= 1.0:
            return 10, f"Ideal EMA gap: {gap:.2f} points ✓"
        elif gap > 1.0:
            return -10, f"Overextended EMA gap: {gap:.2f} points ✗"
        else:  # gap < 0.5
            return -5, f"Too tight EMA gap: {gap:.2f} points ⚠️"

    # Function to analyze option trend alignment
    def analyze_option_trend_alignment(trend, call_ema8, call_ema21, put_ema8, put_ema21):
        call_trend = "UP" if call_ema8 > call_ema21 else "DOWN" if call_ema8 < call_ema21 else "NEUTRAL"
        put_trend = "UP" if put_ema8 > put_ema21 else "DOWN" if put_ema8 < put_ema21 else "NEUTRAL"
        
        if trend == "UPTREND":
            if call_trend == "UP" and put_trend == "DOWN":
                return 10, "Both options perfectly aligned with SPY uptrend ✓"
            elif call_trend == "UP" or put_trend == "DOWN":
                return 5, "One option aligned with SPY uptrend, one diverging ⚠️"
            else:
                return 0, "Neither option aligned with SPY uptrend ✗"
        
        elif trend == "DOWNTREND":
            if call_trend == "DOWN" and put_trend == "UP":
                return 10, "Both options perfectly aligned with SPY downtrend ✓"
            elif call_trend == "DOWN" or put_trend == "UP":
                return 5, "One option aligned with SPY downtrend, one diverging ⚠️"
            else:
                return 0, "Neither option aligned with SPY downtrend ✗"
        
        else:  # NEUTRAL
            return 0, "Neutral SPY trend - Option trend alignment not applicable"

    # Function to analyze pivot zone context
    def analyze_pivot_zone(trend, context, context_description):
        if trend == "UPTREND":
            if context == "PUTs near resistance or CALLs near support":
                return 15, f"CALLs near support - favorable entry point ✓ ({context_description})"
            elif context == "Broken support/resistance":
                return 15, f"Broken resistance - favorable for continuation ✓ ({context_description})"
            elif context == "Mid-range":
                return 7.5, f"Price in mid-range - moderately favorable ⚠️ ({context_description})"
            else:  # Near bounce zones
                return -5, f"Price near potential reversal level - unfavorable ✗ ({context_description})"
        
        elif trend == "DOWNTREND":
            if context == "PUTs near resistance or CALLs near support":
                return 15, f"PUTs near resistance - favorable entry point ✓ ({context_description})"
            elif context == "Broken support/resistance":
                return 15, f"Broken support - favorable for continuation ✓ ({context_description})"
            elif context == "Mid-range":
                return 7.5, f"Price in mid-range - moderately favorable ⚠️ ({context_description})"
            else:  # Near bounce zones
                return -5, f"Price near potential reversal level - unfavorable ✗ ({context_description})"
        
        else:  # NEUTRAL
            return 0, f"Neutral SPY trend - Pivot zone analysis not applicable ({context_description})"

    # Main calculation function
    def calculate_score_and_recommendation():
        # Calculate trend first (needed for context detection)
        trend, trend_score, trend_msg = determine_spy_trend(spy_ema8, spy_ema21)
        
        # Auto-detect pivot zone context
        pivot_context, context_description = determine_pivot_context(
            current_price,
            nearest_levels['nearest_resistance'],
            nearest_levels['nearest_resistance_name'],
            nearest_levels['nearest_support'],
            nearest_levels['nearest_support_name'],
            trend,
            st.session_state.broken_levels
        )
        
        # Calculate scores for each pillar
        option_confirm_score, option_confirm_msg = analyze_option_confirmation(
            trend, call_ema8, call_ema21, put_ema8, put_ema21
        )
        
        opposing_score, opposing_msg = analyze_opposing_option(
            trend, call_ema8, call_ema21, put_ema8, put_ema21
        )
        
        ema_gap_score, ema_gap_msg = analyze_ema_gap(spy_ema8, spy_ema21)
        
        option_alignment_score, option_alignment_msg = analyze_option_trend_alignment(
            trend, call_ema8, call_ema21, put_ema8, put_ema21
        )
        
        pivot_score, pivot_msg = analyze_pivot_zone(
            trend, pivot_context, context_description
        )
        
        # Calculate total score
        total_score = trend_score + option_confirm_score + opposing_score + ema_gap_score + option_alignment_score + pivot_score
        
        # Cap total score at 100
        total_score = min(100, max(0, total_score))
        
        # Determine recommendation
        if total_score >= 90:
            if trend == "UPTREND":
                recommendation = "BUY CALLS"
                color = "green"
            elif trend == "DOWNTREND":
                recommendation = "BUY PUTS"
                color = "red"
            else:
                recommendation = "NO TRADE"
                color = "orange"
        elif total_score >= 70:
            recommendation = "WAIT FOR CONFIRMATION"
            color = "orange"
        else:
            recommendation = "NO TRADE"
            color = "red"
        
        # Create results dictionary
        results = {
            "trend": trend,
            "total_score": total_score,
            "recommendation": recommendation,
            "color": color,
            "pivot_context": pivot_context,
            "context_description": context_description,
            "details": [
                {"category": "1. SPY EMA Trend", "score": trend_score, "message": trend_msg, "weight": "25%"},
                {"category": "2. Option Chart Confirmation", "score": option_confirm_score, "message": option_confirm_msg, "weight": "25%"},
                {"category": "3. Opposing Option Divergence", "score": opposing_score, "message": opposing_msg, "weight": "15%"},
                {"category": "4. EMA Gap Size", "score": ema_gap_score, "message": ema_gap_msg, "weight": "10%"},
                {"category": "5. Option Trend Alignment", "score": option_alignment_score, "message": option_alignment_msg, "weight": "10%"},
                {"category": "6. Pivot Zone Context", "score": pivot_score, "message": pivot_msg, "weight": "15%"}
            ]
        }
        
        return results

    # Show information before calculation
    if not calculate_button:
        # Show instructions when first loading the app
        st.info("Enter your EMA values and current price in the sidebar, then click 'Calculate Score & Recommendation' to analyze your trading setup.")
        
        # Show framework explanation
        st.header("Yetitrader 4-Pillar Framework")
        
        st.markdown("""
        ### The 4 Core Pillars:
        
        1. **EMA Trend Confirmation (SPY 8/21 EMAs)**
           * 8 EMA > 21 EMA → SPY is in an uptrend → Look for CALL entries
           * 8 EMA < 21 EMA → SPY is in a downtrend → Look for PUT entries
        
        2. **Option Chart Agreement (CALL & PUT EMAs)**
           * In UPTREND: CALL chart should show 8 EMA > 21 EMA, PUT chart should show 8 EMA < 21 EMA
           * In DOWNTREND: PUT chart should show 8 EMA > 21 EMA, CALL chart should show 8 EMA < 21 EMA
        
        3. **EMA Gap Analysis**
           * Gap between 8 EMA and 21 EMA matters
           * Small/moderate gap (0.5-1.0 points) → good timing for entry
           * Large gap (>1.0 points) → overextended move → wait for pullback
           * Too tight (<0.5 points) → indecisive market → wait for confirmation
        
        4. **Pivot Zone Awareness**
           * Never enter blindly near support or resistance
           * In a downtrend → don't buy PUTs into support
           * In an uptrend → don't buy CALLs into resistance
           * Broken support/resistance creates favorable continuation scenarios
        """)
        
        st.markdown("""
        ### Confidence Score Interpretation:
        
        * **90-100%**: Ideal alignment — Execute trade
        * **70-89%**: Decent setup, minor caution — Wait for confirmation
        * **60-74%**: Mixed signals — Riskier entry
        * **<60%**: Contradictory signals — Avoid trade
        """)

        # Display current pivot levels
        st.subheader("Current Pivot Levels")
        
        # Calculate trend for the visual (using the default values)
        default_trend, _, _ = determine_spy_trend(spy_ema8, spy_ema21)
        
        # Auto-detect pivot zone context for visualization
        default_context, default_context_desc = determine_pivot_context(
            current_price,
            nearest_levels['nearest_resistance'],
            nearest_levels['nearest_resistance_name'],
            nearest_levels['nearest_support'],
            nearest_levels['nearest_support_name'],
            default_trend,
            st.session_state.broken_levels
        )
        
        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Price range
        price_range = [
            st.session_state.s3,
            st.session_state.s2,
            st.session_state.s1,
            st.session_state.pivot,
            st.session_state.r1,
            st.session_state.r2,
            st.session_state.r3
        ]
        labels = ["S3", "S2", "S1", "Pivot", "R1", "R2", "R3"]
        
        # Create horizontal lines for each level
        for i, (price_level, label) in enumerate(zip(price_range, labels)):
            # Check if this level is in broken_levels
            is_broken = False
            for blevel in st.session_state.broken_levels:
                if blevel[0] == label:
                    is_broken = True
                    break
            
            if is_broken:
                # Use dashed line for broken levels
                ax.axhline(y=price_level, color='orange', linestyle='--', alpha=0.9, linewidth=2)
                ax.text(0.02, price_level, f"{label}: {price_level:.2f} (BROKEN)", verticalalignment='center', fontweight='bold', color='orange')
            else:
                # Use normal colors
                if label.startswith("R"):
                    color = "green"
                elif label.startswith("S"):
                    color = "red"
                else:
                    color = "purple"
                ax.axhline(y=price_level, color=color, linestyle='-', alpha=0.7, linewidth=2)
                ax.text(0.02, price_level, f"{label}: {price_level:.2f}", verticalalignment='center', fontweight='bold', color=color)
        
        # Highlight current price
        ax.axhline(y=current_price, color='blue', linestyle='--', linewidth=2)
        ax.text(0.02, current_price, f"Current: {current_price:.2f}", verticalalignment='center', fontweight='bold', color='blue')
        
        # Add context information
        ax.text(0.5, 0.02, f"Context: {default_context} - {default_context_desc}",
                transform=ax.transAxes, horizontalalignment='center',
                fontweight='bold', fontsize=10, color='blue',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue', boxstyle='round,pad=0.5'))
        
        # Set the y-limits to be slightly outside the range of values
        y_min = min(price_range + [current_price]) - 2
        y_max = max(price_range + [current_price]) + 2
        ax.set_ylim(y_min, y_max)
        
        # Remove x-axis ticks and labels
        ax.set_xticks([])
        ax.set_xticklabels([])
        
        # Set title and labels
        ax.set_title("SPY Pivot Levels with Current Price")
        ax.set_ylabel("Price")
        
        # Display the plot
        st.pyplot(fig)
        
        # Display current pivot levels
        pivot_data = pd.DataFrame([
            {"Level": "R3", "Value": st.session_state.r3, "Status": "Broken" if any(x[0] == "R3" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "R2", "Value": st.session_state.r2, "Status": "Broken" if any(x[0] == "R2" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "R1", "Value": st.session_state.r1, "Status": "Broken" if any(x[0] == "R1" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "Pivot", "Value": st.session_state.pivot, "Status": "Broken" if any(x[0] == "Pivot" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "Current Price", "Value": current_price, "Status": ""},
            {"Level": "S1", "Value": st.session_state.s1, "Status": "Broken" if any(x[0] == "S1" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "S2", "Value": st.session_state.s2, "Status": "Broken" if any(x[0] == "S2" for x in st.session_state.broken_levels) else "Active"},
            {"Level": "S3", "Value": st.session_state.s3, "Status": "Broken" if any(x[0] == "S3" for x in st.session_state.broken_levels) else "Active"}
        ])
        st.table(pivot_data)
        
        # Display detected context
        st.subheader("Auto-Detected Context")
        st.info(f"**{default_context}**: {default_context_desc}")
    else:
        # Calculate scores
        results = calculate_score_and_recommendation()
        
        # Display results in columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display trend and recommendation
            st.header("Analysis Results")
            st.subheader(f"SPY Trend: {results['trend']}")
            
            # Display confidence score with progress bar
            st.subheader("Confidence Score")
            st.progress(results['total_score']/100)
            st.markdown(f"### Score: {results['total_score']}%")
            
            # Display recommendation
            st.markdown(f"## Recommendation: <span style='color:{results['color']}'>{results['recommendation']}</span>", unsafe_allow_html=True)
            
            # Display auto-detected pivot context
            st.subheader("Pivot Zone Context")
            st.info(f"**{results['pivot_context']}**: {results['context_description']}")
            
            # Display detailed scores
            st.subheader("Detailed Analysis")
            
            # Create a DataFrame for better display
            details_df = pd.DataFrame(results['details'])
            
            # Format the DataFrame
            for i, row in details_df.iterrows():
                st.markdown(f"**{row['category']}** (Weight: {row['weight']})")
                if row['score'] > 0:
                    score_color = "green"
                elif row['score'] < 0:
                    score_color = "red"
                else:
                    score_color = "gray"
                st.markdown(f"Score: <span style='color:{score_color}'>{row['score']}</span>", unsafe_allow_html=True)
                st.markdown(f"{row['message']}")
                st.markdown("---")
        
        with col2:
            # Create a pie chart of score contributions
            st.subheader("Score Breakdown")
            
            # Get positive scores only for the pie chart
            positive_scores = [max(0, detail['score']) for detail in results['details']]
            labels = [detail['category'].split('.')[1].strip() for detail in results['details']]
            
            # Only include categories with positive scores
            filtered_labels = []
            filtered_scores = []
            for label, score in zip(labels, positive_scores):
                if score > 0:
                    filtered_labels.append(label)
                    filtered_scores.append(score)
            
            # Create pie chart if there are positive scores
            if sum(filtered_scores) > 0:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(filtered_scores, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.write("No positive score contributions to display.")
            
            # Display EMA values for reference
            st.subheader("EMA Values")
            ema_data = {
                "Asset": ["SPY", "CALL", "PUT"],
                "8 EMA": [spy_ema8, call_ema8, put_ema8],
                "21 EMA": [spy_ema21, call_ema21, put_ema21]
            }
            ema_df = pd.DataFrame(ema_data)
            st.table(ema_df)
            
            # Create a figure for pivot visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Price range
            price_range = [
                st.session_state.s3,
                st.session_state.s2,
                st.session_state.s1,
                st.session_state.pivot,
                st.session_state.r1,
                st.session_state.r2,
                st.session_state.r3
            ]
            labels = ["S3", "S2", "S1", "Pivot", "R1", "R2", "R3"]
            
            # Create horizontal lines for each level
            for i, (price_level, label) in enumerate(zip(price_range, labels)):
                # Check if this level is in broken_levels
                is_broken = False
                for blevel in st.session_state.broken_levels:
                    if blevel[0] == label:
                        is_broken = True
                        break
                
                if is_broken:
                    # Use dashed line for broken levels
                    ax.axhline(y=price_level, color='orange', linestyle='--', alpha=0.9, linewidth=2)
                    ax.text(0.02, price_level, f"{label}: {price_level:.2f} (BROKEN)", verticalalignment='center', fontweight='bold', color='orange')
                else:
                    # Use normal colors
                    if label.startswith("R"):
                        color = "green"
                    elif label.startswith("S"):
                        color = "red"
                    else:
                        color = "purple"
                    ax.axhline(y=price_level, color=color, linestyle='-', alpha=0.7, linewidth=2)
                    ax.text(0.02, price_level, f"{label}: {price_level:.2f}", verticalalignment='center', fontweight='bold', color=color)
            
            # Highlight current price
            ax.axhline(y=current_price, color='blue', linestyle='--', linewidth=2)
            ax.text(0.02, current_price, f"Current: {current_price:.2f}", verticalalignment='center', fontweight='bold', color='blue')
            
            # Add context information
            ax.text(0.5, 0.02, f"Context: {results['pivot_context']}",
                    transform=ax.transAxes, horizontalalignment='center',
                    fontweight='bold', fontsize=10, color='blue',
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue', boxstyle='round,pad=0.5'))
            
            # Set the y-limits to be slightly outside the range of values
            y_min = min(price_range + [current_price]) - 2
            y_max = max(price_range + [current_price]) + 2
            ax.set_ylim(y_min, y_max)
            
            # Remove x-axis ticks and labels
            ax.set_xticks([])
            ax.set_xticklabels([])
            
            # Set title and labels
            ax.set_title("SPY Pivot Levels with Current Price")
            ax.set_ylabel("Price")
            
            # Display the plot
            st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("*Yetitrader 4-Pillar Framework Analyzer - For educational purposes only*")
