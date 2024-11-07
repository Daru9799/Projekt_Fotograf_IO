from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import os

class MainView(object):
    def setupUi(self, MainWindow, presenter):
        super().__init__()
        self.presenter = presenter

        ### Wszystko ponizej jest wygenerowane przez QT Designer (w razie potrzeby zmiany designu wystarczy zamienic ten kod)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1054, 713)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphics_view.setObjectName("graphics_view")
        self.gridLayout_2.addWidget(self.graphics_view, 2, 1, 6, 3)
        self.add_class_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_class_button.setObjectName("add_class_button")
        self.gridLayout_2.addWidget(self.add_class_button, 3, 0, 1, 1)
        self.delete_annotation_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_annotation_button.setObjectName("delete_annotation_button")
        self.gridLayout_2.addWidget(self.delete_annotation_button, 7, 0, 1, 1)
        self.label_file_list = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_file_list.setFont(font)
        self.label_file_list.setObjectName("label_file_list")
        self.gridLayout_2.addWidget(self.label_file_list, 1, 4, 1, 1)
        self.delete_class_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_class_button.setObjectName("delete_class_button")
        self.gridLayout_2.addWidget(self.delete_class_button, 4, 0, 1, 1)
        self.class_list_widget = QtWidgets.QListWidget(self.centralwidget)
        self.class_list_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.class_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.class_list_widget.setObjectName("class_list_widget")
        self.gridLayout_2.addWidget(self.class_list_widget, 2, 0, 1, 1)
        self.label_annotation_list = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_annotation_list.setFont(font)
        self.label_annotation_list.setObjectName("label_annotation_list")
        self.gridLayout_2.addWidget(self.label_annotation_list, 5, 0, 1, 1)
        self.annotation_list_widget = QtWidgets.QListWidget(self.centralwidget)
        self.annotation_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.annotation_list_widget.setObjectName("annotation_list_widget")
        self.gridLayout_2.addWidget(self.annotation_list_widget, 6, 0, 1, 1)
        self.file_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_list_widget.sizePolicy().hasHeightForWidth())
        self.file_list_widget.setSizePolicy(sizePolicy)
        self.file_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.file_list_widget.setObjectName("file_list_widget")
        self.gridLayout_2.addWidget(self.file_list_widget, 2, 4, 4, 1)
        self.zoom_image_slider = QtWidgets.QSlider(self.centralwidget)
        self.zoom_image_slider.setOrientation(QtCore.Qt.Horizontal)
        self.zoom_image_slider.setObjectName("zoom_image_slider")
        self.gridLayout_2.addWidget(self.zoom_image_slider, 8, 2, 1, 1)
        self.label_class_list = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_class_list.setFont(font)
        self.label_class_list.setObjectName("label_class_list")
        self.gridLayout_2.addWidget(self.label_class_list, 1, 0, 1, 1)
        self.draw_polygon_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_polygon_button.setObjectName("draw_polygon_button")
        self.gridLayout_2.addWidget(self.draw_polygon_button, 1, 1, 1, 1)
        self.draw_rectangle_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_rectangle_button.setObjectName("draw_rectangle_button")
        self.gridLayout_2.addWidget(self.draw_rectangle_button, 1, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(3, 1)
        self.gridLayout_2.setRowStretch(7, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1054, 21))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        self.export_menu = QtWidgets.QMenu(self.menubar)
        self.export_menu.setObjectName("export_menu")
        self.import_menu = QtWidgets.QMenu(self.menubar)
        self.import_menu.setObjectName("import_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.new_project_action = QtWidgets.QAction(MainWindow)
        self.new_project_action.setObjectName("new_project_action")
        self.import_COCO_action = QtWidgets.QAction(MainWindow)
        self.import_COCO_action.setObjectName("import_COCO_action")
        self.import_YOLO_action = QtWidgets.QAction(MainWindow)
        self.import_YOLO_action.setObjectName("import_YOLO_action")
        self.show_statistics_action = QtWidgets.QAction(MainWindow)
        self.show_statistics_action.setObjectName("show_statistics_action")
        self.export_COCO_action = QtWidgets.QAction(MainWindow)
        self.export_COCO_action.setObjectName("export_COCO_action")
        self.export_YOLO_action = QtWidgets.QAction(MainWindow)
        self.export_YOLO_action.setObjectName("export_YOLO_action")
        self.import_COCO_action_2 = QtWidgets.QAction(MainWindow)
        self.import_COCO_action_2.setObjectName("import_COCO_action_2")
        self.import_YOLO_action_2 = QtWidgets.QAction(MainWindow)
        self.import_YOLO_action_2.setObjectName("import_YOLO_action_2")
        self.file_menu.addAction(self.new_project_action)
        self.file_menu.addAction(self.show_statistics_action)
        self.export_menu.addAction(self.export_COCO_action)
        self.export_menu.addAction(self.export_YOLO_action)
        self.import_menu.addAction(self.import_COCO_action_2)
        self.import_menu.addAction(self.import_YOLO_action_2)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.export_menu.menuAction())
        self.menubar.addAction(self.import_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fotograf"))
        self.add_class_button.setText(_translate("MainWindow", "Dodaj klasę"))
        self.delete_annotation_button.setText(_translate("MainWindow", "Usuń adnotację"))
        self.label_file_list.setText(_translate("MainWindow", "Dostępne pliki graficzne:"))
        self.delete_class_button.setText(_translate("MainWindow", "Usuń klasę"))
        self.label_annotation_list.setText(_translate("MainWindow", "Lista dodanych adnotacji:"))
        self.label_class_list.setText(_translate("MainWindow", "Klasy:"))
        self.draw_polygon_button.setText(_translate("MainWindow", "Rysuj Poligon"))
        self.draw_rectangle_button.setText(_translate("MainWindow", "Rysuj Prostokąt"))
        self.file_menu.setTitle(_translate("MainWindow", "Plik"))
        self.export_menu.setTitle(_translate("MainWindow", "Eksportuj"))
        self.import_menu.setTitle(_translate("MainWindow", "Importuj"))
        self.new_project_action.setText(_translate("MainWindow", "Załaduj folder ze zdjęciami"))
        self.import_COCO_action.setText(_translate("MainWindow", "Importuj COCO"))
        self.import_YOLO_action.setText(_translate("MainWindow", "Importuj YOLO"))
        self.show_statistics_action.setText(_translate("MainWindow", "Statystyki"))
        self.export_COCO_action.setText(_translate("MainWindow", "Eksportuj do COCO"))
        self.export_YOLO_action.setText(_translate("MainWindow", "Eksportuj do YOLO"))
        self.import_COCO_action_2.setText(_translate("MainWindow", "Importuj COCO"))
        self.import_YOLO_action_2.setText(_translate("MainWindow", "Importuj YOLO"))

################################### Koniec generowania
        # Tworzenie sceny (pod obrazek zeby mozna bylo go wstawic)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

###Podpięcia pod akcje (odwolujemy sie do nazw przyciskow, list itd.) wywoluja one odpowiednie funkcje w presenterze
        self.new_project_action.triggered.connect(self.presenter.create_new_project) #załadowanie folderu ze zdjęciami
        self.file_list_widget.itemClicked.connect(lambda item: self.presenter.folder_list_on_click(item)) #klikniecia w liscie z obrazkami
        self.add_class_button.clicked.connect(self.presenter.classManagerPresenter.openCreateWindow) # Kliknięcie przycisku "Dodaj klasę"