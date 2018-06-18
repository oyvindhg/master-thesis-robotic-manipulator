#!/usr/bin/env python
#
# Copyright (c) 2010 Brandyn White (bwhite@dappervision.com)
#                    Andrew Miller (amiller@dappervision.com)
#
# This code is licensed to you under the terms of the Apache License, version
# 2.0, or, at your option, the terms of the GNU General Public License,
# version 2.0. See the APACHE20 and GPL2 files for the text of the licenses,
# or the following URLs:
# http://www.apache.org/licenses/LICENSE-2.0
# http://www.gnu.org/licenses/gpl-2.0.txt
#
# If you redistribute this file in source form, modified or unmodified, you
# may:
#   1) Leave this header intact and distribute it under the same terms,
#      accompanying it with the APACHE20 and GPL20 files, or
#   2) Delete the Apache 2.0 clause and accompany it with the GPL2 file, or
#   3) Delete the GPL v2 clause and accompany it with the APACHE20 file
# In all cases you must keep the copyright notice intact and include a copy
# of the CONTRIB file.
#
# Binary distributions must follow the binary distribution requirements of
# either License.

from libc.stdint cimport *
import numpy as np
cimport numpy as npc

cdef extern from "numpy/arrayobject.h":
    void import_array()
    cdef object PyArray_SimpleNewFromData(int nd, npc.npy_intp *dims,
                                           int typenum, void *data)

cdef extern from "stdlib.h":
    void free(void *ptr)

cdef extern from "libfreenect.h":
    ctypedef enum freenect_video_format:
        FREENECT_VIDEO_RGB
        FREENECT_VIDEO_BAYER
        FREENECT_VIDEO_IR_8BIT
        FREENECT_VIDEO_IR_10BIT
        FREENECT_VIDEO_IR_10BIT_PACKED
        FREENECT_VIDEO_YUV_RGB
        FREENECT_VIDEO_YUV_RAW

    ctypedef enum freenect_depth_format:
        FREENECT_DEPTH_11BIT
        FREENECT_DEPTH_10BIT
        FREENECT_DEPTH_11BIT_PACKED
        FREENECT_DEPTH_10BIT_PACKED
        FREENECT_DEPTH_REGISTERED
        FREENECT_DEPTH_MM

    ctypedef enum freenect_led_options:
        FREENECT_LED_OFF "LED_OFF"
        FREENECT_LED_GREEN "LED_GREEN"
        FREENECT_LED_RED "LED_RED"
        FREENECT_LED_YELLOW "LED_YELLOW"
        FREENECT_LED_BLINK_GREEN "LED_BLINK_GREEN"
        FREENECT_LED_BLINK_RED_YELLOW "LED_BLINK_RED_YELLOW"

    ctypedef enum freenect_resolution:
        FREENECT_RESOLUTION_LOW
        FREENECT_RESOLUTION_MEDIUM
        FREENECT_RESOLUTION_HIGH

    ctypedef enum freenect_device_flags:
        FREENECT_DEVICE_MOTOR
        FREENECT_DEVICE_CAMERA
        FREENECT_DEVICE_AUDIO

    ctypedef enum freenect_tilt_status_code:
        TILT_STATUS_STOPPED
        TILT_STATUS_LIMIT
        TILT_STATUS_MOVING

    ctypedef struct freenect_raw_tilt_state:
        int16_t accelerometer_x
        int16_t accelerometer_y
        int16_t accelerometer_z
        int8_t tilt_angle
        freenect_tilt_status_code tilt_status

    ctypedef struct freenect_frame_mode:
        uint32_t reserved
        freenect_resolution resolution
        int32_t video_format # we chose one of video_format/depth_format arbitrarily, since they are in a union
        int32_t bytes
        int16_t width
        int16_t height
        int8_t data_bits_per_pixel
        int8_t padding_bits_per_pixel
        int8_t framerate
        int8_t is_valid

    ctypedef struct freenect_context
    ctypedef struct freenect_device

    ctypedef void (*freenect_depth_cb)(freenect_device *dev, void *depth, uint32_t timestamp)
    ctypedef void (*freenect_video_cb)(freenect_device *dev, void *video, uint32_t timestamp)
    int freenect_init(freenect_context **ctx, void *usb_ctx)
    int freenect_shutdown(freenect_context *ctx)
    int freenect_process_events(freenect_context *ctx) nogil
    int freenect_num_devices(freenect_context *ctx)
    int freenect_select_subdevices(freenect_context *ctx, freenect_device_flags subdevs)
    int freenect_open_device(freenect_context *ctx, freenect_device **dev, int index)
    int freenect_close_device(freenect_device *dev)
    void freenect_set_depth_callback(freenect_device *dev, freenect_depth_cb cb)
    void freenect_set_video_callback(freenect_device *dev, freenect_video_cb cb)

    int freenect_get_video_mode_count()
    freenect_frame_mode freenect_get_video_mode(int mode_num)
    freenect_frame_mode freenect_get_current_video_mode(void *dev)
    freenect_frame_mode freenect_find_video_mode(int res, int fmt)
    int freenect_set_video_mode(freenect_device *dev, freenect_frame_mode mode)

    int freenect_get_depth_mode_count()
    freenect_frame_mode freenect_get_depth_mode(int mode_num)
    freenect_frame_mode freenect_get_current_depth_mode(void *dev)
    freenect_frame_mode freenect_find_depth_mode(int res, int fmt)
    int freenect_set_depth_mode(freenect_device *dev, freenect_frame_mode mode)

    int freenect_start_depth(freenect_device *dev)
    int freenect_start_video(freenect_device *dev)
    int freenect_stop_depth(freenect_device *dev)
    int freenect_stop_video(freenect_device *dev)
    int freenect_set_tilt_degs(freenect_device *dev, double angle)
    int freenect_set_led(freenect_device *dev, freenect_led_options option)
    int freenect_update_tilt_state(freenect_device *dev)
    freenect_raw_tilt_state* freenect_get_tilt_state(freenect_device *dev)
    void freenect_get_mks_accel(freenect_raw_tilt_state *state, double* x, double* y, double* z)
    double freenect_get_tilt_degs(freenect_raw_tilt_state *state)


