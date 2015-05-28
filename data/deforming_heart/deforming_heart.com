#Example a/deforming_heart: Deforming heart, time varying nodes, strain and deformed fibres
#
# This example shows how a whole sequence of solutions can be read in at one time and then
# animated.  The viewpoint and scene description can be interactively adjusted while the
# heart is deforming.

#Create some materials
gfx create material bluey ambient 0 0.25 0.5 diffuse 0 0.4 1 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3
gfx create material copper ambient 1 0.2 0 diffuse 0.6 0.3 0 emission 0 0 0 specular 0.7 0.7 0.5 alpha 1 shininess 0.3
gfx create material gold ambient 1 0.4 0 diffuse 1 0.7 0 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.8
gfx create material silver ambient 0.4 0.4 0.4 diffuse 0.7 0.7 0.7 emission 0 0 0 specular 0.7 0.7 0.7 alpha 1 shininess 0.6

#Create a strain spectrum
gfx create spectrum strain
gfx modify spectrum strain clear overwrite_colour
gfx modify spectrum strain linear reverse range -1 0 extend_below red colour_range 1 1 ambient diffuse component 1
gfx modify spectrum strain linear reverse range 0 1 extend_above blue colour_range 1 1 ambient diffuse component 1
gfx modify spectrum strain linear reverse range 0 1 extend_above green colour_range 0.5 0.5 ambient diffuse component 1

#Read in the sequence of nodal positions.
for $i (0..49)
  {
	 $filename = sprintf("heart%04d.exnode", $i);
	 print "Reading $filename time $i\n";
	 gfx read node "$example/$filename" time $i;
  }

#Read in the element description
gfx read elements $example/heart.exelem;

#Create a window and set the viewpoint
gfx create window 1
gfx modify window 1 set perturb_lines
gfx modify window 1 view parallel eye_point -49.8293 -203.894 194.97 interest_point 9.48997 9.25073 -1.96496 up_vector -0.978396 0.111345 -0.174195 view_angle 24.2458 near_clipping_plane 2.96197 far_clipping_plane 1058.51 relative_viewport ndc_placement -1 1 2 2 viewport_coordinates 0 0 1 1

# create initial lines visualisation
gfx modify g_element "/" general clear;
gfx modify g_element heart general clear;
gfx modify g_element heart lines select_on material gold selected_material default_selected

#Set the timekeeper playing
gfx timekeeper default play speed 50 skip;
gfx create time_editor

# Now we can modify the graphics while the time is running....
gfx modify g_element heart surfaces exterior face xi3_0 select_on material copper selected_material default_selected render_shaded

gfx edit scene

#Read in a reference heart position
gfx read node $example/reference_heart0000.exnode;
gfx read elements $example/reference_heart.exelem;

#Define the rc_equivalents of the prolate spheroidal coordinates
gfx define field rc_reference_coordinates coordinate_transform field reference_coordinates
gfx define field rc_coordinates coordinate_transform field coordinates

#Calculate the strains
gfx define field F gradient coordinate rc_reference_coordinates field rc_coordinates
gfx define field F_transpose transpose source_number_of_rows 3 field F
gfx define field identity3 composite 1 0 0 0 1 0 0 0 1

gfx define field C matrix_multiply number_of_rows 3 fields F_transpose F
gfx define field E2 add fields C identity3 scale_factors 1 -1
gfx define field E coordinate_system rectangular_cartesian scale field E2 scale_factors 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5

gfx define field principal_strains eigenvalues field E
gfx define field principal_strain_vectors eigenvectors eigenvalues principal_strains
gfx define field deformed_principal_strain_vectors matrix_multiply number_of_rows 3 fields principal_strain_vectors F_transpose

gfx define field deformed_principal_strain_vector1 composite deformed_principal_strain_vectors.1 deformed_principal_strain_vectors.2 deformed_principal_strain_vectors.3
gfx define field deformed_principal_strain_vector2 composite deformed_principal_strain_vectors.4 deformed_principal_strain_vectors.5 deformed_principal_strain_vectors.6
gfx define field deformed_principal_strain_vector3 composite deformed_principal_strain_vectors.7 deformed_principal_strain_vectors.8 deformed_principal_strain_vectors.9
# since above vectors have the stretch as their magnitude, normalize them:
gfx define field norm_def_principal_strain_vector1 normalise field deformed_principal_strain_vector1
gfx define field norm_def_principal_strain_vector2 normalise field deformed_principal_strain_vector2
gfx define field norm_def_principal_strain_vector3 normalise field deformed_principal_strain_vector3

gfx define field principal_strain1 composite principal_strains.1
gfx define field principal_strain2 composite principal_strains.2
gfx define field principal_strain3 composite principal_strains.3

#Calculate the deformed fibre axes
gfx define field fibre_axes fibre_axes coordinate rc_reference_coordinates fibre reference_fibres
gfx define field deformed_fibre_axes matrix_multiply number_of_rows 3 fields fibre_axes F_transpose

gfx define field deformed_fibre composite deformed_fibre_axes.1 deformed_fibre_axes.2 deformed_fibre_axes.3
gfx define field deformed_sheet composite deformed_fibre_axes.4 deformed_fibre_axes.5 deformed_fibre_axes.6
gfx define field norm_def_fibre normalise field deformed_fibre
gfx define field def_fibre_cross cross_product dimension 3 fields norm_def_fibre deformed_sheet
gfx define field norm_def_fibre_cross normalise field def_fibre_cross
gfx define field norm_def_fibre_cross_normal cross_product dimension 3 fields norm_def_fibre norm_def_fibre_cross
gfx define field orthonormal_deformed_fibre_axes composite norm_def_fibre norm_def_fibre_cross_normal norm_def_fibre_cross

#Show deforming fibres and strain vectors
gfx modify g_element heart streamlines xi 0.5,0.5,0.5 ribbon vector deformed_fibre_axes length 10 width 1 no_data select_on material silver selected_material default_selected
gfx modify g_element heart element_points glyph mirror_cone general size "0*1*1" centre 0,0,0 orientation norm_def_principal_strain_vector1 variable_scale principal_strain1 scale_factors "20*0*0" use_elements cell_centres discretization "1*1*1" native_discretization NONE select_on material bluey data principal_strain1 spectrum strain selected_material default_selected
gfx modify g_element heart element_points glyph mirror_cone general size "0*1*1" centre 0,0,0 orientation norm_def_principal_strain_vector2 variable_scale principal_strain2 scale_factors "20*0*0" use_elements cell_centres discretization "1*1*1" native_discretization NONE select_on material bluey data principal_strain2 spectrum strain selected_material default_selected
gfx modify g_element heart element_points glyph mirror_cone general size "0*1*1" centre 0,0,0 orientation norm_def_principal_strain_vector3 variable_scale principal_strain3 scale_factors "20*0*0" use_elements cell_centres discretization "1*1*1" native_discretization NONE select_on material bluey data principal_strain3 spectrum strain selected_material default_selected
#By toggling off the visibility of the different settings you can vastly speed up the frame rate.

if ($TESTING)
{
	gfx write node group heart fields coordinates & fibres output time 24;	
}
