#!/usr/bin/python
"""
ZincView example visualisation application using OpenCMISS-Zinc, python, Qt (PySide)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
import sys
import json
from PySide import QtGui, QtCore
from zincview_ui import Ui_ZincView
from opencmiss.zinc.context import Context as ZincContext
from opencmiss.zinc.scenecoordinatesystem import *
from opencmiss.zinc.result import RESULT_OK
from opencmiss.zinc.field import Field

def ZincRegion_getMeshSize(region, dimension):
    '''
    Get the number of elements of given dimension in the region and all its child regions.
    :return meshSize
    '''
    fieldmodule = region.getFieldmodule()
    mesh = fieldmodule.findMeshByDimension(dimension)
    meshSize = mesh.getSize()
    # recurse children
    child = region.getFirstChild()
    while child.isValid():
        meshSize = meshSize + ZincRegion_getMeshSize(child, dimension)
        child = child.getNextSibling()
    return meshSize

def ZincRegion_getTimeRange(region):
    '''
    Recursively get the time range of finite element field parameters in region, or any child regions
    :return minimum, maximum or None, None if no range
    '''
    minimum = None
    maximum = None
    # it's not easy to get the range of time; assume all nodes have same
    # time range, and use timesequence from first node field with one.
    # One problem is that often the last time represents the start of an
    # increment, so the new range should be higher, which matters if animating
    fieldmodule = region.getFieldmodule()
    for fieldDomainType in [Field.DOMAIN_TYPE_NODES, Field.DOMAIN_TYPE_DATAPOINTS]:
        nodeset = fieldmodule.findNodesetByFieldDomainType(fieldDomainType)
        nodeiter = nodeset.createNodeiterator()
        node = nodeiter.next()
        if node.isValid:
            fielditer = fieldmodule.createFielditerator()
            field = fielditer.next()
            while field.isValid():
                feField = field.castFiniteElement()
                if feField.isValid():
                    nodetemplate = nodeset.createNodetemplate()
                    nodetemplate.defineFieldFromNode(feField, node)
                    timesequence = nodetemplate.getTimesequence(feField)
                    if timesequence.isValid():
                        count = timesequence.getNumberOfTimes()
                        if count > 0:
                            thisMinimum = timesequence.getTime(1)
                            thisMaximum = timesequence.getTime(count)
                            if minimum is None:
                                minimum = thisMinimum
                                maximum = thisMaximum
                            elif thisMinimum < minimum:
                                minimum = thisMinimum
                            elif thisMaximum > maximum:
                                maximum = thisMaximum
                field = fielditer.next()
    # recurse children
    child = region.getFirstChild()
    while child.isValid():
        thisMinimum, thisMaximum = ZincRegion_getTimeRange(child)
        if thisMinimum is not None:
            if minimum is None:
                minimum = thisMinimum
                maximum = thisMaximum
            elif thisMinimum < minimum:
                minimum = thisMinimum
            elif thisMaximum > maximum:
                maximum = thisMaximum
        child = child.getNextSibling()
    return minimum, maximum

class ZincView(QtGui.QMainWindow):
    '''
    Create a subclass of QMainWindow to get menu bar functionality.
    '''
    
    def __init__(self, parent=None):
        '''
        Initiaise the ZincView first calling the QWidget __init__ function.
        '''
        QtGui.QMainWindow.__init__(self, parent)

        self._context = ZincContext("ZincView")
        self._rootRegion = self._context.createRegion()
        # set up standard materials and glyphs so we can use them elsewhere
        materialmodule = self._context.getMaterialmodule()
        materialmodule.defineStandardMaterials()
        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()
        
        # Using composition to include the visual element of the GUI.
        self.ui = Ui_ZincView()
        self.ui.setupUi(self)
        self.ui.toolBox.setCurrentIndex(0)
        self.ui.sceneviewerwidget.setContext(self._context)
        self.ui.sceneviewerwidget.graphicsInitialized.connect(self._graphicsInitialized)
        self.setWindowIcon(QtGui.QIcon(":/cmiss_icon.ico"))

    def _graphicsInitialized(self):
        '''
        Callback for when SceneviewerWidget is initialised
        Set up additional sceneviewer notifiers for updating widgets
        '''
        sceneviewer = self.ui.sceneviewerwidget.getSceneviewer()
        sceneviewer.setScene(self._rootRegion.getScene())
        self.ui.sceneviewerwidget.setSelectModeAll()
        self.ui.sceneviewer_editor_widget.setSceneviewer(sceneviewer)
        self.allSettingsUpdate()

    def modelClear(self):
        '''
        Clear all subregions, meshes, nodesets, fields and graphics
        '''
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle("ZincView")
        msgBox.setText("Clear will destroy the model and all graphics.")
        msgBox.setInformativeText("Proceed?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QtGui.QMessageBox.Cancel:
            return
        self._rootRegion = self._context.createRegion()
        self.ui.region_chooser.setRootRegion(self._rootRegion)
        scene = self._rootRegion.getScene()
        self.ui.scene_editor.setScene(scene)
        self.ui.sceneviewerwidget.getSceneviewer().setScene(scene)
        self.allSettingsUpdate()

    def modelLoad(self):
        '''
        Read model file or run script to read or define model.
        '''
        fileNameTuple = QtGui.QFileDialog.getOpenFileName(self, "Load ZincView Model", "", "ZincView scripts (*.zincview.py);;Model Files (*.ex* *.fieldml)")
        inputScriptFileName = fileNameTuple[0]
        fileFilter = fileNameTuple[1]
        if not inputScriptFileName:
            return
        #print("reading file " + inputScriptFileName + ", filter " + fileFilter)
        # set current directory to path from file, to support scripts and fieldml with external resources
        path = os.path.dirname(inputScriptFileName)
        os.chdir(path)
        if "scripts" in fileFilter:
            try:
                # f = open(inputScriptFileName, 'r')
                # myfunctions = {}
                # exec f in myfunctions
                # success = myfunctions['loadModel'](self._rootRegion)
                sys.path.append(path)
                _, filename = os.path.split(inputScriptFileName)
                mod_name, _ = os.path.splitext(filename)
                import importlib.util
                spec = importlib.util.spec_from_file_location(mod_name, inputScriptFileName)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

                success = foo.loadModel(self._rootRegion)
            except:
                success = False
        else:
            result = self._rootRegion.readFile(inputScriptFileName)
            success = (result == RESULT_OK)
        if not success:
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle("ZincView")
            msgBox.setText("Error reading file: " + inputScriptFileName)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
            result = msgBox.exec_()
            return
        scene = self._rootRegion.getScene()
        # ensure scene editor graphics list is redisplayed, and widgets are updated
        self.ui.scene_editor.setScene(scene)
        self.ui.region_chooser.setRootRegion(self._rootRegion)
        self.allSettingsUpdate()
        self.viewAll()

    def toolBoxPageChanged(self, page):
        # enable view widget updates only when looking at them
        self.ui.sceneviewer_editor_widget.setEnableUpdates(page == 2)

    def _displayReal(self, widget, value):
        '''
        Display real value in a widget
        '''
        newText = '{:.5g}'.format(value)
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

    def allSettingsUpdate(self):
        '''
        Show initial values on widgets
        '''
        self.tessellationMinimumDivisionsDisplay()
        self.tessellationRefinementFactorsDisplay()
        self.tessellationCircleDivisionsDisplay()
        self.spectrumMinimumDisplay()
        self.spectrumMaximumDisplay()
        self.timeMinimumDisplay()
        self.timeMaximumDisplay()
        self.timeTextDisplay()
        self.timeSliderDisplay()

    def regionChanged(self, int):
        region = self.ui.region_chooser.getRegion()
        self.ui.scene_editor.setScene(region.getScene())

    def viewAll(self):
        '''
        Change sceneviewer to see all of scene.
        '''
        self.ui.sceneviewer_editor_widget.viewAll()

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

        meshSize3d = ZincRegion_getMeshSize(self._rootRegion, 3)
        limit3d = limit
        if limit3d < meshSize3d:
            limit3d = meshSize3d
        overLimit3d = totalSize3d*meshSize3d > limit3d

        meshSize2d = ZincRegion_getMeshSize(self._rootRegion, 2)
        limit2d = limit
        if limit2d < meshSize2d:
            limit2d = meshSize2d
        overLimit2d = totalSize2d*meshSize2d > limit2d
        
        meshSize1d = ZincRegion_getMeshSize(self._rootRegion, 1)
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
        tessellationmodule = self._context.getTessellationmodule()
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
            tessellationmodule = self._context.getTessellationmodule()
            tessellation = tessellationmodule.getDefaultTessellation()
            result, oldMinimumDivisions = tessellation.getMinimumDivisions(3)
            if minimumDivisions != oldMinimumDivisions:
                result, refinementFactors = tessellation.getRefinementFactors(3)
                if self._checkTessellationDivisions(minimumDivisions, refinementFactors, self.ui.tessellation_minimum_divisions_lineedit):
                    if RESULT_OK != tessellation.setMinimumDivisions(minimumDivisions):
                        raise
        except:
            print("Invalid tessellation minimum divisions")
        #self.tessellationMinimumDivisionsDisplay()

    def tessellationRefinementFactorsDisplay(self):
        '''
        Display the current tessellation refinement factors
        '''
        tessellationmodule = self._context.getTessellationmodule()
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
            tessellationmodule = self._context.getTessellationmodule()
            tessellation = tessellationmodule.getDefaultTessellation()
            result, oldRefinementFactors = tessellation.getRefinementFactors(3)
            if refinementFactors != oldRefinementFactors:
                result, minimumDivisions = tessellation.getMinimumDivisions(3)
                if self._checkTessellationDivisions(minimumDivisions, refinementFactors, self.ui.tessellation_refinement_factors_lineedit):
                    if RESULT_OK != tessellation.setRefinementFactors(refinementFactors):
                        raise
        except:
            print("Invalid tessellation refinement factors")
        #self.tessellationRefinementFactorsDisplay()

    def tessellationCircleDivisionsDisplay(self):
        '''
        Display the current tessellation circle divisions
        '''
        tessellationmodule = self._context.getTessellationmodule()
        tessellation = tessellationmodule.getDefaultTessellation()
        circleDivisions = tessellation.getCircleDivisions()
        self.ui.tessellation_circle_divisions_lineedit.setText(str(circleDivisions))

    def tessellationCircleDivisionsEntered(self):
        '''
        Set tessellation circle divisions from values in widget 
        '''
        try:
            circleDivisions = int(self.ui.tessellation_circle_divisions_lineedit.text())
            tessellationmodule = self._context.getTessellationmodule()
            # set circle divisions for all tessellation in module
            result = RESULT_OK
            tessellationmodule.beginChange()
            iter = tessellationmodule.createTessellationiterator()
            tessellation = iter.next()
            while tessellation.isValid():
                result = tessellation.setCircleDivisions(circleDivisions)
                if RESULT_OK != result:
                    break # can't raise here otherwise no call to endChange()
                tessellation = iter.next()
            tessellationmodule.endChange()
            if RESULT_OK != result:
                raise
        except:
            print("Invalid tessellation circle divisions")
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
        if result >= 1: # result is number of components with range, can exceed 1
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
            if RESULT_OK != spectrumcomponent.setRangeMinimum(minimum):
                raise
        except:
            print("Invalid spectrum minimum")
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
            if RESULT_OK != spectrumcomponent.setRangeMaximum(maximum):
                raise
        except:
            print("Invalid spectrum maximum")
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
        # ensure scene editor graphics list is redisplayed
        self.ui.scene_editor.setScene(scene)

    def timeAutorangeClicked(self):
        '''
        Set time min/max to time range of finite element field parameters.
        '''
        minimum, maximum = ZincRegion_getTimeRange(self._rootRegion)
        if minimum is None:
            minimum = 0.0
            maximum = 0.0
        timekeepermodule = self._context.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        timekeeper.setMinimumTime(minimum)
        timekeeper.setMaximumTime(maximum)
        self.timeMinimumDisplay()
        self.timeMaximumDisplay()
        currentTime = timekeeper.getTime()
        if currentTime < minimum:
            timekeeper.setTime(minimum)
        elif currentTime > maximum:
            timekeeper.setTime(maximum)
        self.timeTextDisplay()
        self.timeSliderDisplay()

    def timeMinimumDisplay(self):
        '''
        Display the current default timekeeper minimum time
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        minimum = timekeeper.getMinimumTime()
        self._displayReal(self.ui.time_minimum_lineedit, minimum)

    def timeMinimumEntered(self):
        '''
        Set default timekeeper minimum time from value in the widget
        '''
        try:
            minimum = float(self.ui.time_minimum_lineedit.text())
            scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
            timekeepermodule = scene.getTimekeepermodule()
            timekeeper = timekeepermodule.getDefaultTimekeeper()
            if RESULT_OK != timekeeper.setMinimumTime(minimum):
                raise
        except:
            print("Invalid minimum time")
        self.timeMinimumDisplay()

    def timeMaximumDisplay(self):
        '''
        Display the current default timekeeper maximum time
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        maximum = timekeeper.getMaximumTime()
        self._displayReal(self.ui.time_maximum_lineedit, maximum)

    def timeMaximumEntered(self):
        '''
        Set default timekeeper maximum time from value in the widget
        '''
        try:
            maximum = float(self.ui.time_maximum_lineedit.text())
            scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
            timekeepermodule = scene.getTimekeepermodule()
            timekeeper = timekeepermodule.getDefaultTimekeeper()
            if RESULT_OK != timekeeper.setMaximumTime(maximum):
                raise
        except:
            print("Invalid maximum time")
        self.timeMaximumDisplay()

    def timeTextDisplay(self):
        '''
        Display the default timekeeper current time
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        time = timekeeper.getTime()
        self._displayReal(self.ui.time_text_lineedit, time)

    def timeTextEntered(self):
        '''
        Set default timekeeper current time from value in the widget
        '''
        try:
            time = float(self.ui.time_text_lineedit.text())
            scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
            timekeepermodule = scene.getTimekeepermodule()
            timekeeper = timekeepermodule.getDefaultTimekeeper()
            if RESULT_OK != timekeeper.setTime(time):
                raise
            self.timeSliderDisplay()
        except:
            print("Invalid current time")
        self.timeTextDisplay()

    def timeSliderDisplay(self):
        '''
        Display the default timekeeper current time on the time slider
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        minimum = timekeeper.getMinimumTime()
        maximum = timekeeper.getMaximumTime()
        time = timekeeper.getTime()
        # don't want signal for my change
        self.ui.time_slider.blockSignals(True)
        if maximum != minimum:
            value = int(time*(10000.999/(maximum - minimum)))
        else:
            value = 0
        self.ui.time_slider.setValue(value)
        self.ui.time_slider.blockSignals(False)

    def timeSliderChanged(self, value):
        '''
        Set near clipping plane distance from slider
        '''
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        minimum = timekeeper.getMinimumTime()
        maximum = timekeeper.getMaximumTime()
        if maximum != minimum:
            time = float(value)*((maximum - minimum)/10000.0)
        else:
            time = minimum
        timekeeper.setTime(time)
        self.timeTextDisplay()

    def saveImageClicked(self):
        '''
        Save the view in the window to an image file.
        '''
        fileNameTuple = QtGui.QFileDialog.getSaveFileName(self, "Save image", "", "Image files (*.jpg *.png *.tif *.*)")
        fileName = fileNameTuple[0]
        if not fileName:
            return
        image = self.ui.sceneviewerwidget.grabFrameBuffer()
        image.save(fileName)

    def exportSceneViewersettings(self, outputPrefix, numberOfResources):
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        si = scene.createStreaminformationScene()
        si.setIOFormat(si.IO_FORMAT_THREEJS)
        si.setIODataType(si.IO_FORMAT_THREEJS)
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        minimum = timekeeper.getMinimumTime()
        maximum = timekeeper.getMaximumTime()
        time_enabled = 0
        if (maximum - minimum) > 0.001:
            time_enabled = 1
        sv = self.ui.sceneviewerwidget.getSceneviewer()
        sv.viewAll()
        nearPlane = sv.getNearClippingPlane()
        farPlane = sv.getFarClippingPlane()
        result, eyePos, lookat, upVector = sv.getLookatParameters()
        obj = { "nearPlane": nearPlane, "farPlane": farPlane, "eyePosition": eyePos, "targetPosition": lookat, "upVector": upVector, "numberOfResources": numberOfResources, "timeEnabled" : time_enabled}
        outputName = outputPrefix + "_view.json"
        export_f = open(outputName, "wb+")
        export_f.write(json.dumps(obj))
        export_f.close()

    def exportScene(self, outputPrefix):
        scene = self.ui.sceneviewerwidget.getSceneviewer().getScene()
        si = scene.createStreaminformationScene()
        si.setIOFormat(si.IO_FORMAT_THREEJS)
        si.setIODataType(si.IO_FORMAT_THREEJS)
        timekeepermodule = scene.getTimekeepermodule()
        timekeeper = timekeepermodule.getDefaultTimekeeper()
        minimum = timekeeper.getMinimumTime()
        maximum = timekeeper.getMaximumTime()
        if (maximum - minimum) > 0.0:
            si.setInitialTime(minimum)
            si.setFinishTime(maximum)
            si.setNumberOfTimeSteps(51)
        number = si.getNumberOfResourcesRequired()
        i = 0
        srs =  []
        while i < number:
            outputName = outputPrefix + "_" + str(i + 1) + ".json"
            srs.append(si.createStreamresourceFile(outputName))
            i = i + 1
        scene.exportScene(si)
        return number
        
    def saveWebGLClicked(self):
        '''
        Save the view in the window to WebGL content.
        '''
        fileNameTuple = QtGui.QFileDialog.getSaveFileName(self, "Specify prefix", "")
        fileName = fileNameTuple[0]
        if not fileName:
            return
        #print("reading file", fileName, ", filter", fileFilter)
        # set current directory to path from file, to support scripts and fieldml with external resources
        # Not implemented
        numberOfResources = self.exportScene(fileName)
        self.exportSceneViewersettings(fileName, numberOfResources)


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
