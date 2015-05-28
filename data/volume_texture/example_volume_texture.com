# Visualisation and segmentation of 3-D images of the foot
#
# Reads a series of images from the Visible Human Dataset into one large
# 3-dimensional texture.  This is viewed on slice planes of constant x,
# y or z coordinate.  Scalar fields based on the colours in the texture
# are established to distinguish regions of muscle, bone and the exterior
# skin of the foot and isosurfaces are used to show the boundaries of
# these structures.
#
# Notes:
# - A big & fast computer is needed to calculate isosurfaces at high
#   resolution.
# - A high-end graphics card with lots of texture memory and capable of
#   hardware 3-D textures is required to show the 3-D texture on slice
#   planes.
#
# Note that all images are copyright to and obtained under license
# from the Visible Human Project:
# http://www.nlm.nih.gov/research/visible/visible_human.html
#
# Read in 128 images of 256x400 resolution into 3-D texture 'foot'. These
# are a cropped subset of the Visible Human Dataset containing just the
# left foot. (You might as well use power-of-two resolutions as I have
# since internal storage is padded to the next highest power-of-two.
# Otherwise keep 3-D textures as small as possible for speed!)
# Since this data has one texture-pixel (or texel) per mm, we set the
# physical size of the texture to 256x400x128.
# Note the image file numbers are substituted into the pattern "0000"
# and go from 1860 to 1733 with an increment of -1.
# The compress parameter requests the graphics hardware to compress the texture
# in its representation of the texture allowing the image to be stored in much less
# memory than uncompressed.
# It takes a few seconds to read in this much image data.
gfx create texture foot width 256 height 400 depth 128 clamp_wrap linear_filter image $example/foot0000.jpg number_pattern "0000" number_series 1860 1733 -1 compress;
#
# Create a material containing the texture that we may select along
# with appropriate texture coordinates, to visualise the 3-D image
# on our graphics.
gfx create material foot texture foot;
#
# Create some more materials to colour parts of the model with.
gfx create material bone ambient 0.7 0.7 0.3 diffuse 0.9 0.9 0.8 emission 0 0 0 specular 0.05 0.05 0.05 alpha 1 shininess 0.1;
gfx create material muscle ambient 0.17 0.06 0.06 diffuse 0.35 0.12 0.12 emission 0 0 0 specular 0.17 0.06 0.06 alpha 1 shininess 0.1;
gfx create material skin ambient 0.8 0.8 0.4 diffuse 0.7 0.29 0.16 emission 0.06 0.05 0.03 specular 0.12 0.12 0.08 alpha 1 shininess 0.1;
gfx create material green ambient 0 1 0 diffuse 0 1 0
gfx cre mat bluey ambient 0 0.25 0.5 diffuse 0 0.4 1 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3
#
# Read in a 256x400x128 mm single-element block to view the texture in.
# These dimensions match the physical size and location of the texture.
# Later we will use the "coordinates" field as texture coordinates.
gfx read nodes $example/texture_block.exnode
gfx read elements $example/texture_block.exelem
#
# Since it is expensive to compute high-res iso-surfaces, a slightly
# smaller mesh that just envelopes the foot is read in.  It contains
# a block of elements that are each exactly 32x32x32 mm in size. The
# corners of each element are offset to lie at exactly the centre of
# a 3-D texel.  Hence, we can subdivide these elements in powers of 2
# up to 32 and get the most accurate isosurfaces for the least effort.
gfx read nodes $example/iso_block.exnode
gfx read elements $example/iso_block.exelem
#
# Define the components of the coordinate field as individual scalar
# fields for defining slice planes.
gfx define field x component coordinates.x;
gfx define field y component coordinates.y;
gfx define field z component coordinates.z;
#
# Define the "tex" field to return the red, green and blue components
# of the texture (each on [0,1]) by looking up the texture at the
# position of the "coordinates" field in any element.
gfx define field tex sample_texture coordinates coordinates field foot minimum 0.0 maximum 1.0;
#
# Extract several scalar quantities from tex, notably its colour
# components which the user may choose to visualise.
gfx define field tex.1 component tex.1;
gfx define field tex.2 component tex.2;
gfx define field tex.3 component tex.3;
gfx define field mag_tex magnitude field tex;
gfx define field tex_avg sum_components field tex weights 0.333 0.334 0.333;
# Black and white scalar weighting of red, green and blue reflects the
# relative brightness of the three components to our eyes.
gfx define field tex_bw sum_components field tex weights 0.3 0.55 0.15;
#
# Draw the 3-D texture on the surfaces x = 128.5 and y = 185.5.  The
# .5 makes the slice in the centre of a row of texels.
gfx modify g_element texture_block general clear circle_discretization 6 default_coordinate coordinates element_discretization "1*1*1" native_discretization none;
gfx modify g_element texture_block lines select_on material default selected_material default_selected;
gfx modify g_element texture_block iso_surfaces iso_scalar x iso_value 128.5 use_elements select_on material foot texture_coordinates coordinates selected_material default_selected render_shaded;
gfx modify g_element texture_block iso_surfaces iso_scalar y iso_value 185.5 use_elements select_on material foot texture_coordinates coordinates selected_material default_selected render_shaded;
#
# Note that by opening the "Scene editor" you are free to choose other
# values of x and y to view the texture on, or even another slice plane by
# changing the iso-scalar field in iso_surfaces of the "texture_block"
# group.
#
# Draw the lines of the iso_block mesh.
gfx modify g_element iso_block general clear circle_discretization 6 default_coordinate coordinates element_discretization "16*16*16" native_discretization none;
gfx modify g_element iso_block lines select_on material green selected_material default_selected;
#
if (!$TESTING)
{
  # Create a 3d window
  gfx create window 1
  gfx mod win 1 view perspective
  gfx mod win 1 image view_all
}
#
# Visualise the bones (and some of the fat since they are very similar in
# colour). We do this by generating a scalar field "mag_non_bone" which
# measures the distance in colourspace from an average bone colour of
# Red, Green, Blue = 0.9, 0.75, 0.6.
# This takes a long time to calculate so they are made invisible by default;
# you will have to check their visibility box in the scene editor to see them.
gfx define field non_bone offset field foot offsets -0.9 -0.75 -0.6;
gfx define field mag_non_bone magnitude field non_bone;
gfx modify g_element iso_block iso_surfaces iso_scalar mag_non_bone iso_value 0.2 use_elements select_on material bone texture_coordinates coordinates selected_material default_selected render_shaded invisible;
#
# Visualise the muscles (and some blood vessels) in a similar fashion
# using field "mag_non_muscle" which measures the distance the colour
# is from an average muscle tone.
# This also takes a little while to calculate.
gfx define field non_muscle coordinate_system rectangular_cartesian offset field foot offsets -0.35 -0.12 -0.12;
gfx define field mag_non_muscle coordinate_system rectangular_cartesian magnitude field non_muscle;
gfx modify g_element iso_block iso_surfaces iso_scalar mag_non_muscle iso_value 0.2 use_elements select_on material muscle texture_coordinates coordinates selected_material default_selected render_shaded;
#
# Many combinations of colours adequately differentiate the skin from
# the surrounding blue resin. In the following we promote blue values and
# penalise red and green components. Experimentation gave the value of
# -0.25 which gives a good indication of the skin, although admittedly it
# is slightly outside of it.
gfx define field blue coordinate_system rectangular_cartesian sum_components field foot weights -1 -1 1;
gfx modify g_element iso_block iso_surfaces iso_scalar blue iso_value -0.25 use_elements select_on material skin texture_coordinates coordinates selected_material default_selected render_shaded;
#
# Open the Scene Editor to enable visibility of parts of the image
# to be switched on and off, discretization to be controlled or
# new graphics to be added.
if (!$TESTING)
{
  gfx edit scene;
}
if ($TESTING)
{
  # Turn off all graphics but a lo-res foot skin and export VRML
  gfx modify g_element texture_block general clear circle_discretization 6 default_coordinate coordinates element_discretization "1*1*1" native_discretization none;
  # Use 6*6*6 discretization to test linear filtering with sample_texture
  gfx modify g_element iso_block general clear circle_discretization 6 default_coordinate coordinates element_discretization "6*6*6" native_discretization none;
  gfx modify g_element iso_block iso_surfaces iso_scalar blue iso_value -0.25 use_elements select_on material skin texture_coordinates coordinates selected_material default_selected render_shaded;
  gfx export vrml file foot.wrl
}
#
# Notes & further exercises:
# - There are lots of combinations of colours that will adequately
#   segment many of the features in such 3-D images.  However, subtle
#   changes such as the edges of bones in visible light images and
#   fat are not easy to decipher with such simple methods.
# - If you have the time, try computing the iso-surfaces at 32*32*32
#   resolution to see the best quality possible from these images.
# - On any of the above graphics you may choose the "foot" material
#   to colour the iso-surfaces.  For this to look right you will
#   have to allow proper lighting of the foot texture with the
#   command "gfx modify texture foot modulate". The result tells
#   how well you have segmented and can help remove visual clutter.
#   The muscle layers are particularly good in this example,
#   being slightly redish-brown.
# - One way to help find appropriate scalars and values of scalars
#   for segmentation is to make hi-res slice planes with the same
#   resolution as the texture in the plane.  Choose your scalar
#   field as the data field for the iso-surface and play around
#   with the spectrums to see what threshold will work for you.
# - The original Visible Human dataset is twice the resolution in
#   each direction as the images used here, enabling even more
#   anatomical detail to be gained.
# - Enjoy!
