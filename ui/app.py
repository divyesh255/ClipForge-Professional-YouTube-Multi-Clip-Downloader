from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, Select, TextArea
from textual.containers import Vertical
from textual.widgets import ListView, ListItem, Label

from core.yt import fetch_qualities
from core.downloader import download_clips
from core.validator import validate_url, validate_time_format, time_to_seconds


class ClipForge(App):

    CSS = """
    Screen {
        align: center middle;
    }

    #main {
        width: 85%;
        border: solid green;
        padding: 1 2;
    }

    #clip_list {
        height: 8;
        border: solid cyan;
    }

    #logbox {
        height: 16;
        border: solid yellow;
    }


    #watermark {
        dock: bottom;
        width: 100%;
        text-align: center;
        color: #888888;
        background: #0f172a;
        height: 1;
    }
    """

    clips = []
    downloading = False

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="main"):
            yield Static("🎬 ClipForge Pro")

            yield Input(placeholder="Paste YouTube URL", id="url")
            yield Button("Fetch Qualities", id="fetch")

            self.quality_select = Select([("Best", "best")], id="quality")
            yield self.quality_select

            yield Static("Start Time (HH:MM:SS)")
            self.start_input = Input(placeholder="00:01:20", id="start")
            yield self.start_input

            yield Static("End Time (HH:MM:SS)")
            self.end_input = Input(placeholder="00:01:40", id="end")
            yield self.end_input

            yield Button("➕ Add Clip", id="add")
            yield Button("❌ Delete Selected Clip", id="delete")

            yield ListView(id="clip_list")

            yield Button("⬇ Download All", id="download")

            yield Static("Logs (copy supported)")
            self.logbox = TextArea("", id="logbox", read_only=True, show_line_numbers=True)
            yield self.logbox

            yield Static("ClipForge  •  Made with ❤️  Divyesh Kapadiya", id="watermark")

        yield Footer()

    # -------- LOG --------
    def add_log(self, msg: str):
        def _append():
            self.logbox.text = self.logbox.text + msg + "\n"
            self.logbox.scroll_end(animate=False)
        self.call_later(_append)

    # -------- VALIDATE --------
    def validate_times(self, start, end):

        if not validate_time_format(start):
            self.notify("Invalid start time")
            return False

        if not validate_time_format(end):
            self.notify("Invalid end time")
            return False

        s = time_to_seconds(start)
        e = time_to_seconds(end)

        if e <= s:
            self.notify("End must be greater than start")
            return False

        return True

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "end":
            self.add_clip()

    # -------- BUTTON EVENTS --------
    def on_button_pressed(self, event: Button.Pressed):

        if self.downloading and event.button.id != "download":
            self.notify("Wait until download completes")
            return

        btn = event.button.id

        if btn == "fetch":
            self.handle_fetch()

        elif btn == "add":
            self.add_clip()

        elif btn == "delete":
            self.delete_clip()

        elif btn == "download":
            self.download_all()

    # -------- FETCH --------
    def handle_fetch(self):
        url = self.query_one("#url").value

        if not validate_url(url):
            self.notify("Invalid URL")
            return

        self.add_log("🔎 Fetching qualities...")

        import threading

        def run():
            q = fetch_qualities(url)

            def update():
                options = [("Best", "best")]
                for x in q:
                    if x != "best":
                        options.append((f"{x}p", x))

                self.quality_select.set_options(options)
                self.quality_select.value = "best"

                self.add_log(f"✅ Qualities loaded: {q}")

            self.call_later(update)

        threading.Thread(target=run, daemon=True).start()

    # -------- ADD --------
    def add_clip(self):
        start = self.start_input.value.strip()
        end = self.end_input.value.strip()

        if not self.validate_times(start, end):
            return

        self.clips.append({"start": start, "end": end})
        self.refresh_list()

        self.add_log(f"Added clip {start} → {end}")

        self.start_input.value = ""
        self.end_input.value = ""

    # -------- DELETE --------
    def delete_clip(self):
        lv = self.query_one("#clip_list", ListView)

        if lv.index is None or lv.index >= len(self.clips):
            self.notify("Select clip first")
            return

        removed = self.clips.pop(lv.index)
        self.refresh_list()

        self.add_log(f"Deleted clip {removed['start']} → {removed['end']}")

    def refresh_list(self):
        lv = self.query_one("#clip_list", ListView)
        lv.clear()

        for i, c in enumerate(self.clips, start=1):
            lv.append(ListItem(Label(f"{i}. {c['start']} → {c['end']}")))

    # -------- DOWNLOAD --------
    def download_all(self):
        if self.downloading:
            self.notify("Download already running")
            return

        url = self.query_one("#url").value
        quality = self.quality_select.value or "best"

        if not validate_url(url):
            self.notify("Invalid URL")
            return

        if not self.clips:
            self.notify("No clips added")
            return

        self.downloading = True
        self.add_log("🚀 Starting downloads...")

        import threading

        def run():
            download_clips(url, self.clips, quality, log_callback=self.add_log)

            def done():
                self.downloading = False
                self.add_log("🎉 All downloads completed")

            self.call_later(done)

        threading.Thread(target=run, daemon=True).start()