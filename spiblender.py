import spiceypy as cspice
import bpy
import math
import mathutils
import os
import json
import numpy as np

'''
   developed and maintained by the
    __   __   __      __   __     __   ___     __   ___  __          __   ___
   /__\ /__` '__\    /__` |__) | /  ` |__     /__` |__  |__) \  / | /  ` |__
   \__, .__/ \__/    .__/ |    | \__, |___    .__/ |___ |  \  \/  | \__, |___

   If you have any questions regarding this file contact the
   ESA SPICE Service (ESS) at ESAC:

           Alfredo Escalante Lopez
           (+34) 91-8131-429
           alfredo.escalante.lopez@ext.esa.int

'''

with open('config.json', 'r') as f:
    config = json.load(f)

mk = config['metakernel']
cspice.unload(mk)
cspice.furnsh(mk)

scalefactor = 1
lt = config['lt']

#
# create time series
#
utc0 = config['utc0']
et0 = cspice.utc2et(utc0)
utcf = config['utcf']
etf = cspice.utc2et(utcf)
times = np.linspace(et0, etf, int(config['tsamples']))

#
# compute camera id and parameters from kernel pool
#
instrument = config['instrument']
camera_id = cspice.bodn2c(instrument)
(shape, frame, bsight, vectors, bounds) = cspice.getfov(camera_id, 100)

camera_frame = config['instrument_frame']
if not camera_frame:
    if frame:
        camera_frame = frame
    else:
        print("CAMERA FRAME not defined for "
              "{}".format(config['camera']))

pixel_lines = config['pxlines']
pixel_samples = config['pxsamples']
if not pixel_lines or not pixel_samples:
    try:
        pixel_lines = int(cspice.gdpool('INS' + str(camera_id) + '_PIXEL_LINES', 0, 1))
        pixel_samples = int(cspice.gdpool('INS' + str(camera_id) + '_PIXEL_SAMPLES', 0, 1))
    except:
        pass
        print("PIXEL_SAMPLES and/or PIXEL_LINES not defined for "
              "{}".format(config['camera']))

yfov = config['yfov']
if not yfov:
    try:
        ref_angle = int(cspice.gdpool('INS' + str(camera_id) + '_FOV_REF_ANGLE', 0, 1))
        cross_angle = int(cspice.gdpool('INS' + str(camera_id) + '_FOV_CROSS_ANGLE', 0, 1))
        yfov = 2 * ref_angle
    except:
        pass
        print("Field of View aperture angles not defined for "
              "{}".format(config['camera']))

def render_and_save(filename, path):
    bpy.context.scene.render.filepath = path + filename + ".png"
    bpy.ops.render.render(use_viewport=True, write_still=True)


def update_object_pose(et, object, target, target_frame, center, center_frame, lt, fixpos=False):
    if not fixpos:
        r = cspice.spkpos(target, et, center_frame, lt, center)[0] / scalefactor
        object.scale = (1 / scalefactor, 1 / scalefactor, 1 / scalefactor)
        object.location.x = r[0]
        object.location.y = r[1]
        object.location.z = r[2]
    M = cspice.pxform(center_frame, target_frame, et)
    euler = cspice.m2eul(M, 1, 2, 3)
    object.rotation_euler = mathutils.Euler((euler[0], euler[1], euler[2]), 'XYZ')


def update_dirlight(et, sun, center, center_frame, lt):
    rsun = cspice.spkpos('SUN', et, center_frame, lt, center)[0]
    zsun = rsun / np.linalg.norm(rsun)
    xsun = np.array([0, 0, 1]) - np.dot(np.array([0, 0, 1]), zsun) * zsun
    xsun = xsun / np.linalg.norm(xsun)
    ysun = np.cross(zsun, xsun)
    Msun = np.array([[xsun[0], ysun[0], zsun[0]],
                     [xsun[1], ysun[1], zsun[1]],
                     [xsun[2], ysun[2], zsun[2]]])
    euler = cspice.m2eul(np.linalg.inv(Msun), 1, 2, 3)
    sun.rotation_euler = mathutils.Euler((euler[0], euler[1], euler[2]), 'XYZ')


def main(et, instrument):
    cam = bpy.context.scene.objects["Camera"]
    sun = bpy.context.scene.objects["Sun"]
    juice = bpy.context.scene.objects["JUICE"]
    jupiter = bpy.context.scene.objects["Jupiter"]
    ganymede = bpy.context.scene.objects["Ganymede"]
    europa = bpy.context.scene.objects["Europa"]
    callisto = bpy.context.scene.objects["Callisto"]
    io = bpy.context.scene.objects["Io"]
    earth = bpy.context.scene.objects["Earth"]
    moon = bpy.context.scene.objects["Moon"]

    cam.data.angle = math.radians(yfov)
    r = bpy.context.scene.render
    r.resolution_x = pixel_samples
    r.resolution_y = pixel_lines

    # update_object_pose(et, cam, 'JUICE_JMC-1', 'JUICE_JMC-1', 'JUICE_JMC-1', 'JUICE_JMC-1', 'LT+S', cam=True)
    update_object_pose(et, juice, 'JUICE', 'JUICE_SPACECRAFT', instrument, instrument, lt)
    update_object_pose(et, jupiter, 'JUPITER', 'IAU_JUPITER', instrument, instrument, lt)
    update_object_pose(et, ganymede, 'GANYMEDE', 'IAU_GANYMEDE', instrument, instrument, lt)
    update_object_pose(et, europa, 'EUROPA', 'IAU_EUROPA', instrument, instrument, lt)
    update_object_pose(et, callisto, 'CALLISTO', 'IAU_CALLISTO', instrument, instrument, lt)
    update_object_pose(et, io, 'IO', 'IAU_IO', instrument, instrument, lt)
    update_object_pose(et, earth, 'EARTH', 'IAU_EARTH', instrument, instrument, lt)
    update_object_pose(et, moon, 'MOON', 'IAU_MOON', instrument, instrument, lt)
    update_dirlight(et, sun, instrument, instrument, lt)

    utc = cspice.et2utc(et, 'ISOC', 0)
    render_and_save(instrument + utc, config["output"])


for et in times:
    main(et, instrument)
