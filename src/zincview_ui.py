# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zincview.ui'
#
# Created: Thu May 14 19:47:28 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ZincView(object):
    def setupUi(self, ZincView):
        ZincView.setObjectName("ZincView")
        ZincView.resize(900, 635)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ZincView.sizePolicy().hasHeightForWidth())
        ZincView.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cmiss_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ZincView.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(ZincView)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.sceneviewerwidget = SceneviewerWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sceneviewerwidget.sizePolicy().hasHeightForWidth())
        self.sceneviewerwidget.setSizePolicy(sizePolicy)
        self.sceneviewerwidget.setObjectName("sceneviewerwidget")
        self.gridLayout.addWidget(self.sceneviewerwidget, 0, 0, 1, 1)
        ZincView.setCentralWidget(self.centralwidget)
        self.dockWidget = QtGui.QDockWidget(ZincView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy)
        self.dockWidget.setMinimumSize(QtCore.QSize(230, 113))
        self.dockWidget.setStyleSheet("QToolBox::tab {\n"
"         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                     stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"         border-radius: 5px;\n"
"         color: black;\n"
"     }\n"
"\n"
"     QToolBox::tab:selected { /* italicize selected tabs */\n"
"         font: bold;\n"
"         color: black;\n"
"     }\n"
"QToolBox {\n"
"    padding : 0\n"
"}")
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 228, 607))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolBox = QtGui.QToolBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBox.setAccessibleName("")
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtGui.QFrame.Plain)
        self.toolBox.setObjectName("toolBox")
        self.model = QtGui.QWidget()
        self.model.setGeometry(QtCore.QRect(0, 0, 228, 482))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.model.sizePolicy().hasHeightForWidth())
        self.model.setSizePolicy(sizePolicy)
        self.model.setAccessibleName("")
        self.model.setObjectName("model")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.model)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.model_clear_button = QtGui.QPushButton(self.model)
        self.model_clear_button.setObjectName("model_clear_button")
        self.verticalLayout_4.addWidget(self.model_clear_button)
        self.model_load_button = QtGui.QPushButton(self.model)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.model_load_button.sizePolicy().hasHeightForWidth())
        self.model_load_button.setSizePolicy(sizePolicy)
        self.model_load_button.setObjectName("model_load_button")
        self.verticalLayout_4.addWidget(self.model_load_button)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.toolBox.addItem(self.model, "")
        self.graphics = QtGui.QWidget()
        self.graphics.setGeometry(QtCore.QRect(0, 0, 228, 482))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics.sizePolicy().hasHeightForWidth())
        self.graphics.setSizePolicy(sizePolicy)
        self.graphics.setObjectName("graphics")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.graphics)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scene_editor = SceneEditorWidget(self.graphics)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_editor.sizePolicy().hasHeightForWidth())
        self.scene_editor.setSizePolicy(sizePolicy)
        self.scene_editor.setObjectName("scene_editor")
        self.verticalLayout_3.addWidget(self.scene_editor)
        self.toolBox.addItem(self.graphics, "")
        self.view = QtGui.QWidget()
        self.view.setGeometry(QtCore.QRect(0, 0, 228, 482))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setObjectName("view")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.view)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.view_all_button = QtGui.QPushButton(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_all_button.sizePolicy().hasHeightForWidth())
        self.view_all_button.setSizePolicy(sizePolicy)
        self.view_all_button.setObjectName("view_all_button")
        self.verticalLayout_5.addWidget(self.view_all_button)
        self.perspective_checkbox = QtGui.QCheckBox(self.view)
        self.perspective_checkbox.setChecked(True)
        self.perspective_checkbox.setObjectName("perspective_checkbox")
        self.verticalLayout_5.addWidget(self.perspective_checkbox)
        self.view_angle_label = QtGui.QLabel(self.view)
        self.view_angle_label.setObjectName("view_angle_label")
        self.verticalLayout_5.addWidget(self.view_angle_label)
        self.view_angle = QtGui.QLineEdit(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_angle.sizePolicy().hasHeightForWidth())
        self.view_angle.setSizePolicy(sizePolicy)
        self.view_angle.setObjectName("view_angle")
        self.verticalLayout_5.addWidget(self.view_angle)
        self.eye_point_label = QtGui.QLabel(self.view)
        self.eye_point_label.setObjectName("eye_point_label")
        self.verticalLayout_5.addWidget(self.eye_point_label)
        self.eye_point = QtGui.QLineEdit(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eye_point.sizePolicy().hasHeightForWidth())
        self.eye_point.setSizePolicy(sizePolicy)
        self.eye_point.setObjectName("eye_point")
        self.verticalLayout_5.addWidget(self.eye_point)
        self.lookat_point_label = QtGui.QLabel(self.view)
        self.lookat_point_label.setObjectName("lookat_point_label")
        self.verticalLayout_5.addWidget(self.lookat_point_label)
        self.lookat_point = QtGui.QLineEdit(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lookat_point.sizePolicy().hasHeightForWidth())
        self.lookat_point.setSizePolicy(sizePolicy)
        self.lookat_point.setObjectName("lookat_point")
        self.verticalLayout_5.addWidget(self.lookat_point)
        self.up_vector_label = QtGui.QLabel(self.view)
        self.up_vector_label.setObjectName("up_vector_label")
        self.verticalLayout_5.addWidget(self.up_vector_label)
        self.up_vector = QtGui.QLineEdit(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.up_vector.sizePolicy().hasHeightForWidth())
        self.up_vector.setSizePolicy(sizePolicy)
        self.up_vector.setObjectName("up_vector")
        self.verticalLayout_5.addWidget(self.up_vector)
        self.clipping_planes_groupbox = QtGui.QGroupBox(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clipping_planes_groupbox.sizePolicy().hasHeightForWidth())
        self.clipping_planes_groupbox.setSizePolicy(sizePolicy)
        self.clipping_planes_groupbox.setMinimumSize(QtCore.QSize(0, 0))
        self.clipping_planes_groupbox.setObjectName("clipping_planes_groupbox")
        self.formLayout = QtGui.QFormLayout(self.clipping_planes_groupbox)
        self.formLayout.setObjectName("formLayout")
        self.near_clipping_label = QtGui.QLabel(self.clipping_planes_groupbox)
        self.near_clipping_label.setObjectName("near_clipping_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.near_clipping_label)
        self.far_clipping_label = QtGui.QLabel(self.clipping_planes_groupbox)
        self.far_clipping_label.setObjectName("far_clipping_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.far_clipping_label)
        self.near_clipping_slider = QtGui.QSlider(self.clipping_planes_groupbox)
        self.near_clipping_slider.setMaximum(10000)
        self.near_clipping_slider.setPageStep(100)
        self.near_clipping_slider.setTracking(True)
        self.near_clipping_slider.setOrientation(QtCore.Qt.Horizontal)
        self.near_clipping_slider.setObjectName("near_clipping_slider")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.near_clipping_slider)
        self.far_clipping_slider = QtGui.QSlider(self.clipping_planes_groupbox)
        self.far_clipping_slider.setMaximum(10000)
        self.far_clipping_slider.setPageStep(100)
        self.far_clipping_slider.setOrientation(QtCore.Qt.Horizontal)
        self.far_clipping_slider.setObjectName("far_clipping_slider")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.far_clipping_slider)
        self.verticalLayout_5.addWidget(self.clipping_planes_groupbox)
        self.background_colour_label = QtGui.QLabel(self.view)
        self.background_colour_label.setObjectName("background_colour_label")
        self.verticalLayout_5.addWidget(self.background_colour_label)
        self.background_colour = QtGui.QLineEdit(self.view)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.background_colour.sizePolicy().hasHeightForWidth())
        self.background_colour.setSizePolicy(sizePolicy)
        self.background_colour.setObjectName("background_colour")
        self.verticalLayout_5.addWidget(self.background_colour)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.toolBox.addItem(self.view, "")
        self.rendering = QtGui.QWidget()
        self.rendering.setGeometry(QtCore.QRect(0, 0, 228, 482))
        self.rendering.setObjectName("rendering")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.rendering)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tessellation_groupbox = QtGui.QGroupBox(self.rendering)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tessellation_groupbox.sizePolicy().hasHeightForWidth())
        self.tessellation_groupbox.setSizePolicy(sizePolicy)
        self.tessellation_groupbox.setObjectName("tessellation_groupbox")
        self.formLayout_2 = QtGui.QFormLayout(self.tessellation_groupbox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tessellation_minimum_divisions_label = QtGui.QLabel(self.tessellation_groupbox)
        self.tessellation_minimum_divisions_label.setObjectName("tessellation_minimum_divisions_label")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.tessellation_minimum_divisions_label)
        self.tessellation_minimum_divisions_lineedit = QtGui.QLineEdit(self.tessellation_groupbox)
        self.tessellation_minimum_divisions_lineedit.setObjectName("tessellation_minimum_divisions_lineedit")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.tessellation_minimum_divisions_lineedit)
        self.tessellation_refinement_factors_label = QtGui.QLabel(self.tessellation_groupbox)
        self.tessellation_refinement_factors_label.setObjectName("tessellation_refinement_factors_label")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.tessellation_refinement_factors_label)
        self.tessellation_refinement_factors_lineedit = QtGui.QLineEdit(self.tessellation_groupbox)
        self.tessellation_refinement_factors_lineedit.setObjectName("tessellation_refinement_factors_lineedit")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.tessellation_refinement_factors_lineedit)
        self.tessellation_circle_divisions_label = QtGui.QLabel(self.tessellation_groupbox)
        self.tessellation_circle_divisions_label.setObjectName("tessellation_circle_divisions_label")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.tessellation_circle_divisions_label)
        self.tessellation_circle_divisions_lineedit = QtGui.QLineEdit(self.tessellation_groupbox)
        self.tessellation_circle_divisions_lineedit.setObjectName("tessellation_circle_divisions_lineedit")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.tessellation_circle_divisions_lineedit)
        self.verticalLayout_7.addWidget(self.tessellation_groupbox)
        self.perturb_lines_checkbox = QtGui.QCheckBox(self.rendering)
        self.perturb_lines_checkbox.setObjectName("perturb_lines_checkbox")
        self.verticalLayout_7.addWidget(self.perturb_lines_checkbox)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.toolBox.addItem(self.rendering, "")
        self.data_colouring = QtGui.QWidget()
        self.data_colouring.setObjectName("data_colouring")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.data_colouring)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spectrum_autorange_button = QtGui.QPushButton(self.data_colouring)
        self.spectrum_autorange_button.setObjectName("spectrum_autorange_button")
        self.verticalLayout_6.addWidget(self.spectrum_autorange_button)
        self.frame = QtGui.QFrame(self.data_colouring)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout_3 = QtGui.QFormLayout(self.frame)
        self.formLayout_3.setObjectName("formLayout_3")
        self.spectrum_minimum_label = QtGui.QLabel(self.frame)
        self.spectrum_minimum_label.setObjectName("spectrum_minimum_label")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.spectrum_minimum_label)
        self.spectrum_minimum_lineedit = QtGui.QLineEdit(self.frame)
        self.spectrum_minimum_lineedit.setObjectName("spectrum_minimum_lineedit")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.spectrum_minimum_lineedit)
        self.spectrum_maximum_lineedit = QtGui.QLineEdit(self.frame)
        self.spectrum_maximum_lineedit.setObjectName("spectrum_maximum_lineedit")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.spectrum_maximum_lineedit)
        self.spectrum_maximum_label = QtGui.QLabel(self.frame)
        self.spectrum_maximum_label.setObjectName("spectrum_maximum_label")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.spectrum_maximum_label)
        self.verticalLayout_6.addWidget(self.frame)
        self.spectrum_add_colour_bar_button = QtGui.QPushButton(self.data_colouring)
        self.spectrum_add_colour_bar_button.setObjectName("spectrum_add_colour_bar_button")
        self.verticalLayout_6.addWidget(self.spectrum_add_colour_bar_button)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem3)
        self.toolBox.addItem(self.data_colouring, "")
        self.verticalLayout_2.addWidget(self.toolBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.dockWidget.setWidget(self.dockWidgetContents)
        ZincView.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionOpen = QtGui.QAction(ZincView)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtGui.QAction(ZincView)
        self.actionQuit.setObjectName("actionQuit")
        self.actionView_All = QtGui.QAction(ZincView)
        self.actionView_All.setObjectName("actionView_All")

        self.retranslateUi(ZincView)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(1)
        QtCore.QObject.connect(self.view_angle, QtCore.SIGNAL("editingFinished()"), ZincView.viewAngleEntered)
        QtCore.QObject.connect(self.model_load_button, QtCore.SIGNAL("clicked()"), ZincView.modelLoad)
        QtCore.QObject.connect(self.view_all_button, QtCore.SIGNAL("clicked()"), ZincView.viewAll)
        QtCore.QObject.connect(self.eye_point, QtCore.SIGNAL("editingFinished()"), ZincView.eyePointEntered)
        QtCore.QObject.connect(self.lookat_point, QtCore.SIGNAL("editingFinished()"), ZincView.lookatPointEntered)
        QtCore.QObject.connect(self.up_vector, QtCore.SIGNAL("editingFinished()"), ZincView.upVectorEntered)
        QtCore.QObject.connect(self.perspective_checkbox, QtCore.SIGNAL("clicked(bool)"), ZincView.perspectiveStateChanged)
        QtCore.QObject.connect(self.near_clipping_slider, QtCore.SIGNAL("valueChanged(int)"), ZincView.nearClippingChanged)
        QtCore.QObject.connect(self.far_clipping_slider, QtCore.SIGNAL("valueChanged(int)"), ZincView.farClippingChanged)
        QtCore.QObject.connect(self.background_colour, QtCore.SIGNAL("editingFinished()"), ZincView.backgroundColourEntered)
        QtCore.QObject.connect(self.tessellation_minimum_divisions_lineedit, QtCore.SIGNAL("returnPressed()"), ZincView.tessellationMinimumDivisionsEntered)
        QtCore.QObject.connect(self.tessellation_refinement_factors_lineedit, QtCore.SIGNAL("returnPressed()"), ZincView.tessellationRefinementFactorsEntered)
        QtCore.QObject.connect(self.tessellation_circle_divisions_lineedit, QtCore.SIGNAL("returnPressed()"), ZincView.tessellationCircleDivisionsEntered)
        QtCore.QObject.connect(self.tessellation_minimum_divisions_lineedit, QtCore.SIGNAL("editingFinished()"), ZincView.tessellationMinimumDivisionsDisplay)
        QtCore.QObject.connect(self.tessellation_circle_divisions_lineedit, QtCore.SIGNAL("editingFinished()"), ZincView.tessellationCircleDivisionsDisplay)
        QtCore.QObject.connect(self.tessellation_refinement_factors_lineedit, QtCore.SIGNAL("editingFinished()"), ZincView.tessellationRefinementFactorsDisplay)
        QtCore.QObject.connect(self.perturb_lines_checkbox, QtCore.SIGNAL("clicked(bool)"), ZincView.perturbLinesStateChanged)
        QtCore.QObject.connect(self.model_clear_button, QtCore.SIGNAL("clicked()"), ZincView.modelClear)
        QtCore.QObject.connect(self.spectrum_autorange_button, QtCore.SIGNAL("clicked()"), ZincView.spectrumAutorangeClicked)
        QtCore.QObject.connect(self.spectrum_minimum_lineedit, QtCore.SIGNAL("editingFinished()"), ZincView.spectrumMinimumEntered)
        QtCore.QObject.connect(self.spectrum_maximum_lineedit, QtCore.SIGNAL("editingFinished()"), ZincView.spectrumMaximumEntered)
        QtCore.QObject.connect(self.spectrum_add_colour_bar_button, QtCore.SIGNAL("clicked()"), ZincView.spectrumAddColourBarClicked)
        QtCore.QMetaObject.connectSlotsByName(ZincView)

    def retranslateUi(self, ZincView):
        ZincView.setWindowTitle(QtGui.QApplication.translate("ZincView", "ZincView", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("ZincView", "ZincView Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.model_clear_button.setText(QtGui.QApplication.translate("ZincView", "Clear model...", None, QtGui.QApplication.UnicodeUTF8))
        self.model_load_button.setText(QtGui.QApplication.translate("ZincView", "Load model...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.model), QtGui.QApplication.translate("ZincView", "Model", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.graphics), QtGui.QApplication.translate("ZincView", "Graphics", None, QtGui.QApplication.UnicodeUTF8))
        self.view_all_button.setText(QtGui.QApplication.translate("ZincView", "View All", None, QtGui.QApplication.UnicodeUTF8))
        self.perspective_checkbox.setText(QtGui.QApplication.translate("ZincView", "Perspective projection", None, QtGui.QApplication.UnicodeUTF8))
        self.view_angle_label.setText(QtGui.QApplication.translate("ZincView", "View angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.eye_point_label.setText(QtGui.QApplication.translate("ZincView", "Eye point:", None, QtGui.QApplication.UnicodeUTF8))
        self.lookat_point_label.setText(QtGui.QApplication.translate("ZincView", "Look at point:", None, QtGui.QApplication.UnicodeUTF8))
        self.up_vector_label.setText(QtGui.QApplication.translate("ZincView", "Up vector:", None, QtGui.QApplication.UnicodeUTF8))
        self.clipping_planes_groupbox.setTitle(QtGui.QApplication.translate("ZincView", "Clipping planes:", None, QtGui.QApplication.UnicodeUTF8))
        self.near_clipping_label.setText(QtGui.QApplication.translate("ZincView", "Near:", None, QtGui.QApplication.UnicodeUTF8))
        self.far_clipping_label.setText(QtGui.QApplication.translate("ZincView", "Far:", None, QtGui.QApplication.UnicodeUTF8))
        self.background_colour_label.setText(QtGui.QApplication.translate("ZincView", "Background colour R, G, B:", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.view), QtGui.QApplication.translate("ZincView", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.tessellation_groupbox.setTitle(QtGui.QApplication.translate("ZincView", "Tessellation divisions:", None, QtGui.QApplication.UnicodeUTF8))
        self.tessellation_minimum_divisions_label.setText(QtGui.QApplication.translate("ZincView", "Minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.tessellation_refinement_factors_label.setText(QtGui.QApplication.translate("ZincView", "Refinement:", None, QtGui.QApplication.UnicodeUTF8))
        self.tessellation_circle_divisions_label.setText(QtGui.QApplication.translate("ZincView", "Circle:", None, QtGui.QApplication.UnicodeUTF8))
        self.perturb_lines_checkbox.setText(QtGui.QApplication.translate("ZincView", "Perturb lines", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.rendering), QtGui.QApplication.translate("ZincView", "Rendering", None, QtGui.QApplication.UnicodeUTF8))
        self.spectrum_autorange_button.setText(QtGui.QApplication.translate("ZincView", "Autorange spectrum", None, QtGui.QApplication.UnicodeUTF8))
        self.spectrum_minimum_label.setText(QtGui.QApplication.translate("ZincView", "Minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.spectrum_maximum_label.setText(QtGui.QApplication.translate("ZincView", "Maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.spectrum_add_colour_bar_button.setText(QtGui.QApplication.translate("ZincView", "Add colour bar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.data_colouring), QtGui.QApplication.translate("ZincView", "Data Colouring", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("ZincView", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("ZincView", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_All.setText(QtGui.QApplication.translate("ZincView", "View All", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget
from opencmiss.zincwidgets.sceneeditorwidget import SceneEditorWidget
