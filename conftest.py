# conftest.py
import os
import pytest
from _pytest.runner import TestReport
from playwright.sync_api import sync_playwright
import pytest_html


@pytest.fixture(scope="session")
def playwright_browser_context_args():
    return {
        "viewport": {"width": 1366, "height": 740},
        "record_video_dir": "videos",
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def browser_context(playwright_browser_context_args):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./tmp_profile",
            headless=False,
            **playwright_browser_context_args
        )
        yield context
        context.close()

def pytest_sessionstart(session):
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("Logs", exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep: TestReport = outcome.get_result()

    # only attach on failures
    if rep.when == "call" and rep.failed:
        # find the current page from the test function
        page = item.funcargs.get("browser_context").pages[0]
        screenshot_dir = os.path.join("screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        file_name = f"{item.name}.png"
        screenshot_path = os.path.join(screenshot_dir, file_name)
        page.screenshot(path=screenshot_path, full_page=True)
        if os.path.exists(screenshot_path):
            extra = getattr(rep, "extra", [])
            html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:600px;height:auto;" /></div>'
            extra.append(pytest_html.extras.html(html))
            rep.extra = extra