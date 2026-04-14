import streamlit as st
import os
import shutil
import re
import time
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Virec Data Pipeline",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Virec Data Processing Pipeline")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #f4f6f9;
}
.block-container {
    padding-top: 2rem;
}
.section-card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
### 🏢 Data Engineering Control Panel  
**Environment:** Production  
**Pipeline Phase:** Extraction → Cleaning & Transformation  
""")

# -------------------- ROOT PATH --------------------
root_path = r"D:\virec_data_process\3.1 Full Extraction Phase"

st.markdown("## 📌 Pipeline Configuration")
col1, col2, col3 = st.columns(3)

# -------------------- STATE --------------------
path_state = Path(root_path)
states = [f.name for f in path_state.iterdir() if f.is_dir()]

with col1:
    State = st.selectbox("State", ["Select State"] + states)

# -------------------- COUNTY --------------------
with col2:
    if State != "Select State":
        path_county = Path(root_path) / State
        counties = [f.name for f in path_county.iterdir() if f.is_dir()]
        County = st.selectbox("County", ["Select County"] + counties)
    else:
        County = st.selectbox("County", ["Select State First"])

# -------------------- CATEGORY --------------------
with col3:
    if State != "Select State" and County != "Select County":
        path_category = Path(root_path) / State / County
        categories = [f.name for f in path_category.iterdir() if f.is_dir()]
        Category = st.selectbox("Category", ["Select Category"] + categories)
    else:
        Category = st.selectbox("Category", ["Select County First"])

# -------------------- BUTTON --------------------
if Category not in ["Select Category", "Select County First"]:
    submit = st.button("🚀 Start Pipeline")
else:
    submit = False

# -------------------- CATEGORY SHORT MAP --------------------
category_map = {
    "Property": "prop",
    "Business": "bus",
    "Permits": "permits",
    "Transaction Log": "trxlog"
}

# -------------------- FILENAME VALIDATION --------------------
def validate_filename(file_name, expected_short,result_dict):
    errors = []

    if not file_name.lower().endswith(".csv"):
        errors.append("File must be .csv")
        return errors

    base = file_name[:-4]
    parts = base.split("_")

    if len(parts) < 8:
        errors.append("Filename must contain at least 8 parts")
        return errors

    country = parts[0]
    state = parts[1]
    fips = parts[2]
    extraction_cat = parts[3]
    category = parts[4]
    bronze = parts[-2]
    date = parts[-1]
    subtype = "_".join(parts[5:-2])

    if country != "us":
        errors.append("Country must be 'us'")

    if len(state) != 2:
        errors.append("State must be 2 letters")

    if not re.fullmatch(r"\d{5}", fips):
        errors.append("FIPS must be 5 digits")

    if extraction_cat != "data":
        errors.append("Extraction category must be 'data'")

    if category != expected_short:
        errors.append(f"Category must be '{expected_short}'")

    if not subtype:
        errors.append("Subtype missing")

    if bronze != "bronze":
        errors.append("Missing 'bronze' before date")

    if not re.fullmatch(r"\d{8}", date):
        errors.append("Date must be YYYYMMDD format")

    if not fips == result_dict['fips']:
        errors.append(f"Invalid Fips code. correct code is {result_dict['fips']}")

    return errors

# -------------------- MAIN PIPELINE --------------------
if submit:

    expected_short = category_map.get(Category)

    base_path = r"\\192.168.3.103\d\virec_data_process"

    src_dir = os.path.join(
        base_path,
        "3.1 Full Extraction Phase",
        State,
        County,
        Category
    )

    dest_base = os.path.join(
        base_path,
        "4.1 Cleaning & Transformation Phase",
        State,
        County,
        Category
    )
    state_map = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}
    state_short = state_map[State]
    county_map =[
{
    "fips": "01007",
    "state": "AL",
    "county": "Bibb"
  },
  {
    "fips": "22019",
    "state": "LA",
    "county": "Calcasieu"
  },
  {
    "fips": "26077",
    "state": "MI",
    "county": "Kalamazoo"
  },
  {
    "fips": "26061",
    "state": "MI",
    "county": "Houghton"
  },
  {
    "fips": "27097",
    "state": "MN",
    "county": "Morrison"
  },
  {
    "fips": "28107",
    "state": "MS",
    "county": "Panola"
  },
  {
    "fips": "72079",
    "state": "PR",
    "county": "Lajas"
  },
  {
    "fips": "39033",
    "state": "OH",
    "county": "Crawford"
  },
  {
    "fips": "42059",
    "state": "PA",
    "county": "Greene"
  },
  {
    "fips": "13281",
    "state": "GA",
    "county": "Towns"
  },
  {
    "fips": "17111",
    "state": "IL",
    "county": "McHenry"
  },
  {
    "fips": "54003",
    "state": "WV",
    "county": "Berkeley"
  },
  {
    "fips": "54055",
    "state": "WV",
    "county": "Mercer"
  },
  {
    "fips": "27035",
    "state": "MN",
    "county": "Crow Wing"
  },
  {
    "fips": "28023",
    "state": "MS",
    "county": "Clarke"
  },
  {
    "fips": "37137",
    "state": "NC",
    "county": "Pamlico"
  },
  {
    "fips": "01067",
    "state": "AL",
    "county": "Henry"
  },
  {
    "fips": "20107",
    "state": "KS",
    "county": "Linn"
  },
  {
    "fips": "21081",
    "state": "KY",
    "county": "Grant"
  },
  {
    "fips": "28013",
    "state": "MS",
    "county": "Calhoun"
  },
  {
    "fips": "48313",
    "state": "TX",
    "county": "Madison"
  },
  {
    "fips": "48449",
    "state": "TX",
    "county": "Titus"
  },
  {
    "fips": "40083",
    "state": "OK",
    "county": "Logan"
  },
  {
    "fips": "37013",
    "state": "NC",
    "county": "Beaufort"
  },
  {
    "fips": "51033",
    "state": "VA",
    "county": "Caroline"
  },
  {
    "fips": "39039",
    "state": "OH",
    "county": "Defiance"
  },
  {
    "fips": "51179",
    "state": "VA",
    "county": "Stafford"
  },
  {
    "fips": "51069",
    "state": "VA",
    "county": "Frederick"
  },
  {
    "fips": "49057",
    "state": "UT",
    "county": "Weber"
  },
  {
    "fips": "28123",
    "state": "MS",
    "county": "Scott"
  },
  {
    "fips": "08123",
    "state": "CO",
    "county": "Weld"
  },
  {
    "fips": "18027",
    "state": "IN",
    "county": "Daviess"
  },
  {
    "fips": "21071",
    "state": "KY",
    "county": "Floyd"
  },
  {
    "fips": "42061",
    "state": "PA",
    "county": "Huntingdon"
  },
  {
    "fips": "48331",
    "state": "TX",
    "county": "Milam"
  },
  {
    "fips": "37027",
    "state": "NC",
    "county": "Caldwell"
  },
  {
    "fips": "72013",
    "state": "PR",
    "county": "Arecibo"
  },
  {
    "fips": "13007",
    "state": "GA",
    "county": "Baker"
  },
  {
    "fips": "48397",
    "state": "TX",
    "county": "Rockwall"
  },
  {
    "fips": "24510",
    "state": "MD",
    "county": "Baltimore"
  },
  {
    "fips": "36005",
    "state": "NY",
    "county": "Bronx"
  },
  {
    "fips": "48191",
    "state": "TX",
    "county": "Hall"
  },
  {
    "fips": "56035",
    "state": "WY",
    "county": "Sublette"
  },
  {
    "fips": "45065",
    "state": "SC",
    "county": "McCormick"
  },
  {
    "fips": "20203",
    "state": "KS",
    "county": "Wichita"
  },
  {
    "fips": "42031",
    "state": "PA",
    "county": "Clarion"
  },
  {
    "fips": "28157",
    "state": "MS",
    "county": "Wilkinson"
  },
  {
    "fips": "36095",
    "state": "NY",
    "county": "Schoharie"
  },
  {
    "fips": "42093",
    "state": "PA",
    "county": "Montour"
  },
  {
    "fips": "01003",
    "state": "AL",
    "county": "Baldwin"
  },
  {
    "fips": "12067",
    "state": "FL",
    "county": "Lafayette"
  },
  {
    "fips": "22013",
    "state": "LA",
    "county": "Bienville"
  },
  {
    "fips": "42025",
    "state": "PA",
    "county": "Carbon"
  },
  {
    "fips": "17189",
    "state": "IL",
    "county": "Washington"
  },
  {
    "fips": "72121",
    "state": "PR",
    "county": "Sabana Grande"
  },
  {
    "fips": "20093",
    "state": "KS",
    "county": "Kearny"
  },
  {
    "fips": "23013",
    "state": "ME",
    "county": "Knox"
  },
  {
    "fips": "51735",
    "state": "VA",
    "county": "Poquoson"
  },
  {
    "fips": "39051",
    "state": "OH",
    "county": "Fulton"
  },
  {
    "fips": "45071",
    "state": "SC",
    "county": "Newberry"
  },
  {
    "fips": "18111",
    "state": "IN",
    "county": "Newton"
  },
  {
    "fips": "37001",
    "state": "NC",
    "county": "Alamance"
  },
  {
    "fips": "40069",
    "state": "OK",
    "county": "Johnston"
  },
  {
    "fips": "39075",
    "state": "OH",
    "county": "Holmes"
  },
  {
    "fips": "29029",
    "state": "MO",
    "county": "Camden"
  },
  {
    "fips": "37157",
    "state": "NC",
    "county": "Rockingham"
  },
  {
    "fips": "27121",
    "state": "MN",
    "county": "Pope"
  },
  {
    "fips": "29227",
    "state": "MO",
    "county": "Worth"
  },
  {
    "fips": "05055",
    "state": "AR",
    "county": "Greene"
  },
  {
    "fips": "56007",
    "state": "WY",
    "county": "Carbon"
  },
  {
    "fips": "05101",
    "state": "AR",
    "county": "Newton"
  },
  {
    "fips": "20209",
    "state": "KS",
    "county": "Wyandotte"
  },
  {
    "fips": "48091",
    "state": "TX",
    "county": "Comal"
  },
  {
    "fips": "28077",
    "state": "MS",
    "county": "Lawrence"
  },
  {
    "fips": "29139",
    "state": "MO",
    "county": "Montgomery"
  },
  {
    "fips": "51095",
    "state": "VA",
    "county": "James City"
  },
  {
    "fips": "38037",
    "state": "ND",
    "county": "Grant"
  },
  {
    "fips": "23029",
    "state": "ME",
    "county": "Washington"
  },
  {
    "fips": "29045",
    "state": "MO",
    "county": "Clark"
  },
  {
    "fips": "19035",
    "state": "IA",
    "county": "Cherokee"
  },
  {
    "fips": "37169",
    "state": "NC",
    "county": "Stokes"
  },
  {
    "fips": "42055",
    "state": "PA",
    "county": "Franklin"
  },
  {
    "fips": "40011",
    "state": "OK",
    "county": "Blaine"
  },
  {
    "fips": "54079",
    "state": "WV",
    "county": "Putnam"
  },
  {
    "fips": "13311",
    "state": "GA",
    "county": "White"
  },
  {
    "fips": "26069",
    "state": "MI",
    "county": "Iosco"
  },
  {
    "fips": "04013",
    "state": "AZ",
    "county": "Maricopa"
  },
  {
    "fips": "13001",
    "state": "GA",
    "county": "Appling"
  },
  {
    "fips": "08103",
    "state": "CO",
    "county": "Rio Blanco"
  },
  {
    "fips": "55005",
    "state": "WI",
    "county": "Barron"
  },
  {
    "fips": "20037",
    "state": "KS",
    "county": "Crawford"
  },
  {
    "fips": "27133",
    "state": "MN",
    "county": "Rock"
  },
  {
    "fips": "05147",
    "state": "AR",
    "county": "Woodruff"
  },
  {
    "fips": "13011",
    "state": "GA",
    "county": "Banks"
  },
  {
    "fips": "55081",
    "state": "WI",
    "county": "Monroe"
  },
  {
    "fips": "46065",
    "state": "SD",
    "county": "Hughes"
  },
  {
    "fips": "30061",
    "state": "MT",
    "county": "Mineral"
  },
  {
    "fips": "31021",
    "state": "NE",
    "county": "Burt"
  },
  {
    "fips": "28147",
    "state": "MS",
    "county": "Walthall"
  },
  {
    "fips": "46119",
    "state": "SD",
    "county": "Sully"
  },
  {
    "fips": "20043",
    "state": "KS",
    "county": "Doniphan"
  },
  {
    "fips": "31071",
    "state": "NE",
    "county": "Garfield"
  },
  {
    "fips": "39131",
    "state": "OH",
    "county": "Pike"
  },
  {
    "fips": "05059",
    "state": "AR",
    "county": "Hot Spring"
  },
  {
    "fips": "47159",
    "state": "TN",
    "county": "Smith"
  },
  {
    "fips": "51127",
    "state": "VA",
    "county": "New Kent"
  },
  {
    "fips": "01021",
    "state": "AL",
    "county": "Chilton"
  },
  {
    "fips": "21147",
    "state": "KY",
    "county": "McCreary"
  },
  {
    "fips": "28059",
    "state": "MS",
    "county": "Jackson"
  },
  {
    "fips": "10005",
    "state": "DE",
    "county": "Sussex"
  },
  {
    "fips": "39079",
    "state": "OH",
    "county": "Jackson"
  },
  {
    "fips": "22091",
    "state": "LA",
    "county": "St. Helena"
  },
  {
    "fips": "27151",
    "state": "MN",
    "county": "Swift"
  },
  {
    "fips": "05049",
    "state": "AR",
    "county": "Fulton"
  },
  {
    "fips": "39171",
    "state": "OH",
    "county": "Williams"
  },
  {
    "fips": "22009",
    "state": "LA",
    "county": "Avoyelles"
  },
  {
    "fips": "32009",
    "state": "NV",
    "county": "Esmeralda"
  },
  {
    "fips": "37061",
    "state": "NC",
    "county": "Duplin"
  },
  {
    "fips": "39059",
    "state": "OH",
    "county": "Guernsey"
  },
  {
    "fips": "47003",
    "state": "TN",
    "county": "Bedford"
  },
  {
    "fips": "47117",
    "state": "TN",
    "county": "Marshall"
  },
  {
    "fips": "45087",
    "state": "SC",
    "county": "Union"
  },
  {
    "fips": "20141",
    "state": "KS",
    "county": "Osborne"
  },
  {
    "fips": "29121",
    "state": "MO",
    "county": "Macon"
  },
  {
    "fips": "31111",
    "state": "NE",
    "county": "Lincoln"
  },
  {
    "fips": "48489",
    "state": "TX",
    "county": "Willacy"
  },
  {
    "fips": "22037",
    "state": "LA",
    "county": "East Feliciana"
  },
  {
    "fips": "26113",
    "state": "MI",
    "county": "Missaukee"
  },
  {
    "fips": "37131",
    "state": "NC",
    "county": "Northampton"
  },
  {
    "fips": "48387",
    "state": "TX",
    "county": "Red River"
  },
  {
    "fips": "17037",
    "state": "IL",
    "county": "DeKalb"
  },
  {
    "fips": "48505",
    "state": "TX",
    "county": "Zapata"
  },
  {
    "fips": "06013",
    "state": "CA",
    "county": "Contra Costa"
  },
  {
    "fips": "29197",
    "state": "MO",
    "county": "Schuyler"
  },
  {
    "fips": "16015",
    "state": "ID",
    "county": "Boise"
  },
  {
    "fips": "12011",
    "state": "FL",
    "county": "Broward"
  },
  {
    "fips": "29169",
    "state": "MO",
    "county": "Pulaski"
  },
  {
    "fips": "22053",
    "state": "LA",
    "county": "Jefferson Davis"
  },
  {
    "fips": "40095",
    "state": "OK",
    "county": "Marshall"
  },
  {
    "fips": "47147",
    "state": "TN",
    "county": "Robertson"
  },
  {
    "fips": "35021",
    "state": "NM",
    "county": "Harding"
  },
  {
    "fips": "28031",
    "state": "MS",
    "county": "Covington"
  },
  {
    "fips": "02122",
    "state": "AK",
    "county": "Kenai Peninsula"
  },
  {
    "fips": "29035",
    "state": "MO",
    "county": "Carter"
  },
  {
    "fips": "21175",
    "state": "KY",
    "county": "Morgan"
  },
  {
    "fips": "72023",
    "state": "PR",
    "county": "Cabo Rojo"
  },
  {
    "fips": "30043",
    "state": "MT",
    "county": "Jefferson"
  },
  {
    "fips": "12103",
    "state": "FL",
    "county": "Pinellas"
  },
  {
    "fips": "17131",
    "state": "IL",
    "county": "Mercer"
  },
  {
    "fips": "51036",
    "state": "VA",
    "county": "Charles City"
  },
  {
    "fips": "12085",
    "state": "FL",
    "county": "Martin"
  },
  {
    "fips": "72017",
    "state": "PR",
    "county": "Barceloneta"
  },
  {
    "fips": "19159",
    "state": "IA",
    "county": "Ringgold"
  },
  {
    "fips": "37101",
    "state": "NC",
    "county": "Johnston"
  },
  {
    "fips": "41001",
    "state": "OR",
    "county": "Baker"
  },
  {
    "fips": "42123",
    "state": "PA",
    "county": "Warren"
  },
  {
    "fips": "30023",
    "state": "MT",
    "county": "Deer Lodge"
  },
  {
    "fips": "45067",
    "state": "SC",
    "county": "Marion"
  },
  {
    "fips": "47099",
    "state": "TN",
    "county": "Lawrence"
  },
  {
    "fips": "51147",
    "state": "VA",
    "county": "Prince Edward"
  },
  {
    "fips": "21129",
    "state": "KY",
    "county": "Lee"
  },
  {
    "fips": "41069",
    "state": "OR",
    "county": "Wheeler"
  },
  {
    "fips": "48111",
    "state": "TX",
    "county": "Dallam"
  },
  {
    "fips": "46039",
    "state": "SD",
    "county": "Deuel"
  },
  {
    "fips": "06093",
    "state": "CA",
    "county": "Siskiyou"
  },
  {
    "fips": "33001",
    "state": "NH",
    "county": "Belknap"
  },
  {
    "fips": "53015",
    "state": "WA",
    "county": "Cowlitz"
  },
  {
    "fips": "13045",
    "state": "GA",
    "county": "Carroll"
  },
  {
    "fips": "46071",
    "state": "SD",
    "county": "Jackson"
  },
  {
    "fips": "05011",
    "state": "AR",
    "county": "Bradley"
  },
  {
    "fips": "27029",
    "state": "MN",
    "county": "Clearwater"
  },
  {
    "fips": "13301",
    "state": "GA",
    "county": "Warren"
  },
  {
    "fips": "47155",
    "state": "TN",
    "county": "Sevier"
  },
  {
    "fips": "39073",
    "state": "OH",
    "county": "Hocking"
  },
  {
    "fips": "38071",
    "state": "ND",
    "county": "Ramsey"
  },
  {
    "fips": "40085",
    "state": "OK",
    "county": "Love"
  },
  {
    "fips": "16007",
    "state": "ID",
    "county": "Bear Lake"
  },
  {
    "fips": "42085",
    "state": "PA",
    "county": "Mercer"
  },
  {
    "fips": "48295",
    "state": "TX",
    "county": "Lipscomb"
  },
  {
    "fips": "47103",
    "state": "TN",
    "county": "Lincoln"
  },
  {
    "fips": "37087",
    "state": "NC",
    "county": "Haywood"
  },
  {
    "fips": "02070",
    "state": "AK",
    "county": "Dillingham"
  },
  {
    "fips": "13083",
    "state": "GA",
    "county": "Dade"
  },
  {
    "fips": "36033",
    "state": "NY",
    "county": "Franklin"
  },
  {
    "fips": "37167",
    "state": "NC",
    "county": "Stanly"
  },
  {
    "fips": "13003",
    "state": "GA",
    "county": "Atkinson"
  },
  {
    "fips": "17197",
    "state": "IL",
    "county": "Will"
  },
  {
    "fips": "48273",
    "state": "TX",
    "county": "Kleberg"
  },
  {
    "fips": "38025",
    "state": "ND",
    "county": "Dunn"
  },
  {
    "fips": "48385",
    "state": "TX",
    "county": "Real"
  },
  {
    "fips": "16055",
    "state": "ID",
    "county": "Kootenai"
  },
  {
    "fips": "26057",
    "state": "MI",
    "county": "Gratiot"
  },
  {
    "fips": "45015",
    "state": "SC",
    "county": "Berkeley"
  },
  {
    "fips": "55041",
    "state": "WI",
    "county": "Forest"
  },
  {
    "fips": "02290",
    "state": "AK",
    "county": "Yukon-Koyukuk"
  },
  {
    "fips": "51750",
    "state": "VA",
    "county": "Radford"
  },
  {
    "fips": "48483",
    "state": "TX",
    "county": "Wheeler"
  },
  {
    "fips": "47025",
    "state": "TN",
    "county": "Claiborne"
  },
  {
    "fips": "25003",
    "state": "MA",
    "county": "Berkshire"
  },
  {
    "fips": "28093",
    "state": "MS",
    "county": "Marshall"
  },
  {
    "fips": "40115",
    "state": "OK",
    "county": "Ottawa"
  },
  {
    "fips": "26009",
    "state": "MI",
    "county": "Antrim"
  },
  {
    "fips": "17045",
    "state": "IL",
    "county": "Edgar"
  },
  {
    "fips": "21205",
    "state": "KY",
    "county": "Rowan"
  },
  {
    "fips": "31121",
    "state": "NE",
    "county": "Merrick"
  },
  {
    "fips": "38007",
    "state": "ND",
    "county": "Billings"
  },
  {
    "fips": "45013",
    "state": "SC",
    "county": "Beaufort"
  },
  {
    "fips": "54031",
    "state": "WV",
    "county": "Hardy"
  },
  {
    "fips": "41053",
    "state": "OR",
    "county": "Polk"
  },
  {
    "fips": "20091",
    "state": "KS",
    "county": "Johnson"
  },
  {
    "fips": "49025",
    "state": "UT",
    "county": "Kane"
  },
  {
    "fips": "12071",
    "state": "FL",
    "county": "Lee"
  },
  {
    "fips": "51530",
    "state": "VA",
    "county": "Buena Vista"
  },
  {
    "fips": "21065",
    "state": "KY",
    "county": "Estill"
  },
  {
    "fips": "45045",
    "state": "SC",
    "county": "Greenville"
  },
  {
    "fips": "27085",
    "state": "MN",
    "county": "McLeod"
  },
  {
    "fips": "20067",
    "state": "KS",
    "county": "Grant"
  },
  {
    "fips": "48133",
    "state": "TX",
    "county": "Eastland"
  },
  {
    "fips": "01053",
    "state": "AL",
    "county": "Escambia"
  },
  {
    "fips": "20205",
    "state": "KS",
    "county": "Wilson"
  },
  {
    "fips": "48077",
    "state": "TX",
    "county": "Clay"
  },
  {
    "fips": "13021",
    "state": "GA",
    "county": "Bibb"
  },
  {
    "fips": "37091",
    "state": "NC",
    "county": "Hertford"
  },
  {
    "fips": "32003",
    "state": "NV",
    "county": "Clark"
  },
  {
    "fips": "41041",
    "state": "OR",
    "county": "Lincoln"
  },
  {
    "fips": "51161",
    "state": "VA",
    "county": "Roanoke"
  },
  {
    "fips": "13273",
    "state": "GA",
    "county": "Terrell"
  },
  {
    "fips": "16075",
    "state": "ID",
    "county": "Payette"
  },
  {
    "fips": "13073",
    "state": "GA",
    "county": "Columbia"
  },
  {
    "fips": "17193",
    "state": "IL",
    "county": "White"
  },
  {
    "fips": "32013",
    "state": "NV",
    "county": "Humboldt"
  },
  {
    "fips": "40143",
    "state": "OK",
    "county": "Tulsa"
  },
  {
    "fips": "41021",
    "state": "OR",
    "county": "Gilliam"
  },
  {
    "fips": "16023",
    "state": "ID",
    "county": "Butte"
  },
  {
    "fips": "05069",
    "state": "AR",
    "county": "Jefferson"
  },
  {
    "fips": "05113",
    "state": "AR",
    "county": "Polk"
  },
  {
    "fips": "13213",
    "state": "GA",
    "county": "Murray"
  },
  {
    "fips": "06019",
    "state": "CA",
    "county": "Fresno"
  },
  {
    "fips": "08083",
    "state": "CO",
    "county": "Montezuma"
  },
  {
    "fips": "21211",
    "state": "KY",
    "county": "Shelby"
  },
  {
    "fips": "46059",
    "state": "SD",
    "county": "Hand"
  },
  {
    "fips": "53017",
    "state": "WA",
    "county": "Douglas"
  },
  {
    "fips": "49017",
    "state": "UT",
    "county": "Garfield"
  },
  {
    "fips": "05009",
    "state": "AR",
    "county": "Boone"
  },
  {
    "fips": "27027",
    "state": "MN",
    "county": "Clay"
  },
  {
    "fips": "20125",
    "state": "KS",
    "county": "Montgomery"
  },
  {
    "fips": "54069",
    "state": "WV",
    "county": "Ohio"
  },
  {
    "fips": "06035",
    "state": "CA",
    "county": "Lassen"
  },
  {
    "fips": "06091",
    "state": "CA",
    "county": "Sierra"
  },
  {
    "fips": "12035",
    "state": "FL",
    "county": "Flagler"
  },
  {
    "fips": "06069",
    "state": "CA",
    "county": "San Benito"
  },
  {
    "fips": "30107",
    "state": "MT",
    "county": "Wheatland"
  },
  {
    "fips": "39147",
    "state": "OH",
    "county": "Seneca"
  },
  {
    "fips": "39027",
    "state": "OH",
    "county": "Clinton"
  },
  {
    "fips": "47113",
    "state": "TN",
    "county": "Madison"
  },
  {
    "fips": "48197",
    "state": "TX",
    "county": "Hardeman"
  },
  {
    "fips": "51011",
    "state": "VA",
    "county": "Appomattox"
  },
  {
    "fips": "09009",
    "state": "CT",
    "county": "New Haven"
  },
  {
    "fips": "39085",
    "state": "OH",
    "county": "Lake"
  },
  {
    "fips": "26153",
    "state": "MI",
    "county": "Schoolcraft"
  },
  {
    "fips": "49045",
    "state": "UT",
    "county": "Tooele"
  },
  {
    "fips": "20059",
    "state": "KS",
    "county": "Franklin"
  },
  {
    "fips": "36077",
    "state": "NY",
    "county": "Otsego"
  },
  {
    "fips": "27065",
    "state": "MN",
    "county": "Kanabec"
  },
  {
    "fips": "17173",
    "state": "IL",
    "county": "Shelby"
  },
  {
    "fips": "26039",
    "state": "MI",
    "county": "Crawford"
  },
  {
    "fips": "41063",
    "state": "OR",
    "county": "Wallowa"
  },
  {
    "fips": "29021",
    "state": "MO",
    "county": "Buchanan"
  },
  {
    "fips": "51183",
    "state": "VA",
    "county": "Sussex"
  },
  {
    "fips": "48121",
    "state": "TX",
    "county": "Denton"
  },
  {
    "fips": "28145",
    "state": "MS",
    "county": "Union"
  },
  {
    "fips": "30017",
    "state": "MT",
    "county": "Custer"
  },
  {
    "fips": "18059",
    "state": "IN",
    "county": "Hancock"
  },
  {
    "fips": "13169",
    "state": "GA",
    "county": "Jones"
  },
  {
    "fips": "09007",
    "state": "CT",
    "county": "Middlesex"
  },
  {
    "fips": "17165",
    "state": "IL",
    "county": "Saline"
  },
  {
    "fips": "05047",
    "state": "AR",
    "county": "Franklin"
  },
  {
    "fips": "05097",
    "state": "AR",
    "county": "Montgomery"
  },
  {
    "fips": "37095",
    "state": "NC",
    "county": "Hyde"
  },
  {
    "fips": "36091",
    "state": "NY",
    "county": "Saratoga"
  },
  {
    "fips": "13037",
    "state": "GA",
    "county": "Calhoun"
  },
  {
    "fips": "48071",
    "state": "TX",
    "county": "Chambers"
  },
  {
    "fips": "35003",
    "state": "NM",
    "county": "Catron"
  },
  {
    "fips": "34027",
    "state": "NJ",
    "county": "Morris"
  },
  {
    "fips": "47077",
    "state": "TN",
    "county": "Henderson"
  },
  {
    "fips": "13149",
    "state": "GA",
    "county": "Heard"
  },
  {
    "fips": "48151",
    "state": "TX",
    "county": "Fisher"
  },
  {
    "fips": "35051",
    "state": "NM",
    "county": "Sierra"
  },
  {
    "fips": "37197",
    "state": "NC",
    "county": "Yadkin"
  },
  {
    "fips": "31145",
    "state": "NE",
    "county": "Red Willow"
  },
  {
    "fips": "31183",
    "state": "NE",
    "county": "Wheeler"
  },
  {
    "fips": "12077",
    "state": "FL",
    "county": "Liberty"
  },
  {
    "fips": "21239",
    "state": "KY",
    "county": "Woodford"
  },
  {
    "fips": "48245",
    "state": "TX",
    "county": "Jefferson"
  },
  {
    "fips": "26127",
    "state": "MI",
    "county": "Oceana"
  },
  {
    "fips": "27115",
    "state": "MN",
    "county": "Pine"
  },
  {
    "fips": "36023",
    "state": "NY",
    "county": "Cortland"
  },
  {
    "fips": "12107",
    "state": "FL",
    "county": "Putnam"
  },
  {
    "fips": "47015",
    "state": "TN",
    "county": "Cannon"
  },
  {
    "fips": "06107",
    "state": "CA",
    "county": "Tulare"
  },
  {
    "fips": "30033",
    "state": "MT",
    "county": "Garfield"
  },
  {
    "fips": "05063",
    "state": "AR",
    "county": "Independence"
  },
  {
    "fips": "17123",
    "state": "IL",
    "county": "Marshall"
  },
  {
    "fips": "20127",
    "state": "KS",
    "county": "Morris"
  },
  {
    "fips": "13065",
    "state": "GA",
    "county": "Clinch"
  },
  {
    "fips": "47105",
    "state": "TN",
    "county": "Loudon"
  },
  {
    "fips": "39115",
    "state": "OH",
    "county": "Morgan"
  },
  {
    "fips": "19145",
    "state": "IA",
    "county": "Page"
  },
  {
    "fips": "48375",
    "state": "TX",
    "county": "Potter"
  },
  {
    "fips": "40059",
    "state": "OK",
    "county": "Harper"
  },
  {
    "fips": "72009",
    "state": "PR",
    "county": "Aibonito"
  },
  {
    "fips": "16077",
    "state": "ID",
    "county": "Power"
  },
  {
    "fips": "20079",
    "state": "KS",
    "county": "Harvey"
  },
  {
    "fips": "47121",
    "state": "TN",
    "county": "Meigs"
  },
  {
    "fips": "31117",
    "state": "NE",
    "county": "McPherson"
  },
  {
    "fips": "45011",
    "state": "SC",
    "county": "Barnwell"
  },
  {
    "fips": "30087",
    "state": "MT",
    "county": "Rosebud"
  },
  {
    "fips": "48199",
    "state": "TX",
    "county": "Hardin"
  },
  {
    "fips": "08089",
    "state": "CO",
    "county": "Otero"
  },
  {
    "fips": "21011",
    "state": "KY",
    "county": "Bath"
  },
  {
    "fips": "34001",
    "state": "NJ",
    "county": "Atlantic"
  },
  {
    "fips": "37123",
    "state": "NC",
    "county": "Montgomery"
  },
  {
    "fips": "13261",
    "state": "GA",
    "county": "Sumter"
  },
  {
    "fips": "31001",
    "state": "NE",
    "county": "Adams"
  },
  {
    "fips": "37049",
    "state": "NC",
    "county": "Craven"
  },
  {
    "fips": "28057",
    "state": "MS",
    "county": "Itawamba"
  },
  {
    "fips": "05107",
    "state": "AR",
    "county": "Phillips"
  },
  {
    "fips": "23015",
    "state": "ME",
    "county": "Lincoln"
  },
  {
    "fips": "39151",
    "state": "OH",
    "county": "Stark"
  },
  {
    "fips": "36123",
    "state": "NY",
    "county": "Yates"
  },
  {
    "fips": "41031",
    "state": "OR",
    "county": "Jefferson"
  },
  {
    "fips": "26105",
    "state": "MI",
    "county": "Mason"
  },
  {
    "fips": "13195",
    "state": "GA",
    "county": "Madison"
  },
  {
    "fips": "74300",
    "state": "UM",
    "county": "Midway Islands"
  },
  {
    "fips": "38073",
    "state": "ND",
    "county": "Ransom"
  },
  {
    "fips": "29003",
    "state": "MO",
    "county": "Andrew"
  },
  {
    "fips": "47041",
    "state": "TN",
    "county": "DeKalb"
  },
  {
    "fips": "29117",
    "state": "MO",
    "county": "Livingston"
  },
  {
    "fips": "13237",
    "state": "GA",
    "county": "Putnam"
  },
  {
    "fips": "29229",
    "state": "MO",
    "county": "Wright"
  },
  {
    "fips": "16063",
    "state": "ID",
    "county": "Lincoln"
  },
  {
    "fips": "37023",
    "state": "NC",
    "county": "Burke"
  },
  {
    "fips": "47087",
    "state": "TN",
    "county": "Jackson"
  },
  {
    "fips": "36101",
    "state": "NY",
    "county": "Steuben"
  },
  {
    "fips": "27125",
    "state": "MN",
    "county": "Red Lake"
  },
  {
    "fips": "17151",
    "state": "IL",
    "county": "Pope"
  },
  {
    "fips": "19163",
    "state": "IA",
    "county": "Scott"
  },
  {
    "fips": "33011",
    "state": "NH",
    "county": "Hillsborough"
  },
  {
    "fips": "36075",
    "state": "NY",
    "county": "Oswego"
  },
  {
    "fips": "31103",
    "state": "NE",
    "county": "Keya Paha"
  },
  {
    "fips": "36021",
    "state": "NY",
    "county": "Columbia"
  },
  {
    "fips": "47029",
    "state": "TN",
    "county": "Cocke"
  },
  {
    "fips": "48045",
    "state": "TX",
    "county": "Briscoe"
  },
  {
    "fips": "01119",
    "state": "AL",
    "county": "Sumter"
  },
  {
    "fips": "24047",
    "state": "MD",
    "county": "Worcester"
  },
  {
    "fips": "28075",
    "state": "MS",
    "county": "Lauderdale"
  },
  {
    "fips": "18063",
    "state": "IN",
    "county": "Hendricks"
  },
  {
    "fips": "51197",
    "state": "VA",
    "county": "Wythe"
  },
  {
    "fips": "13259",
    "state": "GA",
    "county": "Stewart"
  },
  {
    "fips": "16013",
    "state": "ID",
    "county": "Blaine"
  },
  {
    "fips": "36119",
    "state": "NY",
    "county": "Westchester"
  },
  {
    "fips": "16061",
    "state": "ID",
    "county": "Lewis"
  },
  {
    "fips": "48427",
    "state": "TX",
    "county": "Starr"
  },
  {
    "fips": "51570",
    "state": "VA",
    "county": "Colonial Heights"
  },
  {
    "fips": "01051",
    "state": "AL",
    "county": "Elmore"
  },
  {
    "fips": "17107",
    "state": "IL",
    "county": "Logan"
  },
  {
    "fips": "17141",
    "state": "IL",
    "county": "Ogle"
  },
  {
    "fips": "31079",
    "state": "NE",
    "county": "Hall"
  },
  {
    "fips": "22105",
    "state": "LA",
    "county": "Tangipahoa"
  },
  {
    "fips": "32510",
    "state": "NV",
    "county": "Carson City"
  },
  {
    "fips": "40031",
    "state": "OK",
    "county": "Comanche"
  },
  {
    "fips": "48361",
    "state": "TX",
    "county": "Orange"
  },
  {
    "fips": "38059",
    "state": "ND",
    "county": "Morton"
  },
  {
    "fips": "49007",
    "state": "UT",
    "county": "Carbon"
  },
  {
    "fips": "45021",
    "state": "SC",
    "county": "Cherokee"
  },
  {
    "fips": "55055",
    "state": "WI",
    "county": "Jefferson"
  },
  {
    "fips": "21107",
    "state": "KY",
    "county": "Hopkins"
  },
  {
    "fips": "38067",
    "state": "ND",
    "county": "Pembina"
  },
  {
    "fips": "47075",
    "state": "TN",
    "county": "Haywood"
  },
  {
    "fips": "29027",
    "state": "MO",
    "county": "Callaway"
  },
  {
    "fips": "40119",
    "state": "OK",
    "county": "Payne"
  },
  {
    "fips": "51165",
    "state": "VA",
    "county": "Rockingham"
  },
  {
    "fips": "46007",
    "state": "SD",
    "county": "Bennett"
  },
  {
    "fips": "53053",
    "state": "WA",
    "county": "Pierce"
  },
  {
    "fips": "12055",
    "state": "FL",
    "county": "Highlands"
  },
  {
    "fips": "49005",
    "state": "UT",
    "county": "Cache"
  },
  {
    "fips": "21209",
    "state": "KY",
    "county": "Scott"
  },
  {
    "fips": "51021",
    "state": "VA",
    "county": "Bland"
  },
  {
    "fips": "54041",
    "state": "WV",
    "county": "Lewis"
  },
  {
    "fips": "27095",
    "state": "MN",
    "county": "Mille Lacs"
  },
  {
    "fips": "72054",
    "state": "PR",
    "county": "Florida"
  },
  {
    "fips": "22057",
    "state": "LA",
    "county": "Lafourche"
  },
  {
    "fips": "45057",
    "state": "SC",
    "county": "Lancaster"
  },
  {
    "fips": "18159",
    "state": "IN",
    "county": "Tipton"
  },
  {
    "fips": "46075",
    "state": "SD",
    "county": "Jones"
  },
  {
    "fips": "40021",
    "state": "OK",
    "county": "Cherokee"
  },
  {
    "fips": "36109",
    "state": "NY",
    "county": "Tompkins"
  },
  {
    "fips": "39157",
    "state": "OH",
    "county": "Tuscarawas"
  },
  {
    "fips": "53043",
    "state": "WA",
    "county": "Lincoln"
  },
  {
    "fips": "54095",
    "state": "WV",
    "county": "Tyler"
  },
  {
    "fips": "20041",
    "state": "KS",
    "county": "Dickinson"
  },
  {
    "fips": "48309",
    "state": "TX",
    "county": "McLennan"
  },
  {
    "fips": "21125",
    "state": "KY",
    "county": "Laurel"
  },
  {
    "fips": "37017",
    "state": "NC",
    "county": "Bladen"
  },
  {
    "fips": "05031",
    "state": "AR",
    "county": "Craighead"
  },
  {
    "fips": "46009",
    "state": "SD",
    "county": "Bon Homme"
  },
  {
    "fips": "53019",
    "state": "WA",
    "county": "Ferry"
  },
  {
    "fips": "35009",
    "state": "NM",
    "county": "Curry"
  },
  {
    "fips": "12039",
    "state": "FL",
    "county": "Gadsden"
  },
  {
    "fips": "20053",
    "state": "KS",
    "county": "Ellsworth"
  },
  {
    "fips": "48247",
    "state": "TX",
    "county": "Jim Hogg"
  },
  {
    "fips": "22087",
    "state": "LA",
    "county": "St. Bernard"
  },
  {
    "fips": "28087",
    "state": "MS",
    "county": "Lowndes"
  },
  {
    "fips": "53033",
    "state": "WA",
    "county": "King"
  },
  {
    "fips": "17139",
    "state": "IL",
    "county": "Moultrie"
  },
  {
    "fips": "48103",
    "state": "TX",
    "county": "Crane"
  },
  {
    "fips": "19023",
    "state": "IA",
    "county": "Butler"
  },
  {
    "fips": "48369",
    "state": "TX",
    "county": "Parmer"
  },
  {
    "fips": "29147",
    "state": "MO",
    "county": "Nodaway"
  },
  {
    "fips": "40065",
    "state": "OK",
    "county": "Jackson"
  },
  {
    "fips": "20063",
    "state": "KS",
    "county": "Gove"
  },
  {
    "fips": "23003",
    "state": "ME",
    "county": "Aroostook"
  },
  {
    "fips": "28065",
    "state": "MS",
    "county": "Jefferson Davis"
  },
  {
    "fips": "40091",
    "state": "OK",
    "county": "McIntosh"
  },
  {
    "fips": "48399",
    "state": "TX",
    "county": "Runnels"
  },
  {
    "fips": "26125",
    "state": "MI",
    "county": "Oakland"
  },
  {
    "fips": "47143",
    "state": "TN",
    "county": "Rhea"
  },
  {
    "fips": "45049",
    "state": "SC",
    "county": "Hampton"
  },
  {
    "fips": "20019",
    "state": "KS",
    "county": "Chautauqua"
  },
  {
    "fips": "27161",
    "state": "MN",
    "county": "Waseca"
  },
  {
    "fips": "40131",
    "state": "OK",
    "county": "Rogers"
  },
  {
    "fips": "13033",
    "state": "GA",
    "county": "Burke"
  },
  {
    "fips": "16009",
    "state": "ID",
    "county": "Benewah"
  },
  {
    "fips": "29221",
    "state": "MO",
    "county": "Washington"
  },
  {
    "fips": "08079",
    "state": "CO",
    "county": "Mineral"
  },
  {
    "fips": "55129",
    "state": "WI",
    "county": "Washburn"
  },
  {
    "fips": "34025",
    "state": "NJ",
    "county": "Monmouth"
  },
  {
    "fips": "19117",
    "state": "IA",
    "county": "Lucas"
  },
  {
    "fips": "29181",
    "state": "MO",
    "county": "Ripley"
  },
  {
    "fips": "49035",
    "state": "UT",
    "county": "Salt Lake"
  },
  {
    "fips": "31129",
    "state": "NE",
    "county": "Nuckolls"
  },
  {
    "fips": "20045",
    "state": "KS",
    "county": "Douglas"
  },
  {
    "fips": "38085",
    "state": "ND",
    "county": "Sioux"
  },
  {
    "fips": "72043",
    "state": "PR",
    "county": "Coamo"
  },
  {
    "fips": "04011",
    "state": "AZ",
    "county": "Greenlee"
  },
  {
    "fips": "29159",
    "state": "MO",
    "county": "Pettis"
  },
  {
    "fips": "51800",
    "state": "VA",
    "county": "Suffolk"
  },
  {
    "fips": "48189",
    "state": "TX",
    "county": "Hale"
  },
  {
    "fips": "38039",
    "state": "ND",
    "county": "Griggs"
  },
  {
    "fips": "54035",
    "state": "WV",
    "county": "Jackson"
  },
  {
    "fips": "47157",
    "state": "TN",
    "county": "Shelby"
  },
  {
    "fips": "46115",
    "state": "SD",
    "county": "Spink"
  },
  {
    "fips": "48463",
    "state": "TX",
    "county": "Uvalde"
  },
  {
    "fips": "48315",
    "state": "TX",
    "county": "Marion"
  },
  {
    "fips": "18005",
    "state": "IN",
    "county": "Bartholomew"
  },
  {
    "fips": "21217",
    "state": "KY",
    "county": "Taylor"
  },
  {
    "fips": "21099",
    "state": "KY",
    "county": "Hart"
  },
  {
    "fips": "17053",
    "state": "IL",
    "county": "Ford"
  },
  {
    "fips": "01063",
    "state": "AL",
    "county": "Greene"
  },
  {
    "fips": "18095",
    "state": "IN",
    "county": "Madison"
  },
  {
    "fips": "13167",
    "state": "GA",
    "county": "Johnson"
  },
  {
    "fips": "27079",
    "state": "MN",
    "county": "Le Sueur"
  },
  {
    "fips": "37009",
    "state": "NC",
    "county": "Ashe"
  },
  {
    "fips": "29163",
    "state": "MO",
    "county": "Pike"
  },
  {
    "fips": "53029",
    "state": "WA",
    "county": "Island"
  },
  {
    "fips": "05007",
    "state": "AR",
    "county": "Benton"
  },
  {
    "fips": "28083",
    "state": "MS",
    "county": "Leflore"
  },
  {
    "fips": "33009",
    "state": "NH",
    "county": "Grafton"
  },
  {
    "fips": "41039",
    "state": "OR",
    "county": "Lane"
  },
  {
    "fips": "20077",
    "state": "KS",
    "county": "Harper"
  },
  {
    "fips": "13019",
    "state": "GA",
    "county": "Berrien"
  },
  {
    "fips": "48063",
    "state": "TX",
    "county": "Camp"
  },
  {
    "fips": "30055",
    "state": "MT",
    "county": "McCone"
  },
  {
    "fips": "51025",
    "state": "VA",
    "county": "Brunswick"
  },
  {
    "fips": "38069",
    "state": "ND",
    "county": "Pierce"
  },
  {
    "fips": "48319",
    "state": "TX",
    "county": "Mason"
  },
  {
    "fips": "20133",
    "state": "KS",
    "county": "Neosho"
  },
  {
    "fips": "40055",
    "state": "OK",
    "county": "Greer"
  },
  {
    "fips": "48187",
    "state": "TX",
    "county": "Guadalupe"
  },
  {
    "fips": "21235",
    "state": "KY",
    "county": "Whitley"
  },
  {
    "fips": "40039",
    "state": "OK",
    "county": "Custer"
  },
  {
    "fips": "51083",
    "state": "VA",
    "county": "Halifax"
  },
  {
    "fips": "19001",
    "state": "IA",
    "county": "Adair"
  },
  {
    "fips": "02180",
    "state": "AK",
    "county": "Nome"
  },
  {
    "fips": "18065",
    "state": "IN",
    "county": "Henry"
  },
  {
    "fips": "19071",
    "state": "IA",
    "county": "Fremont"
  },
  {
    "fips": "48109",
    "state": "TX",
    "county": "Culberson"
  },
  {
    "fips": "26093",
    "state": "MI",
    "county": "Livingston"
  },
  {
    "fips": "48423",
    "state": "TX",
    "county": "Smith"
  },
  {
    "fips": "37057",
    "state": "NC",
    "county": "Davidson"
  },
  {
    "fips": "01109",
    "state": "AL",
    "county": "Pike"
  },
  {
    "fips": "55083",
    "state": "WI",
    "county": "Oconto"
  },
  {
    "fips": "55131",
    "state": "WI",
    "county": "Washington"
  },
  {
    "fips": "42083",
    "state": "PA",
    "county": "McKean"
  },
  {
    "fips": "45055",
    "state": "SC",
    "county": "Kershaw"
  },
  {
    "fips": "30079",
    "state": "MT",
    "county": "Prairie"
  },
  {
    "fips": "37071",
    "state": "NC",
    "county": "Gaston"
  },
  {
    "fips": "38105",
    "state": "ND",
    "county": "Williams"
  },
  {
    "fips": "40145",
    "state": "OK",
    "county": "Wagoner"
  },
  {
    "fips": "30099",
    "state": "MT",
    "county": "Teton"
  },
  {
    "fips": "48269",
    "state": "TX",
    "county": "King"
  },
  {
    "fips": "27075",
    "state": "MN",
    "county": "Lake"
  },
  {
    "fips": "31127",
    "state": "NE",
    "county": "Nemaha"
  },
  {
    "fips": "06039",
    "state": "CA",
    "county": "Madera"
  },
  {
    "fips": "41049",
    "state": "OR",
    "county": "Morrow"
  },
  {
    "fips": "48099",
    "state": "TX",
    "county": "Coryell"
  },
  {
    "fips": "37109",
    "state": "NC",
    "county": "Lincoln"
  },
  {
    "fips": "27163",
    "state": "MN",
    "county": "Washington"
  },
  {
    "fips": "47185",
    "state": "TN",
    "county": "White"
  },
  {
    "fips": "20023",
    "state": "KS",
    "county": "Cheyenne"
  },
  {
    "fips": "39169",
    "state": "OH",
    "county": "Wayne"
  },
  {
    "fips": "20065",
    "state": "KS",
    "county": "Graham"
  },
  {
    "fips": "26079",
    "state": "MI",
    "county": "Kalkaska"
  },
  {
    "fips": "42005",
    "state": "PA",
    "county": "Armstrong"
  },
  {
    "fips": "51683",
    "state": "VA",
    "county": "Manassas"
  },
  {
    "fips": "19187",
    "state": "IA",
    "county": "Webster"
  },
  {
    "fips": "39089",
    "state": "OH",
    "county": "Licking"
  },
  {
    "fips": "04003",
    "state": "AZ",
    "county": "Cochise"
  },
  {
    "fips": "47167",
    "state": "TN",
    "county": "Tipton"
  },
  {
    "fips": "42051",
    "state": "PA",
    "county": "Fayette"
  },
  {
    "fips": "27005",
    "state": "MN",
    "county": "Becker"
  },
  {
    "fips": "55013",
    "state": "WI",
    "county": "Burnett"
  },
  {
    "fips": "13067",
    "state": "GA",
    "county": "Cobb"
  },
  {
    "fips": "13143",
    "state": "GA",
    "county": "Haralson"
  },
  {
    "fips": "46047",
    "state": "SD",
    "county": "Fall River"
  },
  {
    "fips": "29007",
    "state": "MO",
    "county": "Audrain"
  },
  {
    "fips": "25007",
    "state": "MA",
    "county": "Dukes"
  },
  {
    "fips": "18091",
    "state": "IN",
    "county": "La Porte"
  },
  {
    "fips": "51107",
    "state": "VA",
    "county": "Loudoun"
  },
  {
    "fips": "53063",
    "state": "WA",
    "county": "Spokane"
  },
  {
    "fips": "45025",
    "state": "SC",
    "county": "Chesterfield"
  },
  {
    "fips": "18037",
    "state": "IN",
    "county": "Dubois"
  },
  {
    "fips": "21231",
    "state": "KY",
    "county": "Wayne"
  },
  {
    "fips": "22047",
    "state": "LA",
    "county": "Iberville"
  },
  {
    "fips": "38021",
    "state": "ND",
    "county": "Dickey"
  },
  {
    "fips": "39031",
    "state": "OH",
    "county": "Coshocton"
  },
  {
    "fips": "53027",
    "state": "WA",
    "county": "Grays Harbor"
  },
  {
    "fips": "22107",
    "state": "LA",
    "county": "Tensas"
  },
  {
    "fips": "46121",
    "state": "SD",
    "county": "Todd"
  },
  {
    "fips": "22093",
    "state": "LA",
    "county": "St. James"
  },
  {
    "fips": "22083",
    "state": "LA",
    "county": "Richland"
  },
  {
    "fips": "05071",
    "state": "AR",
    "county": "Johnson"
  },
  {
    "fips": "21219",
    "state": "KY",
    "county": "Todd"
  },
  {
    "fips": "54057",
    "state": "WV",
    "county": "Mineral"
  },
  {
    "fips": "08069",
    "state": "CO",
    "county": "Larimer"
  },
  {
    "fips": "39093",
    "state": "OH",
    "county": "Lorain"
  },
  {
    "fips": "51005",
    "state": "VA",
    "county": "Alleghany"
  },
  {
    "fips": "53069",
    "state": "WA",
    "county": "Wahkiakum"
  },
  {
    "fips": "19017",
    "state": "IA",
    "county": "Bremer"
  },
  {
    "fips": "45037",
    "state": "SC",
    "county": "Edgefield"
  },
  {
    "fips": "26161",
    "state": "MI",
    "county": "Washtenaw"
  },
  {
    "fips": "49037",
    "state": "UT",
    "county": "San Juan"
  },
  {
    "fips": "16037",
    "state": "ID",
    "county": "Custer"
  },
  {
    "fips": "06083",
    "state": "CA",
    "county": "Santa Barbara"
  },
  {
    "fips": "16059",
    "state": "ID",
    "county": "Lemhi"
  },
  {
    "fips": "56011",
    "state": "WY",
    "county": "Crook"
  },
  {
    "fips": "17203",
    "state": "IL",
    "county": "Woodford"
  },
  {
    "fips": "45007",
    "state": "SC",
    "county": "Anderson"
  },
  {
    "fips": "56013",
    "state": "WY",
    "county": "Fremont"
  },
  {
    "fips": "40033",
    "state": "OK",
    "county": "Cotton"
  },
  {
    "fips": "37141",
    "state": "NC",
    "county": "Pender"
  },
  {
    "fips": "22085",
    "state": "LA",
    "county": "Sabine"
  },
  {
    "fips": "13251",
    "state": "GA",
    "county": "Screven"
  },
  {
    "fips": "72151",
    "state": "PR",
    "county": "Yabucoa"
  },
  {
    "fips": "04001",
    "state": "AZ",
    "county": "Apache"
  },
  {
    "fips": "17025",
    "state": "IL",
    "county": "Clay"
  },
  {
    "fips": "51109",
    "state": "VA",
    "county": "Louisa"
  },
  {
    "fips": "20057",
    "state": "KS",
    "county": "Ford"
  },
  {
    "fips": "48025",
    "state": "TX",
    "county": "Bee"
  },
  {
    "fips": "46027",
    "state": "SD",
    "county": "Clay"
  },
  {
    "fips": "21115",
    "state": "KY",
    "county": "Johnson"
  },
  {
    "fips": "40105",
    "state": "OK",
    "county": "Nowata"
  },
  {
    "fips": "29039",
    "state": "MO",
    "county": "Cedar"
  },
  {
    "fips": "31089",
    "state": "NE",
    "county": "Holt"
  },
  {
    "fips": "72001",
    "state": "PR",
    "county": "Adjuntas"
  },
  {
    "fips": "18103",
    "state": "IN",
    "county": "Miami"
  },
  {
    "fips": "15007",
    "state": "HI",
    "county": "Kauai"
  },
  {
    "fips": "16039",
    "state": "ID",
    "county": "Elmore"
  },
  {
    "fips": "51031",
    "state": "VA",
    "county": "Campbell"
  },
  {
    "fips": "48053",
    "state": "TX",
    "county": "Burnet"
  },
  {
    "fips": "28161",
    "state": "MS",
    "county": "Yalobusha"
  },
  {
    "fips": "28063",
    "state": "MS",
    "county": "Jefferson"
  },
  {
    "fips": "45079",
    "state": "SC",
    "county": "Richland"
  },
  {
    "fips": "20175",
    "state": "KS",
    "county": "Seward"
  },
  {
    "fips": "05099",
    "state": "AR",
    "county": "Nevada"
  },
  {
    "fips": "13165",
    "state": "GA",
    "county": "Jenkins"
  },
  {
    "fips": "30067",
    "state": "MT",
    "county": "Park"
  },
  {
    "fips": "29001",
    "state": "MO",
    "county": "Adair"
  },
  {
    "fips": "31055",
    "state": "NE",
    "county": "Douglas"
  },
  {
    "fips": "48471",
    "state": "TX",
    "county": "Walker"
  },
  {
    "fips": "51690",
    "state": "VA",
    "county": "Martinsville"
  },
  {
    "fips": "40005",
    "state": "OK",
    "county": "Atoka"
  },
  {
    "fips": "35013",
    "state": "NM",
    "county": "Dona Ana"
  },
  {
    "fips": "24003",
    "state": "MD",
    "county": "Anne Arundel"
  },
  {
    "fips": "29510",
    "state": "MO",
    "county": "St. Louis"
  },
  {
    "fips": "19003",
    "state": "IA",
    "county": "Adams"
  },
  {
    "fips": "27073",
    "state": "MN",
    "county": "Lac qui Parle"
  },
  {
    "fips": "47037",
    "state": "TN",
    "county": "Davidson"
  },
  {
    "fips": "51017",
    "state": "VA",
    "county": "Bath"
  },
  {
    "fips": "19179",
    "state": "IA",
    "county": "Wapello"
  },
  {
    "fips": "04023",
    "state": "AZ",
    "county": "Santa Cruz"
  },
  {
    "fips": "02060",
    "state": "AK",
    "county": "Bristol Bay"
  },
  {
    "fips": "12079",
    "state": "FL",
    "county": "Madison"
  },
  {
    "fips": "48445",
    "state": "TX",
    "county": "Terry"
  },
  {
    "fips": "17149",
    "state": "IL",
    "county": "Pike"
  },
  {
    "fips": "34003",
    "state": "NJ",
    "county": "Bergen"
  },
  {
    "fips": "36117",
    "state": "NY",
    "county": "Wayne"
  },
  {
    "fips": "39029",
    "state": "OH",
    "county": "Columbiana"
  },
  {
    "fips": "48047",
    "state": "TX",
    "county": "Brooks"
  },
  {
    "fips": "51059",
    "state": "VA",
    "county": "Fairfax"
  },
  {
    "fips": "28109",
    "state": "MS",
    "county": "Pearl River"
  },
  {
    "fips": "46013",
    "state": "SD",
    "county": "Brown"
  },
  {
    "fips": "31123",
    "state": "NE",
    "county": "Morrill"
  },
  {
    "fips": "01065",
    "state": "AL",
    "county": "Hale"
  },
  {
    "fips": "31053",
    "state": "NE",
    "county": "Dodge"
  },
  {
    "fips": "48425",
    "state": "TX",
    "county": "Somervell"
  },
  {
    "fips": "34041",
    "state": "NJ",
    "county": "Warren"
  },
  {
    "fips": "01077",
    "state": "AL",
    "county": "Lauderdale"
  },
  {
    "fips": "38043",
    "state": "ND",
    "county": "Kidder"
  },
  {
    "fips": "29129",
    "state": "MO",
    "county": "Mercer"
  },
  {
    "fips": "51830",
    "state": "VA",
    "county": "Williamsburg"
  },
  {
    "fips": "17069",
    "state": "IL",
    "county": "Hardin"
  },
  {
    "fips": "51770",
    "state": "VA",
    "county": "Roanoke"
  },
  {
    "fips": "42095",
    "state": "PA",
    "county": "Northampton"
  },
  {
    "fips": "13023",
    "state": "GA",
    "county": "Bleckley"
  },
  {
    "fips": "27031",
    "state": "MN",
    "county": "Cook"
  },
  {
    "fips": "27023",
    "state": "MN",
    "county": "Chippewa"
  },
  {
    "fips": "72127",
    "state": "PR",
    "county": "San Juan"
  },
  {
    "fips": "26015",
    "state": "MI",
    "county": "Barry"
  },
  {
    "fips": "40017",
    "state": "OK",
    "county": "Canadian"
  },
  {
    "fips": "37163",
    "state": "NC",
    "county": "Sampson"
  },
  {
    "fips": "13241",
    "state": "GA",
    "county": "Rabun"
  },
  {
    "fips": "13225",
    "state": "GA",
    "county": "Peach"
  },
  {
    "fips": "47093",
    "state": "TN",
    "county": "Knox"
  },
  {
    "fips": "72035",
    "state": "PR",
    "county": "Cayey"
  },
  {
    "fips": "21193",
    "state": "KY",
    "county": "Perry"
  },
  {
    "fips": "72129",
    "state": "PR",
    "county": "San Lorenzo"
  },
  {
    "fips": "53005",
    "state": "WA",
    "county": "Benton"
  },
  {
    "fips": "13015",
    "state": "GA",
    "county": "Bartow"
  },
  {
    "fips": "30027",
    "state": "MT",
    "county": "Fergus"
  },
  {
    "fips": "41057",
    "state": "OR",
    "county": "Tillamook"
  },
  {
    "fips": "56001",
    "state": "WY",
    "county": "Albany"
  },
  {
    "fips": "42013",
    "state": "PA",
    "county": "Blair"
  },
  {
    "fips": "06049",
    "state": "CA",
    "county": "Modoc"
  },
  {
    "fips": "39111",
    "state": "OH",
    "county": "Monroe"
  },
  {
    "fips": "39061",
    "state": "OH",
    "county": "Hamilton"
  },
  {
    "fips": "56029",
    "state": "WY",
    "county": "Park"
  },
  {
    "fips": "45017",
    "state": "SC",
    "county": "Calhoun"
  },
  {
    "fips": "41013",
    "state": "OR",
    "county": "Crook"
  },
  {
    "fips": "19047",
    "state": "IA",
    "county": "Crawford"
  },
  {
    "fips": "45059",
    "state": "SC",
    "county": "Laurens"
  },
  {
    "fips": "18087",
    "state": "IN",
    "county": "Lagrange"
  },
  {
    "fips": "27159",
    "state": "MN",
    "county": "Wadena"
  },
  {
    "fips": "38091",
    "state": "ND",
    "county": "Steele"
  },
  {
    "fips": "21133",
    "state": "KY",
    "county": "Letcher"
  },
  {
    "fips": "24041",
    "state": "MD",
    "county": "Talbot"
  },
  {
    "fips": "27049",
    "state": "MN",
    "county": "Goodhue"
  },
  {
    "fips": "17137",
    "state": "IL",
    "county": "Morgan"
  },
  {
    "fips": "39155",
    "state": "OH",
    "county": "Trumbull"
  },
  {
    "fips": "42121",
    "state": "PA",
    "county": "Venango"
  },
  {
    "fips": "18071",
    "state": "IN",
    "county": "Jackson"
  },
  {
    "fips": "31115",
    "state": "NE",
    "county": "Loup"
  },
  {
    "fips": "48233",
    "state": "TX",
    "county": "Hutchinson"
  },
  {
    "fips": "17143",
    "state": "IL",
    "county": "Peoria"
  },
  {
    "fips": "27139",
    "state": "MN",
    "county": "Scott"
  },
  {
    "fips": "08051",
    "state": "CO",
    "county": "Gunnison"
  },
  {
    "fips": "36007",
    "state": "NY",
    "county": "Broome"
  },
  {
    "fips": "38051",
    "state": "ND",
    "county": "McIntosh"
  },
  {
    "fips": "72107",
    "state": "PR",
    "county": "Orocovis"
  },
  {
    "fips": "18155",
    "state": "IN",
    "county": "Switzerland"
  },
  {
    "fips": "13287",
    "state": "GA",
    "county": "Turner"
  },
  {
    "fips": "48009",
    "state": "TX",
    "county": "Archer"
  },
  {
    "fips": "54087",
    "state": "WV",
    "county": "Roane"
  },
  {
    "fips": "37111",
    "state": "NC",
    "county": "McDowell"
  },
  {
    "fips": "56009",
    "state": "WY",
    "county": "Converse"
  },
  {
    "fips": "37075",
    "state": "NC",
    "county": "Graham"
  },
  {
    "fips": "48401",
    "state": "TX",
    "county": "Rusk"
  },
  {
    "fips": "51073",
    "state": "VA",
    "county": "Gloucester"
  },
  {
    "fips": "04015",
    "state": "AZ",
    "county": "Mohave"
  },
  {
    "fips": "22005",
    "state": "LA",
    "county": "Ascension"
  },
  {
    "fips": "37011",
    "state": "NC",
    "county": "Avery"
  },
  {
    "fips": "48289",
    "state": "TX",
    "county": "Leon"
  },
  {
    "fips": "22023",
    "state": "LA",
    "county": "Cameron"
  },
  {
    "fips": "54107",
    "state": "WV",
    "county": "Wood"
  },
  {
    "fips": "60040",
    "state": "AS",
    "county": "Swains Island"
  },
  {
    "fips": "26075",
    "state": "MI",
    "county": "Jackson"
  },
  {
    "fips": "37073",
    "state": "NC",
    "county": "Gates"
  },
  {
    "fips": "47127",
    "state": "TN",
    "county": "Moore"
  },
  {
    "fips": "55051",
    "state": "WI",
    "county": "Iron"
  },
  {
    "fips": "17029",
    "state": "IL",
    "county": "Coles"
  },
  {
    "fips": "24039",
    "state": "MD",
    "county": "Somerset"
  },
  {
    "fips": "36035",
    "state": "NY",
    "county": "Fulton"
  },
  {
    "fips": "51063",
    "state": "VA",
    "county": "Floyd"
  },
  {
    "fips": "13141",
    "state": "GA",
    "county": "Hancock"
  },
  {
    "fips": "48341",
    "state": "TX",
    "county": "Moore"
  },
  {
    "fips": "19115",
    "state": "IA",
    "county": "Louisa"
  },
  {
    "fips": "28033",
    "state": "MS",
    "county": "DeSoto"
  },
  {
    "fips": "29175",
    "state": "MO",
    "county": "Randolph"
  },
  {
    "fips": "21233",
    "state": "KY",
    "county": "Webster"
  },
  {
    "fips": "05019",
    "state": "AR",
    "county": "Clark"
  },
  {
    "fips": "31173",
    "state": "NE",
    "county": "Thurston"
  },
  {
    "fips": "38053",
    "state": "ND",
    "county": "McKenzie"
  },
  {
    "fips": "37105",
    "state": "NC",
    "county": "Lee"
  },
  {
    "fips": "41051",
    "state": "OR",
    "county": "Multnomah"
  },
  {
    "fips": "17157",
    "state": "IL",
    "county": "Randolph"
  },
  {
    "fips": "08119",
    "state": "CO",
    "county": "Teller"
  },
  {
    "fips": "05041",
    "state": "AR",
    "county": "Desha"
  },
  {
    "fips": "30045",
    "state": "MT",
    "county": "Judith Basin"
  },
  {
    "fips": "31095",
    "state": "NE",
    "county": "Jefferson"
  },
  {
    "fips": "17119",
    "state": "IL",
    "county": "Madison"
  },
  {
    "fips": "47189",
    "state": "TN",
    "county": "Wilson"
  },
  {
    "fips": "54063",
    "state": "WV",
    "county": "Monroe"
  },
  {
    "fips": "48131",
    "state": "TX",
    "county": "Duval"
  },
  {
    "fips": "28039",
    "state": "MS",
    "county": "George"
  },
  {
    "fips": "39045",
    "state": "OH",
    "county": "Fairfield"
  },
  {
    "fips": "45027",
    "state": "SC",
    "county": "Clarendon"
  },
  {
    "fips": "51175",
    "state": "VA",
    "county": "Southampton"
  },
  {
    "fips": "06047",
    "state": "CA",
    "county": "Merced"
  },
  {
    "fips": "19055",
    "state": "IA",
    "county": "Delaware"
  },
  {
    "fips": "20115",
    "state": "KS",
    "county": "Marion"
  },
  {
    "fips": "48411",
    "state": "TX",
    "county": "San Saba"
  },
  {
    "fips": "20187",
    "state": "KS",
    "county": "Stanton"
  },
  {
    "fips": "18039",
    "state": "IN",
    "county": "Elkhart"
  },
  {
    "fips": "02090",
    "state": "AK",
    "county": "Fairbanks North Star"
  },
  {
    "fips": "29023",
    "state": "MO",
    "county": "Butler"
  },
  {
    "fips": "45005",
    "state": "SC",
    "county": "Allendale"
  },
  {
    "fips": "51600",
    "state": "VA",
    "county": "Fairfax"
  },
  {
    "fips": "04005",
    "state": "AZ",
    "county": "Coconino"
  },
  {
    "fips": "36011",
    "state": "NY",
    "county": "Cayuga"
  },
  {
    "fips": "48365",
    "state": "TX",
    "county": "Panola"
  },
  {
    "fips": "72019",
    "state": "PR",
    "county": "Barranquitas"
  },
  {
    "fips": "20171",
    "state": "KS",
    "county": "Scott"
  },
  {
    "fips": "06081",
    "state": "CA",
    "county": "San Mateo"
  },
  {
    "fips": "18099",
    "state": "IN",
    "county": "Marshall"
  },
  {
    "fips": "25027",
    "state": "MA",
    "county": "Worcester"
  },
  {
    "fips": "40061",
    "state": "OK",
    "county": "Haskell"
  },
  {
    "fips": "29135",
    "state": "MO",
    "county": "Moniteau"
  },
  {
    "fips": "48393",
    "state": "TX",
    "county": "Roberts"
  },
  {
    "fips": "26109",
    "state": "MI",
    "county": "Menominee"
  },
  {
    "fips": "16051",
    "state": "ID",
    "county": "Jefferson"
  },
  {
    "fips": "27157",
    "state": "MN",
    "county": "Wabasha"
  },
  {
    "fips": "20099",
    "state": "KS",
    "county": "Labette"
  },
  {
    "fips": "17015",
    "state": "IL",
    "county": "Carroll"
  },
  {
    "fips": "22055",
    "state": "LA",
    "county": "Lafayette"
  },
  {
    "fips": "27131",
    "state": "MN",
    "county": "Rice"
  },
  {
    "fips": "48391",
    "state": "TX",
    "county": "Refugio"
  },
  {
    "fips": "18179",
    "state": "IN",
    "county": "Wells"
  },
  {
    "fips": "48035",
    "state": "TX",
    "county": "Bosque"
  },
  {
    "fips": "39013",
    "state": "OH",
    "county": "Belmont"
  },
  {
    "fips": "42043",
    "state": "PA",
    "county": "Dauphin"
  },
  {
    "fips": "06043",
    "state": "CA",
    "county": "Mariposa"
  },
  {
    "fips": "21187",
    "state": "KY",
    "county": "Owen"
  },
  {
    "fips": "51187",
    "state": "VA",
    "county": "Warren"
  },
  {
    "fips": "06085",
    "state": "CA",
    "county": "Santa Clara"
  },
  {
    "fips": "20153",
    "state": "KS",
    "county": "Rawlins"
  },
  {
    "fips": "20083",
    "state": "KS",
    "county": "Hodgeman"
  },
  {
    "fips": "55021",
    "state": "WI",
    "county": "Columbia"
  },
  {
    "fips": "48027",
    "state": "TX",
    "county": "Bell"
  },
  {
    "fips": "48115",
    "state": "TX",
    "county": "Dawson"
  },
  {
    "fips": "19049",
    "state": "IA",
    "county": "Dallas"
  },
  {
    "fips": "27105",
    "state": "MN",
    "county": "Nobles"
  },
  {
    "fips": "39077",
    "state": "OH",
    "county": "Huron"
  },
  {
    "fips": "51047",
    "state": "VA",
    "county": "Culpeper"
  },
  {
    "fips": "51159",
    "state": "VA",
    "county": "Richmond"
  },
  {
    "fips": "22059",
    "state": "LA",
    "county": "La Salle"
  },
  {
    "fips": "48149",
    "state": "TX",
    "county": "Fayette"
  },
  {
    "fips": "54109",
    "state": "WV",
    "county": "Wyoming"
  },
  {
    "fips": "55103",
    "state": "WI",
    "county": "Richland"
  },
  {
    "fips": "28085",
    "state": "MS",
    "county": "Lincoln"
  },
  {
    "fips": "54029",
    "state": "WV",
    "county": "Hancock"
  },
  {
    "fips": "27155",
    "state": "MN",
    "county": "Traverse"
  },
  {
    "fips": "48181",
    "state": "TX",
    "county": "Grayson"
  },
  {
    "fips": "38101",
    "state": "ND",
    "county": "Ward"
  },
  {
    "fips": "37089",
    "state": "NC",
    "county": "Henderson"
  },
  {
    "fips": "72057",
    "state": "PR",
    "county": "Guayama"
  },
  {
    "fips": "72071",
    "state": "PR",
    "county": "Isabela"
  },
  {
    "fips": "12131",
    "state": "FL",
    "county": "Walton"
  },
  {
    "fips": "22077",
    "state": "LA",
    "county": "Pointe Coupee"
  },
  {
    "fips": "48451",
    "state": "TX",
    "county": "Tom Green"
  },
  {
    "fips": "51700",
    "state": "VA",
    "county": "Newport News"
  },
  {
    "fips": "17083",
    "state": "IL",
    "county": "Jersey"
  },
  {
    "fips": "08043",
    "state": "CO",
    "county": "Fremont"
  },
  {
    "fips": "08047",
    "state": "CO",
    "county": "Gilpin"
  },
  {
    "fips": "19039",
    "state": "IA",
    "county": "Clarke"
  },
  {
    "fips": "33019",
    "state": "NH",
    "county": "Sullivan"
  },
  {
    "fips": "48119",
    "state": "TX",
    "county": "Delta"
  },
  {
    "fips": "48049",
    "state": "TX",
    "county": "Brown"
  },
  {
    "fips": "55061",
    "state": "WI",
    "county": "Kewaunee"
  },
  {
    "fips": "18025",
    "state": "IN",
    "county": "Crawford"
  },
  {
    "fips": "22117",
    "state": "LA",
    "county": "Washington"
  },
  {
    "fips": "29005",
    "state": "MO",
    "county": "Atchison"
  },
  {
    "fips": "37161",
    "state": "NC",
    "county": "Rutherford"
  },
  {
    "fips": "51015",
    "state": "VA",
    "county": "Augusta"
  },
  {
    "fips": "21043",
    "state": "KY",
    "county": "Carter"
  },
  {
    "fips": "36069",
    "state": "NY",
    "county": "Ontario"
  },
  {
    "fips": "46129",
    "state": "SD",
    "county": "Walworth"
  },
  {
    "fips": "17073",
    "state": "IL",
    "county": "Henry"
  },
  {
    "fips": "46137",
    "state": "SD",
    "county": "Ziebach"
  },
  {
    "fips": "23017",
    "state": "ME",
    "county": "Oxford"
  },
  {
    "fips": "08111",
    "state": "CO",
    "county": "San Juan"
  },
  {
    "fips": "47035",
    "state": "TN",
    "county": "Cumberland"
  },
  {
    "fips": "72067",
    "state": "PR",
    "county": "Hormigueros"
  },
  {
    "fips": "48433",
    "state": "TX",
    "county": "Stonewall"
  },
  {
    "fips": "19123",
    "state": "IA",
    "county": "Mahaska"
  },
  {
    "fips": "05021",
    "state": "AR",
    "county": "Clay"
  },
  {
    "fips": "27087",
    "state": "MN",
    "county": "Mahnomen"
  },
  {
    "fips": "26049",
    "state": "MI",
    "county": "Genesee"
  },
  {
    "fips": "38093",
    "state": "ND",
    "county": "Stutsman"
  },
  {
    "fips": "19063",
    "state": "IA",
    "county": "Emmet"
  },
  {
    "fips": "42039",
    "state": "PA",
    "county": "Crawford"
  },
  {
    "fips": "48237",
    "state": "TX",
    "county": "Jack"
  },
  {
    "fips": "49023",
    "state": "UT",
    "county": "Juab"
  },
  {
    "fips": "08061",
    "state": "CO",
    "county": "Kiowa"
  },
  {
    "fips": "08097",
    "state": "CO",
    "county": "Pitkin"
  },
  {
    "fips": "47131",
    "state": "TN",
    "county": "Obion"
  },
  {
    "fips": "47063",
    "state": "TN",
    "county": "Hamblen"
  },
  {
    "fips": "50005",
    "state": "VT",
    "county": "Caledonia"
  },
  {
    "fips": "55141",
    "state": "WI",
    "county": "Wood"
  },
  {
    "fips": "24029",
    "state": "MD",
    "county": "Kent"
  },
  {
    "fips": "05109",
    "state": "AR",
    "county": "Pike"
  },
  {
    "fips": "48153",
    "state": "TX",
    "county": "Floyd"
  },
  {
    "fips": "08027",
    "state": "CO",
    "county": "Custer"
  },
  {
    "fips": "25025",
    "state": "MA",
    "county": "Suffolk"
  },
  {
    "fips": "28103",
    "state": "MS",
    "county": "Noxubee"
  },
  {
    "fips": "44001",
    "state": "RI",
    "county": "Bristol"
  },
  {
    "fips": "56019",
    "state": "WY",
    "county": "Johnson"
  },
  {
    "fips": "34037",
    "state": "NJ",
    "county": "Sussex"
  },
  {
    "fips": "29071",
    "state": "MO",
    "county": "Franklin"
  },
  {
    "fips": "39121",
    "state": "OH",
    "county": "Noble"
  },
  {
    "fips": "40111",
    "state": "OK",
    "county": "Okmulgee"
  },
  {
    "fips": "55093",
    "state": "WI",
    "county": "Pierce"
  },
  {
    "fips": "48485",
    "state": "TX",
    "county": "Wichita"
  },
  {
    "fips": "15001",
    "state": "HI",
    "county": "Hawaii"
  },
  {
    "fips": "26023",
    "state": "MI",
    "county": "Branch"
  },
  {
    "fips": "47161",
    "state": "TN",
    "county": "Stewart"
  },
  {
    "fips": "48281",
    "state": "TX",
    "county": "Lampasas"
  },
  {
    "fips": "01041",
    "state": "AL",
    "county": "Crenshaw"
  },
  {
    "fips": "08041",
    "state": "CO",
    "county": "El Paso"
  },
  {
    "fips": "19015",
    "state": "IA",
    "county": "Boone"
  },
  {
    "fips": "46087",
    "state": "SD",
    "county": "McCook"
  },
  {
    "fips": "48037",
    "state": "TX",
    "county": "Bowie"
  },
  {
    "fips": "48371",
    "state": "TX",
    "county": "Pecos"
  },
  {
    "fips": "08063",
    "state": "CO",
    "county": "Kit Carson"
  },
  {
    "fips": "30091",
    "state": "MT",
    "county": "Sheridan"
  },
  {
    "fips": "55063",
    "state": "WI",
    "county": "La Crosse"
  },
  {
    "fips": "30053",
    "state": "MT",
    "county": "Lincoln"
  },
  {
    "fips": "22001",
    "state": "LA",
    "county": "Acadia"
  },
  {
    "fips": "48107",
    "state": "TX",
    "county": "Crosby"
  },
  {
    "fips": "06007",
    "state": "CA",
    "county": "Butte"
  },
  {
    "fips": "46019",
    "state": "SD",
    "county": "Butte"
  },
  {
    "fips": "19167",
    "state": "IA",
    "county": "Sioux"
  },
  {
    "fips": "08029",
    "state": "CO",
    "county": "Delta"
  },
  {
    "fips": "29207",
    "state": "MO",
    "county": "Stoddard"
  },
  {
    "fips": "37035",
    "state": "NC",
    "county": "Catawba"
  },
  {
    "fips": "20003",
    "state": "KS",
    "county": "Anderson"
  },
  {
    "fips": "42111",
    "state": "PA",
    "county": "Somerset"
  },
  {
    "fips": "28001",
    "state": "MS",
    "county": "Adams"
  },
  {
    "fips": "12095",
    "state": "FL",
    "county": "Orange"
  },
  {
    "fips": "17185",
    "state": "IL",
    "county": "Wabash"
  },
  {
    "fips": "27053",
    "state": "MN",
    "county": "Hennepin"
  },
  {
    "fips": "19111",
    "state": "IA",
    "county": "Lee"
  },
  {
    "fips": "20199",
    "state": "KS",
    "county": "Wallace"
  },
  {
    "fips": "22061",
    "state": "LA",
    "county": "Lincoln"
  },
  {
    "fips": "72039",
    "state": "PR",
    "county": "Ciales"
  },
  {
    "fips": "45051",
    "state": "SC",
    "county": "Horry"
  },
  {
    "fips": "48355",
    "state": "TX",
    "county": "Nueces"
  },
  {
    "fips": "37159",
    "state": "NC",
    "county": "Rowan"
  },
  {
    "fips": "18045",
    "state": "IN",
    "county": "Fountain"
  },
  {
    "fips": "18001",
    "state": "IN",
    "county": "Adams"
  },
  {
    "fips": "56017",
    "state": "WY",
    "county": "Hot Springs"
  },
  {
    "fips": "33015",
    "state": "NH",
    "county": "Rockingham"
  },
  {
    "fips": "48453",
    "state": "TX",
    "county": "Travis"
  },
  {
    "fips": "48499",
    "state": "TX",
    "county": "Wood"
  },
  {
    "fips": "01093",
    "state": "AL",
    "county": "Marion"
  },
  {
    "fips": "39139",
    "state": "OH",
    "county": "Richland"
  },
  {
    "fips": "48105",
    "state": "TX",
    "county": "Crockett"
  },
  {
    "fips": "40063",
    "state": "OK",
    "county": "Hughes"
  },
  {
    "fips": "18113",
    "state": "IN",
    "county": "Noble"
  },
  {
    "fips": "40137",
    "state": "OK",
    "county": "Stephens"
  },
  {
    "fips": "13291",
    "state": "GA",
    "county": "Union"
  },
  {
    "fips": "22043",
    "state": "LA",
    "county": "Grant"
  },
  {
    "fips": "36053",
    "state": "NY",
    "county": "Madison"
  },
  {
    "fips": "41055",
    "state": "OR",
    "county": "Sherman"
  },
  {
    "fips": "21153",
    "state": "KY",
    "county": "Magoffin"
  },
  {
    "fips": "42097",
    "state": "PA",
    "county": "Northumberland"
  },
  {
    "fips": "53003",
    "state": "WA",
    "county": "Asotin"
  },
  {
    "fips": "40035",
    "state": "OK",
    "county": "Craig"
  },
  {
    "fips": "37151",
    "state": "NC",
    "county": "Randolph"
  },
  {
    "fips": "02270",
    "state": "AK",
    "county": "Wade Hampton"
  },
  {
    "fips": "51141",
    "state": "VA",
    "county": "Patrick"
  },
  {
    "fips": "06109",
    "state": "CA",
    "county": "Tuolumne"
  },
  {
    "fips": "30093",
    "state": "MT",
    "county": "Silver Bow"
  },
  {
    "fips": "17199",
    "state": "IL",
    "county": "Williamson"
  },
  {
    "fips": "40053",
    "state": "OK",
    "county": "Grant"
  },
  {
    "fips": "13155",
    "state": "GA",
    "county": "Irwin"
  },
  {
    "fips": "17055",
    "state": "IL",
    "county": "Franklin"
  },
  {
    "fips": "17023",
    "state": "IL",
    "county": "Clark"
  },
  {
    "fips": "21041",
    "state": "KY",
    "county": "Carroll"
  },
  {
    "fips": "27061",
    "state": "MN",
    "county": "Itasca"
  },
  {
    "fips": "27117",
    "state": "MN",
    "county": "Pipestone"
  },
  {
    "fips": "55059",
    "state": "WI",
    "county": "Kenosha"
  },
  {
    "fips": "31047",
    "state": "NE",
    "county": "Dawson"
  },
  {
    "fips": "53077",
    "state": "WA",
    "county": "Yakima"
  },
  {
    "fips": "17109",
    "state": "IL",
    "county": "McDonough"
  },
  {
    "fips": "32019",
    "state": "NV",
    "county": "Lyon"
  },
  {
    "fips": "48339",
    "state": "TX",
    "county": "Montgomery"
  },
  {
    "fips": "48497",
    "state": "TX",
    "county": "Wise"
  },
  {
    "fips": "48469",
    "state": "TX",
    "county": "Victoria"
  },
  {
    "fips": "06037",
    "state": "CA",
    "county": "Los Angeles"
  },
  {
    "fips": "38081",
    "state": "ND",
    "county": "Sargent"
  },
  {
    "fips": "17171",
    "state": "IL",
    "county": "Scott"
  },
  {
    "fips": "26001",
    "state": "MI",
    "county": "Alcona"
  },
  {
    "fips": "21079",
    "state": "KY",
    "county": "Garrard"
  },
  {
    "fips": "01105",
    "state": "AL",
    "county": "Perry"
  },
  {
    "fips": "27033",
    "state": "MN",
    "county": "Cottonwood"
  },
  {
    "fips": "26107",
    "state": "MI",
    "county": "Mecosta"
  },
  {
    "fips": "39069",
    "state": "OH",
    "county": "Henry"
  },
  {
    "fips": "47133",
    "state": "TN",
    "county": "Overton"
  },
  {
    "fips": "08019",
    "state": "CO",
    "county": "Clear Creek"
  },
  {
    "fips": "02188",
    "state": "AK",
    "county": "Northwest Arctic"
  },
  {
    "fips": "20013",
    "state": "KS",
    "county": "Brown"
  },
  {
    "fips": "51075",
    "state": "VA",
    "county": "Goochland"
  },
  {
    "fips": "49009",
    "state": "UT",
    "county": "Daggett"
  },
  {
    "fips": "08071",
    "state": "CO",
    "county": "Las Animas"
  },
  {
    "fips": "37015",
    "state": "NC",
    "county": "Bertie"
  },
  {
    "fips": "19169",
    "state": "IA",
    "county": "Story"
  },
  {
    "fips": "39175",
    "state": "OH",
    "county": "Wyandot"
  },
  {
    "fips": "53045",
    "state": "WA",
    "county": "Mason"
  },
  {
    "fips": "29225",
    "state": "MO",
    "county": "Webster"
  },
  {
    "fips": "27007",
    "state": "MN",
    "county": "Beltrami"
  },
  {
    "fips": "12047",
    "state": "FL",
    "county": "Hamilton"
  },
  {
    "fips": "27051",
    "state": "MN",
    "county": "Grant"
  },
  {
    "fips": "21101",
    "state": "KY",
    "county": "Henderson"
  },
  {
    "fips": "21055",
    "state": "KY",
    "county": "Crittenden"
  },
  {
    "fips": "21149",
    "state": "KY",
    "county": "McLean"
  },
  {
    "fips": "30081",
    "state": "MT",
    "county": "Ravalli"
  },
  {
    "fips": "13247",
    "state": "GA",
    "county": "Rockdale"
  },
  {
    "fips": "30109",
    "state": "MT",
    "county": "Wibaux"
  },
  {
    "fips": "18019",
    "state": "IN",
    "county": "Clark"
  },
  {
    "fips": "20167",
    "state": "KS",
    "county": "Russell"
  },
  {
    "fips": "50013",
    "state": "VT",
    "county": "Grand Isle"
  },
  {
    "fips": "22051",
    "state": "LA",
    "county": "Jefferson"
  },
  {
    "fips": "31049",
    "state": "NE",
    "county": "Deuel"
  },
  {
    "fips": "29057",
    "state": "MO",
    "county": "Dade"
  },
  {
    "fips": "18075",
    "state": "IN",
    "county": "Jay"
  },
  {
    "fips": "72147",
    "state": "PR",
    "county": "Vieques"
  },
  {
    "fips": "39049",
    "state": "OH",
    "county": "Franklin"
  },
  {
    "fips": "13119",
    "state": "GA",
    "county": "Franklin"
  },
  {
    "fips": "05127",
    "state": "AR",
    "county": "Scott"
  },
  {
    "fips": "47115",
    "state": "TN",
    "county": "Marion"
  },
  {
    "fips": "48055",
    "state": "TX",
    "county": "Caldwell"
  },
  {
    "fips": "13123",
    "state": "GA",
    "county": "Gilmer"
  },
  {
    "fips": "28137",
    "state": "MS",
    "county": "Tate"
  },
  {
    "fips": "06063",
    "state": "CA",
    "county": "Plumas"
  },
  {
    "fips": "28143",
    "state": "MS",
    "county": "Tunica"
  },
  {
    "fips": "48123",
    "state": "TX",
    "county": "DeWitt"
  },
  {
    "fips": "29187",
    "state": "MO",
    "county": "St. Francois"
  },
  {
    "fips": "20181",
    "state": "KS",
    "county": "Sherman"
  },
  {
    "fips": "13017",
    "state": "GA",
    "county": "Ben Hill"
  },
  {
    "fips": "06015",
    "state": "CA",
    "county": "Del Norte"
  },
  {
    "fips": "28117",
    "state": "MS",
    "county": "Prentiss"
  },
  {
    "fips": "50025",
    "state": "VT",
    "county": "Windham"
  },
  {
    "fips": "56025",
    "state": "WY",
    "county": "Natrona"
  },
  {
    "fips": "26019",
    "state": "MI",
    "county": "Benzie"
  },
  {
    "fips": "06053",
    "state": "CA",
    "county": "Monterey"
  },
  {
    "fips": "46109",
    "state": "SD",
    "county": "Roberts"
  },
  {
    "fips": "25015",
    "state": "MA",
    "county": "Hampshire"
  },
  {
    "fips": "42079",
    "state": "PA",
    "county": "Luzerne"
  },
  {
    "fips": "06075",
    "state": "CA",
    "county": "San Francisco"
  },
  {
    "fips": "51009",
    "state": "VA",
    "county": "Amherst"
  },
  {
    "fips": "08107",
    "state": "CO",
    "county": "Routt"
  },
  {
    "fips": "08025",
    "state": "CO",
    "county": "Crowley"
  },
  {
    "fips": "47165",
    "state": "TN",
    "county": "Sumner"
  },
  {
    "fips": "27127",
    "state": "MN",
    "county": "Redwood"
  },
  {
    "fips": "49003",
    "state": "UT",
    "county": "Box Elder"
  },
  {
    "fips": "24013",
    "state": "MD",
    "county": "Carroll"
  },
  {
    "fips": "48097",
    "state": "TX",
    "county": "Cooke"
  },
  {
    "fips": "48447",
    "state": "TX",
    "county": "Throckmorton"
  },
  {
    "fips": "21019",
    "state": "KY",
    "county": "Boyd"
  },
  {
    "fips": "47175",
    "state": "TN",
    "county": "Van Buren"
  },
  {
    "fips": "40103",
    "state": "OK",
    "county": "Noble"
  },
  {
    "fips": "48167",
    "state": "TX",
    "county": "Galveston"
  },
  {
    "fips": "53025",
    "state": "WA",
    "county": "Grant"
  },
  {
    "fips": "24021",
    "state": "MD",
    "county": "Frederick"
  },
  {
    "fips": "12001",
    "state": "FL",
    "county": "Alachua"
  },
  {
    "fips": "48075",
    "state": "TX",
    "county": "Childress"
  },
  {
    "fips": "48317",
    "state": "TX",
    "county": "Martin"
  },
  {
    "fips": "13209",
    "state": "GA",
    "county": "Montgomery"
  },
  {
    "fips": "38095",
    "state": "ND",
    "county": "Towner"
  },
  {
    "fips": "46005",
    "state": "SD",
    "county": "Beadle"
  },
  {
    "fips": "05117",
    "state": "AR",
    "county": "Prairie"
  },
  {
    "fips": "46055",
    "state": "SD",
    "county": "Haakon"
  },
  {
    "fips": "13077",
    "state": "GA",
    "county": "Coweta"
  },
  {
    "fips": "28051",
    "state": "MS",
    "county": "Holmes"
  },
  {
    "fips": "48285",
    "state": "TX",
    "county": "Lavaca"
  },
  {
    "fips": "35031",
    "state": "NM",
    "county": "McKinley"
  },
  {
    "fips": "20183",
    "state": "KS",
    "county": "Smith"
  },
  {
    "fips": "56039",
    "state": "WY",
    "county": "Teton"
  },
  {
    "fips": "18119",
    "state": "IN",
    "county": "Owen"
  },
  {
    "fips": "49041",
    "state": "UT",
    "county": "Sevier"
  },
  {
    "fips": "48415",
    "state": "TX",
    "county": "Scurry"
  },
  {
    "fips": "45081",
    "state": "SC",
    "county": "Saluda"
  },
  {
    "fips": "05095",
    "state": "AR",
    "county": "Monroe"
  },
  {
    "fips": "27137",
    "state": "MN",
    "county": "St. Louis"
  },
  {
    "fips": "37059",
    "state": "NC",
    "county": "Davie"
  },
  {
    "fips": "42049",
    "state": "PA",
    "county": "Erie"
  },
  {
    "fips": "42133",
    "state": "PA",
    "county": "York"
  },
  {
    "fips": "21029",
    "state": "KY",
    "county": "Bullitt"
  },
  {
    "fips": "39123",
    "state": "OH",
    "county": "Ottawa"
  },
  {
    "fips": "46107",
    "state": "SD",
    "county": "Potter"
  },
  {
    "fips": "46069",
    "state": "SD",
    "county": "Hyde"
  },
  {
    "fips": "36099",
    "state": "NY",
    "county": "Seneca"
  },
  {
    "fips": "40037",
    "state": "OK",
    "county": "Creek"
  },
  {
    "fips": "48017",
    "state": "TX",
    "county": "Bailey"
  },
  {
    "fips": "48377",
    "state": "TX",
    "county": "Presidio"
  },
  {
    "fips": "50021",
    "state": "VT",
    "county": "Rutland"
  },
  {
    "fips": "01031",
    "state": "AL",
    "county": "Coffee"
  },
  {
    "fips": "13005",
    "state": "GA",
    "county": "Bacon"
  },
  {
    "fips": "47137",
    "state": "TN",
    "county": "Pickett"
  },
  {
    "fips": "36097",
    "state": "NY",
    "county": "Schuyler"
  },
  {
    "fips": "32007",
    "state": "NV",
    "county": "Elko"
  },
  {
    "fips": "32021",
    "state": "NV",
    "county": "Mineral"
  },
  {
    "fips": "27071",
    "state": "MN",
    "county": "Koochiching"
  },
  {
    "fips": "26053",
    "state": "MI",
    "county": "Gogebic"
  },
  {
    "fips": "35027",
    "state": "NM",
    "county": "Lincoln"
  },
  {
    "fips": "13255",
    "state": "GA",
    "county": "Spalding"
  },
  {
    "fips": "72149",
    "state": "PR",
    "county": "Villalba"
  },
  {
    "fips": "29091",
    "state": "MO",
    "county": "Howell"
  },
  {
    "fips": "38057",
    "state": "ND",
    "county": "Mercer"
  },
  {
    "fips": "26031",
    "state": "MI",
    "county": "Cheboygan"
  },
  {
    "fips": "18021",
    "state": "IN",
    "county": "Clay"
  },
  {
    "fips": "38089",
    "state": "ND",
    "county": "Stark"
  },
  {
    "fips": "08015",
    "state": "CO",
    "county": "Chaffee"
  },
  {
    "fips": "48367",
    "state": "TX",
    "county": "Parker"
  },
  {
    "fips": "33005",
    "state": "NH",
    "county": "Cheshire"
  },
  {
    "fips": "27059",
    "state": "MN",
    "county": "Isanti"
  },
  {
    "fips": "42075",
    "state": "PA",
    "county": "Lebanon"
  },
  {
    "fips": "13227",
    "state": "GA",
    "county": "Pickens"
  },
  {
    "fips": "29095",
    "state": "MO",
    "county": "Jackson"
  },
  {
    "fips": "32005",
    "state": "NV",
    "county": "Douglas"
  },
  {
    "fips": "51515",
    "state": "VA",
    "county": "Bedford"
  },
  {
    "fips": "13043",
    "state": "GA",
    "county": "Candler"
  },
  {
    "fips": "29173",
    "state": "MO",
    "county": "Ralls"
  },
  {
    "fips": "41071",
    "state": "OR",
    "county": "Yamhill"
  },
  {
    "fips": "01131",
    "state": "AL",
    "county": "Wilcox"
  },
  {
    "fips": "72137",
    "state": "PR",
    "county": "Toa Baja"
  },
  {
    "fips": "22067",
    "state": "LA",
    "county": "Morehouse"
  },
  {
    "fips": "56015",
    "state": "WY",
    "county": "Goshen"
  },
  {
    "fips": "05119",
    "state": "AR",
    "county": "Pulaski"
  },
  {
    "fips": "21237",
    "state": "KY",
    "county": "Wolfe"
  },
  {
    "fips": "18163",
    "state": "IN",
    "county": "Vanderburgh"
  },
  {
    "fips": "33003",
    "state": "NH",
    "county": "Carroll"
  },
  {
    "fips": "20095",
    "state": "KS",
    "county": "Kingman"
  },
  {
    "fips": "48465",
    "state": "TX",
    "county": "Val Verde"
  },
  {
    "fips": "42089",
    "state": "PA",
    "county": "Monroe"
  },
  {
    "fips": "46111",
    "state": "SD",
    "county": "Sanborn"
  },
  {
    "fips": "46067",
    "state": "SD",
    "county": "Hutchinson"
  },
  {
    "fips": "29209",
    "state": "MO",
    "county": "Stone"
  },
  {
    "fips": "31027",
    "state": "NE",
    "county": "Cedar"
  },
  {
    "fips": "22089",
    "state": "LA",
    "county": "St. Charles"
  },
  {
    "fips": "55069",
    "state": "WI",
    "county": "Lincoln"
  },
  {
    "fips": "27101",
    "state": "MN",
    "county": "Murray"
  },
  {
    "fips": "28091",
    "state": "MS",
    "county": "Marion"
  },
  {
    "fips": "12101",
    "state": "FL",
    "county": "Pasco"
  },
  {
    "fips": "26067",
    "state": "MI",
    "county": "Ionia"
  },
  {
    "fips": "40023",
    "state": "OK",
    "county": "Choctaw"
  },
  {
    "fips": "29161",
    "state": "MO",
    "county": "Phelps"
  },
  {
    "fips": "29079",
    "state": "MO",
    "county": "Grundy"
  },
  {
    "fips": "12083",
    "state": "FL",
    "county": "Marion"
  },
  {
    "fips": "48227",
    "state": "TX",
    "county": "Howard"
  },
  {
    "fips": "19099",
    "state": "IA",
    "county": "Jasper"
  },
  {
    "fips": "39005",
    "state": "OH",
    "county": "Ashland"
  },
  {
    "fips": "22113",
    "state": "LA",
    "county": "Vermilion"
  },
  {
    "fips": "42065",
    "state": "PA",
    "county": "Jefferson"
  },
  {
    "fips": "56027",
    "state": "WY",
    "county": "Niobrara"
  },
  {
    "fips": "40121",
    "state": "OK",
    "county": "Pittsburg"
  },
  {
    "fips": "46117",
    "state": "SD",
    "county": "Stanley"
  },
  {
    "fips": "26143",
    "state": "MI",
    "county": "Roscommon"
  },
  {
    "fips": "34013",
    "state": "NJ",
    "county": "Essex"
  },
  {
    "fips": "13215",
    "state": "GA",
    "county": "Muscogee"
  },
  {
    "fips": "28079",
    "state": "MS",
    "county": "Leake"
  },
  {
    "fips": "36003",
    "state": "NY",
    "county": "Allegany"
  },
  {
    "fips": "46127",
    "state": "SD",
    "county": "Union"
  },
  {
    "fips": "17061",
    "state": "IL",
    "county": "Greene"
  },
  {
    "fips": "46079",
    "state": "SD",
    "county": "Lake"
  },
  {
    "fips": "01115",
    "state": "AL",
    "county": "St. Clair"
  },
  {
    "fips": "48015",
    "state": "TX",
    "county": "Austin"
  },
  {
    "fips": "49039",
    "state": "UT",
    "county": "Sanpete"
  },
  {
    "fips": "12087",
    "state": "FL",
    "county": "Monroe"
  },
  {
    "fips": "29115",
    "state": "MO",
    "county": "Linn"
  },
  {
    "fips": "35039",
    "state": "NM",
    "county": "Rio Arriba"
  },
  {
    "fips": "01043",
    "state": "AL",
    "county": "Cullman"
  },
  {
    "fips": "36055",
    "state": "NY",
    "county": "Monroe"
  },
  {
    "fips": "48135",
    "state": "TX",
    "county": "Ector"
  },
  {
    "fips": "21181",
    "state": "KY",
    "county": "Nicholas"
  },
  {
    "fips": "39053",
    "state": "OH",
    "county": "Gallia"
  },
  {
    "fips": "49029",
    "state": "UT",
    "county": "Morgan"
  },
  {
    "fips": "31065",
    "state": "NE",
    "county": "Furnas"
  },
  {
    "fips": "72049",
    "state": "PR",
    "county": "Culebra"
  },
  {
    "fips": "29131",
    "state": "MO",
    "county": "Miller"
  },
  {
    "fips": "31041",
    "state": "NE",
    "county": "Custer"
  },
  {
    "fips": "47059",
    "state": "TN",
    "county": "Greene"
  },
  {
    "fips": "19043",
    "state": "IA",
    "county": "Clayton"
  },
  {
    "fips": "26035",
    "state": "MI",
    "county": "Clare"
  },
  {
    "fips": "12115",
    "state": "FL",
    "county": "Sarasota"
  },
  {
    "fips": "21039",
    "state": "KY",
    "county": "Carlisle"
  },
  {
    "fips": "13087",
    "state": "GA",
    "county": "Decatur"
  },
  {
    "fips": "48001",
    "state": "TX",
    "county": "Anderson"
  },
  {
    "fips": "21229",
    "state": "KY",
    "county": "Washington"
  },
  {
    "fips": "37199",
    "state": "NC",
    "county": "Yancey"
  },
  {
    "fips": "48443",
    "state": "TX",
    "county": "Terrell"
  },
  {
    "fips": "46003",
    "state": "SD",
    "county": "Aurora"
  },
  {
    "fips": "25017",
    "state": "MA",
    "county": "Middlesex"
  },
  {
    "fips": "21197",
    "state": "KY",
    "county": "Powell"
  },
  {
    "fips": "49043",
    "state": "UT",
    "county": "Summit"
  },
  {
    "fips": "36107",
    "state": "NY",
    "county": "Tioga"
  },
  {
    "fips": "19029",
    "state": "IA",
    "county": "Cass"
  },
  {
    "fips": "48215",
    "state": "TX",
    "county": "Hidalgo"
  },
  {
    "fips": "38001",
    "state": "ND",
    "county": "Adams"
  },
  {
    "fips": "46033",
    "state": "SD",
    "county": "Custer"
  },
  {
    "fips": "48029",
    "state": "TX",
    "county": "Bexar"
  },
  {
    "fips": "13111",
    "state": "GA",
    "county": "Fannin"
  },
  {
    "fips": "37125",
    "state": "NC",
    "county": "Moore"
  },
  {
    "fips": "21131",
    "state": "KY",
    "county": "Leslie"
  },
  {
    "fips": "49047",
    "state": "UT",
    "county": "Uintah"
  },
  {
    "fips": "55113",
    "state": "WI",
    "county": "Sawyer"
  },
  {
    "fips": "36029",
    "state": "NY",
    "county": "Erie"
  },
  {
    "fips": "30013",
    "state": "MT",
    "county": "Cascade"
  },
  {
    "fips": "30047",
    "state": "MT",
    "county": "Lake"
  },
  {
    "fips": "46089",
    "state": "SD",
    "county": "McPherson"
  },
  {
    "fips": "05079",
    "state": "AR",
    "county": "Lincoln"
  },
  {
    "fips": "17129",
    "state": "IL",
    "county": "Menard"
  },
  {
    "fips": "05125",
    "state": "AR",
    "county": "Saline"
  },
  {
    "fips": "16081",
    "state": "ID",
    "county": "Teton"
  },
  {
    "fips": "42113",
    "state": "PA",
    "county": "Sullivan"
  },
  {
    "fips": "02130",
    "state": "AK",
    "county": "Ketchikan Gateway"
  },
  {
    "fips": "06101",
    "state": "CA",
    "county": "Sutter"
  },
  {
    "fips": "12057",
    "state": "FL",
    "county": "Hillsborough"
  },
  {
    "fips": "17049",
    "state": "IL",
    "county": "Effingham"
  },
  {
    "fips": "29087",
    "state": "MO",
    "county": "Holt"
  },
  {
    "fips": "20029",
    "state": "KS",
    "county": "Cloud"
  },
  {
    "fips": "08055",
    "state": "CO",
    "county": "Huerfano"
  },
  {
    "fips": "31037",
    "state": "NE",
    "county": "Colfax"
  },
  {
    "fips": "35033",
    "state": "NM",
    "county": "Mora"
  },
  {
    "fips": "05043",
    "state": "AR",
    "county": "Drew"
  },
  {
    "fips": "19061",
    "state": "IA",
    "county": "Dubuque"
  },
  {
    "fips": "02016",
    "state": "AK",
    "county": "Aleutians West"
  },
  {
    "fips": "31099",
    "state": "NE",
    "county": "Kearney"
  },
  {
    "fips": "18067",
    "state": "IN",
    "county": "Howard"
  },
  {
    "fips": "02170",
    "state": "AK",
    "county": "Matanuska-Susitna"
  },
  {
    "fips": "37153",
    "state": "NC",
    "county": "Richmond"
  },
  {
    "fips": "01121",
    "state": "AL",
    "county": "Talladega"
  },
  {
    "fips": "22039",
    "state": "LA",
    "county": "Evangeline"
  },
  {
    "fips": "48379",
    "state": "TX",
    "county": "Rains"
  },
  {
    "fips": "16029",
    "state": "ID",
    "county": "Caribou"
  },
  {
    "fips": "53011",
    "state": "WA",
    "county": "Clark"
  },
  {
    "fips": "38099",
    "state": "ND",
    "county": "Walsh"
  },
  {
    "fips": "54023",
    "state": "WV",
    "county": "Grant"
  },
  {
    "fips": "26005",
    "state": "MI",
    "county": "Allegan"
  },
  {
    "fips": "51027",
    "state": "VA",
    "county": "Buchanan"
  },
  {
    "fips": "20197",
    "state": "KS",
    "county": "Wabaunsee"
  },
  {
    "fips": "31017",
    "state": "NE",
    "county": "Brown"
  },
  {
    "fips": "13059",
    "state": "GA",
    "county": "Clarke"
  },
  {
    "fips": "09003",
    "state": "CT",
    "county": "Hartford"
  },
  {
    "fips": "38009",
    "state": "ND",
    "county": "Bottineau"
  },
  {
    "fips": "37147",
    "state": "NC",
    "county": "Pitt"
  },
  {
    "fips": "06025",
    "state": "CA",
    "county": "Imperial"
  },
  {
    "fips": "31165",
    "state": "NE",
    "county": "Sioux"
  },
  {
    "fips": "17169",
    "state": "IL",
    "county": "Schuyler"
  },
  {
    "fips": "38027",
    "state": "ND",
    "county": "Eddy"
  },
  {
    "fips": "24027",
    "state": "MD",
    "county": "Howard"
  },
  {
    "fips": "48305",
    "state": "TX",
    "county": "Lynn"
  },
  {
    "fips": "49055",
    "state": "UT",
    "county": "Wayne"
  },
  {
    "fips": "13173",
    "state": "GA",
    "county": "Lanier"
  },
  {
    "fips": "36037",
    "state": "NY",
    "county": "Genesee"
  },
  {
    "fips": "05131",
    "state": "AR",
    "county": "Sebastian"
  },
  {
    "fips": "51169",
    "state": "VA",
    "county": "Scott"
  },
  {
    "fips": "02013",
    "state": "AK",
    "county": "Aleutians East"
  },
  {
    "fips": "20047",
    "state": "KS",
    "county": "Edwards"
  },
  {
    "fips": "13199",
    "state": "GA",
    "county": "Meriwether"
  },
  {
    "fips": "48421",
    "state": "TX",
    "county": "Sherman"
  },
  {
    "fips": "09013",
    "state": "CT",
    "county": "Tolland"
  },
  {
    "fips": "19161",
    "state": "IA",
    "county": "Sac"
  },
  {
    "fips": "46113",
    "state": "SD",
    "county": "Shannon"
  },
  {
    "fips": "48081",
    "state": "TX",
    "county": "Coke"
  },
  {
    "fips": "08073",
    "state": "CO",
    "county": "Lincoln"
  },
  {
    "fips": "40043",
    "state": "OK",
    "county": "Dewey"
  },
  {
    "fips": "19097",
    "state": "IA",
    "county": "Jackson"
  },
  {
    "fips": "05085",
    "state": "AR",
    "county": "Lonoke"
  },
  {
    "fips": "19193",
    "state": "IA",
    "county": "Woodbury"
  },
  {
    "fips": "17075",
    "state": "IL",
    "county": "Iroquois"
  },
  {
    "fips": "38055",
    "state": "ND",
    "county": "McLean"
  },
  {
    "fips": "39087",
    "state": "OH",
    "county": "Lawrence"
  },
  {
    "fips": "18107",
    "state": "IN",
    "county": "Montgomery"
  },
  {
    "fips": "31151",
    "state": "NE",
    "county": "Saline"
  },
  {
    "fips": "45023",
    "state": "SC",
    "county": "Chester"
  },
  {
    "fips": "12089",
    "state": "FL",
    "county": "Nassau"
  },
  {
    "fips": "20129",
    "state": "KS",
    "county": "Morton"
  },
  {
    "fips": "31139",
    "state": "NE",
    "county": "Pierce"
  },
  {
    "fips": "53055",
    "state": "WA",
    "county": "San Juan"
  },
  {
    "fips": "37019",
    "state": "NC",
    "county": "Brunswick"
  },
  {
    "fips": "26121",
    "state": "MI",
    "county": "Muskegon"
  },
  {
    "fips": "21061",
    "state": "KY",
    "county": "Edmonson"
  },
  {
    "fips": "55087",
    "state": "WI",
    "county": "Outagamie"
  },
  {
    "fips": "20035",
    "state": "KS",
    "county": "Cowley"
  },
  {
    "fips": "48157",
    "state": "TX",
    "county": "Fort Bend"
  },
  {
    "fips": "05145",
    "state": "AR",
    "county": "White"
  },
  {
    "fips": "22003",
    "state": "LA",
    "county": "Allen"
  },
  {
    "fips": "37025",
    "state": "NC",
    "county": "Cabarrus"
  },
  {
    "fips": "19079",
    "state": "IA",
    "county": "Hamilton"
  },
  {
    "fips": "48383",
    "state": "TX",
    "county": "Reagan"
  },
  {
    "fips": "31051",
    "state": "NE",
    "county": "Dixon"
  },
  {
    "fips": "21105",
    "state": "KY",
    "county": "Hickman"
  },
  {
    "fips": "19149",
    "state": "IA",
    "county": "Plymouth"
  },
  {
    "fips": "37093",
    "state": "NC",
    "county": "Hoke"
  },
  {
    "fips": "12133",
    "state": "FL",
    "county": "Washington"
  },
  {
    "fips": "37103",
    "state": "NC",
    "county": "Jones"
  },
  {
    "fips": "13081",
    "state": "GA",
    "county": "Crisp"
  },
  {
    "fips": "37127",
    "state": "NC",
    "county": "Nash"
  },
  {
    "fips": "55107",
    "state": "WI",
    "county": "Rusk"
  },
  {
    "fips": "27011",
    "state": "MN",
    "county": "Big Stone"
  },
  {
    "fips": "06017",
    "state": "CA",
    "county": "El Dorado"
  },
  {
    "fips": "31003",
    "state": "NE",
    "county": "Antelope"
  },
  {
    "fips": "49011",
    "state": "UT",
    "county": "Davis"
  },
  {
    "fips": "29083",
    "state": "MO",
    "county": "Henry"
  },
  {
    "fips": "31155",
    "state": "NE",
    "county": "Saunders"
  },
  {
    "fips": "34009",
    "state": "NJ",
    "county": "Cape May"
  },
  {
    "fips": "18165",
    "state": "IN",
    "county": "Vermillion"
  },
  {
    "fips": "20147",
    "state": "KS",
    "county": "Phillips"
  },
  {
    "fips": "72065",
    "state": "PR",
    "county": "Hatillo"
  },
  {
    "fips": "55073",
    "state": "WI",
    "county": "Marathon"
  },
  {
    "fips": "55111",
    "state": "WI",
    "county": "Sauk"
  },
  {
    "fips": "19057",
    "state": "IA",
    "county": "Des Moines"
  },
  {
    "fips": "05045",
    "state": "AR",
    "county": "Faulkner"
  },
  {
    "fips": "20021",
    "state": "KS",
    "county": "Cherokee"
  },
  {
    "fips": "36065",
    "state": "NY",
    "county": "Oneida"
  },
  {
    "fips": "46031",
    "state": "SD",
    "county": "Corson"
  },
  {
    "fips": "23019",
    "state": "ME",
    "county": "Penobscot"
  },
  {
    "fips": "48467",
    "state": "TX",
    "county": "Van Zandt"
  },
  {
    "fips": "18145",
    "state": "IN",
    "county": "Shelby"
  },
  {
    "fips": "35053",
    "state": "NM",
    "county": "Socorro"
  },
  {
    "fips": "51181",
    "state": "VA",
    "county": "Surry"
  },
  {
    "fips": "12027",
    "state": "FL",
    "county": "DeSoto"
  },
  {
    "fips": "17181",
    "state": "IL",
    "county": "Union"
  },
  {
    "fips": "30057",
    "state": "MT",
    "county": "Madison"
  },
  {
    "fips": "31063",
    "state": "NE",
    "county": "Frontier"
  },
  {
    "fips": "39149",
    "state": "OH",
    "county": "Shelby"
  },
  {
    "fips": "72099",
    "state": "PR",
    "county": "Moca"
  },
  {
    "fips": "13121",
    "state": "GA",
    "county": "Fulton"
  },
  {
    "fips": "18047",
    "state": "IN",
    "county": "Franklin"
  },
  {
    "fips": "30031",
    "state": "MT",
    "county": "Gallatin"
  },
  {
    "fips": "38087",
    "state": "ND",
    "county": "Slope"
  },
  {
    "fips": "13031",
    "state": "GA",
    "county": "Bulloch"
  },
  {
    "fips": "13139",
    "state": "GA",
    "county": "Hall"
  },
  {
    "fips": "13313",
    "state": "GA",
    "county": "Whitfield"
  },
  {
    "fips": "53047",
    "state": "WA",
    "county": "Okanogan"
  },
  {
    "fips": "13013",
    "state": "GA",
    "county": "Barrow"
  },
  {
    "fips": "24019",
    "state": "MD",
    "county": "Dorchester"
  },
  {
    "fips": "49053",
    "state": "UT",
    "county": "Washington"
  },
  {
    "fips": "29013",
    "state": "MO",
    "county": "Bates"
  },
  {
    "fips": "45053",
    "state": "SC",
    "county": "Jasper"
  },
  {
    "fips": "19173",
    "state": "IA",
    "county": "Taylor"
  },
  {
    "fips": "27001",
    "state": "MN",
    "county": "Aitkin"
  },
  {
    "fips": "38063",
    "state": "ND",
    "county": "Nelson"
  },
  {
    "fips": "48303",
    "state": "TX",
    "county": "Lubbock"
  },
  {
    "fips": "41005",
    "state": "OR",
    "county": "Clackamas"
  },
  {
    "fips": "48041",
    "state": "TX",
    "county": "Brazos"
  },
  {
    "fips": "51053",
    "state": "VA",
    "county": "Dinwiddie"
  },
  {
    "fips": "26051",
    "state": "MI",
    "county": "Gladwin"
  },
  {
    "fips": "48349",
    "state": "TX",
    "county": "Navarro"
  },
  {
    "fips": "13101",
    "state": "GA",
    "county": "Echols"
  },
  {
    "fips": "27093",
    "state": "MN",
    "county": "Meeker"
  },
  {
    "fips": "51057",
    "state": "VA",
    "county": "Essex"
  },
  {
    "fips": "13047",
    "state": "GA",
    "county": "Catoosa"
  },
  {
    "fips": "72109",
    "state": "PR",
    "county": "Patillas"
  },
  {
    "fips": "18073",
    "state": "IN",
    "county": "Jasper"
  },
  {
    "fips": "50015",
    "state": "VT",
    "county": "Lamoille"
  },
  {
    "fips": "40067",
    "state": "OK",
    "county": "Jefferson"
  },
  {
    "fips": "27083",
    "state": "MN",
    "county": "Lyon"
  },
  {
    "fips": "23025",
    "state": "ME",
    "county": "Somerset"
  },
  {
    "fips": "51620",
    "state": "VA",
    "county": "Franklin"
  },
  {
    "fips": "16053",
    "state": "ID",
    "county": "Jerome"
  },
  {
    "fips": "08121",
    "state": "CO",
    "county": "Washington"
  },
  {
    "fips": "01027",
    "state": "AL",
    "county": "Clay"
  },
  {
    "fips": "06111",
    "state": "CA",
    "county": "Ventura"
  },
  {
    "fips": "26129",
    "state": "MI",
    "county": "Ogemaw"
  },
  {
    "fips": "42069",
    "state": "PA",
    "county": "Lackawanna"
  },
  {
    "fips": "46125",
    "state": "SD",
    "county": "Turner"
  },
  {
    "fips": "32017",
    "state": "NV",
    "county": "Lincoln"
  },
  {
    "fips": "47177",
    "state": "TN",
    "county": "Warren"
  },
  {
    "fips": "35057",
    "state": "NM",
    "county": "Torrance"
  },
  {
    "fips": "42081",
    "state": "PA",
    "county": "Lycoming"
  },
  {
    "fips": "39107",
    "state": "OH",
    "county": "Mercer"
  },
  {
    "fips": "26115",
    "state": "MI",
    "county": "Monroe"
  },
  {
    "fips": "21095",
    "state": "KY",
    "county": "Harlan"
  },
  {
    "fips": "19019",
    "state": "IA",
    "county": "Buchanan"
  },
  {
    "fips": "47109",
    "state": "TN",
    "county": "McNairy"
  },
  {
    "fips": "45019",
    "state": "SC",
    "county": "Charleston"
  },
  {
    "fips": "18123",
    "state": "IN",
    "county": "Perry"
  },
  {
    "fips": "21185",
    "state": "KY",
    "county": "Oldham"
  },
  {
    "fips": "21141",
    "state": "KY",
    "county": "Logan"
  },
  {
    "fips": "35005",
    "state": "NM",
    "county": "Chaves"
  },
  {
    "fips": "48461",
    "state": "TX",
    "county": "Upton"
  },
  {
    "fips": "51580",
    "state": "VA",
    "county": "Covington"
  },
  {
    "fips": "20155",
    "state": "KS",
    "county": "Reno"
  },
  {
    "fips": "29167",
    "state": "MO",
    "county": "Polk"
  },
  {
    "fips": "13157",
    "state": "GA",
    "county": "Jackson"
  },
  {
    "fips": "47055",
    "state": "TN",
    "county": "Giles"
  },
  {
    "fips": "48259",
    "state": "TX",
    "county": "Kendall"
  },
  {
    "fips": "19033",
    "state": "IA",
    "county": "Cerro Gordo"
  },
  {
    "fips": "08013",
    "state": "CO",
    "county": "Boulder"
  },
  {
    "fips": "39007",
    "state": "OH",
    "county": "Ashtabula"
  },
  {
    "fips": "39143",
    "state": "OH",
    "county": "Sandusky"
  },
  {
    "fips": "48173",
    "state": "TX",
    "county": "Glasscock"
  },
  {
    "fips": "47057",
    "state": "TN",
    "county": "Grainger"
  },
  {
    "fips": "51125",
    "state": "VA",
    "county": "Nelson"
  },
  {
    "fips": "34039",
    "state": "NJ",
    "county": "Union"
  },
  {
    "fips": "17085",
    "state": "IL",
    "county": "Jo Daviess"
  },
  {
    "fips": "01111",
    "state": "AL",
    "county": "Randolph"
  },
  {
    "fips": "55121",
    "state": "WI",
    "county": "Trempealeau"
  },
  {
    "fips": "30001",
    "state": "MT",
    "county": "Beaverhead"
  },
  {
    "fips": "51810",
    "state": "VA",
    "county": "Virginia Beach"
  },
  {
    "fips": "56041",
    "state": "WY",
    "county": "Uinta"
  },
  {
    "fips": "38045",
    "state": "ND",
    "county": "LaMoure"
  },
  {
    "fips": "13071",
    "state": "GA",
    "county": "Colquitt"
  },
  {
    "fips": "30009",
    "state": "MT",
    "county": "Carbon"
  },
  {
    "fips": "25009",
    "state": "MA",
    "county": "Essex"
  },
  {
    "fips": "37115",
    "state": "NC",
    "county": "Madison"
  },
  {
    "fips": "29065",
    "state": "MO",
    "county": "Dent"
  },
  {
    "fips": "41011",
    "state": "OR",
    "county": "Coos"
  },
  {
    "fips": "40135",
    "state": "OK",
    "county": "Sequoyah"
  },
  {
    "fips": "16003",
    "state": "ID",
    "county": "Adams"
  },
  {
    "fips": "35025",
    "state": "NM",
    "county": "Lea"
  },
  {
    "fips": "48059",
    "state": "TX",
    "county": "Callahan"
  },
  {
    "fips": "18015",
    "state": "IN",
    "county": "Carroll"
  },
  {
    "fips": "42127",
    "state": "PA",
    "county": "Wayne"
  },
  {
    "fips": "13127",
    "state": "GA",
    "county": "Glynn"
  },
  {
    "fips": "20055",
    "state": "KS",
    "county": "Finney"
  },
  {
    "fips": "36059",
    "state": "NY",
    "county": "Nassau"
  },
  {
    "fips": "01079",
    "state": "AL",
    "county": "Lawrence"
  },
  {
    "fips": "41007",
    "state": "OR",
    "county": "Clatsop"
  },
  {
    "fips": "48439",
    "state": "TX",
    "county": "Tarrant"
  },
  {
    "fips": "53041",
    "state": "WA",
    "county": "Lewis"
  },
  {
    "fips": "12111",
    "state": "FL",
    "county": "St. Lucie"
  },
  {
    "fips": "20189",
    "state": "KS",
    "county": "Stevens"
  },
  {
    "fips": "27145",
    "state": "MN",
    "county": "Stearns"
  },
  {
    "fips": "72031",
    "state": "PR",
    "county": "Carolina"
  },
  {
    "fips": "21201",
    "state": "KY",
    "county": "Robertson"
  },
  {
    "fips": "37179",
    "state": "NC",
    "county": "Union"
  },
  {
    "fips": "28121",
    "state": "MS",
    "county": "Rankin"
  },
  {
    "fips": "13179",
    "state": "GA",
    "county": "Liberty"
  },
  {
    "fips": "13039",
    "state": "GA",
    "county": "Camden"
  },
  {
    "fips": "18049",
    "state": "IN",
    "county": "Fulton"
  },
  {
    "fips": "23007",
    "state": "ME",
    "county": "Franklin"
  },
  {
    "fips": "26025",
    "state": "MI",
    "county": "Calhoun"
  },
  {
    "fips": "28019",
    "state": "MS",
    "county": "Choctaw"
  },
  {
    "fips": "05075",
    "state": "AR",
    "county": "Lawrence"
  },
  {
    "fips": "01075",
    "state": "AL",
    "county": "Lamar"
  },
  {
    "fips": "16011",
    "state": "ID",
    "county": "Bingham"
  },
  {
    "fips": "26139",
    "state": "MI",
    "county": "Ottawa"
  },
  {
    "fips": "13249",
    "state": "GA",
    "county": "Schley"
  },
  {
    "fips": "18127",
    "state": "IN",
    "county": "Porter"
  },
  {
    "fips": "40109",
    "state": "OK",
    "county": "Oklahoma"
  },
  {
    "fips": "72139",
    "state": "PR",
    "county": "Trujillo Alto"
  },
  {
    "fips": "19101",
    "state": "IA",
    "county": "Jefferson"
  },
  {
    "fips": "37069",
    "state": "NC",
    "county": "Franklin"
  },
  {
    "fips": "47011",
    "state": "TN",
    "county": "Bradley"
  },
  {
    "fips": "28061",
    "state": "MS",
    "county": "Jasper"
  },
  {
    "fips": "13051",
    "state": "GA",
    "county": "Chatham"
  },
  {
    "fips": "47047",
    "state": "TN",
    "county": "Fayette"
  },
  {
    "fips": "38065",
    "state": "ND",
    "county": "Oliver"
  },
  {
    "fips": "31177",
    "state": "NE",
    "county": "Washington"
  },
  {
    "fips": "29199",
    "state": "MO",
    "county": "Scotland"
  },
  {
    "fips": "54051",
    "state": "WV",
    "county": "Marshall"
  },
  {
    "fips": "48051",
    "state": "TX",
    "county": "Burleson"
  },
  {
    "fips": "45041",
    "state": "SC",
    "county": "Florence"
  },
  {
    "fips": "17065",
    "state": "IL",
    "county": "Hamilton"
  },
  {
    "fips": "17159",
    "state": "IL",
    "county": "Richland"
  },
  {
    "fips": "20073",
    "state": "KS",
    "county": "Greenwood"
  },
  {
    "fips": "21075",
    "state": "KY",
    "county": "Fulton"
  },
  {
    "fips": "22075",
    "state": "LA",
    "county": "Plaquemines"
  },
  {
    "fips": "26055",
    "state": "MI",
    "county": "Grand Traverse"
  },
  {
    "fips": "04021",
    "state": "AZ",
    "county": "Pinal"
  },
  {
    "fips": "40073",
    "state": "OK",
    "county": "Kingfisher"
  },
  {
    "fips": "06051",
    "state": "CA",
    "county": "Mono"
  },
  {
    "fips": "55043",
    "state": "WI",
    "county": "Grant"
  },
  {
    "fips": "46101",
    "state": "SD",
    "county": "Moody"
  },
  {
    "fips": "48487",
    "state": "TX",
    "county": "Wilbarger"
  },
  {
    "fips": "37099",
    "state": "NC",
    "county": "Jackson"
  },
  {
    "fips": "18011",
    "state": "IN",
    "county": "Boone"
  },
  {
    "fips": "31013",
    "state": "NE",
    "county": "Box Butte"
  },
  {
    "fips": "13177",
    "state": "GA",
    "county": "Lee"
  },
  {
    "fips": "47179",
    "state": "TN",
    "county": "Washington"
  },
  {
    "fips": "51097",
    "state": "VA",
    "county": "King and Queen"
  },
  {
    "fips": "47111",
    "state": "TN",
    "county": "Macon"
  },
  {
    "fips": "19031",
    "state": "IA",
    "county": "Cedar"
  },
  {
    "fips": "30019",
    "state": "MT",
    "county": "Daniels"
  },
  {
    "fips": "42073",
    "state": "PA",
    "county": "Lawrence"
  },
  {
    "fips": "29151",
    "state": "MO",
    "county": "Osage"
  },
  {
    "fips": "31125",
    "state": "NE",
    "county": "Nance"
  },
  {
    "fips": "21143",
    "state": "KY",
    "county": "Lyon"
  },
  {
    "fips": "41027",
    "state": "OR",
    "county": "Hood River"
  },
  {
    "fips": "36087",
    "state": "NY",
    "county": "Rockland"
  },
  {
    "fips": "12037",
    "state": "FL",
    "county": "Franklin"
  },
  {
    "fips": "39153",
    "state": "OH",
    "county": "Summit"
  },
  {
    "fips": "51775",
    "state": "VA",
    "county": "Salem"
  },
  {
    "fips": "53001",
    "state": "WA",
    "county": "Adams"
  },
  {
    "fips": "18053",
    "state": "IN",
    "county": "Grant"
  },
  {
    "fips": "13231",
    "state": "GA",
    "county": "Pike"
  },
  {
    "fips": "32011",
    "state": "NV",
    "county": "Eureka"
  },
  {
    "fips": "18151",
    "state": "IN",
    "county": "Steuben"
  },
  {
    "fips": "39025",
    "state": "OH",
    "county": "Clermont"
  },
  {
    "fips": "50001",
    "state": "VT",
    "county": "Addison"
  },
  {
    "fips": "17195",
    "state": "IL",
    "county": "Whiteside"
  },
  {
    "fips": "54071",
    "state": "WV",
    "county": "Pendleton"
  },
  {
    "fips": "27165",
    "state": "MN",
    "county": "Watonwan"
  },
  {
    "fips": "28133",
    "state": "MS",
    "county": "Sunflower"
  },
  {
    "fips": "54091",
    "state": "WV",
    "county": "Taylor"
  },
  {
    "fips": "42053",
    "state": "PA",
    "county": "Forest"
  },
  {
    "fips": "47039",
    "state": "TN",
    "county": "Decatur"
  },
  {
    "fips": "01107",
    "state": "AL",
    "county": "Pickens"
  },
  {
    "fips": "29215",
    "state": "MO",
    "county": "Texas"
  },
  {
    "fips": "02150",
    "state": "AK",
    "county": "Kodiak Island"
  },
  {
    "fips": "06021",
    "state": "CA",
    "county": "Glenn"
  },
  {
    "fips": "16027",
    "state": "ID",
    "county": "Canyon"
  },
  {
    "fips": "31033",
    "state": "NE",
    "county": "Cheyenne"
  },
  {
    "fips": "19045",
    "state": "IA",
    "county": "Clinton"
  },
  {
    "fips": "31141",
    "state": "NE",
    "county": "Platte"
  },
  {
    "fips": "22109",
    "state": "LA",
    "county": "Terrebonne"
  },
  {
    "fips": "26147",
    "state": "MI",
    "county": "St. Clair"
  },
  {
    "fips": "40099",
    "state": "OK",
    "county": "Murray"
  },
  {
    "fips": "42007",
    "state": "PA",
    "county": "Beaver"
  },
  {
    "fips": "26141",
    "state": "MI",
    "county": "Presque Isle"
  },
  {
    "fips": "01017",
    "state": "AL",
    "county": "Chambers"
  },
  {
    "fips": "02100",
    "state": "AK",
    "county": "Haines"
  },
  {
    "fips": "20005",
    "state": "KS",
    "county": "Atchison"
  },
  {
    "fips": "31137",
    "state": "NE",
    "county": "Phelps"
  },
  {
    "fips": "54077",
    "state": "WV",
    "county": "Preston"
  },
  {
    "fips": "37119",
    "state": "NC",
    "county": "Mecklenburg"
  },
  {
    "fips": "13161",
    "state": "GA",
    "county": "Jeff Davis"
  },
  {
    "fips": "53071",
    "state": "WA",
    "county": "Walla Walla"
  },
  {
    "fips": "19025",
    "state": "IA",
    "county": "Calhoun"
  },
  {
    "fips": "13145",
    "state": "GA",
    "county": "Harris"
  },
  {
    "fips": "18007",
    "state": "IN",
    "county": "Benton"
  },
  {
    "fips": "51195",
    "state": "VA",
    "county": "Wise"
  },
  {
    "fips": "19083",
    "state": "IA",
    "county": "Hardin"
  },
  {
    "fips": "13321",
    "state": "GA",
    "county": "Worth"
  },
  {
    "fips": "20025",
    "state": "KS",
    "county": "Clark"
  },
  {
    "fips": "01091",
    "state": "AL",
    "county": "Marengo"
  },
  {
    "fips": "38083",
    "state": "ND",
    "county": "Sheridan"
  },
  {
    "fips": "16085",
    "state": "ID",
    "county": "Valley"
  },
  {
    "fips": "40093",
    "state": "OK",
    "county": "Major"
  },
  {
    "fips": "16033",
    "state": "ID",
    "county": "Clark"
  },
  {
    "fips": "13025",
    "state": "GA",
    "county": "Brantley"
  },
  {
    "fips": "06073",
    "state": "CA",
    "county": "San Diego"
  },
  {
    "fips": "39043",
    "state": "OH",
    "county": "Erie"
  },
  {
    "fips": "21183",
    "state": "KY",
    "county": "Ohio"
  },
  {
    "fips": "46041",
    "state": "SD",
    "county": "Dewey"
  },
  {
    "fips": "48335",
    "state": "TX",
    "county": "Mitchell"
  },
  {
    "fips": "08105",
    "state": "CO",
    "county": "Rio Grande"
  },
  {
    "fips": "20089",
    "state": "KS",
    "county": "Jewell"
  },
  {
    "fips": "20193",
    "state": "KS",
    "county": "Thomas"
  },
  {
    "fips": "13187",
    "state": "GA",
    "county": "Lumpkin"
  },
  {
    "fips": "48161",
    "state": "TX",
    "county": "Freestone"
  },
  {
    "fips": "22099",
    "state": "LA",
    "county": "St. Martin"
  },
  {
    "fips": "40141",
    "state": "OK",
    "county": "Tillman"
  },
  {
    "fips": "37037",
    "state": "NC",
    "county": "Chatham"
  },
  {
    "fips": "39129",
    "state": "OH",
    "county": "Pickaway"
  },
  {
    "fips": "21087",
    "state": "KY",
    "county": "Green"
  },
  {
    "fips": "23027",
    "state": "ME",
    "county": "Waldo"
  },
  {
    "fips": "13293",
    "state": "GA",
    "county": "Upson"
  },
  {
    "fips": "27113",
    "state": "MN",
    "county": "Pennington"
  },
  {
    "fips": "41047",
    "state": "OR",
    "county": "Marion"
  },
  {
    "fips": "38035",
    "state": "ND",
    "county": "Grand Forks"
  },
  {
    "fips": "41061",
    "state": "OR",
    "county": "Union"
  },
  {
    "fips": "13129",
    "state": "GA",
    "county": "Gordon"
  },
  {
    "fips": "21109",
    "state": "KY",
    "county": "Jackson"
  },
  {
    "fips": "47153",
    "state": "TN",
    "county": "Sequatchie"
  },
  {
    "fips": "46035",
    "state": "SD",
    "county": "Davison"
  },
  {
    "fips": "13309",
    "state": "GA",
    "county": "Wheeler"
  },
  {
    "fips": "26101",
    "state": "MI",
    "county": "Manistee"
  },
  {
    "fips": "12086",
    "state": "FL",
    "county": "Miami-Dade"
  },
  {
    "fips": "35017",
    "state": "NM",
    "county": "Grant"
  },
  {
    "fips": "27099",
    "state": "MN",
    "county": "Mower"
  },
  {
    "fips": "48407",
    "state": "TX",
    "county": "San Jacinto"
  },
  {
    "fips": "26145",
    "state": "MI",
    "county": "Saginaw"
  },
  {
    "fips": "13115",
    "state": "GA",
    "county": "Floyd"
  },
  {
    "fips": "46085",
    "state": "SD",
    "county": "Lyman"
  },
  {
    "fips": "69085",
    "state": "MP",
    "county": "Northern Islands"
  },
  {
    "fips": "55127",
    "state": "WI",
    "county": "Walworth"
  },
  {
    "fips": "05129",
    "state": "AR",
    "county": "Searcy"
  },
  {
    "fips": "55135",
    "state": "WI",
    "county": "Waupaca"
  },
  {
    "fips": "27081",
    "state": "MN",
    "county": "Lincoln"
  },
  {
    "fips": "49049",
    "state": "UT",
    "county": "Utah"
  },
  {
    "fips": "30065",
    "state": "MT",
    "county": "Musselshell"
  },
  {
    "fips": "51640",
    "state": "VA",
    "county": "Galax"
  },
  {
    "fips": "51163",
    "state": "VA",
    "county": "Rockbridge"
  },
  {
    "fips": "48325",
    "state": "TX",
    "county": "Medina"
  },
  {
    "fips": "20123",
    "state": "KS",
    "county": "Mitchell"
  },
  {
    "fips": "46083",
    "state": "SD",
    "county": "Lincoln"
  },
  {
    "fips": "39117",
    "state": "OH",
    "county": "Morrow"
  },
  {
    "fips": "29149",
    "state": "MO",
    "county": "Oregon"
  },
  {
    "fips": "32027",
    "state": "NV",
    "county": "Pershing"
  },
  {
    "fips": "42117",
    "state": "PA",
    "county": "Tioga"
  },
  {
    "fips": "29033",
    "state": "MO",
    "county": "Carroll"
  },
  {
    "fips": "13107",
    "state": "GA",
    "county": "Emanuel"
  },
  {
    "fips": "18153",
    "state": "IN",
    "county": "Sullivan"
  },
  {
    "fips": "22045",
    "state": "LA",
    "county": "Iberia"
  },
  {
    "fips": "46135",
    "state": "SD",
    "county": "Yankton"
  },
  {
    "fips": "47013",
    "state": "TN",
    "county": "Campbell"
  },
  {
    "fips": "19037",
    "state": "IA",
    "county": "Chickasaw"
  },
  {
    "fips": "48345",
    "state": "TX",
    "county": "Motley"
  },
  {
    "fips": "17191",
    "state": "IL",
    "county": "Wayne"
  },
  {
    "fips": "08095",
    "state": "CO",
    "county": "Phillips"
  },
  {
    "fips": "45029",
    "state": "SC",
    "county": "Colleton"
  },
  {
    "fips": "36067",
    "state": "NY",
    "county": "Onondaga"
  },
  {
    "fips": "40007",
    "state": "OK",
    "county": "Beaver"
  },
  {
    "fips": "25011",
    "state": "MA",
    "county": "Franklin"
  },
  {
    "fips": "23031",
    "state": "ME",
    "county": "York"
  },
  {
    "fips": "29075",
    "state": "MO",
    "county": "Gentry"
  },
  {
    "fips": "39019",
    "state": "OH",
    "county": "Carroll"
  },
  {
    "fips": "55029",
    "state": "WI",
    "county": "Door"
  },
  {
    "fips": "13303",
    "state": "GA",
    "county": "Washington"
  },
  {
    "fips": "01069",
    "state": "AL",
    "county": "Houston"
  },
  {
    "fips": "37129",
    "state": "NC",
    "county": "New Hanover"
  },
  {
    "fips": "36017",
    "state": "NY",
    "county": "Chenango"
  },
  {
    "fips": "37189",
    "state": "NC",
    "county": "Watauga"
  },
  {
    "fips": "22121",
    "state": "LA",
    "county": "West Baton Rouge"
  },
  {
    "fips": "39009",
    "state": "OH",
    "county": "Athens"
  },
  {
    "fips": "08101",
    "state": "CO",
    "county": "Pueblo"
  },
  {
    "fips": "17063",
    "state": "IL",
    "county": "Grundy"
  },
  {
    "fips": "29171",
    "state": "MO",
    "county": "Putnam"
  },
  {
    "fips": "08037",
    "state": "CO",
    "county": "Eagle"
  },
  {
    "fips": "19109",
    "state": "IA",
    "county": "Kossuth"
  },
  {
    "fips": "72037",
    "state": "PR",
    "county": "Ceiba"
  },
  {
    "fips": "21027",
    "state": "KY",
    "county": "Breckinridge"
  },
  {
    "fips": "31045",
    "state": "NE",
    "county": "Dawes"
  },
  {
    "fips": "45039",
    "state": "SC",
    "county": "Fairfield"
  },
  {
    "fips": "72007",
    "state": "PR",
    "county": "Aguas Buenas"
  },
  {
    "fips": "13185",
    "state": "GA",
    "county": "Lowndes"
  },
  {
    "fips": "08065",
    "state": "CO",
    "county": "Lake"
  },
  {
    "fips": "20009",
    "state": "KS",
    "county": "Barton"
  },
  {
    "fips": "21007",
    "state": "KY",
    "county": "Ballard"
  },
  {
    "fips": "51660",
    "state": "VA",
    "county": "Harrisonburg"
  },
  {
    "fips": "72105",
    "state": "PR",
    "county": "Naranjito"
  },
  {
    "fips": "19005",
    "state": "IA",
    "county": "Allamakee"
  },
  {
    "fips": "19133",
    "state": "IA",
    "county": "Monona"
  },
  {
    "fips": "22079",
    "state": "LA",
    "county": "Rapides"
  },
  {
    "fips": "51013",
    "state": "VA",
    "county": "Arlington"
  },
  {
    "fips": "29051",
    "state": "MO",
    "county": "Cole"
  },
  {
    "fips": "12121",
    "state": "FL",
    "county": "Suwannee"
  },
  {
    "fips": "18171",
    "state": "IN",
    "county": "Warren"
  },
  {
    "fips": "19165",
    "state": "IA",
    "county": "Shelby"
  },
  {
    "fips": "18035",
    "state": "IN",
    "county": "Delaware"
  },
  {
    "fips": "21073",
    "state": "KY",
    "county": "Franklin"
  },
  {
    "fips": "26137",
    "state": "MI",
    "county": "Otsego"
  },
  {
    "fips": "48213",
    "state": "TX",
    "county": "Henderson"
  },
  {
    "fips": "42077",
    "state": "PA",
    "county": "Lehigh"
  },
  {
    "fips": "17017",
    "state": "IL",
    "county": "Cass"
  },
  {
    "fips": "01019",
    "state": "AL",
    "county": "Cherokee"
  },
  {
    "fips": "20101",
    "state": "KS",
    "county": "Lane"
  },
  {
    "fips": "54011",
    "state": "WV",
    "county": "Cabell"
  },
  {
    "fips": "01029",
    "state": "AL",
    "county": "Cleburne"
  },
  {
    "fips": "27171",
    "state": "MN",
    "county": "Wright"
  },
  {
    "fips": "51149",
    "state": "VA",
    "county": "Prince George"
  },
  {
    "fips": "54015",
    "state": "WV",
    "county": "Clay"
  },
  {
    "fips": "22031",
    "state": "LA",
    "county": "De Soto"
  },
  {
    "fips": "06059",
    "state": "CA",
    "county": "Orange"
  },
  {
    "fips": "28081",
    "state": "MS",
    "county": "Lee"
  },
  {
    "fips": "48141",
    "state": "TX",
    "county": "El Paso"
  },
  {
    "fips": "01073",
    "state": "AL",
    "county": "Jefferson"
  },
  {
    "fips": "27039",
    "state": "MN",
    "county": "Dodge"
  },
  {
    "fips": "06099",
    "state": "CA",
    "county": "Stanislaus"
  },
  {
    "fips": "19157",
    "state": "IA",
    "county": "Poweshiek"
  },
  {
    "fips": "31163",
    "state": "NE",
    "county": "Sherman"
  },
  {
    "fips": "47083",
    "state": "TN",
    "county": "Houston"
  },
  {
    "fips": "13171",
    "state": "GA",
    "county": "Lamar"
  },
  {
    "fips": "12029",
    "state": "FL",
    "county": "Dixie"
  },
  {
    "fips": "55089",
    "state": "WI",
    "county": "Ozaukee"
  },
  {
    "fips": "53075",
    "state": "WA",
    "county": "Whitman"
  },
  {
    "fips": "37165",
    "state": "NC",
    "county": "Scotland"
  },
  {
    "fips": "55117",
    "state": "WI",
    "county": "Sheboygan"
  },
  {
    "fips": "55011",
    "state": "WI",
    "county": "Buffalo"
  },
  {
    "fips": "12065",
    "state": "FL",
    "county": "Jefferson"
  },
  {
    "fips": "26097",
    "state": "MI",
    "county": "Mackinac"
  },
  {
    "fips": "17133",
    "state": "IL",
    "county": "Monroe"
  },
  {
    "fips": "31031",
    "state": "NE",
    "county": "Cherry"
  },
  {
    "fips": "06005",
    "state": "CA",
    "county": "Amador"
  },
  {
    "fips": "29085",
    "state": "MO",
    "county": "Hickory"
  },
  {
    "fips": "46037",
    "state": "SD",
    "county": "Day"
  },
  {
    "fips": "02164",
    "state": "AK",
    "county": "Lake and Peninsula"
  },
  {
    "fips": "05133",
    "state": "AR",
    "county": "Sevier"
  },
  {
    "fips": "13289",
    "state": "GA",
    "county": "Twiggs"
  },
  {
    "fips": "28009",
    "state": "MS",
    "county": "Benton"
  },
  {
    "fips": "19073",
    "state": "IA",
    "county": "Greene"
  },
  {
    "fips": "40149",
    "state": "OK",
    "county": "Washita"
  },
  {
    "fips": "42119",
    "state": "PA",
    "county": "Union"
  },
  {
    "fips": "26021",
    "state": "MI",
    "county": "Berrien"
  },
  {
    "fips": "13211",
    "state": "GA",
    "county": "Morgan"
  },
  {
    "fips": "31149",
    "state": "NE",
    "county": "Rock"
  },
  {
    "fips": "19107",
    "state": "IA",
    "county": "Keokuk"
  },
  {
    "fips": "50017",
    "state": "VT",
    "county": "Orange"
  },
  {
    "fips": "38079",
    "state": "ND",
    "county": "Rolette"
  },
  {
    "fips": "54043",
    "state": "WV",
    "county": "Lincoln"
  },
  {
    "fips": "01083",
    "state": "AL",
    "county": "Limestone"
  },
  {
    "fips": "16069",
    "state": "ID",
    "county": "Nez Perce"
  },
  {
    "fips": "27091",
    "state": "MN",
    "county": "Martin"
  },
  {
    "fips": "51119",
    "state": "VA",
    "county": "Middlesex"
  },
  {
    "fips": "26007",
    "state": "MI",
    "county": "Alpena"
  },
  {
    "fips": "05023",
    "state": "AR",
    "county": "Cleburne"
  },
  {
    "fips": "21067",
    "state": "KY",
    "county": "Fayette"
  },
  {
    "fips": "37121",
    "state": "NC",
    "county": "Mitchell"
  },
  {
    "fips": "01125",
    "state": "AL",
    "county": "Tuscaloosa"
  },
  {
    "fips": "29177",
    "state": "MO",
    "county": "Ray"
  },
  {
    "fips": "16031",
    "state": "ID",
    "county": "Cassia"
  },
  {
    "fips": "48223",
    "state": "TX",
    "county": "Hopkins"
  },
  {
    "fips": "39055",
    "state": "OH",
    "county": "Geauga"
  },
  {
    "fips": "51193",
    "state": "VA",
    "county": "Westmoreland"
  },
  {
    "fips": "48261",
    "state": "TX",
    "county": "Kenedy"
  },
  {
    "fips": "55067",
    "state": "WI",
    "county": "Langlade"
  },
  {
    "fips": "48475",
    "state": "TX",
    "county": "Ward"
  },
  {
    "fips": "06003",
    "state": "CA",
    "county": "Alpine"
  },
  {
    "fips": "51685",
    "state": "VA",
    "county": "Manassas Park"
  },
  {
    "fips": "48431",
    "state": "TX",
    "county": "Sterling"
  },
  {
    "fips": "37055",
    "state": "NC",
    "county": "Dare"
  },
  {
    "fips": "36089",
    "state": "NY",
    "county": "St. Lawrence"
  },
  {
    "fips": "27077",
    "state": "MN",
    "county": "Lake of the Woods"
  },
  {
    "fips": "51105",
    "state": "VA",
    "county": "Lee"
  },
  {
    "fips": "42105",
    "state": "PA",
    "county": "Potter"
  },
  {
    "fips": "18031",
    "state": "IN",
    "county": "Decatur"
  },
  {
    "fips": "01001",
    "state": "AL",
    "county": "Autauga"
  },
  {
    "fips": "18077",
    "state": "IN",
    "county": "Jefferson"
  },
  {
    "fips": "51117",
    "state": "VA",
    "county": "Mecklenburg"
  },
  {
    "fips": "29186",
    "state": "MO",
    "county": "Ste. Genevieve"
  },
  {
    "fips": "56003",
    "state": "WY",
    "county": "Big Horn"
  },
  {
    "fips": "20069",
    "state": "KS",
    "county": "Gray"
  },
  {
    "fips": "01103",
    "state": "AL",
    "county": "Morgan"
  },
  {
    "fips": "30095",
    "state": "MT",
    "county": "Stillwater"
  },
  {
    "fips": "34035",
    "state": "NJ",
    "county": "Somerset"
  },
  {
    "fips": "21045",
    "state": "KY",
    "county": "Casey"
  },
  {
    "fips": "30089",
    "state": "MT",
    "county": "Sanders"
  },
  {
    "fips": "49051",
    "state": "UT",
    "county": "Wasatch"
  },
  {
    "fips": "30029",
    "state": "MT",
    "county": "Flathead"
  },
  {
    "fips": "12019",
    "state": "FL",
    "county": "Clay"
  },
  {
    "fips": "46045",
    "state": "SD",
    "county": "Edmunds"
  },
  {
    "fips": "54037",
    "state": "WV",
    "county": "Jefferson"
  },
  {
    "fips": "12093",
    "state": "FL",
    "county": "Okeechobee"
  },
  {
    "fips": "39125",
    "state": "OH",
    "county": "Paulding"
  },
  {
    "fips": "53009",
    "state": "WA",
    "county": "Clallam"
  },
  {
    "fips": "20157",
    "state": "KS",
    "county": "Republic"
  },
  {
    "fips": "20011",
    "state": "KS",
    "county": "Bourbon"
  },
  {
    "fips": "13305",
    "state": "GA",
    "county": "Wayne"
  },
  {
    "fips": "34007",
    "state": "NJ",
    "county": "Camden"
  },
  {
    "fips": "37039",
    "state": "NC",
    "county": "Cherokee"
  },
  {
    "fips": "42035",
    "state": "PA",
    "county": "Clinton"
  },
  {
    "fips": "47129",
    "state": "TN",
    "county": "Morgan"
  },
  {
    "fips": "48279",
    "state": "TX",
    "county": "Lamb"
  },
  {
    "fips": "21031",
    "state": "KY",
    "county": "Butler"
  },
  {
    "fips": "19177",
    "state": "IA",
    "county": "Van Buren"
  },
  {
    "fips": "20075",
    "state": "KS",
    "county": "Hamilton"
  },
  {
    "fips": "26117",
    "state": "MI",
    "county": "Montcalm"
  },
  {
    "fips": "31067",
    "state": "NE",
    "county": "Gage"
  },
  {
    "fips": "26111",
    "state": "MI",
    "county": "Midland"
  },
  {
    "fips": "16049",
    "state": "ID",
    "county": "Idaho"
  },
  {
    "fips": "06077",
    "state": "CA",
    "county": "San Joaquin"
  },
  {
    "fips": "26089",
    "state": "MI",
    "county": "Leelanau"
  },
  {
    "fips": "35029",
    "state": "NM",
    "county": "Luna"
  },
  {
    "fips": "20179",
    "state": "KS",
    "county": "Sheridan"
  },
  {
    "fips": "30069",
    "state": "MT",
    "county": "Petroleum"
  },
  {
    "fips": "45061",
    "state": "SC",
    "county": "Lee"
  },
  {
    "fips": "54013",
    "state": "WV",
    "county": "Calhoun"
  },
  {
    "fips": "51167",
    "state": "VA",
    "county": "Russell"
  },
  {
    "fips": "17161",
    "state": "IL",
    "county": "Rock Island"
  },
  {
    "fips": "02185",
    "state": "AK",
    "county": "North Slope"
  },
  {
    "fips": "21097",
    "state": "KY",
    "county": "Harrison"
  },
  {
    "fips": "20039",
    "state": "KS",
    "county": "Decatur"
  },
  {
    "fips": "48417",
    "state": "TX",
    "county": "Shackelford"
  },
  {
    "fips": "46057",
    "state": "SD",
    "county": "Hamlin"
  },
  {
    "fips": "21053",
    "state": "KY",
    "county": "Clinton"
  },
  {
    "fips": "18029",
    "state": "IN",
    "county": "Dearborn"
  },
  {
    "fips": "40127",
    "state": "OK",
    "county": "Pushmataha"
  },
  {
    "fips": "20151",
    "state": "KS",
    "county": "Pratt"
  },
  {
    "fips": "12051",
    "state": "FL",
    "county": "Hendry"
  },
  {
    "fips": "55075",
    "state": "WI",
    "county": "Marinette"
  },
  {
    "fips": "13125",
    "state": "GA",
    "county": "Glascock"
  },
  {
    "fips": "42003",
    "state": "PA",
    "county": "Allegheny"
  },
  {
    "fips": "08077",
    "state": "CO",
    "county": "Mesa"
  },
  {
    "fips": "18043",
    "state": "IN",
    "county": "Floyd"
  },
  {
    "fips": "19041",
    "state": "IA",
    "county": "Clay"
  },
  {
    "fips": "13055",
    "state": "GA",
    "county": "Chattooga"
  },
  {
    "fips": "12049",
    "state": "FL",
    "county": "Hardee"
  },
  {
    "fips": "28095",
    "state": "MS",
    "county": "Monroe"
  },
  {
    "fips": "37079",
    "state": "NC",
    "county": "Greene"
  },
  {
    "fips": "31059",
    "state": "NE",
    "county": "Fillmore"
  },
  {
    "fips": "12031",
    "state": "FL",
    "county": "Duval"
  },
  {
    "fips": "38019",
    "state": "ND",
    "county": "Cavalier"
  },
  {
    "fips": "19143",
    "state": "IA",
    "county": "Osceola"
  },
  {
    "fips": "17079",
    "state": "IL",
    "county": "Jasper"
  },
  {
    "fips": "28029",
    "state": "MS",
    "county": "Copiah"
  },
  {
    "fips": "51135",
    "state": "VA",
    "county": "Nottoway"
  },
  {
    "fips": "20143",
    "state": "KS",
    "county": "Ottawa"
  },
  {
    "fips": "36121",
    "state": "NY",
    "county": "Wyoming"
  },
  {
    "fips": "42029",
    "state": "PA",
    "county": "Chester"
  },
  {
    "fips": "20139",
    "state": "KS",
    "county": "Osage"
  },
  {
    "fips": "48003",
    "state": "TX",
    "county": "Andrews"
  },
  {
    "fips": "29099",
    "state": "MO",
    "county": "Jefferson"
  },
  {
    "fips": "48239",
    "state": "TX",
    "county": "Jackson"
  },
  {
    "fips": "39127",
    "state": "OH",
    "county": "Perry"
  },
  {
    "fips": "36015",
    "state": "NY",
    "county": "Chemung"
  },
  {
    "fips": "55115",
    "state": "WI",
    "county": "Shawano"
  },
  {
    "fips": "18017",
    "state": "IN",
    "county": "Cass"
  },
  {
    "fips": "20177",
    "state": "KS",
    "county": "Shawnee"
  },
  {
    "fips": "22065",
    "state": "LA",
    "county": "Madison"
  },
  {
    "fips": "20051",
    "state": "KS",
    "county": "Ellis"
  },
  {
    "fips": "01009",
    "state": "AL",
    "county": "Blount"
  },
  {
    "fips": "37053",
    "state": "NC",
    "county": "Currituck"
  },
  {
    "fips": "35041",
    "state": "NM",
    "county": "Roosevelt"
  },
  {
    "fips": "48429",
    "state": "TX",
    "county": "Stephens"
  },
  {
    "fips": "38049",
    "state": "ND",
    "county": "McHenry"
  },
  {
    "fips": "21089",
    "state": "KY",
    "county": "Greenup"
  },
  {
    "fips": "31143",
    "state": "NE",
    "county": "Polk"
  },
  {
    "fips": "38017",
    "state": "ND",
    "county": "Cass"
  },
  {
    "fips": "39081",
    "state": "OH",
    "county": "Jefferson"
  },
  {
    "fips": "48043",
    "state": "TX",
    "county": "Brewster"
  },
  {
    "fips": "01045",
    "state": "AL",
    "county": "Dale"
  },
  {
    "fips": "02068",
    "state": "AK",
    "county": "Denali"
  },
  {
    "fips": "30037",
    "state": "MT",
    "county": "Golden Valley"
  },
  {
    "fips": "24009",
    "state": "MD",
    "county": "Calvert"
  },
  {
    "fips": "17067",
    "state": "IL",
    "county": "Hancock"
  },
  {
    "fips": "47079",
    "state": "TN",
    "county": "Henry"
  },
  {
    "fips": "29073",
    "state": "MO",
    "county": "Gasconade"
  },
  {
    "fips": "13117",
    "state": "GA",
    "county": "Forsyth"
  },
  {
    "fips": "32001",
    "state": "NV",
    "county": "Churchill"
  },
  {
    "fips": "13279",
    "state": "GA",
    "county": "Toombs"
  },
  {
    "fips": "28153",
    "state": "MS",
    "county": "Wayne"
  },
  {
    "fips": "28049",
    "state": "MS",
    "county": "Hinds"
  },
  {
    "fips": "26059",
    "state": "MI",
    "county": "Hillsdale"
  },
  {
    "fips": "29101",
    "state": "MO",
    "county": "Johnson"
  },
  {
    "fips": "27129",
    "state": "MN",
    "county": "Renville"
  },
  {
    "fips": "01005",
    "state": "AL",
    "county": "Barbour"
  },
  {
    "fips": "31083",
    "state": "NE",
    "county": "Harlan"
  },
  {
    "fips": "46029",
    "state": "SD",
    "county": "Codington"
  },
  {
    "fips": "28041",
    "state": "MS",
    "county": "Greene"
  },
  {
    "fips": "19007",
    "state": "IA",
    "county": "Appanoose"
  },
  {
    "fips": "09001",
    "state": "CT",
    "county": "Fairfield"
  },
  {
    "fips": "28097",
    "state": "MS",
    "county": "Montgomery"
  },
  {
    "fips": "29153",
    "state": "MO",
    "county": "Ozark"
  },
  {
    "fips": "47149",
    "state": "TN",
    "county": "Rutherford"
  },
  {
    "fips": "51139",
    "state": "VA",
    "county": "Page"
  },
  {
    "fips": "27169",
    "state": "MN",
    "county": "Winona"
  },
  {
    "fips": "21119",
    "state": "KY",
    "county": "Knott"
  },
  {
    "fips": "26157",
    "state": "MI",
    "county": "Tuscola"
  },
  {
    "fips": "54019",
    "state": "WV",
    "county": "Fayette"
  },
  {
    "fips": "12043",
    "state": "FL",
    "county": "Glades"
  },
  {
    "fips": "21173",
    "state": "KY",
    "county": "Montgomery"
  },
  {
    "fips": "16087",
    "state": "ID",
    "county": "Washington"
  },
  {
    "fips": "31097",
    "state": "NE",
    "county": "Johnson"
  },
  {
    "fips": "37021",
    "state": "NC",
    "county": "Buncombe"
  },
  {
    "fips": "46049",
    "state": "SD",
    "county": "Faulk"
  },
  {
    "fips": "13099",
    "state": "GA",
    "county": "Early"
  },
  {
    "fips": "29009",
    "state": "MO",
    "county": "Barry"
  },
  {
    "fips": "26087",
    "state": "MI",
    "county": "Lapeer"
  },
  {
    "fips": "51113",
    "state": "VA",
    "county": "Madison"
  },
  {
    "fips": "01049",
    "state": "AL",
    "county": "DeKalb"
  },
  {
    "fips": "37135",
    "state": "NC",
    "county": "Orange"
  },
  {
    "fips": "06097",
    "state": "CA",
    "county": "Sonoma"
  },
  {
    "fips": "29049",
    "state": "MO",
    "county": "Clinton"
  },
  {
    "fips": "08017",
    "state": "CO",
    "county": "Cheyenne"
  },
  {
    "fips": "19091",
    "state": "IA",
    "county": "Humboldt"
  },
  {
    "fips": "31181",
    "state": "NE",
    "county": "Webster"
  },
  {
    "fips": "49013",
    "state": "UT",
    "county": "Duchesne"
  },
  {
    "fips": "56043",
    "state": "WY",
    "county": "Washakie"
  },
  {
    "fips": "28115",
    "state": "MS",
    "county": "Pontotoc"
  },
  {
    "fips": "01101",
    "state": "AL",
    "county": "Montgomery"
  },
  {
    "fips": "72081",
    "state": "PR",
    "county": "Lares"
  },
  {
    "fips": "19197",
    "state": "IA",
    "county": "Wright"
  },
  {
    "fips": "28069",
    "state": "MS",
    "county": "Kemper"
  },
  {
    "fips": "72103",
    "state": "PR",
    "county": "Naguabo"
  },
  {
    "fips": "13097",
    "state": "GA",
    "county": "Douglas"
  },
  {
    "fips": "27043",
    "state": "MN",
    "county": "Faribault"
  },
  {
    "fips": "26041",
    "state": "MI",
    "county": "Delta"
  },
  {
    "fips": "28135",
    "state": "MS",
    "county": "Tallahatchie"
  },
  {
    "fips": "12127",
    "state": "FL",
    "county": "Volusia"
  },
  {
    "fips": "48221",
    "state": "TX",
    "county": "Hood"
  },
  {
    "fips": "48277",
    "state": "TX",
    "county": "Lamar"
  },
  {
    "fips": "22073",
    "state": "LA",
    "county": "Ouachita"
  },
  {
    "fips": "27119",
    "state": "MN",
    "county": "Polk"
  },
  {
    "fips": "35043",
    "state": "NM",
    "county": "Sandoval"
  },
  {
    "fips": "21191",
    "state": "KY",
    "county": "Pendleton"
  },
  {
    "fips": "54053",
    "state": "WV",
    "county": "Mason"
  },
  {
    "fips": "19139",
    "state": "IA",
    "county": "Muscatine"
  },
  {
    "fips": "01129",
    "state": "AL",
    "county": "Washington"
  },
  {
    "fips": "47101",
    "state": "TN",
    "county": "Lewis"
  },
  {
    "fips": "08125",
    "state": "CO",
    "county": "Yuma"
  },
  {
    "fips": "13089",
    "state": "GA",
    "county": "DeKalb"
  },
  {
    "fips": "33013",
    "state": "NH",
    "county": "Merrimack"
  },
  {
    "fips": "18149",
    "state": "IN",
    "county": "Starke"
  },
  {
    "fips": "12033",
    "state": "FL",
    "county": "Escambia"
  },
  {
    "fips": "37029",
    "state": "NC",
    "county": "Camden"
  },
  {
    "fips": "12003",
    "state": "FL",
    "county": "Baker"
  },
  {
    "fips": "37193",
    "state": "NC",
    "county": "Wilkes"
  },
  {
    "fips": "22111",
    "state": "LA",
    "county": "Union"
  },
  {
    "fips": "13029",
    "state": "GA",
    "county": "Bryan"
  },
  {
    "fips": "72059",
    "state": "PR",
    "county": "Guayanilla"
  },
  {
    "fips": "16057",
    "state": "ID",
    "county": "Latah"
  },
  {
    "fips": "08045",
    "state": "CO",
    "county": "Garfield"
  },
  {
    "fips": "19113",
    "state": "IA",
    "county": "Linn"
  },
  {
    "fips": "19121",
    "state": "IA",
    "county": "Madison"
  },
  {
    "fips": "45083",
    "state": "SC",
    "county": "Spartanburg"
  },
  {
    "fips": "54073",
    "state": "WV",
    "county": "Pleasants"
  },
  {
    "fips": "17125",
    "state": "IL",
    "county": "Mason"
  },
  {
    "fips": "50009",
    "state": "VT",
    "county": "Essex"
  },
  {
    "fips": "29111",
    "state": "MO",
    "county": "Lewis"
  },
  {
    "fips": "42063",
    "state": "PA",
    "county": "Indiana"
  },
  {
    "fips": "51137",
    "state": "VA",
    "county": "Orange"
  },
  {
    "fips": "46099",
    "state": "SD",
    "county": "Minnehaha"
  },
  {
    "fips": "47019",
    "state": "TN",
    "county": "Carter"
  },
  {
    "fips": "19195",
    "state": "IA",
    "county": "Worth"
  },
  {
    "fips": "48147",
    "state": "TX",
    "county": "Fannin"
  },
  {
    "fips": "19075",
    "state": "IA",
    "county": "Grundy"
  },
  {
    "fips": "51079",
    "state": "VA",
    "county": "Greene"
  },
  {
    "fips": "39063",
    "state": "OH",
    "county": "Hancock"
  },
  {
    "fips": "17081",
    "state": "IL",
    "county": "Jefferson"
  },
  {
    "fips": "53013",
    "state": "WA",
    "county": "Columbia"
  },
  {
    "fips": "45003",
    "state": "SC",
    "county": "Aiken"
  },
  {
    "fips": "48253",
    "state": "TX",
    "county": "Jones"
  },
  {
    "fips": "53039",
    "state": "WA",
    "county": "Klickitat"
  },
  {
    "fips": "41019",
    "state": "OR",
    "county": "Douglas"
  },
  {
    "fips": "21127",
    "state": "KY",
    "county": "Lawrence"
  },
  {
    "fips": "30021",
    "state": "MT",
    "county": "Dawson"
  },
  {
    "fips": "37191",
    "state": "NC",
    "county": "Wayne"
  },
  {
    "fips": "42125",
    "state": "PA",
    "county": "Washington"
  },
  {
    "fips": "39163",
    "state": "OH",
    "county": "Vinton"
  },
  {
    "fips": "31009",
    "state": "NE",
    "county": "Blaine"
  },
  {
    "fips": "18085",
    "state": "IN",
    "county": "Kosciusko"
  },
  {
    "fips": "17127",
    "state": "IL",
    "county": "Massac"
  },
  {
    "fips": "17071",
    "state": "IL",
    "county": "Henderson"
  },
  {
    "fips": "21179",
    "state": "KY",
    "county": "Nelson"
  },
  {
    "fips": "40013",
    "state": "OK",
    "county": "Bryan"
  },
  {
    "fips": "54061",
    "state": "WV",
    "county": "Monongalia"
  },
  {
    "fips": "08039",
    "state": "CO",
    "county": "Elbert"
  },
  {
    "fips": "10001",
    "state": "DE",
    "county": "Kent"
  },
  {
    "fips": "54059",
    "state": "WV",
    "county": "Mingo"
  },
  {
    "fips": "18173",
    "state": "IN",
    "county": "Warrick"
  },
  {
    "fips": "51081",
    "state": "VA",
    "county": "Greensville"
  },
  {
    "fips": "13233",
    "state": "GA",
    "county": "Polk"
  },
  {
    "fips": "51191",
    "state": "VA",
    "county": "Washington"
  },
  {
    "fips": "18079",
    "state": "IN",
    "county": "Jennings"
  },
  {
    "fips": "49027",
    "state": "UT",
    "county": "Millard"
  },
  {
    "fips": "13285",
    "state": "GA",
    "county": "Troup"
  },
  {
    "fips": "12015",
    "state": "FL",
    "county": "Charlotte"
  },
  {
    "fips": "05035",
    "state": "AR",
    "county": "Crittenden"
  },
  {
    "fips": "48129",
    "state": "TX",
    "county": "Donley"
  },
  {
    "fips": "38103",
    "state": "ND",
    "county": "Wells"
  },
  {
    "fips": "29143",
    "state": "MO",
    "county": "New Madrid"
  },
  {
    "fips": "05121",
    "state": "AR",
    "county": "Randolph"
  },
  {
    "fips": "30007",
    "state": "MT",
    "county": "Broadwater"
  },
  {
    "fips": "55033",
    "state": "WI",
    "county": "Dunn"
  },
  {
    "fips": "20119",
    "state": "KS",
    "county": "Meade"
  },
  {
    "fips": "51199",
    "state": "VA",
    "county": "York"
  },
  {
    "fips": "17163",
    "state": "IL",
    "county": "St. Clair"
  },
  {
    "fips": "54103",
    "state": "WV",
    "county": "Wetzel"
  },
  {
    "fips": "40003",
    "state": "OK",
    "county": "Alfalfa"
  },
  {
    "fips": "22097",
    "state": "LA",
    "county": "St. Landry"
  },
  {
    "fips": "37117",
    "state": "NC",
    "county": "Martin"
  },
  {
    "fips": "21195",
    "state": "KY",
    "county": "Pike"
  },
  {
    "fips": "20131",
    "state": "KS",
    "county": "Nemaha"
  },
  {
    "fips": "44007",
    "state": "RI",
    "county": "Providence"
  },
  {
    "fips": "21199",
    "state": "KY",
    "county": "Pulaski"
  },
  {
    "fips": "19189",
    "state": "IA",
    "county": "Winnebago"
  },
  {
    "fips": "51007",
    "state": "VA",
    "county": "Amelia"
  },
  {
    "fips": "55017",
    "state": "WI",
    "county": "Chippewa"
  },
  {
    "fips": "39113",
    "state": "OH",
    "county": "Montgomery"
  },
  {
    "fips": "36009",
    "state": "NY",
    "county": "Cattaraugus"
  },
  {
    "fips": "45077",
    "state": "SC",
    "county": "Pickens"
  },
  {
    "fips": "04027",
    "state": "AZ",
    "county": "Yuma"
  },
  {
    "fips": "48137",
    "state": "TX",
    "county": "Edwards"
  },
  {
    "fips": "28017",
    "state": "MS",
    "county": "Chickasaw"
  },
  {
    "fips": "08087",
    "state": "CO",
    "county": "Morgan"
  },
  {
    "fips": "40113",
    "state": "OK",
    "county": "Osage"
  },
  {
    "fips": "22123",
    "state": "LA",
    "county": "West Carroll"
  },
  {
    "fips": "72015",
    "state": "PR",
    "county": "Arroyo"
  },
  {
    "fips": "48073",
    "state": "TX",
    "county": "Cherokee"
  },
  {
    "fips": "48177",
    "state": "TX",
    "county": "Gonzales"
  },
  {
    "fips": "20097",
    "state": "KS",
    "county": "Kiowa"
  },
  {
    "fips": "29185",
    "state": "MO",
    "county": "St. Clair"
  },
  {
    "fips": "50011",
    "state": "VT",
    "county": "Franklin"
  },
  {
    "fips": "51099",
    "state": "VA",
    "county": "King George"
  },
  {
    "fips": "29043",
    "state": "MO",
    "county": "Christian"
  },
  {
    "fips": "20001",
    "state": "KS",
    "county": "Allen"
  },
  {
    "fips": "29107",
    "state": "MO",
    "county": "Lafayette"
  },
  {
    "fips": "04012",
    "state": "AZ",
    "county": "La Paz"
  },
  {
    "fips": "15005",
    "state": "HI",
    "county": "Kalawao"
  },
  {
    "fips": "17035",
    "state": "IL",
    "county": "Cumberland"
  },
  {
    "fips": "16067",
    "state": "ID",
    "county": "Minidoka"
  },
  {
    "fips": "78010",
    "state": "VI",
    "county": "St. Croix"
  },
  {
    "fips": "48183",
    "state": "TX",
    "county": "Gregg"
  },
  {
    "fips": "28047",
    "state": "MS",
    "county": "Harrison"
  },
  {
    "fips": "18109",
    "state": "IN",
    "county": "Morgan"
  },
  {
    "fips": "32023",
    "state": "NV",
    "county": "Nye"
  },
  {
    "fips": "27019",
    "state": "MN",
    "county": "Carver"
  },
  {
    "fips": "13085",
    "state": "GA",
    "county": "Dawson"
  },
  {
    "fips": "37077",
    "state": "NC",
    "county": "Granville"
  },
  {
    "fips": "78030",
    "state": "VI",
    "county": "St. Thomas"
  },
  {
    "fips": "37067",
    "state": "NC",
    "county": "Forsyth"
  },
  {
    "fips": "16041",
    "state": "ID",
    "county": "Franklin"
  },
  {
    "fips": "27143",
    "state": "MN",
    "county": "Sibley"
  },
  {
    "fips": "42099",
    "state": "PA",
    "county": "Perry"
  },
  {
    "fips": "47043",
    "state": "TN",
    "county": "Dickson"
  },
  {
    "fips": "17117",
    "state": "IL",
    "county": "Macoupin"
  },
  {
    "fips": "54075",
    "state": "WV",
    "county": "Pocahontas"
  },
  {
    "fips": "38077",
    "state": "ND",
    "county": "Richland"
  },
  {
    "fips": "53037",
    "state": "WA",
    "county": "Kittitas"
  },
  {
    "fips": "38033",
    "state": "ND",
    "county": "Golden Valley"
  },
  {
    "fips": "13319",
    "state": "GA",
    "county": "Wilkinson"
  },
  {
    "fips": "18061",
    "state": "IN",
    "county": "Harrison"
  },
  {
    "fips": "17183",
    "state": "IL",
    "county": "Vermilion"
  },
  {
    "fips": "31069",
    "state": "NE",
    "county": "Garden"
  },
  {
    "fips": "22115",
    "state": "LA",
    "county": "Vernon"
  },
  {
    "fips": "47095",
    "state": "TN",
    "county": "Lake"
  },
  {
    "fips": "37003",
    "state": "NC",
    "county": "Alexander"
  },
  {
    "fips": "45075",
    "state": "SC",
    "county": "Orangeburg"
  },
  {
    "fips": "48179",
    "state": "TX",
    "county": "Gray"
  },
  {
    "fips": "31113",
    "state": "NE",
    "county": "Logan"
  },
  {
    "fips": "20195",
    "state": "KS",
    "county": "Trego"
  },
  {
    "fips": "08031",
    "state": "CO",
    "county": "Denver"
  },
  {
    "fips": "35006",
    "state": "NM",
    "county": "Cibola"
  },
  {
    "fips": "42011",
    "state": "PA",
    "county": "Berks"
  },
  {
    "fips": "05057",
    "state": "AR",
    "county": "Hempstead"
  },
  {
    "fips": "20149",
    "state": "KS",
    "county": "Pottawatomie"
  },
  {
    "fips": "19067",
    "state": "IA",
    "county": "Floyd"
  },
  {
    "fips": "21177",
    "state": "KY",
    "county": "Muhlenberg"
  },
  {
    "fips": "13027",
    "state": "GA",
    "county": "Brooks"
  },
  {
    "fips": "24045",
    "state": "MD",
    "county": "Wicomico"
  },
  {
    "fips": "27135",
    "state": "MN",
    "county": "Roseau"
  },
  {
    "fips": "31105",
    "state": "NE",
    "county": "Kimball"
  },
  {
    "fips": "08091",
    "state": "CO",
    "county": "Ouray"
  },
  {
    "fips": "55049",
    "state": "WI",
    "county": "Iowa"
  },
  {
    "fips": "48265",
    "state": "TX",
    "county": "Kerr"
  },
  {
    "fips": "36115",
    "state": "NY",
    "county": "Washington"
  },
  {
    "fips": "27015",
    "state": "MN",
    "county": "Brown"
  },
  {
    "fips": "45009",
    "state": "SC",
    "county": "Bamberg"
  },
  {
    "fips": "48337",
    "state": "TX",
    "county": "Montague"
  },
  {
    "fips": "72063",
    "state": "PR",
    "county": "Gurabo"
  },
  {
    "fips": "21161",
    "state": "KY",
    "county": "Mason"
  },
  {
    "fips": "26065",
    "state": "MI",
    "county": "Ingham"
  },
  {
    "fips": "30075",
    "state": "MT",
    "county": "Powder River"
  },
  {
    "fips": "72101",
    "state": "PR",
    "county": "Morovis"
  },
  {
    "fips": "35028",
    "state": "NM",
    "county": "Los Alamos"
  },
  {
    "fips": "13093",
    "state": "GA",
    "county": "Dooly"
  },
  {
    "fips": "06115",
    "state": "CA",
    "county": "Yuba"
  },
  {
    "fips": "55047",
    "state": "WI",
    "county": "Green Lake"
  },
  {
    "fips": "55109",
    "state": "WI",
    "county": "St. Croix"
  },
  {
    "fips": "17059",
    "state": "IL",
    "county": "Gallatin"
  },
  {
    "fips": "19153",
    "state": "IA",
    "county": "Polk"
  },
  {
    "fips": "36061",
    "state": "NY",
    "county": "New York"
  },
  {
    "fips": "48307",
    "state": "TX",
    "county": "McCulloch"
  },
  {
    "fips": "38023",
    "state": "ND",
    "county": "Divide"
  },
  {
    "fips": "47091",
    "state": "TN",
    "county": "Johnson"
  },
  {
    "fips": "01011",
    "state": "AL",
    "county": "Bullock"
  },
  {
    "fips": "22049",
    "state": "LA",
    "county": "Jackson"
  },
  {
    "fips": "47005",
    "state": "TN",
    "county": "Benton"
  },
  {
    "fips": "48293",
    "state": "TX",
    "county": "Limestone"
  },
  {
    "fips": "55007",
    "state": "WI",
    "county": "Bayfield"
  },
  {
    "fips": "42107",
    "state": "PA",
    "county": "Schuylkill"
  },
  {
    "fips": "48413",
    "state": "TX",
    "county": "Schleicher"
  },
  {
    "fips": "30083",
    "state": "MT",
    "county": "Richland"
  },
  {
    "fips": "05141",
    "state": "AR",
    "county": "Van Buren"
  },
  {
    "fips": "13223",
    "state": "GA",
    "county": "Paulding"
  },
  {
    "fips": "21225",
    "state": "KY",
    "county": "Union"
  },
  {
    "fips": "37181",
    "state": "NC",
    "county": "Vance"
  },
  {
    "fips": "27167",
    "state": "MN",
    "county": "Wilkin"
  },
  {
    "fips": "48169",
    "state": "TX",
    "county": "Garza"
  },
  {
    "fips": "20159",
    "state": "KS",
    "county": "Rice"
  },
  {
    "fips": "27107",
    "state": "MN",
    "county": "Norman"
  },
  {
    "fips": "51730",
    "state": "VA",
    "county": "Petersburg"
  },
  {
    "fips": "08109",
    "state": "CO",
    "county": "Saguache"
  },
  {
    "fips": "41067",
    "state": "OR",
    "county": "Washington"
  },
  {
    "fips": "19127",
    "state": "IA",
    "county": "Marshall"
  },
  {
    "fips": "18167",
    "state": "IN",
    "county": "Vigo"
  },
  {
    "fips": "31157",
    "state": "NE",
    "county": "Scotts Bluff"
  },
  {
    "fips": "24043",
    "state": "MD",
    "county": "Washington"
  },
  {
    "fips": "27025",
    "state": "MN",
    "county": "Chisago"
  },
  {
    "fips": "28071",
    "state": "MS",
    "county": "Lafayette"
  },
  {
    "fips": "17089",
    "state": "IL",
    "county": "Kane"
  },
  {
    "fips": "47123",
    "state": "TN",
    "county": "Monroe"
  },
  {
    "fips": "72003",
    "state": "PR",
    "county": "Aguada"
  },
  {
    "fips": "06067",
    "state": "CA",
    "county": "Sacramento"
  },
  {
    "fips": "42045",
    "state": "PA",
    "county": "Delaware"
  },
  {
    "fips": "16047",
    "state": "ID",
    "county": "Gooding"
  },
  {
    "fips": "41059",
    "state": "OR",
    "county": "Umatilla"
  },
  {
    "fips": "48145",
    "state": "TX",
    "county": "Falls"
  },
  {
    "fips": "01013",
    "state": "AL",
    "county": "Butler"
  },
  {
    "fips": "48101",
    "state": "TX",
    "county": "Cottle"
  },
  {
    "fips": "42067",
    "state": "PA",
    "county": "Juniata"
  },
  {
    "fips": "55071",
    "state": "WI",
    "county": "Manitowoc"
  },
  {
    "fips": "18129",
    "state": "IN",
    "county": "Posey"
  },
  {
    "fips": "12069",
    "state": "FL",
    "county": "Lake"
  },
  {
    "fips": "13283",
    "state": "GA",
    "county": "Treutlen"
  },
  {
    "fips": "17051",
    "state": "IL",
    "county": "Fayette"
  },
  {
    "fips": "05065",
    "state": "AR",
    "county": "Izard"
  },
  {
    "fips": "48113",
    "state": "TX",
    "county": "Dallas"
  },
  {
    "fips": "51003",
    "state": "VA",
    "county": "Albemarle"
  },
  {
    "fips": "08059",
    "state": "CO",
    "county": "Jefferson"
  },
  {
    "fips": "39173",
    "state": "OH",
    "county": "Wood"
  },
  {
    "fips": "20105",
    "state": "KS",
    "county": "Lincoln"
  },
  {
    "fips": "46063",
    "state": "SD",
    "county": "Harding"
  },
  {
    "fips": "47067",
    "state": "TN",
    "county": "Hancock"
  },
  {
    "fips": "27037",
    "state": "MN",
    "county": "Dakota"
  },
  {
    "fips": "47065",
    "state": "TN",
    "county": "Hamilton"
  },
  {
    "fips": "54049",
    "state": "WV",
    "county": "Marion"
  },
  {
    "fips": "72123",
    "state": "PR",
    "county": "Salinas"
  },
  {
    "fips": "41023",
    "state": "OR",
    "county": "Grant"
  },
  {
    "fips": "51680",
    "state": "VA",
    "county": "Lynchburg"
  },
  {
    "fips": "72133",
    "state": "PR",
    "county": "Santa Isabel"
  },
  {
    "fips": "13193",
    "state": "GA",
    "county": "Macon"
  },
  {
    "fips": "28007",
    "state": "MS",
    "county": "Attala"
  },
  {
    "fips": "21051",
    "state": "KY",
    "county": "Clay"
  },
  {
    "fips": "28025",
    "state": "MS",
    "county": "Clay"
  },
  {
    "fips": "29213",
    "state": "MO",
    "county": "Taney"
  },
  {
    "fips": "13265",
    "state": "GA",
    "county": "Taliaferro"
  },
  {
    "fips": "19191",
    "state": "IA",
    "county": "Winneshiek"
  },
  {
    "fips": "40151",
    "state": "OK",
    "county": "Woods"
  },
  {
    "fips": "45047",
    "state": "SC",
    "county": "Greenwood"
  },
  {
    "fips": "42047",
    "state": "PA",
    "county": "Elk"
  },
  {
    "fips": "12097",
    "state": "FL",
    "county": "Osceola"
  },
  {
    "fips": "18177",
    "state": "IN",
    "county": "Wayne"
  },
  {
    "fips": "47089",
    "state": "TN",
    "county": "Jefferson"
  },
  {
    "fips": "22119",
    "state": "LA",
    "county": "Webster"
  },
  {
    "fips": "08049",
    "state": "CO",
    "county": "Grand"
  },
  {
    "fips": "18121",
    "state": "IN",
    "county": "Parke"
  },
  {
    "fips": "05103",
    "state": "AR",
    "county": "Ouachita"
  },
  {
    "fips": "13103",
    "state": "GA",
    "county": "Effingham"
  },
  {
    "fips": "19053",
    "state": "IA",
    "county": "Decatur"
  },
  {
    "fips": "26149",
    "state": "MI",
    "county": "St. Joseph"
  },
  {
    "fips": "39015",
    "state": "OH",
    "county": "Brown"
  },
  {
    "fips": "46081",
    "state": "SD",
    "county": "Lawrence"
  },
  {
    "fips": "48263",
    "state": "TX",
    "county": "Kent"
  },
  {
    "fips": "55077",
    "state": "WI",
    "county": "Marquette"
  },
  {
    "fips": "22011",
    "state": "LA",
    "county": "Beauregard"
  },
  {
    "fips": "51133",
    "state": "VA",
    "county": "Northumberland"
  },
  {
    "fips": "20163",
    "state": "KS",
    "county": "Rooks"
  },
  {
    "fips": "20111",
    "state": "KS",
    "county": "Lyon"
  },
  {
    "fips": "47141",
    "state": "TN",
    "county": "Putnam"
  },
  {
    "fips": "12063",
    "state": "FL",
    "county": "Jackson"
  },
  {
    "fips": "37007",
    "state": "NC",
    "county": "Anson"
  },
  {
    "fips": "26003",
    "state": "MI",
    "county": "Alger"
  },
  {
    "fips": "32029",
    "state": "NV",
    "county": "Storey"
  },
  {
    "fips": "29031",
    "state": "MO",
    "county": "Cape Girardeau"
  },
  {
    "fips": "29125",
    "state": "MO",
    "county": "Maries"
  },
  {
    "fips": "50023",
    "state": "VT",
    "county": "Washington"
  },
  {
    "fips": "13091",
    "state": "GA",
    "county": "Dodge"
  },
  {
    "fips": "46015",
    "state": "SD",
    "county": "Brule"
  },
  {
    "fips": "46105",
    "state": "SD",
    "county": "Perkins"
  },
  {
    "fips": "42091",
    "state": "PA",
    "county": "Montgomery"
  },
  {
    "fips": "41029",
    "state": "OR",
    "county": "Jackson"
  },
  {
    "fips": "36043",
    "state": "NY",
    "county": "Herkimer"
  },
  {
    "fips": "47073",
    "state": "TN",
    "county": "Hawkins"
  },
  {
    "fips": "12045",
    "state": "FL",
    "county": "Gulf"
  },
  {
    "fips": "31075",
    "state": "NE",
    "county": "Grant"
  },
  {
    "fips": "19171",
    "state": "IA",
    "county": "Tama"
  },
  {
    "fips": "21015",
    "state": "KY",
    "county": "Boone"
  },
  {
    "fips": "08075",
    "state": "CO",
    "county": "Logan"
  },
  {
    "fips": "45069",
    "state": "SC",
    "county": "Marlboro"
  },
  {
    "fips": "13189",
    "state": "GA",
    "county": "McDuffie"
  },
  {
    "fips": "36111",
    "state": "NY",
    "county": "Ulster"
  },
  {
    "fips": "27067",
    "state": "MN",
    "county": "Kandiyohi"
  },
  {
    "fips": "47139",
    "state": "TN",
    "county": "Polk"
  },
  {
    "fips": "48359",
    "state": "TX",
    "county": "Oldham"
  },
  {
    "fips": "54005",
    "state": "WV",
    "county": "Boone"
  },
  {
    "fips": "31087",
    "state": "NE",
    "county": "Hitchcock"
  },
  {
    "fips": "51678",
    "state": "VA",
    "county": "Lexington"
  },
  {
    "fips": "48067",
    "state": "TX",
    "county": "Cass"
  },
  {
    "fips": "01015",
    "state": "AL",
    "county": "Calhoun"
  },
  {
    "fips": "23009",
    "state": "ME",
    "county": "Hancock"
  },
  {
    "fips": "28005",
    "state": "MS",
    "county": "Amite"
  },
  {
    "fips": "47135",
    "state": "TN",
    "county": "Perry"
  },
  {
    "fips": "48007",
    "state": "TX",
    "county": "Aransas"
  },
  {
    "fips": "30049",
    "state": "MT",
    "county": "Lewis and Clark"
  },
  {
    "fips": "23011",
    "state": "ME",
    "county": "Kennebec"
  },
  {
    "fips": "46093",
    "state": "SD",
    "county": "Meade"
  },
  {
    "fips": "21155",
    "state": "KY",
    "county": "Marion"
  },
  {
    "fips": "46073",
    "state": "SD",
    "county": "Jerauld"
  },
  {
    "fips": "47071",
    "state": "TN",
    "county": "Hardin"
  },
  {
    "fips": "27013",
    "state": "MN",
    "county": "Blue Earth"
  },
  {
    "fips": "13243",
    "state": "GA",
    "county": "Randolph"
  },
  {
    "fips": "29037",
    "state": "MO",
    "county": "Cass"
  },
  {
    "fips": "18125",
    "state": "IN",
    "county": "Pike"
  },
  {
    "fips": "21121",
    "state": "KY",
    "county": "Knox"
  },
  {
    "fips": "40025",
    "state": "OK",
    "county": "Cimarron"
  },
  {
    "fips": "18105",
    "state": "IN",
    "county": "Monroe"
  },
  {
    "fips": "41065",
    "state": "OR",
    "county": "Wasco"
  },
  {
    "fips": "31085",
    "state": "NE",
    "county": "Hayes"
  },
  {
    "fips": "08093",
    "state": "CO",
    "county": "Park"
  },
  {
    "fips": "15009",
    "state": "HI",
    "county": "Maui"
  },
  {
    "fips": "53007",
    "state": "WA",
    "county": "Chelan"
  },
  {
    "fips": "31061",
    "state": "NE",
    "county": "Franklin"
  },
  {
    "fips": "37139",
    "state": "NC",
    "county": "Pasquotank"
  },
  {
    "fips": "02220",
    "state": "AK",
    "county": "Sitka"
  },
  {
    "fips": "48033",
    "state": "TX",
    "county": "Borden"
  },
  {
    "fips": "13245",
    "state": "GA",
    "county": "Richmond"
  },
  {
    "fips": "08115",
    "state": "CO",
    "county": "Sedgwick"
  },
  {
    "fips": "40027",
    "state": "OK",
    "county": "Cleveland"
  },
  {
    "fips": "13257",
    "state": "GA",
    "county": "Stephens"
  },
  {
    "fips": "05027",
    "state": "AR",
    "county": "Columbia"
  },
  {
    "fips": "22015",
    "state": "LA",
    "county": "Bossier"
  },
  {
    "fips": "39167",
    "state": "OH",
    "county": "Washington"
  },
  {
    "fips": "51019",
    "state": "VA",
    "county": "Bedford"
  },
  {
    "fips": "51131",
    "state": "VA",
    "county": "Northampton"
  },
  {
    "fips": "55123",
    "state": "WI",
    "county": "Vernon"
  },
  {
    "fips": "51077",
    "state": "VA",
    "county": "Grayson"
  },
  {
    "fips": "01055",
    "state": "AL",
    "county": "Etowah"
  },
  {
    "fips": "20145",
    "state": "KS",
    "county": "Pawnee"
  },
  {
    "fips": "42001",
    "state": "PA",
    "county": "Adams"
  },
  {
    "fips": "19119",
    "state": "IA",
    "county": "Lyon"
  },
  {
    "fips": "39011",
    "state": "OH",
    "county": "Auglaize"
  },
  {
    "fips": "54089",
    "state": "WV",
    "county": "Summers"
  },
  {
    "fips": "29133",
    "state": "MO",
    "county": "Mississippi"
  },
  {
    "fips": "51029",
    "state": "VA",
    "county": "Buckingham"
  },
  {
    "fips": "02282",
    "state": "AK",
    "county": "Yakutat"
  },
  {
    "fips": "19013",
    "state": "IA",
    "county": "Black Hawk"
  },
  {
    "fips": "12105",
    "state": "FL",
    "county": "Polk"
  },
  {
    "fips": "06087",
    "state": "CA",
    "county": "Santa Cruz"
  },
  {
    "fips": "55133",
    "state": "WI",
    "county": "Waukesha"
  },
  {
    "fips": "40015",
    "state": "OK",
    "county": "Caddo"
  },
  {
    "fips": "06079",
    "state": "CA",
    "county": "San Luis Obispo"
  },
  {
    "fips": "29141",
    "state": "MO",
    "county": "Morgan"
  },
  {
    "fips": "51061",
    "state": "VA",
    "county": "Fauquier"
  },
  {
    "fips": "13183",
    "state": "GA",
    "county": "Long"
  },
  {
    "fips": "21033",
    "state": "KY",
    "county": "Caldwell"
  },
  {
    "fips": "51143",
    "state": "VA",
    "county": "Pittsylvania"
  },
  {
    "fips": "51790",
    "state": "VA",
    "county": "Staunton"
  },
  {
    "fips": "42131",
    "state": "PA",
    "county": "Wyoming"
  },
  {
    "fips": "42019",
    "state": "PA",
    "county": "Butler"
  },
  {
    "fips": "01113",
    "state": "AL",
    "county": "Russell"
  },
  {
    "fips": "21085",
    "state": "KY",
    "county": "Grayson"
  },
  {
    "fips": "47181",
    "state": "TN",
    "county": "Wayne"
  },
  {
    "fips": "02240",
    "state": "AK",
    "county": "Southeast Fairbanks"
  },
  {
    "fips": "17041",
    "state": "IL",
    "county": "Douglas"
  },
  {
    "fips": "31093",
    "state": "NE",
    "county": "Howard"
  },
  {
    "fips": "33007",
    "state": "NH",
    "county": "Coos"
  },
  {
    "fips": "17187",
    "state": "IL",
    "county": "Warren"
  },
  {
    "fips": "36025",
    "state": "NY",
    "county": "Delaware"
  },
  {
    "fips": "39119",
    "state": "OH",
    "county": "Muskingum"
  },
  {
    "fips": "21203",
    "state": "KY",
    "county": "Rockcastle"
  },
  {
    "fips": "20007",
    "state": "KS",
    "county": "Barber"
  },
  {
    "fips": "29127",
    "state": "MO",
    "county": "Marion"
  },
  {
    "fips": "37187",
    "state": "NC",
    "county": "Washington"
  },
  {
    "fips": "72085",
    "state": "PR",
    "county": "Las Piedras"
  },
  {
    "fips": "27017",
    "state": "MN",
    "county": "Carlton"
  },
  {
    "fips": "06011",
    "state": "CA",
    "county": "Colusa"
  },
  {
    "fips": "36039",
    "state": "NY",
    "county": "Greene"
  },
  {
    "fips": "12009",
    "state": "FL",
    "county": "Brevard"
  },
  {
    "fips": "46011",
    "state": "SD",
    "county": "Brookings"
  },
  {
    "fips": "41015",
    "state": "OR",
    "county": "Curry"
  },
  {
    "fips": "19081",
    "state": "IA",
    "county": "Hancock"
  },
  {
    "fips": "53049",
    "state": "WA",
    "county": "Pacific"
  },
  {
    "fips": "24023",
    "state": "MD",
    "county": "Garrett"
  },
  {
    "fips": "29189",
    "state": "MO",
    "county": "St. Louis"
  },
  {
    "fips": "48381",
    "state": "TX",
    "county": "Randall"
  },
  {
    "fips": "22025",
    "state": "LA",
    "county": "Catahoula"
  },
  {
    "fips": "08011",
    "state": "CO",
    "county": "Bent"
  },
  {
    "fips": "11001",
    "state": "DC",
    "county": "District of Columbia"
  },
  {
    "fips": "28067",
    "state": "MS",
    "county": "Jones"
  },
  {
    "fips": "29109",
    "state": "MO",
    "county": "Lawrence"
  },
  {
    "fips": "08081",
    "state": "CO",
    "county": "Moffat"
  },
  {
    "fips": "27089",
    "state": "MN",
    "county": "Marshall"
  },
  {
    "fips": "28105",
    "state": "MS",
    "county": "Oktibbeha"
  },
  {
    "fips": "47151",
    "state": "TN",
    "county": "Scott"
  },
  {
    "fips": "55065",
    "state": "WI",
    "county": "Lafayette"
  },
  {
    "fips": "40089",
    "state": "OK",
    "county": "McCurtain"
  },
  {
    "fips": "26033",
    "state": "MI",
    "county": "Chippewa"
  },
  {
    "fips": "48267",
    "state": "TX",
    "county": "Kimble"
  },
  {
    "fips": "42103",
    "state": "PA",
    "county": "Pike"
  },
  {
    "fips": "51740",
    "state": "VA",
    "county": "Portsmouth"
  },
  {
    "fips": "19155",
    "state": "IA",
    "county": "Pottawattamie"
  },
  {
    "fips": "26085",
    "state": "MI",
    "county": "Lake"
  },
  {
    "fips": "48503",
    "state": "TX",
    "county": "Young"
  },
  {
    "fips": "48195",
    "state": "TX",
    "county": "Hansford"
  },
  {
    "fips": "40041",
    "state": "OK",
    "county": "Delaware"
  },
  {
    "fips": "02261",
    "state": "AK",
    "county": "Valdez-Cordova"
  },
  {
    "fips": "55119",
    "state": "WI",
    "county": "Taylor"
  },
  {
    "fips": "21213",
    "state": "KY",
    "county": "Simpson"
  },
  {
    "fips": "17155",
    "state": "IL",
    "county": "Putnam"
  },
  {
    "fips": "05083",
    "state": "AR",
    "county": "Logan"
  },
  {
    "fips": "12013",
    "state": "FL",
    "county": "Calhoun"
  },
  {
    "fips": "29105",
    "state": "MO",
    "county": "Laclede"
  },
  {
    "fips": "36073",
    "state": "NY",
    "county": "Orleans"
  },
  {
    "fips": "39095",
    "state": "OH",
    "county": "Lucas"
  },
  {
    "fips": "47085",
    "state": "TN",
    "county": "Humphreys"
  },
  {
    "fips": "28101",
    "state": "MS",
    "county": "Newton"
  },
  {
    "fips": "39017",
    "state": "OH",
    "county": "Butler"
  },
  {
    "fips": "06029",
    "state": "CA",
    "county": "Kern"
  },
  {
    "fips": "60050",
    "state": "AS",
    "county": "Western"
  },
  {
    "fips": "45043",
    "state": "SC",
    "county": "Georgetown"
  },
  {
    "fips": "29063",
    "state": "MO",
    "county": "DeKalb"
  },
  {
    "fips": "35061",
    "state": "NM",
    "county": "Valencia"
  },
  {
    "fips": "55101",
    "state": "WI",
    "county": "Racine"
  },
  {
    "fips": "21169",
    "state": "KY",
    "county": "Metcalfe"
  },
  {
    "fips": "29097",
    "state": "MO",
    "county": "Jasper"
  },
  {
    "fips": "16079",
    "state": "ID",
    "county": "Shoshone"
  },
  {
    "fips": "39057",
    "state": "OH",
    "county": "Greene"
  },
  {
    "fips": "21227",
    "state": "KY",
    "county": "Warren"
  },
  {
    "fips": "51610",
    "state": "VA",
    "county": "Falls Church"
  },
  {
    "fips": "49001",
    "state": "UT",
    "county": "Beaver"
  },
  {
    "fips": "08023",
    "state": "CO",
    "county": "Costilla"
  },
  {
    "fips": "28027",
    "state": "MS",
    "county": "Coahoma"
  },
  {
    "fips": "29137",
    "state": "MO",
    "county": "Monroe"
  },
  {
    "fips": "39097",
    "state": "OH",
    "county": "Madison"
  },
  {
    "fips": "22027",
    "state": "LA",
    "county": "Claiborne"
  },
  {
    "fips": "26091",
    "state": "MI",
    "county": "Lenawee"
  },
  {
    "fips": "29069",
    "state": "MO",
    "county": "Dunklin"
  },
  {
    "fips": "05051",
    "state": "AR",
    "county": "Garland"
  },
  {
    "fips": "47187",
    "state": "TN",
    "county": "Williamson"
  },
  {
    "fips": "28119",
    "state": "MS",
    "county": "Quitman"
  },
  {
    "fips": "08117",
    "state": "CO",
    "county": "Summit"
  },
  {
    "fips": "48021",
    "state": "TX",
    "county": "Bastrop"
  },
  {
    "fips": "13063",
    "state": "GA",
    "county": "Clayton"
  },
  {
    "fips": "51071",
    "state": "VA",
    "county": "Giles"
  },
  {
    "fips": "48083",
    "state": "TX",
    "county": "Coleman"
  },
  {
    "fips": "48353",
    "state": "TX",
    "county": "Nolan"
  },
  {
    "fips": "12129",
    "state": "FL",
    "county": "Wakulla"
  },
  {
    "fips": "29081",
    "state": "MO",
    "county": "Harrison"
  },
  {
    "fips": "17001",
    "state": "IL",
    "county": "Adams"
  },
  {
    "fips": "28129",
    "state": "MS",
    "county": "Smith"
  },
  {
    "fips": "53073",
    "state": "WA",
    "county": "Whatcom"
  },
  {
    "fips": "21215",
    "state": "KY",
    "county": "Spencer"
  },
  {
    "fips": "18013",
    "state": "IN",
    "county": "Brown"
  },
  {
    "fips": "13205",
    "state": "GA",
    "county": "Mitchell"
  },
  {
    "fips": "42109",
    "state": "PA",
    "county": "Snyder"
  },
  {
    "fips": "26155",
    "state": "MI",
    "county": "Shiawassee"
  },
  {
    "fips": "18069",
    "state": "IN",
    "county": "Huntington"
  },
  {
    "fips": "31179",
    "state": "NE",
    "county": "Wayne"
  },
  {
    "fips": "34029",
    "state": "NJ",
    "county": "Ocean"
  },
  {
    "fips": "26063",
    "state": "MI",
    "county": "Huron"
  },
  {
    "fips": "20161",
    "state": "KS",
    "county": "Riley"
  },
  {
    "fips": "30077",
    "state": "MT",
    "county": "Powell"
  },
  {
    "fips": "54001",
    "state": "WV",
    "county": "Barbour"
  },
  {
    "fips": "72047",
    "state": "PR",
    "county": "Corozal"
  },
  {
    "fips": "30101",
    "state": "MT",
    "county": "Toole"
  },
  {
    "fips": "22007",
    "state": "LA",
    "county": "Assumption"
  },
  {
    "fips": "29223",
    "state": "MO",
    "county": "Wayne"
  },
  {
    "fips": "21167",
    "state": "KY",
    "county": "Mercer"
  },
  {
    "fips": "24015",
    "state": "MD",
    "county": "Cecil"
  },
  {
    "fips": "45085",
    "state": "SC",
    "county": "Sumter"
  },
  {
    "fips": "56023",
    "state": "WY",
    "county": "Lincoln"
  },
  {
    "fips": "29093",
    "state": "MO",
    "county": "Iron"
  },
  {
    "fips": "21111",
    "state": "KY",
    "county": "Jefferson"
  },
  {
    "fips": "01085",
    "state": "AL",
    "county": "Lowndes"
  },
  {
    "fips": "06023",
    "state": "CA",
    "county": "Humboldt"
  },
  {
    "fips": "26037",
    "state": "MI",
    "county": "Clinton"
  },
  {
    "fips": "17153",
    "state": "IL",
    "county": "Pulaski"
  },
  {
    "fips": "27103",
    "state": "MN",
    "county": "Nicollet"
  },
  {
    "fips": "39021",
    "state": "OH",
    "county": "Champaign"
  },
  {
    "fips": "48093",
    "state": "TX",
    "county": "Comanche"
  },
  {
    "fips": "21157",
    "state": "KY",
    "county": "Marshall"
  },
  {
    "fips": "42087",
    "state": "PA",
    "county": "Mifflin"
  },
  {
    "fips": "40075",
    "state": "OK",
    "county": "Kiowa"
  },
  {
    "fips": "55125",
    "state": "WI",
    "county": "Vilas"
  },
  {
    "fips": "41033",
    "state": "OR",
    "county": "Josephine"
  },
  {
    "fips": "18041",
    "state": "IN",
    "county": "Fayette"
  },
  {
    "fips": "18183",
    "state": "IN",
    "county": "Whitley"
  },
  {
    "fips": "55027",
    "state": "WI",
    "county": "Dodge"
  },
  {
    "fips": "48251",
    "state": "TX",
    "county": "Johnson"
  },
  {
    "fips": "20169",
    "state": "KS",
    "county": "Saline"
  },
  {
    "fips": "21037",
    "state": "KY",
    "county": "Campbell"
  },
  {
    "fips": "48255",
    "state": "TX",
    "county": "Karnes"
  },
  {
    "fips": "48283",
    "state": "TX",
    "county": "La Salle"
  },
  {
    "fips": "55045",
    "state": "WI",
    "county": "Green"
  },
  {
    "fips": "25019",
    "state": "MA",
    "county": "Nantucket"
  },
  {
    "fips": "48165",
    "state": "TX",
    "county": "Gaines"
  },
  {
    "fips": "18117",
    "state": "IN",
    "county": "Orange"
  },
  {
    "fips": "54045",
    "state": "WV",
    "county": "Logan"
  },
  {
    "fips": "29041",
    "state": "MO",
    "county": "Chariton"
  },
  {
    "fips": "47145",
    "state": "TN",
    "county": "Roane"
  },
  {
    "fips": "48023",
    "state": "TX",
    "county": "Baylor"
  },
  {
    "fips": "40107",
    "state": "OK",
    "county": "Okfuskee"
  },
  {
    "fips": "42023",
    "state": "PA",
    "county": "Cameron"
  },
  {
    "fips": "51087",
    "state": "VA",
    "county": "Henrico"
  },
  {
    "fips": "01047",
    "state": "AL",
    "county": "Dallas"
  },
  {
    "fips": "05025",
    "state": "AR",
    "county": "Cleveland"
  },
  {
    "fips": "09011",
    "state": "CT",
    "county": "New London"
  },
  {
    "fips": "18101",
    "state": "IN",
    "county": "Martin"
  },
  {
    "fips": "21189",
    "state": "KY",
    "county": "Owsley"
  },
  {
    "fips": "29055",
    "state": "MO",
    "county": "Crawford"
  },
  {
    "fips": "12081",
    "state": "FL",
    "county": "Manatee"
  },
  {
    "fips": "29157",
    "state": "MO",
    "county": "Perry"
  },
  {
    "fips": "01133",
    "state": "AL",
    "county": "Winston"
  },
  {
    "fips": "30097",
    "state": "MT",
    "county": "Sweet Grass"
  },
  {
    "fips": "05029",
    "state": "AR",
    "county": "Conway"
  },
  {
    "fips": "13159",
    "state": "GA",
    "county": "Jasper"
  },
  {
    "fips": "30071",
    "state": "MT",
    "county": "Phillips"
  },
  {
    "fips": "51001",
    "state": "VA",
    "county": "Accomack"
  },
  {
    "fips": "44003",
    "state": "RI",
    "county": "Kent"
  },
  {
    "fips": "17009",
    "state": "IL",
    "county": "Brown"
  },
  {
    "fips": "48343",
    "state": "TX",
    "county": "Morris"
  },
  {
    "fips": "55079",
    "state": "WI",
    "county": "Milwaukee"
  },
  {
    "fips": "38047",
    "state": "ND",
    "county": "Logan"
  },
  {
    "fips": "01123",
    "state": "AL",
    "county": "Tallapoosa"
  },
  {
    "fips": "48019",
    "state": "TX",
    "county": "Bandera"
  },
  {
    "fips": "41035",
    "state": "OR",
    "county": "Klamath"
  },
  {
    "fips": "39109",
    "state": "OH",
    "county": "Miami"
  },
  {
    "fips": "54105",
    "state": "WV",
    "county": "Wirt"
  },
  {
    "fips": "47033",
    "state": "TN",
    "county": "Crockett"
  },
  {
    "fips": "48243",
    "state": "TX",
    "county": "Jeff Davis"
  },
  {
    "fips": "55091",
    "state": "WI",
    "county": "Pepin"
  },
  {
    "fips": "36001",
    "state": "NY",
    "county": "Albany"
  },
  {
    "fips": "48219",
    "state": "TX",
    "county": "Hockley"
  },
  {
    "fips": "29113",
    "state": "MO",
    "county": "Lincoln"
  },
  {
    "fips": "05001",
    "state": "AR",
    "county": "Arkansas"
  },
  {
    "fips": "05033",
    "state": "AR",
    "county": "Crawford"
  },
  {
    "fips": "53051",
    "state": "WA",
    "county": "Pend Oreille"
  },
  {
    "fips": "13297",
    "state": "GA",
    "county": "Walton"
  },
  {
    "fips": "39003",
    "state": "OH",
    "county": "Allen"
  },
  {
    "fips": "54093",
    "state": "WV",
    "county": "Tucker"
  },
  {
    "fips": "27111",
    "state": "MN",
    "county": "Otter Tail"
  },
  {
    "fips": "17121",
    "state": "IL",
    "county": "Marion"
  },
  {
    "fips": "42033",
    "state": "PA",
    "county": "Clearfield"
  },
  {
    "fips": "21221",
    "state": "KY",
    "county": "Trigg"
  },
  {
    "fips": "16073",
    "state": "ID",
    "county": "Owyhee"
  },
  {
    "fips": "40001",
    "state": "OK",
    "county": "Adair"
  },
  {
    "fips": "08021",
    "state": "CO",
    "county": "Conejos"
  },
  {
    "fips": "72077",
    "state": "PR",
    "county": "Juncos"
  },
  {
    "fips": "17093",
    "state": "IL",
    "county": "Kendall"
  },
  {
    "fips": "13057",
    "state": "GA",
    "county": "Cherokee"
  },
  {
    "fips": "47081",
    "state": "TN",
    "county": "Hickman"
  },
  {
    "fips": "56005",
    "state": "WY",
    "county": "Campbell"
  },
  {
    "fips": "21103",
    "state": "KY",
    "county": "Henry"
  },
  {
    "fips": "05013",
    "state": "AR",
    "county": "Calhoun"
  },
  {
    "fips": "27057",
    "state": "MN",
    "county": "Hubbard"
  },
  {
    "fips": "30085",
    "state": "MT",
    "county": "Roosevelt"
  },
  {
    "fips": "13105",
    "state": "GA",
    "county": "Elbert"
  },
  {
    "fips": "54099",
    "state": "WV",
    "county": "Wayne"
  },
  {
    "fips": "29201",
    "state": "MO",
    "county": "Scott"
  },
  {
    "fips": "01089",
    "state": "AL",
    "county": "Madison"
  },
  {
    "fips": "16017",
    "state": "ID",
    "county": "Bonner"
  },
  {
    "fips": "51093",
    "state": "VA",
    "county": "Isle of Wight"
  },
  {
    "fips": "55015",
    "state": "WI",
    "county": "Calumet"
  },
  {
    "fips": "42071",
    "state": "PA",
    "county": "Lancaster"
  },
  {
    "fips": "51157",
    "state": "VA",
    "county": "Rappahannock"
  },
  {
    "fips": "54025",
    "state": "WV",
    "county": "Greenbrier"
  },
  {
    "fips": "21113",
    "state": "KY",
    "county": "Jessamine"
  },
  {
    "fips": "27109",
    "state": "MN",
    "county": "Olmsted"
  },
  {
    "fips": "40019",
    "state": "OK",
    "county": "Carter"
  },
  {
    "fips": "13147",
    "state": "GA",
    "county": "Hart"
  },
  {
    "fips": "51045",
    "state": "VA",
    "county": "Craig"
  },
  {
    "fips": "29183",
    "state": "MO",
    "county": "St. Charles"
  },
  {
    "fips": "18089",
    "state": "IN",
    "county": "Lake"
  },
  {
    "fips": "48347",
    "state": "TX",
    "county": "Nacogdoches"
  },
  {
    "fips": "08053",
    "state": "CO",
    "county": "Hinsdale"
  },
  {
    "fips": "18033",
    "state": "IN",
    "county": "De Kalb"
  },
  {
    "fips": "24001",
    "state": "MD",
    "county": "Allegany"
  },
  {
    "fips": "25023",
    "state": "MA",
    "county": "Plymouth"
  },
  {
    "fips": "39159",
    "state": "OH",
    "county": "Union"
  },
  {
    "fips": "13197",
    "state": "GA",
    "county": "Marion"
  },
  {
    "fips": "29061",
    "state": "MO",
    "county": "Daviess"
  },
  {
    "fips": "72135",
    "state": "PR",
    "county": "Toa Alta"
  },
  {
    "fips": "53057",
    "state": "WA",
    "county": "Skagit"
  },
  {
    "fips": "13217",
    "state": "GA",
    "county": "Newton"
  },
  {
    "fips": "31011",
    "state": "NE",
    "county": "Boone"
  },
  {
    "fips": "27141",
    "state": "MN",
    "county": "Sherburne"
  },
  {
    "fips": "72143",
    "state": "PR",
    "county": "Vega Alta"
  },
  {
    "fips": "05061",
    "state": "AR",
    "county": "Howard"
  },
  {
    "fips": "29179",
    "state": "MO",
    "county": "Reynolds"
  },
  {
    "fips": "29195",
    "state": "MO",
    "county": "Saline"
  },
  {
    "fips": "39145",
    "state": "OH",
    "county": "Scioto"
  },
  {
    "fips": "17113",
    "state": "IL",
    "county": "McLean"
  },
  {
    "fips": "18023",
    "state": "IN",
    "county": "Clinton"
  },
  {
    "fips": "28149",
    "state": "MS",
    "county": "Warren"
  },
  {
    "fips": "54083",
    "state": "WV",
    "county": "Randolph"
  },
  {
    "fips": "21021",
    "state": "KY",
    "county": "Boyle"
  },
  {
    "fips": "72095",
    "state": "PR",
    "county": "Maunabo"
  },
  {
    "fips": "42037",
    "state": "PA",
    "county": "Columbia"
  },
  {
    "fips": "31035",
    "state": "NE",
    "county": "Clay"
  },
  {
    "fips": "18175",
    "state": "IN",
    "county": "Washington"
  },
  {
    "fips": "36047",
    "state": "NY",
    "county": "Kings"
  },
  {
    "fips": "60030",
    "state": "AS",
    "county": "Rose Island"
  },
  {
    "fips": "01059",
    "state": "AL",
    "county": "Franklin"
  },
  {
    "fips": "48203",
    "state": "TX",
    "county": "Harrison"
  },
  {
    "fips": "19087",
    "state": "IA",
    "county": "Henry"
  },
  {
    "fips": "30103",
    "state": "MT",
    "county": "Treasure"
  },
  {
    "fips": "47049",
    "state": "TN",
    "county": "Fentress"
  },
  {
    "fips": "28003",
    "state": "MS",
    "county": "Alcorn"
  },
  {
    "fips": "08005",
    "state": "CO",
    "county": "Arapahoe"
  },
  {
    "fips": "18051",
    "state": "IN",
    "county": "Gibson"
  },
  {
    "fips": "20027",
    "state": "KS",
    "county": "Clay"
  },
  {
    "fips": "26081",
    "state": "MI",
    "county": "Kent"
  },
  {
    "fips": "30063",
    "state": "MT",
    "county": "Missoula"
  },
  {
    "fips": "17031",
    "state": "IL",
    "county": "Cook"
  },
  {
    "fips": "04019",
    "state": "AZ",
    "county": "Pima"
  },
  {
    "fips": "20049",
    "state": "KS",
    "county": "Elk"
  },
  {
    "fips": "51111",
    "state": "VA",
    "county": "Lunenburg"
  },
  {
    "fips": "13317",
    "state": "GA",
    "county": "Wilkes"
  },
  {
    "fips": "35019",
    "state": "NM",
    "county": "Guadalupe"
  },
  {
    "fips": "13079",
    "state": "GA",
    "county": "Crawford"
  },
  {
    "fips": "28045",
    "state": "MS",
    "county": "Hancock"
  },
  {
    "fips": "13109",
    "state": "GA",
    "county": "Evans"
  },
  {
    "fips": "31023",
    "state": "NE",
    "county": "Butler"
  },
  {
    "fips": "37185",
    "state": "NC",
    "county": "Warren"
  },
  {
    "fips": "31131",
    "state": "NE",
    "county": "Otoe"
  },
  {
    "fips": "16005",
    "state": "ID",
    "county": "Bannock"
  },
  {
    "fips": "27045",
    "state": "MN",
    "county": "Fillmore"
  },
  {
    "fips": "06033",
    "state": "CA",
    "county": "Lake"
  },
  {
    "fips": "35001",
    "state": "NM",
    "county": "Bernalillo"
  },
  {
    "fips": "19051",
    "state": "IA",
    "county": "Davis"
  },
  {
    "fips": "27009",
    "state": "MN",
    "county": "Benton"
  },
  {
    "fips": "13151",
    "state": "GA",
    "county": "Henry"
  },
  {
    "fips": "47097",
    "state": "TN",
    "county": "Lauderdale"
  },
  {
    "fips": "36113",
    "state": "NY",
    "county": "Warren"
  },
  {
    "fips": "51520",
    "state": "VA",
    "county": "Bristol"
  },
  {
    "fips": "21139",
    "state": "KY",
    "county": "Livingston"
  },
  {
    "fips": "20017",
    "state": "KS",
    "county": "Chase"
  },
  {
    "fips": "46103",
    "state": "SD",
    "county": "Pennington"
  },
  {
    "fips": "13137",
    "state": "GA",
    "county": "Habersham"
  },
  {
    "fips": "45073",
    "state": "SC",
    "county": "Oconee"
  },
  {
    "fips": "05143",
    "state": "AR",
    "county": "Washington"
  },
  {
    "fips": "29067",
    "state": "MO",
    "county": "Douglas"
  },
  {
    "fips": "13267",
    "state": "GA",
    "county": "Tattnall"
  },
  {
    "fips": "42009",
    "state": "PA",
    "county": "Bedford"
  },
  {
    "fips": "48311",
    "state": "TX",
    "county": "McMullen"
  },
  {
    "fips": "48479",
    "state": "TX",
    "county": "Webb"
  },
  {
    "fips": "21017",
    "state": "KY",
    "county": "Bourbon"
  },
  {
    "fips": "06071",
    "state": "CA",
    "county": "San Bernardino"
  },
  {
    "fips": "36103",
    "state": "NY",
    "county": "Suffolk"
  },
  {
    "fips": "47027",
    "state": "TN",
    "county": "Clay"
  },
  {
    "fips": "36079",
    "state": "NY",
    "county": "Putnam"
  },
  {
    "fips": "48327",
    "state": "TX",
    "county": "Menard"
  },
  {
    "fips": "38097",
    "state": "ND",
    "county": "Traill"
  },
  {
    "fips": "04025",
    "state": "AZ",
    "county": "Yavapai"
  },
  {
    "fips": "53067",
    "state": "WA",
    "county": "Thurston"
  },
  {
    "fips": "22071",
    "state": "LA",
    "county": "Orleans"
  },
  {
    "fips": "31007",
    "state": "NE",
    "county": "Banner"
  },
  {
    "fips": "13219",
    "state": "GA",
    "county": "Oconee"
  },
  {
    "fips": "48287",
    "state": "TX",
    "county": "Lee"
  },
  {
    "fips": "28043",
    "state": "MS",
    "county": "Grenada"
  },
  {
    "fips": "39023",
    "state": "OH",
    "county": "Clark"
  },
  {
    "fips": "39101",
    "state": "OH",
    "county": "Marion"
  },
  {
    "fips": "45033",
    "state": "SC",
    "county": "Dillon"
  },
  {
    "fips": "48455",
    "state": "TX",
    "county": "Trinity"
  },
  {
    "fips": "17057",
    "state": "IL",
    "county": "Fulton"
  },
  {
    "fips": "09015",
    "state": "CT",
    "county": "Windham"
  },
  {
    "fips": "39133",
    "state": "OH",
    "county": "Portage"
  },
  {
    "fips": "72141",
    "state": "PR",
    "county": "Utuado"
  },
  {
    "fips": "28073",
    "state": "MS",
    "county": "Lamar"
  },
  {
    "fips": "31167",
    "state": "NE",
    "county": "Stanton"
  },
  {
    "fips": "05137",
    "state": "AR",
    "county": "Stone"
  },
  {
    "fips": "36071",
    "state": "NY",
    "county": "Orange"
  },
  {
    "fips": "47007",
    "state": "TN",
    "county": "Bledsoe"
  },
  {
    "fips": "17003",
    "state": "IL",
    "county": "Alexander"
  },
  {
    "fips": "19151",
    "state": "IA",
    "county": "Pocahontas"
  },
  {
    "fips": "37031",
    "state": "NC",
    "county": "Carteret"
  },
  {
    "fips": "37051",
    "state": "NC",
    "county": "Cumberland"
  },
  {
    "fips": "48241",
    "state": "TX",
    "county": "Jasper"
  },
  {
    "fips": "19137",
    "state": "IA",
    "county": "Montgomery"
  },
  {
    "fips": "13295",
    "state": "GA",
    "county": "Walker"
  },
  {
    "fips": "19011",
    "state": "IA",
    "county": "Benton"
  },
  {
    "fips": "19095",
    "state": "IA",
    "county": "Iowa"
  },
  {
    "fips": "47171",
    "state": "TN",
    "county": "Unicoi"
  },
  {
    "fips": "28125",
    "state": "MS",
    "county": "Sharkey"
  },
  {
    "fips": "13009",
    "state": "GA",
    "county": "Baldwin"
  },
  {
    "fips": "35035",
    "state": "NM",
    "county": "Otero"
  },
  {
    "fips": "01099",
    "state": "AL",
    "county": "Monroe"
  },
  {
    "fips": "18139",
    "state": "IN",
    "county": "Rush"
  },
  {
    "fips": "19089",
    "state": "IA",
    "county": "Howard"
  },
  {
    "fips": "45091",
    "state": "SC",
    "county": "York"
  },
  {
    "fips": "48127",
    "state": "TX",
    "county": "Dimmit"
  },
  {
    "fips": "48185",
    "state": "TX",
    "county": "Grimes"
  },
  {
    "fips": "48301",
    "state": "TX",
    "county": "Loving"
  },
  {
    "fips": "48495",
    "state": "TX",
    "county": "Winkler"
  },
  {
    "fips": "20061",
    "state": "KS",
    "county": "Geary"
  },
  {
    "fips": "25013",
    "state": "MA",
    "county": "Hampden"
  },
  {
    "fips": "72073",
    "state": "PR",
    "county": "Jayuya"
  },
  {
    "fips": "12041",
    "state": "FL",
    "county": "Gilchrist"
  },
  {
    "fips": "55023",
    "state": "WI",
    "county": "Crawford"
  },
  {
    "fips": "39065",
    "state": "OH",
    "county": "Hardin"
  },
  {
    "fips": "34015",
    "state": "NJ",
    "county": "Gloucester"
  },
  {
    "fips": "48297",
    "state": "TX",
    "county": "Live Oak"
  },
  {
    "fips": "41003",
    "state": "OR",
    "county": "Benton"
  },
  {
    "fips": "48435",
    "state": "TX",
    "county": "Sutton"
  },
  {
    "fips": "22069",
    "state": "LA",
    "county": "Natchitoches"
  },
  {
    "fips": "26135",
    "state": "MI",
    "county": "Oscoda"
  },
  {
    "fips": "48493",
    "state": "TX",
    "county": "Wilson"
  },
  {
    "fips": "36013",
    "state": "NY",
    "county": "Chautauqua"
  },
  {
    "fips": "54065",
    "state": "WV",
    "county": "Morgan"
  },
  {
    "fips": "19093",
    "state": "IA",
    "county": "Ida"
  },
  {
    "fips": "13069",
    "state": "GA",
    "county": "Coffee"
  },
  {
    "fips": "18157",
    "state": "IN",
    "county": "Tippecanoe"
  },
  {
    "fips": "51595",
    "state": "VA",
    "county": "Emporia"
  },
  {
    "fips": "13239",
    "state": "GA",
    "county": "Quitman"
  },
  {
    "fips": "29059",
    "state": "MO",
    "county": "Dallas"
  },
  {
    "fips": "31025",
    "state": "NE",
    "county": "Cass"
  },
  {
    "fips": "48011",
    "state": "TX",
    "county": "Armstrong"
  },
  {
    "fips": "19077",
    "state": "IA",
    "county": "Guthrie"
  },
  {
    "fips": "20031",
    "state": "KS",
    "county": "Coffey"
  },
  {
    "fips": "08057",
    "state": "CO",
    "county": "Jackson"
  },
  {
    "fips": "37063",
    "state": "NC",
    "county": "Durham"
  },
  {
    "fips": "26045",
    "state": "MI",
    "county": "Eaton"
  },
  {
    "fips": "40133",
    "state": "OK",
    "county": "Seminole"
  },
  {
    "fips": "54033",
    "state": "WV",
    "county": "Harrison"
  },
  {
    "fips": "51177",
    "state": "VA",
    "county": "Spotsylvania"
  },
  {
    "fips": "13269",
    "state": "GA",
    "county": "Taylor"
  },
  {
    "fips": "05091",
    "state": "AR",
    "county": "Miller"
  },
  {
    "fips": "17033",
    "state": "IL",
    "county": "Crawford"
  },
  {
    "fips": "27069",
    "state": "MN",
    "county": "Kittson"
  },
  {
    "fips": "48491",
    "state": "TX",
    "county": "Williamson"
  },
  {
    "fips": "48205",
    "state": "TX",
    "county": "Hartley"
  },
  {
    "fips": "48193",
    "state": "TX",
    "county": "Hamilton"
  },
  {
    "fips": "05105",
    "state": "AR",
    "county": "Perry"
  },
  {
    "fips": "29219",
    "state": "MO",
    "county": "Warren"
  },
  {
    "fips": "53065",
    "state": "WA",
    "county": "Stevens"
  },
  {
    "fips": "51630",
    "state": "VA",
    "county": "Fredericksburg"
  },
  {
    "fips": "13113",
    "state": "GA",
    "county": "Fayette"
  },
  {
    "fips": "47183",
    "state": "TN",
    "county": "Weakley"
  },
  {
    "fips": "53031",
    "state": "WA",
    "county": "Jefferson"
  },
  {
    "fips": "53059",
    "state": "WA",
    "county": "Skamania"
  },
  {
    "fips": "40079",
    "state": "OK",
    "county": "Le Flore"
  },
  {
    "fips": "08099",
    "state": "CO",
    "county": "Prowers"
  },
  {
    "fips": "55095",
    "state": "WI",
    "county": "Polk"
  },
  {
    "fips": "20081",
    "state": "KS",
    "county": "Haskell"
  },
  {
    "fips": "37085",
    "state": "NC",
    "county": "Harnett"
  },
  {
    "fips": "40057",
    "state": "OK",
    "county": "Harmon"
  },
  {
    "fips": "46095",
    "state": "SD",
    "county": "Mellette"
  },
  {
    "fips": "46051",
    "state": "SD",
    "county": "Grant"
  },
  {
    "fips": "06057",
    "state": "CA",
    "county": "Nevada"
  },
  {
    "fips": "72005",
    "state": "PR",
    "county": "Aguadilla"
  },
  {
    "fips": "48013",
    "state": "TX",
    "county": "Atascosa"
  },
  {
    "fips": "48481",
    "state": "TX",
    "county": "Wharton"
  },
  {
    "fips": "48457",
    "state": "TX",
    "county": "Tyler"
  },
  {
    "fips": "18133",
    "state": "IN",
    "county": "Putnam"
  },
  {
    "fips": "21013",
    "state": "KY",
    "county": "Bell"
  },
  {
    "fips": "20135",
    "state": "KS",
    "county": "Ness"
  },
  {
    "fips": "23023",
    "state": "ME",
    "county": "Sagadahoc"
  },
  {
    "fips": "16083",
    "state": "ID",
    "county": "Twin Falls"
  },
  {
    "fips": "18093",
    "state": "IN",
    "county": "Lawrence"
  },
  {
    "fips": "48085",
    "state": "TX",
    "county": "Collin"
  },
  {
    "fips": "50027",
    "state": "VT",
    "county": "Windsor"
  },
  {
    "fips": "51101",
    "state": "VA",
    "county": "King William"
  },
  {
    "fips": "39067",
    "state": "OH",
    "county": "Harrison"
  },
  {
    "fips": "54009",
    "state": "WV",
    "county": "Brooke"
  },
  {
    "fips": "72093",
    "state": "PR",
    "county": "Maricao"
  },
  {
    "fips": "37177",
    "state": "NC",
    "county": "Tyrrell"
  },
  {
    "fips": "17039",
    "state": "IL",
    "county": "De Witt"
  },
  {
    "fips": "42015",
    "state": "PA",
    "county": "Bradford"
  },
  {
    "fips": "22033",
    "state": "LA",
    "county": "East Baton Rouge"
  },
  {
    "fips": "01023",
    "state": "AL",
    "county": "Choctaw"
  },
  {
    "fips": "23001",
    "state": "ME",
    "county": "Androscoggin"
  },
  {
    "fips": "29017",
    "state": "MO",
    "county": "Bollinger"
  },
  {
    "fips": "48231",
    "state": "TX",
    "county": "Hunt"
  },
  {
    "fips": "30105",
    "state": "MT",
    "county": "Valley"
  },
  {
    "fips": "72069",
    "state": "PR",
    "county": "Humacao"
  },
  {
    "fips": "54027",
    "state": "WV",
    "county": "Hampshire"
  },
  {
    "fips": "06045",
    "state": "CA",
    "county": "Mendocino"
  },
  {
    "fips": "48329",
    "state": "TX",
    "county": "Midland"
  },
  {
    "fips": "21035",
    "state": "KY",
    "county": "Calloway"
  },
  {
    "fips": "53061",
    "state": "WA",
    "county": "Snohomish"
  },
  {
    "fips": "36045",
    "state": "NY",
    "county": "Jefferson"
  },
  {
    "fips": "51185",
    "state": "VA",
    "county": "Tazewell"
  },
  {
    "fips": "40129",
    "state": "OK",
    "county": "Roger Mills"
  },
  {
    "fips": "28015",
    "state": "MS",
    "county": "Carroll"
  },
  {
    "fips": "55078",
    "state": "WI",
    "county": "Menominee"
  },
  {
    "fips": "21049",
    "state": "KY",
    "county": "Clark"
  },
  {
    "fips": "37081",
    "state": "NC",
    "county": "Guilford"
  },
  {
    "fips": "31169",
    "state": "NE",
    "county": "Thayer"
  },
  {
    "fips": "19021",
    "state": "IA",
    "county": "Buena Vista"
  },
  {
    "fips": "51560",
    "state": "VA",
    "county": "Clifton Forge"
  },
  {
    "fips": "06009",
    "state": "CA",
    "county": "Calaveras"
  },
  {
    "fips": "48201",
    "state": "TX",
    "county": "Harris"
  },
  {
    "fips": "19185",
    "state": "IA",
    "county": "Wayne"
  },
  {
    "fips": "51540",
    "state": "VA",
    "county": "Charlottesville"
  },
  {
    "fips": "12021",
    "state": "FL",
    "county": "Collier"
  },
  {
    "fips": "27003",
    "state": "MN",
    "county": "Anoka"
  },
  {
    "fips": "34023",
    "state": "NJ",
    "county": "Middlesex"
  },
  {
    "fips": "22063",
    "state": "LA",
    "county": "Livingston"
  },
  {
    "fips": "36093",
    "state": "NY",
    "county": "Schenectady"
  },
  {
    "fips": "39135",
    "state": "OH",
    "county": "Preble"
  },
  {
    "fips": "51153",
    "state": "VA",
    "county": "Prince William"
  },
  {
    "fips": "51089",
    "state": "VA",
    "county": "Henry"
  },
  {
    "fips": "16071",
    "state": "ID",
    "county": "Oneida"
  },
  {
    "fips": "37107",
    "state": "NC",
    "county": "Lenoir"
  },
  {
    "fips": "55025",
    "state": "WI",
    "county": "Dane"
  },
  {
    "fips": "29077",
    "state": "MO",
    "county": "Greene"
  },
  {
    "fips": "48323",
    "state": "TX",
    "county": "Maverick"
  },
  {
    "fips": "56033",
    "state": "WY",
    "county": "Sheridan"
  },
  {
    "fips": "22103",
    "state": "LA",
    "county": "St. Tammany"
  },
  {
    "fips": "48175",
    "state": "TX",
    "county": "Goliad"
  },
  {
    "fips": "46021",
    "state": "SD",
    "county": "Campbell"
  },
  {
    "fips": "05115",
    "state": "AR",
    "county": "Pope"
  },
  {
    "fips": "28011",
    "state": "MS",
    "county": "Bolivar"
  },
  {
    "fips": "26159",
    "state": "MI",
    "county": "Van Buren"
  },
  {
    "fips": "34021",
    "state": "NJ",
    "county": "Mercer"
  },
  {
    "fips": "47125",
    "state": "TN",
    "county": "Montgomery"
  },
  {
    "fips": "31153",
    "state": "NE",
    "county": "Sarpy"
  },
  {
    "fips": "12023",
    "state": "FL",
    "county": "Columbia"
  },
  {
    "fips": "42057",
    "state": "PA",
    "county": "Fulton"
  },
  {
    "fips": "48235",
    "state": "TX",
    "county": "Irion"
  },
  {
    "fips": "55003",
    "state": "WI",
    "county": "Ashland"
  },
  {
    "fips": "26131",
    "state": "MI",
    "county": "Ontonagon"
  },
  {
    "fips": "54097",
    "state": "WV",
    "county": "Upshur"
  },
  {
    "fips": "28141",
    "state": "MS",
    "county": "Tishomingo"
  },
  {
    "fips": "32031",
    "state": "NV",
    "county": "Washoe"
  },
  {
    "fips": "40153",
    "state": "OK",
    "county": "Woodward"
  },
  {
    "fips": "42017",
    "state": "PA",
    "county": "Bucks"
  },
  {
    "fips": "48275",
    "state": "TX",
    "county": "Knox"
  },
  {
    "fips": "27149",
    "state": "MN",
    "county": "Stevens"
  },
  {
    "fips": "37133",
    "state": "NC",
    "county": "Onslow"
  },
  {
    "fips": "27063",
    "state": "MN",
    "county": "Jackson"
  },
  {
    "fips": "46043",
    "state": "SD",
    "county": "Douglas"
  },
  {
    "fips": "31077",
    "state": "NE",
    "county": "Greeley"
  },
  {
    "fips": "48249",
    "state": "TX",
    "county": "Jim Wells"
  },
  {
    "fips": "05073",
    "state": "AR",
    "county": "Lafayette"
  },
  {
    "fips": "40049",
    "state": "OK",
    "county": "Garvin"
  },
  {
    "fips": "26123",
    "state": "MI",
    "county": "Newaygo"
  },
  {
    "fips": "38029",
    "state": "ND",
    "county": "Emmons"
  },
  {
    "fips": "08033",
    "state": "CO",
    "county": "Dolores"
  },
  {
    "fips": "29155",
    "state": "MO",
    "county": "Pemiscot"
  },
  {
    "fips": "12091",
    "state": "FL",
    "county": "Okaloosa"
  },
  {
    "fips": "40051",
    "state": "OK",
    "county": "Grady"
  },
  {
    "fips": "21163",
    "state": "KY",
    "county": "Meade"
  },
  {
    "fips": "72115",
    "state": "PR",
    "county": "Quebradillas"
  },
  {
    "fips": "29019",
    "state": "MO",
    "county": "Boone"
  },
  {
    "fips": "51023",
    "state": "VA",
    "county": "Botetourt"
  },
  {
    "fips": "55001",
    "state": "WI",
    "county": "Adams"
  },
  {
    "fips": "55035",
    "state": "WI",
    "county": "Eau Claire"
  },
  {
    "fips": "13061",
    "state": "GA",
    "county": "Clay"
  },
  {
    "fips": "30039",
    "state": "MT",
    "county": "Granite"
  },
  {
    "fips": "13299",
    "state": "GA",
    "county": "Ware"
  },
  {
    "fips": "28037",
    "state": "MS",
    "county": "Franklin"
  },
  {
    "fips": "18181",
    "state": "IN",
    "county": "White"
  },
  {
    "fips": "44005",
    "state": "RI",
    "county": "Newport"
  },
  {
    "fips": "55053",
    "state": "WI",
    "county": "Jackson"
  },
  {
    "fips": "05135",
    "state": "AR",
    "county": "Sharp"
  },
  {
    "fips": "45063",
    "state": "SC",
    "county": "Lexington"
  },
  {
    "fips": "48299",
    "state": "TX",
    "county": "Llano"
  },
  {
    "fips": "30041",
    "state": "MT",
    "county": "Hill"
  },
  {
    "fips": "48159",
    "state": "TX",
    "county": "Franklin"
  },
  {
    "fips": "49019",
    "state": "UT",
    "county": "Grand"
  },
  {
    "fips": "26013",
    "state": "MI",
    "county": "Baraga"
  },
  {
    "fips": "18057",
    "state": "IN",
    "county": "Hamilton"
  },
  {
    "fips": "31081",
    "state": "NE",
    "county": "Hamilton"
  },
  {
    "fips": "06089",
    "state": "CA",
    "county": "Shasta"
  },
  {
    "fips": "25005",
    "state": "MA",
    "county": "Bristol"
  },
  {
    "fips": "72153",
    "state": "PR",
    "county": "Yauco"
  },
  {
    "fips": "36057",
    "state": "NY",
    "county": "Montgomery"
  },
  {
    "fips": "12119",
    "state": "FL",
    "county": "Sumter"
  },
  {
    "fips": "20071",
    "state": "KS",
    "county": "Greeley"
  },
  {
    "fips": "16021",
    "state": "ID",
    "county": "Boundary"
  },
  {
    "fips": "28155",
    "state": "MS",
    "county": "Webster"
  },
  {
    "fips": "46017",
    "state": "SD",
    "county": "Buffalo"
  },
  {
    "fips": "51760",
    "state": "VA",
    "county": "Richmond"
  },
  {
    "fips": "19105",
    "state": "IA",
    "county": "Jones"
  },
  {
    "fips": "21123",
    "state": "KY",
    "county": "Larue"
  },
  {
    "fips": "41037",
    "state": "OR",
    "county": "Lake"
  },
  {
    "fips": "38061",
    "state": "ND",
    "county": "Mountrail"
  },
  {
    "fips": "48079",
    "state": "TX",
    "county": "Cochran"
  },
  {
    "fips": "31147",
    "state": "NE",
    "county": "Richardson"
  },
  {
    "fips": "28111",
    "state": "MS",
    "county": "Perry"
  },
  {
    "fips": "44009",
    "state": "RI",
    "county": "Washington"
  },
  {
    "fips": "37183",
    "state": "NC",
    "county": "Wake"
  },
  {
    "fips": "48409",
    "state": "TX",
    "county": "San Patricio"
  },
  {
    "fips": "48459",
    "state": "TX",
    "county": "Upshur"
  },
  {
    "fips": "08035",
    "state": "CO",
    "county": "Douglas"
  },
  {
    "fips": "16019",
    "state": "ID",
    "county": "Bonneville"
  },
  {
    "fips": "28127",
    "state": "MS",
    "county": "Simpson"
  },
  {
    "fips": "38075",
    "state": "ND",
    "county": "Renville"
  },
  {
    "fips": "31107",
    "state": "NE",
    "county": "Knox"
  },
  {
    "fips": "48373",
    "state": "TX",
    "county": "Polk"
  },
  {
    "fips": "69100",
    "state": "MP",
    "county": "Rota"
  },
  {
    "fips": "21077",
    "state": "KY",
    "county": "Gallatin"
  },
  {
    "fips": "56045",
    "state": "WY",
    "county": "Weston"
  },
  {
    "fips": "41045",
    "state": "OR",
    "county": "Malheur"
  },
  {
    "fips": "13191",
    "state": "GA",
    "county": "McIntosh"
  },
  {
    "fips": "51035",
    "state": "VA",
    "county": "Carroll"
  },
  {
    "fips": "18137",
    "state": "IN",
    "county": "Ripley"
  },
  {
    "fips": "21137",
    "state": "KY",
    "county": "Lincoln"
  },
  {
    "fips": "04007",
    "state": "AZ",
    "county": "Gila"
  },
  {
    "fips": "28151",
    "state": "MS",
    "county": "Washington"
  },
  {
    "fips": "38003",
    "state": "ND",
    "county": "Barnes"
  },
  {
    "fips": "21003",
    "state": "KY",
    "county": "Allen"
  },
  {
    "fips": "37041",
    "state": "NC",
    "county": "Chowan"
  },
  {
    "fips": "12117",
    "state": "FL",
    "county": "Seminole"
  },
  {
    "fips": "35011",
    "state": "NM",
    "county": "DeBaca"
  },
  {
    "fips": "48163",
    "state": "TX",
    "county": "Frio"
  },
  {
    "fips": "06055",
    "state": "CA",
    "county": "Napa"
  },
  {
    "fips": "05149",
    "state": "AR",
    "county": "Yell"
  },
  {
    "fips": "24011",
    "state": "MD",
    "county": "Caroline"
  },
  {
    "fips": "13271",
    "state": "GA",
    "county": "Telfair"
  },
  {
    "fips": "10003",
    "state": "DE",
    "county": "New Castle"
  },
  {
    "fips": "26099",
    "state": "MI",
    "county": "Macomb"
  },
  {
    "fips": "31161",
    "state": "NE",
    "county": "Sheridan"
  },
  {
    "fips": "49015",
    "state": "UT",
    "county": "Emery"
  },
  {
    "fips": "24031",
    "state": "MD",
    "county": "Montgomery"
  },
  {
    "fips": "18003",
    "state": "IN",
    "county": "Allen"
  },
  {
    "fips": "45031",
    "state": "SC",
    "county": "Darlington"
  },
  {
    "fips": "37097",
    "state": "NC",
    "county": "Iredell"
  },
  {
    "fips": "47173",
    "state": "TN",
    "county": "Union"
  },
  {
    "fips": "51067",
    "state": "VA",
    "county": "Franklin"
  },
  {
    "fips": "28163",
    "state": "MS",
    "county": "Yazoo"
  },
  {
    "fips": "22035",
    "state": "LA",
    "county": "East Carroll"
  },
  {
    "fips": "40087",
    "state": "OK",
    "county": "McClain"
  },
  {
    "fips": "48089",
    "state": "TX",
    "county": "Colorado"
  },
  {
    "fips": "20085",
    "state": "KS",
    "county": "Jackson"
  },
  {
    "fips": "01033",
    "state": "AL",
    "county": "Colbert"
  },
  {
    "fips": "09005",
    "state": "CT",
    "county": "Litchfield"
  },
  {
    "fips": "40117",
    "state": "OK",
    "county": "Pawnee"
  },
  {
    "fips": "05139",
    "state": "AR",
    "county": "Union"
  },
  {
    "fips": "41009",
    "state": "OR",
    "county": "Columbia"
  },
  {
    "fips": "29047",
    "state": "MO",
    "county": "Clay"
  },
  {
    "fips": "13135",
    "state": "GA",
    "county": "Gwinnett"
  },
  {
    "fips": "17115",
    "state": "IL",
    "county": "Macon"
  },
  {
    "fips": "26103",
    "state": "MI",
    "county": "Marquette"
  },
  {
    "fips": "12061",
    "state": "FL",
    "county": "Indian River"
  },
  {
    "fips": "37155",
    "state": "NC",
    "county": "Robeson"
  },
  {
    "fips": "46061",
    "state": "SD",
    "county": "Hanson"
  },
  {
    "fips": "21151",
    "state": "KY",
    "county": "Madison"
  },
  {
    "fips": "19183",
    "state": "IA",
    "county": "Washington"
  },
  {
    "fips": "31109",
    "state": "NE",
    "county": "Lancaster"
  },
  {
    "fips": "53023",
    "state": "WA",
    "county": "Garfield"
  },
  {
    "fips": "13181",
    "state": "GA",
    "county": "Lincoln"
  },
  {
    "fips": "16035",
    "state": "ID",
    "county": "Clearwater"
  },
  {
    "fips": "12053",
    "state": "FL",
    "county": "Hernando"
  },
  {
    "fips": "25021",
    "state": "MA",
    "county": "Norfolk"
  },
  {
    "fips": "31171",
    "state": "NE",
    "county": "Thomas"
  },
  {
    "fips": "04009",
    "state": "AZ",
    "county": "Graham"
  },
  {
    "fips": "20207",
    "state": "KS",
    "county": "Woodson"
  },
  {
    "fips": "53021",
    "state": "WA",
    "county": "Franklin"
  },
  {
    "fips": "48351",
    "state": "TX",
    "county": "Newton"
  },
  {
    "fips": "05123",
    "state": "AR",
    "county": "St. Francis"
  },
  {
    "fips": "24005",
    "state": "MD",
    "county": "Baltimore"
  },
  {
    "fips": "48507",
    "state": "TX",
    "county": "Zavala"
  },
  {
    "fips": "54101",
    "state": "WV",
    "county": "Webster"
  },
  {
    "fips": "40009",
    "state": "OK",
    "county": "Beckham"
  },
  {
    "fips": "21005",
    "state": "KY",
    "county": "Anderson"
  },
  {
    "fips": "39103",
    "state": "OH",
    "county": "Medina"
  },
  {
    "fips": "18131",
    "state": "IN",
    "county": "Pulaski"
  },
  {
    "fips": "37045",
    "state": "NC",
    "county": "Cleveland"
  },
  {
    "fips": "40147",
    "state": "OK",
    "county": "Washington"
  },
  {
    "fips": "01039",
    "state": "AL",
    "county": "Covington"
  },
  {
    "fips": "46053",
    "state": "SD",
    "county": "Gregory"
  },
  {
    "fips": "35059",
    "state": "NM",
    "county": "Union"
  },
  {
    "fips": "22081",
    "state": "LA",
    "county": "Red River"
  },
  {
    "fips": "17019",
    "state": "IL",
    "county": "Champaign"
  },
  {
    "fips": "45001",
    "state": "SC",
    "county": "Abbeville"
  },
  {
    "fips": "47017",
    "state": "TN",
    "county": "Carroll"
  },
  {
    "fips": "48211",
    "state": "TX",
    "county": "Hemphill"
  },
  {
    "fips": "37047",
    "state": "NC",
    "county": "Columbus"
  },
  {
    "fips": "37083",
    "state": "NC",
    "county": "Halifax"
  },
  {
    "fips": "30073",
    "state": "MT",
    "county": "Pondera"
  },
  {
    "fips": "38005",
    "state": "ND",
    "county": "Benson"
  },
  {
    "fips": "40123",
    "state": "OK",
    "county": "Pontotoc"
  },
  {
    "fips": "21023",
    "state": "KY",
    "county": "Bracken"
  },
  {
    "fips": "51720",
    "state": "VA",
    "county": "Norton"
  },
  {
    "fips": "17179",
    "state": "IL",
    "county": "Tazewell"
  },
  {
    "fips": "72025",
    "state": "PR",
    "county": "Caguas"
  },
  {
    "fips": "13221",
    "state": "GA",
    "county": "Oglethorpe"
  },
  {
    "fips": "37065",
    "state": "NC",
    "county": "Edgecombe"
  },
  {
    "fips": "24017",
    "state": "MD",
    "county": "Charles"
  },
  {
    "fips": "40125",
    "state": "OK",
    "county": "Pottawatomie"
  },
  {
    "fips": "13229",
    "state": "GA",
    "county": "Pierce"
  },
  {
    "fips": "48057",
    "state": "TX",
    "county": "Calhoun"
  },
  {
    "fips": "25001",
    "state": "MA",
    "county": "Barnstable"
  },
  {
    "fips": "47107",
    "state": "TN",
    "county": "McMinn"
  },
  {
    "fips": "41017",
    "state": "OR",
    "county": "Deschutes"
  },
  {
    "fips": "48229",
    "state": "TX",
    "county": "Hudspeth"
  },
  {
    "fips": "06041",
    "state": "CA",
    "county": "Marin"
  },
  {
    "fips": "12059",
    "state": "FL",
    "county": "Holmes"
  },
  {
    "fips": "05015",
    "state": "AR",
    "county": "Carroll"
  },
  {
    "fips": "27153",
    "state": "MN",
    "county": "Todd"
  },
  {
    "fips": "28055",
    "state": "MS",
    "county": "Issaquena"
  },
  {
    "fips": "05005",
    "state": "AR",
    "county": "Baxter"
  },
  {
    "fips": "36041",
    "state": "NY",
    "county": "Hamilton"
  },
  {
    "fips": "47061",
    "state": "TN",
    "county": "Grundy"
  },
  {
    "fips": "08085",
    "state": "CO",
    "county": "Montrose"
  },
  {
    "fips": "72113",
    "state": "PR",
    "county": "Ponce"
  },
  {
    "fips": "56037",
    "state": "WY",
    "county": "Sweetwater"
  },
  {
    "fips": "17105",
    "state": "IL",
    "county": "Livingston"
  },
  {
    "fips": "20015",
    "state": "KS",
    "county": "Butler"
  },
  {
    "fips": "27147",
    "state": "MN",
    "county": "Steele"
  },
  {
    "fips": "46023",
    "state": "SD",
    "county": "Charles Mix"
  },
  {
    "fips": "17095",
    "state": "IL",
    "county": "Knox"
  },
  {
    "fips": "28021",
    "state": "MS",
    "county": "Claiborne"
  },
  {
    "fips": "35015",
    "state": "NM",
    "county": "Eddy"
  },
  {
    "fips": "37113",
    "state": "NC",
    "county": "Macon"
  },
  {
    "fips": "39165",
    "state": "OH",
    "county": "Warren"
  },
  {
    "fips": "36085",
    "state": "NY",
    "county": "Richmond"
  },
  {
    "fips": "20173",
    "state": "KS",
    "county": "Sedgwick"
  },
  {
    "fips": "51103",
    "state": "VA",
    "county": "Lancaster"
  },
  {
    "fips": "48419",
    "state": "TX",
    "county": "Shelby"
  },
  {
    "fips": "19175",
    "state": "IA",
    "county": "Union"
  },
  {
    "fips": "48031",
    "state": "TX",
    "county": "Blanco"
  },
  {
    "fips": "29145",
    "state": "MO",
    "county": "Newton"
  },
  {
    "fips": "32015",
    "state": "NV",
    "county": "Lander"
  },
  {
    "fips": "36081",
    "state": "NY",
    "county": "Queens"
  },
  {
    "fips": "51041",
    "state": "VA",
    "county": "Chesterfield"
  },
  {
    "fips": "30111",
    "state": "MT",
    "county": "Yellowstone"
  },
  {
    "fips": "48271",
    "state": "TX",
    "county": "Kinney"
  },
  {
    "fips": "53035",
    "state": "WA",
    "county": "Kitsap"
  },
  {
    "fips": "17145",
    "state": "IL",
    "county": "Perry"
  },
  {
    "fips": "39035",
    "state": "OH",
    "county": "Cuyahoga"
  },
  {
    "fips": "12073",
    "state": "FL",
    "county": "Leon"
  },
  {
    "fips": "22029",
    "state": "LA",
    "county": "Concordia"
  },
  {
    "fips": "48207",
    "state": "TX",
    "county": "Haskell"
  },
  {
    "fips": "22101",
    "state": "LA",
    "county": "St. Mary"
  },
  {
    "fips": "18143",
    "state": "IN",
    "county": "Scott"
  },
  {
    "fips": "17147",
    "state": "IL",
    "county": "Piatt"
  },
  {
    "fips": "51650",
    "state": "VA",
    "county": "Hampton"
  },
  {
    "fips": "06061",
    "state": "CA",
    "county": "Placer"
  },
  {
    "fips": "51820",
    "state": "VA",
    "county": "Waynesboro"
  },
  {
    "fips": "19129",
    "state": "IA",
    "county": "Mills"
  },
  {
    "fips": "26071",
    "state": "MI",
    "county": "Iron"
  },
  {
    "fips": "22041",
    "state": "LA",
    "county": "Franklin"
  },
  {
    "fips": "38041",
    "state": "ND",
    "county": "Hettinger"
  },
  {
    "fips": "26073",
    "state": "MI",
    "county": "Isabella"
  },
  {
    "fips": "04017",
    "state": "AZ",
    "county": "Navajo"
  },
  {
    "fips": "01071",
    "state": "AL",
    "county": "Jackson"
  },
  {
    "fips": "28139",
    "state": "MS",
    "county": "Tippah"
  },
  {
    "fips": "36083",
    "state": "NY",
    "county": "Rensselaer"
  },
  {
    "fips": "51171",
    "state": "VA",
    "county": "Shenandoah"
  },
  {
    "fips": "30059",
    "state": "MT",
    "county": "Meagher"
  },
  {
    "fips": "06027",
    "state": "CA",
    "county": "Inyo"
  },
  {
    "fips": "29211",
    "state": "MO",
    "county": "Sullivan"
  },
  {
    "fips": "05053",
    "state": "AR",
    "county": "Grant"
  },
  {
    "fips": "12113",
    "state": "FL",
    "county": "Santa Rosa"
  },
  {
    "fips": "17099",
    "state": "IL",
    "county": "La Salle"
  },
  {
    "fips": "17103",
    "state": "IL",
    "county": "Lee"
  },
  {
    "fips": "47169",
    "state": "TN",
    "county": "Trousdale"
  },
  {
    "fips": "54081",
    "state": "WV",
    "county": "Raleigh"
  },
  {
    "fips": "48171",
    "state": "TX",
    "county": "Gillespie"
  },
  {
    "fips": "51121",
    "state": "VA",
    "county": "Montgomery"
  },
  {
    "fips": "48069",
    "state": "TX",
    "county": "Castro"
  },
  {
    "fips": "17101",
    "state": "IL",
    "county": "Lawrence"
  },
  {
    "fips": "28089",
    "state": "MS",
    "county": "Madison"
  },
  {
    "fips": "72089",
    "state": "PR",
    "county": "Luquillo"
  },
  {
    "fips": "20087",
    "state": "KS",
    "county": "Jefferson"
  },
  {
    "fips": "13201",
    "state": "GA",
    "county": "Miller"
  },
  {
    "fips": "48333",
    "state": "TX",
    "county": "Mills"
  },
  {
    "fips": "36019",
    "state": "NY",
    "county": "Clinton"
  },
  {
    "fips": "17007",
    "state": "IL",
    "county": "Boone"
  },
  {
    "fips": "29217",
    "state": "MO",
    "county": "Vernon"
  },
  {
    "fips": "21117",
    "state": "KY",
    "county": "Kenton"
  },
  {
    "fips": "30015",
    "state": "MT",
    "county": "Chouteau"
  },
  {
    "fips": "15003",
    "state": "HI",
    "county": "Honolulu"
  },
  {
    "fips": "35049",
    "state": "NM",
    "county": "Santa Fe"
  },
  {
    "fips": "29011",
    "state": "MO",
    "county": "Barton"
  },
  {
    "fips": "30011",
    "state": "MT",
    "county": "Carter"
  },
  {
    "fips": "17077",
    "state": "IL",
    "county": "Jackson"
  },
  {
    "fips": "05087",
    "state": "AR",
    "county": "Madison"
  },
  {
    "fips": "13163",
    "state": "GA",
    "county": "Jefferson"
  },
  {
    "fips": "21135",
    "state": "KY",
    "county": "Lewis"
  },
  {
    "fips": "17047",
    "state": "IL",
    "county": "Edwards"
  },
  {
    "fips": "28113",
    "state": "MS",
    "county": "Pike"
  },
  {
    "fips": "39047",
    "state": "OH",
    "county": "Fayette"
  },
  {
    "fips": "16025",
    "state": "ID",
    "county": "Camas"
  },
  {
    "fips": "32033",
    "state": "NV",
    "county": "White Pine"
  },
  {
    "fips": "26027",
    "state": "MI",
    "county": "Cass"
  },
  {
    "fips": "05037",
    "state": "AR",
    "county": "Cross"
  },
  {
    "fips": "13175",
    "state": "GA",
    "county": "Laurens"
  },
  {
    "fips": "49031",
    "state": "UT",
    "county": "Piute"
  },
  {
    "fips": "28159",
    "state": "MS",
    "county": "Winston"
  },
  {
    "fips": "21059",
    "state": "KY",
    "county": "Daviess"
  },
  {
    "fips": "55039",
    "state": "WI",
    "county": "Fond du Lac"
  },
  {
    "fips": "31057",
    "state": "NE",
    "county": "Dundy"
  },
  {
    "fips": "40029",
    "state": "OK",
    "county": "Coal"
  },
  {
    "fips": "27055",
    "state": "MN",
    "county": "Houston"
  },
  {
    "fips": "37149",
    "state": "NC",
    "county": "Polk"
  },
  {
    "fips": "31135",
    "state": "NE",
    "county": "Perkins"
  },
  {
    "fips": "37143",
    "state": "NC",
    "county": "Perquimans"
  },
  {
    "fips": "05039",
    "state": "AR",
    "county": "Dallas"
  },
  {
    "fips": "17167",
    "state": "IL",
    "county": "Sangamon"
  },
  {
    "fips": "48209",
    "state": "TX",
    "county": "Hays"
  },
  {
    "fips": "30035",
    "state": "MT",
    "county": "Glacier"
  },
  {
    "fips": "18135",
    "state": "IN",
    "county": "Randolph"
  },
  {
    "fips": "26011",
    "state": "MI",
    "county": "Arenac"
  },
  {
    "fips": "41025",
    "state": "OR",
    "county": "Harney"
  },
  {
    "fips": "54067",
    "state": "WV",
    "county": "Nicholas"
  },
  {
    "fips": "72051",
    "state": "PR",
    "county": "Dorado"
  },
  {
    "fips": "26029",
    "state": "MI",
    "county": "Charlevoix"
  },
  {
    "fips": "08001",
    "state": "CO",
    "county": "Adams"
  },
  {
    "fips": "21165",
    "state": "KY",
    "county": "Menifee"
  },
  {
    "fips": "36051",
    "state": "NY",
    "county": "Livingston"
  },
  {
    "fips": "12125",
    "state": "FL",
    "county": "Union"
  },
  {
    "fips": "20113",
    "state": "KS",
    "county": "McPherson"
  },
  {
    "fips": "24025",
    "state": "MD",
    "county": "Harford"
  },
  {
    "fips": "39137",
    "state": "OH",
    "county": "Putnam"
  },
  {
    "fips": "48095",
    "state": "TX",
    "county": "Concho"
  },
  {
    "fips": "34031",
    "state": "NJ",
    "county": "Passaic"
  },
  {
    "fips": "49021",
    "state": "UT",
    "county": "Iron"
  },
  {
    "fips": "01035",
    "state": "AL",
    "county": "Conecuh"
  },
  {
    "fips": "17011",
    "state": "IL",
    "county": "Bureau"
  },
  {
    "fips": "33017",
    "state": "NH",
    "county": "Strafford"
  },
  {
    "fips": "29123",
    "state": "MO",
    "county": "Madison"
  },
  {
    "fips": "31029",
    "state": "NE",
    "county": "Chase"
  },
  {
    "fips": "06031",
    "state": "CA",
    "county": "Kings"
  },
  {
    "fips": "21063",
    "state": "KY",
    "county": "Elliott"
  },
  {
    "fips": "54021",
    "state": "WV",
    "county": "Gilmer"
  },
  {
    "fips": "30003",
    "state": "MT",
    "county": "Big Horn"
  },
  {
    "fips": "54039",
    "state": "WV",
    "county": "Kanawha"
  },
  {
    "fips": "05081",
    "state": "AR",
    "county": "Little River"
  },
  {
    "fips": "21145",
    "state": "KY",
    "county": "McCracken"
  },
  {
    "fips": "36105",
    "state": "NY",
    "county": "Sullivan"
  },
  {
    "fips": "19125",
    "state": "IA",
    "county": "Marion"
  },
  {
    "fips": "16045",
    "state": "ID",
    "county": "Gem"
  },
  {
    "fips": "29089",
    "state": "MO",
    "county": "Howard"
  },
  {
    "fips": "21083",
    "state": "KY",
    "county": "Graves"
  },
  {
    "fips": "21093",
    "state": "KY",
    "county": "Hardin"
  },
  {
    "fips": "36031",
    "state": "NY",
    "county": "Essex"
  },
  {
    "fips": "22021",
    "state": "LA",
    "county": "Caldwell"
  },
  {
    "fips": "38011",
    "state": "ND",
    "county": "Bowman"
  },
  {
    "fips": "51049",
    "state": "VA",
    "county": "Cumberland"
  },
  {
    "fips": "01127",
    "state": "AL",
    "county": "Walker"
  },
  {
    "fips": "22127",
    "state": "LA",
    "county": "Winn"
  },
  {
    "fips": "36049",
    "state": "NY",
    "county": "Lewis"
  },
  {
    "fips": "48005",
    "state": "TX",
    "county": "Angelina"
  },
  {
    "fips": "45035",
    "state": "SC",
    "county": "Dorchester"
  },
  {
    "fips": "51550",
    "state": "VA",
    "county": "Chesapeake"
  },
  {
    "fips": "27041",
    "state": "MN",
    "county": "Douglas"
  },
  {
    "fips": "72145",
    "state": "PR",
    "county": "Vega Baja"
  },
  {
    "fips": "01061",
    "state": "AL",
    "county": "Geneva"
  },
  {
    "fips": "20185",
    "state": "KS",
    "county": "Stafford"
  },
  {
    "fips": "31185",
    "state": "NE",
    "county": "York"
  },
  {
    "fips": "45089",
    "state": "SC",
    "county": "Williamsburg"
  },
  {
    "fips": "31091",
    "state": "NE",
    "county": "Hooker"
  },
  {
    "fips": "26083",
    "state": "MI",
    "county": "Keweenaw"
  },
  {
    "fips": "41043",
    "state": "OR",
    "county": "Linn"
  },
  {
    "fips": "13133",
    "state": "GA",
    "county": "Greene"
  },
  {
    "fips": "39161",
    "state": "OH",
    "county": "Van Wert"
  },
  {
    "fips": "48257",
    "state": "TX",
    "county": "Kaufman"
  },
  {
    "fips": "55139",
    "state": "WI",
    "county": "Winnebago"
  },
  {
    "fips": "26017",
    "state": "MI",
    "county": "Bay"
  },
  {
    "fips": "54017",
    "state": "WV",
    "county": "Doddridge"
  },
  {
    "fips": "01117",
    "state": "AL",
    "county": "Shelby"
  },
  {
    "fips": "13253",
    "state": "GA",
    "county": "Seminole"
  },
  {
    "fips": "13075",
    "state": "GA",
    "county": "Cook"
  },
  {
    "fips": "19069",
    "state": "IA",
    "county": "Franklin"
  },
  {
    "fips": "39071",
    "state": "OH",
    "county": "Highland"
  },
  {
    "fips": "48291",
    "state": "TX",
    "county": "Liberty"
  },
  {
    "fips": "19009",
    "state": "IA",
    "county": "Audubon"
  },
  {
    "fips": "26165",
    "state": "MI",
    "county": "Wexford"
  },
  {
    "fips": "55019",
    "state": "WI",
    "county": "Clark"
  },
  {
    "fips": "38013",
    "state": "ND",
    "county": "Burke"
  },
  {
    "fips": "39037",
    "state": "OH",
    "county": "Darke"
  },
  {
    "fips": "48389",
    "state": "TX",
    "county": "Reeves"
  },
  {
    "fips": "72053",
    "state": "PR",
    "county": "Fajardo"
  },
  {
    "fips": "39141",
    "state": "OH",
    "county": "Ross"
  },
  {
    "fips": "34019",
    "state": "NJ",
    "county": "Hunterdon"
  },
  {
    "fips": "26119",
    "state": "MI",
    "county": "Montmorency"
  },
  {
    "fips": "40071",
    "state": "OK",
    "county": "Kay"
  },
  {
    "fips": "37033",
    "state": "NC",
    "county": "Caswell"
  },
  {
    "fips": "55037",
    "state": "WI",
    "county": "Florence"
  },
  {
    "fips": "01095",
    "state": "AL",
    "county": "Marshall"
  },
  {
    "fips": "66010",
    "state": "GU",
    "county": "Guam"
  },
  {
    "fips": "13153",
    "state": "GA",
    "county": "Houston"
  },
  {
    "fips": "48225",
    "state": "TX",
    "county": "Houston"
  },
  {
    "fips": "02232",
    "state": "AK",
    "county": "Skagway-Hoonah-Angoon"
  },
  {
    "fips": "48143",
    "state": "TX",
    "county": "Erath"
  },
  {
    "fips": "13277",
    "state": "GA",
    "county": "Tift"
  },
  {
    "fips": "51155",
    "state": "VA",
    "county": "Pulaski"
  },
  {
    "fips": "29205",
    "state": "MO",
    "county": "Shelby"
  },
  {
    "fips": "48357",
    "state": "TX",
    "county": "Ochiltree"
  },
  {
    "fips": "17091",
    "state": "IL",
    "county": "Kankakee"
  },
  {
    "fips": "21171",
    "state": "KY",
    "county": "Monroe"
  },
  {
    "fips": "31043",
    "state": "NE",
    "county": "Dakota"
  },
  {
    "fips": "12109",
    "state": "FL",
    "county": "St. Johns"
  },
  {
    "fips": "40045",
    "state": "OK",
    "county": "Ellis"
  },
  {
    "fips": "51145",
    "state": "VA",
    "county": "Powhatan"
  },
  {
    "fips": "78020",
    "state": "VI",
    "county": "St. John"
  },
  {
    "fips": "21207",
    "state": "KY",
    "county": "Russell"
  },
  {
    "fips": "31159",
    "state": "NE",
    "county": "Seward"
  },
  {
    "fips": "51510",
    "state": "VA",
    "county": "Alexandria"
  },
  {
    "fips": "20201",
    "state": "KS",
    "county": "Washington"
  },
  {
    "fips": "22125",
    "state": "LA",
    "county": "West Feliciana"
  },
  {
    "fips": "46077",
    "state": "SD",
    "county": "Kingsbury"
  },
  {
    "fips": "12075",
    "state": "FL",
    "county": "Levy"
  },
  {
    "fips": "51115",
    "state": "VA",
    "county": "Mathews"
  },
  {
    "fips": "56021",
    "state": "WY",
    "county": "Laramie"
  },
  {
    "fips": "39083",
    "state": "OH",
    "county": "Knox"
  },
  {
    "fips": "13131",
    "state": "GA",
    "county": "Grady"
  },
  {
    "fips": "48117",
    "state": "TX",
    "county": "Deaf Smith"
  },
  {
    "fips": "51590",
    "state": "VA",
    "county": "Danville"
  },
  {
    "fips": "02110",
    "state": "AK",
    "county": "Juneau"
  },
  {
    "fips": "08113",
    "state": "CO",
    "county": "San Miguel"
  },
  {
    "fips": "55009",
    "state": "WI",
    "county": "Brown"
  },
  {
    "fips": "21159",
    "state": "KY",
    "county": "Martin"
  },
  {
    "fips": "12099",
    "state": "FL",
    "county": "Palm Beach"
  },
  {
    "fips": "18141",
    "state": "IN",
    "county": "St. Joseph"
  },
  {
    "fips": "48405",
    "state": "TX",
    "county": "San Augustine"
  },
  {
    "fips": "13263",
    "state": "GA",
    "county": "Talbot"
  },
  {
    "fips": "22017",
    "state": "LA",
    "county": "Caddo"
  },
  {
    "fips": "17043",
    "state": "IL",
    "county": "DuPage"
  },
  {
    "fips": "36063",
    "state": "NY",
    "county": "Niagara"
  },
  {
    "fips": "13275",
    "state": "GA",
    "county": "Thomas"
  },
  {
    "fips": "13307",
    "state": "GA",
    "county": "Webster"
  },
  {
    "fips": "20033",
    "state": "KS",
    "county": "Comanche"
  },
  {
    "fips": "16043",
    "state": "ID",
    "county": "Fremont"
  },
  {
    "fips": "28099",
    "state": "MS",
    "county": "Neshoba"
  },
  {
    "fips": "05017",
    "state": "AR",
    "county": "Chicot"
  },
  {
    "fips": "29015",
    "state": "MO",
    "county": "Benton"
  },
  {
    "fips": "40047",
    "state": "OK",
    "county": "Garfield"
  },
  {
    "fips": "08067",
    "state": "CO",
    "county": "La Plata"
  },
  {
    "fips": "18081",
    "state": "IN",
    "county": "Johnson"
  },
  {
    "fips": "19085",
    "state": "IA",
    "county": "Harrison"
  },
  {
    "fips": "34033",
    "state": "NJ",
    "county": "Salem"
  },
  {
    "fips": "50019",
    "state": "VT",
    "county": "Orleans"
  },
  {
    "fips": "19065",
    "state": "IA",
    "county": "Fayette"
  },
  {
    "fips": "37043",
    "state": "NC",
    "county": "Clay"
  },
  {
    "fips": "21091",
    "state": "KY",
    "county": "Hancock"
  },
  {
    "fips": "35047",
    "state": "NM",
    "county": "San Miguel"
  },
  {
    "fips": "48473",
    "state": "TX",
    "county": "Waller"
  },
  {
    "fips": "55099",
    "state": "WI",
    "county": "Price"
  },
  {
    "fips": "19135",
    "state": "IA",
    "county": "Monroe"
  },
  {
    "fips": "29103",
    "state": "MO",
    "county": "Knox"
  },
  {
    "fips": "30005",
    "state": "MT",
    "county": "Blaine"
  },
  {
    "fips": "39091",
    "state": "OH",
    "county": "Logan"
  },
  {
    "fips": "42041",
    "state": "PA",
    "county": "Cumberland"
  },
  {
    "fips": "26151",
    "state": "MI",
    "county": "Sanilac"
  },
  {
    "fips": "26095",
    "state": "MI",
    "county": "Luce"
  },
  {
    "fips": "30051",
    "state": "MT",
    "county": "Liberty"
  },
  {
    "fips": "48125",
    "state": "TX",
    "county": "Dickens"
  },
  {
    "fips": "48501",
    "state": "TX",
    "county": "Yoakum"
  },
  {
    "fips": "12007",
    "state": "FL",
    "county": "Bradford"
  },
  {
    "fips": "50003",
    "state": "VT",
    "county": "Bennington"
  },
  {
    "fips": "19131",
    "state": "IA",
    "county": "Mitchell"
  },
  {
    "fips": "28053",
    "state": "MS",
    "county": "Humphreys"
  },
  {
    "fips": "38015",
    "state": "ND",
    "county": "Burleigh"
  },
  {
    "fips": "48061",
    "state": "TX",
    "county": "Cameron"
  },
  {
    "fips": "47021",
    "state": "TN",
    "county": "Cheatham"
  },
  {
    "fips": "40077",
    "state": "OK",
    "county": "Latimer"
  },
  {
    "fips": "05089",
    "state": "AR",
    "county": "Marion"
  },
  {
    "fips": "47031",
    "state": "TN",
    "county": "Coffee"
  },
  {
    "fips": "35045",
    "state": "NM",
    "county": "San Juan"
  },
  {
    "fips": "06105",
    "state": "CA",
    "county": "Trinity"
  },
  {
    "fips": "20109",
    "state": "KS",
    "county": "Logan"
  },
  {
    "fips": "13049",
    "state": "GA",
    "county": "Charlton"
  },
  {
    "fips": "18115",
    "state": "IN",
    "county": "Ohio"
  },
  {
    "fips": "48437",
    "state": "TX",
    "county": "Swisher"
  },
  {
    "fips": "26047",
    "state": "MI",
    "county": "Emmet"
  },
  {
    "fips": "48087",
    "state": "TX",
    "county": "Collingsworth"
  },
  {
    "fips": "48217",
    "state": "TX",
    "county": "Hill"
  },
  {
    "fips": "69110",
    "state": "MP",
    "county": "Saipan"
  },
  {
    "fips": "20121",
    "state": "KS",
    "county": "Miami"
  },
  {
    "fips": "47069",
    "state": "TN",
    "county": "Hardeman"
  },
  {
    "fips": "47051",
    "state": "TN",
    "county": "Franklin"
  },
  {
    "fips": "72041",
    "state": "PR",
    "county": "Cidra"
  },
  {
    "fips": "22095",
    "state": "LA",
    "county": "St. John the Baptist"
  },
  {
    "fips": "42021",
    "state": "PA",
    "county": "Cambria"
  },
  {
    "fips": "08009",
    "state": "CO",
    "county": "Baca"
  },
  {
    "fips": "48065",
    "state": "TX",
    "county": "Carson"
  },
  {
    "fips": "16001",
    "state": "ID",
    "county": "Ada"
  },
  {
    "fips": "38031",
    "state": "ND",
    "county": "Foster"
  },
  {
    "fips": "29119",
    "state": "MO",
    "county": "McDonald"
  },
  {
    "fips": "48155",
    "state": "TX",
    "county": "Foard"
  },
  {
    "fips": "17201",
    "state": "IL",
    "county": "Winnebago"
  },
  {
    "fips": "51085",
    "state": "VA",
    "county": "Hanover"
  },
  {
    "fips": "36027",
    "state": "NY",
    "county": "Dutchess"
  },
  {
    "fips": "47001",
    "state": "TN",
    "county": "Anderson"
  },
  {
    "fips": "39041",
    "state": "OH",
    "county": "Delaware"
  },
  {
    "fips": "49033",
    "state": "UT",
    "county": "Rich"
  },
  {
    "fips": "01087",
    "state": "AL",
    "county": "Macon"
  },
  {
    "fips": "20117",
    "state": "KS",
    "county": "Marshall"
  },
  {
    "fips": "12005",
    "state": "FL",
    "county": "Bay"
  },
  {
    "fips": "13235",
    "state": "GA",
    "county": "Pulaski"
  },
  {
    "fips": "12017",
    "state": "FL",
    "county": "Citrus"
  },
  {
    "fips": "51037",
    "state": "VA",
    "county": "Charlotte"
  },
  {
    "fips": "01057",
    "state": "AL",
    "county": "Fayette"
  },
  {
    "fips": "46025",
    "state": "SD",
    "county": "Clark"
  },
  {
    "fips": "60010",
    "state": "AS",
    "county": "Eastern"
  },
  {
    "fips": "39001",
    "state": "OH",
    "county": "Adams"
  },
  {
    "fips": "13095",
    "state": "GA",
    "county": "Dougherty"
  },
  {
    "fips": "02050",
    "state": "AK",
    "county": "Bethel"
  },
  {
    "fips": "18097",
    "state": "IN",
    "county": "Marion"
  },
  {
    "fips": "12123",
    "state": "FL",
    "county": "Taylor"
  },
  {
    "fips": "21001",
    "state": "KY",
    "county": "Adair"
  },
  {
    "fips": "31101",
    "state": "NE",
    "county": "Keith"
  },
  {
    "fips": "30025",
    "state": "MT",
    "county": "Fallon"
  },
  {
    "fips": "05077",
    "state": "AR",
    "county": "Lee"
  },
  {
    "fips": "34011",
    "state": "NJ",
    "county": "Cumberland"
  },
  {
    "fips": "19181",
    "state": "IA",
    "county": "Warren"
  },
  {
    "fips": "35007",
    "state": "NM",
    "county": "Colfax"
  },
  {
    "fips": "37005",
    "state": "NC",
    "county": "Alleghany"
  },
  {
    "fips": "48403",
    "state": "TX",
    "county": "Sabine"
  },
  {
    "fips": "55137",
    "state": "WI",
    "county": "Waushara"
  },
  {
    "fips": "37171",
    "state": "NC",
    "county": "Surry"
  },
  {
    "fips": "40139",
    "state": "OK",
    "county": "Texas"
  },
  {
    "fips": "47053",
    "state": "TN",
    "county": "Gibson"
  },
  {
    "fips": "26133",
    "state": "MI",
    "county": "Osceola"
  },
  {
    "fips": "06065",
    "state": "CA",
    "county": "Riverside"
  },
  {
    "fips": "48321",
    "state": "TX",
    "county": "Matagorda"
  },
  {
    "fips": "47009",
    "state": "TN",
    "county": "Blount"
  },
  {
    "fips": "26043",
    "state": "MI",
    "county": "Dickinson"
  },
  {
    "fips": "42129",
    "state": "PA",
    "county": "Westmoreland"
  },
  {
    "fips": "21223",
    "state": "KY",
    "county": "Trimble"
  },
  {
    "fips": "39099",
    "state": "OH",
    "county": "Mahoning"
  },
  {
    "fips": "72027",
    "state": "PR",
    "county": "Camuy"
  },
  {
    "fips": "31015",
    "state": "NE",
    "county": "Boyd"
  },
  {
    "fips": "34005",
    "state": "NJ",
    "county": "Burlington"
  },
  {
    "fips": "54085",
    "state": "WV",
    "county": "Ritchie"
  },
  {
    "fips": "01037",
    "state": "AL",
    "county": "Coosa"
  },
  {
    "fips": "17177",
    "state": "IL",
    "county": "Stephenson"
  },
  {
    "fips": "55085",
    "state": "WI",
    "county": "Oneida"
  },
  {
    "fips": "37195",
    "state": "NC",
    "county": "Wilson"
  },
  {
    "fips": "42101",
    "state": "PA",
    "county": "Philadelphia"
  },
  {
    "fips": "39105",
    "state": "OH",
    "county": "Meigs"
  },
  {
    "fips": "47119",
    "state": "TN",
    "county": "Maury"
  },
  {
    "fips": "69120",
    "state": "MP",
    "county": "Tinian"
  },
  {
    "fips": "48441",
    "state": "TX",
    "county": "Taylor"
  },
  {
    "fips": "31073",
    "state": "NE",
    "county": "Gosper"
  },
  {
    "fips": "27047",
    "state": "MN",
    "county": "Freeborn"
  },
  {
    "fips": "13035",
    "state": "GA",
    "county": "Butts"
  },
  {
    "fips": "35037",
    "state": "NM",
    "county": "Quay"
  },
  {
    "fips": "21069",
    "state": "KY",
    "county": "Fleming"
  },
  {
    "fips": "31175",
    "state": "NE",
    "county": "Valley"
  },
  {
    "fips": "17135",
    "state": "IL",
    "county": "Montgomery"
  },
  {
    "fips": "37175",
    "state": "NC",
    "county": "Transylvania"
  },
  {
    "fips": "40097",
    "state": "OK",
    "county": "Mayes"
  },
  {
    "fips": "42027",
    "state": "PA",
    "county": "Centre"
  },
  {
    "fips": "20137",
    "state": "KS",
    "county": "Norton"
  },
  {
    "fips": "01025",
    "state": "AL",
    "county": "Clarke"
  },
  {
    "fips": "47045",
    "state": "TN",
    "county": "Dyer"
  },
  {
    "fips": "29203",
    "state": "MO",
    "county": "Shannon"
  },
  {
    "fips": "31039",
    "state": "NE",
    "county": "Cuming"
  },
  {
    "fips": "17013",
    "state": "IL",
    "county": "Calhoun"
  },
  {
    "fips": "18169",
    "state": "IN",
    "county": "Wabash"
  },
  {
    "fips": "27021",
    "state": "MN",
    "county": "Cass"
  },
  {
    "fips": "05003",
    "state": "AR",
    "county": "Ashley"
  },
  {
    "fips": "06095",
    "state": "CA",
    "county": "Solano"
  },
  {
    "fips": "01097",
    "state": "AL",
    "county": "Mobile"
  },
  {
    "fips": "40101",
    "state": "OK",
    "county": "Muskogee"
  },
  {
    "fips": "55105",
    "state": "WI",
    "county": "Rock"
  },
  {
    "fips": "46123",
    "state": "SD",
    "county": "Tripp"
  },
  {
    "fips": "51043",
    "state": "VA",
    "county": "Clarke"
  },
  {
    "fips": "13053",
    "state": "GA",
    "county": "Chattahoochee"
  },
  {
    "fips": "06103",
    "state": "CA",
    "county": "Tehama"
  },
  {
    "fips": "51091",
    "state": "VA",
    "county": "Highland"
  },
  {
    "fips": "29025",
    "state": "MO",
    "county": "Caldwell"
  },
  {
    "fips": "21057",
    "state": "KY",
    "county": "Cumberland"
  },
  {
    "fips": "17005",
    "state": "IL",
    "county": "Bond"
  },
  {
    "fips": "48363",
    "state": "TX",
    "county": "Palo Pinto"
  },
  {
    "fips": "27123",
    "state": "MN",
    "county": "Ramsey"
  },
  {
    "fips": "46097",
    "state": "SD",
    "county": "Miner"
  },
  {
    "fips": "48395",
    "state": "TX",
    "county": "Robertson"
  },
  {
    "fips": "28131",
    "state": "MS",
    "county": "Stone"
  },
  {
    "fips": "08007",
    "state": "CO",
    "county": "Archuleta"
  },
  {
    "fips": "35023",
    "state": "NM",
    "county": "Hidalgo"
  },
  {
    "fips": "47163",
    "state": "TN",
    "county": "Sullivan"
  },
  {
    "fips": "51710",
    "state": "VA",
    "county": "Norfolk"
  },
  {
    "fips": "51051",
    "state": "VA",
    "county": "Dickenson"
  },
  {
    "fips": "27173",
    "state": "MN",
    "county": "Yellow Medicine"
  },
  {
    "fips": "21009",
    "state": "KY",
    "county": "Barren"
  },
  {
    "fips": "20165",
    "state": "KS",
    "county": "Rush"
  },
  {
    "fips": "29053",
    "state": "MO",
    "county": "Cooper"
  },
  {
    "fips": "29165",
    "state": "MO",
    "county": "Platte"
  },
  {
    "fips": "05093",
    "state": "AR",
    "county": "Mississippi"
  },
  {
    "fips": "31119",
    "state": "NE",
    "county": "Madison"
  },
  {
    "fips": "47023",
    "state": "TN",
    "county": "Chester"
  },
  {
    "fips": "55057",
    "state": "WI",
    "county": "Juneau"
  },
  {
    "fips": "13207",
    "state": "GA",
    "county": "Monroe"
  },
  {
    "fips": "51670",
    "state": "VA",
    "county": "Hopewell"
  },
  {
    "fips": "08003",
    "state": "CO",
    "county": "Alamosa"
  },
  {
    "fips": "51065",
    "state": "VA",
    "county": "Fluvanna"
  },
  {
    "fips": "05067",
    "state": "AR",
    "county": "Jackson"
  },
  {
    "fips": "02280",
    "state": "AK",
    "county": "Wrangell-Petersburg"
  },
  {
    "fips": "19103",
    "state": "IA",
    "county": "Johnson"
  },
  {
    "fips": "23021",
    "state": "ME",
    "county": "Piscataquis"
  },
  {
    "fips": "31133",
    "state": "NE",
    "county": "Pawnee"
  },
  {
    "fips": "17027",
    "state": "IL",
    "county": "Clinton"
  },
  {
    "fips": "18161",
    "state": "IN",
    "county": "Union"
  },
  {
    "fips": "72061",
    "state": "PR",
    "county": "Guaynabo"
  },
  {
    "fips": "21047",
    "state": "KY",
    "county": "Christian"
  },
  {
    "fips": "37145",
    "state": "NC",
    "county": "Person"
  },
  {
    "fips": "18083",
    "state": "IN",
    "county": "Knox"
  },
  {
    "fips": "17087",
    "state": "IL",
    "county": "Johnson"
  },
  {
    "fips": "55097",
    "state": "WI",
    "county": "Portage"
  },
  {
    "fips": "23005",
    "state": "ME",
    "county": "Cumberland"
  },
  {
    "fips": "31019",
    "state": "NE",
    "county": "Buffalo"
  },
  {
    "fips": "56031",
    "state": "WY",
    "county": "Platte"
  },
  {
    "fips": "26163",
    "state": "MI",
    "county": "Wayne"
  },
  {
    "fips": "50007",
    "state": "VT",
    "county": "Chittenden"
  },
  {
    "fips": "05111",
    "state": "AR",
    "county": "Poinsett"
  },
  {
    "fips": "06001",
    "state": "CA",
    "county": "Alameda"
  },
  {
    "fips": "31005",
    "state": "NE",
    "county": "Arthur"
  },
  {
    "fips": "28035",
    "state": "MS",
    "county": "Forrest"
  },
  {
    "fips": "02020",
    "state": "AK",
    "county": "Anchorage"
  },
  {
    "fips": "21025",
    "state": "KY",
    "county": "Breathitt"
  },
  {
    "fips": "17097",
    "state": "IL",
    "county": "Lake"
  },
  {
    "fips": "17175",
    "state": "IL",
    "county": "Stark"
  },
  {
    "fips": "20191",
    "state": "KS",
    "county": "Sumner"
  },
  {
    "fips": "37173",
    "state": "NC",
    "county": "Swain"
  },
  {
    "fips": "17021",
    "state": "IL",
    "county": "Christian"
  },
  {
    "fips": "16065",
    "state": "ID",
    "county": "Madison"
  },
  {
    "fips": "48039",
    "state": "TX",
    "county": "Brazoria"
  },
  {
    "fips": "01081",
    "state": "AL",
    "county": "Lee"
  },
  {
    "fips": "34017",
    "state": "NJ",
    "county": "Hudson"
  },
  {
    "fips": "19059",
    "state": "IA",
    "county": "Dickinson"
  },
  {
    "fips": "46091",
    "state": "SD",
    "county": "Marshall"
  },
  {
    "fips": "18009",
    "state": "IN",
    "county": "Blackford"
  },
  {
    "fips": "19147",
    "state": "IA",
    "county": "Palo Alto"
  },
  {
    "fips": "13315",
    "state": "GA",
    "county": "Wilcox"
  },
  {
    "fips": "42115",
    "state": "PA",
    "county": "Susquehanna"
  },
  {
    "fips": "18147",
    "state": "IN",
    "county": "Spencer"
  },
  {
    "fips": "54047",
    "state": "WV",
    "county": "McDowell"
  },
  {
    "fips": "06113",
    "state": "CA",
    "county": "Yolo"
  },
  {
    "fips": "48477",
    "state": "TX",
    "county": "Washington"
  },
  {
    "fips": "55031",
    "state": "WI",
    "county": "Douglas"
  },
  {
    "fips": "18055",
    "state": "IN",
    "county": "Greene"
  },
  {
    "fips": "40081",
    "state": "OK",
    "county": "Lincoln"
  },
  {
    "fips": "54007",
    "state": "WV",
    "county": "Braxton"
  },
  {
    "fips": "48139",
    "state": "TX",
    "county": "Ellis"
  },
  {
    "fips": "51840",
    "state": "VA",
    "county": "Winchester"
  },
  {
    "fips": "35055",
    "state": "NM",
    "county": "Taos"
  },
  {
    "fips": "20103",
    "state": "KS",
    "county": "Leavenworth"
  },
  {
    "fips": "19027",
    "state": "IA",
    "county": "Carroll"
  },
  {
    "fips": "51173",
    "state": "VA",
    "county": "Smyth"
  }
    ]



    result = [
        item for item in county_map
        if item["state"] == state_short and item["county"] == County
    ]

    result_dict = result[0] if result else None

    folders = ["Clean_Script", "Cleaned_Data", "QA_Report", "Raw_Data", "Transformation"]

    progress = st.progress(0)
    status = st.empty()

    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create folders
    status.info("📁 Creating destination folders...")
    for folder in folders:
        os.makedirs(os.path.join(dest_base, folder), exist_ok=True)

    progress.progress(25)
    time.sleep(1)

    # Copy CSV
    status.info("📂 Copying CSV files...")
    raw_dest = os.path.join(dest_base, "Raw_Data")
    os.makedirs(raw_dest, exist_ok=True)

    csv_found = 0
    csv_copied = 0
    error_files = []
    valid_files = []

    if not os.path.exists(src_dir):
        st.error("❌ Source directory not found")
        st.stop()

    for file in os.listdir(src_dir):
        if file.lower().endswith(".csv"):
            csv_found += 1

            src_path = os.path.join(src_dir, file)
            dst_path = os.path.join(raw_dest, file)

            shutil.copy2(src_path, dst_path)
            csv_copied += 1

            errors = validate_filename(file, expected_short,result_dict)

            if errors:
                error_files.append((file, errors))
            else:
                valid_files.append(file)

    # progress.progress(70)
    # time.sleep(1)

    # progress.progress(100)
    # status.success("✅ Pipeline Completed Successfully")
    # st.snow()
    # st.toast("✅ Process completed!", icon="🎉")

    with st.spinner("Processing..."):
     time.sleep(2)

    st.toast("Done", icon="✅")
    # -------------------- SUMMARY --------------------
    st.markdown("## 📊 Pipeline Execution Summary")
    st.markdown(f"**Execution Time:** {execution_time}")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total CSV Found", csv_found)
    col2.metric("Total CSV Copied", csv_copied)
    col3.metric("Valid Files", len(valid_files))
    col4.metric("Files With Errors", len(error_files))

    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- CHART --------------------
    st.markdown("## 📈 Validation Overview")

    labels = ["Valid Files", "Error Files"]
    values = [len(valid_files), len(error_files)]

    # Center layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
     fig, ax = plt.subplots(figsize=(3, 3))  # 👈 smaller size

    ax.pie(
        values,
        labels=labels,
        autopct="%0.1f%%",
        textprops={'fontsize': 10},
        radius=0.9  # 👈 extra control
    )

    st.pyplot(fig, use_container_width=False)  # 👈 important


    # -------------------- VALID FILES --------------------
    if valid_files:
        st.markdown("### ✅ Valid CSV Files")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for file in valid_files:
            st.success(file)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------- ERROR FILES --------------------
    if error_files:
        st.markdown("### ❌ Filename Validation Errors")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        for file, errs in error_files:
            st.error(f"📄 {file}")
            for e in errs:
                st.write(f"- {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if csv_found > 0:
            st.success("🎉 All filenames are valid")
