# pages/flight_results_page.py
from playwright.sync_api import Page
import json
from pathlib import Path

class FlightResultsPage:
    def __init__(self, page: Page):
        self.page = page

    def apply_non_stop_checkbox_filter(self):
        non_stop_checkbox = self.page.locator('//*[@id="mat-mdc-slide-toggle-1"]')
        non_stop_checkbox.click()
        print("Non-stop checkbox filter applied")

    def apply_non_stop_filter_via_popup(self):
        filter_button = self.page.locator("//button[contains(@class, 'filters-button')]//span[contains(text(), 'Filter')]")
        filter_button.wait_for(state="visible")
        filter_button.click()
        print("Filter popup opened")

        non_stop_radio = self.page.get_by_label("Nonstop only")
        non_stop_radio.wait_for(state="visible")
        non_stop_radio.check()
        print("Non-stop option selected in popup")

        apply_button = self.page.get_by_role("button", name="Apply")
        apply_button.wait_for(state="visible")
        apply_button.click()
        print("Apply button clicked in popup")

    def extract_flight_details(self):
        left_sections = self.page.locator('div.basic-flight-card-layout-left-top-section-container').element_handles()
        right_sections = self.page.locator('div.right-section').element_handles()
        flight_details = []

        for left, right in zip(left_sections, right_sections):
            try:
                flight_number = left.query_selector('.operating-airline-multiline span').inner_text().strip()
            except:
                flight_number = "N/A"

            try:
                departure_time = left.query_selector('.bound-departure-datetime').inner_text().strip()
            except:
                departure_time = "N/A"

            try:
                arrival_time = left.query_selector('.bound-arrival-datetime').inner_text().strip()
            except:
                arrival_time = "N/A"

            def get_price(class_name):
                try:
                    price_element = right.query_selector(f'.{class_name} .price-amount')
                    if price_element:
                        price_text = price_element.inner_text().strip()
                        return f"INR {price_text}"
                    return "N/A"
                except:
                    return "N/A"

            economy_price = get_price("eco")
            premium_economy_price = get_price("ecoPremium")
            business_price = get_price("business")

            flight_details.append({
                "flightNumber": flight_number,
                "departureTime": departure_time,
                "arrivalTime": arrival_time,
                "prices": {
                    "economy": economy_price,
                    "premiumEconomy": premium_economy_price,
                    "business": business_price
                }
            })

        log_dir = Path("Logs")
        log_dir.mkdir(exist_ok=True)

        json_file_path = log_dir / "FlightDetails.json"
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(flight_details, f, indent=2)
            print(f"Flight details saved to {json_file_path}")

        html_file_path = log_dir / "FlightDetails.html"
        html_content = f"""
        <html>
        <head><title>Flight Report</title></head>
        <body>
        <h1>Flight Search Report</h1>
        <pre>{json.dumps(flight_details, indent=2)}</pre>
        </body>
        </html>
        """
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            print(f"HTML report saved to {html_file_path}")

        return flight_details

    def capture_final_screenshot(self, filename: str):
        self.page.evaluate("window.scrollBy(0, 300)")
        self.page.wait_for_timeout(1000)
        self.page.screenshot(path=filename, full_page=True)
        print(f"Final screenshot taken: {filename}")
