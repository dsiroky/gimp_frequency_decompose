#!/usr/bin/env python

from gimpfu import *

def separate(img, orig, radius):
    blurred = orig.copy()
    img.add_layer(blurred, 0)
    pdb.plug_in_gauss_iir2(img, blurred, radius, radius)
    origcopy = orig.copy()
    img.add_layer(origcopy, 1)
    residual = blurred.copy()
    pdb.gimp_layer_set_mode(blurred, GRAIN_EXTRACT_MODE)
    xlayer = pdb.gimp_image_merge_down(img, blurred, 0)
    pdb.gimp_layer_set_mode(xlayer, GRAIN_MERGE_MODE)
    xlayer.name = "radius %.1f" % radius
    return residual

def do_stuff(img, layer, basepixels, steps) :
    gimp.progress_init("Doing stuff to " + layer.name + "...")

    pdb.gimp_image_undo_group_start(img)

    nlayer = layer
    for step in range(steps):
        nlayer = separate(img, nlayer, basepixels * 2 ** step)

    img.add_layer(nlayer, steps)
    nlayer.name = "residual"

    pdb.gimp_image_undo_group_end(img)

register(
    "frequency_decompose",
    "Frequency decompose",
    "Decompose image to layers with different frequencies.",
    "David Siroky",
    "David Siroky",
    "2016",
    "<Image>/Filters/Generic/Frequency decompose",
    "*",
    [
        (PF_FLOAT, "basepixels", "Base pixels", 3.0),
        (PF_INT, "steps", "Steps", 5)
    ],
    [],
    do_stuff
    )

main()
