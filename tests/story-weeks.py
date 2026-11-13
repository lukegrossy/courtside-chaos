"""Mobile WebKit story regressions. Run with python tests/story-weeks.py."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from time import monotonic
import unittest

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SHOTS = Path("/tmp/courtside-story-weeks")
STATS = "#stSeason,#stWeek,#stRecord,#stCash,#stMorale,#stBuzz,#stCred"
# Positions in the 192 x 366 portrait canvas, including the 34px header.
PUPS = [(57, 110), (42, 200), (67, 260), (141, 260), (161, 200), (147, 110)]


class StoryWeeks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0),
                                         partial(SimpleHTTPRequestHandler, directory=ROOT))
        Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.pw = sync_playwright().start()
        cls.addClassCleanup(cls.pw.stop)
        cls.browser = cls.pw.webkit.launch()
        cls.addClassCleanup(cls.browser.close)
        SHOTS.mkdir(exist_ok=True, parents=True)

    def setUp(self):
        self.page = self.browser.new_page(**self.pw.devices["iPhone 13"], reduced_motion="reduce")
        self.page.route("**/*", lambda route: route.continue_() if route.request.url.startswith(
                f"http://127.0.0.1:{self.server.server_port}/") else route.abort())
        self.addCleanup(self.page.close)
        self.addCleanup(self.shot, "last-screen")
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.goto(f"http://127.0.0.1:{self.server.server_port}", wait_until="domcontentloaded")
        self.ui = self.page.locator

    def tearDown(self):
        self.assertEqual(self.errors, [])

    def shot(self, label):
        self.page.screenshot(path=SHOTS / f"{self._testMethodName}-{label}.png")

    def resume(self):
        self.page.reload(wait_until="domcontentloaded")
        dialogs = []
        def confirm(dialog):
            dialogs.append(dialog.message)
            dialog.accept()
        self.page.once("dialog", confirm)
        self.ui("#startbtn").tap()
        self.assertEqual(dialogs, ["Resume your saved franchise? Choose Cancel to start a new game."])

    def start_week(self, week, story=None):
        # Only the starting checkpoint is synthetic. A null story lets the
        # actual scheduler deal Week 2. Week 4 starts before Sandra gives notice.
        state = dict(cash=40000, morale=72, buzz=48, cred=36, season=1,
                     week=week, tw=week, wins=week-1, losses=0, streak=1,
                     venue="HOME", foe="FARGO", stage="regular", debtWeeks=0,
                     flags={}, done={}, met={"sandra": True, "ricky": True},
                     triggeredAt={}, champs=0)
        self.page.evaluate("(save) => localStorage.setItem('courtside_save', JSON.stringify(save))",
                           dict(v=4, S=state, cur=story, deckIds=[], deckPos=0))
        self.resume()
        expect(self.ui("#dash.on #stWeek")).to_have_text(f"{week:02d}")

    def choose_a(self):
        self.ui("#dash.on #callBtn").tap()
        self.ui("#decide.on #dA").tap()

    def finish_week(self):
        deadline = monotonic() + 45
        while monotonic() < deadline:
            if self.ui("#dash.on #nextBtn").is_visible():
                return
            for selector in ("#moment.on #mA", "#caw.on", "#gazS.on"):
                screen = self.ui(selector)
                if screen.count():
                    screen.tap(position={"x": 12, "y": 60})
                    break
            self.page.wait_for_timeout(100)
        self.fail("No postgame dashboard. Active screens: " +
                  str(self.ui(".screen.on").evaluate_all("els => els.map(el => el.id)")))

    def art(self, selector, suffix):
        img = self.ui(f"{selector}[src$='{suffix}']")
        expect(img).to_be_visible()
        img.evaluate("img => img.decode()")
        expect(img).to_have_css("opacity", "1")

    def test_possum(self):
        self.start_week(2)
        expect(self.ui("#noteh")).to_have_text("THE FUSE BOX")
        self.choose_a()
        frame = self.ui("#mgOverlay.on #mgFrame[src*='possum-fusebox.html']")
        canvas = frame.content_frame.locator("#game.on #c")
        expect(canvas).to_be_visible()
        box = canvas.bounding_box()
        self.assertGreater(box["height"], box["width"])
        stage = self.ui("#stage").bounding_box()
        for dimension in ("width", "height"):
            self.assertAlmostEqual(frame.bounding_box()[dimension], stage[dimension], delta=1)
        self.shot("cabinet")

        # Read the visible green pilot tabs and tap their pups. The game
        # handles all hit testing, rescue animation and session messages.
        read_safe = """(c, pups) => {
          const ctx = c.getContext('2d');
          const scale = c.width / 192;
          for (const [x,y] of pups) {
            const [r,g,b] = ctx.getImageData((x+8)*scale,(y+9)*scale,1,1).data;
            if (g > r+25 && g > b+40) return [x,y];
          }
          return null;
        }"""
        remaining = PUPS.copy()
        crate = frame.content_frame.locator("#crate .full")
        deadline = monotonic() + 25
        while remaining and monotonic() < deadline:
            # The last pup is always safe and can be tapped directly.
            target = remaining[0] if len(remaining) == 1 else canvas.evaluate(read_safe, remaining)
            if target:
                x, y = target
                self.page.touchscreen.tap(box["x"] + box["width"] * x/192,
                                          box["y"] + box["height"] * y/366)
                if crate.count() == 7-len(remaining):
                    remaining.remove((x,y))
            self.page.wait_for_timeout(70)
        self.assertEqual(remaining, [], "Six pups must reach the crate")
        expect(self.ui("#mgFrame")).to_have_attribute("src", "about:blank")
        expect(self.ui("#caw.on #cawTxt")).to_contain_text("Six babies, one crate")
        self.finish_week()
        expect(self.ui("#notescroll")).to_contain_text("reached into a live panel")
        self.art("#dash.on #portrait", "/sandra/season-one/pleased.webp")
        expect(self.ui("#nextBtn .txt")).to_have_text("NEXT WEEK")
        self.shot("result")

    def handover(self, animated):
        self.start_week(4, "ricky_statue")
        self.choose_a()
        self.finish_week()
        expect(self.ui("#notescroll")).to_contain_text("Grace is covering")
        if animated:
            self.page.emulate_media(reduced_motion="no-preference")
        self.ui("#nextBtn").tap()
        card = self.ui("#caw.on.handover")
        expect(card.locator("#cawName")).to_have_text("SANDRA")
        self.art("#cawPort.show", "cutscenes/sandra_departure.webp")
        film = self.ui("#departureFilm")
        if animated:
            expect(film).to_be_visible()
            self.page.wait_for_function("""() => {
              const v = document.querySelector('#departureFilm');
              return v.currentSrc.endsWith('/sandra_departure.mp4') && v.playsInline &&
                     !v.paused && !v.error && v.videoWidth > 0 && v.currentTime > .2;
            }""", timeout=8000)
        else:
            expect(film).to_be_hidden()
        self.shot("departure")
        card.tap()
        if animated:
            expect(self.ui("#caw")).to_have_css("opacity", "0")
        expect(card.locator("#cawName")).to_have_text("GRACE")
        self.art("#cawPort.show", "cutscenes/grace_owner_office.webp")
        expect(film).to_be_hidden()
        self.assertTrue(film.evaluate("v => v.paused"))
        expect(card).to_have_css("opacity", "1")
        self.shot("intro")
        card.tap()
        self.assert_grace_desk()

    def assert_grace_desk(self):
        expect(self.ui("#dash.on #stWeek")).to_have_text("05")
        expect(self.ui("#dash.on #noteh")).to_have_text("SANDRA'S WEEK OFF")
        self.art("#dash.on #portrait", "grace/owner-office.webp")
        expect(self.ui("#callBtn")).to_be_visible()
        expect(self.ui("#caw.on")).to_have_count(0)

    def test_grace_film(self):
        self.handover(animated=True)

    def test_grace_continuity(self):
        self.handover(animated=False)
        stats = self.ui(STATS).all_text_contents()
        note = self.ui("#notescroll").inner_text()
        self.resume()
        self.assert_grace_desk()
        self.assertEqual(stats, self.ui(STATS).all_text_contents())
        self.assertEqual(note, self.ui("#notescroll").inner_text())
        self.shot("resumed-desk")
        self.choose_a()
        self.finish_week()
        expect(self.ui("#notescroll")).to_contain_text("Sandra's back Monday")
        self.art("#dash.on #portrait", "grace/owner-office.webp")
        self.shot("completed-result")
        self.ui("#nextBtn").tap()
        # Depending on the scheduler, Sandra may introduce a supporting cast
        # member before the next setup is shown.
        self.page.wait_for_selector("#caw.on.cardmode, #dash.on #callBtn:visible")
        if self.ui("#caw.on.cardmode").count():
            self.ui("#caw.on").tap()
        expect(self.ui("#dash.on #stWeek")).to_have_text("06")
        self.art("#dash.on #portrait", "/sandra/season-one/holiday.webp")
        self.shot("sandra-returns")

    def test_grace_completed_save(self):
        self.handover(animated=False)
        self.choose_a()
        self.finish_week()
        expect(self.ui("#noteh")).to_have_text("FROM GRACE'S DESK")
        expect(self.ui("#nextBtn")).to_be_visible()
        result_stats = self.ui(STATS).all_text_contents()
        self.shot("before-reload")
        self.resume()
        expect(self.ui("#dash.on #stWeek")).to_have_text("05")
        self.shot("resumed-result")
        self.assertEqual(result_stats, self.ui(STATS).all_text_contents())
        expect(self.ui("#noteh")).to_have_text("FROM GRACE'S DESK")
        expect(self.ui("#nextBtn")).to_be_visible()
        expect(self.ui("#callBtn")).to_be_hidden()
        self.art("#portrait", "grace/owner-office.webp")


if __name__ == "__main__":
    unittest.main(verbosity=2)
