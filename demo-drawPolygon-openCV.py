import cv2
import numpy as np

# Lista punktów wielokąta
polygon_points = []
selected_point = None
dragging = False
radius = 10  # Promień obszaru, w którym możemy "chwytać" punkt
polygon_closed = False

# Funkcja do rysowania poligonu i punktów
def draw_polygon(image):
    temp_image = image.copy()
    if len(polygon_points) > 1:
        # Rysujemy linie między punktami
        cv2.polylines(temp_image, [np.array(polygon_points)], isClosed=polygon_closed, color=(0, 255, 0), thickness=2)
    # Rysujemy wszystkie punkty
    for point in polygon_points:
        cv2.circle(temp_image, point, radius, (0, 0, 255), -1)
    return temp_image

# Funkcja do sprawdzania, czy kliknięto w pobliżu krawędzi
def is_point_on_edge(x, y):
    if not polygon_closed:
        return None  # Poligon nie jest zamknięty, nie sprawdzamy krawędzi

    for i in range(len(polygon_points)):
        # Indeks następnego punktu (jeśli poligon zamknięty, ostatni łączy się z pierwszym)
        next_i = (i + 1) % len(polygon_points)

        # Sprawdzamy, czy kliknięto w pobliżu krawędzi (odcinka między dwoma punktami)
        pt1 = np.array(polygon_points[i])
        pt2 = np.array(polygon_points[next_i])
        dist = np.abs(np.cross(pt2 - pt1, np.array([x, y]) - pt1) / np.linalg.norm(pt2 - pt1))

        if dist < radius:
            # Sprawdzamy, czy kliknięto "pomiędzy" dwoma wierzchołkami (na odcinku)
            if min(pt1[0], pt2[0]) <= x <= max(pt1[0], pt2[0]) and min(pt1[1], pt2[1]) <= y <= max(pt1[1], pt2[1]):
                return i, next_i  # Zwracamy indeksy punktów tworzących tę krawędź
    return None

# Funkcja obsługi myszy
def mouse_callback(event, x, y, flags, param):
    global selected_point, dragging, polygon_points, polygon_closed

    if event == cv2.EVENT_LBUTTONDOWN:
        # Sprawdzamy, czy kliknięto w pobliżu pierwszego wierzchołka (zamknięcie poligonu)
        if not polygon_closed and len(polygon_points) > 2 and np.linalg.norm(np.array(polygon_points[0]) - np.array((x, y))) < radius:
            polygon_closed = True
        else:
            # Sprawdzamy, czy kliknięto w pobliżu istniejącego wierzchołka (przesuwanie)
            for i, point in enumerate(polygon_points):
                if np.linalg.norm(np.array(point) - np.array((x, y))) < radius:
                    selected_point = i
                    dragging = True
                    break
            # Jeśli poligon jest zamknięty, sprawdzamy, czy kliknięto na krawędź
            if not dragging and polygon_closed:
                edge = is_point_on_edge(x, y)
                if edge:
                    # Wstawiamy nowy punkt w miejscu kliknięcia na krawędzi
                    i, next_i = edge
                    new_point = (x, y)  # Tworzymy punkt dokładnie w miejscu kliknięcia
                    polygon_points.insert(next_i, new_point)
            # Jeżeli nie kliknięto w żaden wierzchołek ani krawędź, dodajemy nowy punkt (jeśli poligon nie jest zamknięty)
            if not dragging and not polygon_closed:
                polygon_points.append((x, y))

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        # Przesuwamy wybrany wierzchołek w nowe miejsce
        polygon_points[selected_point] = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        # Zwalniamy wybrany punkt
        dragging = False
        selected_point = None

# Tworzymy pusty obraz
image = np.ones((500, 500, 3), dtype='uint8') * 255

# Ustawiamy okno i funkcję obsługi myszy
cv2.namedWindow("Polygon Drawer")
cv2.setMouseCallback("Polygon Drawer", mouse_callback)

while True:
    # Wyświetlamy obraz z poligonem
    temp_image = draw_polygon(image)
    cv2.imshow("Polygon Drawer", temp_image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Przerwanie po naciśnięciu 'q'
        break

cv2.destroyAllWindows()
