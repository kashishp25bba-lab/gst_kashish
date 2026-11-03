# GST Rate Finder & GST Calculator

A Python-based web application built using Streamlit.

## Features

### GST Rate Finder
- Search products by name.
- Display GST rate.
- Display GST applicability.
- Display HSN code.
- Show official source links.
- Clear and Reset buttons.
- Error message when a product is unavailable.

### GST Calculator
- Enter product price.
- Enter GST rate.
- Select Intra-State or Inter-State.
- Calculate CGST and SGST separately.
- Calculate IGST.
- Display total GST and final price.

## Technologies Used
- Python
- Streamlit
- Pandas

## Project Structure

```text
GST-Rate-Finder/
│
├── app.py
├── gst_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run the Project

1. Install Python.
2. Download or clone this repository.
3. Open the terminal in the project folder.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
streamlit run app.py
```

## Adding GST Product Data

Open `gst_data.csv` and add verified product information.

Required columns:

- product_name
- gst_rate
- applicability_status
- hsn_code
- source_name
- source_url
- last_verified

Only add information verified against official government
notifications or the CBIC GST rate schedule.

## Official Sources

- https://cbic-gst.gov.in/hindi/gst-goods-services-rates.html
- https://taxinformation.cbic.gov.in/
- https://tutorial.gst.gov.in/userguide/taxpayersdashboard/Search_HSN_SAC_Tax_Rates.htm

## Disclaimer

This application is an educational and informational tool.
Always verify the applicable GST rate and HSN classification
from current official government sources before using them
for taxation, billing or compliance.
