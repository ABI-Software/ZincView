"""
Example ZincView model loading script.

Must implement loadModel() function which must return True on success.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from opencmiss.zinc.element import Element
from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.region import Region
from opencmiss.zinc.status import OK as ZINC_OK
#from opencmiss.zinc.streamregion import StreaminformationRegion

def getDefaultCoordinateField(fieldmodule):
    '''
    Get the first coordinate field in the region
    '''
    fielditer = fieldmodule.createFielditerator()
    field = fielditer.next()
    while field.isValid():
        if field.isTypeCoordinate() and (field.getValueType() == Field.VALUE_TYPE_REAL) and \
                (field.getNumberOfComponents() <= 3) and field.castFiniteElement().isValid():
            return field
        field = fielditer.next()
    return None

def loadModel(region):
    '''
    This function must be implemented and return True on success to be
    a valid ZincView script
    '''
    result = region.readFile('heart.exfile')
    if result != ZINC_OK:
        return False
    scene = region.getScene()
    scene.beginChange()
    scene.removeAllGraphics()
    fieldmodule = region.getFieldmodule()

    fieldmodule.beginChange()
    coordinates = getDefaultCoordinateField(fieldmodule)
    bob = fieldmodule.createFieldStringConstant("bob")
    bob.setName("bob")
    bob.setManaged(True)
    for i in range(1, coordinates.getNumberOfComponents() + 1):
        component = fieldmodule.createFieldComponent(coordinates, i)
        component.setName(coordinates.getComponentName(i))
        component.setManaged(True)
    rc_coordinates = fieldmodule.createFieldCoordinateTransformation(coordinates)
    rc_coordinates.setCoordinateSystemType(Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN)
    direction = fieldmodule.createFieldConstant([0.8, 0.4, 0.1])
    slice = fieldmodule.createFieldDotProduct(rc_coordinates, direction)
    slice.setName("slice")
    slice.setManaged(True)
    fieldmodule.endChange()

    lines = scene.createGraphicsLines()
    lines.setName("lines")
    lines.setCoordinateField(coordinates)
    surfaces = scene.createGraphicsSurfaces()
    surfaces.setName("surfaces")
    surfaces.setCoordinateField(coordinates)
    surfaces.setExterior(True)
    surfaces.setElementFaceType(Element.FACE_TYPE_XI3_0)
    muscle = scene.getMaterialmodule().findMaterialByName('muscle')
    surfaces.setMaterial(muscle)
    node_points = scene.createGraphicsPoints()
    node_points.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
    node_points.setName("node_points")
    node_points.setCoordinateField(coordinates)
    attributes = node_points.getGraphicspointattributes()
    attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
    attributes.setBaseSize([2.0])
    gold = scene.getMaterialmodule().findMaterialByName('gold')
    node_points.setMaterial(gold)
    scene.endChange()
    return True
