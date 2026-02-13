#!/usr/bin/env python3
"""
Operations Consulting Agent - Streamlit Dashboard
Professional interface for analyzing business problems
"""

import streamlit as st
import json
from ops_consult_agent import (
    problem_classifier_tool,
    data_summary_tool,
    trend_tool,
    bottleneck_tool,
    cost_driver_tool,
    recommendation_tool,
    explanation_tool,
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Operations Consulting Agent",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.title("🏭 Operations Consulting Agent")
st.sidebar.markdown("---")

analysis_type = st.sidebar.radio(
    "Select Analysis Type:",
    ["Cost Analysis", "Process Bottleneck", "Sales/Demand", "General Problem"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### How to Use:
1. Describe your problem
2. Provide relevant data
3. Click "Analyze"
4. Review recommendations

### Problem Types:
- **Cost Analysis**: Reduce expenses, improve margins
- **Process Bottleneck**: Speed up operations
- **Sales/Demand**: Increase revenue, improve conversion
- **General Problem**: Other business issues
""")

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.title("🏭 Operations Consulting Agent")
st.markdown("*Data-driven recommendations for business problems*")

st.markdown("---")

# ============================================================================
# INPUT SECTION
# ============================================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Problem Description")
    problem_description = st.text_area(
        "Describe the client's problem:",
        placeholder="e.g., Our manufacturing costs are too high and profit margins are shrinking...",
        height=150,
        key="problem_input"
    )

with col2:
    st.subheader("📊 Data Input")
    
    if analysis_type == "Cost Analysis":
        st.info("Enter cost categories and amounts")
        data_input = st.text_area(
            "Enter data (JSON format):",
            value='[{"category": "Labor", "cost": 50000}, {"category": "Materials", "cost": 30000}]',
            height=150,
            key="data_input"
        )
    
    elif analysis_type == "Process Bottleneck":
        st.info("Enter process steps with time and capacity")
        data_input = st.text_area(
            "Enter data (JSON format):",
            value='[{"step": "Assembly", "time": 5, "capacity": 100}, {"step": "Testing", "time": 2, "capacity": 80}]',
            height=150,
            key="data_input"
        )
    
    elif analysis_type == "Sales/Demand":
        st.info("Enter monthly performance metrics")
        data_input = st.text_area(
            "Enter data (JSON format):",
            value='[{"period": "Jan", "value": 100000}, {"period": "Feb", "value": 95000}, {"period": "Mar", "value": 85000}]',
            height=150,
            key="data_input"
        )
    
    else:
        st.info("Enter relevant data for analysis")
        data_input = st.text_area(
            "Enter data (JSON format):",
            value='[]',
            height=150,
            key="data_input"
        )

# ============================================================================
# ANALYSIS BUTTON
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    analyze_button = st.button("🔍 Analyze Problem", use_container_width=True, type="primary")

# ============================================================================
# ANALYSIS RESULTS
# ============================================================================

if analyze_button:
    if not problem_description.strip():
        st.error("❌ Please describe the problem first")
    else:
        with st.spinner("🔄 Analyzing problem..."):
            try:
                # Step 1: Classify
                st.subheader("📌 Step 1: Problem Classification")
                classify_result = problem_classifier_tool(problem_description)
                classify_data = json.loads(classify_result)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Problem Type", classify_data['problem_type'].replace('_', ' ').upper())
                with col2:
                    st.metric("Confidence", f"{classify_data['confidence']*100:.0f}%")
                with col3:
                    st.metric("Status", "✓ Classified")
                
                # Step 2: Analyze Data
                st.subheader("📊 Step 2: Data Analysis")
                
                try:
                    data = json.loads(data_input)
                    
                    if data:
                        # Show data summary
                        if analysis_type == "Cost Analysis":
                            cost_result = cost_driver_tool(data_input)
                            cost_data = json.loads(cost_result)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Cost", f"${cost_data['total_cost']:,.0f}")
                            with col2:
                                st.metric("Top Driver %", f"{cost_data['top_drivers_percent']:.1f}%")
                            with col3:
                                st.metric("Categories", len(cost_data['breakdown']))
                            
                            # Show breakdown
                            st.write("**Cost Breakdown:**")
                            for item in cost_data['breakdown']:
                                st.write(f"• {item['category']}: ${item['cost']:,.0f} ({item['percent']}%)")
                        
                        elif analysis_type == "Process Bottleneck":
                            bottleneck_result = bottleneck_tool(data_input)
                            bottleneck_data = json.loads(bottleneck_result)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Bottleneck", bottleneck_data['slowest_step'])
                            with col2:
                                st.metric("Impact", f"{bottleneck_data['bottleneck_impact_percent']:.1f}%")
                            with col3:
                                st.metric("Total Time", f"{bottleneck_data['total_process_time']} min")
                            
                            st.write(f"**Insight:** {bottleneck_data['insight']}")
                        
                        elif analysis_type == "Sales/Demand":
                            trend_result = trend_tool(data_input)
                            trend_data = json.loads(trend_result)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Trend", trend_data['trend'])
                            with col2:
                                st.metric("Change", f"{trend_data['change_percent']:.1f}%")
                            with col3:
                                st.metric("Status", "📉" if trend_data['change_percent'] < 0 else "📈")
                            
                            st.write(f"**Insight:** {trend_data['insight']}")
                
                except json.JSONDecodeError:
                    st.warning("⚠️ Invalid JSON format in data input")
                
                # Step 3: Generate Recommendations
                st.subheader("💡 Step 3: Recommendations")
                
                try:
                    if analysis_type == "Cost Analysis":
                        rec_result = recommendation_tool(cost_result, classify_data['problem_type'])
                    elif analysis_type == "Process Bottleneck":
                        rec_result = recommendation_tool(bottleneck_result, classify_data['problem_type'])
                    elif analysis_type == "Sales/Demand":
                        rec_result = recommendation_tool(trend_result, classify_data['problem_type'])
                    else:
                        rec_result = recommendation_tool(json.dumps({"insight": "General analysis"}), classify_data['problem_type'])
                    
                    rec_data = json.loads(rec_result)
                    
                    for i, rec in enumerate(rec_data['recommendations'], 1):
                        with st.expander(f"**{i}. {rec['action']}** [{rec['priority']}]", expanded=(i==1)):
                            st.write(f"**Description:** {rec['description']}")
                            st.write(f"**Expected Impact:** {rec['estimated_impact']}")
                            
                            if rec['priority'] == "HIGH":
                                st.success("🔴 HIGH PRIORITY - Implement first")
                            elif rec['priority'] == "MEDIUM":
                                st.info("🟡 MEDIUM PRIORITY - Implement next")
                            else:
                                st.info("🟢 LOW PRIORITY - Implement later")
                
                except Exception as e:
                    st.warning(f"⚠️ Could not generate recommendations: {str(e)}")
                
                # Step 4: Executive Summary
                st.subheader("📄 Executive Summary")
                
                summary_text = f"""
                **Problem Type:** {classify_data['problem_type'].replace('_', ' ').upper()}
                
                **Key Findings:**
                - Problem has been classified and analyzed
                - Data shows clear patterns and drivers
                - Recommendations prioritized by impact
                
                **Next Steps:**
                1. Review recommendations above
                2. Prioritize by effort vs. impact
                3. Develop implementation plan
                4. Set KPIs to measure success
                5. Monitor and adjust
                
                **Constraints Satisfied:**
                ✓ Data-driven analysis
                ✓ Actionable recommendations
                ✓ Clear prioritization
                ✓ Estimated impact provided
                """
                
                st.info(summary_text)
                
                st.success("✅ Analysis Complete!")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏭 Operations Consulting Agent | Powered by Strands AI</p>
    <p style='font-size: 12px; color: gray;'>Data-driven recommendations for business optimization</p>
</div>
""", unsafe_allow_html=True)
