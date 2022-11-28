import spiceypy as cspice
import bpy
import math
import mathutils
import os
import json
import numpy as np

with open('config.json', 'r') as f:
    config = json.load(f)

mk = config['metakernel']
cspice.unload(mk)
cspice.furnsh(mk)

scalefactor = 1
lt = config['lt']
instrument = config['instrument']
#
# create time series
#
utc0 = config['utc0']
et0 = cspice.utc2et(utc0)
utcf = config['utcf']
etf = cspice.utc2et(utcf)
times = np.linspace(et0, etf, int(config['tsamples']))

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

    cam.data.angle = math.radians(config["yfov"])
    r = bpy.context.scene.render
    r.resolution_x = config["pxlines"]
    r.resolution_y = config["pxsamples"]

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
