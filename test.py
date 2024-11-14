import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        # Utwórz widok graficzny i scenę
        self.view = QGraphicsView(self)
        self.view.setGeometry(50, 50, 700, 500)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Utworzenie obrazu w OpenCV
        image = np.zeros((500, 700, 3), dtype=np.uint8)

        # Współrzędne prostokąta: (x, y, szerokość, wysokość)
        rect_x, rect_y, rect_w, rect_h = 100, 100, 200, 150

        # Narysuj prostokąt w OpenCV
        cv2.rectangle(image, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (0, 255, 0), 2)

        # Konwertuj obraz z OpenCV (BGR) do formatu RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Utwórz QImage z obrazu numpy
        height, width, channel = image_rgb.shape
        bytes_per_line = 3 * width
        qimage = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Utwórz QPixmap z QImage
        pixmap = QPixmap.fromImage(qimage)

        # Utwórz element graficzny obrazu
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        self.show()


# Główna pętla aplikacji PyQt
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())