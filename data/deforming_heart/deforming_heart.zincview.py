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
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.streamregion import StreaminformationRegion
from opencmiss.zinc.spectrum import Spectrumcomponent

def loadModel(region):
    '''
    Read time-varying deforming heart model.
    Define strains fields and make some graphics to visualise them.
    '''
    sir = region.createStreaminformationRegion()
    sir.createStreamresourceFile("reference_heart.exnode")
    sir.createStreamresourceFile("reference_heart.exelem")
    for i in range(51):
        filename = 'heart{:0>4}.exnode'.format(i)
        fr = sir.createStreamresourceFile(filename)
        sir.setResourceAttributeReal(fr, StreaminformationRegion.ATTRIBUTE_TIME, i/50.0)
    sir.createStreamresourceFile("heart.exelem")
    result = region.read(sir)
    if result != ZINC_OK:
        print "failed to read"
        return False
    scene = region.getScene()
    timekeepermodule = scene.getTimekeepermodule()
    timekeeper = timekeepermodule.getDefaultTimekeeper()
    timekeeper.setMinimumTime(0.0)
    timekeeper.setMaximumTime(1.0)
    timekeeper.setTime(0.0)

    scene.beginChange()
    scene.removeAllGraphics()
    fieldmodule = region.getFieldmodule()
    coordinates = fieldmodule.findFieldByName("coordinates")
    reference_coordinates = fieldmodule.findFieldByName("reference_coordinates")
    fibres = fieldmodule.findFieldByName("fibres")

    lines = scene.createGraphicsLines()
    lines.setCoordinateField(coordinates)
    surfaces = scene.createGraphicsSurfaces()
    surfaces.setName("surfaces")
    surfaces.setCoordinateField(coordinates)
    surfaces.setExterior(True)
    surfaces.setElementFaceType(Element.FACE_TYPE_XI3_0)
    tissue = scene.getMaterialmodule().findMaterialByName('tissue')
    surfaces.setMaterial(tissue)

    principal_strain_direction = []
    principal_strain = []
    E = fieldmodule.findFieldByName("E")
    if E.isValid():
        for i in range(3):
            principal_strain.append(fieldmodule.findFieldByName("principal_strain{:}".format(i + 1)))
            principal_strain_direction.append(fieldmodule.findFieldByName("principal_strain{:}_direction".format(i + 1)))
    else:
        fieldmodule.beginChange()
        rc_reference_coordinates = fieldmodule.createFieldCoordinateTransformation(reference_coordinates)
        rc_coordinates = fieldmodule.createFieldCoordinateTransformation(coordinates)
        F = fieldmodule.createFieldGradient(rc_coordinates, rc_reference_coordinates)
        F_transpose = fieldmodule.createFieldTranspose(3, F)
        identity3 = fieldmodule.createFieldConstant([1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])
        C = fieldmodule.createFieldMatrixMultiply(3, F_transpose, F)
        E2 = C - identity3
        E = E2*fieldmodule.createFieldConstant(0.5)
        E.setName("E")
        E.setManaged(True)
        principal_strains = fieldmodule.createFieldEigenvalues(E)
        principal_strains.setName("principal_strains")
        principal_strains.setManaged(True)
        principal_strain_vectors = fieldmodule.createFieldEigenvectors(principal_strains)
        deformed_principal_strain_vectors = fieldmodule.createFieldMatrixMultiply(3, principal_strain_vectors, F_transpose)
        # should be easier than this to get several components:
        deformed_principal_strain_vector = [ \
            fieldmodule.createFieldMatrixMultiply(1, fieldmodule.createFieldConstant([1.0, 0.0, 0.0]), deformed_principal_strain_vectors), \
            fieldmodule.createFieldMatrixMultiply(1, fieldmodule.createFieldConstant([0.0, 1.0, 0.0]), deformed_principal_strain_vectors), \
            fieldmodule.createFieldMatrixMultiply(1, fieldmodule.createFieldConstant([0.0, 0.0, 1.0]), deformed_principal_strain_vectors) ]
        for i in range(3):
            direction = fieldmodule.createFieldNormalise(deformed_principal_strain_vector[i])
            direction.setName("principal_strain{:}_direction".format(i + 1))
            direction.setManaged(True)
            principal_strain_direction.append(direction)
            strain = fieldmodule.createFieldComponent(principal_strains, i + 1)
            strain.setName("principal_strain{:}".format(i + 1))
            strain.setManaged(True)
            principal_strain.append(strain)
        # Calculate the deformed fibre axes
        fibre_axes = fieldmodule.createFieldFibreAxes(fibres, rc_reference_coordinates)
        fibre_axes.setName("fibre_axes")
        fibre_axes.setManaged(True)
        deformed_fibre_axes = fieldmodule.createFieldMatrixMultiply(3, fibre_axes, F_transpose)
        deformed_fibre_axes.setName("deformed_fibre_axes")
        deformed_fibre_axes.setManaged(True)
        fieldmodule.endChange()

    spectrummodule = scene.getSpectrummodule()
    strainSpectrum = spectrummodule.findSpectrumByName("strain")
    if not strainSpectrum.isValid():
        spectrummodule.beginChange()
        strainSpectrum = spectrummodule.createSpectrum()
        strainSpectrum.setName("strain")
        strainSpectrum.setManaged(True)
        # red when negative
        spectrumComponent1 = strainSpectrum.createSpectrumcomponent()
        spectrumComponent1.setColourMappingType(Spectrumcomponent.COLOUR_MAPPING_TYPE_RED)
        spectrumComponent1.setRangeMinimum(-1.0)
        spectrumComponent1.setRangeMaximum(0.0)
        spectrumComponent1.setExtendAbove(False)
        spectrumComponent1.setColourMinimum(1.0)
        spectrumComponent1.setColourMaximum(1.0)
        # blue when positive
        spectrumComponent2 = strainSpectrum.createSpectrumcomponent()
        spectrumComponent2.setColourMappingType(Spectrumcomponent.COLOUR_MAPPING_TYPE_BLUE)
        spectrumComponent2.setRangeMinimum(0.0)
        spectrumComponent2.setRangeMaximum(1.0)
        spectrumComponent2.setExtendBelow(False)
        spectrumComponent2.setColourMinimum(1.0)
        spectrumComponent2.setColourMaximum(1.0)
        # this adds some green to the blue above so not too dark
        spectrumComponent3 = strainSpectrum.createSpectrumcomponent()
        spectrumComponent3.setColourMappingType(Spectrumcomponent.COLOUR_MAPPING_TYPE_GREEN)
        spectrumComponent3.setRangeMinimum(0.0)
        spectrumComponent3.setRangeMaximum(1.0)
        spectrumComponent3.setExtendBelow(False)
        spectrumComponent3.setColourMinimum(0.5)
        spectrumComponent3.setColourMaximum(0.5)
        spectrummodule.endChange()

    # visualise the strain vectors with mirrored glyphs
    for i in range(3):
        points = scene.createGraphicsPoints()
        points.setFieldDomainType(Field.DOMAIN_TYPE_MESH3D)
        points.setCoordinateField(coordinates)
        points.setDataField(principal_strain[i])
        points.setSpectrum(strainSpectrum)
        attr = points.getGraphicspointattributes()
        attr.setGlyphShapeType(Glyph.SHAPE_TYPE_CONE)
        attr.setGlyphRepeatMode(Glyph.REPEAT_MODE_MIRROR)
        attr.setBaseSize([0.0, 1.0, 1.0])
        attr.setOrientationScaleField(principal_strain_direction[i])
        attr.setSignedScaleField(principal_strain[i])
        attr.setScaleFactors([20.0, 0.0, 0.0])

    scene.endChange()
    return True
