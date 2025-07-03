# pages/home_page.py
from playwright.sync_api import Page
from pages.flight_results_page import FlightResultsPage
import random
import time

class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_randomly(self):
        delay = random.randint(800, 30000)
        time.sleep(delay / 1000.0)

    def prepare_page_stealth(self):
        self.page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })
        self.page.context.set_default_timeout(10000)
        self.page.context.grant_permissions(['geolocation'], origin="https://www.airindia.com")
        print("Stealth settings applied")

    def accept_cookies(self):
        try:
            accept_button = self.page.locator("#onetrust-accept-btn-handler")
            if accept_button.is_visible(timeout=5000):
                accept_button.click()
                print("Clicked Accept All cookies button")

                # Wait for the dark overlay to disappear
                overlay = self.page.locator(".onetrust-pc-dark-filter")
                overlay.wait_for(state="hidden", timeout=10000)
                print("Cookie dark overlay is now hidden")

                # also wait for the entire consent modal to disappear
                consent_box = self.page.locator("#onetrust-consent-sdk")
                consent_box.wait_for(state="hidden", timeout=10000)
                print("Cookie consent SDK hidden")
            else:
                print("Cookie button not visible, skipping")
        except Exception as e:
            print(f"accept_cookies error: {e}")


    def setup_geolocation_permissions(self):
        def dialog_handler(dialog):
            if dialog.type == 'permission':
                dialog.accept()
                print("Geolocation permission granted automatically")
            else:
                dialog.dismiss()
                print("Unknown dialog dismissed")
        self.page.on("dialog", dialog_handler)
        self.page.context.grant_permissions(['geolocation'], origin="https://www.airindia.com")
        print("Geolocation permission granted")

    def select_trip_type(self, trip_type: str):
        self.page.get_by_label(trip_type).click()
        print(f"Selected Trip Type: {trip_type}")

    # def select_date(self, month_value, weekday, month, day):
    #     date_field = self.page.locator("//input[@id='dpFromDate' and @name='dpFrom' and @placeholder='Select Date']").first
    #     date_field.wait_for(state='visible')
    #     date_field.click()
    #     print("Calendar opened")

    #     month_dropdown = self.page.locator('select[title="month-dropdown"]')
    #     month_dropdown.wait_for(state='visible')
    #     month_dropdown.select_option(month_value)
    #     print(f"Selected month: {month_value}")

    #     label_prefix = f"{weekday}, {month} {day},"
    #     date_locator = self.page.locator(f"//div[@role='gridcell' and starts-with(@aria-label, '{label_prefix}')]//div[contains(@class, 'custom-day') and contains(@class, 'locked')]")
    #     date_locator.wait_for(state='visible')
    #     date_locator.click()
    #     print(f"Selected date: {weekday}, {month} {day}")
    def select_date(
        self,
        month_value,
        weekday,
        month,
        day,
        return_month_value=None,
        return_weekday=None,
        return_month=None,
        return_day=None
    ):
        date_field = self.page.locator("//input[@id='dpFromDate' and @name='dpFrom' and @placeholder='Select Date']").first
        date_field.wait_for(state='visible')
        date_field.click()
        print("Calendar opened")

        month_dropdown = self.page.locator('select[title="month-dropdown"]')
        month_dropdown.wait_for(state='visible')
        month_dropdown.select_option(month_value)
        print(f"Selected month: {month_value}")

        label_prefix = f"{weekday}, {month} {day},"
        date_locator = self.page.locator(f"//div[@role='gridcell' and starts-with(@aria-label, '{label_prefix}')]//div[contains(@class, 'custom-day') and contains(@class, 'locked')]")
        date_locator.wait_for(state='visible')
        date_locator.click()
        print(f"Selected date: {weekday}, {month} {day}")

        # if Round Trip return date
        # if return_month_value and return_weekday and return_month and return_day:

        if return_month_value and return_weekday and return_month and return_day:
            self.page.wait_for_timeout(2000)

            # robustly wait for any dpToDate to appear
            return_date_field = self.page.locator("//input[@id='dpToDate' and @name='dpTo' and @placeholder='Select Date']").first
            return_date_field.wait_for(state="visible", timeout=10000)
            return_date_field.click()
            print("Return date input is now visible")

            # use first() to be safe (there may be multiple but they will be identical once visible)
            return_date_field.first.wait_for(state="attached", timeout=5000)
            
            # # wait for the attribute
            # self.page.wait_for_function(
            #     """selector => {
            #         const el = document.querySelectorAll(selector)[1];
            #         return el && !el.disabled;
            #     }""",
            #     arg='input#dpToDate[name="dpTo"]',
            #     timeout=5000
            # )
            # print("Return date input is now enabled")

            # # click the second input
            # return_date_field.nth(1).click()
            print("Calendar opened for return date")

            return_month_dropdown = self.page.locator('select[title="month-dropdown"]')
            return_month_dropdown.wait_for(state='visible')
            return_month_dropdown.select_option(return_month_value)
            print(f"Selected return month: {return_month_value}")

            return_label_prefix = f"{return_weekday}, {return_month} {return_day},"
            return_date_locator = self.page.locator(
                f"//div[@role='gridcell' and starts-with(@aria-label, '{return_label_prefix}')]//div[contains(@class, 'custom-day') and contains(@class, 'locked')]"
            )
            return_date_locator.wait_for(state='visible')
            return_date_locator.click()
            print(f"Selected return date: {return_weekday}, {return_month} {return_day}")


    def enter_from_city(self, city):
        from_input = self.page.locator('div.ai-input-wrap >> input[data-id="ai-autocomplete-input-FROM"]')
        from_input.wait_for(state='visible')
        from_input.click()
        print('Clicked on "From" input')
        for c in city:
            from_input.type(c, delay=100)
        time.sleep(1.5)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        print(f'"From" city selected: {city}')

    def enter_to_city(self, city):
        to_input = self.page.locator('input[data-id="ai-autocomplete-input-TO"]')
        to_input.wait_for(state='visible')
        to_input.click()
        print('Clicked on "To" input')
        for c in city:
            to_input.type(c, delay=100)
        time.sleep(1.5)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        print(f'"To" city selected: {city}')

    def click_search(self):
        search_button = self.page.locator('button.ai-basic-button.ai-btn-full-width:has-text("Search")')
        search_button.wait_for(state='visible')
        search_button.click()
        print("Clicked Search")

    def get_flight_results(self):
        return FlightResultsPage(self.page)
