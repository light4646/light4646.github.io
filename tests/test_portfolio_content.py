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

    def test_shipped_showcase_paints_no_panel_on_the_cream_page(self):
        showcase_rules = re.findall(r"\.shipped-showcase\s*\{([^{}]*)\}", HTML)
        self.assertTrue(showcase_rules, "Missing .shipped-showcase rule")
        for body in showcase_rules:
            self.assertNotRegex(
                body,
                r"background[^;:]*:",
                "the showcase must not paint its own panel — it sits directly on the cream page",
            )
            self.assertNotRegex(
                body,
                r"(?:\bborder[^;:]*|box-shadow)\s*:",
                "no panel chrome: the open section may not draw edges, radii, or shadows",
            )
            self.assertNotRegex(
                body,
                r"margin-(?:left|right)\s*:\s*-",
                "negative panel-bleed margins must go with the panel (overflow risk on the open page)",
            )

    def test_app_entries_paint_no_card_surface_on_the_open_page(self):
        self.assertNotIn("--card-glow", HTML, "the card glow belongs to the retired dark panel")
        card_rules = re.findall(r"\.app-card(?::hover)?\s*\{([^{}]*)\}", HTML)
        self.assertTrue(card_rules, "Missing .app-card rule")
        for body in card_rules:
            self.assertNotRegex(
                body,
                r"background[^;:]*:",
                "app entries must not paint gradients or fills — three open columns, not three cards",
            )
            self.assertNotRegex(
                body,
                r"(?:\bborder[^;:]*|box-shadow)\s*:",
                "app entries must not be outlined or shadowed boxes",
            )

    def test_showcase_text_uses_cream_page_ink_and_accent_tokens(self):
        for dark_panel_color in ("#79cbb7", "#bbb5a9", "#8e897e"):
            self.assertNotIn(
                dark_panel_color,
                HTML,
                f"{dark_panel_color} is dark-panel palette; the open section uses cream-page tokens",
            )
        scoped_rules = re.findall(
            r"(\.(?:shipped-showcase|shipped-head|app-card)[^{}<>\"']*)\{([^{}]*)\}", HTML
        )
        self.assertTrue(scoped_rules, "Missing showcase CSS rules")
        for selector, body in scoped_rules:
            for value in re.findall(r"(?<![\w-])color\s*:\s*([^;}]+)", body):
                self.assertRegex(
                    value.strip(),
                    r"^(?:var\(--(?:ink|ink-soft|accent|accent-deep)\)|inherit)$",
                    f"{selector.strip()} text must use the cream-page ink/accent tokens for readability",
                )

    def test_app_card_hover_never_repaints_a_surface(self):
        hover_rule = re.search(r"\.app-card:hover\s*\{([^{}]*)\}", HTML)
        if hover_rule is not None:
            declarations = hover_rule.group(1)
            self.assertNotRegex(
                declarations,
                r"background[^;:]*:",
                "hover must not summon a card surface on the open page",
            )
            self.assertNotIn(
                "--card-glow",
                declarations,
                "hover must not re-arm the retired dark-panel glow",
            )
            self.assertNotRegex(declarations, r"box-shadow\s*:")


if __name__ == "__main__":
    unittest.main()