cdef extern from "libfreenect_sync.h":
    int freenect_sync_get_video(void **video, uint32_t *timestamp, int index, freenect_video_format fmt) nogil
    int freenect_sync_get_depth(void **depth, uint32_t *timestamp, int index, freenect_depth_format fmt) nogil
    void freenect_sync_stop()
############## NEW CODE #################
    int freenect_sync_camera_to_world(uint16_t* cx, uint16_t* cy, int16_t* wz, float* wx, float* wy, int index)
    void freenect_sync_map_rgb_to_depth(uint16_t* depth_mm, uint8_t* rgb_raw, uint8_t* rgb_registered, int index)
    void freenect_sync_isolate_object(uint16_t* depth_mm, uint8_t* rgb_raw, uint32_t* borders, uint8_t* rgb_registered, int index)
#########################################

VIDEO_RGB = FREENECT_VIDEO_RGB
VIDEO_BAYER = FREENECT_VIDEO_BAYER
VIDEO_IR_8BIT = FREENECT_VIDEO_IR_8BIT
VIDEO_IR_10BIT = FREENECT_VIDEO_IR_10BIT
VIDEO_IR_10BIT_PACKED = FREENECT_VIDEO_IR_10BIT_PACKED
VIDEO_YUV_RGB = FREENECT_VIDEO_YUV_RGB
VIDEO_YUV_RAW = FREENECT_VIDEO_YUV_RAW
DEPTH_11BIT = FREENECT_DEPTH_11BIT
DEPTH_10BIT = FREENECT_DEPTH_10BIT
DEPTH_11BIT_PACKED = FREENECT_DEPTH_11BIT_PACKED
DEPTH_10BIT_PACKED = FREENECT_DEPTH_10BIT_PACKED
DEPTH_REGISTERED = FREENECT_DEPTH_REGISTERED
DEPTH_MM = FREENECT_DEPTH_MM
LED_OFF = FREENECT_LED_OFF
LED_GREEN = FREENECT_LED_GREEN
LED_RED = FREENECT_LED_RED
LED_YELLOW = FREENECT_LED_YELLOW
LED_BLINK_GREEN = FREENECT_LED_BLINK_GREEN
LED_BLINK_RED_YELLOW = FREENECT_LED_BLINK_RED_YELLOW
RESOLUTION_LOW = FREENECT_RESOLUTION_LOW
RESOLUTION_MEDIUM = FREENECT_RESOLUTION_MEDIUM
RESOLUTION_HIGH = FREENECT_RESOLUTION_HIGH
DEVICE_MOTOR = FREENECT_DEVICE_MOTOR
DEVICE_CAMERA = FREENECT_DEVICE_CAMERA
DEVICE_AUDIO = FREENECT_DEVICE_AUDIO

