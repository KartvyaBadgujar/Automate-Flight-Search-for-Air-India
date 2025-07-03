# Air India Flight Search Automation

This project automates the Air India website’s flight search feature using **Playwright with Python**. It covers both One Way and Round Trip flows, applies filters, captures flight details, and generates comprehensive reports.

---

## 🚀 Features

-   **Automated Search Flows**: Seamlessly handles both **One Way** and **Round Trip** flight searches.
-   **Dynamic Element Handling**: Robustly selects departure and return dates from interactive calendars.
-   **City Selection**: Accurately enters origin and destination cities.
-   **Advanced Filtering**: Applies **non-stop flight** filters to refine search results.
-   **Data Extraction**: Efficiently extracts and logs all available flight data (flight number, duration, price, etc.).
-   **Evidence Generation**: Automatically captures screenshots and video recordings of the test execution.
-   **Reporting**: Generates detailed **HTML** and **JSON** reports for analysis.
-   **Page Object Model (POM)**: Built with a modular and maintainable POM structure.

---

## 📂 Project Structure

```bash
AirIndia-Flight-Search-Automation/
├── Logs/
│   ├── FlightDetails.html
│   └── FlightDetails.json
├── pages/
│   ├── flight_results_page.py
│   └── home_page.py
├── reports/
│   └── report.html
├── screenshots/
│   └── search_results.png
├── tests/
│   └── test_flight_search.py
├── videos/
│   └── test_flight_search.mp4
├── .gitignore
├── conftest.py
├── pytest.ini
└── requirements.txt
````

-----

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

### 1\. Prerequisites

  - Python 3.10+
  - `pip` and `venv` installed

### 2\. Clone the Repository

```bash
git clone [[https://github.com/yourusername/AirIndia-Flight-Search-Automation.git](https://github.com/yourusername/AirIndia-Flight-Search-Automation.git)](https://github.com/KartvyaBadgujar/Automate-Flight-Search-for-Air-India.git)
cd AirIndia-Flight-Search-Automation
```

### 3\. Set Up a Virtual Environment

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4\. Install Dependencies

Install all required packages and browser binaries for Playwright.

```bash
pip install -r requirements.txt
playwright install
```

### 5\. Run the Tests

Execute the automated tests using `pytest`. The command below will also generate an HTML report.

```bash
pytest tests/test_flight_search.py
```

-----

## 📝 Test Scenarios Covered

  - ✅ **One Way Search**: Successfully searches for a one-way flight from Delhi (DEL) to Mumbai (BOM).
  - ✅ **Round Trip Search**: Successfully searches for a round-trip flight from Delhi (DEL) to Mumbai (BOM).
  - ✅ **Filter Application**: Correctly applies the "Non-stop" flight filter.
  - ✅ **Date Selection**: Accurately picks dates using the calendar widget.
  - ✅ **Evidence Capture**: Generates screenshots of the flight search results.
  - ✅ **Data Logging**: Creates JSON and HTML reports containing the extracted flight details.

-----

## 🧩 Tools & Technologies

  - **Automation Framework**: [Playwright](https://playwright.dev/python/)
  - **Test Runner**: [Pytest](https://docs.pytest.org/)
  - **Reporting**: [pytest-html](https://pytest-html.readthedocs.io/)
  - **Language**: [Python 3.11](https://www.python.org/)
  - **Version Control**: [Git & GitHub](https://github.com/)

-----

## 📊 Reports & Logs

After a successful test run, you can find the generated artifacts in the following directories:

  - **HTML Reports**: `reports/`
  - **Screenshots**: `screenshots/`
  - **Flight Data Logs**: `Logs/` (in both JSON and HTML formats)

-----
