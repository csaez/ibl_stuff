from PySide import QtGui, QtCore

IMAGE_WIDTH = 250
IMAGE_HEIGHT = 150


class Image(QtGui.QWidget):

    def __init__(self, foreground, background, *arg, **kwds):
        super(Image, self).__init__(*arg, **kwds)
        self.foreground = foreground
        self.background = background
        self.pos = IMAGE_WIDTH

    def swipe(self, pos):
        self.pos = pos
        self.repaint()

    def paintEvent(self, event):
        super(Image, self).paintEvent(event)
        p = QtGui.QPainter(self)
        p.drawImage(0, 0, QtGui.QImage(self.background))
        r = QtGui.QRegion(self.pos, 0, IMAGE_WIDTH, IMAGE_HEIGHT)
        p.setClipRegion(r)
        p.drawImage(0, 0, QtGui.QImage(self.foreground))


class Preview(QtGui.QGraphicsView):

    def __init__(self, ibl_data=None, *arg, **kwds):
        super(Preview, self).__init__(*arg, **kwds)
        self.ibl_data = ibl_data or dict()
        for x in (self.setHorizontalScrollBarPolicy,
                  self.setVerticalScrollBarPolicy):
            x(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedSize(IMAGE_WIDTH, 125)
        self.init_ui()

    def init_ui(self):
        scn = QtGui.QGraphicsScene()
        self.setScene(scn)
        self.image = QtGui.QWidget()
        self.ui_image = scn.addWidget(self.image)
        self.update_ui()

    def update_ui(self, ibl_data=None):
        if ibl_data is not None:
            self.ibl_data = ibl_data
        self.image = Image(self.ibl_data.get("sample"),
                           self.ibl_data.get("pano"))
        self.ui_image.setWidget(self.image)

    def mouseMoveEvent(self, event):
        super(Preview, self).mouseMoveEvent(event)
        pos = event.pos().x()
        if pos < 0:
            pos = 0
        self.image.swipe(pos)