cdef inline str _format_ptr(void *ptr):
    if sizeof(void *) == 4:
        return "0x%08x" % <Py_ssize_t>ptr
    elif sizeof(void *) == 8:
        return "0x%016x" % <Py_ssize_t>ptr
    else:
        raise TypeError("What kind of system are you using?!")

cdef class CtxPtr:
    cdef freenect_context* _ptr
    def __init__(self):
        # Safety: do not allow Python to create instances as they would be NULL
        raise TypeError("Cannot create instances of CtxPtr from Python")

    def __repr__(self):
        return "<Ctx Pointer %s>" % _format_ptr(self._ptr)

cdef class DevPtr:
    cdef freenect_device* _ptr
    cdef CtxPtr ctx
    def __init__(self):
        # Safety: do not allow Python to create instances as they would be NULL
        raise TypeError("Cannot create instances of DevPtr from Python")

    def __repr__(self):
        return "<Dev Pointer %s>" % _format_ptr(self._ptr)

cdef class StatePtr:
    cdef freenect_raw_tilt_state* _ptr
    def __init__(self):
        # Safety: do not allow Python to create instances as they would be NULL
        raise TypeError("Cannot create instances of StatePtr from Python")

    def __repr__(self):
        return "<State Pointer %s>" % _format_ptr(self._ptr)

    def _get_accelx(self):
        return int(self._ptr.accelerometer_x)

    def _get_accely(self):
        return int(self._ptr.accelerometer_y)

    def _get_accelz(self):
        return int(self._ptr.accelerometer_z)

    def _get_tilt_angle(self):
        return int(self._ptr.tilt_angle)

    def _get_tilt_status(self):
        return int(self._ptr.tilt_status)

    accelerometer_x = property(_get_accelx)
    accelerometer_y = property(_get_accely)
    accelerometer_z = property(_get_accelz)
    tilt_angle = property(_get_tilt_angle)
    tilt_status = property(_get_tilt_status)

def set_depth_mode(DevPtr dev, int res, int mode):
    return freenect_set_depth_mode(dev._ptr, freenect_find_depth_mode(res, mode))

def set_video_mode(DevPtr dev, int res, int mode):
    return freenect_set_video_mode(dev._ptr, freenect_find_video_mode(res, mode))

def get_depth_format(DevPtr dev):
    return freenect_get_current_depth_mode(dev._ptr).video_format

def get_video_format(DevPtr dev):
    return freenect_get_current_video_mode(dev._ptr).video_format

def start_depth(DevPtr dev):
    return freenect_start_depth(dev._ptr)

def start_video(DevPtr dev):
    return freenect_start_video(dev._ptr)

def stop_depth(DevPtr dev):
    return freenect_stop_depth(dev._ptr)

def stop_video(DevPtr dev):
    return freenect_stop_video(dev._ptr)

def shutdown(CtxPtr ctx):
    return freenect_shutdown(ctx._ptr)

def process_events(CtxPtr ctx):
    return freenect_process_events(ctx._ptr)

def num_devices(CtxPtr ctx):
    return freenect_num_devices(ctx._ptr)

def close_device(DevPtr dev):
    return freenect_close_device(dev._ptr)

def set_tilt_degs(DevPtr dev, float angle):
    freenect_set_tilt_degs(dev._ptr, angle)

def set_led(DevPtr dev, freenect_led_options option):
    return freenect_set_led(dev._ptr, option)

def update_tilt_state(DevPtr dev):
    return freenect_update_tilt_state(dev._ptr)

def get_tilt_state(DevPtr dev):
    cdef freenect_raw_tilt_state* state = freenect_get_tilt_state(dev._ptr)
    cdef StatePtr state_out = StatePtr.__new__(StatePtr)
    state_out._ptr = state
    return state_out

