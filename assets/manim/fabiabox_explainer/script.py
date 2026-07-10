from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
DIM = "#444444"
MONO = "DejaVu Sans Mono"

class FABIABoxExplainer(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # Scene 1 — Title
        title = Text("FABIABox", font=MONO, font_size=72, color=PRIMARY, weight=BOLD)
        tagline = Text("The AI Co-Founder That Ships Your Company.", font=MONO, font_size=28, color=SECONDARY)
        title.move_to(UP * 0.5)
        tagline.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(tagline, shift=DOWN), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(title), FadeOut(tagline), run_time=0.5)

        # Scene 2 — The Problem
        founder = Circle(radius=0.4, color=PRIMARY, fill_opacity=0.2).move_to(LEFT * 5)
        founder_label = Text("Founder", font=MONO, font_size=18, color=PRIMARY).next_to(founder, DOWN, buff=0.2)
        idea_bubble = Ellipse(width=1.6, height=1.0, color=ACCENT, stroke_width=3).move_to(LEFT * 2.5 + UP * 1.2)
        idea_text = Text("Idea", font=MONO, font_size=24, color=ACCENT).move_to(idea_bubble.get_center())

        self.play(Create(founder), FadeIn(founder_label), run_time=0.8)
        self.play(Create(idea_bubble), Write(idea_text), run_time=1.0)
        self.wait(0.5)

        walls = VGroup(*[
            VGroup(
                Rectangle(width=1.4, height=1.8, color=DIM, fill_color=DIM, fill_opacity=0.3),
                Text(label, font=MONO, font_size=18, color=ACCENT)
            ).arrange(DOWN, buff=0.2)
            for label in ["Team", "Code", "Launch", "Ops"]
        ]).arrange(RIGHT, buff=0.4).move_to(RIGHT * 1.5)

        self.play(FadeIn(walls, shift=UP), run_time=1.2)
        self.wait(1.5)

        problem = Text("Stuck.", font=MONO, font_size=36, color="#FF6B6B").move_to(DOWN * 2.5)
        self.play(Write(problem), run_time=0.8)
        self.wait(1.0)
        self.play(
            FadeOut(founder), FadeOut(founder_label), FadeOut(idea_bubble), FadeOut(idea_text),
            FadeOut(walls), FadeOut(problem), run_time=0.5
        )

        # Scene 3 — The Solution
        hub = Circle(radius=0.8, color=PRIMARY, fill_color=PRIMARY, fill_opacity=0.2)
        hub_label = Text("FABIABox", font=MONO, font_size=22, color=PRIMARY, weight=BOLD)
        hub_group = VGroup(hub, hub_label).move_to(ORIGIN)

        modules = [
            ("Architect", UP * 2.5),
            ("Research", LEFT * 3 + UP * 0.8),
            ("Build", LEFT * 3 + DOWN * 0.8),
            ("Launch", RIGHT * 3 + UP * 0.8),
            ("Operate", RIGHT * 3 + DOWN * 0.8),
        ]

        module_objs = []
        for name, pos in modules:
            rect = RoundedRectangle(corner_radius=0.15, width=1.8, height=0.7, color=SECONDARY, fill_color=SECONDARY, fill_opacity=0.15)
            txt = Text(name, font=MONO, font_size=20, color=SECONDARY)
            mod = VGroup(rect, txt).move_to(pos)
            module_objs.append(mod)

        self.play(Create(hub_group), run_time=1.0)
        self.wait(0.3)
        for mod in module_objs:
            line = Line(hub.get_center(), mod.get_center(), color=DIM, stroke_width=2)
            self.play(Create(line), FadeIn(mod, scale=0.8), run_time=0.7)
        self.wait(1.0)

        # Scene 4 — Outcome
        output_box = RoundedRectangle(corner_radius=0.2, width=4.0, height=2.2, color=ACCENT, stroke_width=4, fill_color=ACCENT, fill_opacity=0.1)
        output_box.move_to(ORIGIN)
        url = Text("fabiabox.com", font=MONO, font_size=30, color=ACCENT).move_to(output_box.get_center() + UP * 0.3)
        live = Text("LIVE", font=MONO, font_size=24, color=SECONDARY).move_to(output_box.get_center() + DOWN * 0.5)

        self.play(
            FadeOut(hub_group), *[FadeOut(mod) for mod in module_objs],
            run_time=0.5
        )
        # Fade out lines separately
        self.play(*[FadeOut(mob) for mob in self.mobjects if isinstance(mob, Line)], run_time=0.3)

        self.play(Create(output_box), Write(url), run_time=1.0)
        self.play(Write(live), run_time=0.8)
        self.wait(1.0)

        # Scene 5 — CTA
        cta = Text("Your idea. Shipped by AI.", font=MONO, font_size=32, color=PRIMARY).move_to(DOWN * 2.2)
        self.play(FadeIn(cta, shift=UP), run_time=1.0)
        self.wait(2.0)
