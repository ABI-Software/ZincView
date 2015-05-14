#!/usr/bin/python
"""
ZincView example visualisation application using OpenCMISS-Zinc, python, Qt (PySide)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import math
import os
import sys
from PySide import QtGui, QtCore
from zincview_ui import Ui_ZincView
from opencmiss.zinc.context import Context as ZincContext
from opencmiss.zinc.scenecoordinatesystem import *
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.field import Field
from opencmiss.zinc.sceneviewer import Sceneviewer, Sceneviewerevent

class ZincView(QtGui.QMainWindow):
    '''
    Create a subclass of QMainWindow to get menu bar functionality.
    '''
    
    def __init__(self, parent=None):
        '''
        Initiaise the ZincView first calling the QWidget __init__ function.
        '''
        QtGui.QMainWindow.__init__(self, parent)

        self._context = ZincContext("ZincView");
        # set up standard materials and glyphs so we can use them elsewhere
        materialmodule = self._context.getMaterialmodule()
        materialmodule.defineStandardMaterials()
        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()
        
        # Using composition to include the visual element of the GUI.
        self.ui = Ui_ZincView()
        self.ui.setupUi(self)
        self.ui.sceneviewerwidget.setContext(self._context)
        self.ui.sceneviewerwidget.graphicsInitialized.connect(self._graphicsInitialized)
        self.setWindowIcon(QtGui.QIcon(":/cmiss_icon.ico"))
        self._maximumClippingDistance = 1

    def _graphicsInitialized(self):
        '''
        Callback for when SceneviewerWidget is initialised
        Set up additional sceneviewer notifiers for updating widgets
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        self.ui.sceneviewerwidget.setSelectModeAll()
        self._sceneviewernotifier = sceneviewer.createSceneviewernotifier()
        self._sceneviewernotifier.setCallback(self._sceneviewerChange)
        self._maximumClippingDistance = sceneviewer.getFarClippingPlane()
        # show initial values on widgets
        self.viewSettingsUpdate()
        self.backgroundColourDisplay()
        self.tessellationMinimumDivisionsDisplay()
        self.tessellationRefinementFactorsDisplay()
        self.tessellationCircleDivisionsDisplay()
        self.spectrumMinimumDisplay()
        self.spectrumMaximumDisplay()

    def _sceneviewerChange(self, event):
        '''
        Change to scene viewer; update view widgets if transformation changed
        '''
        changeFlags = event.getChangeFlags()
        if changeFlags & Sceneviewerevent.CHANGE_FLAG_TRANSFORM:
            self.viewSettingsUpdate()
 
    def modelClear(self):
        '''
        Clear all subregions, meshes, nodesets, fields and graphics
        '''
        # GRC could replace by adding Context.setDefaultRegion() method to Zinc API
        # or clear method
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("ZincView")
        msgBox.setText("Clear will destroy the model and all graphics.")
        msgBox.setInformativeText("Proceed?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QtGui.QMessageBox.Cancel:
            return
        region = self._context.getDefaultRegion()
        region.beginHierarchicalChange()
        child = region.getFirstChild()
        while child.isValid():
            region.removeChild(child)
            child = region.getFirstChild()
        fieldmodule = region.getFieldmodule()
        for dimension in [3, 2, 1]:
            mesh = fieldmodule.findMeshByDimension(dimension)
            mesh.destroyAllElements()
        nodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        nodeset.destroyAllNodes()
        nodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)
        nodeset.destroyAllNodes()
        iter = fieldmodule.createFielditerator()
        field = iter.next()
        while field.isValid():
            if field.isManaged():
                field.setManaged(False)
                # must reset iterator
                iter = fieldmodule.createFielditerator()
            field = iter.next()
        scene = region.getScene()
        scene.removeAllGraphics()
        self.ui.scene_editor.setScene(scene)
        region.endHierarchicalChange()
 
    def modelLoad(self):
        '''
        Read model file or run script to read or define model.
        '''
        fileNameTuple = QtGui.QFileDialog.getOpenFileName(self, "Load ZincView Model", "", "Model Files (*.ex* *.fieldml);;ZincView scripts (*.zincview.py)");
        fileName = fileNameTuple[0]
        fileFilter = fileNameTuple[1]
        if not fileName:
            return
        #print "reading file", fileName, ", filter", fileFilter
        # set current directory to path from file, to support scripts and fieldml with external resources
        path = os.path.dirname(fileName)
        os.chdir(path)
        region = self._context.getDefaultRegion()
        if "scripts" in fileFilter:
            try:
                f = open(fileName, 'r')
                myfunctions = {}
                exec f in myfunctions
                success = myfunctions['loadModel'](self._context.getDefaultRegion())
            except:
                success = False
        else:
            result = region.readFile(str(fileName))
            success = (result == ZINC_OK)
        if not success:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("ZincView")
            msgBox.setText("Error reading file: " + fileName)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
            result = msgBox.exec_()
            return
        self.viewAll()
        scene = region.getScene()
        self.ui.scene_editor.setScene(scene)
 
    def _displayReal(self, widget, value):
        '''
        Display real value in a widget
        '''
        newText = unicode('{:.5g}'.format(value))
        widget.setText(newText)
 
    def _displayScaleInteger(self, widget, values, numberFormat = '{:d}'):
        '''
        Display vector of integer values in a widget, separated by '*'
        '''
        newText = "*".join(numberFormat.format(value) for value in values)
        widget.setText(newText)

    def _parseScaleInteger(self, widget):
        '''
        Return integer vector from comma separated text in line edit widget
        '''
        text = widget.text()
        values = [int(value) for value in text.split('*')]
        if len(values) < 1:
            raise
        return values
 
    def _displayVector(self, widget, values, numberFormat = '{:.5g}'):
        '''
        Display real vector values in a widget
        '''
        newText = ", ".join(numberFormat.format(value) for value in values)
        widget.setText(newText)

    def _parseVector(self, widget):
        '''
        Return real vector from comma separated text in line edit widget
        '''
        text = widget.text()
        values = [float(value) for value in text.split(',')]
        if len(values) < 1:
            raise
        return values

    def viewAll(self):
        '''
        Change sceneviewer to see all of scene.
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        sceneviewer.viewAll()
        self._maximumClippingDistance = sceneviewer.getFarClippingPlane()
        self.viewSettingsUpdate()

    def viewSettingsUpdate(self):
        '''
        Show the current scene viewer settings on the view widgets
        '''
        self.viewAngleDisplay()
        self.eyePointDisplay()
        self.lookatPointDisplay()
        self.upVectorDisplay()
        self.nearClippingDisplay()
        self.farClippingDisplay()

    def perspectiveStateChanged(self, state):
        '''
        Set perspective/parallel projection
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        if (state):
            sceneviewer.setProjectionMode(Sceneviewer.PROJECTION_MODE_PERSPECTIVE)
        else:
            sceneviewer.setProjectionMode(Sceneviewer.PROJECTION_MODE_PARALLEL)

    def viewAngleDisplay(self):
        '''
        Display the current scene viewer diagonal view angle
        '''
        viewAngleRadians = self.ui.sceneviewerwidget.getSceneviewer().getViewAngle()
        viewAngleDegrees = viewAngleRadians*180.0/math.pi
        self._displayReal(self.ui.view_angle, viewAngleDegrees)

    def viewAngleEntered(self):
        '''
        Set scene viewer diagonal view angle from value in the view angle widget
        '''
        try:
            viewAngleRadians = float(self.ui.view_angle.text())*math.pi/180.0
            if ZINC_OK != self.ui.sceneviewerwidget.getSceneviewer().setViewAngle(viewAngleRadians):
                raise
        except:
            print "Invalid view angle"
        self.viewAngleDisplay()

    def setLookatParametersNonSkew(self):
        '''
        Set eye, lookat point and up vector simultaneous in non-skew projection
        '''
        eye = self._parseVector(self.ui.eye_point)
        lookat = self._parseVector(self.ui.lookat_point)
        up_vector = self._parseVector(self.ui.up_vector)
        if ZINC_OK != self.ui.sceneviewerwidget.getSceneviewer().setLookatParametersNonSkew(eye, lookat, up_vector):
            raise

    def eyePointDisplay(self):
        '''
        Display the current scene viewer eye point
        '''
        result, eye = self.ui.sceneviewerwidget.getSceneviewer().getEyePosition()
        self._displayVector(self.ui.eye_point, eye)

    def eyePointEntered(self):
        '''
        Set scene viewer wyw point from text in widget
        '''
        try:
            self.setLookatParametersNonSkew()
        except:
            print "Invalid eye point"
            self.eyePositionDisplay()

    def lookatPointDisplay(self):
        '''
        Display the current scene viewer lookat point
        '''
        result, lookat = self.ui.sceneviewerwidget.getSceneviewer().getLookatPosition()
        self._displayVector(self.ui.lookat_point, lookat)

    def lookatPointEntered(self):
        '''
        Set scene viewer lookat point from text in widget
        '''
        try:
            self.setLookatParametersNonSkew()
        except:
            print "Invalid lookat point"
            self.lookatPositionDisplay()

    def upVectorDisplay(self):
        '''
        Display the current scene viewer eye point
        '''
        result, up_vector = self.ui.sceneviewerwidget.getSceneviewer().getUpVector()
        self._displayVector(self.ui.up_vector, up_vector)

    def upVectorEntered(self):
        '''
        Set scene viewer up vector from text in widget
        '''
        try:
            self.setLookatParametersNonSkew()
        except:
            print "Invalid up vector"
            self.upVectorDisplay()

    def nearClippingDisplay(self):
        '''
        Display the current near clipping plane distance
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        near = sceneviewer.getNearClippingPlane()
        value = int(10001.0*near/self._maximumClippingDistance) - 1
        # don't want signal for my change
        self.ui.near_clipping_slider.blockSignals(True)
        self.ui.near_clipping_slider.setValue(value)
        self.ui.near_clipping_slider.blockSignals(False)

    def nearClippingChanged(self, value):
        '''
        Set near clipping plane distance from slider
        '''
        near = (value + 1)*self._maximumClippingDistance/10001.0
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        sceneviewer.setNearClippingPlane(near)

    def farClippingDisplay(self):
        '''
        Display the current far clipping plane distance
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        value = int(10001.0*sceneviewer.getFarClippingPlane()/self._maximumClippingDistance) - 1
        self.ui.far_clipping_slider.blockSignals(True)
        self.ui.far_clipping_slider.setValue(value)
        self.ui.far_clipping_slider.blockSignals(False)

    def farClippingChanged(self, value):
        '''
        Set far clipping plane distance from slider
        '''
        far = (value + 1)*self._maximumClippingDistance/10001.0
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        sceneviewer.setFarClippingPlane(far)

    def backgroundColourDisplay(self):
        '''
        Display the current scene viewer eye point
        '''
        result, colourRGB = self.ui.sceneviewerwidget.getSceneviewer().getBackgroundColourRGB()
        self._displayVector(self.ui.background_colour, colourRGB)

    def backgroundColourEntered(self):
        '''
        Set scene viewer diagonal view angle from value in the view angle widget
        '''
        try:
            colourRGB = self._parseVector(self.ui.background_colour)
            sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
            if ZINC_OK != sceneviewer.setBackgroundColourRGB(colourRGB):
                raise
        except:
            print "Invalid background colour"
        self.backgroundColourDisplay()

    def _checkTessellationDivisions(self, minimumDivisions, refinementFactors, widget):
        '''
        Check total divisions not too high or get user confirmation
        Call with both of the vectors set, each must have at least one component.
        Returns True if can apply.
        '''
        limit = 100000 # max elements*totalsize for each dimension

        min = 1
        ref = 1
        totalDivisions = [1,1,1]
        totalSize3d = 1
        for i in range(3):
            if i < len(minimumDivisions):
                min = minimumDivisions[i]
            if i < len(refinementFactors):
                ref = refinementFactors[i]
            totalDivisions[i] = min*ref
            totalSize3d = totalSize3d*min*ref
        totalSize2d = totalDivisions[0]*totalDivisions[1]
        if totalDivisions[1]*totalDivisions[2] > totalSize2d:
            totalSize2d = totalDivisions[1]*totalDivisions[2]
        if totalDivisions[2]*totalDivisions[0] > totalSize2d:
            totalSize2d = totalDivisions[2]*totalDivisions[0]
        totalSize1d = totalDivisions[0]
        if totalDivisions[1] > totalSize1d:
            totalSize1d = totalDivisions[1]
        if totalDivisions[2] > totalSize1d:
            totalSize1d = totalDivisions[2]

        fieldmodule = self._context.getDefaultRegion().getFieldmodule()

        meshSize3d = fieldmodule.findMeshByDimension(3).getSize()
        limit3d = limit
        if limit3d < meshSize3d:
            limit3d = meshSize3d
        overLimit3d = totalSize3d*meshSize3d > limit3d

        meshSize2d = fieldmodule.findMeshByDimension(2).getSize()
        limit2d = limit
        if limit2d < meshSize2d:
            limit2d = meshSize2d
        overLimit2d = totalSize2d*meshSize2d > limit2d
        
        meshSize1d = fieldmodule.findMeshByDimension(1).getSize()
        limit1d = limit
        if limit1d < meshSize1d:
            limit1d = meshSize1d
        overLimit1d = totalSize1d*meshSize1d > limit1d

        if not (overLimit1d or overLimit2d or overLimit3d):
            return True
        widget.blockSignals(True)
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("ZincView")
        divisionsText = "*".join('{:d}'.format(value) for value in totalDivisions)
        msgBox.setText("Fine tessellation divisions " + divisionsText + " can take a long time to apply.")
        msgBox.setInformativeText("Please confirm action.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Apply | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        result = msgBox.exec_()
        widget.blockSignals(False)
        return result == QtGui.QMessageBox.Apply

    def tessellationMinimumDivisionsDisplay(self):
        '''
        Display the current tessellation minimum divisions
        '''
        scene = self._context.getDefaultRegion().getScene()
        tessellationmodule = scene.getTessellationmodule()
        tessellation = tessellationmodule.getDefaultTessellation()
        result, minimumDivisions = tessellation.getMinimumDivisions(3)
        self._displayScaleInteger(self.ui.tessellation_minimum_divisions_lineedit, minimumDivisions)

    def tessellationMinimumDivisionsEntered(self):
        '''
        Set default tessellation minimum divisions from values in widget 
        '''
        try:
            minimumDivisions = self._parseScaleInteger(self.ui.tessellation_minimum_divisions_lineedit)
            # pack to length 3 for comparing with old values
            while len(minimumDivisions) < 3:
                minimumDivisions.append(minimumDivisions[-1])
            scene = self._context.getDefaultRegion().getScene()
            tessellationmodule = scene.getTessellationmodule()
            tessellation = tessellationmodule.getDefaultTessellation()
            result, oldMinimumDivisions = tessellation.getMinimumDivisions(3)
            if minimumDivisions != oldMinimumDivisions:
                result, refinementFactors = tessellation.getRefinementFactors(3)
                if self._checkTessellationDivisions(minimumDivisions, refinementFactors, self.ui.tessellation_minimum_divisions_lineedit):
                    if ZINC_OK != tessellation.setMinimumDivisions(minimumDivisions):
                        raise
        except:
            print "Invalid tessellation minimum divisions"
        #self.tessellationMinimumDivisionsDisplay()

    def tessellationRefinementFactorsDisplay(self):
        '''
        Display the current tessellation refinement factors
        '''
        scene = self._context.getDefaultRegion().getScene()
        tessellationmodule = scene.getTessellationmodule()
        tessellation = tessellationmodule.getDefaultTessellation()
        result, refinementFactors = tessellation.getRefinementFactors(3)
        self._displayScaleInteger(self.ui.tessellation_refinement_factors_lineedit, refinementFactors)

    def tessellationRefinementFactorsEntered(self):
        '''
        Set default tessellation refinement factors from values in widget 
        '''
        try:
            refinementFactors = self._parseScaleInteger(self.ui.tessellation_refinement_factors_lineedit)
            # pack to length 3 for comparing with old values
            while len(refinementFactors) < 3:
                refinementFactors.append(refinementFactors[-1])
            scene = self._context.getDefaultRegion().getScene()
            tessellationmodule = scene.getTessellationmodule()
            tessellation = tessellationmodule.getDefaultTessellation()
            result, oldRefinementFactors = tessellation.getRefinementFactors(3)
            if refinementFactors != oldRefinementFactors:
                result, minimumDivisions = tessellation.getMinimumDivisions(3)
                if self._checkTessellationDivisions(minimumDivisions, refinementFactors, self.ui.tessellation_refinement_factors_lineedit):
                    if ZINC_OK != tessellation.setRefinementFactors(refinementFactors):
                        raise
        except:
            print "Invalid tessellation refinement factors"
        #self.tessellationRefinementFactorsDisplay()

    def tessellationCircleDivisionsDisplay(self):
        '''
        Display the current tessellation circle divisions
        '''
        scene = self._context.getDefaultRegion().getScene()
        tessellationmodule = scene.getTessellationmodule()
        tessellation = tessellationmodule.getDefaultTessellation()
        circleDivisions = tessellation.getCircleDivisions()
        self.ui.tessellation_circle_divisions_lineedit.setText(unicode(circleDivisions))

    def tessellationCircleDivisionsEntered(self):
        '''
        Set tessellation circle divisions from values in widget 
        '''
        try:
            circleDivisions = int(self.ui.tessellation_circle_divisions_lineedit.text())
            scene = self._context.getDefaultRegion().getScene()
            tessellationmodule = scene.getTessellationmodule()
            # set circle divisions for all tessellation in module
            result = ZINC_OK
            tessellationmodule.beginChange()
            iter = tessellationmodule.createTessellationiterator()
            tessellation = iter.next()
            while tessellation.isValid():
                result = tessellation.setCircleDivisions(circleDivisions);
                if ZINC_OK != result:
                    break # can't raise here otherwise no call to endChange()
                tessellation = iter.next()
            tessellationmodule.endChange()
            if ZINC_OK != result:
                raise
        except:
            print "Invalid tessellation circle divisions"
        #self.tessellationCircleDivisionsDisplay()

    def perturbLinesStateChanged(self, state):
        '''
        Set perturb lines flag from checkbox
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        sceneviewer.setPerturbLinesFlag(state)

    def spectrumAutorangeClicked(self):
        '''
        Set spectrum min/max to fit range of visible data in scene graphics.
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        scene = sceneviewer.getScene()
        filter = sceneviewer.getScenefilter()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        result, minimum, maximum = scene.getSpectrumDataRange(filter, spectrum, 1)
        if result == ZINC_OK:
            spectrummodule.beginChange()
            spectrumcomponent = spectrum.getFirstSpectrumcomponent()
            spectrumcomponent.setRangeMinimum(minimum)
            spectrumcomponent.setRangeMaximum(maximum)
            spectrummodule.endChange()
            self.spectrumMinimumDisplay()
            self.spectrumMaximumDisplay()

    def spectrumMinimumDisplay(self):
        '''
        Display the current default spectrum minimum
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        spectrumcomponent = spectrum.getFirstSpectrumcomponent()
        minimum = spectrumcomponent.getRangeMinimum()
        self._displayReal(self.ui.spectrum_minimum_lineedit, minimum)

    def spectrumMinimumEntered(self):
        '''
        Set default spectrum minimum from value in the widget
        '''
        try:
            minimum = float(self.ui.spectrum_minimum_lineedit.text())
            scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
            spectrummodule = scene.getSpectrummodule()
            spectrum = spectrummodule.getDefaultSpectrum()
            spectrumcomponent = spectrum.getFirstSpectrumcomponent()
            if ZINC_OK != spectrumcomponent.setRangeMinimum(minimum):
                raise
        except:
            print "Invalid spectrum minimum"
        self.spectrumMinimumDisplay()

    def spectrumMaximumDisplay(self):
        '''
        Display the current default spectrum maximum
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        spectrumcomponent = spectrum.getFirstSpectrumcomponent()
        maximum = spectrumcomponent.getRangeMaximum()
        self._displayReal(self.ui.spectrum_maximum_lineedit, maximum)

    def spectrumMaximumEntered(self):
        '''
        Set default spectrum maximum from value in the widget
        '''
        try:
            maximum = float(self.ui.spectrum_maximum_lineedit.text())
            scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
            spectrummodule = scene.getSpectrummodule()
            spectrum = spectrummodule.getDefaultSpectrum()
            spectrumcomponent = spectrum.getFirstSpectrumcomponent()
            if ZINC_OK != spectrumcomponent.setRangeMaximum(maximum):
                raise
        except:
            print "Invalid spectrum maximum"
        self.spectrumMaximumDisplay()

    def spectrumAddColourBarClicked(self):
        '''
        Add an overlay graphics showing the default spectrum colour bar.
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        scene = sceneviewer.getScene()
        scene.beginChange()
        spectrummodule = scene.getSpectrummodule()
        spectrum = spectrummodule.getDefaultSpectrum()
        glyphmodule = scene.getGlyphmodule()
        glyphmodule.beginChange()
        colourbar = glyphmodule.findGlyphByName("colourbar")
        if not colourbar.isValid():
            colourbar = glyphmodule.createGlyphColourBar(spectrum)
            colourbar.setName("colourbar")
        glyphmodule.endChange()
        graphics = scene.findGraphicsByName("colourbar")
        if graphics.isValid():
            scene.removeGraphics(graphics)
        graphics = scene.createGraphicsPoints()
        graphics.setName("colourbar")
        graphics.setScenecoordinatesystem(SCENECOORDINATESYSTEM_NORMALISED_WINDOW_FIT_LEFT)
        pointattributes = graphics.getGraphicspointattributes()
        pointattributes.setGlyph(colourbar)
        pointattributes.setBaseSize([1.0,1.0,1.0])
        pointattributes.setGlyphOffset([-0.9,0.0,0.0])
        scene.endChange()
        self.ui.scene_editor.setScene(scene)

# main start
def main(argv):
    '''
    The entry point for the application, handle application arguments and initialise the 
    GUI.
    '''
    
    app = QtGui.QApplication(argv)

    w = ZincView()
    w.show()

    sys.exit(app.exec_())
# main end

if __name__ == '__main__':
    main(sys.argv)