def get_mks_accel(StatePtr state):
    cdef double x, y, z
    freenect_get_mks_accel(state._ptr, &x, &y, &z)
    return x, y, z

def get_accel(DevPtr dev):
    """MKS Accelerometer helper

    Args:
        dev:

    Returns:
        (x, y, z) accelerometer values
    """
    update_tilt_state(dev)
    return get_mks_accel(get_tilt_state(dev))


def get_tilt_degs(StatePtr state):
    return freenect_get_tilt_degs(state._ptr)


def error_open_device():
    print("Error: Can't open device. 1.) is it plugged in? 2.) Read the README")

cpdef init():
    cdef freenect_context* ctx
    if freenect_init(&ctx, NULL) < 0:
        return
    # We take both the motor and camera devices here, since we provide access
    # to both but haven't wrapped the python API for selecting subdevices yet.
    # Also, we don't support audio in the python wrapper yet, so no sense claiming
    # the device.
    freenect_select_subdevices(ctx, <freenect_device_flags> (FREENECT_DEVICE_MOTOR | FREENECT_DEVICE_CAMERA))
    cdef CtxPtr ctx_out = CtxPtr.__new__(CtxPtr)
    ctx_out._ptr = ctx
    return ctx_out

cpdef open_device(CtxPtr ctx, int index):
    cdef freenect_device* dev
    if freenect_open_device(ctx._ptr, &dev, index) < 0:
        return
    cdef DevPtr dev_out = DevPtr.__new__(DevPtr)
    dev_out._ptr = dev
    dev_out.ctx = ctx
    return dev_out

_depth_cb, _video_cb = None, None

cdef void depth_cb(freenect_device *dev, void *data, uint32_t timestamp) with gil:
    cdef freenect_frame_mode mode = freenect_get_current_depth_mode(dev)
    if not mode.is_valid:
        return
    if not _depth_cb:
        return
    cdef DevPtr dev_out = DevPtr.__new__(DevPtr)
    dev_out._ptr = dev
    pydata = _depth_cb_np(data, &mode)
    _depth_cb(dev_out, pydata, timestamp)

cdef void video_cb(freenect_device *dev, void *data, uint32_t timestamp) with gil:
    cdef freenect_frame_mode mode = freenect_get_current_video_mode(dev)
    if not mode.is_valid:
        return
    if not _video_cb:
        return
    cdef DevPtr dev_out = DevPtr.__new__(DevPtr)
    dev_out._ptr = dev
    pydata = _video_cb_np(data, &mode)
    _video_cb(dev_out, pydata, timestamp)

def set_depth_callback(DevPtr dev, cb):
    global _depth_cb
    if cb is not None:
        _depth_cb = cb
        freenect_set_depth_callback(dev._ptr, depth_cb)
    else:
        _depth_cb = None
        freenect_set_depth_callback(dev._ptr, NULL)

def set_video_callback(DevPtr dev, cb):
    global _video_cb
    if cb is not None:
        _video_cb = cb
        freenect_set_video_callback(dev._ptr, video_cb)
    else:
        _video_cb = None
        freenect_set_video_callback(dev._ptr, NULL)


class Kill(Exception):
    """This kills the runloop, raise from the body only"""


def runloop(depth=None, video=None, body=None, dev=None):
    """Sets up the kinect and maintains a runloop

    This is where most of the action happens.  You can get the dev pointer from the callback
    and let this function do all of the setup for you.  You may want to use threads to perform
    computation externally as the callbacks should really just be used for copying data.

    Args:
        depth: A function that takes (dev, depth, timestamp), corresponding to C function.
            If None (default), then you won't get a callback for depth.
        video: A function that takes (dev, video, timestamp), corresponding to C function.
            If None (default), then you won't get a callback for video.
        body: A function that takes (dev, ctx) and is called in the body of process_events
        dev: Optional freenect device context. If supplied, this function will use it instead
            of creating and destroying its own..
    """
    global _depth_cb, _video_cb
    if depth:
       _depth_cb = depth
    if video:
       _video_cb = video
    cdef DevPtr mdev
    cdef CtxPtr ctx
    cdef freenect_device* devp
    cdef freenect_context* ctxp
    if dev is None:
        ctx = init()
        if not ctx:
            error_open_device()
            return
        mdev = open_device(ctx, 0)
        if not mdev:
            error_open_device()
            return
        if depth is not None:
            freenect_set_depth_mode(mdev._ptr, freenect_find_depth_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_DEPTH_11BIT))
        if video is not None:
            freenect_set_video_mode(mdev._ptr, freenect_find_video_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_VIDEO_RGB))

    else:
        mdev = dev
    devp = mdev._ptr
    ctxp = mdev.ctx._ptr
    if depth is not None:
        freenect_start_depth(devp)
        freenect_set_depth_callback(devp, depth_cb)
    if video is not None:
        freenect_start_video(devp)
        freenect_set_video_callback(devp, video_cb)
    try:
        while True:
            with nogil:
                if freenect_process_events(ctxp) < 0:
                    break
            if body:
                body(mdev, mdev.ctx)
    except Kill:
        pass
    freenect_stop_depth(devp)
    freenect_stop_video(devp)
    if dev is None:
        freenect_close_device(devp)
        freenect_shutdown(ctxp)

