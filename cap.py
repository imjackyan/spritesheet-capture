import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab, Image
import argparse, time, math


parser = argparse.ArgumentParser(description="Gif Capture")
parser.add_argument('-f', '--frameTime', default=0.05, type=float, help="time between each capture in seconds")
parser.add_argument('-d', '--duration', default=60, type=float, help="full capture duration in seconds")
parser.add_argument('-c', '--columns', default=10, type=int, help="number of columns of final sprite sheet")
parser.add_argument('-o', '--output', default="images/image.png", type=str, help="the output destination AND file name. ie path/img.png")

args = parser.parse_args();


class Window(QtWidgets.QWidget):
    frameTime = 0.05
    duration = 60
    columns = 10
    images = []
    output_dir = ""

    def __init__(self, frame_time = 0.05, duration = 60, columns = 10, output_directory = "image.png"):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0,0,screen_width, screen_height)
        self.setWindowTitle(" ")
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print("Capturing the screen...")

        self.frameTime = frame_time
        self.duration = duration
        self.columns = columns
        self.output_dir = output_directory

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("black"), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        # width = self.end.x() - self.begin.x()
        # height = self.end.y() - self.begin.y()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        img = ImageGrab.grab(bbox=(x1,y1,x2,y2))

        mon = {'top': y1, 'left': x1, 'width': x2-x1, 'height': y2-y1}
        sct = mss()

        last_time = time.time()
        start_time = last_time
        i = 0
        run = True
        while run:
            if(time.time() - last_time > self.frameTime):
                last_time = time.time()

                #img = sct.grab(mon)
                #tools.to_png(img.rgb, img.size, ("images/img_" + str(i) + ".png"))
                img = ImageGrab.grab(bbox=(x1,y1,x2,y2))
                #img.save("images/img_" + str(i) + ".PNG")

                self.images.append(img)

                i += 1
                #print("image {} captured @ {}".format(i, last_time))

                if last_time - start_time > self.duration:
                    run = False
                    self.createSpritesheet()

    def createSpritesheet(self):
        w = self.images[0].size[0]
        h = self.images[0].size[1]
        mWidth = self.columns * w
        mHeight = math.ceil(len(self.images) / self.columns) * h

        master = Image.new(mode='RGBA', size=(mWidth, mHeight), color=(0,0,0,0))

        row = 0
        col = 0
        for image in self.images:
            location = (w * col, h * row)
            master.paste(image, location)
            col += 1
            if col >= self.columns:
                col = 0
                row += 1

        hasDot = False

        path = self.output_dir
        for i in range(len(self.output_dir)-1,0,-1):
            if self.output_dir[i] == '.':
                hasDot = True
            if self.output_dir[i] == '/':
                if not hasDot:
                    break
                path = self.output_dir[0:i]
                break


        if not os.path.isdir(path):
            os.makedirs(path)

        master.save(self.output_dir)
        print("Sprite sheet successfully saved to {}".format(self.output_dir))
        #print("{} {}".format(w, h))
        #print("{} {}".format(mWidth, mHeight))


app = QtWidgets.QApplication(sys.argv)
window = Window(args.frameTime, args.duration, args.columns, args.output)
window.show()
app.aboutToQuit.connect(app.deleteLater)
sys.exit(app.exec_())
