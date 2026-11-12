"""Verify the arrival sequence and safe-area desk layout in mobile WebKit."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
handler = partial(SimpleHTTPRequestHandler, directory=root)
with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server, sync_playwright() as pw:
    Thread(target=server.serve_forever, daemon=True).start()
    browser = pw.webkit.launch()
    page = browser.new_page(**pw.devices["iPhone 13"], reduced_motion="reduce")
    page.on("pageerror", lambda err: print("Game error:", err, flush=True))
    page.goto(f"http://127.0.0.1:{server.server_port}", wait_until="domcontentloaded")
    page.add_style_tag(content=":root{--screen-safe-top:59px}")
    page.evaluate("window.dispatchEvent(new Event('resize'))")
    page.locator("#startbtn").tap()
    for screen in ("cut", "quote"):
        page.locator(f"#{screen}.on").tap()
    cutaway = page.locator("#caw.on")
    cutaway.wait_for()
    assert "Winter, 1984" in page.locator("#cawTxt").inner_text()
    cutaway.tap()
    page.wait_for_selector("#caw.on.introProfile #introDoor:visible", timeout=4000)
    profiles = set()
    cast_order = ["HANK WILLIS", "RICKY MALONE", "TINY MCGEE", "LEO G. ROSS", "THE ROOKIE", "SAWDUST SAM"]
    expected_pages = [speaker for speaker in cast_order for _ in range(2)]
    intro_pages = []
    saw_people = False
    saw_doorway = False
    saw_monday = False
    board_pages = []
    for _ in range(55):
        if page.locator("#dash.on").count():
            break
        if page.locator("#cawVid.show[src$='welcome_boss.mp4']").count():
            assert saw_monday
            cutaway.tap(position={"x": 12, "y": 60})
            page.locator("#dash.on").wait_for()
            break
        if "Right. The people." in page.locator("#cawTxt").inner_text():
            assert not intro_pages
            saw_people = True
        if page.locator("#caw.titleCard.on").count():
            assert saw_doorway
            title = page.locator("#cawTxt")
            assert title.is_visible()
            assert title.text_content() == "Monday morning\nDay 1", repr(title.text_content())
            saw_monday = True
        if page.locator("#caw.introProfile.cardmode.on").count():
            pic = page.locator("#cawCard").bounding_box()
            name = page.locator("#cawName")
            speaker = name.inner_text().upper()
            profiles.add(speaker)
            if speaker in cast_order:
                assert saw_people
                intro_pages.append(speaker)
            if page.locator("#cawPort.show[src$='office-chalkboard.webp']").count():
                page.locator("#cawPort").evaluate("img => img.decode()")
                assert intro_pages == expected_pages, intro_pages
                board_pages.append(page.locator("#cawTxt").inner_text())
            if page.locator("#cawPort.show[src$='office-door-neutral.webp']").count():
                assert len(board_pages) == 2
                saw_doorway = True
            assert pic["y"] >= 59, pic
            assert pic["y"] + pic["height"] <= name.bounding_box()["y"] + 1, pic
        cutaway.tap(position={"x": 12, "y": 60})
        page.wait_for_timeout(100)
    page.locator("#dash.on").wait_for()
    assert any("CASH" in text and "MORALE" in text for text in board_pages)
    assert any("BUZZ" in text and "CRED" in text for text in board_pages)
    assert intro_pages == expected_pages, intro_pages
    assert {"HANK WILLIS", "SANDRA"} <= profiles, profiles
    for width, height, top, bottom in [(393, 852, 59, 34), (375, 667, 20, 0), (393, 650, 0, 0), (430, 932, 62, 34), (393, 748, 59, 34), (393, 852, 59, 34)]:
        page.set_viewport_size({"width": width, "height": height})
        page.locator("#dash").evaluate(
            "(el, [t,b]) => { el.style.setProperty('--safe-top',t+'px'); el.style.setProperty('--safe-bottom',b+'px'); }",
            [top, bottom],
        )
        print(page.locator("#dash").evaluate("el => [el.style.cssText, getComputedStyle(el).top, el.getBoundingClientRect().toJSON(), window.innerHeight, window.scrollY]"), flush=True)
        page.wait_for_function(
            "([top, bottom]) => { const r = document.querySelector('#dash').getBoundingClientRect(); return Math.abs(r.top - top) < 1 && Math.abs(innerHeight - r.bottom - bottom) < 1; }",
            arg=[top, bottom], timeout=5000,
        )
        logo = page.locator(".chlogo").bounding_box()
        footer = page.locator(".ljfooter").bounding_box()
        assert top + 7 <= logo["y"] <= top + 9, logo
        assert footer["y"] + footer["height"] <= height - bottom + 1, footer
        paper = page.locator(".notebook").bounding_box()
        desk = page.locator("#desk").bounding_box()
        for selector, ratio in [(".calendar",63/638),("#portwin",407/634),(".slips",149/638),(".economy",94/638)]:
            panel = page.locator(selector).bounding_box()
            assert abs(panel["height"] - panel["width"]*ratio) < 1, (selector,panel)
        assert paper["height"] > 120
        assert page.locator("#ticker").inner_text() == ""
        note = page.locator("#notescroll")
        note.evaluate("el => el.scrollTop = 0")
        assert abs(desk["width"] - width * 0.94) < 1
        assert abs(footer["y"] + footer["height"] - (height - bottom - 3)) < 2
        paragraphs = note.locator(".opening-note p")
        assert paragraphs.count() == 3
        assert "Tiny" in paragraphs.nth(1).inner_text()
        assert "CASH" not in note.inner_text()
        tiny = paragraphs.nth(1).bounding_box()
        body = note.bounding_box()
        if height >= 820:
            assert tiny["y"] < body["y"] + body["height"]
        if width == 393 and height == 852:
            page.locator("#portrait").evaluate("img => img.decode()")
            page.locator("#desk").screenshot(path="/tmp/week-one-desk.png", scale="device")
        assert note.evaluate("el => { el.scrollTop = el.scrollHeight; return el.scrollHeight - el.clientHeight - el.scrollTop <= 1; }")
        assert page.locator(".chlogo").bounding_box()["y"] == logo["y"]
    page.locator("#callBtn").tap()
    page.locator("#decide.on").wait_for()
    page.locator("#dB").tap()
    for _ in range(80):
        screen = page.locator(".screen.on").last
        screen.wait_for()
        name = screen.get_attribute("id")
        if name == "dash":
            break
        if name == "moment":
            page.locator("#mA").tap()
        elif name in ("caw", "gazS"):
            screen.tap(position={"x": 20, "y": 68})
        page.wait_for_timeout(150)
    page.locator("#dash.on #nextBtn:visible").wait_for()
    assert page.locator("#slotL .slab").text_content() == "RESULT", page.locator("#desk").inner_text()
    assert page.locator("#ticker").inner_text() == ""
    assert page.locator("#nextBtn .txt").text_content() == "NEXT WEEK", page.locator("#nextBtn").inner_html()
    page.locator(".slips").screenshot(path="/tmp/postgame-slips.png", scale="device")
    page.locator("#nextBtn").tap()
    page.wait_for_function("document.querySelector('#stWeek').textContent.trim() === '02'")
    assert page.locator("#ticker").inner_text() == ""
    browser.close()
