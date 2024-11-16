# 🌱 **Carbon Footprint Calculator**

## **About the Project**
The **Carbon Footprint Calculator** is an interactive web application built using **Streamlit**. It allows users to estimate their carbon emissions based on their daily activities. By simply describing their activities (e.g., "I drove my car for 50 km and used electricity for 100 kWh"), users can:
- Parse their inputs into meaningful activities and quantities.
- Calculate carbon emissions using predefined emission factors.
- Visualize the emissions by activity.
- Download the emission report as a CSV file.

This project empowers individuals to understand their carbon footprint and take steps toward a more sustainable future.

---

## **Features**
- **Natural Language Parsing**: Automatically recognizes activities and quantities from user inputs.
- **Activity Categories**: Includes emissions from transportation, energy usage, cooking, waste management, and more.
- **Emission Calculations**: Uses predefined emission factors to calculate carbon emissions.
- **Interactive Visualization**: Displays a bar chart showing emissions by activity.
- **Exportable Reports**: Users can download their emission results as a CSV file.

---

## **Dataset**
The project utilizes the dataset **`Updated_CO2_Emission_Factors.xlsx`** to calculate emissions. This dataset contains:
- **Activity descriptions**.
- **Corresponding CO₂ emission factors** (in kg CO₂/unit).

### **Dataset Preview**:
| **Activity**            | **CO₂ Emission Factor (kg CO₂/unit)** |
|--------------------------|---------------------------------------|
| Air travel (short haul)  | 0.254                                 |
| Electricity usage (kWh)  | 0.233                                 |
| Driving (km)             | 0.12                                  |
| Water usage (liters)     | 0.001                                 |
| Plastic waste (kg)       | 6.0                                   |

The emission factors were compiled from reputable sources to provide accurate and reliable calculations.

---

## **Tech Stack**
- **Frontend**: Streamlit
- **Backend**: Python
- **NLP**: SpaCy
- **Data Visualization**: Matplotlib, Streamlit Pyplot
- **Data Handling**: Pandas
- **Dataset**: `Updated_CO2_Emission_Factors.xlsx`

---

## **How to Run**
1. **Install Dependencies**:
   Install all required libraries and dependencies using the following command:
   ```bash
   pip install -r requirements.txt

**Required dependencies**:

Streamlit
Pandas
Matplotlib
Spacy
OpenPyXL (for handling Excel files)
Regex

2. **Run the App: Launch the Streamlit application using:**:
   streamlit run carbon_footprint_app.py

3. **Open the App in Your Browser:**
   The app will open in your default browser at a URL like http://localhost:8501.

---
## **Screenshots**
**Input and Results:**
![image](https://github.com/user-attachments/assets/2ce8d2cb-603d-4630-873b-e89fd6c2d1a7)
![image](https://github.com/user-attachments/assets/ae077a47-c243-4828-8269-5f6a0d8227a7)
![image](https://github.com/user-attachments/assets/2af6db02-bbad-4ac4-9dea-b7f3540784b5)

**Emission Visualization:**
![image](https://github.com/user-attachments/assets/d60088fd-b254-4f62-a50b-4f9ba32518ea)

---
## **Acknowledgements**

SpaCy for natural language processing.
Streamlit for building interactive web applications.
Data compiled from reputable sources to provide accurate emission factors.



