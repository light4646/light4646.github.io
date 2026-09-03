import re
import unittest
from pathlib import Path


HTML = (Path(__file__).parent.parent / "index.html").read_text(encoding="utf-8")


class PortfolioContentTests(unittest.TestCase):
    def test_page_declares_a_favicon_to_avoid_browser_404s(self):
        self.assertIn('<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">', HTML)

    def test_all_three_published_apps_are_featured_with_store_links(self):
        apps = {
            "Caduceus — MCAT Arena": "https://apps.apple.com/us/app/caduceus-mcat-arena/id6780739539",
            "Crown — DAT Arena": "https://apps.apple.com/us/app/crown-dat-arena/id6783618704",
            "Apex — Focus Racing": "https://apps.apple.com/us/app/apex-focus-racing/id6784372545",
        }
        self.assertEqual(HTML.count('class="app-card"'), 3)
        for name, url in apps.items():
            self.assertIn(name, HTML)
            self.assertIn(url, HTML)

    def test_app_showcase_has_a_direct_developer_portfolio_link(self):
        self.assertIn("Three apps. Built and shipped by one developer.", HTML)
        self.assertIn(
            "https://apps.apple.com/us/developer/nour-zaki/id6780739541",
            HTML,
        )

    def test_light_is_presented_as_a_featured_working_ai_system(self):
        self.assertIn("Light — Personal AI Operating System", HTML)
        self.assertIn('class="proj proj-light"', HTML)
        for capability in (
            "persistent memory",
            "tool orchestration",
            "scheduled automations",
            "coding workflows",
        ):
            self.assertRegex(HTML, re.compile(capability, re.IGNORECASE))
        self.assertNotIn(">Personal Assistant<", HTML)

    def test_ios_work_filter_exists(self):
        self.assertIn('data-filter="ios"', HTML)
        self.assertGreaterEqual(HTML.count('data-cat="ios"'), 3)


if __name__ == "__main__":
    unittest.main()
