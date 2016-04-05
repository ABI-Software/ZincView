"""
Example ZincView model loading script.

Loads a time-varying prolate spheroidal dog heart deformation simulation with fibre field.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from opencmiss.zinc.element import Element
from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.region import Region
from opencmiss.zinc.result import RESULT_OK
from opencmiss.zinc.streamregion import StreaminformationRegion
from opencmiss.zinc.spectrum import Spectrumcomponent

def loadModel(region):
    sir = region.createStreaminformationRegion()
    sir.createStreamresourceFile("texture_block.exelem")
    sir.createStreamresourceFile("texture_block.exnode")
    result = region.read(sir)
    if result != RESULT_OK:
        print("Failed to read texture_block")
        return False
    
    sir = region.createStreaminformationRegion()
    sir.createStreamresourceFile("iso_block.exelem")
    sir.createStreamresourceFile("iso_block.exnode")
    result = region.read(sir)
    if result != RESULT_OK:
        print("Failed to read iso_block")
        return False
    scene = region.getScene()
       
    field_module = region.getFieldmodule()
    coordinate_field = field_module.findFieldByName('coordinates')
    x_field = field_module.createFieldComponent(coordinate_field, 1)
    x_field.setName("x")
    x_field.setManaged(True)
    y_field = field_module.createFieldComponent(coordinate_field, 2)
    y_field.setName("y")
    y_field.setManaged(True)
    textureBlockGroup = field_module.findFieldByName('texture_block')
    isoBlockGroup = field_module.findFieldByName('iso_block')
    
    #coordinate_field = field_module.findFieldByName('coordinates')
    # Create an image field. A temporary xi source field is created for us.
    image_field = field_module.createFieldImage()
    image_field.setFilterMode(image_field.FILTER_MODE_LINEAR)
    image_field.setWrapMode(image_field.WRAP_MODE_EDGE_CLAMP)

    image_field.setDomainField(coordinate_field)
    image_field.setTextureCoordinateSizes([256, 400, 128])
    # Create a stream information object that we can use to read the
    # image file from disk
    stream_information = image_field.createStreaminformationImage()
    i = 1860
    while i >= 1733:
        stream_information.createStreamresourceFile("foot"+str(i)+ ".jpg")
        i = i - 1
    image_field.read(stream_information)
    foot = scene.getMaterialmodule().createMaterial()
    foot.setManaged(True)
    foot.setName("foot")
    foot.setTextureField(1, image_field)
    
    #rescaledImage = field_module.createFieldImagefilterRescaleIntensity(image_field, 0.0, 1.0)
    rescaledImage = image_field
    
    bone = scene.getMaterialmodule().findMaterialByName('bone')
    muscle = scene.getMaterialmodule().findMaterialByName('muscle')
    skin = scene.getMaterialmodule().createMaterial()
    skin.setName("skin")
    skin.setManaged(True)
    skin.setAttributeReal3(skin.ATTRIBUTE_AMBIENT, [0.8, 0.8, 0.4])
    skin.setAttributeReal3(skin.ATTRIBUTE_DIFFUSE, [0.7, 0.29, 0.16])
    skin.setAttributeReal3(skin.ATTRIBUTE_EMISSION, [0.06, 0.05, 0.03])
    skin.setAttributeReal3(skin.ATTRIBUTE_SPECULAR, [0.12, 0.12, 0.08])
    skin.setAttributeReal(skin.ATTRIBUTE_ALPHA, 1.0)
    skin.setAttributeReal(skin.ATTRIBUTE_SHININESS, 0.1)
    green = scene.getMaterialmodule().findMaterialByName('green')
    
    scene.beginChange()
    scene.removeAllGraphics()
    
    lines = scene.createGraphicsLines()
    lines.setCoordinateField(coordinate_field)
    lines.setSubgroupField(textureBlockGroup)
    
    contour = scene.createGraphicsContours()
    contour.setCoordinateField(coordinate_field)
    contour.setIsoscalarField(x_field)
    contour.setListIsovalues(128.5)
    contour.setMaterial(foot)
    contour.setTextureCoordinateField(coordinate_field)
    contour.setSubgroupField(textureBlockGroup)

    contour = scene.createGraphicsContours()
    contour.setCoordinateField(coordinate_field)
    contour.setIsoscalarField(y_field)
    contour.setListIsovalues(185.5)
    contour.setMaterial(foot)
    contour.setTextureCoordinateField(coordinate_field)
    contour.setSubgroupField(textureBlockGroup)
    
    tessellation_module = scene.getTessellationmodule()
    tessellation = tessellation_module.createTessellation()
    tessellation.setName("iso_tessellation")
    tessellation.setMinimumDivisions([16])
    
    offset1 = field_module.createFieldConstant([-0.9, -0.75, -0.6])
    non_bone = field_module.createFieldAdd(rescaledImage, offset1)
    mag_non_bone = field_module.createFieldMagnitude(non_bone)
    mag_non_bone.setName("mag_non_bone")
    mag_non_bone.setManaged(True)
    contour = scene.createGraphicsContours()
    contour.setCoordinateField(coordinate_field)
    contour.setIsoscalarField(mag_non_bone)
    contour.setListIsovalues(0.2)
    contour.setMaterial(bone)
    contour.setTextureCoordinateField(coordinate_field)
    contour.setSubgroupField(isoBlockGroup)
    contour.setTessellation(tessellation)
    contour.setVisibilityFlag(False)
    
    offset2 = field_module.createFieldConstant([-0.35, -0.12, -0.12])
    non_muscle = field_module.createFieldAdd(rescaledImage, offset2)
    mag_non_muscle = field_module.createFieldMagnitude(non_muscle)
    mag_non_muscle.setName("mag_non_muscle")
    mag_non_muscle.setManaged(True)
    contour = scene.createGraphicsContours()
    contour.setCoordinateField(coordinate_field)
    contour.setIsoscalarField(mag_non_muscle)
    contour.setListIsovalues(0.2)
    contour.setMaterial(muscle)
    contour.setTextureCoordinateField(coordinate_field)
    contour.setSubgroupField(isoBlockGroup)
    contour.setTessellation(tessellation)
    contour.setVisibilityFlag(True)
    
    rescaledImage1 = field_module.createFieldComponent(rescaledImage, 1)
    rescaledImage2 = field_module.createFieldComponent(rescaledImage, 2)
    rescaledImage3 = field_module.createFieldComponent(rescaledImage, 3)
    negative = field_module.createFieldConstant([-1.0])
    negativeRescaledImage1 = field_module.createFieldMultiply(rescaledImage1, negative)
    negativeRescaledImage2 = field_module.createFieldMultiply(rescaledImage2, negative)
    sumfield1 = field_module.createFieldAdd(negativeRescaledImage1, negativeRescaledImage2)
    bluefield = field_module.createFieldAdd(sumfield1, rescaledImage3)
    bluefield.setName("blue")
    bluefield.setManaged(True)
    contour = scene.createGraphicsContours()
    contour.setCoordinateField(coordinate_field)
    contour.setIsoscalarField(bluefield)
    contour.setListIsovalues(-0.25)
    contour.setMaterial(skin)
    contour.setTextureCoordinateField(coordinate_field)
    contour.setSubgroupField(isoBlockGroup)
    contour.setTessellation(tessellation)
    contour.setVisibilityFlag(True)
    
    scene.endChange()

    return True
