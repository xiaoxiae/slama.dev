from manim import *


class Stack(VMobject):
    def __init__(self, size, **kwargs):
        # initialize the vmobject
        super().__init__(**kwargs)

        self.squares = VGroup()
        self.labels = VGroup()
        self.index = 0
        self.pointer = Arrow(ORIGIN, UP * 1.2)

        for _ in range(size):
            self.squares.add(Square(side_length=0.8))

        self.squares.arrange(buff=0.15)

        self.pointer.next_to(self.squares[0], DOWN)

        # IMPORTANT - we have to add all of the subobjects for them to be displayed
        self.add(self.squares, self.pointer, self.labels)

    def __peek(self) -> VMobject:
        """Return the current top element in the stack."""
        return self.squares[self.index]

    def __create_label(self, element) -> VMobject:
        """Create the label for the given element (given its color and size)."""
        return (
            Tex(str(element))
            .set_height(self.__peek().height / 2)
            .set_color(self.__peek().get_color())
            .move_to(self.__peek())
            .set_z_index(1)  # labels on top!
        )

    def __animate_indicate(self, element, increase: bool = True) -> Animation:
        """Return an animation indicating the current element."""
        return Indicate(
            element,
            color=self.__peek().get_color(),
            scale_factor=1.1 if increase else 1/1.1,
        )

    def push(self, element) -> Animation:
        """Pushes an element onto the stack, returning an appropriate animation."""
        label = self.__create_label(element)
        self.labels.add(label)

        self.index += 1

        return AnimationGroup(
            FadeIn(label),
            self.pointer.animate.next_to(self.__peek(), DOWN),
            self.__animate_indicate(self.squares[self.index - 1], increase=True),
        )

    def pop(self) -> AnimationGroup:
        """Pops an element from the stack, returning an appropriate animation."""
        label = self.labels[-1]
        self.labels.remove(label)

        self.index -= 1

        return AnimationGroup(
            FadeOut(label),
            self.pointer.animate.next_to(self.__peek(), DOWN),
            self.__animate_indicate(self.__peek(), increase=False),
        )

    def clear(self) -> AnimationGroup:
        """Clear the entire stack, returning the appropriate animation."""
        result = Succession(*[self.pop() for _ in range(self.index)])

        self.index = 0

        return result


class StackExample(Scene):
    def construct(self):
        stack = Stack(10)

        self.play(Write(stack))

        self.wait(0.5)

        for i in range(5):
            self.play(stack.push(i))

        self.play(stack.pop())

        self.wait(0.5)

        # we can even use the animate syntax!
        self.play(stack.animate.scale(1.2).set_color(BLUE))

        self.wait(0.5)

        for i in range(2):
            self.play(stack.push(i))

        self.play(stack.pop())

        self.play(stack.clear())

        self.play(FadeOut(stack))