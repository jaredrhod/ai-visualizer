import json
import sys
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server  # noqa: E402


class FacePageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.scripts = []
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "canvas" and attrs.get("id") == "stage":
            self.canvas = attrs
        elif tag == "script" and "src" in attrs:
            self.scripts.append(attrs["src"])
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


class CognitiveCommandFaceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def get_json(self, path):
        with urllib.request.urlopen(self.base_url + path, timeout=2) as response:
            self.assertEqual(response.status, 200)
            return json.load(response)

    def test_face_is_discovered_and_served_with_browser_contract(self):
        config = self.get_json("/config")
        faces = {face["id"]: face for face in config["faces"]}
        self.assertIn("cognitive-command", faces)
        self.assertEqual(faces["cognitive-command"]["title"], "Cognitive Command")
        self.assertIn("mesh", faces["cognitive-command"]["tagline"].lower())

        with urllib.request.urlopen(
            self.base_url + "/faces/cognitive-command/index.html", timeout=2
        ) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "text/html")
            html = response.read().decode("utf-8")

        parser = FacePageParser()
        parser.feed(html)
        self.assertEqual(parser.title.strip(), "Cognitive Command")
        self.assertIsNotNone(parser.canvas)
        self.assertEqual(parser.canvas.get("role"), "img")
        self.assertEqual(
            parser.canvas.get("aria-label"), "Alfred Cognitive Command interface"
        )
        self.assertIn("../../core.js", parser.scripts)


if __name__ == "__main__":
    unittest.main()
