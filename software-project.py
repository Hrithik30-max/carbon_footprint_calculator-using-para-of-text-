import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import spacy
from spacy.matcher import PhraseMatcher

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Specific Keywords Mapping
specific_keywords = {
    # Travel and Transport
    "flight": "air travel",
    "fly": "air travel",
    "electric car": "electric vehicle travel",
    "ev": "electric vehicle travel",
    "train": "train travel",
    "rail": "train travel",
    "metro": "metro travel",
    "drive": "driving",
    "drove": "driving",
    "car": "driving",
    "bus": "bus travel",
    "coach": "bus travel",
    "cycle": "cycling",
    "bicycle": "cycling",
    "bike": "cycling",
    "walk": "walking",
    "walking": "walking",

    # Energy Consumption
    "electricity": "electricity usage",
    "power consumption": "electricity usage",
    "energy consumption": "electricity usage",
    "ac": "air conditioner",
    "air conditioner": "air conditioner",
    "heater": "heating usage",
    "heating": "heating usage",
    "fan": "fan usage",
    "cooling": "fan usage",

    # Cooking and Appliances
    "gas stove": "gas stove usage",
    "oven": "oven usage",
    "microwave": "microwave usage",
    "toaster": "toaster usage",
    "cooking": "cooking gas usage",
    "stove": "cooking gas usage",

    # Water Usage
    "water": "water usage",
    "shower": "shower usage",
    "bath": "bath usage",
    "washing machine": "washing machine usage",
    "laundry": "laundry usage",
    "wash": "laundry usage",

    # Waste Management
    "plastic": "plastic waste management",
    "recycling": "recycling",
    "trash": "trash disposal",
    "waste": "trash disposal",
    "compost": "composting",
    "organic waste": "organic waste management",

    # Miscellaneous
    "light": "lighting usage",
    "bulb": "lighting usage",
    "charging": "device charging",
    "charge": "device charging",
    "phone": "device charging",
    "laptop": "device charging",
    "desktop": "computer usage",
    "computer": "computer usage",
    "printer": "printer usage"
}

# Define a PhraseMatcher for multi-word activities
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(key) for key in specific_keywords.keys()]
matcher.add("ACTIVITY", patterns)

# Preload the Emission Factors Dataset
EMISSION_FACTORS_FILE = "Updated_CO2_Emission_Factors.xlsx"
emission_factors = pd.read_excel(EMISSION_FACTORS_FILE)

# Function to parse inputs
def parse_specific_inputs_with_spacy_and_regex(user_inputs):
    parsed_activities = []
    doc = nlp(user_inputs)

    for sent in doc.sents:
        sub_sentences = re.split(r'\s+and\s+', sent.text)
        for sub_sentence in sub_sentences:
            quantities = re.findall(r'\b\d+(?:\.\d+)?\b', sub_sentence)
            quantities = [float(q) for q in quantities]

            sub_doc = nlp(sub_sentence)
            matches = matcher(sub_doc)
            activities = [specific_keywords[sub_doc[start:end].text.lower()] for _, start, end in matches]
            activities = list(dict.fromkeys(activities))

            while quantities and activities:
                parsed_activities.append({
                    "activity": activities.pop(0),
                    "quantity": quantities.pop(0)
                })

    return parsed_activities

# Emission calculation function
def calculate_emissions(parsed_inputs, emission_factors):
    results = []
    total_emissions = 0

    for entry in parsed_inputs:
        activity = entry["activity"]
        quantity = entry["quantity"]
        matching_rows = emission_factors[
            emission_factors["Activity"].str.contains(f"^{re.escape(activity)}$", case=False, regex=True)
        ]

        if not matching_rows.empty:
            emission_factor = matching_rows["CO₂ Emission Factor (kg CO₂/unit)"].values[0]
        else:
            emission_factor = 0

        emissions = quantity * emission_factor
        total_emissions += emissions

        results.append({
            "activity": activity,
            "quantity": quantity,
            "emissions": emissions
        })

    return results, total_emissions

# Visualization function
def visualize_emissions(emission_results):
    activities = [entry["activity"] for entry in emission_results]
    emissions = [entry["emissions"] for entry in emission_results]
    plt.figure(figsize=(10, 6))
    plt.barh(activities, emissions, color='skyblue')
    plt.xlabel("Emissions (kg CO₂)", fontsize=12)
    plt.ylabel("Activities", fontsize=12)
    plt.title("Carbon Emissions by Activity", fontsize=16)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit app
st.title("🌱 Carbon Footprint Calculator")
st.markdown("""
### Welcome to the Carbon Footprint Calculator!
This tool helps you calculate your carbon emissions based on your daily activities. Here's how to use it:
1. Enter your activities in the text box below (e.g., "I drove my car for 50 km and used electricity for 100 kWh").
2. Click the "Calculate Emissions" button.
3. View your emissions breakdown and total emissions.

🌟 **Take a step toward understanding and reducing your carbon footprint!**
""")

# Text input for activities
user_input = st.text_area(
    "Describe your activities (e.g., 'I rode my bike for 15 kilometers and used electricity for 200 kWh'):",
    height=200
)

if st.button("🔍 Calculate Emissions"):
    if not user_input.strip():
        st.error("❌ Please enter some activities.")
    else:
        st.markdown("### 📝 Parsed Inputs")
        parsed_inputs = parse_specific_inputs_with_spacy_and_regex(user_input)
        st.json(parsed_inputs)

        st.markdown("### 📊 Emission Results")
        emission_results, total_emissions = calculate_emissions(parsed_inputs, emission_factors)
        st.json(emission_results)
        st.success(f"🌍 **Your total emissions: {total_emissions:.2f} kg CO₂**")

        st.markdown("#### Visualization")
        visualize_emissions(emission_results)

        st.markdown("### 📥 Download Your Emission Report")
        results_df = pd.DataFrame(emission_results)
        results_csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", results_csv, "emission_results.csv", "text/csv")

# Footer
st.markdown("""
---
🌍 **Did you know?**
- Transportation accounts for about 29% of global CO₂ emissions.
- Simple actions like using public transport, cycling, or walking can significantly reduce your carbon footprint.
- Let's work together for a greener planet! 🌱
""")
