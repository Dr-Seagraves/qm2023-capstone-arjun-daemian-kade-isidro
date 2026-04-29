#!/usr/bin/env python3
"""Generate a PowerPoint presentation for the capstone project."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def add_title_slide(prs, title, subtitle):
    """Add a title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(44, 62, 80)  # Dark blue/gray
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(236, 240, 241)
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(2))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.word_wrap = True
    p = subtitle_frame.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(189, 195, 199)
    
    return slide

def add_content_slide(prs, title, content_points):
    """Add a content slide with bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.7))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(44, 62, 80)
    
    # Add a line
    line = slide.shapes.add_connector(1, Inches(0.5), Inches(1.1), Inches(9.5), Inches(1.1))
    line.line.color.rgb = RGBColor(52, 152, 219)
    line.line.width = Pt(2)
    
    # Content
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(8.4), Inches(5.5))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, point in enumerate(content_points):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.text = point
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(44, 62, 80)
        p.level = 0
        p.space_before = Pt(6)
        p.space_after = Pt(6)
    
    return slide

# Create presentation
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Slide 1: Title
add_title_slide(prs, 
    "Corruption, Crime, and Foreign Investment",
    "QM 2023 Capstone Project\nArjun • Daemian • Kade • Isidro")

# Slide 2: Research Question
add_content_slide(prs,
    "Research Question",
    [
        "How does perceived corruption and crime of a country affect foreign direct investment?",
        "",
        "Key Variables:",
        "• Corruption Perceptions Index (CPI) – Transparency International",
        "• Crime Index – Numbeo",
        "• Geopolitical Economic Policy Uncertainty (GEPU)",
        "• Foreign Direct Investment (FDI) – World Bank",
        "",
        "Sample: 20 countries, 2012–2025 (237 country-year observations)"
    ])

# Slide 3: Hypotheses
add_content_slide(prs,
    "Hypotheses",
    [
        "H1: As corruption increases, foreign investment decreases",
        "",
        "H2: Crime rates have a measurable impact on economic uncertainty",
        "",
        "H3: Perceived corruption (CPI) is the biggest determinant of FDI among our chosen factors",
        "",
        "Expected mechanism: Investors respond to governance quality and institutional risk"
    ])

# Slide 4: Data Sources
add_content_slide(prs,
    "Data Sources & Quality",
    [
        "✓ Crime Index: Numbeo (https://www.numbeo.com/crime/)",
        "",
        "✓ Foreign Direct Investment: World Bank",
        "  (https://data.worldbank.org/indicator/BX.KLT.DINV.CD.WD)",
        "",
        "✓ Corruption Perceptions Index: Transparency International",
        "  (https://www.transparency.org)",
        "",
        "✓ Geopolitical Uncertainty: Policy Uncertainty Index",
        "  (https://www.policyuncertainty.com)",
        "",
        "All data: Annual frequency, 2012–2025"
    ])

# Slide 5: EDA Key Findings
add_content_slide(prs,
    "M2: Exploratory Data Analysis Findings",
    [
        "Weak negative correlation (r = -0.14) between FDI and CPI score",
        "   ↳ Makes intuitive sense: higher corruption → lower investment",
        "",
        "Optimal lag: 12 years (captures longer-term investment relationships)",
        "",
        "Most sensitive countries: Singapore, Sweden, Ireland",
        "   ↳ Changes in CPI have outsized impact on FDI perceptions",
        "",
        "⚠ China identified as outlier with atypical investment patterns",
        "",
        "Seasonal patterns evident in time series"
    ])

# Slide 6: Methodology
add_content_slide(prs,
    "Methodology: Model A (Econometric)",
    [
        "Two-Way Fixed Effects Model (Required approach)",
        "",
        "Outcome: log(|FDI|) – signed log transform",
        "",
        "Key driver: CPI score (lagged)",
        "",
        "Controls: Crime Index, Geopolitical Uncertainty (GEPU)",
        "",
        "Fixed effects: Country and Year",
        "",
        "SEs: Clustered by country to account for within-country correlation"
    ])

# Slide 7: Main Results
add_content_slide(prs,
    "Model A: Main Results",
    [
        "CPI Score (lagged 1-year):",
        "   Coefficient: -0.1135   |   p-value: 0.4238   |   NOT significant",
        "",
        "GEPU (Geopolitical Uncertainty):",
        "   Coefficient: -0.0159   |   p-value: 0.1876   |   NOT significant",
        "",
        "Model Fit:",
        "   Within R²: 0.0149 (low explanatory power)",
        "   F-test p-value: 0.1832",
        "",
        "⚠ Interpretation: CPI effect is small and not statistically robust"
    ])

# Slide 8: Model Comparison
add_content_slide(prs,
    "Model B: Machine Learning Comparison",
    [
        "Does Random Forest better predict FDI than OLS?",
        "",
        "Out-of-sample Performance:",
        "   OLS:           RMSE = 15.42   |   R² = -0.053",
        "   Random Forest: RMSE = 14.64   |   R² = 0.052",
        "",
        "Verdict: Modest improvement (~5% RMSE reduction)",
        "",
        "Trade-off: RF better for prediction but less interpretable",
        "   Prefer OLS for causal inference about corruption effects"
    ])

# Slide 9: Diagnostics
add_content_slide(prs,
    "Diagnostics & Robustness Checks",
    [
        "Heteroskedasticity (Breusch-Pagan):",
        "   p-value: 0.056 → Slight evidence, but marginal",
        "   Use of clustered SEs justified as conservative approach",
        "",
        "Multicollinearity: Controlled, VIF values acceptable",
        "",
        "Robustness tests:",
        "   • Alternative lags (1, 2, 3 years) → Unstable effects",
        "   • Exclude 2020 → Coefficients change meaningfully",
        "   • Crime-based subsamples → No stable pattern"
    ])

# Slide 10: Policy Implications
add_content_slide(prs,
    "Policy Recommendations",
    [
        "1. Prioritize BROAD investment-climate reforms",
        "   ↳ CPI alone is insufficient; must improve contract enforcement,",
        "      regulatory consistency, and transparency",
        "",
        "2. Address uncertainty and risk in high-crime environments",
        "   ↳ Offer political-risk insurance, faster permitting, security measures",
        "",
        "3. Expect gradual, not immediate, FDI responses to reforms",
        "   ↳ Institutional trust builds over time (explains 12-year optimal lag)",
        "",
        "4. Monitor scenario outcomes (Baseline, Improvement, Stress)"
    ])

# Slide 11: Limitations
add_content_slide(prs,
    "Limitations & Risks",
    [
        "Small sample: Only 20 countries with complete data",
        "",
        "Omitted variables: GDP growth, exchange rates, tax policy, trade openness",
        "",
        "Endogeneity: Does FDI drive corruption reforms, or vice versa?",
        "",
        "Measurement: CPI is perception-based; crime data are survey estimates",
        "",
        "Crisis sensitivity: Results sensitive to 2020 inclusion",
        "",
        "Generalizability: Cannot confidently apply to countries outside sample"
    ])

# Slide 12: Future Directions
add_content_slide(prs,
    "Future Research Directions",
    [
        "✓ Add macro controls: GDP growth, inflation, sovereign debt",
        "",
        "✓ Test heterogeneous effects by region, income group, or sector",
        "",
        "✓ Extend sample: More countries and longer time periods for power",
        "",
        "✓ Explore nonlinearities: Does corruption matter more above a threshold?",
        "",
        "✓ Investigate causal pathways: Mediation analysis through institutional channels",
        "",
        "✓ Alternative governance measures: World Bank GEI, Rule of Law Index"
    ])

# Slide 13: Conclusion
add_content_slide(prs,
    "Conclusion",
    [
        "Finding: Weak statistical relationship between CPI and FDI in this sample",
        "",
        "Key takeaway: FDI is driven by broader risk environment, not corruption alone",
        "",
        "Policy insight: Multi-dimensional reform strategy more effective than",
        "anti-corruption focus in isolation",
        "",
        "Data-driven recommendation: Invest in uncertainty reduction and",
        "institutional credibility alongside corruption control",
        "",
        "Next step: Expand sample and incorporate additional institutional variables"
    ])

# Save
prs.save('Capstone_Project_Presentation.pptx')
print("✓ Presentation created: Capstone_Project_Presentation.pptx")
