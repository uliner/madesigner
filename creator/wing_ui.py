#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Wing Panel tab

author: Curtis L. Olson
website: madesigner.flightgear.org
started: November 2013
"""

import os.path
import sys
from PyQt4 import QtGui, QtCore
#import xml.etree.ElementTree as ET
import lxml.etree as ET
from combobox_nowheel import QComboBoxNoWheel

from leading_edge_ui import LeadingEdgeUI
from trailing_edge_ui import TrailingEdgeUI
from spar_ui import SparUI
from sheet_ui import SheetUI
from simple_hole_ui import SimpleHoleUI
from shaped_hole_ui import ShapedHoleUI
from build_tab_ui import BuildTabUI
from flap_ui import FlapUI


class WingUI():
    def __init__(self, changefunc, name="New"):
        self.valid = True
        self.changefunc = changefunc
        self.container = self.make_page(name=name)
        self.xml = None
        self.wing_link = "none"
        self.leading_edges = []
        self.trailing_edges = []
        self.spars = []
        self.stringers = []
        self.sheeting = []
        self.simple_holes = []
        self.shaped_holes = []
        self.build_tabs = []
        self.flaps = []

    def onChange(self):
        self.changefunc()

    def rebuildStations(self):
        self.changefunc()
        # rebuild stations when station list has changed
        for le in self.leading_edges:
            if le.valid:
                le.rebuild_stations(self.edit_stations.text())
        for te in self.trailing_edges:
            if te.valid:
                te.rebuild_stations(self.edit_stations.text())
        for spar in self.spars:
            if spar.valid:
                spar.rebuild_stations(self.edit_stations.text())
        for stringer in self.stringers:
            if stringer.valid:
                stringer.rebuild_stations(self.edit_stations.text())
        for sheet in self.sheeting:
            if sheet.valid:
                sheet.rebuild_stations(self.edit_stations.text())
        for hole in self.simple_holes:
            if hole.valid:
                hole.rebuild_stations(self.edit_stations.text())
        for hole in self.shaped_holes:
            if hole.valid:
                hole.rebuild_stations(self.edit_stations.text())
        for tab in self.build_tabs:
            if tab.valid:
                tab.rebuild_stations(self.edit_stations.text())
        for flap in self.flaps:
            if flap.valid:
                flap.rebuild_stations(self.edit_stations.text())

    def rebuild_wing_list(self, wing_list=[]):
        myname = self.get_name()
        wing_link_text = self.edit_wing_link.currentText()
        print "wing_link_text = " + str(wing_link_text)
        if wing_link_text == None or wing_link_text == "none":
            if self.wing_link != "":
                print "Connecting up with saved name: " + self.wing_link
                wing_link_text = self.wing_link
        self.edit_wing_link.clear()
        self.edit_wing_link.addItem("none")
        for index,wing in enumerate(wing_list):
            if ( wing != myname ):
                self.edit_wing_link.addItem(wing)
        index = self.edit_wing_link.findText(wing_link_text)
        if index != None:
            self.edit_wing_link.setCurrentIndex(index)
        else:
            self.edit_wing_link.setCurrentIndex(0)

    def select_airfoil_root(self):
        basepath = os.path.split(os.path.abspath(sys.argv[0]))[0]
        airfoil_path = basepath + "/data/airfoils/"
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open File",
                                                     airfoil_path,
                                                     "Airfoil (*.dat)")
        if ( filename == "" ):
            return
        basename = os.path.basename(str(filename))
        fileroot, ext = os.path.splitext(basename)
        self.edit_airfoil_root.setText(fileroot)

    def select_airfoil_tip(self):
        basepath = os.path.split(os.path.abspath(sys.argv[0]))[0]
        airfoil_path = basepath + "/data/airfoils/"
        filename = QtGui.QFileDialog.getOpenFileName(None, "Open File",
                                                     airfoil_path,
                                                     "Airfoil (*.dat)")
        if ( filename == "" ):
            return
        basename = os.path.basename(str(filename))
        fileroot, ext = os.path.splitext(basename)
        self.edit_airfoil_tip.setText(fileroot)

    def generate_stations(self):
        text, ok = QtGui.QInputDialog.getText(None, 'Input Dialog', 
            'Enter number of stations (ribs):')
        
        if ok:
            span = float(self.edit_span.text())
            num = int(text)
            spacing = span / float(num)
            stations = ""
            pos = 0.0
            for i in range(num):
                #print str(i) + " " + str(pos)
                stations += ("%.2f" % pos).rstrip('0').rstrip('.') + " "
                pos += spacing
            stations += ("%.2f" % span).rstrip('0').rstrip('.')
            self.edit_stations.setText(stations)                

    def add_leading_edge(self, xml_node=None):
        leading_edge = LeadingEdgeUI(self.changefunc)
        leading_edge.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            leading_edge.parse_xml(xml_node)
        self.leading_edges.append(leading_edge)
        self.layout_le.addWidget( leading_edge.get_widget() )
        self.changefunc()

    def add_trailing_edge(self, xml_node=None):
        trailing_edge = TrailingEdgeUI(self.changefunc)
        trailing_edge.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            trailing_edge.parse_xml(xml_node)
        self.trailing_edges.append(trailing_edge)
        self.layout_te.addWidget( trailing_edge.get_widget() )
        self.changefunc()

    def add_spar(self, xml_node=None):
        spar = SparUI(self.changefunc)
        spar.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            spar.parse_xml(xml_node)
        self.spars.append(spar)
        self.layout_spars.addWidget( spar.get_widget() )
        self.changefunc()

    def add_stringer(self, xml_node=None):
        stringer = SparUI(self.changefunc)
        stringer.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            stringer.parse_xml(xml_node)
        self.stringers.append(stringer)
        self.layout_stringers.addWidget( stringer.get_widget() )
        self.changefunc()

    def add_sheet(self, xml_node=None):
        sheet = SheetUI(self.changefunc)
        sheet.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            sheet.parse_xml(xml_node)
        self.sheeting.append(sheet)
        self.layout_sheeting.addWidget( sheet.get_widget() )
        self.changefunc()

    def add_simple_hole(self, xml_node=None):
        hole = SimpleHoleUI(self.changefunc)
        hole.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            hole.parse_xml(xml_node)
        self.simple_holes.append(hole)
        self.layout_simple_holes.addWidget( hole.get_widget() )
        self.changefunc()

    def add_shaped_hole(self, xml_node=None):
        hole = ShapedHoleUI(self.changefunc)
        hole.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            hole.parse_xml(xml_node)
        self.shaped_holes.append(hole)
        self.layout_shaped_holes.addWidget( hole.get_widget() )
        self.changefunc()

    def add_build_tab(self, xml_node=None):
        tab = BuildTabUI(self.changefunc)
        tab.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            tab.parse_xml(xml_node)
        self.build_tabs.append(tab)
        self.layout_build_tabs.addWidget( tab.get_widget() )
        self.changefunc()

    def add_flap(self, xml_node=None):
        flap = FlapUI(self.changefunc)
        flap.rebuild_stations(self.edit_stations.text())
        if xml_node != None:
            flap.parse_xml(xml_node)
        self.flaps.append(flap)
        self.layout_flaps.addWidget( flap.get_widget() )
        self.changefunc()

    def delete_self(self):
        if self.valid:
            self.changefunc()
            self.container.deleteLater()
            self.valid = False

    def make_page(self, name):
        # make the full edit widget
        toppage = QtGui.QFrame()
        toplayout = QtGui.QVBoxLayout()
        toppage.setLayout(toplayout)

        page = QtGui.QFrame()
        layout = QtGui.QVBoxLayout()
        page.setLayout(layout)

        maincontents = QtGui.QFrame()
        formlayout = QtGui.QFormLayout()
        maincontents.setLayout( formlayout )
        layout.addWidget(maincontents)

        scroll = QtGui.QScrollArea()
        scroll.setWidget(page)
        scroll.setWidgetResizable(True)
        #layout.addWidget(scroll)
        toplayout.addWidget(scroll)

        frame = QtGui.QGroupBox("Leading Edges")
        self.layout_le = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_le)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Trailing Edges")
        self.layout_te = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_te)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Spars")
        self.layout_spars = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_spars)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Stringers")
        self.layout_stringers = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_stringers)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Sheeting")
        self.layout_sheeting = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_sheeting)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Simple Holes")
        self.layout_simple_holes = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_simple_holes)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Shaped Holes")
        self.layout_shaped_holes = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_shaped_holes)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Build Tabs")
        self.layout_build_tabs = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_build_tabs)
        layout.addWidget(frame)

        frame = QtGui.QGroupBox("Control Surfaces")
        self.layout_flaps = QtGui.QVBoxLayout()
        frame.setLayout(self.layout_flaps)
        layout.addWidget(frame)

        # 'Command' button bar
        cmd_group = QtGui.QFrame()
        toplayout.addWidget(cmd_group)
        cmd_layout = QtGui.QHBoxLayout()
        cmd_group.setLayout( cmd_layout )

        cmd_layout.addWidget( QtGui.QLabel("<b>Wing Tools:</b> ") )

        select_airfoil = QtGui.QPushButton("Assist Me ...")
        menu = QtGui.QMenu()
        menu.addAction("Select Root Airfoil", self.select_airfoil_root)
        menu.addAction("Select Tip Airfoil", self.select_airfoil_tip)
        menu.addAction("Generate Stations", self.generate_stations)
        select_airfoil.setMenu(menu)
        cmd_layout.addWidget(select_airfoil)

        add_feature = QtGui.QPushButton("Add Feature ...")
        menu = QtGui.QMenu()
        menu.addAction("Leading Edge", self.add_leading_edge)
        menu.addAction("Trailing Edge", self.add_trailing_edge)
        menu.addAction("Spar", self.add_spar)
        menu.addAction("Stringer", self.add_stringer)
        menu.addAction("Sheeting", self.add_sheet)
        menu.addAction("Lighting/Spar Hole", self.add_simple_hole)
        menu.addAction("Shaped Hole", self.add_shaped_hole)
        menu.addAction("Build Tab", self.add_build_tab)
        menu.addAction("Add Control Surface", self.add_flap)
        add_feature.setMenu(menu)
        cmd_layout.addWidget(add_feature)

        cmd_layout.addStretch(1)

        delete = QtGui.QPushButton('Delete Wing')
        delete.clicked.connect(self.delete_self)
        cmd_layout.addWidget(delete)

        # form content
        self.edit_name = QtGui.QLineEdit()
        self.edit_name.setFixedWidth(250)
        self.edit_name.textChanged.connect(self.onChange)
        self.edit_name.setText(name)
        self.edit_airfoil_root = QtGui.QLineEdit()
        self.edit_airfoil_root.setFixedWidth(250)
        self.edit_airfoil_root.textChanged.connect(self.onChange)
        self.edit_airfoil_tip = QtGui.QLineEdit()
        self.edit_airfoil_tip.setFixedWidth(250)
        self.edit_airfoil_tip.textChanged.connect(self.onChange)
        self.edit_span = QtGui.QLineEdit()
        self.edit_span.setFixedWidth(250)
        self.edit_span.textChanged.connect(self.onChange)
        self.edit_chord_root = QtGui.QLineEdit()
        self.edit_chord_root.setFixedWidth(250)
        self.edit_chord_root.textChanged.connect(self.onChange)
        self.edit_chord_tip = QtGui.QLineEdit()
        self.edit_chord_tip.setFixedWidth(250)
        self.edit_chord_tip.textChanged.connect(self.onChange)
        self.edit_chord_curve = QtGui.QLineEdit()
        self.edit_chord_curve.setFixedWidth(250)
        self.edit_chord_curve.textChanged.connect(self.onChange)
        self.edit_twist = QtGui.QLineEdit()
        self.edit_twist.setFixedWidth(250)
        self.edit_twist.textChanged.connect(self.onChange)
        self.edit_sweep = QtGui.QLineEdit()
        self.edit_sweep.setFixedWidth(250)
        self.edit_sweep.textChanged.connect(self.onChange)
        self.edit_sweep_curve = QtGui.QLineEdit()
        self.edit_sweep_curve.setFixedWidth(250)
        self.edit_sweep_curve.textChanged.connect(self.onChange)
        self.edit_dihedral = QtGui.QLineEdit()
        self.edit_dihedral.setFixedWidth(250)
        self.edit_dihedral.textChanged.connect(self.onChange)
        self.edit_stations = QtGui.QLineEdit()
        self.edit_stations.setFixedWidth(250)
        self.edit_stations.textChanged.connect(self.rebuildStations)
        self.edit_wing_link = QComboBoxNoWheel()
        self.edit_wing_link.setFixedWidth(250)
        self.edit_wing_link.currentIndexChanged.connect(self.onChange)
        self.edit_wing_link.addItem("none")

        formlayout.addRow( "<b>Wing Name:</b>", self.edit_name )
        formlayout.addRow( "<b>Root Airfoil:</b>", self.edit_airfoil_root )
        formlayout.addRow( "<b>Tip Airfoil (if different):</b>", self.edit_airfoil_tip )
        formlayout.addRow( "<b>Span:</b>", self.edit_span )
        formlayout.addRow( "<b>Root Chord:</b>", self.edit_chord_root )
        formlayout.addRow( "<b>Tip Chord (if different):</b>", self.edit_chord_tip )
        formlayout.addRow( "<b>Chord Curve (see docs):</b>", self.edit_chord_curve )
        formlayout.addRow( "<b>Twist/Washout (deg):</b>", self.edit_twist )
        formlayout.addRow( "<b>Sweep Angle (deg):</b>", self.edit_sweep )
        formlayout.addRow( "<b>Sweep Curve (see docs):</b>", self.edit_sweep_curve )
        formlayout.addRow( "<b>Dihedral (deg):</b>", self.edit_dihedral )
        formlayout.addRow( "<b>Stations:</b>", self.edit_stations )
        formlayout.addRow( "<b>Link to Wing:</b>", self.edit_wing_link )

        return toppage

    def get_widget(self):
        return self.container

    def get_name(self):
        return self.edit_name.text()

    def get_value(self, node):
        e = self.xml.find(node)
        if e != None and e.text != None:
            return e.text
        else:
            return ""

    def parse_xml(self, node):
        self.xml = node
        self.edit_name.setText(self.get_value('name'))
        self.edit_airfoil_root.setText(self.get_value('airfoil-root'))
        self.edit_airfoil_tip.setText(self.get_value('airfoil-tip'))
        self.edit_span.setText(self.get_value('span'))
        chord_root = self.get_value('chord-root')
        chord_tip = self.get_value('chord-tip')
        self.edit_chord_root.setText(chord_root)
        if ( chord_tip != chord_root ):
            self.edit_chord_tip.setText(chord_tip)
        self.edit_chord_curve.setText(self.get_value('chord-curve'))
        self.edit_twist.setText(self.get_value('twist'))
        self.edit_sweep.setText(self.get_value('sweep'))
        self.edit_sweep_curve.setText(self.get_value('sweep-curve'))
        self.edit_dihedral.setText(self.get_value('dihedral'))
        self.edit_stations.setText(self.get_value('stations'))
        self.wing_link = self.get_value('wing-link')

        for le_node in node.findall('leading-edge'):
            self.add_leading_edge(le_node)
        for te_node in node.findall('trailing-edge'):
            self.add_trailing_edge(te_node)
        for spar_node in node.findall('spar'):
            self.add_spar(spar_node)
        for stringer_node in node.findall('stringer'):
            self.add_stringer(stringer_node)
        for sheet_node in node.findall('sheet'):
            self.add_sheet(sheet_node)
        for hole_node in node.findall('simple-hole'):
            self.add_simple_hole(hole_node)
        for hole_node in node.findall('shaped-hole'):
            self.add_shaped_hole(hole_node)
        for tab_node in node.findall('build-tab'):
            self.add_build_tab(tab_node)
        for flap_node in node.findall('flap'):
            self.add_flap(flap_node)

    def update_node(self, node, value):
        e = self.xml.find(node)
        if e == None:
            e = ET.SubElement(self.xml, node)
        e.text = str(value)
        
    def gen_xml(self, node):
        self.xml = node
        self.update_node('name', self.edit_name.text())
        self.update_node('airfoil-root', self.edit_airfoil_root.text())
        self.update_node('airfoil-tip', self.edit_airfoil_tip.text())
        self.update_node('span', self.edit_span.text())
        self.update_node('chord-root', self.edit_chord_root.text())
        self.update_node('chord-tip', self.edit_chord_tip.text())
        self.update_node('chord-curve', self.edit_chord_curve.text())
        self.update_node('twist', self.edit_twist.text())
        self.update_node('sweep', self.edit_sweep.text())
        self.update_node('sweep-curve', self.edit_sweep_curve.text())
        self.update_node('dihedral', self.edit_dihedral.text())
        self.update_node('stations', self.edit_stations.text())
        self.update_node('wing-link', self.edit_wing_link.currentText())

        for le in self.leading_edges:
            if le.valid:
                subnode = ET.SubElement(node, 'leading-edge')
                le.gen_xml(subnode)
        for te in self.trailing_edges:
            if te.valid:
                subnode = ET.SubElement(node, 'trailing-edge')
                te.gen_xml(subnode)
        for spar in self.spars:
            if spar.valid:
                subnode = ET.SubElement(node, 'spar')
                spar.gen_xml(subnode)
        for stringer in self.stringers:
            if stringer.valid:
                subnode = ET.SubElement(node, 'stringer')
                stringer.gen_xml(subnode)
        for sheet in self.sheeting:
            if sheet.valid:
                subnode = ET.SubElement(node, 'sheet')
                sheet.gen_xml(subnode)
        for hole in self.simple_holes:
            if hole.valid:
                subnode = ET.SubElement(node, 'simple-hole')
                hole.gen_xml(subnode)
        for hole in self.shaped_holes:
            if hole.valid:
                subnode = ET.SubElement(node, 'shaped-hole')
                hole.gen_xml(subnode)
        for tab in self.build_tabs:
            if tab.valid:
                subnode = ET.SubElement(node, 'build-tab')
                tab.gen_xml(subnode)
        for flap in self.flaps:
            if flap.valid:
                subnode = ET.SubElement(node, 'flap')
                flap.gen_xml(subnode)


