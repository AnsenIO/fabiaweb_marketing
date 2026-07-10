from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MONO = "DejaVu Sans Mono"

class FABIABoxIntro(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        title = Text("FABIABox", font=MONO, font_size=72, color=PRIMARY, weight=BOLD)
        tagline = Text("The AI Co-Founder That Ships Your Company.", font=MONO, font_size=28, color=SECONDARY)
        box = RoundedRectangle(corner_radius=0.2, width=2.2, height=1.2, stroke_color=PRIMARY, stroke_width=4, fill_color=PRIMARY, fill_opacity=0.1)
        label = Text("IDEA  →  PRODUCT  →  COMPANY", font=MONO, font_size=20, color=ACCENT)

        title.move_to(UP * 1.5)
        tagline.next_to(title, DOWN, buff=0.5)
        box.move_to(DOWN * 0.8)
        label.next_to(box, DOWN, buff=0.4)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(tagline, shift=DOWN), run_time=1.2)
        self.wait(0.8)
        self.play(Create(box), run_time=1.0)
        self.wait(0.5)
        self.play(Write(label), run_time=1.0)
        self.wait(2.5)
