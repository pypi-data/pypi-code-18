from threading import Lock
import glfw
from pymj.builder import cymj
from pymj.generated import const
import time
import numpy as np
import scipy.misc
import copy


class MjViewerBasic(cymj.MjRenderContextWindow):

    def __init__(self, sim):
        super().__init__(sim)

        self._gui_lock = Lock()
        self._button_left_pressed = False
        self._button_right_pressed = False
        self._last_mouse_x = 0
        self._last_mouse_y = 0

        framebuffer_width, _ = glfw.get_framebuffer_size(self.window)
        window_width, _ = glfw.get_window_size(self.window)
        self._scale = framebuffer_width * 1.0 / window_width

        glfw.set_cursor_pos_callback(self.window, self._cursor_pos_callback)
        glfw.set_mouse_button_callback(
            self.window, self._mouse_button_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)
        glfw.set_key_callback(self.window, self.key_callback)

    def render(self):
        if self.window is None:
            return
        elif glfw.window_should_close(self.window):
            exit(0)

        with self._gui_lock:
            super().render()

        glfw.poll_events()

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.RELEASE and key == glfw.KEY_ESCAPE:
            print("Pressed ESC")
            print("Quitting.")
            exit(0)

    def _cursor_pos_callback(self, window, xpos, ypos):
        if not (self._button_left_pressed or self._button_right_pressed):
            return

        # Determine whether to move, zoom or rotate view
        mod_shift = (
            glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or
            glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS)
        if self._button_right_pressed:
            action = const.MOUSE_MOVE_H if mod_shift else const.MOUSE_MOVE_V
        elif self._button_left_pressed:
            action = const.MOUSE_ROTATE_H if mod_shift else const.MOUSE_ROTATE_V
        else:
            action = const.MOUSE_ZOOM

        # Determine
        dx = int(self._scale * xpos) - self._last_mouse_x
        dy = int(self._scale * ypos) - self._last_mouse_y
        width, height = glfw.get_framebuffer_size(window)

        with self._gui_lock:
            self.move_camera(action, dx / height, dy / height)

        self._last_mouse_x = int(self._scale * xpos)
        self._last_mouse_y = int(self._scale * ypos)

    def _mouse_button_callback(self, window, button, act, mods):
        self._button_left_pressed = (
            glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
        self._button_right_pressed = (
            glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

        x, y = glfw.get_cursor_pos(window)
        self._last_mouse_x = int(self._scale * x)
        self._last_mouse_y = int(self._scale * y)

    def _scroll_callback(self, window, x_offset, y_offset):
        with self._gui_lock:
            self.move_camera(const.MOUSE_ZOOM, 0, -0.05 * y_offset)


class MjViewer(MjViewerBasic):

    def __init__(self, sim):
        super().__init__(sim)

        self._ncam = sim.model.ncam
        self._paused = False # is viewer paused.
        self._advance_by_one_step = False # should we advance viewer just by one step.

        # Vars for recording video
        self._record_video = False
        self._video_frames = []
        self._video_idx = 0
        self._video_path = "/tmp/video_%07d.mp4"

        # vars for capturing screen
        self._image_idx = 0
        self._image_path = "/tmp/frame_%07d.png"

        # run_speed = x1, means running real time, x2 means fast-forward times two.
        self._run_speed = 1.0
        self._loop_count = 0

        self._show_mocap = True # Show / hide mocap bodies.

        self._time_per_render = 1 / 60.0 # this variable is estamated as a running average.
        self._hide_overlay = False # hide the entire overlay.

    def render(self):
        def render_inner_loop(self):
            render_start = time.time()
            super().render()
            self._time_per_render = 0.999 * self._time_per_render + 0.001 * (time.time() - render_start)
            if self._record_video:
                self._video_frames.append(self._read_pixels_as_in_window())
        self._create_full_overlay()
        # Render the same frame if paused.
        if self._paused:
            while self._paused:
                render_inner_loop(self)
                if self._advance_by_one_step:
                    self._advance_by_one_step = False
                    break
        else:
            # inner_loop runs "_loop_count" times in expectation (where "_loop_count" is a float).
            # Therefore, frames are displayed in the real-time.
            self._loop_count += self.sim.model.opt.timestep / (self._time_per_render * self._run_speed)
            while self._loop_count > 0:
                render_inner_loop(self)
                self._loop_count -= 1
        # Markers and overlay are regenerated in every pass.
        self._markers[:] = []
        self._overlay.clear()

    def _read_pixels_as_in_window(self):
        # Reads pixels with markers and overlay.
        resolution = glfw.get_framebuffer_size(self.sim._render_context_window.window)
        if self.sim._render_context_offscreen is None:
            self.sim.render(*resolution)
        offscreen_ctx = self.sim._render_context_offscreen
        window_ctx = self.sim._render_context_window
        # Save markers and overlay from offscreen.
        offscreen_markers = copy.deepcopy(offscreen_ctx._markers)
        offscreen_overlay = copy.deepcopy(offscreen_ctx._overlay)
        # Copy markers and overlay from window.
        offscreen_ctx._markers[:] = window_ctx._markers[:]
        offscreen_ctx._overlay.clear()
        offscreen_ctx._overlay.update(window_ctx._overlay)
        img = self.sim.render(*resolution)
        # Restore markers and overlay to offscreen.
        offscreen_ctx._markers[:] = offscreen_markers[:]
        offscreen_ctx._overlay.clear()
        offscreen_ctx._overlay.update(offscreen_overlay)
        return img

    def _create_full_overlay(self):
        # Code to generate overlay.
        if self._hide_overlay:
            return
        self.add_overlay(const.GRID_TOPLEFT, "Run speed = %.3f x real time" % self._run_speed, "[S]lower, [F]aster")
        self.add_overlay(const.GRID_TOPLEFT, "Switch camera (#cams = %d)" % (self._ncam + 1),
                                             "[Tab] (camera ID = %d)" % self.cam.fixedcamid)
        self.add_overlay(const.GRID_TOPLEFT, "[C]ontact forces", "Off" if self.vopt.flags[10] == 1 else "On")
        self.add_overlay(const.GRID_TOPLEFT, "Display [M]ocap bodies", "On" if self._show_mocap else "Off")
        if self._paused is not None:
            if not self._paused:
                self.add_overlay(const.GRID_TOPLEFT, "Stop", "[Space]")
            else:
                self.add_overlay(const.GRID_TOPLEFT, "Start", "[Space]")
            self.add_overlay(const.GRID_TOPLEFT, "Advance simulation by one step", "[right arrow]")
        self.add_overlay(const.GRID_TOPLEFT, "[H]ide Menu", "")
        if self._record_video:
            ndots = int(7 * (time.time() % 1))
            dots = ("." * ndots) + (" " * (6 - ndots))
            self.add_overlay(const.GRID_TOPLEFT, "Record [V]ideo (On) " + dots, "")
        else:
            self.add_overlay(const.GRID_TOPLEFT, "Record [V]ideo (Off) ", "")
        if self._video_idx > 0:
            fname = self._video_path % (self._video_idx - 1)
            self.add_overlay(const.GRID_TOPLEFT, "   saved as %s" % fname, "")

        self.add_overlay(const.GRID_TOPLEFT, "Capture fram[e]", "")
        if self._image_idx > 0:
            fname = self._image_path % (self._image_idx - 1)
            self.add_overlay(const.GRID_TOPLEFT, "   saved as %s" % fname, "")
        self.add_overlay(const.GRID_TOPLEFT, "Start [i]pdb", "")
        self.add_overlay(const.GRID_BOTTOMLEFT, "FPS", "%d" % (1 / self._time_per_render))
        self.add_overlay(const.GRID_BOTTOMLEFT, "Solver iterations", str(self.sim.data.solver_iter + 1))

    def key_callback(self, window, key, scancode, action, mods):
        super().key_callback(window, key, scancode, action, mods)
        if action != glfw.RELEASE:
            return
        elif key == glfw.KEY_TAB: # Switches cameras.
            self.cam.fixedcamid += 1
            self.cam.type = const.CAMERA_FIXED
            if self.cam.fixedcamid >= self._ncam:
                self.cam.fixedcamid = -1
                self.cam.type = const.CAMERA_FREE
        elif key == glfw.KEY_H: # hides all overlay.
            self._hide_overlay = not self._hide_overlay
        elif key == glfw.KEY_SPACE and self._paused is not None: # stops simulation.
            self._paused = not self._paused
        elif key == glfw.KEY_RIGHT and self._paused is not None: # Advances simulation by one step.
            self._advance_by_one_step = True
            self._paused = True
        elif key == glfw.KEY_V: # Records video.
            self._record_video = not self._record_video
            if not self._record_video and len(self._video_frames) > 0:
                # This include captures console, if in the top declaration.
                from moviepy.editor import ImageSequenceClip
                clip = ImageSequenceClip(self._video_frames, fps=60)
                self._video_frames = []
                clip.write_videofile(self._video_path % self._video_idx)
                self._video_idx += 1
        elif key == glfw.KEY_R: # capture screenshot
            img = self._read_pixels_as_in_window()
            scipy.misc.imsave(self._image_path % self._image_idx, img)
            self._image_idx += 1
        elif key == glfw.KEY_I: # drops in debugger.
            print('You can access the simulator by self.sim')
            import ipdb; ipdb.set_trace()
        elif key == glfw.KEY_S: # Slows down simulation.
            self._run_speed /= 2.0
        elif key == glfw.KEY_F: # Speeds up simulation.
            self._run_speed *= 2.0
        elif key == glfw.KEY_C: # Displays contact forces.
            vopt = self.vopt
            vopt.flags[10] = vopt.flags[11] = not vopt.flags[10]
        elif key == glfw.KEY_M: # Shows / hides mocap bodies
            self._show_mocap = not self._show_mocap
            for body_idx1, val in enumerate(self.sim.model.body_mocapid):
                if val != -1:
                    for geom_idx, body_idx2 in enumerate(self.sim.model.geom_bodyid):
                        if body_idx1 == body_idx2:
                            self.sim.model.geom_rgba[geom_idx, 3] = float(self._show_mocap)

