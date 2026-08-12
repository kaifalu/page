#!/usr/bin/env python3
"""Regenerate the static HTML pages for Kai-Fa Lu's GitHub Pages website.

Run from anywhere after installing Jinja2:
    python -m pip install -r requirements.txt
    python tools/build_pages.py

The website remains fully static after generation; GitHub Pages does not need Python.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import html

from jinja2 import Environment, BaseLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://kaifalu.github.io/kaifalu_page/"

SOCIALS = {
    "email": "mailto:kflu.917@gmail.com",
    "scholar": "https://scholar.google.com/citations?hl=en&user=a8eAKS8AAAAJ",
    "researchgate": "https://www.researchgate.net/profile/Lu-Kaifa",
    "github": "https://github.com/kaifalu",
    "linkedin": "https://www.linkedin.com/in/kaifa-lu-828676225/",
    "cecreh": "https://www.depts.ttu.edu/cecreh/",
    "iadapt": "https://dcp.ufl.edu/iadapt/",
}

PUBLICATIONS: list[dict[str, str]] = [
    {"id":"J1","year":"2026","authors":"Peng, Z., Lu, K., Liu, Y., Hou, Q., Zhang, Q.","title":"Symbiotic Planning Theory: The CORE Framework for Human-AI Cocreation in Urban Planning","venue":"Journal of the American Planning Association","details":"1–16","doi":"https://doi.org/10.1080/01944363.2026.2640038","topic":"planning-ai","status":"published"},
    {"id":"J2","year":"2026","authors":"Lu, K., Liu, Y., Peng, Z., Zhai, W.","title":"Characterizing Performance Resilience of Transportation Networks against Hurricane Events","venue":"Applied Geography","details":"186, 103820","doi":"https://doi.org/10.1016/j.apgeog.2025.103820","topic":"resilience","status":"published"},
    {"id":"J3","year":"2026","authors":"Popoola, T., Andrews, J., Lu, K., Hayhoe, K., Nejat, A.","title":"Modeling NFIP-Insured Housing Losses from Texas and Florida Flood Disasters: A Comparative Analysis of Hurricane Harvey, Tax Day Flood, and Hurricane Irma","venue":"Urban Climate","details":"68, 103029","doi":"https://doi.org/10.1016/j.uclim.2026.103029","topic":"resilience","status":"published"},
    {"id":"J4","year":"2026","authors":"Yang, X., Lu, K.*, Li, X.","title":"Assessing Vulnerability of Rural Buildings to Tornadoes and Their Relationships with Building Attributes and Surrounding Land Uses","venue":"International Journal of Disaster Risk Reduction","details":"137, 106097","doi":"https://doi.org/10.1016/j.ijdrr.2026.106097","topic":"resilience","status":"published"},
    {"id":"J5","year":"2026","authors":"Hou, Q., Hafiz, D., Peng, Z., Lu, K.","title":"From Perception to Adoption: A State-of-the-Art Review of Theoretical Approaches to Fully Autonomous Vehicle Acceptance and Transportation System Impacts","venue":"Transport Policy","details":"In Press","doi":"","topic":"mobility","status":"in-press"},
    {"id":"J6","year":"2025","authors":"Yang, X. & Lu, K.*","title":"Analysis of Rural Housing Vulnerability to Windstorms Using Machine Learning Techniques: A Case Study of “6.23” Tornado in Yancheng, China (in Chinese)","venue":"Architectural Journal","details":"32, 2–8","doi":"","topic":"resilience","status":"published"},
    {"id":"J7","year":"2025","authors":"Lu, K., Liu, Y., Peng, Z.","title":"Assessing the Impacts of Transit Systems and Urban Street Features on Bike-Sharing Ridership: A Graph-based Spatiotemporal Analysis and Prediction Model","venue":"Journal of Transport Geography","details":"128, 104356","doi":"https://doi.org/10.1016/j.jtrangeo.2025.104356","topic":"mobility","status":"published"},
    {"id":"J8","year":"2025","authors":"Lu, K., Liu, Y., Peng, Z.","title":"Unraveling Urban Bike-sharing Dynamics: Spatiotemporal Imbalances in Bike Rentals and Returns in Washington D.C.","venue":"Cities","details":"162, 105967","doi":"https://doi.org/10.1016/j.cities.2025.105967","topic":"mobility","status":"published"},
    {"id":"J9","year":"2024","authors":"Peng, Z., Lu, K., Liu, Y., & Zhai, W.","title":"The Pathway of Urban Planning AI: From Planning Support to Plan-Making","venue":"Journal of Planning Education and Research","details":"44(4), 2263–2279","doi":"https://doi.org/10.1177/0739456X231180568","topic":"planning-ai","status":"published"},
    {"id":"J10","year":"2024","authors":"Liu, Y., Peng, Z., Hou, Q., & Lu, K.","title":"The Role, Opportunities, and Challenges of Generative AI in Comprehensive Planning of American Small Towns – Using ChatGPT as an Example (in Chinese)","venue":"Journal of Urban Regional Planning","details":"16(1), 215–228","doi":"","topic":"planning-ai","status":"published"},
    {"id":"J11","year":"2024","authors":"Liu, Y., Lu, K., Peng, Z., & Zhai, W.","title":"Autonomous Shuttle Acceptance in an American Suburban Context: A Revealed Preference Study in Lake Nona, Florida","venue":"Travel Behaviour and Society","details":"37, 100865","doi":"https://doi.org/10.1016/j.tbs.2024.100865","topic":"mobility","status":"published"},
    {"id":"J12","year":"2024","authors":"Miao, C., Peng, Z., Cui, A., He, X., Chen, F., Lu, K., et al.","title":"Quantifying and Predicting Air Quality on Different Road Types in Urban Environments Using Mobile Monitoring and Automated Machine Learning","venue":"Atmospheric Pollution Research","details":"15(3), 102015","doi":"https://doi.org/10.1016/j.apr.2023.102015","topic":"environment","status":"published"},
    {"id":"J13","year":"2024","authors":"Jin, M., Gallagher, J., Li, X., Lu, K., Peng, Z., & He, H.","title":"Characterizing the Distribution Pattern of Traffic-related Air Pollutants in Near-road Neighborhoods","venue":"Environmental Monitoring and Assessment","details":"196(8), 767","doi":"https://doi.org/10.1007/s10661-024-12917-3","topic":"environment","status":"published"},
    {"id":"J14","year":"2023","authors":"Lu, D., He, H., Zhao, H., Lu, K., Peng, Z., & Li, J.","title":"Quantifying Traffic-related Carbon Emissions on Elevated Roads through On-road Measurements","venue":"Environmental Research","details":"231, 116200","doi":"https://doi.org/10.1016/j.envres.2023.116200","topic":"environment","status":"published"},
    {"id":"J15","year":"2023","authors":"Wang, H., Hu, Q., Huang, C., Lu, K., He, H., & Peng, Z.","title":"Quantification of Gaseous and Particulate Emission Factors from a Cargo Ship on the Huangpu River","venue":"Journal of Marine Science and Engineering","details":"11(8), 1580","doi":"https://doi.org/10.3390/jmse11081580","topic":"environment","status":"published"},
    {"id":"J16","year":"2023","authors":"Lu, K., Peng, Z.","title":"Impacts of Viaduct and Geometry Configurations on the Distribution of Traffic-related Particulate Matter in Urban Street Canyon","venue":"Science of the Total Environment","details":"858, 159902","doi":"https://doi.org/10.1016/j.scitotenv.2022.159902","topic":"environment","status":"published"},
    {"id":"J17","year":"2022","authors":"Zhu, X., Lu, K., Peng, Z., et al.","title":"Spatiotemporal Variations of Carbon Dioxide (CO2) at Urban Neighborhood Scale: Characterization of Distribution Patterns and Contributions of Emission Sources","venue":"Sustainable Cities and Society","details":"78, 103646","doi":"https://doi.org/10.1016/j.scs.2021.103646","topic":"environment","status":"published"},
    {"id":"J18","year":"2022","authors":"Lu, K., Wang, H., Li, X., et al.","title":"Assessing the Effects of Non-local Traffic Restriction Policy on Urban Air Quality","venue":"Transport Policy","details":"115, 62–74","doi":"https://doi.org/10.1016/j.tranpol.2021.11.005","topic":"policy","status":"published"},
    {"id":"J19","year":"2021","authors":"Jia, Y., Lu, K., Zheng, T., et al.","title":"Effects of Roadside Green Infrastructure on Particle Exposure: A Focus on Cyclists and Pedestrians on Pathways Between Urban Roads and Vegetative Barriers","venue":"Atmospheric Pollution Research","details":"12, 1–12","doi":"https://doi.org/10.1016/j.apr.2021.01.017","topic":"environment","status":"published"},
    {"id":"J20","year":"2020","authors":"Lu, K., He, H., Wang, H., et al.","title":"Characterizing Temporal and Vertical Distribution Patterns of Traffic-emitted Pollutants Near an Elevated Expressway in Urban Residential Areas","venue":"Building and Environment","details":"172, 106678","doi":"https://doi.org/10.1016/j.buildenv.2020.106678","topic":"environment","status":"published"},
    {"id":"J21","year":"2023","authors":"Yang, X., Li, X., Lu, K., & Peng, Z.","title":"Integrating Rural Livelihood Resilience and Sustainability for Post-disaster Community Relocation: A Theoretical Framework and Empirical Study","venue":"Natural Hazards","details":"116(2), 1775–1803","doi":"https://doi.org/10.1007/s11069-022-05739-4","topic":"resilience","status":"published"},
    {"id":"J22","year":"2022","authors":"Zhao, H., He, H., Lu, K., et al.","title":"Measuring the Impact of an Exogenous Factor: An Exponential Smoothing Model of the Response of Shipping to COVID-19","venue":"Transport Policy","details":"118, 91–100","doi":"https://doi.org/10.1016/j.tranpol.2022.01.015","topic":"policy","status":"published"},
    {"id":"J23","year":"2022","authors":"Zhu, X., He, H., Lu, K., et al.","title":"Characterizing Carbon Emissions from China V and China VI Gasoline Vehicles Based on Portable Emission Measurement Systems","venue":"Journal of Cleaner Production","details":"378(10), 134458","doi":"https://doi.org/10.1016/j.jclepro.2022.134458","topic":"environment","status":"published"},
    {"id":"J24","year":"2022","authors":"Zhao, H., He, H., Lu, K., et al.","title":"Characterizing the Distribution Pattern of Submicron and Coarse Particles on High-density Container Truck Roads through Mobile Monitoring","venue":"Atmospheric Pollution Research","details":"13(10), 101561","doi":"https://doi.org/10.1016/j.apr.2022.101561","topic":"environment","status":"published"},
    {"id":"J25","year":"2022","authors":"Wang, D., Wang, H., Lu, K., et al.","title":"Regional Prediction of Ozone and Fine Particulate Matter Using Diffusion Convolutional Recurrent Neural Network","venue":"International Journal of Environmental Research and Public Health","details":"19(7), 3988","doi":"https://doi.org/10.3390/ijerph19073988","topic":"machine-learning","status":"published"},
    {"id":"J26","year":"2021","authors":"Cai, W., Wang, H., Wu, C., Lu, K., et al.","title":"Characterizing the Interruption-Recovery Patterns of Urban Air Pollution under the COVID-19 Lockdown in China","venue":"Building and Environment","details":"205, 108231","doi":"https://doi.org/10.1016/j.buildenv.2021.108231","topic":"environment","status":"published"},
    {"id":"J27","year":"2020","authors":"Wang, D., Wang, H., Li, C., Lu, K., et al.","title":"Roadside Air Quality Forecasting in Shanghai with a Novel Sequence-to-Sequence Model","venue":"International Journal of Environmental Research and Public Health","details":"17(24), 9471","doi":"https://doi.org/10.3390/ijerph17249471","topic":"machine-learning","status":"published"},
]

UNDER_REVIEW: list[dict[str, str]] = [
    {"id":"J28","year":"2026","authors":"Lu, K., Hou, Q., Zhang, Q., Liu, Y., Peng, Z.","title":"Planning Automation of Shared Micromobility System Design: A Multi-Agent Deep Reinforcement Learning Approach","venue":"Nature Computational Science","details":"Under Review","topic":"planning-ai","status":"review"},
    {"id":"J29","year":"2026","authors":"Liu, Y., Lu, K., Zhang, Q., et al.","title":"Are Current Streets Suitable for Autonomous Bus Transit? User Perception and Street View Imagery Analysis across 12 U.S. Sites","venue":"Sustainable Cities and Society","details":"Under Review","topic":"mobility","status":"review"},
    {"id":"J30","year":"2026","authors":"Lu, K., Hou, Q., Liu, Y., Peng, Z.","title":"Spatial Dynamics of Campus-Centric Micromobility: Shared Dockless Scooter Usage in University vs. Non-University Towns","venue":"Transportation Research Part D: Transport and Environment","details":"Under Review","topic":"mobility","status":"review"},
    {"id":"J31","year":"2026","authors":"Lu, K., Hou, Q., Liu, Y., Peng, Z.","title":"Leveraging Shared Micromobility to Boost Transit Accessibility and Ridership: Evidence from Florida Cities on Multimodal Integration","venue":"Travel Behavior and Society","details":"Under Review","topic":"mobility","status":"review"},
    {"id":"J32","year":"2026","authors":"Lu, K., Hou, Q., Peng, Z.","title":"Impact of Shared Micromobility System Sizes on Usage Patterns and Their Planning Implications: A Meta-Analysis of 52 U.S. Cities","venue":"Journal of Planning Education and Research","details":"Under Review","topic":"mobility","status":"review"},
    {"id":"J33","year":"2026","authors":"Liu, Y., Lu, K., Hou, Q., et al.","title":"Can Discounted Uber Rides Connecting to Transit Help Regain Bus Ridership? Evidence from Pinellas County, Florida","venue":"Transport Policy","details":"Under the Second Round of Review","topic":"mobility","status":"review"},
    {"id":"J34","year":"2026","authors":"Zhang, Q., Peng, Z., Hou, Q., Lu, K., Wang, D., Liu, Y.","title":"Human-AI Collaboration in Transit Network Design: A Data-Driven Planning Case from Tampa","venue":"Journal of Planning Education and Research","details":"Under Review","topic":"planning-ai","status":"review"},
    {"id":"J35","year":"2026","authors":"Lu, K., Hou, Q., Andrews, J., Nejat, A.","title":"State and Local Governmental Capacity in Disaster Recovery: Evidence from CDBG-DR","venue":"Nature Climate Change","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J36","year":"2026","authors":"Lu, K., Hou, Q., Andrews, J., Nejat, A.","title":"Measuring Governmental Capacity in Disaster Recovery: Evidence from Texas CDBG-DR","venue":"International Journal of Disaster Risk Reduction","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J37","year":"2026","authors":"Lu, K., Hou, Q., Popoola, T., Hayhoe, K., Andrews, J., Nejat, A.","title":"Projecting Future Climate-Housing Exposure through Integrated Climate, Urban Growth, and Social Vulnerability Assessment: A Harris County, Texas Case Study","venue":"Urban Climate","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J38","year":"2026","authors":"Lu, K., Hou, Q., Peng, Z.","title":"Spatiotemporal Multi-Graph Diffusion Learning for Predicting Transportation Network Performance and Climate Resilience","venue":"The 34th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, Riverside, CA, USA","details":"Under Review","topic":"machine-learning","status":"review"},
    {"id":"J39","year":"2026","authors":"Lu, K., Hou, Q., Popoola, T., Hayhoe, K., Andrews, J., Nejat, A.","title":"Wildfire Risk Assessment in the United States: A State-of-the-Art Review of Synthesizing Contexts, Modeling Approaches, and Risk Indicators","venue":"Risk Analysis","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J40","year":"2026","authors":"Andrews, J., Lu, K., Popoola, T., Hayhoe, K., Nejat, A.","title":"Mapped Flood Zone Exposure and Flood Burden Recorded in Assistance Data: The Hydrologic Blind Spot of United States Flood Insurance","venue":"Nature Communications","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J41","year":"2026","authors":"Andrews, J., Lu, K., Popoola, T., Hayhoe, K., Nejat, A.","title":"Climate Extremes and Insurance Exposure: Projecting Future National Flood Insurance Program (NFIP) Claim Counts in Harris County, Texas","venue":"Natural Hazards","details":"Under Review","topic":"resilience","status":"review"},
    {"id":"J42","year":"2026","authors":"Andrews, J., Nejat, A., Lu, K.","title":"Narrative Signals as Leading Indicators of Disaster Recovery Program Execution Context-Dependent Evidence from Texas CDBG-DR Grant Portfolios, 2009–2025","venue":"International Journal of Disaster Risk Reduction","details":"Under Review","topic":"resilience","status":"review"},
]

BOOKS = [
    {"id":"B1","year":"2022","authors":"Peng, Z., Lu, K., Jin, M., et al.","title":"China’s Metro Explosion: Lessons from China’s Big Four Cities","venue":"In J. D. Landis (Ed.), Megaprojects for Megacities. Edward Elgar Publishing","url":"http://dx.doi.org/10.4337/9781803920634"},
    {"id":"B2","year":"2022","authors":"Peng, Z., Zhai, W., Lu, K.","title":"Smart, Sustainable, and Resilient Transportation System","venue":"In New Thinking in GIScience. Springer","url":"https://doi.org/10.1007/978-981-19-3816-0_34"},
]

REPORTS = [
    {"id":"R1","year":"2024","authors":"Peng, Z., Lu, K., Liu, Y.","title":"Micromobility Analytics in Florida: Usage Patterns, Public Transit Synergies, and Crash Insights","venue":"Florida Department of Transportation","url":"https://rosap.ntl.bts.gov/view/dot/86120"},
    {"id":"R2","year":"2023","authors":"Peng, Z., Liu, Y., Hou, Q., Lu, K.","title":"A Synthesis of Economic Impact Assessment of Transit Services","venue":"Florida Department of Transportation","url":"https://rosap.ntl.bts.gov/view/dot/84601"},
    {"id":"R3","year":"2023","authors":"Peng, Z., Lu, K., Liu, Y.","title":"Examining Data Needs and Implementation Process of AV-Based Microtransit Service: A Case Study in Lake Nona","venue":"Florida Department of Transportation","url":"https://rosap.ntl.bts.gov/view/dot/74775"},
]

RESEARCH_THEMES = [
    {"number":"01","code":"RES","title":"Urban Resilience","text":"Transportation-network performance, climate hazards, disaster recovery, housing vulnerability, and equitable resilience.","tags":["Hurricanes","Housing","Recovery"]},
    {"number":"02","code":"AI","title":"Urban Planning AI","text":"Human–AI cocreation, data-driven plan-making, planning automation, and AI-enabled decision support.","tags":["Cocreation","Automation","Decision Support"]},
    {"number":"03","code":"TRN","title":"Traffic Modeling & Planning","text":"Multimodal mobility, traffic and transit systems, system evaluation, transportation policy, and planning models.","tags":["Transit","Micromobility","Policy"]},
    {"number":"04","code":"ENV","title":"Environmental Planning & Engineering","text":"Near-road air quality, emissions, environmental monitoring, infrastructure effects, and adaptation planning.","tags":["Air Quality","Monitoring","Adaptation"]},
    {"number":"05","code":"GEO","title":"GeoAI & Big Data","text":"GIS dashboards, spatial analytics, spatiotemporal graphs, Street View imagery, and geospatial decision systems.","tags":["GIS","Spatial Data","Dashboards"]},
    {"number":"06","code":"ML","title":"Machine Learning","text":"Graph neural networks, deep reinforcement learning, NLP, LLMs, SEM, forecasting, and predictive analytics.","tags":["GNN","DRL","NLP & LLMs"]},
]

DASHBOARDS = [
    {
        "id":"cdbg-dashboard",
        "title":"CDBG-DR Fund Dashboard",
        "subtitle":"National disaster-recovery finance and implementation intelligence",
        "url":"https://kaifalu.github.io/HUD-CDBG-DR-Fund-Dashboard-Hierarchical/",
        "image":"assets/img/dashboard-cdbg-fund-overview.webp",
        "image_alt":"Illustrative interface preview of the CDBG-DR Fund Dashboard",
        "scope":"United States · 2001–2023",
        "summary":"An interactive platform for exploring HUD Community Development Block Grant–Disaster Recovery programs, connecting project- and activity-level finance, Quarterly Performance Report narratives, and geography.",
        "metrics":["18 disaster and appropriation categories","40 states and U.S. territories","7 hierarchical filters","Side-by-side program comparison"],
        "features":["Quarterly and cumulative funding trends","Obligated, expended, and disbursed funds","State, county, city/place, and urban-area analysis","Downloadable aggregates and figures"],
        "audience":"Researchers, agencies, grantees, planners, policymakers, nonprofits, students, and community stakeholders",
        "accent":"teal"
    },
    {
        "id":"climate-housing-dashboard",
        "title":"Climate-Housing Exposure Index Dashboard",
        "subtitle":"Place-based climate, growth, vulnerability, and housing decision support",
        "url":"https://kaifalu.github.io/Climate-Housing-Exposure-Index-Dashboard/",
        "image":"assets/img/dashboard-climate-housing-overview.webp",
        "image_alt":"Interface preview of the Climate-Housing Exposure Index Dashboard",
        "scope":"Harris County, Texas · 2020–2050",
        "summary":"An interactive platform showing how future precipitation extremes intersect with housing, population, employment, social vulnerability, and land-use change to support place-based climate-risk assessment.",
        "metrics":["1.5°C, 2.0°C, 2.5°C, and 3.0°C scenarios","2020–2050 growth comparisons","Climate-Housing Exposure Index","Compound hotspot identification"],
        "features":["Extreme-precipitation and CHEI mapping","Population, household, employment, and housing growth","Social vulnerability and housing-stock layers","Adaptation and environmental-justice screening"],
        "audience":"Researchers, planners, local governments, housing agencies, emergency managers, policymakers, nonprofits, and communities",
        "accent":"gold"
    },
]

PROJECTS = [
    {"id":"cecreh","date":"2025.10–Present","role":"Postdoctoral Research Associate","title":"Resilient Housing, Disaster Recovery & Climate Decision Systems","image":"assets/img/dashboard-climate-housing-overview.webp","image_alt":"Climate-Housing Exposure Index Dashboard interface","funding":"HUD & NSF · $2M","featured":True,"description":"Current research at the Center of Excellence in Capacity-building for REsilient Housing (CECREH), Texas Tech University, translating disaster-recovery and climate-risk research into public-facing decision systems.","bullets":["Develop interactive GIS dashboards connecting disaster-recovery finance, implementation narratives, climate hazards, housing, growth, and social vulnerability.","Apply SEM, NLP, and LLMs to narrative and numeric program data to analyze governmental capacity and recovery performance.","Support equitable housing recovery, climate adaptation, and long-term community planning through transparent, accessible analytics."]},
    {"id":"dissertation","date":"2023.08–2025.08","role":"Principal Investigator","title":"AI-Driven Shared Micromobility Planning & Operation","image":"assets/img/planning-ai-framework.webp","image_alt":"AI-driven shared micromobility planning framework","funding":"Ph.D. Dissertation · University of Florida","featured":True,"description":"A research program integrating spatial analytics, predictive modeling, and planning automation.","bullets":["Apply spatial data analysis and Bayesian Additive Regression Tree models to reveal usage patterns and contributing factors.","Use graph neural networks to predict bike- and scooter-sharing ridership.","Develop multi-agent deep reinforcement learning to optimize system design for usage, equity, cost-effectiveness, and multimodal integration."]},
    {"id":"micromobility-framework","date":"2023.03–2024.10","role":"Research Assistant","title":"Assessment of Modeling Framework for Micromobility","image":"assets/img/shared-micromobility.webp","image_alt":"Shared micromobility devices","funding":"FDOT · $300k","description":"A statewide modeling framework integrating survey, spatial, and machine-learning methods.","bullets":["Analyze usage patterns, mode choices, crash patterns, and relationships with public transit in Florida.","Contributed to the technical report Micromobility Analytics in Florida."]},
    {"id":"transit-impact","date":"2023.06–2023.12","role":"Research Assistant","title":"Economic Impact Assessment of Transit Services","image":"assets/img/florida-mobility-inventory.webp","image_alt":"Map of mobility systems in Florida","funding":"FDOT · $150k","description":"A synthesis of benefit-cost and economic-impact methods used in public transit.","bullets":["Examine applications of Benefit-Cost Analysis and Economic Impact Analysis.","Identify geographic variation, themes, trends, and research gaps through literature review, bibliometric mapping, and case studies."]},
    {"id":"revenue","date":"2022.07–2022.10","role":"Research Assistant","title":"Florida Transportation Revenue Forecasting & Allocation","image":"assets/img/transport-revenue.webp","image_alt":"Transportation revenue modeling framework","funding":"FDOT · $200k","description":"Phase I research on future transportation revenues and allocation processes.","bullets":["Develop models to understand forces affecting future transportation revenues in Florida.","Delineate the allocation process and concerns of districts and metropolitan planning organizations."]},
    {"id":"av-microtransit","date":"2021.06–2023.01","role":"Research Assistant","title":"AV-Based Microtransit Implementation in Lake Nona","image":"assets/img/av-microtransit.webp","image_alt":"Autonomous shuttle in Lake Nona","funding":"FDOT · $350k","description":"A case-study framework for evaluating autonomous microtransit implementation.","bullets":["Examine policy support, infrastructure and technology, service management, financial sustainability, ridership, and community impact."]},
    {"id":"inventory","date":"2021.07–2022.03","role":"Research Assistant","title":"Florida Microtransit & Micromobility Inventory","image":"assets/img/florida-mobility-inventory.webp","image_alt":"Florida microtransit and micromobility inventory map","funding":"FDOT · $280k","description":"A statewide inventory of emerging mobility services.","bullets":["Map geofenced service areas and identify relationships with transit agencies across Florida."]},
    {"id":"resilience","date":"Doctoral Research","role":"Lead Researcher","title":"Transportation Network Resilience against Hurricanes","image":"assets/img/transportation-resilience.webp","image_alt":"Transportation network resilience analysis in Miami-Dade County","funding":"Miami-Dade County Case Study","description":"Characterization and forecasting of highway-network performance under hurricane disruption.","bullets":["Quantify changes in traffic volume and speed to characterize resilience phases.","Develop spatiotemporal graph-based models using geographic, land-use, and population-density relationships."]},
    {"id":"environment-policy","date":"2018.09–2021.03","role":"Research Assistant","title":"Transportation Policy, Infrastructure & Atmospheric Environment","image":"assets/img/transport-policy-air-quality.webp","image_alt":"Analysis of transportation policy effects on urban air quality","funding":"National Planning Office · $150k","description":"Research on transportation policies, infrastructure, and traffic-related pollutants.","bullets":["Investigate traffic-restriction policy, viaducts, and street-canyon effects on urban air quality.","Analyze spatiotemporal patterns of traffic-related pollutants."]},
    {"id":"monitoring","date":"2018.09–2021.03","role":"Research Assistant","title":"Three-Dimensional Atmospheric Monitoring","image":"assets/img/environmental-monitoring.webp","image_alt":"Unmanned aerial vehicle used for atmospheric monitoring","funding":"Ministry of Science & Technology · $750k","description":"Vertical observation technologies using unmanned aerial vehicles and heavy-load airships.","bullets":["Contributed to an intelligent pod system for three-dimensional atmospheric environmental monitoring (China Patent CN215932395U)."]},
    {"id":"rfid","date":"2016.06–2017.07","role":"Principal Investigator","title":"RFID-Based Automatic Toll System for Roadside Parking","image":"assets/img/rfid-parking.webp","image_alt":"RFID roadside parking payment system","funding":"Hunan Education Commission · $3k","description":"A prototype system designed to monitor illegal parking and improve charging efficiency and accuracy.","bullets":[]},
    {"id":"railway","date":"2017–2018","role":"Transportation Planner & Engineer Intern","title":"Railway Station Design & Operations Practice","image":"assets/img/railway-planning.webp","image_alt":"Railway station planning drawing","funding":"China Railway Guangzhou & Wuhan Groups","description":"Practice in passenger and freight transport, centralized traffic control, train scheduling, and freight-station planning.","bullets":[]},
]

TEACHING = [
    ("Spring 2025","GIS Automation for Geospatial Modeling and Analysis","Graduate level","Teaching Assistant","University of Florida"),
    ("Fall 2024","Transportation Policy and Planning","Graduate level · Online & Hybrid","Teaching Assistant","University of Florida"),
    ("Spring 2024","Transportation and Land Use Modeling","Graduate level","Teaching Assistant","University of Florida"),
    ("Fall 2023","Planning for Climate Change","Graduate level","Teaching Assistant","University of Florida"),
    ("Spring 2022","Transportation and Land Use Modeling","Graduate level","Co-Instructor","University of Florida"),
    ("Spring 2019","Operations Research","Undergraduate level","Teaching Assistant","Shanghai Jiao Tong University"),
]

MENTORING = [
    ("Texas Tech University","Hussein Orekoya","Ph.D. Dissertation","2025 & 2026"),
    ("Texas Tech University","Prashant Aryal","Ph.D. Dissertation","2025 & 2026"),
    ("Texas Tech University","Temidayo Popoola","Ph.D. Dissertation","2025 & 2026"),
    ("Texas Tech University","Amin Sobhani","Ph.D. Dissertation","2025 & 2026"),
    ("University of Florida","Khalid A. Aljuhani","Ph.D. Dissertation","2024 & 2025"),
    ("University of Florida","Qing Hou","Ph.D. Dissertation","2025"),
    ("University of Florida","Yue Dong","Master’s Thesis","2023"),
    ("Shanghai Jiao Tong University","Xinghang Zhu","Master’s Thesis","2020 & 2021"),
]

REVIEWERS = [
    ("Journal of the American Planning Association","2025 & 2026"),
    ("Journal of Planning Education and Research","2025 & 2026"),
    ("Travel Behaviour and Society","2025 & 2026"),
    ("Journal of Environmental Management","2023"),
    ("Humanities and Social Sciences Communications","2024"),
    ("Scientific Reports","2024 & 2025"),
    ("Transportation Research Part D: Transport and Environment","2025"),
    ("Stochastic Environmental Research and Risk Assessment","2024"),
]

AFFILIATIONS = [
    "Center of Excellence in Capacity-building for REsilient Housing (CECREH), Postdoctoral",
    "International Association for China Planning (IACP), Student Member",
    "International Center for Adaptation Planning and Design (iAdapt), Member",
    "University of Florida Transportation Institute (UFTI), Student Member",
    "Committee on Extreme Weather and Climate Change Adaptation (AMR50), Friend Member",
]

CERTIFICATES = [
    ("2024","Machine Learning Certificate","Electrical and Computer Engineering, University of Florida"),
    ("2024","Urban Analytics (URP) Certificate","Urban and Regional Planning, University of Florida"),
    ("2024","Generative AI with Diffusion Models","NVIDIA"),
    ("2023","Data Parallelism: How to Train Deep Learning Models on Multiple GPUs","NVIDIA"),
    ("2022 & 2023","Certificate of Outstanding Merit","University of Florida International Center"),
]

AWARDS = [
    ("2025","Best Presentation/Research Award","AI and Cities: An International Forum for Innovation and Collaboration, University of Florida"),
    ("2025","WRS Infrastructure & Environment Inc. Award in Memoriam of Mario Ripol","Outstanding Achievement in Planning Information and Analysis, University of Florida"),
    ("2023","Merit Commendation","Ph.D. Research Poster, Graduate Student Research Symposium, University of Florida"),
    ("2021","COSCO Maritime Scholarship","Top 5%, China Ocean Shipping Company"),
    ("2021","Outstanding Graduates of Shanghai","Top 3%"),
    ("2019","Second Prize","National Graduate Mathematical Contest in Modeling"),
    ("2018","Outstanding Undergraduates of Hunan Province","Top 3%"),
    ("2017","Meritorious Winner","American Undergraduate Mathematical Contest in Modeling"),
    ("2017","National Scholarship","Top 3%, Ministry of Education of China"),
    ("2016","First Prize","National Undergraduate Mathematical Contest in Modeling"),
    ("2015","Third Prize","National Undergraduate Mathematical Contest"),
    ("2015 & 2016","National Encouragement Scholarship","Top 5%, Ministry of Education of China"),
    ("2015–2021","First-Class Scholarship","Top 10%, Shanghai Jiao Tong University & Central South University"),
]

PRESENTATIONS = [
    ("2026.06","51st Annual Natural Hazards Workshop Research Meeting","State and Local Governmental Capacity in Disaster Recovery: Evidence from CDBG-DR","Broomfield, Colorado, USA"),
    ("2026.06","51st Annual Natural Hazards Workshop Poster Session","Measuring Governmental Capacity in Disaster Recovery: Evidence from Texas CDBG-DR","Broomfield, Colorado, USA"),
    ("2025.10","Association of Collegiate Schools of Planning (ACSP) Conference","AI-Driven Approach to Optimize and Automate Shared Micromobility System Design and Planning","Minneapolis, Minnesota, USA"),
    ("2025.01","Transportation Research Board 104th Annual Meeting","Characterizing Performance Resilience of Transportation Networks against Extreme Weather Events","Washington, D.C., USA"),
    ("2025.01","Transportation Research Board 104th Annual Meeting","Integrating Public Transit Effects and Street View Imagery into a Dynamic Spatiotemporal Graph-based Machine Learning Model for Predicting Bike-sharing Ridership","Washington, D.C., USA"),
    ("2024.11","Association of Collegiate Schools of Planning (ACSP) Conference","Impact of Shared Micromobility System Sizes on Usage Patterns: Planning Implications","Seattle, Washington, USA"),
    ("2024.07","18th International Association for China Planning (IACP) Conference","Impact of Shared Micromobility System Sizes on Usage Patterns and Their Planning Implications","Hangzhou, China"),
    ("2024.01","Transportation Research Board 103rd Annual Meeting","Demystifying the Spatiotemporal Heterogeneity of Rental-Return Imbalance on Bike-Sharing Systems: A Bayesian Additive Regression Trees (BART) Model","Washington, D.C., USA"),
    ("2023.10","Association of Collegiate Schools of Planning (ACSP) Conference","Leveraging Deep Learning with Geospatial Data Analytics for Quantification and Prediction of Performance Resilience of Transportation Networks against Extreme Weather Events","Chicago, Illinois, USA"),
    ("2023.07","17th International Association for China Planning (IACP) Conference","Using Origin-Destination Flow Graph and Public Transit Information to Enhance Short-Term Ridership Prediction in Bike-Sharing Systems","Tianjin, China"),
    ("2023.01","Transportation Research Board 102nd Annual Meeting","Characterization and Prediction of Transportation Network Resilience: A Spatiotemporal Graph Diffusion Convolutional Recurrent Neural Network Approach","Washington, D.C., USA"),
    ("2023.01","Transportation Research Board 102nd Annual Meeting","Characterizing Carbon Emissions from China V and China VI Gasoline Vehicles Based on Portable Emission Measurement Systems","Washington, D.C., USA"),
    ("2023.01","Transportation Research Board 102nd Annual Meeting","Characterizing the Traffic-related Carbon Emission Factors on Elevated Roads Based on On-road Measurements","Washington, D.C., USA"),
    ("2021.01","Transportation Research Board 100th Annual Meeting","Investigating Pedestrians’ Exposure to Traffic-Related PM and BC at Intersections: A Case Study in Shanghai, China","Washington, D.C., USA"),
    ("2020.01","Transportation Research Board 99th Annual Meeting","Characterization of Traffic-related Pollutant Distribution Patterns in Urban Residential Areas with an Elevated Expressway","Washington, D.C., USA"),
]

INVITED_TALKS = [
    ("2024.06","Guest Lecture at Chang’an University","Integrating Public Transit Effects and Street View Imagery into a Dynamic Spatiotemporal Graph-Based Machine Learning Model for Analyzing and Predicting Bike-Sharing Ridership","Xi’an, China"),
]

EDUCATION = [
    {"date":"2021–2025","degree":"Ph.D.","field":"Urban and Regional Planning","school":"University of Florida","gpa":"GPA 3.90/4.00","detail":"Dissertation: AI-Driven Approach to Optimize and Automate Shared Micromobility System Planning and Operation"},
    {"date":"2021–2024","degree":"M.S.","field":"Electrical and Computer Engineering","school":"University of Florida","gpa":"GPA 3.89/4.00","detail":"Machine learning, neural networks and deep learning, data analytics, time series, pattern recognition, and computer communications"},
    {"date":"2018–2021","degree":"M.S.","field":"Transportation Engineering","school":"Shanghai Jiao Tong University","gpa":"GPA 3.83/4.00","detail":"Thesis: Characterizing Traffic-related Pollutant Distribution Patterns Under the Impacts of Urban Viaduct and Street Canyon"},
    {"date":"2014–2018","degree":"B.S.","field":"Transportation Engineering","school":"Central South University","gpa":"GPA 92.40/100.00","detail":"Thesis: Optimization of Vehicle Routing Problem over Local Road Network within Changsha South Railway Station"},
]


def highlight_name(value: str) -> Markup:
    escaped = html.escape(value)
    escaped = escaped.replace("Lu, K.*", '<strong class="self-author">Lu, K.*</strong>')
    escaped = escaped.replace("Lu, K.", '<strong class="self-author">Lu, K.</strong>')
    return Markup(escaped)


def topic_label(topic: str) -> str:
    return {
        "planning-ai":"Planning AI",
        "resilience":"Resilience",
        "mobility":"Mobility",
        "environment":"Environment",
        "policy":"Policy",
        "machine-learning":"Machine Learning",
    }.get(topic, topic.replace("-", " ").title())


def status_label(status: str) -> str:
    return {"published":"Published", "in-press":"In Press", "review":"Under Review"}.get(status, status.title())


env = Environment(loader=BaseLoader(), autoescape=select_autoescape(["html", "xml"]), trim_blocks=True, lstrip_blocks=True)
env.filters["highlight_name"] = highlight_name
env.filters["topic_label"] = topic_label
env.filters["status_label"] = status_label

BASE_TEMPLATE = r'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{{ description }}">
  <meta name="author" content="Kai-Fa Lu">
  <meta name="theme-color" content="#082a3d">
  <meta property="og:title" content="{{ title }}">
  <meta property="og:description" content="{{ description }}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ canonical }}">
  <meta property="og:image" content="{{ base_url }}assets/img/social-card.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{{ canonical }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap" rel="stylesheet">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <script>document.documentElement.classList.add('js')</script>
  <title>{{ title }}</title>
  <link rel="stylesheet" href="assets/css/styles.css">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Kai-Fa Lu",
    "alternateName": "Kaifa Lu",
    "url": "{{ base_url }}",
    "image": "{{ base_url }}assets/img/kai-fa-lu-profile.webp",
    "jobTitle": "Post-Doctoral Research Associate in Civil & Construction Engineering",
    "affiliation": [
      {"@type":"Organization","name":"Center of Excellence in Capacity-building for REsilient Housing (CECREH), Texas Tech University","url":"{{ socials.cecreh }}"},
      {"@type":"Organization","name":"International Center for Adaptation Planning and Design (iAdapt), University of Florida","url":"{{ socials.iadapt }}"}
    ],
    "email": "mailto:kflu.917@gmail.com",
    "sameAs": ["{{ socials.scholar }}","{{ socials.researchgate }}","{{ socials.github }}","{{ socials.linkedin }}"]
  }
  </script>
</head>
<body data-page="{{ page }}">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="page-progress" aria-hidden="true"><span></span></div>
  <header class="site-header" id="top">
    <div class="container nav-wrap">
      <a class="brand" href="index.html" aria-label="Kai-Fa Lu home">
        <span class="brand-mark">KFL</span>
        <span class="brand-copy"><strong>Kai-Fa Lu</strong><small>Urban Resilience · Planning AI · GeoAI</small></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open navigation"><span></span><span></span><span></span></button>
      <nav id="site-nav" class="site-nav" aria-label="Primary navigation">
        <a data-nav="home" href="index.html">Home</a>
        <a data-nav="research" href="research.html">Research</a>
        <a data-nav="publications" href="publications.html">Publications</a>
        <a data-nav="activities" href="activities.html">Activities</a>
        <a data-nav="contact" href="index.html#contact">Contact</a>
      </nav>
      <div class="nav-actions">
        <button class="theme-toggle" type="button" aria-label="Toggle color theme" title="Toggle color theme">
          <svg class="sun-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41"></path></svg>
          <svg class="moon-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        </button>
        <a class="nav-cv" href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener">CV <span aria-hidden="true">↗</span></a>
      </div>
    </div>
  </header>
  <main id="main">{{ content | safe }}</main>
  <footer class="site-footer">
    <div class="container footer-layout">
      <div><strong>Kai-Fa Lu, Ph.D.</strong><span>Post-Doctoral Research Associate · CECREH, Texas Tech University · Member, iAdapt, University of Florida</span></div>
      <p>© <span id="year"></span> Kai-Fa Lu. Designed for GitHub Pages.</p>
      <a href="#top">Back to top ↑</a>
    </div>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>'''

HOME_TEMPLATE = r'''
<section class="hero home-hero">
  <div class="hero-grid-pattern" aria-hidden="true"></div><div class="hero-glow hero-glow-a" aria-hidden="true"></div><div class="hero-glow hero-glow-b" aria-hidden="true"></div>
  <div class="container hero-layout">
    <div class="hero-copy reveal">
      <a class="role-line role-line-link" href="{{ socials.cecreh }}" target="_blank" rel="noopener"><span class="status-dot"></span> Post-Doctoral Research Associate · CECREH · Texas Tech University <span aria-hidden="true">↗</span></a>
      <p class="hero-overline">Urban resilience × planning AI × GeoAI</p>
      <h1>Turning urban data into <em>intelligent, resilient</em> decisions.</h1>
      <p class="hero-lead">I am <strong>Kai-Fa Lu, Ph.D.</strong>, a researcher in Civil &amp; Construction Engineering whose work integrates resilient housing, disaster recovery, climate decision systems, transportation planning, GeoAI, big data, and machine learning.</p>
      <div class="hero-actions"><a class="btn btn-primary" href="research.html">Explore research <span aria-hidden="true">↗</span></a><a class="btn btn-ghost" href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener">Download CV <span aria-hidden="true">↓</span></a></div>
      <div class="profile-links" aria-label="Professional profiles"><a href="{{ socials.email }}">Email <span>↗</span></a><a href="{{ socials.scholar }}" target="_blank" rel="noopener">Google Scholar <span>↗</span></a><a href="{{ socials.researchgate }}" target="_blank" rel="noopener">ResearchGate <span>↗</span></a><a href="{{ socials.github }}" target="_blank" rel="noopener">GitHub <span>↗</span></a><a href="{{ socials.linkedin }}" target="_blank" rel="noopener">LinkedIn <span>↗</span></a></div>
      <div class="hero-affiliations" aria-label="Current institutional affiliations">
        <a href="{{ socials.cecreh }}" target="_blank" rel="noopener"><span class="affiliation-monogram ttu">TTU</span><span><small>Current appointment</small><strong>CECREH · Texas Tech University</strong></span><i>↗</i></a>
        <a href="{{ socials.iadapt }}" target="_blank" rel="noopener"><span class="affiliation-monogram uf">UF</span><span><small>Research affiliation</small><strong>iAdapt · University of Florida</strong></span><i>↗</i></a>
      </div>
    </div>
    <div class="hero-visual reveal reveal-delay">
      <div class="portrait-orbit orbit-one" aria-hidden="true"></div><div class="portrait-orbit orbit-two" aria-hidden="true"></div>
      <div class="portrait-shell"><div class="portrait-accent" aria-hidden="true"></div><div class="portrait-frame"><img src="assets/img/kai-fa-lu-profile.webp" alt="Professional portrait of Kai-Fa Lu" width="1000" height="1250" fetchpriority="high"></div><div class="portrait-label"><span>Current appointment</span><strong>Post-Doctoral Research Associate</strong><small>CECREH · Civil &amp; Construction Engineering · Texas Tech University</small></div></div>
      <div class="focus-card focus-card-top"><span class="focus-icon">AI</span><div><small>Research lens</small><strong>Planning Intelligence</strong></div></div>
      <div class="focus-card focus-card-bottom"><span class="focus-icon">GEO</span><div><small>Research lens</small><strong>Climate &amp; Resilience</strong></div></div>
      <div class="focus-card focus-card-side"><span class="focus-icon">DS</span><div><small>Research product</small><strong>Decision Systems</strong></div></div>
    </div>
  </div>
  <div class="container stat-panel reveal"><div class="stat"><strong>27</strong><span>Journal publications</span></div><div class="stat"><strong>15</strong><span>Manuscripts under review</span></div><div class="stat"><strong>2</strong><span>Live resilience dashboards</span></div><div class="stat"><strong>4</strong><span>Degrees in planning &amp; engineering</span></div></div>
</section>

<section class="research-signal" aria-label="Research interests"><div class="container signal-track">{% for item in themes %}<span>{{ item.title }}</span>{% endfor %}</div></section>

<section id="about" class="section section-about">
  <div class="container about-layout">
    <div class="section-intro reveal"><span class="section-number">01</span><span class="section-kicker">Research profile</span><h2>Connecting engineering, planning, and AI for real-world urban challenges.</h2></div>
    <div class="about-content reveal"><p class="about-lead">My work spans resilient communities and intelligent mobility, with a consistent focus on translating complex evidence into accessible tools for planning, engineering, and policy.</p><p>At <a class="inline-affiliation" href="{{ socials.cecreh }}" target="_blank" rel="noopener">CECREH, Texas Tech University ↗</a>, I develop GIS-based decision systems for disaster-recovery programs, housing, and climate risk; apply structural equation modeling, natural language processing, and large language models to program performance; and assess risks facing underserved communities.</p><p>I remain affiliated with the <a class="inline-affiliation" href="{{ socials.iadapt }}" target="_blank" rel="noopener">International Center for Adaptation Planning and Design (iAdapt), University of Florida ↗</a>, where my doctoral and collaborative research has advanced urban planning AI, shared-mobility analytics, transportation systems, and adaptation planning.</p><div class="interest-cloud"><span>Python</span><span>MATLAB</span><span>R</span><span>ArcGIS</span><span>Graph Neural Networks</span><span>Deep Reinforcement Learning</span><span>NLP &amp; LLMs</span><span>Spatiotemporal Analytics</span><span>GIS Dashboards</span></div></div>
  </div>
</section>

<section class="affiliation-section">
  <div class="container affiliation-layout">
    <div class="affiliation-intro reveal"><span class="section-kicker">Institutional affiliations</span><h2>Research anchored in two interdisciplinary centers.</h2><p>Current work at Texas Tech University and continuing collaboration with the University of Florida connect resilient housing, climate adaptation, planning AI, and transportation research.</p></div>
    <div class="affiliation-cards">
      <a class="institution-card institution-card-ttu reveal" href="{{ socials.cecreh }}" target="_blank" rel="noopener"><div class="institution-top"><span class="institution-seal">TTU</span><span class="institution-status">Current appointment</span></div><h3>Texas Tech University</h3><strong>Center of Excellence in Capacity-building for REsilient Housing (CECREH)</strong><p>Post-Doctoral Research Associate in Civil &amp; Construction Engineering, advancing research and decision tools for housing recovery, climate risk, community vulnerability, and equitable resilience.</p><span class="institution-link">Visit CECREH ↗</span></a>
      <a class="institution-card institution-card-uf reveal" href="{{ socials.iadapt }}" target="_blank" rel="noopener"><div class="institution-top"><span class="institution-seal">UF</span><span class="institution-status">Research affiliation</span></div><h3>University of Florida</h3><strong>International Center for Adaptation Planning and Design (iAdapt)</strong><p>Member and research affiliate connecting urban planning AI, climate adaptation, transportation-system dynamics, shared mobility, and knowledge-to-action exchange.</p><span class="institution-link">Visit iAdapt ↗</span></a>
    </div>
  </div>
</section>

<section id="research" class="section section-tint">
  <div class="container">
    <div class="section-head reveal"><div><span class="section-number">02</span><span class="section-kicker">Research agenda</span></div><div><h2>Six complementary research themes.</h2><p>The latest CV frames the research program around resilience, planning AI, traffic modeling, environmental engineering, GeoAI and big data, and machine learning.</p></div></div>
    <div class="theme-grid">{% for item in themes %}<article class="theme-card reveal"><div class="theme-card-top"><span>{{ item.number }}</span><b>{{ item.code }}</b></div><h3>{{ item.title }}</h3><p>{{ item.text }}</p><div class="theme-tags">{% for tag in item.tags %}<span>{{ tag }}</span>{% endfor %}</div></article>{% endfor %}</div>
    <div class="projects-head reveal"><span class="section-kicker">Current research program</span><h3>Resilient Housing, Disaster Recovery &amp; Climate Decision Systems.</h3><p>Two live, public-facing dashboards translate research on disaster-recovery finance and future climate–housing exposure into exploratory decision support.</p></div>
    <article class="project-feature current-program reveal"><div class="project-image"><img src="{{ projects[0].image }}" alt="{{ projects[0].image_alt }}" loading="lazy"></div><div class="project-copy"><span class="project-label">Current research · {{ projects[0].date }}</span><h3>{{ projects[0].title }}</h3><p>{{ projects[0].description }}</p><ul class="project-points">{% for bullet in projects[0].bullets %}<li>{{ bullet }}</li>{% endfor %}</ul><div class="project-details"><span>{{ projects[0].role }}</span><span>{{ projects[0].funding }}</span></div><div class="project-action-row"><a class="project-link" href="research.html#cecreh">Full research portfolio ↗</a><a class="project-link" href="{{ socials.cecreh }}" target="_blank" rel="noopener">CECREH ↗</a></div></div></article>

    <div class="dashboard-showcase" aria-label="Interactive resilience dashboards">
      {% for dashboard in dashboards %}<article class="dashboard-card dashboard-card-{{ dashboard.accent }} reveal" id="home-{{ dashboard.id }}">
        <a class="dashboard-preview" href="{{ dashboard.url }}" target="_blank" rel="noopener"><img src="{{ dashboard.image }}" alt="{{ dashboard.image_alt }}" loading="lazy"><span class="live-badge"><i></i> Live interactive dashboard</span><span class="preview-launch">Open dashboard ↗</span></a>
        <div class="dashboard-body"><div class="dashboard-heading"><span>{{ dashboard.scope }}</span><h3>{{ dashboard.title }}</h3><p class="dashboard-subtitle">{{ dashboard.subtitle }}</p></div><p>{{ dashboard.summary }}</p><div class="dashboard-metrics">{% for metric in dashboard.metrics %}<span>{{ metric }}</span>{% endfor %}</div><div class="dashboard-actions"><a class="btn btn-primary" href="{{ dashboard.url }}" target="_blank" rel="noopener">Launch dashboard ↗</a><a class="text-link" href="research.html#{{ dashboard.id }}">Research context ↓</a></div></div>
      </article>{% endfor %}
    </div>

    <div class="projects-head projects-head-secondary reveal"><span class="section-kicker">Selected work</span><h3>Additional projects connecting methods to policy and practice.</h3></div>
    <div class="project-grid">{% for p in [projects[1],projects[2],projects[7],projects[8]] %}<article class="project-card reveal"><div class="project-image"><img src="{{ p.image }}" alt="{{ p.image_alt }}" loading="lazy"></div><div class="project-copy"><span class="project-label">{{ p.date }}</span><h3>{{ p.title }}</h3><p>{{ p.description }}</p><a class="project-link" href="research.html#{{ p.id }}">Details ↗</a></div></article>{% endfor %}</div>
  </div>
</section>

<section id="publications" class="section publications-section">
  <div class="publication-orb" aria-hidden="true"></div><div class="container">
    <div class="section-head section-head-light reveal"><div><span class="section-number">03</span><span class="section-kicker">Selected publications</span></div><div><h2>Recent research across planning AI, mobility, resilience, and climate risk.</h2><p>Selected 2025–2026 publications; the complete CV-derived record is available in the publication directory.</p></div></div>
    <div class="publication-list featured-publications">{% for pub in selected_publications %}<article class="publication reveal"><div class="pub-meta"><span>{{ pub.year }}</span><span>{{ pub.status | status_label }}</span></div><div class="pub-main"><h3>{{ pub.title }}</h3><p>{{ pub.authors | highlight_name }} · <em>{{ pub.venue }}</em>{% if pub.details %}, {{ pub.details }}{% endif %}</p></div>{% if pub.doi %}<a class="pub-link" href="{{ pub.doi }}" target="_blank" rel="noopener" aria-label="Open publication DOI">DOI ↗</a>{% else %}<span class="pub-status">{{ pub.status | status_label }}</span>{% endif %}</article>{% endfor %}</div>
    <div class="publication-footer reveal"><p>Browse all 27 journal publications, 15 manuscripts under review, book chapters, and technical reports.</p><div><a class="btn btn-light" href="publications.html">Full publication record ↗</a><a class="text-link-light" href="{{ socials.scholar }}" target="_blank" rel="noopener">Google Scholar ↗</a></div></div>
  </div>
</section>

<section id="experience" class="section">
  <div class="container"><div class="section-head reveal"><div><span class="section-number">04</span><span class="section-kicker">Experience &amp; education</span></div><div><h2>A multidisciplinary path across planning, engineering, and data science.</h2><p>Current research experience at Texas Tech University is built on doctoral and engineering training at the University of Florida, Shanghai Jiao Tong University, and Central South University.</p></div></div>
  <div class="journey-layout"><div class="journey-column"><div class="journey-label reveal">Research journey</div><div class="timeline"><article class="timeline-item reveal"><div class="timeline-marker"></div><span class="timeline-date">2025.10–Present</span><h3>Post-Doctoral Research Associate</h3><p class="timeline-org"><a href="{{ socials.cecreh }}" target="_blank" rel="noopener">CECREH · Texas Tech University ↗</a></p><p>Disaster-recovery and housing dashboards; SEM, NLP, and LLM analysis; climate-risk assessment and resilient policy tools.</p></article><article class="timeline-item reveal"><div class="timeline-marker"></div><span class="timeline-date">2023.08–2025.08</span><h3>Principal Investigator · Ph.D. Dissertation</h3><p class="timeline-org"><a href="{{ socials.iadapt }}" target="_blank" rel="noopener">University of Florida · iAdapt ↗</a></p><p>AI-driven planning automation and optimization for shared micromobility systems.</p></article><article class="timeline-item reveal"><div class="timeline-marker"></div><span class="timeline-date">2021–2024</span><h3>Research Assistant · Transportation Projects</h3><p class="timeline-org">University of Florida</p><p>FDOT-funded work on micromobility, microtransit, transit economic impacts, and revenue forecasting.</p></article><article class="timeline-item reveal"><div class="timeline-marker"></div><span class="timeline-date">2018–2021</span><h3>Research Assistant · Environmental Transportation</h3><p class="timeline-org">Shanghai Jiao Tong University</p><p>Transportation policies, infrastructure, atmospheric monitoring, traffic emissions, and urban air quality.</p></article></div></div>
  <div class="journey-column"><div class="journey-label reveal">Education</div><div class="education-stack">{% for item in education %}<article class="education-card reveal"><div><span>{{ item.date }}</span><strong>{{ item.degree }}</strong></div><h3>{{ item.field }}</h3><p>{{ item.school }} · {{ item.gpa }}</p><small>{{ item.detail }}</small></article>{% endfor %}</div></div></div></div>
</section>

<section id="highlights" class="section section-tint">
  <div class="container"><div class="section-head reveal"><div><span class="section-number">05</span><span class="section-kicker">Professional highlights</span></div><div><h2>Research, teaching, service, and recognition.</h2><p>A selected view of activities documented in the latest curriculum vitae.</p></div></div>
  <div class="recognition-grid"><article class="recognition-card recognition-card-wide reveal"><span class="recognition-label">Teaching</span><h3>Planning, modeling, climate, and geospatial analytics</h3><div class="mini-list">{% for item in teaching[:5] %}<div><strong>{{ item[0].replace('Spring ','').replace('Fall ','') }}</strong><span>{{ item[1] }} · {{ item[3] }}</span></div>{% endfor %}</div><a class="card-link" href="activities.html#teaching">All teaching activities ↗</a></article><article class="recognition-card reveal"><span class="recognition-label">Recognition</span><h3>Selected awards</h3><div class="award-list">{% for award in awards[:3] %}<div><span>{{ award[0] }}</span><p><strong>{{ award[1] }}</strong><br>{{ award[2] }}</p></div>{% endfor %}</div><a class="card-link" href="activities.html#awards">Full recognition record ↗</a></article><article class="recognition-card reveal"><span class="recognition-label">Academic service</span><h3>Mentoring &amp; peer review</h3><p>Mentoring at Texas Tech University, the University of Florida, and Shanghai Jiao Tong University; reviewer service across planning, transportation, environmental, and interdisciplinary journals.</p><a class="card-link" href="activities.html#service">View academic service ↗</a></article></div></div>
</section>

<section id="contact" class="contact-section"><div class="contact-pattern" aria-hidden="true"></div><div class="container contact-layout"><div class="reveal"><span class="contact-kicker">Contact &amp; collaboration</span><h2>Let’s connect around resilient cities and intelligent mobility.</h2><p>I welcome research conversations involving resilient housing, disaster recovery, climate decision systems, urban planning AI, transportation, GeoAI, and machine learning.</p></div><div class="contact-card reveal"><a href="{{ socials.email }}"><span>Email</span><strong>kflu.917@gmail.com</strong><i>↗</i></a><a href="tel:+13528714546"><span>Phone</span><strong>+1 (352) 871-4546</strong><i>↗</i></a><a href="{{ socials.cecreh }}" target="_blank" rel="noopener"><span>Current appointment</span><strong>CECREH · Texas Tech University</strong><i>↗</i></a><a href="{{ socials.iadapt }}" target="_blank" rel="noopener"><span>Research affiliation</span><strong>iAdapt · University of Florida</strong><i>↗</i></a><a href="{{ socials.scholar }}" target="_blank" rel="noopener"><span>Publications</span><strong>Google Scholar</strong><i>↗</i></a><a href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener"><span>Curriculum vitae</span><strong>Open latest CV</strong><i>↗</i></a></div></div></section>

'''
PAGE_HERO = r'''<section class="page-hero"><div class="page-hero-grid" aria-hidden="true"></div><div class="container page-hero-layout"><div class="reveal"><p class="page-eyebrow">{{ eyebrow }}</p><h1>{{ heading | safe }}</h1><p>{{ lead }}</p>{% if actions %}<div class="hero-actions">{{ actions | safe }}</div>{% endif %}</div><div class="page-hero-aside reveal reveal-delay">{{ aside | safe }}</div></div></section>'''

RESEARCH_TEMPLATE = r'''
{{ page_hero | safe }}
<section class="research-affiliation-bar"><div class="container"><a href="{{ socials.cecreh }}" target="_blank" rel="noopener"><span class="affiliation-monogram ttu">TTU</span><span><small>Current appointment</small><strong>CECREH · Texas Tech University</strong></span><i>↗</i></a><a href="{{ socials.iadapt }}" target="_blank" rel="noopener"><span class="affiliation-monogram uf">UF</span><span><small>Research affiliation</small><strong>iAdapt · University of Florida</strong></span><i>↗</i></a></div></section>
<section class="section"><div class="container"><div class="section-head reveal"><div><span class="section-number">01</span><span class="section-kicker">Research themes</span></div><div><h2>A connected portfolio of methods and applications.</h2><p>These six themes follow the research interests in the latest CV and provide a practical structure for the project portfolio.</p></div></div><div class="theme-grid theme-grid-page">{% for item in themes %}<article class="theme-card reveal"><div class="theme-card-top"><span>{{ item.number }}</span><b>{{ item.code }}</b></div><h3>{{ item.title }}</h3><p>{{ item.text }}</p><div class="theme-tags">{% for tag in item.tags %}<span>{{ tag }}</span>{% endfor %}</div></article>{% endfor %}</div></div></section>

<section id="cecreh" class="section section-tint current-research-section"><div class="container"><div class="section-head reveal"><div><span class="section-number">02</span><span class="section-kicker">Current research program</span></div><div><h2>Resilient Housing, Disaster Recovery &amp; Climate Decision Systems.</h2><p>At CECREH, Texas Tech University, research on recovery capacity, housing, climate hazards, growth, and vulnerability is translated into public-facing analytical systems for researchers, practitioners, governments, and communities.</p></div></div>
<article class="current-research-overview reveal"><div><span class="program-label">2025.10–Present · Postdoctoral Research Associate</span><h3>From research evidence to decision-ready tools</h3><p>{{ projects[0].description }}</p><ul>{% for bullet in projects[0].bullets %}<li>{{ bullet }}</li>{% endfor %}</ul><div class="program-links"><a class="btn btn-primary" href="{{ socials.cecreh }}" target="_blank" rel="noopener">Visit CECREH ↗</a><span>HUD &amp; NSF · $2M research portfolio</span></div></div><div class="program-visual"><img src="assets/img/dashboard-climate-housing-overview.webp" alt="Climate-Housing Exposure Index Dashboard preview" loading="lazy"><span>Interactive climate and housing decision support</span></div></article>

<div class="dashboard-research-grid">
{% for dashboard in dashboards %}<article id="{{ dashboard.id }}" class="dashboard-research-card dashboard-card-{{ dashboard.accent }} reveal"><a class="dashboard-research-image" href="{{ dashboard.url }}" target="_blank" rel="noopener"><img src="{{ dashboard.image }}" alt="{{ dashboard.image_alt }}" loading="lazy"><span class="live-badge"><i></i> Live research product</span></a><div class="dashboard-research-content"><div class="dashboard-heading"><span>{{ dashboard.scope }}</span><h3>{{ dashboard.title }}</h3><p class="dashboard-subtitle">{{ dashboard.subtitle }}</p></div><p>{{ dashboard.summary }}</p><div class="dashboard-detail-columns"><div><h4>What it enables</h4><ul>{% for feature in dashboard.features %}<li>{{ feature }}</li>{% endfor %}</ul></div><div><h4>Research scale</h4><ul>{% for metric in dashboard.metrics %}<li>{{ metric }}</li>{% endfor %}</ul></div></div><div class="dashboard-audience"><strong>Designed for</strong><span>{{ dashboard.audience }}</span></div><div class="dashboard-actions"><a class="btn btn-primary" href="{{ dashboard.url }}" target="_blank" rel="noopener">Launch dashboard ↗</a><a class="text-link" href="mailto:kflu.917@gmail.com?subject={{ dashboard.title | urlencode }}">Discuss the research ↗</a></div></div></article>{% endfor %}
</div></div></section>

<section class="section"><div class="container"><div class="section-head reveal"><div><span class="section-number">03</span><span class="section-kicker">Project portfolio</span></div><div><h2>Research experience from doctoral work to foundational engineering projects.</h2><p>Project dates, roles, funding, and descriptions are updated from the latest CV; visual materials are retained from the original GitHub webpage package.</p></div></div><div class="project-archive">{% for p in projects[1:] %}<article id="{{ p.id }}" class="archive-project reveal {% if p.featured %}archive-project-featured{% endif %}"><div class="archive-project-image"><img src="{{ p.image }}" alt="{{ p.image_alt }}" loading="lazy"></div><div class="archive-project-body"><div class="archive-project-meta"><span>{{ p.date }}</span><span>{{ p.role }}</span></div><h3>{{ p.title }}</h3><p>{{ p.description }}</p>{% if p.bullets %}<ul>{% for bullet in p.bullets %}<li>{{ bullet }}</li>{% endfor %}</ul>{% endif %}<div class="funding-line">{{ p.funding }}</div></div></article>{% endfor %}</div></div></section>
<section class="section method-section"><div class="container"><div class="method-layout"><div class="reveal"><span class="section-kicker">Methods &amp; tools</span><h2>Computational methods grounded in planning and engineering questions.</h2><p>Programming languages and software listed in the CV include Python, MATLAB, R, Java, C/C++, ArcGIS, AutoCAD, PTV VISUM, TransCAD, SketchUp, FLUENT, Microsoft Office, and Origin.</p></div><div class="method-cloud reveal"><span>Spatial Data Analysis</span><span>Graph Neural Networks</span><span>Deep Reinforcement Learning</span><span>Structural Equation Modeling</span><span>Natural Language Processing</span><span>Large Language Models</span><span>Spatiotemporal Forecasting</span><span>GIS Dashboards</span><span>Traffic Simulation</span><span>Environmental Monitoring</span></div></div></div></section>

'''
PUBLICATIONS_TEMPLATE = r'''
{{ page_hero | safe }}
<section class="section publication-directory-section"><div class="container"><div class="directory-toolbar reveal"><label class="search-box"><span>Search</span><input id="publication-search" type="search" placeholder="Title, author, journal, year…" autocomplete="off"></label><div class="filter-groups"><div class="filter-row" aria-label="Filter by status"><button class="directory-filter active" data-filter-group="status" data-filter="all">All outputs</button><button class="directory-filter" data-filter-group="status" data-filter="published">Published</button><button class="directory-filter" data-filter-group="status" data-filter="in-press">In press</button><button class="directory-filter" data-filter-group="status" data-filter="review">Under review</button></div><div class="filter-row" aria-label="Filter by topic"><button class="directory-filter active" data-filter-group="topic" data-filter="all">All topics</button><button class="directory-filter" data-filter-group="topic" data-filter="planning-ai">Planning AI</button><button class="directory-filter" data-filter-group="topic" data-filter="mobility">Mobility</button><button class="directory-filter" data-filter-group="topic" data-filter="resilience">Resilience</button><button class="directory-filter" data-filter-group="topic" data-filter="environment">Environment</button><button class="directory-filter" data-filter-group="topic" data-filter="policy">Policy</button><button class="directory-filter" data-filter-group="topic" data-filter="machine-learning">Machine learning</button></div></div><div class="results-count" aria-live="polite"><strong id="visible-count">{{ all_publications|length }}</strong><span>records shown</span></div></div>
<div class="directory-head reveal"><div><span class="section-kicker">Journal papers & manuscripts</span><h2>Complete publication record</h2></div><a class="text-link" href="{{ socials.scholar }}" target="_blank" rel="noopener">Google Scholar ↗</a></div>
<div class="directory-list" id="publication-list">{% for pub in all_publications %}<article class="directory-entry publication-record reveal" data-status="{{ pub.status }}" data-topic="{{ pub.topic }}" data-search="{{ (pub.year ~ ' ' ~ pub.authors ~ ' ' ~ pub.title ~ ' ' ~ pub.venue ~ ' ' ~ pub.details)|lower }}"><div class="record-code"><span>{{ pub.id }}</span><strong>{{ pub.year }}</strong></div><div class="record-body"><div class="record-labels"><span>{{ pub.status | status_label }}</span><span>{{ pub.topic | topic_label }}</span></div><h3>{{ pub.title }}</h3><p>{{ pub.authors | highlight_name }} · <em>{{ pub.venue }}</em>{% if pub.details %}, {{ pub.details }}{% endif %}</p></div>{% if pub.doi %}<a class="record-link" href="{{ pub.doi }}" target="_blank" rel="noopener" aria-label="Open DOI for {{ pub.title }}">DOI ↗</a>{% else %}<span class="record-link record-link-muted">{{ pub.status | status_label }}</span>{% endif %}</article>{% endfor %}</div><div class="empty-state" id="publication-empty" hidden>No records match the current search and filters.</div></div></section>
<section class="section section-tint"><div class="container"><div class="section-head reveal"><div><span class="section-number">02</span><span class="section-kicker">Additional outputs</span></div><div><h2>Book chapters and technical reports.</h2><p>These outputs extend the publication record into professional synthesis, transportation practice, and applied research.</p></div></div><div class="output-columns"><div><h3 class="output-heading">Book chapters</h3>{% for item in books %}<article class="compact-output reveal"><span>{{ item.id }} · {{ item.year }}</span><h4>{{ item.title }}</h4><p>{{ item.authors | highlight_name }} · {{ item.venue }}</p><a href="{{ item.url }}" target="_blank" rel="noopener">Open chapter ↗</a></article>{% endfor %}</div><div><h3 class="output-heading">Technical reports</h3>{% for item in reports %}<article class="compact-output reveal"><span>{{ item.id }} · {{ item.year }}</span><h4>{{ item.title }}</h4><p>{{ item.authors | highlight_name }} · {{ item.venue }}</p><a href="{{ item.url }}" target="_blank" rel="noopener">Open report ↗</a></article>{% endfor %}</div></div></div></section>
'''

ACTIVITIES_TEMPLATE = r'''
{{ page_hero | safe }}
<section id="teaching" class="section"><div class="container"><div class="section-head reveal"><div><span class="section-number">01</span><span class="section-kicker">Teaching</span></div><div><h2>Instruction across modeling, policy, climate, GIS, and operations research.</h2><p>Teaching roles from the University of Florida and Shanghai Jiao Tong University.</p></div></div><div class="activity-table reveal"><div class="activity-row activity-row-head"><span>Term</span><span>Course</span><span>Level</span><span>Role</span></div>{% for item in teaching %}<div class="activity-row"><span>{{ item[0] }}</span><div><strong>{{ item[1] }}</strong><small>{{ item[4] }}</small></div><span>{{ item[2] }}</span><span>{{ item[3] }}</span></div>{% endfor %}</div></div></section>
<section id="service" class="section section-tint"><div class="container"><div class="section-head reveal"><div><span class="section-number">02</span><span class="section-kicker">Academic service</span></div><div><h2>Mentoring, peer review, affiliations, and conference service.</h2><p>Selected academic contributions documented in the latest CV.</p></div></div><div class="service-grid"><article class="service-card service-card-wide reveal"><span class="recognition-label">Mentoring</span><h3>Mentor–mentee experience</h3><div class="service-list">{% for item in mentoring %}<div><span>{{ item[3] }}</span><p><strong>{{ item[1] }}</strong><br>{{ item[2] }} · {{ item[0] }}</p></div>{% endfor %}</div></article><article class="service-card reveal"><span class="recognition-label">Peer review</span><h3>Journal reviewer service</h3><div class="service-list service-list-compact">{% for item in reviewers %}<div><span>{{ item[1] }}</span><p>{{ item[0] }}</p></div>{% endfor %}</div></article><article class="service-card reveal"><span class="recognition-label">Affiliations</span><h3>Institutional &amp; professional communities</h3><div class="service-affiliations"><a href="{{ socials.cecreh }}" target="_blank" rel="noopener"><span class="affiliation-monogram ttu">TTU</span><div><strong>CECREH · Texas Tech University</strong><small>Postdoctoral Research Associate</small></div><i>↗</i></a><a href="{{ socials.iadapt }}" target="_blank" rel="noopener"><span class="affiliation-monogram uf">UF</span><div><strong>iAdapt · University of Florida</strong><small>Member / Research Affiliate</small></div><i>↗</i></a></div><ul class="clean-list"><li>International Association for China Planning (IACP), Student Member</li><li>University of Florida Transportation Institute (UFTI), Student Member</li><li>Committee on Extreme Weather and Climate Change Adaptation (AMR50), Friend Member</li></ul><div class="event-note"><strong>Conference events</strong><p>Co-hosted “AI and Cities: An International Forum for Innovation and Collaboration” at the University of Florida (2025).</p><p>Co-organized the CECREH Inaugural Summit at Texas Tech University (2025).</p></div></article></div></div></section>
<section id="awards" class="section"><div class="container"><div class="section-head reveal"><div><span class="section-number">03</span><span class="section-kicker">Awards & certificates</span></div><div><h2>Recognition in research, planning analysis, and quantitative modeling.</h2><p>Selected awards, scholarships, and professional certificates.</p></div></div><div class="award-certificate-layout"><div><h3 class="output-heading">Awards & scholarships</h3><div class="award-timeline">{% for item in awards %}<article class="award-entry reveal"><span>{{ item[0] }}</span><div><h4>{{ item[1] }}</h4><p>{{ item[2] }}</p></div></article>{% endfor %}</div></div><div><h3 class="output-heading">Certificates</h3><div class="certificate-stack">{% for item in certificates %}<article class="certificate-card reveal"><span>{{ item[0] }}</span><h4>{{ item[1] }}</h4><p>{{ item[2] }}</p></article>{% endfor %}</div><h3 class="output-heading skills-heading">Technical skills</h3><div class="skill-block reveal"><p><strong>Programming:</strong> Python, MATLAB, R, Java, C/C++</p><p><strong>Software:</strong> ArcGIS, AutoCAD, PTV VISUM, TransCAD, SketchUp, FLUENT, Microsoft Office, Origin</p></div></div></div></div></section>
<section id="presentations" class="section section-tint"><div class="container"><div class="section-head reveal"><div><span class="section-number">04</span><span class="section-kicker">Presentations & talks</span></div><div><h2>Conference presentations from transportation, planning, resilience, and environmental research.</h2><p>Fifteen conference presentations and one invited guest lecture are listed in the current CV.</p></div></div><div class="presentation-list">{% for item in presentations %}<article class="presentation-entry reveal"><span>{{ item[0] }}</span><div><h3>{{ item[2] }}</h3><p>{{ item[1] }} · {{ item[3] }}</p></div></article>{% endfor %}</div><div class="invited-block reveal"><span class="recognition-label">Invited talk</span>{% for item in invited_talks %}<h3>{{ item[2] }}</h3><p>{{ item[0] }} · {{ item[1] }} · {{ item[3] }}</p>{% endfor %}</div></div></section>
'''

ERROR_TEMPLATE = r'''
<section class="error-page"><div class="error-grid" aria-hidden="true"></div><div class="container error-card reveal"><span>404</span><h1>This route has moved.</h1><p>The redesigned portfolio uses a clearer set of pages. Continue to the homepage, research portfolio, or publication directory.</p><div class="hero-actions"><a class="btn btn-primary" href="index.html">Homepage</a><a class="btn btn-ghost" href="research.html">Research</a><a class="btn btn-ghost" href="publications.html">Publications</a></div></div></section>'''


def render_base(*, page: str, title: str, description: str, filename: str, content: str) -> str:
    return env.from_string(BASE_TEMPLATE).render(
        page=page, title=title, description=description, canonical=BASE_URL + ("" if filename == "index.html" else filename), base_url=BASE_URL, socials=SOCIALS, content=Markup(content)
    )


def make_page_hero(eyebrow: str, heading: str, lead: str, aside: str, actions: str = "") -> str:
    return env.from_string(PAGE_HERO).render(eyebrow=eyebrow, heading=Markup(heading), lead=lead, aside=Markup(aside), actions=Markup(actions))


def write(filename: str, text: str) -> None:
    path = ROOT / filename
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def main() -> None:
    selected = [PUBLICATIONS[0], PUBLICATIONS[1], PUBLICATIONS[2], PUBLICATIONS[3], PUBLICATIONS[4], PUBLICATIONS[6]]
    home = env.from_string(HOME_TEMPLATE).render(socials=SOCIALS, themes=RESEARCH_THEMES, projects=PROJECTS, dashboards=DASHBOARDS, selected_publications=selected, education=EDUCATION, teaching=TEACHING, awards=AWARDS)
    write("index.html", render_base(page="home", title="Kai-Fa Lu | Urban Resilience, Planning AI & GeoAI", description="Academic portfolio of Kai-Fa Lu, a postdoctoral researcher integrating urban resilience, planning AI, traffic modeling, environmental engineering, GeoAI, big data, and machine learning.", filename="index.html", content=home))

    research_hero = make_page_hero(
        "Research portfolio",
        "Engineering <em>intelligent and resilient</em> urban systems.",
        "A project portfolio spanning disaster recovery and housing, shared mobility, transportation-network resilience, environmental monitoring, traffic policy, GeoAI, and machine learning.",
        '<div class="hero-aside-stat"><strong>2</strong><span>live resilience dashboards</span></div><div class="hero-aside-stat"><strong>11</strong><span>additional research projects</span></div><div class="hero-aside-stat"><strong>$2M</strong><span>current HUD & NSF research portfolio</span></div><a class="aside-link" href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener">Open complete CV ↗</a>',
        '<a class="btn btn-primary" href="#cecreh">Current research ↓</a><a class="btn btn-ghost" href="publications.html">Publications ↗</a>'
    )
    research = env.from_string(RESEARCH_TEMPLATE).render(page_hero=Markup(research_hero), themes=RESEARCH_THEMES, projects=PROJECTS, dashboards=DASHBOARDS, socials=SOCIALS)
    write("research.html", render_base(page="research", title="Research | Kai-Fa Lu", description="Research portfolio of Kai-Fa Lu across urban resilience, planning AI, traffic modeling, environmental engineering, GeoAI, big data, and machine learning.", filename="research.html", content=research))

    all_pubs = PUBLICATIONS + UNDER_REVIEW
    pub_hero = make_page_hero(
        "Scholarly record",
        "Research across <em>planning, mobility, resilience, and environment.</em>",
        "A complete, searchable record updated from the latest CV, including peer-reviewed journal articles, manuscripts under review, book chapters, and technical reports.",
        '<div class="hero-aside-stat"><strong>27</strong><span>journal publications</span></div><div class="hero-aside-stat"><strong>15</strong><span>manuscripts under review</span></div><div class="hero-aside-stat"><strong>5</strong><span>book chapters & technical reports</span></div>',
        '<a class="btn btn-primary" href="#publication-list">Browse record ↓</a><a class="btn btn-ghost" href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener">Open CV ↗</a>'
    )
    pubs = env.from_string(PUBLICATIONS_TEMPLATE).render(page_hero=Markup(pub_hero), all_publications=all_pubs, books=BOOKS, reports=REPORTS, socials=SOCIALS)
    write("publications.html", render_base(page="publications", title="Publications | Kai-Fa Lu", description="Complete publication record for Kai-Fa Lu: 27 journal publications, 15 manuscripts under review, book chapters, and technical reports.", filename="publications.html", content=pubs))

    activities_hero = make_page_hero(
        "Academic activities",
        "Teaching, service, <em>recognition, and scholarly exchange.</em>",
        "A CV-derived record of teaching, mentoring, peer review, professional affiliations, awards, certificates, conference presentations, and invited talks.",
        '<div class="hero-aside-stat"><strong>6</strong><span>teaching appointments</span></div><div class="hero-aside-stat"><strong>8</strong><span>mentoring relationships</span></div><div class="hero-aside-stat"><strong>16</strong><span>presentations & invited talks</span></div>',
        '<a class="btn btn-primary" href="#teaching">Explore activities ↓</a><a class="btn btn-ghost" href="assets/Kaifa-Lu-CV.pdf" target="_blank" rel="noopener">Open CV ↗</a>'
    )
    acts = env.from_string(ACTIVITIES_TEMPLATE).render(page_hero=Markup(activities_hero), teaching=TEACHING, mentoring=MENTORING, reviewers=REVIEWERS, affiliations=AFFILIATIONS, awards=AWARDS, certificates=CERTIFICATES, presentations=PRESENTATIONS, invited_talks=INVITED_TALKS, socials=SOCIALS)
    write("activities.html", render_base(page="activities", title="Activities | Kai-Fa Lu", description="Teaching, academic service, awards, certificates, presentations, and invited talks by Kai-Fa Lu.", filename="activities.html", content=acts))

    error = env.from_string(ERROR_TEMPLATE).render()
    write("404.html", render_base(page="404", title="Page Not Found | Kai-Fa Lu", description="The requested page has moved within Kai-Fa Lu's redesigned academic portfolio.", filename="404.html", content=error))


if __name__ == "__main__":
    main()
