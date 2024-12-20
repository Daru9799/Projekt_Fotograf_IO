from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QKeyEvent, QIntValidator
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QMessageBox
from PyQt5.QtGui import QMouseEvent, QIntValidator
from PyQt5.Qt import Qt



class MainView(object):
    def setupUi(self, MainWindow, presenter):
        super().__init__()
        self.presenter = presenter
        self.pixmap_item = None #zmienna przechowująca referencje do aktualnego zdjęcia

        ### Wszystko ponizej jest wygenerowane przez QT Designer (w razie potrzeby zmiany designu wystarczy zamienic ten kod)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1054, 713)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.file_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_list_widget.sizePolicy().hasHeightForWidth())
        self.file_list_widget.setSizePolicy(sizePolicy)
        self.file_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.file_list_widget.setObjectName("file_list_widget")
        self.gridLayout_2.addWidget(self.file_list_widget, 2, 5, 3, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_annotation_list = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_annotation_list.sizePolicy().hasHeightForWidth())
        self.label_annotation_list.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_annotation_list.setFont(font)
        self.label_annotation_list.setObjectName("label_annotation_list")
        self.verticalLayout_5.addWidget(self.label_annotation_list)
        self.annotation_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.annotation_list_widget.sizePolicy().hasHeightForWidth())
        self.annotation_list_widget.setSizePolicy(sizePolicy)
        self.annotation_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.annotation_list_widget.setObjectName("annotation_list_widget")
        self.verticalLayout_5.addWidget(self.annotation_list_widget)
        self.delete_annotation_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_annotation_button.sizePolicy().hasHeightForWidth())
        self.delete_annotation_button.setSizePolicy(sizePolicy)
        self.delete_annotation_button.setObjectName("delete_annotation_button")
        self.verticalLayout_5.addWidget(self.delete_annotation_button)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 15, 0, 1, 1)
        self.class_list_widget = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.class_list_widget.sizePolicy().hasHeightForWidth())
        self.class_list_widget.setSizePolicy(sizePolicy)
        self.class_list_widget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.class_list_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.class_list_widget.setObjectName("class_list_widget")
        self.gridLayout_2.addWidget(self.class_list_widget, 2, 0, 7, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_exif_data = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_exif_data.sizePolicy().hasHeightForWidth())
        self.label_exif_data.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_exif_data.setFont(font)
        self.label_exif_data.setIndent(-1)
        self.label_exif_data.setObjectName("label_exif_data")
        self.verticalLayout_2.addWidget(self.label_exif_data)
        self.show_exif_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_exif_button.setObjectName("show_exif_button")
        self.verticalLayout_2.addWidget(self.show_exif_button)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 15, 5, 2, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_tools = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_tools.sizePolicy().hasHeightForWidth())
        self.label_tools.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_tools.setFont(font)
        self.label_tools.setObjectName("label_tools")
        self.verticalLayout.addWidget(self.label_tools)
        self.draw_rectangle_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.draw_rectangle_button.sizePolicy().hasHeightForWidth())
        self.draw_rectangle_button.setSizePolicy(sizePolicy)
        self.draw_rectangle_button.setObjectName("draw_rectangle_button")
        self.verticalLayout.addWidget(self.draw_rectangle_button)
        self.draw_polygon_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_polygon_button.setObjectName("draw_polygon_button")
        self.verticalLayout.addWidget(self.draw_polygon_button)
        self.auto_selection_button = QtWidgets.QPushButton(self.centralwidget)
        self.auto_selection_button.setObjectName("auto_selection_button")
        self.verticalLayout.addWidget(self.auto_selection_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout, 6, 5, 4, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_class_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_class_button.sizePolicy().hasHeightForWidth())
        self.add_class_button.setSizePolicy(sizePolicy)
        self.add_class_button.setObjectName("add_class_button")
        self.horizontalLayout.addWidget(self.add_class_button)
        self.delete_class_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_class_button.sizePolicy().hasHeightForWidth())
        self.delete_class_button.setSizePolicy(sizePolicy)
        self.delete_class_button.setObjectName("delete_class_button")
        self.horizontalLayout.addWidget(self.delete_class_button)
        self.gridLayout_2.addLayout(self.horizontalLayout, 9, 0, 1, 1)
        self.graphics_view = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(220)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics_view.sizePolicy().hasHeightForWidth())
        self.graphics_view.setSizePolicy(sizePolicy)
        self.graphics_view.setMinimumSize(QtCore.QSize(0, 0))
        self.graphics_view.setObjectName("graphics_view")
        self.gridLayout_2.addWidget(self.graphics_view, 2, 1, 15, 4)
        self.label_class_list = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_class_list.sizePolicy().hasHeightForWidth())
        self.label_class_list.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_class_list.setFont(font)
        self.label_class_list.setObjectName("label_class_list")
        self.gridLayout_2.addWidget(self.label_class_list, 1, 0, 1, 1)
        self.label_file_list = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_file_list.sizePolicy().hasHeightForWidth())
        self.label_file_list.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_file_list.setFont(font)
        self.label_file_list.setObjectName("label_file_list")
        self.gridLayout_2.addWidget(self.label_file_list, 1, 5, 1, 1)
        self.label_image_size = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_image_size.sizePolicy().hasHeightForWidth())
        self.label_image_size.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_image_size.setFont(font)
        self.label_image_size.setObjectName("label_image_size")
        self.gridLayout_2.addWidget(self.label_image_size, 17, 1, 1, 1)
        # self.zoom_image_slider = QtWidgets.QSlider(self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.zoom_image_slider.sizePolicy().hasHeightForWidth())
        # self.zoom_image_slider.setSizePolicy(sizePolicy)
        # self.zoom_image_slider.setOrientation(QtCore.Qt.Horizontal)
        # self.zoom_image_slider.setObjectName("zoom_image_slider")
        # self.gridLayout_2.addWidget(self.zoom_image_slider, 17, 2, 1, 2)



        # Pusta kolumna dla wyrównania
        # Spacer z lewej strony
        spacer_left = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # Suwak zooma
        self.zoom_image_slider = QtWidgets.QSlider(self.centralwidget)
        self.zoom_image_slider.setOrientation(QtCore.Qt.Horizontal)
        self.zoom_image_slider.setObjectName("zoom_image_slider")

        # Pole wartości zooma
        self.zoom_value_widget = QtWidgets.QLineEdit(self.centralwidget)
        self.zoom_value_widget.setFixedWidth(50)  # Stała szerokość
        self.zoom_value_widget.setAlignment(QtCore.Qt.AlignCenter)  # Wyśrodkowanie tekstu w polu
        self.zoom_value_widget.setObjectName("zoom_value_widget")

        # Spacer z prawej strony
        spacer_right = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # Ustawienia proporcji kolumn
        self.gridLayout_2.setColumnStretch(1, 1)  # Lewy spacer
        self.gridLayout_2.setColumnStretch(2, 3)  # Suwak (kolumna środkowa)
        self.gridLayout_2.setColumnStretch(3, 1)  # Pole wartości zooma
        self.gridLayout_2.setColumnStretch(4, 1)  # Prawy spacer

        # Dodanie elementów do siatki
        self.gridLayout_2.addItem(spacer_left, 17, 1, 1, 1)  # Lewa kolumna
        self.gridLayout_2.addWidget(self.zoom_image_slider, 17, 2, 1, 1)  # Środkowa kolumna - suwak
        self.gridLayout_2.addWidget(self.zoom_value_widget, 17, 3, 1, 1)  # Prawa kolumna - pole wartości
        self.gridLayout_2.addItem(spacer_right, 17, 4, 1, 1)  # Prawa kolumna




        self.label_notification = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_notification.sizePolicy().hasHeightForWidth())
        self.label_notification.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_notification.setFont(font)
        self.label_notification.setObjectName("label_notification")
        self.gridLayout_2.addWidget(self.label_notification, 1, 1, 1, 4)
        self.gridLayout_2.setColumnStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1054, 26))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        self.export_menu = QtWidgets.QMenu(self.menubar)
        self.export_menu.setObjectName("export_menu")
        self.import_menu = QtWidgets.QMenu(self.menubar)
        self.import_menu.setObjectName("import_menu")
        self.menuAdnotacje = QtWidgets.QMenu(self.menubar)
        self.menuAdnotacje.setObjectName("menuAdnotacje")
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
        self.save_project_action = QtWidgets.QAction(MainWindow)
        self.save_project_action.setObjectName("save_project_action")
        self.save_as_new_project_action = QtWidgets.QAction(MainWindow)
        self.save_as_new_project_action.setObjectName("save_as_new_project_action")
        self.show_statistics_action_2 = QtWidgets.QAction(MainWindow)
        self.show_statistics_action_2.setObjectName("show_statistics_action_2")
        self.load_project_action = QtWidgets.QAction(MainWindow)
        self.load_project_action.setObjectName("load_project_action")
        self.file_menu.addAction(self.new_project_action)
        self.file_menu.addAction(self.load_project_action)
        self.file_menu.addAction(self.save_project_action)
        self.file_menu.addAction(self.save_as_new_project_action)
        self.export_menu.addAction(self.export_COCO_action)
        self.export_menu.addAction(self.export_YOLO_action)
        self.import_menu.addAction(self.import_COCO_action_2)
        self.import_menu.addAction(self.import_YOLO_action_2)
        self.menuAdnotacje.addAction(self.show_statistics_action_2)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.export_menu.menuAction())
        self.menubar.addAction(self.import_menu.menuAction())
        self.menubar.addAction(self.menuAdnotacje.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #TESTY -------------------------------------------------------------
        # item = QListWidgetItem(self.class_list_widget)
        # self.class_list_widget.addItem(item)
        # row = CustomClassListItemView("aha")
        # item.setSizeHint(row.minimumSizeHint())
        # self.class_list_widget.setItemWidget(item, row)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fotograf"))
        self.label_annotation_list.setText(_translate("MainWindow", "Lista dodanych adnotacji:"))
        self.delete_annotation_button.setText(_translate("MainWindow", "Usuń adnotację"))
        self.label_exif_data.setText(_translate("MainWindow", "Dane exif:"))
        self.show_exif_button.setText(_translate("MainWindow", "Pokaż dane exif"))
        self.label_tools.setText(_translate("MainWindow", "Narzędzia:"))
        self.draw_rectangle_button.setText(_translate("MainWindow", "Rysuj Prostokąt"))
        self.draw_polygon_button.setText(_translate("MainWindow", "Rysuj Poligon"))
        self.auto_selection_button.setText(_translate("MainWindow", "Automatyczne zaznaczanie"))
        self.add_class_button.setText(_translate("MainWindow", "Dodaj klasę"))
        self.delete_class_button.setText(_translate("MainWindow", "Usuń klasę"))
        self.label_class_list.setText(_translate("MainWindow", "Klasy:"))
        self.label_file_list.setText(_translate("MainWindow", "Dostępne pliki graficzne:"))
        self.label_image_size.setText(_translate("MainWindow", "Brak aktywnego obrazu"))
        self.label_notification.setText(_translate("MainWindow", "Brak aktywnego narzędzia do rysowania."))
        self.file_menu.setTitle(_translate("MainWindow", "Plik"))
        self.export_menu.setTitle(_translate("MainWindow", "Eksportuj"))
        self.import_menu.setTitle(_translate("MainWindow", "Importuj"))
        self.menuAdnotacje.setTitle(_translate("MainWindow", "Adnotacje"))
        self.new_project_action.setText(_translate("MainWindow", "Załaduj folder ze zdjęciami"))
        self.import_COCO_action.setText(_translate("MainWindow", "Importuj COCO"))
        self.import_YOLO_action.setText(_translate("MainWindow", "Importuj YOLO"))
        self.show_statistics_action.setText(_translate("MainWindow", "Statystyki"))
        self.export_COCO_action.setText(_translate("MainWindow", "Eksportuj do COCO"))
        self.export_YOLO_action.setText(_translate("MainWindow", "Eksportuj do YOLO"))
        self.import_COCO_action_2.setText(_translate("MainWindow", "Importuj COCO"))
        self.import_YOLO_action_2.setText(_translate("MainWindow", "Importuj YOLO"))
        self.save_project_action.setText(_translate("MainWindow", "Zapisz"))
        self.save_as_new_project_action.setText(_translate("MainWindow", "Zapisz jako plik projektowy"))
        self.show_statistics_action_2.setText(_translate("MainWindow", "Statystyki"))
        self.load_project_action.setText(_translate("MainWindow", "Wczytaj plik projektowy"))

######################################## Koniec generowania
        self.set_zoom_slider_visibility(False)
        #Ustawienie ikonek
        MainWindow.setWindowIcon(QIcon("img/cameraIcon.png"))

        # Tworzenie sceny (pod obrazek zeby mozna bylo go wstawic)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        #Przypisanie sledzenia klikniecia do funkcji
        self.graphics_view.mousePressEvent = self.mouse_press_event
        self.graphics_view.mouseReleaseEvent = self.mouse_release_event

        #Scroll
        self.graphics_view.wheelEvent = self.mouse_wheel_event

        #Obsluga klawisza
        self.centralwidget.keyPressEvent = self.key_press_event

        #Śledzenie myszy
        self.graphics_view.setMouseTracking(True)

        #Obsługa ruchu myszy
        self.graphics_view.mouseMoveEvent = self.mouse_move_event
        self.is_dragging = False
        self.last_mouse_position = None
        self.is_drawing_rectangle = False  # Domyślnie nie rysujemy prostokąta

        #ZOOM
        # Ustawienie zakresu wartości suwaka zoomu (od 10% do 500%)
        self.zoom_image_slider.setRange(10, 500)
        self.zoom_value_widget.setValidator(QIntValidator(self.zoom_value_widget))
        self.zoom_value_widget.setText(str(70))
        self.zoom_value_widget.setStyleSheet("color: white;")
        # Ustawienie początkowej wartości suwaka na 70%
        self.zoom_image_slider.setValue(70)

###Podpięcia pod akcje (odwolujemy sie do nazw przyciskow, list itd.) wywoluja one odpowiednie funkcje w presenterze
        self.new_project_action.triggered.connect(self.presenter.create_new_project) #załadowanie folderu ze zdjęciami
        self.file_list_widget.itemClicked.connect(lambda item: self.presenter.folder_list_on_click(item)) #klikniecia w liscie z obrazkami
        self.add_class_button.clicked.connect(self.presenter.classManagerPresenter.openCreateWindow) # Kliknięcie przycisku "Dodaj klasę"
        self.delete_class_button.clicked.connect(self.presenter.classManagerPresenter.deleteClass) #Klikniecie przycisku "usun klasę"
        self.draw_rectangle_button.clicked.connect(self.presenter.activate_rectangle_tool) #Kliknięcie przycisku rysuj prostokąt
        self.draw_polygon_button.clicked.connect(self.presenter.activate_polygon_tool)  # Kliknięcie przycisku rysuj poligon
        self.auto_selection_button.clicked.connect(self.presenter.activate_auto_selection_tool)
        self.zoom_image_slider.valueChanged.connect(self.presenter.zoom_slider) #Kliknięcie w zooma
        self.delete_annotation_button.clicked.connect(self.presenter.annotation_presenter.delete_selected_annotations)# Usuń Annotacje- przycisk
        self.show_exif_button.clicked.connect(self.presenter.open_exif_window)
        self.zoom_value_widget.editingFinished.connect(self.presenter.zoom_value)
        self.export_COCO_action.triggered.connect(self.presenter.export_to_coco_fun)
        self.import_COCO_action_2.triggered.connect(self.presenter.import_from_coco)
        self.save_project_action.triggered.connect(self.presenter.save_project_fun)
        self.save_as_new_project_action.triggered.connect(self.presenter.save_as_project_fun)
        self.export_YOLO_action.triggered.connect(self.presenter.export_to_yolo_fun)
        self.load_project_action.triggered.connect(self.presenter.import_project)
        self.import_YOLO_action_2.triggered.connect(self.presenter.import_from_yolo)
        self.show_statistics_action_2.triggered.connect(self.presenter.statistics_presenter.open_statistics_window)


###Wskazówki dla użytkownika
        self.delete_annotation_button.setToolTip("Zaznacz kwadrat obok wybranej adnotacji, a następnie kliknij tutaj, aby ją usunąć")
        self.zoom_image_slider.setToolTip("Przesuń w prawo/lewo w celu zwiększenia/zmniejszenia obrazu")
###Funkcje pomocnicze (np. Settery zeby nie grzebac bezposrednio w zmiennych)
    def set_image_size_label(self, text):
        self.label_image_size.setText(text)

    def set_notification_label(self, text):
        self.label_notification.setText(text)

    # Przesyła współrzędne kliknięcia do funkcji
    def mouse_press_event(self, event: QMouseEvent):
        scene_pos = self.graphics_view.mapToScene(event.pos())

        if self.pixmap_item:
            image_pos = self.pixmap_item.mapFromScene(scene_pos)
            x, y = image_pos.x(), image_pos.y()
            if event.button() == Qt.LeftButton:
                self.presenter.handle_mouse_click(x, y)  # Wywołanie funkcji w prezenterze z współrzędnymi obrazka
            #Przeciąganie po kliknięciu prawego przycisku
            if event.button() == Qt.RightButton:
                self.graphics_view.setCursor(QtCore.Qt.ClosedHandCursor)
                self.is_dragging = True
                self.last_mouse_position = event.pos()

    def mouse_move_event(self, event: QMouseEvent):
        # Obsługuje przeciąganie obrazu, jeśli lewy przycisk myszy jest wciśnięty lub prawy przycisk przy aktywnym narzędziu do rysowania
        self.handle_dragging(event)

        # Zwykłe śledzenie ruchu myszy
        scene_pos = self.graphics_view.mapToScene(event.pos())
        if self.pixmap_item:
            image_pos = self.pixmap_item.mapFromScene(scene_pos)
            x, y = image_pos.x(), image_pos.y()
            self.presenter.handle_mouse_move(x, y)

    def handle_dragging(self, event: QMouseEvent):
        # Sprawdzamy, czy przeciąganie jest aktywne:
        # - Dla lewego przycisku, gdy narzędzie do rysowania jest wyłączone
        # - Dla prawego przycisku, gdy narzędzie do rysowania jest włączone
        if self.is_dragging and event.buttons() == Qt.RightButton:
            # Obliczanie różnicy pozycji kursora od ostatniego ruchu
            delta = event.pos() - self.last_mouse_position
            # Aktualizacja ostatniej pozycji kursora
            self.last_mouse_position = event.pos()

            # Przesunięcie paska przewijania w poziomie
            self.graphics_view.horizontalScrollBar().setValue(
                self.graphics_view.horizontalScrollBar().value() - delta.x()
            )
            # Przesunięcie paska przewijania w pionie
            self.graphics_view.verticalScrollBar().setValue(
                self.graphics_view.verticalScrollBar().value() - delta.y()
            )

    def mouse_release_event(self, event: QMouseEvent):
        # Zakończenie przeciągania po zwolnieniu przycisku myszy
        if event.button() == event.button() == Qt.RightButton:
            self.is_dragging = False
            self.last_mouse_position = None
            if self.presenter.drawing_tool is None:
                self.change_to_arrow_cursor()
            else:
                self.change_to_cross_cursor()

        if event.button() == event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.last_mouse_position = None
            # Testowo, do zmiany : ----------------------------------------------- !!!!!!!!!!!!!!!!!!!!!!!!
            self.presenter.handle_mouse_left_click_release()

    #Zmiana kursora gdy jesteśmy w obszarze obrazka
    def change_to_cross_cursor(self):
        self.graphics_view.setCursor(QtCore.Qt.CrossCursor)

    #Przywrócenie domyślneog kursora
    def change_to_arrow_cursor(self):
        self.graphics_view.setCursor(QtCore.Qt.ArrowCursor)

    #Aktualizacja zooma
    def apply_zooming(self, zoom_value):
        self.graphics_view.resetTransform()
        # Zastosowanie nowego skalowania
        self.graphics_view.scale(zoom_value, zoom_value)

    def set_draw_rectangle_button_text(self, text):
        self.draw_rectangle_button.setText(text)

    def set_draw_polygon_button_text(self, text):
        self.draw_polygon_button.setText(text)

    def set_auto_selection_button_text(self, text):
        self.auto_selection_button.setText(text)

    def key_press_event(self, event):
        try:
            # Obsługa ESC
            if event.key() == Qt.Key_Escape:
                self.presenter.handle_escape_click()

            # Obsługa klawisza Enter
            elif event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.presenter.handle_enter_click()

            # Obsługa Ctrl + / Ctrl -
            elif event.modifiers() == Qt.ControlModifier:  # Check for Ctrl modifier first
                if event.key() == Qt.Key_Minus or event.key() == Qt.Key_Underscore:
                    self.presenter.handle_crtl_minus()
                elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:  # "+" or "="
                    self.presenter.handle_crtl_plus()
        except Exception as e:
            print(f"Error in key_press_event: {e}")

    #Sprawdzenie kierunku przewijania scrolla
    def mouse_wheel_event(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:  # Scroll w górę
                self.presenter.handle_scroll_up()
            elif event.angleDelta().y() < 0:  # Scroll w dół
                self.presenter.handle_scroll_down()

    def set_zoom_slider_visibility(self, visible: bool):
        self.zoom_image_slider.setVisible(visible)
        self.zoom_value_widget.setVisible(visible)

    def get_selected_class(self):
        selected_item = self.class_list_widget.selectedItems()
        if selected_item:
            selected_item = selected_item[0]
            # Pobieramy CustomClassListItemView powiązany z QListWidgetItem
            custom_view = self.class_list_widget.itemWidget(selected_item)
            return custom_view
        return None

    def show_message_OK(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_message_Yes_No(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        yes_button = msg.button(QMessageBox.Yes)
        no_button = msg.button(QMessageBox.No)

        yes_button.setText("Tak")
        no_button.setText("Anuluj")

        response = msg.exec_()
        return response == QMessageBox.Yes

    #Zwraca nazwę aktualnei zaznaczonego obrazka
    def get_selected_image(self):
        selected_item = self.file_list_widget.currentItem()
        if selected_item is not None:
            return selected_item.text()
        return None

    def set_no_active_tool_text(self):
        self.set_notification_label("Brak aktywnego narzędzia do rysowania.")

    def toggle_all_buttons(self, enabled: bool):
        # Iteruj przez wszystkie dzieci centralwidget
        for child in self.centralwidget.findChildren(QtWidgets.QPushButton):
            child.setEnabled(enabled)


        # Obsługa przesuwania obrazu, jeśli kursor jest blisko krawędzi
        # self.handle_edge_scrolling(event.pos())

    # def handle_edge_scrolling(self, cursor_pos):
    #     edge_threshold = 30  # Próg odległości od krawędzi w pikselach
    #     view_rect = self.graphics_view.viewport().rect()
    #
    #     if self.presenter.drawing_tool is not None:
    #         if cursor_pos.x() < edge_threshold:
    #             # Kursor blisko lewej krawędzi
    #             self.graphics_view.horizontalScrollBar().setValue(
    #                 self.graphics_view.horizontalScrollBar().value() - 20
    #             )
    #         elif cursor_pos.x() > view_rect.width() - edge_threshold:
    #             # Kursor blisko prawej krawędzi
    #             self.graphics_view.horizontalScrollBar().setValue(
    #                 self.graphics_view.horizontalScrollBar().value() + 20
    #             )
    #
    #         if cursor_pos.y() < edge_threshold:
    #             # Kursor blisko górnej krawędzi
    #             self.graphics_view.verticalScrollBar().setValue(
    #                 self.graphics_view.verticalScrollBar().value() - 20
    #             )
    #         elif cursor_pos.y() > view_rect.height() - edge_threshold:
    #             # Kursor blisko dolnej krawędzi
    #             self.graphics_view.verticalScrollBar().setValue(
    #                 self.graphics_view.verticalScrollBar().value() + 20
    #             )

