from manim import *
from random import random, seed
from enum import Enum

# inspired by https://softologyblog.wordpress.com/2019/12/28/3d-cellular-automata-3/


class Grid:
    class ColorType(Enum):
        FROM_COORDINATES = 0
        FROM_PALETTE = 1

    def __init__(
        self,
        scene,
        grid_size,
        survives_when,
        revives_when,
        state_count=2,
        size=1,
        palette=["#000b5e", "#001eff"],
        color_type=ColorType.FROM_PALETTE,
    ):
        self.grid = {}
        self.scene = scene
        self.grid_size = grid_size
        self.size = size
        self.survives_when = survives_when
        self.revives_when = revives_when
        self.state_count = state_count
        self.palette = palette
        self.color_type = color_type

        self.bounding_box = Cube(side_length=self.size, color=GRAY, fill_opacity=0.05)
        self.scene.add(self.bounding_box)

    def fadeOut(self):
        self.scene.play(
            FadeOut(self.bounding_box),
            *[FadeOut(self.grid[index][0]) for index in self.grid],
        )

    def __index_to_position(self, index):
        """Convert the index of a cell to its position in 3D."""
        dirs = [RIGHT, UP, OUT]

        # be careful!
        # we can't just add stuff to ORIGIN, since it doesn't create new objects,
        # meaning we would be moving the origin, which messes with the animations
        result = list(ORIGIN)
        for dir, value in zip(dirs, index):
            result += (
                ((value - (self.grid_size - 1) / 2) / self.grid_size) * dir * self.size
            )

        return result

    def __get_new_cell(self, index):
        """Create a new cell"""
        cell = (
            Cube(
                side_length=1 / self.grid_size * self.size, color=BLUE, fill_opacity=1
            ).move_to(self.__index_to_position(index)),
            self.state_count - 1,
        )

        self.__update_cell_color(index, *cell)

        return cell

    def __return_neighbouring_cell_coordinates(self, index):
        """Return the coordinates of the neighbourhood of a given index."""
        neighbourhood = set()
        for dx in range(-1, 1 + 1):
            for dy in range(-1, 1 + 1):
                for dz in range(-1, 1 + 1):
                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    nx = index[0] + dx
                    ny = index[1] + dy
                    nz = index[2] + dz

                    # don't loop around (although we could)
                    if (
                        nx < 0
                        or nx >= self.grid_size
                        or ny < 0
                        or ny >= self.grid_size
                        or nz < 0
                        or nz >= self.grid_size
                    ):
                        continue

                    neighbourhood.add((nx, ny, nz))

        return neighbourhood

    def __count_neighbours(self, index):
        """Return the number of neighbouring cells for a given index (excluding itself)."""
        total = 0
        for neighbour_index in self.__return_neighbouring_cell_coordinates(index):
            if neighbour_index in self.grid:
                total += 1

        return total

    def __return_possible_cell_change_indexes(self):
        """Return the indexes of all possible cells that could change."""
        changes = set()
        for index in self.grid:
            changes |= self.__return_neighbouring_cell_coordinates(index).union({index})
        return changes

    def toggle(self, index):
        """Toggle a given cell."""
        if index in self.grid:
            self.scene.remove(self.grid[index][0])
            del self.grid[index]
        else:
            self.grid[index] = self.__get_new_cell(index)
            self.scene.add(self.grid[index][0])

    def __update_cell_color(self, index, cell, age):
        """Update the color of the specified cell."""
        if self.color_type == self.ColorType.FROM_PALETTE:
            state_colors = color_gradient(self.palette, self.state_count - 1)

            cell.set_color(state_colors[age - 1])
        else:

            def coordToHex(n):
                return hex(int(n * (256 / self.grid_size)))[2:].ljust(2, "0")

            cell.set_color(
                f"#{coordToHex(index[0])}{coordToHex(index[1])}{coordToHex(index[2])}"
            )

    def do_iteration(self):
        """Perform the automata generation, returning True if a state of any cell changed."""
        new_grid = {}
        something_changed = False

        for index in self.__return_possible_cell_change_indexes():
            neighbours = self.__count_neighbours(index)

            # alive rules
            if index in self.grid:
                cell, age = self.grid[index]

                # always decrease age
                if age != 1:
                    age -= 1
                    something_changed = True

                # survive if within range or age isn't 1
                if neighbours in self.survives_when or age != 1:
                    self.__update_cell_color(index, cell, age)
                    new_grid[index] = (cell, age)
                else:
                    self.scene.remove(self.grid[index][0])
                    something_changed = True

            # dead rules
            else:
                # revive if within range
                if neighbours in self.revives_when:
                    new_grid[index] = self.__get_new_cell(index)
                    self.scene.add(new_grid[index][0])
                    something_changed = True

        self.grid = new_grid

        return something_changed


class GOLFirst(ThreeDScene):
    def construct(self):
        seed(0xDEADBEEF)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=-0.20)

        grid_size = 16
        size = 3.5

        grid = Grid(
            self,
            grid_size,
            [4, 5],
            [5],
            state_count=2,
            size=size,
            color_type=Grid.ColorType.FROM_COORDINATES,
        )

        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    if random() < 0.2:
                        grid.toggle((i, j, k))

        grid.fadeIn()

        self.wait(1)

        for i in range(50):
            something_changed = grid.do_iteration()

            if not something_changed:
                break

            self.wait(0.2)

        self.wait(2)

        grid.fadeOut()


class GOLSecond(ThreeDScene):
    def construct(self):
        seed(0xDEADBEEF)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        grid_size = 16
        size = 3.5

        grid = Grid(
            self,
            grid_size,
            [2, 6, 9],
            [4, 6, 8, 9],
            state_count=10,
            size=size,
            color_type=Grid.ColorType.FROM_PALETTE,
        )

        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    if random() < 0.3:
                        grid.toggle((i, j, k))

        self.wait(2)

        for i in range(70):
            something_changed = grid.do_iteration()

            if not something_changed:
                break

            self.wait(0.1)

        self.wait(2)

        grid.fadeOut()
