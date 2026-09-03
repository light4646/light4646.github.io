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

    def test_fresh_page_load_settles_on_the_nour_zaki_hero(self):
        self.assertIn('id="home"', HTML)
        self.assertIn("history.replaceState(null, '', location.pathname + location.search)", HTML)
        self.assertIn("scrollTo({ top: 0, left: 0, behavior: 'instant' })", HTML)

    def test_app_grid_has_no_frame_border_or_seam_chrome(self):
        grid_rules = re.findall(r"\.app-grid\s*\{([^}]*)\}", HTML)
        self.assertTrue(grid_rules, "Missing .app-grid rule")
        for body in grid_rules:
            self.assertNotRegex(
                body,
                r"background[^;:]*:",
                "a painted .app-grid surface shows through the gaps as divider seams",
            )
            self.assertNotRegex(
                body,
                r"(?:\bborder[^;:]*|\boutline[^;:]*|box-shadow)\s*:",
                "nothing may draw a hard outer rectangle around the app grid",
            )
        gap = re.search(r"gap:\s*([\d.]+)px", grid_rules[0])
        self.assertIsNotNone(gap, "Expected a px gap between app cards")
        self.assertGreaterEqual(
            float(gap.group(1)),
            16,
            "hairline gaps read as panel seam lines; separate cards with real spacing",
        )

    def test_app_cards_fade_into_the_showcase_instead_of_boxed_panel_fills(self):
        card_rules = re.findall(r"\.app-card\s*\{([^}]*)\}", HTML)
        self.assertTrue(card_rules, "Missing .app-card rule")
        for body in card_rules:
            self.assertNotRegex(
                body,
                r"background[^;:]*:\s*#",
                "a solid fill reads as a panel pasted onto the showcase ink",
            )
            self.assertNotRegex(body, r"\bborder[^;:]*:", "cards must not be outlined boxes")
        base_rule = card_rules[0]
        self.assertRegex(
            base_rule,
            r"background\s*:[^;]*gradient",
            "cards should keep a deliberate soft tonal gradient, not vanish entirely",
        )
        self.assertRegex(
            base_rule,
            r"rgba\([^)]*,\s*0\s*\)|transparent",
            "the card gradient must fade fully into the surrounding showcase ink",
        )

    def test_app_card_hover_response_stays_soft_and_boxless(self):
        hover_rule = re.search(r"\.app-card:hover\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(hover_rule, "Missing .app-card:hover rule — keep a subtle hover response")
        declarations = hover_rule.group(1)
        self.assertNotIn("translate", declarations)
        self.assertNotIn("scale(", declarations)
        self.assertNotRegex(
            declarations,
            r"background[^;:]*:\s*#",
            "hover must intensify the fade, not repaint the card as a solid box",
        )
        self.assertRegex(declarations, r"[\w-]+\s*:", "hover rule must declare an actual response")


if __name__ == "__main__":
    unittest.main()
