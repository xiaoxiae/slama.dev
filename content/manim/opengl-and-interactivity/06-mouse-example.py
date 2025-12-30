from manim import *
from manim.opengl import *


class MouseScene(Scene):
    def construct(self):
        self.circle = Circle(color=BLUE)

        self.play(Write(self.circle))

        self.interactive_embed()

    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        """Called each time the mouse is dragged (moves pressed across the windows)."""
        # resize the circle to where the mouse cursor currently is
        new_radius = np.linalg.norm(point)

        # no animations (the object is already in the scene), only changes!
        self.circle.become(
            Circle(
                color=BLUE,
                radius=new_radius,
                fill_opacity=0.5 * abs(np.sin(new_radius)),  # for some spark ;)
            )
        )

        # here we DON'T want to use the default controls since dragging moves the camera
