# Copyright (C) 2021 Jean Da Costa machado.
# Jean3dimensional@gmail.com
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Modified 2026-11-20 by bobajeff: Updated draw code to work with Blender 5.1.2
'''
This is a utility module for drawing lines in the 3D viewport on Blender 5.1.2
using the GPU Api


The idea is to get rid of messy draw functions and data that is hard to keep track.
This class works directly like a callable draw handler and keeps track of all the geometry data.
'''

__all__ = ["DrawCallback"]

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix, Vector

vertex_shader = '''
void main() {
    gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
    gl_Position.z -= 0.002;
    finalColor = color;
}
'''

fragment_shader = '''
void main() {
    fragColor = finalColor;
}
'''

point_fragment_shader = '''
void main() {
    vec2 coord = (gl_PointCoord - vec2(0.5, 0.5)) * 2.0;
    float fac = dot(coord, coord);
    if (fac > 0.5) {
        discard;
    }
    fragColor = finalColor;
}
'''


def _create_shader(frag_source):
    vert_out = gpu.types.GPUStageInterfaceInfo("my_interface")
    vert_out.smooth('VEC4', "finalColor")

    shader_info = gpu.types.GPUShaderCreateInfo()
    shader_info.push_constant('MAT4', "ModelViewProjectionMatrix")
    shader_info.vertex_in(0, 'VEC3', "pos")
    shader_info.vertex_in(1, 'VEC4', "color")
    shader_info.vertex_out(vert_out)
    shader_info.fragment_out(0, 'VEC4', "fragColor")

    shader_info.vertex_source(vertex_shader)
    shader_info.fragment_source(frag_source)

    return gpu.shader.create_from_info(shader_info)


class DrawCallback:
    running_draws = set()

    def __init__(self):
        self.matrix = Matrix.Identity(4)
        self.draw_on_top = False
        # Options: 'NONE', 'ALPHA', 'ALPHA_PREMULT', 'ADDITIVE', 'ADDITIVE_PREMULT', 'MULTIPLY', 'SUBTRACT', 'INVERT'
        self.blend_mode = 'ALPHA'

        self.line_width = 1.0
        self.point_size = 3.0

        self.draw_handler = None

        self.line_coords = []
        self.line_colors = []
        self.point_coords = []
        self.point_colors = []

        self._line_shader = _create_shader(fragment_shader)
        self._point_shader = _create_shader(point_fragment_shader)

        self._line_batch = batch_for_shader(
            self._line_shader, 'LINES', {"pos": self.line_coords, "color": self.line_colors}
        )
        self._point_batch = batch_for_shader(
            self._point_shader, 'POINTS', {"pos": self.point_coords, "color": self.point_colors}
        )

    def __call__(self, *args, **kwargs):
        self._draw()

    def setup_handler(self):
        # Utility function to easily add it as a draw handler
        self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(self, (), "WINDOW", "POST_VIEW")
        self.__class__.running_draws.add(self)

    def remove_handler(self):
        # Utility function to remove the handler
        if not self.draw_handler:
            return
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, "WINDOW")
        self.draw_handler = None
        self.__class__.running_draws.remove(self)

    @classmethod
    def remove_all_handlers(cls):
        for draw in list(cls.running_draws):
            draw.remove_handler()

    def update_batch(self):
        # This takes the data rebuilds the shader batch.
        # Call it every time you clear the data or add new lines, otherwize,
        # You wont see changes in the viewport
        coords = [self.matrix @ Vector(coord) for coord in self.line_coords]
        self._line_batch = batch_for_shader(
            self._line_shader, 'LINES', {"pos": coords, "color": self.line_colors}
        )
        coords = [self.matrix @ Vector(coord) for coord in self.point_coords]
        self._point_batch = batch_for_shader(
            self._point_shader, 'POINTS', {"pos": coords, "color": self.point_colors}
        )

    def add_line(self, start, end, color1=(1, 0, 0, 1), color2=None):
        self.line_coords.append(Vector(start))
        self.line_coords.append(Vector(end))
        self.line_colors.append(color1)
        self.line_colors.append(color1 if color2 is None else color2)

    def add_point(self, location, color=(1, 0, 0, 1)):
        self.point_coords.append(Vector(location))
        self.point_colors.append(color)

    def clear_data(self):
        # just clear all the data
        self.line_coords.clear()
        self.line_colors.clear()
        self.point_coords.clear()
        self.point_colors.clear()

    def _start_drawing(self):
        # This handles all the settings of the renderer before starting the draw stuff
        gpu.state.blend_set(self.blend_mode)
        if self.draw_on_top:
            gpu.state.depth_test_set('NONE')
        else:
            gpu.state.depth_test_set('LESS_EQUAL')

        gpu.state.line_width_set(self.line_width)
        gpu.state.point_size_set(self.point_size)

    def _stop_drawing(self):
        gpu.state.blend_set('NONE')
        gpu.state.depth_test_set('NONE')
        gpu.state.line_width_set(1.0)
        gpu.state.point_size_set(1.0)

    def _draw(self):
        self._start_drawing()
        
        if self.line_coords:
            self._line_shader.bind()
            self._line_batch.draw(self._line_shader)
            
        if self.point_coords:
            self._point_shader.bind()
            self._point_batch.draw(self._point_shader)
            
        self._stop_drawing()


if __name__ == "__main__":
    DrawCallback.remove_all_handlers()

    draw = DrawCallback()
    draw.add_line((10, 0, 0), (-10, 0, 0), color1=(1, 0, 0, 1), color2=(0, 0, 1, 1))
    draw.add_line((0, 0, 0), (0, 0, 5), color1=(0, 1, 0, 1), color2=(0, 1, 1, 1))
    draw.add_point((0, 0, 5), color=(1, 1, 0, 1))

    draw.draw_on_top = True
    draw.blend_mode = 'ADDITIVE'
    draw.line_width = 5.0
    draw.point_size = 10.0

    draw.update_batch()
    draw.setup_handler()