def base_runloop(CtxPtr ctx, body=None):
    """Starts a runloop

    This function can be used instead of runloop() to allow the Python code to
    perform all setup steps independently. This simply calls process_events in
    a loop, optionally calling a body function in between. Raise the Kill
    exception to break out of the runloop.

    Args:
        ctx: Freenect library context
        body: A function that takes (ctx) and is called in the body of process_events
    """
    cdef freenect_context* ctxp
    ctxp = ctx._ptr
    try:
        while True:
            with nogil:
                if freenect_process_events(ctxp) < 0:
                    break
            if body:
                body(ctx)
    except Kill:
        pass

import_array()

cdef object _depth_cb_np(void *data, freenect_frame_mode *mode):
    cdef npc.npy_intp dims[2]

    if mode.video_format in (DEPTH_11BIT, DEPTH_10BIT, DEPTH_REGISTERED, DEPTH_MM):
        dims[0], dims[1] = mode.height, mode.width
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT16, data)
    else:
        return (<char *>data)[:mode.bytes]


cdef _video_cb_np(void *data, freenect_frame_mode *mode):
    cdef npc.npy_intp dims[3]

    if mode.video_format in (VIDEO_RGB, VIDEO_YUV_RGB):
        dims[0], dims[1], dims[2]  = mode.height, mode.width, 3
        return PyArray_SimpleNewFromData(3, dims, npc.NPY_UINT8, data)
    elif mode.video_format == VIDEO_IR_8BIT:
        dims[0], dims[1]  = mode.height, mode.width
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT8, data)
    elif mode.video_format == VIDEO_IR_10BIT:
        dims[0], dims[1]  = mode.height, mode.width
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT16, data)
    else:
        return (<char *>data)[:mode.bytes]

def sync_get_depth(index=0, format=DEPTH_11BIT):
    """Get the next available depth frame from the kinect, as a numpy array.

    Args:
        index: Kinect device index (default: 0)
        format: Depth format (default: DEPTH_11BIT)

    Returns:
        (depth, timestamp) or None on error
        depth: A numpy array, shape:(640,480) dtype:np.uint16
        timestamp: int representing the time
    """
    cdef void* data
    cdef uint32_t timestamp
    cdef npc.npy_intp dims[2]
    cdef int out
    cdef int _index = index
    cdef freenect_depth_format _format = format
    with nogil:
        out = freenect_sync_get_depth(&data, &timestamp, _index, _format)
    if out:
        error_open_device()
        return
    if format in [DEPTH_11BIT, DEPTH_10BIT, DEPTH_MM, DEPTH_REGISTERED]:
        dims[0], dims[1]  = 480, 640
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT16, data), timestamp

    else:
        raise TypeError('Conversion not implemented for type [%d]' % (format))


