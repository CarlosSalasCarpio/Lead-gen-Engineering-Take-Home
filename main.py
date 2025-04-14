import asyncio
import pandas as pd
import csv
from playwright.async_api import async_playwright

LIMIT = 50
OUTPUT_FILE = "clinics.csv"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.bhcoe.org/aba-therapy-directory/")
        await page.wait_for_timeout(4000)

        previous_count = -1
        retry_count = 0

        # Scroll and click "Load More" until reaching LIMIT (not counting duplicates)
        while True:
            items = await page.query_selector_all("article.dp-dfg-item")
            print(f"Clinics found on page: {len(items)}")

            if len(items) >= LIMIT * 2:  # Load more than necessary to compensate for deduplication
                print(f"Reached upper fetch limit. Proceeding to data extraction.")
                break

            if len(items) == previous_count:
                retry_count += 1
                if retry_count >= 2:
                    print("No more clinics added after retries.")
                    break
            else:
                retry_count = 0

            previous_count = len(items)

            try:
                load_more = await page.query_selector("a.dp-dfg-load-more-button")
                if not load_more:
                    print("'Load More' button not found.")
                    break

                print("Clicking 'Load More'")
                await load_more.scroll_into_view_if_needed()
                await load_more.click()
                await page.wait_for_timeout(4000)

            except Exception as e:
                print(f"Error clicking 'Load More': {e}")
                break

        items = await page.query_selector_all("article.dp-dfg-item")
        seen_names = set()
        data = []
        detail_page = await browser.new_page()

        for item in items:
            if len(data) >= LIMIT:
                break

            try:
                name_el = await item.query_selector(".dp-dfg-header")
                location_el = await item.query_selector(".city-state")
                link_el = await item.query_selector(".entry-title a")

                name = await name_el.inner_text() if name_el else ""
                location = await location_el.inner_text() if location_el else ""
                detail_url = await link_el.get_attribute("href") if link_el else ""

                # Skip if name already seen
                if name.strip() in seen_names:
                    continue
                seen_names.add(name.strip())

                address = ""
                website = ""

                if detail_url:
                    try:
                        await detail_page.goto(detail_url, timeout=60000)
                        await detail_page.wait_for_timeout(3000)

                        address_el = await detail_page.query_selector(
                            "a[href^='https://maps.google.com/maps?q=']"
                        )
                        address = await address_el.inner_text() if address_el else ""

                        website_el = await detail_page.query_selector(
                            "a[href*='utm_source=BHCOE-ABA-directory']"
                        )
                        website = await website_el.get_attribute("href") if website_el else ""

                    except Exception as e:
                        print(f"Error visiting detail page: {e}")

                data.append({
                    "Name": name.strip(),
                    "Location": location.strip(),
                    "Address": address.strip(),
                    "URL": website.strip() or detail_url.strip()
                })

                print(f"{len(data)}. {name.strip()}")

            except Exception as e:
                print(f"Error processing clinic: {e}")

        await browser.close()

        df = pd.DataFrame(data)
        df.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL)
        print(f"CSV file saved to: {OUTPUT_FILE}")

asyncio.run(main())