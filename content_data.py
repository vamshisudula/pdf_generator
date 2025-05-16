"""
This file contains the dynamic content for the investment proposal PDF generator.
Add or modify content as needed for different sections of the proposal.
"""

# Market Outlook content
market_outlook_content = """
The current market outlook presents a mixed picture with both opportunities and challenges. 
Equity markets have shown resilience despite global economic uncertainties, with key indices 
demonstrating moderate growth over the past quarter. Fixed income markets are adjusting to 
the changing interest rate environment, creating potential for strategic positioning.

Emerging markets continue to offer growth potential, particularly in sectors aligned with 
technological innovation and sustainable development. However, investors should remain 
cautious of volatility triggered by geopolitical tensions and inflationary pressures.
"""

# Debt Overview content
debt_overview_content = """
The debt market is experiencing significant shifts due to changing monetary policies. 
Government securities offer stability but with modest returns, while corporate bonds 
present higher yields with corresponding credit risk. The yield curve suggests potential 
for strategic duration positioning.

Credit quality remains a key consideration, with selective high-yield opportunities 
emerging in specific sectors. Inflation-protected securities may offer value as a 
hedge against persistent price pressures.
"""

# Asset Allocation content
asset_allocation_content = """
Our recommended asset allocation strategy balances growth opportunities with risk 
management. We suggest a diversified approach with:
- 45% allocation to equities (30% domestic, 15% international)
- 30% allocation to fixed income securities
- 10% allocation to alternative investments
- 15% allocation to cash and equivalents

This balanced approach aims to capture market upside while providing downside protection 
through diversification across asset classes.
"""

# Asset Allocation structured data
# Percentages
equity_percentage = "50%"
debt_percentage = "50%"

# Total amount
total_amount = "3.75 Cr."

# Mutual funds breakdown (use <br /> for line breaks)
mutual_funds_breakdown = "Large Cap Fund - 50 Lacs.<br />Global Funds - 50 Lacs.<br />Hybrid Fund/Multi Asset Fund - 50 Lacs.<br />Thematic Fund - 25 Lacs."

# Asset class amounts
mutual_funds_amount = "2.75 Cr."
pms_amount = "1.00 Cr."
private_equity_amount = "0.50 Cr."
debt_amount = "0.50 Cr."

# Mutual Fund content
mutual_fund_content = """
Our mutual fund recommendations focus on funds with consistent performance, experienced 
management teams, and reasonable expense ratios. We've identified several funds across 
categories that align with our overall investment strategy:

Large Cap: XYZ Growth Fund, ABC Blue Chip Fund
Mid Cap: LMN Opportunities Fund
Small Cap: PQR Emerging Companies Fund
Debt: STU Short Duration Fund, VWX Corporate Bond Fund
"""

# PMS content
pms_content = """
For investors seeking personalized portfolio management, our PMS offerings provide 
tailored investment solutions with active management and regular performance reviews. 
Our flagship strategies include:

Growth Strategy: Focused on high-growth companies with strong fundamentals
Value Strategy: Targeting undervalued companies with potential for price appreciation
Balanced Strategy: Combining growth and value approaches for moderate risk profile
"""

# Fixed Income content
fixed_income_content = """
Our fixed income recommendations aim to balance yield with safety. Current opportunities 
include:
- AAA-rated corporate bonds with 3-5 year duration
- Select AA+ rated PSU bonds offering yield premium
- Short-term government securities for liquidity management
- Strategic allocation to floating rate instruments

These selections are designed to provide regular income while managing interest rate risk.
"""

# Private Equity content
private_equity_content = """
For qualified investors, private equity offers potential for enhanced returns through 
access to non-public companies. Our recommended approach includes:
- Allocation to established PE funds with proven track records
- Focus on sectors with strong growth potential including healthcare, technology, and renewable energy
- Consideration of venture capital for early-stage exposure
- Structured approach to manage illiquidity risk

Private equity investments should typically constitute 5-10% of the overall portfolio for suitable investors.
"""

# Direct Equity content
direct_equity_content = """
Our direct equity recommendations focus on companies with strong fundamentals, sustainable 
competitive advantages, and reasonable valuations. Current sector preferences include:
- Financial services: Leading private banks and select NBFCs
- Information Technology: Companies with digital transformation capabilities
- Healthcare: Pharmaceutical companies with strong R&D pipelines
- Consumer: Companies with established brands and distribution networks

Stock selection is based on thorough fundamental analysis, with regular monitoring and portfolio rebalancing.
"""

# Variable mapping for template variables
textareaContent = ""  # This will be set dynamically based on the file