def sync_get_video(index=0, format=VIDEO_RGB):
    """Get the next available rgb frame from the kinect, as a numpy array.

    Args:
        index: Kinect device index (default: 0)
        format: Depth format (default: VIDEO_RGB)

    Returns:
        (depth, timestamp) or None on error
        depth: A numpy array, shape:(480, 640, 3) dtype:np.uint8
        timestamp: int representing the time
    """
    cdef void* data
    cdef uint32_t timestamp
    cdef npc.npy_intp dims[3]
    cdef int out
    cdef int _index = index
    cdef freenect_video_format _format = format

    with nogil:
        out = freenect_sync_get_video(&data, &timestamp, _index, _format)
    if out:
        error_open_device()
        return
    if format == VIDEO_RGB:
        dims[0], dims[1], dims[2]  = 480, 640, 3
        return PyArray_SimpleNewFromData(3, dims, npc.NPY_UINT8, data), timestamp
    elif format == VIDEO_IR_8BIT:
        dims[0], dims[1]  = 480, 640
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT8, data), timestamp
    elif format == VIDEO_IR_10BIT:
        dims[0], dims[1]  = 480, 640
        return PyArray_SimpleNewFromData(2, dims, npc.NPY_UINT16, data), timestamp
    else:
        raise TypeError('Conversion not implemented for type [%d]' % (format))

#########################################
############## NEW CODE #################

def depth_to_xy(depth_image, index=0):


    depth_y = 480
    depth_x = 640


    cdef npc.npy_intp dims[3]
    cdef npc.npy_float _y[480 * 640]
    cdef npc.npy_float _x[480 * 640]
    cdef npc.npy_int16 _z[480 * 640]
    cdef npc.npy_uint16 _px[480 * 640]
    cdef npc.npy_uint16 _py[480 * 640]
    cdef int _index = index
    cdef npc.npy_float _xyz[480 * 640 * 3]

    for py in range(0, depth_y):
        for px in range(0, depth_x):

            z = depth_image[py][px]
            _z[py * depth_x + px] = z
            _px[py * depth_x + px] = px
            _py[py * depth_x + px] = py

    freenect_sync_camera_to_world(_px, _py, _z, _x, _y, _index)

    for py in range(0, depth_y):
        for px in range(0, depth_x):

            _xyz[py * depth_x * 3 + px * 3] = _x[py * depth_x + px]
            _xyz[py * depth_x * 3 + px * 3 + 1] = _y[py * depth_x + px]
            _xyz[py * depth_x * 3 + px * 3 + 2] = _z[py * depth_x + px]

    dims[0], dims[1], dims[2] = depth_y, depth_x, 3

    xyz_arr = PyArray_SimpleNewFromData(3, dims, npc.NPY_FLOAT, _xyz)
    xyz = np.copy(xyz_arr)

    return xyz

def isolate_object(rgb_raw, depth_mm, box, index=0):


    depth_y = 480
    depth_x = 640

    cdef npc.npy_intp dims[3]
    cdef npc.npy_uint8 _rgb_raw[480*640*3]
    cdef npc.npy_uint16 _depth_mm[480*640]
    cdef npc.npy_uint8 _rgb_reg[480*640*3]
    cdef npc.npy_uint32 _box[4]
    cdef int _index = index


    width = box[2][2]
    left = int(round(box[2][0] - 0.5 * width))
    height = box[2][3]
    top = int(round(box[2][1] - 0.5 * height))
    right = int(round(left + width))
    bottom = int(round(top + height))

    if (left < 0): left = 0
    if (right > rgb_raw.shape[1] - 1): right = rgb_raw.shape[1] - 1
    if (top < 0): top = 0
    if (bottom > rgb_raw.shape[0] - 1): bottom = rgb_raw.shape[0] - 1

    _box[0] = left
    _box[1] = top
    _box[2] = right
    _box[3] = bottom

    for y in range(0,depth_y):
        for x in range(0,depth_x):
            for col in range(0, 3):
                _rgb_raw[y*depth_x*3 + x*3 + col] = rgb_raw[y][x][col]

    for x in range(0,depth_x):
        for y in range(0,depth_y):
            _depth_mm[y*depth_x + x] = depth_mm[y][x]

    dims[0], dims[1], dims[2] = depth_y, depth_x, 3

    freenect_sync_isolate_object(_depth_mm, _rgb_raw, _box, _rgb_reg, _index)

    cd_arr = PyArray_SimpleNewFromData(3, dims, npc.NPY_UINT8, _rgb_reg)
    cd = np.copy(cd_arr)

    return cd



