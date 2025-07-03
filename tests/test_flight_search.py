import re
import pytest
from pages.home_page import HomePage
from pages.flight_results_page import FlightResultsPage
from pathlib import Path
import time

def test_flight_search_oneway(browser_context):
    page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
    page.set_default_timeout(600000)

    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
    """)

    homepage = HomePage(page)
    page.goto("https://www.airindia.com", timeout=60000)
    homepage.prepare_page_stealth()
    try:
        page.click("button:has-text('Accept')", timeout=5000)
    except:
        print("No cookie popup detected, proceeding.")

    homepage.select_trip_type("One Way")

    homepage.select_date(
        month_value="7-2025",
        weekday="Tuesday",
        month="July",
        day=8
    )

    homepage.setup_geolocation_permissions()
    homepage.enter_from_city("Delhi")
    homepage.enter_to_city("Mumbai")

    # with page.expect_navigation(url=r"/booking/availability/\d+", timeout=20000):
    #     homepage.click_search()
    homepage.click_search()

    page.wait_for_url(re.compile(r"/booking/availability/.*"), timeout=30000)

    # page.locator("div.basic-flight-card-layout-left-top-section-container").wait_for(
    #     state="visible", timeout=15000
    # )   


    assert "/booking/availability/" in page.url

    flight_results_page = FlightResultsPage(page)
    flight_results_page.apply_non_stop_checkbox_filter()
    flight_results_page.apply_non_stop_filter_via_popup()
    flight_details = flight_results_page.extract_flight_details()
    assert len(flight_details) > 0, "No flights were found."
    Path("screenshots").mkdir(exist_ok=True)
    flight_results_page.capture_final_screenshot("screenshots/final_oneway.png")
    print("✅ One Way test completed successfully")


def test_flight_search_roundtrip(browser_context):
    page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
    page.set_default_timeout(600000)

    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
    """)

    homepage = HomePage(page)
    page.goto("https://www.airindia.com", timeout=60000)
    homepage.prepare_page_stealth()
    try:
        page.click("button:has-text('Accept')", timeout=5000)
    except:
        print("No cookie popup detected, proceeding.")

    homepage.select_trip_type("Round Trip")
    # time.sleep(2)

    homepage.select_date(
        month_value="7-2025",
        weekday="Friday",
        month="July",
        day=18,
        return_month_value="8-2025",
        return_weekday="Monday",
        return_month="August",
        return_day=4
    )


    homepage.setup_geolocation_permissions()
    homepage.enter_from_city("Delhi")
    homepage.enter_to_city("Mumbai")

    homepage.click_search()

    page.wait_for_url(re.compile(r"/booking/availability/.*"), timeout=30000)

    assert "/booking/availability/" in page.url

    flight_results_page = FlightResultsPage(page)
    flight_results_page.apply_non_stop_checkbox_filter()
    flight_results_page.apply_non_stop_filter_via_popup()
    flight_details = flight_results_page.extract_flight_details()
    assert len(flight_details) > 0, "No flights were found."
    Path("screenshots").mkdir(exist_ok=True)
    flight_results_page.capture_final_screenshot("screenshots/final_roundtrip.png")
    print("✅ Round Trip test completed successfully")
