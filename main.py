import sys
import math
import operator
import pickle


from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, qApp, QSizePolicy, QSlider
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIcon, QImage
from source import processing


class MainWindow(QMainWindow):
    MODE_NODE = '1'
    MODE_NODE_DEL = '2'
    MODE_EDGE = '3'
    MODE_DIRECTED_EDGE = '4'
    MODE_PATH = '5'
    MODE_TEXT = '6'
    MODE_EDGE_DEL = '7'
    MODE_LOAD = '8'
    MODE_COLOR_B = 'B'
    MODE_COLOR_G = 'G'
    MODE_COLOR_R = 'R'
    MODE_COLOR_Y = 'Y'



    MSG_MODE_NODE = 'Add and move Node mode'
    MSG_MODE_NODE_DEL = 'Delete Node mode'
    MSG_MODE_EDGE = 'Add Edge mode'
    MSG_MODE_DIRECTED_EDGE = 'Add directed Edge mode'
    MSG_MODE_PATH = 'Minimal Path mode'
    MSG_MODE_TEXT = 'Add name'
    MSG_MODE_LOAD = 'Load'
    MSG_MODE_EDGE_DEL = 'Delete Edge mode'
    MSG_MODE_COLOR_B = 'Change color blue'
    MSG_MODE_COLOR_G = 'Change color green'
    MSG_MODE_COLOR_R = 'Change color red'
    MSG_MODE_COLOR_Y = 'Change color yellow'




    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.mode = self.MODE_NODE

        self.setGeometry(150, 150, 1000, 1000)
        self.setWindowTitle('Draw a graph')

        self.canvas = processing.Canvas()
        self.setCentralWidget(self.canvas)

        exitAction = QAction(QIcon('images/save.png'), 'Save', self)
        exitAction.setShortcut('Ctrl+L')
        exitAction.triggered.connect(self.mode_save)

        insertNodeAction = QAction(QIcon('images/node.png'), 'Node', self)
        insertNodeAction.setShortcut('1')
        insertNodeAction.triggered.connect(self.nodeMode)

        addEdgeAction = QAction(QIcon('images/line.png'), 'Edge', self)
        addEdgeAction.setShortcut('2')
        addEdgeAction.triggered.connect(self.edgeMode)

        addDirectedEdgeAction = QAction(QIcon('images/arrow.png'), 'DirectedEdge', self)
        addDirectedEdgeAction.setShortcut('3')
        addDirectedEdgeAction.triggered.connect(self.directedEdgeMode)

        deleteNodeAction = QAction(QIcon('images/delete.png'), 'Delete', self)
        deleteNodeAction.setShortcut('4')
        deleteNodeAction.triggered.connect(self.deleteMode)

        findPathAction = QAction(QIcon('images/find.png'), 'Path', self)
        findPathAction.setShortcut('5')
        findPathAction.triggered.connect(self.findMode)

        name_node = QAction(QIcon('images/text.png'), 'Name node', self)
        name_node.setShortcut('6')
        name_node.triggered.connect(self.name_node_mode)

        deleteEdgeAction = QAction(QIcon('images/delete_edge.png'), 'Delete', self)
        deleteEdgeAction.setShortcut('7')
        deleteEdgeAction.triggered.connect(self.deleteModeEdge)

        change_color_b = QAction(QIcon('images/blue.png'), 'Color blue', self)
        change_color_b.setShortcut('B')
        change_color_b.triggered.connect(self.color_b)

        change_color_g = QAction(QIcon('images/green.png'), 'Color green', self)
        change_color_g.setShortcut('G')
        change_color_g.triggered.connect(self.color_g)

        change_color_r = QAction(QIcon('images/red.png'), 'Color red', self)
        change_color_r.setShortcut('R')
        change_color_r.triggered.connect(self.color_r)

        change_color_y = QAction(QIcon('images/yellow.png'), 'Color yellow', self)
        change_color_y.setShortcut('Y')
        change_color_y.triggered.connect(self.color_y)

        load = QAction(QIcon('images/load.png'), 'Load', self)
        load.setShortcut('8')
        load.triggered.connect(self.mode_load)


        self.statusBar()
        self.statusBar().showMessage(self.MSG_MODE_NODE)

        self.toolbar = self.addToolBar('Simple graph')

        self.toolbar.addAction(insertNodeAction)
        self.toolbar.addAction(addEdgeAction)
        self.toolbar.addAction(addDirectedEdgeAction)
        self.toolbar.addAction(deleteNodeAction)
        self.toolbar.addAction(findPathAction)
        self.toolbar.addAction(name_node)
        self.toolbar.addAction(deleteEdgeAction)
        self.toolbar.addAction(change_color_b)
        self.toolbar.addAction(change_color_g)
        self.toolbar.addAction(change_color_r)
        self.toolbar.addAction(change_color_y)
        self.toolbar.addAction(load)





        # sld = QSlider(Qt.Horizontal)
        # sld.valueChanged.connect(self.nodeAndArrowResize)
        # sld.setMinimum(3)
        # sld.setMaximum(15)
        #
        # self.toolbar.addWidget(sld)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        self.toolbar.addAction(exitAction)

        self.show()

    def nodeAndArrowResize(self, value):
        self.canvas.pt_radius = value
        if value > 5:
            self.canvas.arrow_size_coef = 0.3 * value
        else:
            self.canvas.arrow_size_coef = 1.25
        self.canvas.update()

    def nodeMode(self):
        self.canvas.mode = self.MODE_NODE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_NODE)

    def deleteMode(self):
        self.canvas.mode = self.MODE_NODE_DEL
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_NODE_DEL)

    def edgeMode(self):
        self.canvas.mode = self.MODE_EDGE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_EDGE)

    def directedEdgeMode(self):
        self.canvas.mode = self.MODE_DIRECTED_EDGE
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_DIRECTED_EDGE)

    def findMode(self):
        self.canvas.mode = self.MODE_PATH
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_PATH)

    def color_b(self):
        self.canvas.mode = self.MODE_COLOR_B
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_COLOR_B)

    def color_g(self):
        self.canvas.mode = self.MODE_COLOR_G
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_COLOR_G)

    def color_r(self):
        self.canvas.mode = self.MODE_COLOR_R
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_COLOR_R)

    def color_y(self):
        self.canvas.mode = self.MODE_COLOR_Y
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_COLOR_Y)


    def name_node_mode(self):
        self.canvas.mode = self.MODE_TEXT
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_TEXT)

    def deleteModeEdge(self):
        self.canvas.mode = self.MODE_EDGE_DEL
        self.selected_node_idx = None
        self.draggin_idx = []
        self.statusBar().showMessage(self.MSG_MODE_EDGE_DEL)

    def mode_load(self):
        text = self.canvas.get_file_name()
        try:
            with open(text + '.pickle', 'rb') as f:
                a = pickle.load(f)
                e = a[0]
                n = a[1]
                self.canvas.nodes += n
                for n_i, e_i in zip(n, e.values()):
                    self.canvas.edges[id(n_i)] = e_i
                self.canvas.update()
        except FileNotFoundError:
            pass

    def mode_save(self):
        text = self.canvas.get_file_name()
        try:
            with open(text + '.pickle', 'wb') as f:
                temp = list()
                temp.append(self.canvas.edges)
                temp.append(self.canvas.nodes)
                pickle.dump(temp, f)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
