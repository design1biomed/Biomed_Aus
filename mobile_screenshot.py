from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # iPhone 13 Pro viewport
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()
        page.goto('http://127.0.0.1:8001/')
        page.wait_for_timeout(2000)
        page.screenshot(path='mobile_index.png', full_page=True)
        browser.close()

if __name__ == '__main__':
    run()