def color_to_depth(rgb_raw, depth_mm, index=0):

    depth_y = 480
    depth_x = 640

    cdef npc.npy_intp dims[3]
    cdef npc.npy_uint8 _rgb_raw[480*640*3]
    cdef npc.npy_uint16 _depth_mm[480*640]
    cdef npc.npy_uint8 _rgb_reg[480*640*3]
    cdef int _index = index

    for y in range(0,depth_y):
        for x in range(0,depth_x):
            for col in range(0, 3):
                _rgb_raw[y*depth_x*3 + x*3 + col] = rgb_raw[y][x][col]

    for x in range(0,depth_x):
        for y in range(0,depth_y):
            _depth_mm[y*depth_x + x] = depth_mm[y][x]

    dims[0], dims[1], dims[2] = depth_y, depth_x, 3

    freenect_sync_map_rgb_to_depth(_depth_mm, _rgb_raw, _rgb_reg, _index)

    cd_arr = PyArray_SimpleNewFromData(3, dims, npc.NPY_UINT8, _rgb_reg)
    cd = np.copy(cd_arr)

    return cd


# def synch_get_video_and_depth(index=0, format_vid=VIDEO_RGB, format_depth=DEPTH_MM):
#
#     cdef void * data_vid
#     cdef uint32_t timestamp_vid
#     cdef npc.npy_intp dims_vid[3]
#     cdef int out_vid
#     cdef freenect_video_format _format_vid = format_vid
#
#     # Get image
#     with nogil:
#         out = freenect_sync_get_video( & data_vid, & timestamp_vid, _index, _format_vid)
#     if out:
#         error_open_device()
#         return
#     if format_vid == VIDEO_RGB:
#         dims_vid[0], dims_vid[1], dims_vid[2] = 480, 640, 3
#         vid = PyArray_SimpleNewFromData(3, dims_vid, npc.NPY_UINT8, data_vid), timestamp_vid
#     elif format_vid == VIDEO_IR_8BIT:
#         dims_vid[0], dims_vid[1] = 480, 640
#         vid = PyArray_SimpleNewFromData(2, dims_vid, npc.NPY_UINT8, data_vid), timestamp_vid
#     elif format_vid == VIDEO_IR_10BIT:
#         dims_vid[0], dims_vid[1] = 480, 640
#         vid = PyArray_SimpleNewFromData(2, dims_vid, npc.NPY_UINT16, data_vid), timestamp_vid
#     else:
#         raise TypeError('Conversion not implemented for type [%d]' % (format_vid))
#
#     cdef void * data_depth
#     cdef uint32_t timestamp_depth
#     cdef npc.npy_intp dims_depth[2]
#     cdef int out_depth
#     cdef int _index = index
#     cdef freenect_depth_format _format_depth = format_depth
#
#     # Get depth
#     with nogil:
#         out = freenect_sync_get_depth( &data_depth, &timestamp_depth, _index, _format_depth)
#     if out:
#         error_open_device()
#         return
#     if format_depth in [DEPTH_11BIT, DEPTH_10BIT, DEPTH_MM, DEPTH_REGISTERED]:
#         dims_depth[0], dims_depth[1] = 480, 640
#         depth = PyArray_SimpleNewFromData(2, dims_depth, npc.NPY_UINT16, data_depth), timestamp_depth
#     else:
#         raise TypeError('Conversion not implemented for type [%d]' % (format_depth))

    # Map image to depth frame

    # cdef npc.npy_intp dims[3]
    # cdef uint16_t _depth_mm[480 * 640]
    # cdef uint8_t _rgb_raw[480 * 640 * 3]
    # cdef uint8_t _rgb_reg[480 * 640 * 3]
    #
    # cdef uint16_t temp = (uint16_t)data_depth[0]

    # for i in range(0, 480 * 640):
    #     temp = data_depth[i]
    #     _depth_mm[i] = temp
    #
    # for i in range(0, 480 * 640 * 3):
    #     _rgb_raw[i] = data_vid[i]

    # dims[0], dims[1], dims[2] = 480, 640, 3
    # freenect_map_rgb_to_depth(_depth_mm, _rgb_raw, _rgb_reg, _index)
    # vid_fixed = PyArray_SimpleNewFromData(3, dims, npc.NPY_UINT8, _rgb_reg)

    # return vid, depth


#########################################


def sync_stop():
    """Terminate the synchronous runloop if running, else this is a NOP
    """
    freenect_sync_stop()


