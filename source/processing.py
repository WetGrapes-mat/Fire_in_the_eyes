import math
import main

from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QFont, QPen
from .entities import Node, Edge


class Canvas(QWidget):
    pt_radius = 3
    arrow_size_coef = 1.25
    delta_coef = 3

    def __init__(self, parent=None):
        super().__init__()
        self.setGeometry(0, 0, 400, 400)
        self.nodes = []
        self.edges = {}
        self.drag_idx = []
        self.path_edges = []
        self.selected_node_idx = None
        self.edges_counter = 0
        self.mode = main.MainWindow.MODE_NODE
        self.cotrolPressed = False
        self.information = {}  # словарь для вывода информации например {'число дуг':'2','число вершин':'3' }

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawGraph(qp)
        qp.end()

    def __calculateTip(self, edge):
        vector = float(edge.v1.x - edge.v2.x), float(edge.v1.y - edge.v2.y)
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        vector_sized = vector[0] * 10 / vector_length, vector[1] * 10 / vector_length

        alpha = 30 * 2 * math.pi / 360

        sin_alpha = math.sin(alpha)
        cos_alpha = math.cos(alpha)

        tip1 = (vector_sized[0] * cos_alpha - vector_sized[1] * sin_alpha,
                vector_sized[0] * sin_alpha + vector_sized[1] * cos_alpha)

        sin_alpha = math.sin(-alpha)
        cos_alpha = math.cos(-alpha)

        tip2 = (vector_sized[0] * cos_alpha - vector_sized[1] * sin_alpha,
                vector_sized[0] * sin_alpha + vector_sized[1] * cos_alpha)

        return tip1, tip2

    def drawGraph(self, qp):  # отрисовка
        pos_y = 10

        self.information["Edges: "] = self.edges_counter
        self.information["Nodes: "] = len(self.nodes)

        # if len(self.information) > 10:
        #    i = 1
        #    for key, item in self.information.items():
        #        if i > 2:
        #            a = self.information.pop(key)
        #        i += 1

        for key, item in self.information.items():
            qp.drawText(int(5), int(pos_y), "{}: {}".format(key.capitalize(), item))
            pos_y += 15
        qp.setPen(Qt.black)
        qp.setBrush(Qt.black)

        for i, node in enumerate(self.nodes):
            qpoint = QPoint(int(node.x), int(node.y))

            if i == self.selected_node_idx:
                qp.setBrush(Qt.magenta)
            elif i in self.drag_idx:
                qp.setBrush(Qt.cyan)
            elif node.color is not None:
                self.change_color_node(node, qp)

            qp.drawEllipse(qpoint, self.pt_radius * 2, self.pt_radius * 2)
            qp.drawText(int(node.x + 10), int(node.y + 10), node.text_name)
            qp.setBrush(Qt.black)

        for _, edges in self.edges.items():
            for edge in edges:
                repeat_edge_count = 0
                for edge_ in edges:
                    if edge.v1.x == edge_.v1.x and edge.v2.x == edge_.v2.x and edge.v1.y == edge_.v1.y \
                            and edge.v2.y == edge_.v2.y:
                        repeat_edge_count += 1
                if edge.color is not None:
                    self.change_color_edge(edge, qp)
                    dx = edge.v2.x - edge.v1.x
                    dy = edge.v2.y - edge.v1.y
                    weight = str(int(abs(edge)))
                    qp.drawLine(int(edge.v1.x), int(edge.v1.y), int(edge.v2.x),
                                int(edge.v2.y))  # простая дуга рисование
                    font = QFont("Helvetica")
                    font.setPixelSize(13)
                    qp.setFont(font)
                    qp.setPen(Qt.black)
                    qp.drawText(int(dx / 2 + edge.v1.x), int(dy / 2 + edge.v1.y), weight)
                    if repeat_edge_count > 1:
                        print("check 2")
                        qp.drawText(int(dx / 2 + edge.v1.x - 10), int(dy / 2 + edge.v1.y - 10), str(repeat_edge_count))
                    if edge.direction:
                        self.change_color_edge(edge, qp)
                        tip = self.__calculateTip(edge)
                        coef = self.arrow_size_coef
                        qp.drawPolygon(QPoint(int(edge.v2.x), int(edge.v2.y)),
                                       QPoint(int(edge.v2.x + coef * tip[0][0]), int(edge.v2.y + coef * tip[0][1])),
                                       QPoint(int(edge.v2.x + coef * tip[1][0]), int(edge.v2.y + coef * tip[1][1])))
                else:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.black)
                    dx = edge.v2.x - edge.v1.x
                    dy = edge.v2.y - edge.v1.y
                    weight = str(int(abs(edge)))
                    qp.drawLine(int(edge.v1.x), int(edge.v1.y), int(edge.v2.x),
                                int(edge.v2.y))  # простая дуга рисование
                    font = QFont("Helvetica")
                    font.setPixelSize(13)
                    qp.setFont(font)
                    qp.drawText(int(dx / 2 + edge.v1.x), int(dy / 2 + edge.v1.y), weight)
                    if repeat_edge_count > 1:
                        print("check 2")
                        qp.drawText(int(dx / 2 + edge.v1.x - 10), int(dy / 2 + edge.v1.y - 10), str(repeat_edge_count))
                    if edge.direction:
                        qp.setPen(Qt.black)
                        tip = self.__calculateTip(edge)
                        coef = self.arrow_size_coef
                        qp.drawPolygon(QPoint(int(edge.v2.x), int(edge.v2.y)),
                                       QPoint(int(edge.v2.x + coef * tip[0][0]), int(edge.v2.y + coef * tip[0][1])),
                                       QPoint(int(edge.v2.x + coef * tip[1][0]), int(edge.v2.y + coef * tip[1][1])))
                        qp.setPen(Qt.black)

        if self.path_edges:
            path_nodes = []
            for _ in self.path_edges:
                for node in self.nodes:
                    if _ == id(node):
                        path_nodes.append(node)

            for i in range(len(path_nodes)):
                if i == len(path_nodes) - 1:
                    break
                qPen = QPen()
                qPen.setColor(Qt.yellow)
                qPen.setWidth(2)
                qp.setPen(qPen)
                qp.drawLine(int(path_nodes[i].x), int(path_nodes[i].y), int(path_nodes[i + 1].x),
                            int(path_nodes[i + 1].y))
                qp.setPen(Qt.black)

    def _get_point(self, evt):
        return evt.pos().x(), evt.pos().y()

    def _focus_node(self, x, y):
        node = Node([x, y])
        distances = []
        for v in self.nodes:
            distances.append(math.sqrt(sum((i1 - i2) ** 2 for i1, i2 in zip(v, node))))
        if distances and (min(distances) < self.pt_radius + self.delta_coef):
            focused_node_idx = distances.index(min(distances))
            return focused_node_idx
        return None

    def addNode(self, x, y):
        new_node = Node([x, y])
        self.nodes.append(new_node)
        self.edges[id(new_node)] = []
        return

    def deleteNode(self, node_idx):
        node = self.nodes[node_idx]
        print(node)
        for node_id, edges in self.edges.items():
            for i, edge in enumerate(edges):
                print("Incoming edges:")
                print(edge)
                if edge.v2 == node:
                    print("Deleting {}".format(edge))
                    del edges[i]
        print("Deleting outgoing edges")
        del self.edges[id(node)]
        print("Deleting node")
        del self.nodes[node_idx]

    # можно попробовать изменить логику и чтобы узла хранили одну и туже дугу если она не направленая
    # но если так то не работает поиск пути
    def addEdge(self, v1_idx, v2_idx, directed=False):
        v1 = self.nodes[v1_idx]
        v2 = self.nodes[v2_idx]
        self.edges_counter += 1
        new_edge = Edge(v1, v2, directed)
        new_edge_back = Edge(v2, v1, directed)
        if not new_edge in self.edges[id(v1)] and not new_edge_back in self.edges[id(v2)]:
            if directed is False:
                self.edges[id(v1)].append(new_edge)
                self.edges[id(v2)].append(new_edge_back)
            elif directed is True:
                self.edges[id(v1)].append(new_edge)
        return

    def deleteEdge(self, x, y):
        delta_p = 5
        delta_m = -5
        delete_counter = 0
        for node_id, edge_1 in self.edges.items():
            for edge in edge_1:
                distance = abs((edge.v1.y - edge.v2.y) * x + (edge.v2.x - edge.v1.x) * y +
                               (edge.v1.x * edge.v2.y - edge.v2.x * edge.v1.y)) / \
                           (((edge.v2.x - edge.v1.x) ** 2 + (edge.v2.y - edge.v1.y) ** 2) ** 0.5)
                if delta_m < distance or distance < delta_p:
                    if (edge.v1.x <= x <= edge.v2.x or edge.v2.x <= x <= edge.v1.x) and (
                            edge.v1.y <= y <= edge.v2.y or edge.v2.y <= y <= edge.v1.y):
                        edge_1.remove(edge)

                        delete_counter += 1
        if delete_counter == 1:
            self.edges_counter -= 1
        if delete_counter == 2:
            self.edges_counter -= 1
        self.update()

    def _focus_edge(self, x, y):

        delta_p = 10
        delta_m = -10

        f = False
        for node_id, edge_1 in self.edges.items():
            for edge in edge_1:
                distance = abs((edge.v1.y - edge.v2.y) * x + (edge.v2.x - edge.v1.x) * y +
                               (edge.v1.x * edge.v2.y - edge.v2.x * edge.v1.y)) / \
                           (((edge.v2.x - edge.v1.x) ** 2 + (edge.v2.y - edge.v1.y) ** 2) ** 0.5)

                if delta_m < distance or distance < delta_p:
                    if (edge.v1.x <= x <= edge.v2.x or edge.v2.x <= x <= edge.v1.x) and (
                            edge.v1.y <= y <= edge.v2.y or edge.v2.y <= y <= edge.v1.y):
                        f = True
        return f

    def set_edge_color(self, x, y, color):
        delta_m = -5
        delta_p = 5
        for node_id, edge_1 in self.edges.items():
            for edge in edge_1:
                distance = abs((edge.v1.y - edge.v2.y) * x + (edge.v2.x - edge.v1.x) * y +
                               (edge.v1.x * edge.v2.y - edge.v2.x * edge.v1.y)) / \
                           (((edge.v2.x - edge.v1.x) ** 2 + (edge.v2.y - edge.v1.y) ** 2) ** 0.5)
                if delta_m < distance or distance < delta_p:
                    if (edge.v1.x <= x <= edge.v2.x or edge.v2.x <= x <= edge.v1.x) and (
                            edge.v1.y <= y <= edge.v2.y or edge.v2.y <= y <= edge.v1.y):
                        edge.color = color

    def grabNode(self, node_idx):
        self.path_edges = []
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:

            print('Shift+MouseClick')
            if node_idx not in self.drag_idx:
                self.drag_idx.append(node_idx)
            else:
                self.drag_idx.remove(node_idx)

            self.cotrolPressed = True
            self.update()

        else:
            if self.cotrolPressed == True:
                if node_idx not in self.drag_idx:
                    self.drag_idx.append(node_idx)
                else:
                    self.drag_idx.remove(node_idx)
                    self.drag_idx.append(node_idx)  # making sure the pointed node is the last in the indices list
                self.cotrolPressed = False
            else:
                self.drag_idx = [node_idx, ]
        return

    def change_color_node(self, node, qt):
        t = node.color
        if t == 1:
            return qt.setBrush(Qt.blue)
        elif t == 2:
            return qt.setBrush(Qt.green)
        elif t == 3:
            return qt.setBrush(Qt.red)
        elif t == 4:
            return qt.setBrush(Qt.yellow)

    def change_color_edge(self, edge, qt):
        t = edge.color
        if t == 1:
            qt.setBrush(Qt.blue)
            qt.setPen(Qt.blue)
            return qt
        elif t == 2:
            qt.setBrush(Qt.green)
            qt.setPen(Qt.green)
            return qt
        elif t == 3:
            qt.setBrush(Qt.red)
            qt.setPen(Qt.red)
            return qt
        elif t == 4:
            qt.setBrush(Qt.yellow)
            qt.setPen(Qt.yellow)
            return qt

    def get_file_name(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter file name:')
        if ok:
            return text

    def mousePressEvent(self, evt):

        if self.mode == main.MainWindow.MODE_NODE:
            self.path_edges = []
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    self.grabNode(focused_node_idx)
                else:
                    self.addNode(x, y)
                    self.update()
            print('Список вершин ', self.nodes)
            print('Список дуг ', self.edges)
            print('-' * 30)

        elif self.mode == main.MainWindow.MODE_EDGE:
            self.path_edges = []
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx:  # same node, deselect
                            self.selected_node_idx = None
                            self.update()
                        else:
                            self.addEdge(self.selected_node_idx, focused_node_idx)
                            self.selected_node_idx = None
                            self.update()
            print('Список вершин ', self.nodes)
            print('Список дуг ', self.edges)
            print('-' * 30)


        elif self.mode == main.MainWindow.MODE_DIRECTED_EDGE:
            self.path_edges = []
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx:
                            self.selected_node_idx = None
                            self.update()
                        else:
                            self.addEdge(self.selected_node_idx, focused_node_idx, directed=True)
                            self.selected_node_idx = None
                            self.update()
            print('Список вершин ', self.nodes)
            print('Список дуг ', self.edges)
            print('-' * 30)


        elif self.mode == main.MainWindow.MODE_NODE_DEL:
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)

                if not focused_node_idx is None:
                    self.deleteNode(focused_node_idx)
                self.update()
            print('Список вершин ', self.nodes)
            print('Список дуг ', self.edges)
            print('-' * 30)


        elif self.mode == main.MainWindow.MODE_PATH:
            if evt.button() == Qt.LeftButton and self.drag_idx == []:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    if self.selected_node_idx is None:
                        self.selected_node_idx = focused_node_idx
                        self.update()
                    else:
                        if self.selected_node_idx == focused_node_idx:  # same node
                            self.selected_node_idx = None
                            self.update()
                        else:
                            distances, chain = self.dijkstra(self.selected_node_idx, focused_node_idx)
                            print("#" * 30, " Dijkstra result ", "#" * 30)
                            print("V1: {} \n".format(self.selected_node_idx))
                            print("V2: {} \n".format(focused_node_idx))
                            print(distances, chain, distances[id(self.nodes[focused_node_idx])])
                            self.information["path len:"] = int(distances[id(self.nodes[focused_node_idx])])
                            self.selected_node_idx = None
                            self.update()

        elif self.mode == main.MainWindow.MODE_COLOR_B:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    self.nodes[self._focus_node(x, y)].color = 1
                    self.update()
                elif self._focus_edge(x, y):
                    self.set_edge_color(x, y, 1)
                    self.update()

        elif self.mode == main.MainWindow.MODE_COLOR_G:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    self.nodes[self._focus_node(x, y)].color = 2
                    self.update()
                elif self._focus_edge(x, y):
                    self.set_edge_color(x, y, 2)
                    self.update()


        elif self.mode == main.MainWindow.MODE_COLOR_R:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    self.nodes[self._focus_node(x, y)].color = 3

                    self.update()
                elif self._focus_edge(x, y):
                    self.set_edge_color(x, y, 3)
                    self.update()

        elif self.mode == main.MainWindow.MODE_COLOR_Y:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    self.nodes[self._focus_node(x, y)].color = 4

                    self.update()
                elif self._focus_edge(x, y):
                    self.set_edge_color(x, y, 4)
                    self.update()

        elif self.mode == main.MainWindow.MODE_TEXT:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)
                focused_node_idx = self._focus_node(x, y)
                if not focused_node_idx is None:
                    text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter node name:')
                    if ok:
                        self.nodes[self._focus_node(x, y)].text_name = text
                    self.update()

        elif self.mode == main.MainWindow.MODE_EDGE_DEL:
            if evt.button() == Qt.LeftButton:
                x, y = self._get_point(evt)

                self.deleteEdge(x, y)
                self.update()




    def mouseMoveEvent(self, evt):
        if self.drag_idx != [] and not self.cotrolPressed:

            moving_nodes = [self.nodes[i] for i in self.drag_idx]
            last_node = moving_nodes[-1]

            x, y = self._get_point(evt)

            x_delta = x - last_node.x
            y_delta = y - last_node.y

            for node in moving_nodes:
                node.x += x_delta
                node.y += y_delta

            self.update()

    def mouseReleaseEvent(self, evt):
        if evt.button() == Qt.LeftButton and not self.cotrolPressed and self.drag_idx != []:

            print('Список вершин ', self.nodes)
            print('Список дуг ', self.edges)
            print('-' * 30)

            moving_nodes = [self.nodes[i] for i in self.drag_idx]
            last_node = moving_nodes[-1]

            x, y = self._get_point(evt)

            x_delta = x - last_node.x
            y_delta = y - last_node.y

            for node in moving_nodes:
                node.x += x_delta
                node.y += y_delta

            self.drag_idx = []
            self.update()

    def dijkstra(self, v1_idx, v2_idx, directed=True):

        v1 = self.nodes[v1_idx]
        v2 = self.nodes[v2_idx]

        dist = {}
        prev = {}
        q = {}
        visited = set()

        for v in self.nodes:
            dist[id(v)] = 999999999
            prev[id(v)] = -1
            q[id(v)] = v

        dist[id(v1)] = 0

        while len(visited) != len(q):

            temp_dict = {}
            for k, v in dist.items():
                if k not in visited:
                    temp_dict[k] = v
            i = min(temp_dict, key=temp_dict.get)

            visited.add(i)

            for e in self.edges[i]:
                if id(e.v2) in q and id(e.v2) not in visited:
                    alt = dist[i] + abs(e)
                    if alt < dist[id(e.v2)]:
                        dist[id(e.v2)] = alt
                        prev[id(e.v2)] = i

            l = []
            l.append(id(v2))
            prev_id = prev[id(v2)]
            l.append(prev_id)
            while prev_id != -1:
                prev_id = prev[prev_id]
                if prev_id != -1:
                    l.append(prev_id)

            self.path_edges = l

        return dist, prev