# Mutual Fund table data
mutual_fund_names = """HDFC Top 100 Fund<br />Nippon India Large cap Fund<br />ICICI Bluechip Fund<br />Bajaj Finserv large Cap
Fund<br />Motilal Oswal Nasdaq 100 Fund of Fund<br />ICICI Prudential US Bluechip Equity Fund<br />Nippon
India US Equity Opportunites Fund<br />HDFC Balance Advantage Fund<br />SBI Balance Advantage Fund<br />ICICI
Prudential Multi asset Fund"""

mutual_fund_categories = """LargeCap<br />LargeCap<br />Large Cap<br />Large Cap<br />Global Fund<br />Global Fund<br />Global Fund<br />Hybrid<br />Hybrid<br />Multi
Asset"""

mutual_fund_returns_1yr = """10.50%<br />9.75%<br />11.20%<br />8.90%<br />15.30%<br />12.80%<br />14.20%<br />7.90%<br />8.50%<br />9.30%<br />16.40%<br />13.70%"""

mutual_fund_returns_3yr = """12.30%<br />11.50%<br />13.40%<br />10.20%<br />18.70%<br />14.90%<br />16.80%<br />9.50%<br />10.20%<br />11.40%<br />19.80%<br />15.90%"""

mutual_fund_returns_5yr = """14.80%<br />13.20%<br />15.70%<br />12.50%<br />21.40%<br />17.30%<br />19.50%<br />11.80%<br />12.60%<br />13.90%<br />22.50%<br />18.20%"""

# PMS data
pms_names = """Seven Island Multi Cap Fund<br />Marcellus Consistent Compounder<br />ASK India Select Portfolio"""
pms_categories = """PMS<br />PMS<br />PMS"""
pms_amounts = """0.50Cr<br />0.25Cr<br />0.25Cr"""
pms_target = "Target: 1.00Cr"

# Fixed Income data
fixed_income_data = """
<tr>
  <td>10.5% SATIN CREDITCARE NETWORK LIMITED 2027</td>
  <td>28 Jan 2027(M)</td>
  <td>Monthly</td>
  <td>10.50%</td>
  <td>10 Lac</td>
  <td class="senior-secured">Senior Secured</td>
  <td>1,00,000</td>
  <td>A by ICRA</td>
</tr>
<tr>
  <td>11.25% IIFL HOME FINANCE LIMITED 2028</td>
  <td>15 Feb 2028(M)</td>
  <td>Monthly</td>
  <td>11.25%</td>
  <td>15 Lac</td>
  <td class="senior-secured">Senior Secured</td>
  <td>1,00,000</td>
  <td>AA by CRISIL</td>
</tr>
<tr>
  <td>9.75% SHRIRAM TRANSPORT FINANCE COMPANY LTD 2025</td>
  <td>20 Aug 2025(M)</td>
  <td>Quarterly</td>
  <td>9.75%</td>
  <td>10 Lac</td>
  <td class="senior-secured">Senior Secured</td>
  <td>1,00,000</td>
  <td>AA+ by CRISIL</td>
</tr>
<tr>
  <td>8.85% HDFC BANK LTD 2026</td>
  <td>12 May 2026(M)</td>
  <td>Semi-Annual</td>
  <td>8.85%</td>
  <td>15 Lac</td>
  <td class="senior-secured">Tier 2 Bond</td>
  <td>10,00,000</td>
  <td>AAA by CRISIL</td>
</tr>
"""

# Private Equity data
private_equity_data = """
<tr>
  <td>SBI AMC</td>
  <td>Financials</td>
  <td>0.20Cr</td>
</tr>
<tr>
  <td>Paytm</td>
  <td>Fintech</td>
  <td>0.15Cr</td>
</tr>
<tr>
  <td>Zomato</td>
  <td>Food Delivery</td>
  <td>0.15Cr</td>
</tr>
"""

# Direct Equity data
direct_equity_data = """
<tr>
  <td>Bajaj Finance ltd.</td>
  <td>Financials</td>
  <td>0.10Cr</td>
</tr>
<tr>
  <td>HDFC Bank</td>
  <td>Banking</td>
  <td>0.10Cr</td>
</tr>
<tr>
  <td>Reliance Industries</td>
  <td>Conglomerate</td>
  <td>0.10Cr</td>
</tr>
<tr>
  <td>Infosys</td>
  <td>IT</td>
  <td>0.10Cr</td>
</tr>
<tr>
  <td>TCS</td>
  <td>IT</td>
  <td>0.10Cr</td>
</tr>
"""

# Dictionary mapping HTML files to their content
content_mapping = {
    "3_market_outlook.html": market_outlook_content,
    "4_debt_overview.html": debt_overview_content,
    "5_asset_allocation.html": asset_allocation_content,
    "6_mutual_fund.html": mutual_fund_content,
    "7_pms.html": pms_content,
    "8_fixed_income.html": fixed_income_content,
    "9_private_equity.html": private_equity_content,
    "10_direct_equity.html": direct_equity_content
}
