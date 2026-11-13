"""Exercise the portrait Possum game and the first Grace handover in mobile WebKit."""
import json
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from time import monotonic

from playwright.sync_api import expect, sync_playwright


class StoryWeeks(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=root))
        Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        pw = self.enterContext(sync_playwright())
        browser = pw.webkit.launch()
        self.addCleanup(browser.close)
        self.page = browser.new_page(**pw.devices["iPhone 13"], reduced_motion="reduce")
        self.page.set_default_timeout(8000)
        self.page.goto(f"http://127.0.0.1:{server.server_port}", wait_until="domcontentloaded")
        self.addCleanup(self.shot, self._testMethodName + "-last-screen")

    def shot(self, name):
        folder = Path("/tmp/story-weeks")
        folder.mkdir(exist_ok=True)
        self.page.screenshot(path=folder / (name + ".png"), scale="device")

    def accept_resume(self):
        with self.page.expect_event("dialog") as dialog:
            self.page.once("dialog", lambda d: d.accept())
            self.page.locator("#startbtn").tap()
        self.assertIn("Resume your saved franchise", dialog.value.message)

    def resume(self):
        self.accept_resume()
        self.page.locator("#dash.on #callBtn").wait_for()

    def start_week(self, week, story):
        # A setup save before the decision. The game owns every subsequent save,
        # including the Week 4 leave flag, Week 5 selection and Grace's met flag.
        state = dict(week=week, tw=week, season=1, stage="regular", cash=39000,
                     morale=72, buzz=48, cred=36, wins=week-1, losses=0, streak=1,
                     debtWeeks=0, champs=0, venue="HOME", foe="FARGO", flags={},
                     done={"tiny_openmic": True}, triggeredAt={},
                     met=dict.fromkeys(("sandra", "hank", "tiny", "ricky", "leo", "import", "sam"), True))
        if week == 4:
            state["done"].update(possum_fusebox=True, chainsaw_night=True)
        save = dict(v=4, S=state, cur=story, deckIds=[], deckPos=0)
        self.page.evaluate("s => localStorage.setItem('courtside_save', s)", json.dumps(save))
        self.resume()

    def choose_a(self):
        self.page.locator("#callBtn").tap()
        self.page.locator("#decide.on #dA").tap()

    def finish_week(self):
        end = self.page.locator("#dash.on #nextBtn:visible")
        deadline = monotonic() + 45
        while monotonic() < deadline and not end.count():
            screen = self.page.locator("#caw.on, #gazS.on, #moment.on")
            if screen.count():
                active = screen.last
                if active.get_attribute("id") == "moment":
                    self.page.locator("#mA").tap()
                else:
                    active.tap(position={"x": 12, "y": 60})
            self.page.wait_for_timeout(120)
        expect(end).to_be_visible()
        expect(end.locator(".txt")).to_have_text("NEXT WEEK")

    def image(self, selector, suffix):
        img = self.page.locator(f"{selector}[src$='{suffix}']")
        expect(img).to_be_visible()
        img.evaluate("img => img.decode()")

    def test_possum(self):
        page = self.page
        self.start_week(2, "possum_fusebox")
        expect(page.locator("#noteh")).to_have_text("THE FUSE BOX")
        self.choose_a()
        frame = page.frame_locator("#mgOverlay.on #mgFrame")
        canvas = frame.locator("#game.on #c")
        expect(canvas).to_be_visible()
        box = canvas.bounding_box()
        self.assertGreater(box["height"], box["width"])
        host = page.locator("#mgFrame").bounding_box()
        stage = page.locator(".phone").bounding_box()
        for dimension in ("x", "y", "width", "height"):
            self.assertAlmostEqual(host[dimension], stage[dimension], delta=1)
        self.shot("possum-board")
        # Read the visible green pilot tabs at the six cabinet slots. Touches
        # use their screen coordinates so the iframe's stage transform applies.
        slots = [(57, 110), (42, 200), (67, 260), (141, 260), (161, 200), (147, 110)]
        deadline = monotonic() + 40
        while frame.locator("#crate .full").count() < 6 and monotonic() < deadline:
            target = canvas.evaluate("""(c, slots) => {
                const ctx = c.getContext('2d');
                return slots.find(([x,y]) => {
                    const [r,g,b] = ctx.getImageData((x-9)*c.width/192,(y+10)*c.height/366,1,1).data;
                    return r === 53 && g === 94 && b === 43;
                });
            }""", slots)
            if target:
                x, y = target
                page.touchscreen.tap(box["x"] + x * box["width"]/192,
                                     box["y"] + y * box["height"]/366)
            page.wait_for_timeout(70)
        expect(frame.locator("#crate .full")).to_have_count(6)
        self.shot("possum-six-caught")
        expect(page.locator("#mgFrame")).to_have_attribute("src", "about:blank")
        self.finish_week()
        expect(page.locator("#notescroll")).to_contain_text("came out ahead")
        expect(page.locator("#noteh")).to_have_text("FROM SANDRA'S DESK")
        self.image("#portrait", "/sandra/season-one/pleased.webp")
        self.shot("possum-result")

    def test_grace(self):
        page = self.page
        self.start_week(4, "ricky_statue")
        self.choose_a()
        self.finish_week()
        expect(page.locator("#notescroll")).to_contain_text("Grace is covering")
        page.emulate_media(reduced_motion="no-preference")
        page.locator("#nextBtn").tap()
        card = page.locator("#caw.on.handover")
        expect(card.locator("#cawName")).to_have_text("SANDRA")
        self.image("#cawPort", "/sandra_departure.webp")
        film = card.locator("#departureFilm")
        expect(film).to_have_attribute("src", "assets/cutscenes/sandra_departure.mp4")
        expect(film).to_be_visible()
        page.wait_for_function("""() => {const v = document.querySelector('#departureFilm');
            return v.playsInline && !v.webkitDisplayingFullscreen && !v.paused &&
                   v.videoWidth > 0 && v.currentTime > 0.15; }""")
        self.shot("sandra-departure")
        card.tap(position={"x": 12, "y": 60})
        expect(card.locator("#cawName")).to_have_text("GRACE")
        expect(card.locator("#cawTxt")).to_contain_text("your things in Sandra's office")
        self.image("#cawPort", "/grace_owner_office.webp")
        expect(film).to_be_hidden()
        self.assertTrue(film.evaluate("v => v.paused"))
        self.shot("grace-introduction")
        card.tap(position={"x": 12, "y": 60})
        desk = page.locator("#dash.on")
        expect(desk.locator("#noteh")).to_have_text("SANDRA'S WEEK OFF")
        expect(desk.locator("#stWeek")).to_have_text("05")
        self.image("#portrait", "/grace/owner-office.webp")
        self.shot("grace-desk")
        fields = desk.locator("#stWeek,#stRecord,#stCash,#stMorale,#stBuzz,#stCred,#notescroll")
        before = fields.all_text_contents()
        page.reload(wait_until="domcontentloaded")
        self.resume()
        self.assertEqual(fields.all_text_contents(), before)
        self.image("#portrait", "/grace/owner-office.webp")
        self.assertEqual(card.count(), 0)
        self.shot("grace-resumed")
        page.emulate_media(reduced_motion="reduce")
        self.choose_a()
        self.finish_week()
        expect(desk.locator("#noteh")).to_have_text("FROM GRACE'S DESK")
        self.image("#portrait", "/grace/owner-office.webp")
        # Retain the exact browser-written checkpoint so we can also exercise
        # the uninterrupted return to Sandra if post-decision resume regresses.
        finished = page.evaluate("localStorage.getItem('courtside_save')")
        postgame = fields.all_text_contents()
        self.shot("grace-postgame")
        page.locator("#nextBtn").tap()
        # Week 6 may introduce a supporting character before returning to the desk.
        if page.locator("#caw.on").count():
            page.locator("#caw.on").tap(position={"x": 12, "y": 60})
        expect(desk.locator("#stWeek")).to_have_text("06")
        self.image("#portrait", "/sandra/season-one/holiday.webp")
        self.shot("sandra-back")

        page.evaluate("s => localStorage.setItem('courtside_save', s)", finished)
        page.reload(wait_until="domcontentloaded")
        self.accept_resume()
        expect(desk).to_be_visible()
        self.image("#portrait", "/grace/owner-office.webp")
        self.shot("grace-postgame-resumed")
        expect(desk.locator("#nextBtn")).to_be_visible()
        expect(desk.locator("#callBtn")).to_be_hidden()
        self.assertEqual(fields.all_text_contents(), postgame)


if __name__ == "__main__":
    unittest.main(verbosity=2)
