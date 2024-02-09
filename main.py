from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading


peaje = ""
class VentanaDePeaje:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.tarifa = ""
        self.clase = ""

        self.root.geometry("480x480")

        texto_clase = "Clase: {}".format(self.clase)
        self.etiqueta_clase = tk.Label(root, text=texto_clase, font=("Arial", 16, "bold"))
        self.etiqueta_clase.place(x=200, y=10)

        texto_cuota = "Cuota:"
        self.etiqueta_cuota = tk.Label(root, text=texto_cuota, font=("Arial", 20, "bold"))
        self.etiqueta_cuota.place(x=90, y=160)

        texto_peaje = "${} ".format(self.tarifa)
        self.etiqueta_peaje = tk.Label(root, text=texto_peaje, font=("Arial", 90, "bold"))
        self.etiqueta_peaje.place(x=90, y=200)

        self.actualizar_etiquetas()

    def actualizar_etiquetas(self):

        if str(peaje) == "car":
            self.tarifa = 120
            self.clase = "Vehículo ligero"

        elif str(peaje) == "motorcycle":
            self.tarifa = 74
            self.clase = "Motocicleta"

        elif str(peaje) == "truck":
            self.tarifa = 182
            self.clase = "Camión"

        elif str(peaje) == "bus":
            self.tarifa = 164
            self.clase = "Autobús"

        print("this is te final value of Peaje: {}<------".format(str(peaje)))

        if str(peaje) !="NA":
            # Actualiza el texto de las etiquetas
            texto_peaje = "${}".format(self.tarifa)
            self.etiqueta_peaje.config(text=texto_peaje)
            texto_clase = "Clase: {}".format(self.clase)
            self.etiqueta_clase.config(text=texto_clase)
        else:
            # Actualiza el texto de las etiquetas
            texto_peaje = "Alto"
            self.etiqueta_peaje.config(text=texto_peaje)
            texto_clase = "N/A"
            self.etiqueta_clase.config(text=texto_clase)

        # Programa la próxima actualización
        self.root.after(2000, self.actualizar_etiquetas)

class VentanaDeTarifas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarifa")
        y_bar = 80
        cons_x = 370

        self.root.geometry("530x800")

        self.imagen = self.cargar_imagen("v_class.png")

        self.etiqueta_imagen = tk.Label(self.root, image=self.imagen)
        self.etiqueta_imagen.place(x=0 , y= 100)

        texto_desc = "Clases de vehículos:"
        self.texto_desc = tk.Label(root, text=texto_desc, font=("Arial", 16, "bold"))
        self.texto_desc.place(x=180, y=20)

        texto_tarifas = "Tarifas"
        self.texto_tarifas = tk.Label(root, text=texto_tarifas, font=("Arial", 14, "bold"))
        self.texto_tarifas.place(x=340, y=y_bar)

        texto_tarifa_pesado = "$ 198"
        self.texto_tarifa_pesado = tk.Label(root, text=texto_tarifa_pesado, font=("Arial", 20, "bold"))
        self.texto_tarifa_pesado.place(x=cons_x, y=y_bar + 60)

        texto_tarifa__semipesado = "$ 174"
        self.texto_tarifa__semipesado = tk.Label(root, text=texto_tarifa__semipesado, font=("Arial", 20, "bold"))
        self.texto_tarifa__semipesado.place(x=cons_x, y=y_bar + 170 )

        texto_tarifa_carga = "$ 144"
        self.texto_tarifa_carga = tk.Label(root, text=texto_tarifa_carga, font=("Arial", 20, "bold"))
        self.texto_tarifa_carga.place(x=cons_x, y=y_bar + 270 )

        texto_tarifa_autobus = "$ 164"
        self.texto_tarifa_autobus = tk.Label(root, text=texto_tarifa_autobus, font=("Arial", 20, "bold"))
        self.texto_tarifa_autobus.place(x=cons_x, y=y_bar + 380 )

        texto_tarifa_ligero = "$ 120"
        self.texto_tarifa_ligero = tk.Label(root, text=texto_tarifa_ligero, font=("Arial", 20, "bold"))
        self.texto_tarifa_ligero.place(x=cons_x, y=y_bar + 460 )

        texto_tarifa_moto = "$ 74"
        self.texto_tarifa_moto = tk.Label(root, text=texto_tarifa_moto, font=("Arial", 20, "bold"))
        self.texto_tarifa_moto.place(x=cons_x, y=y_bar + 540 )

    def cargar_imagen(self, nombre_archivo):
        imagen = Image.open(nombre_archivo)
        imagen = ImageTk.PhotoImage(imagen)
        return imagen

def detection():
    global peaje

    model = YOLO('yolov8n.pt')
    video_path = './test3.mp4'
    cap = cv2.VideoCapture(video_path)

    target_width = 1280
    target_height = 720

    ret = True
    while ret:
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (target_width, target_height))

            # roi test3 (ROI)
            roi = frame[410: 720, 650:1200]

            # roi test4 (ROI)
            #roi = frame[160: 720, 430:1000]

            # roi gta4_test (ROI)
            #roi = frame[160: 720, 100:900]

            results = model.track(roi, persist=False, classes=[2, 3, 5, 7])

            names = model.names
            for r in results:
                for c in r.boxes.cls:
                    peaje = names[int(c)]
                    print(peaje)


            frame_ = results[0].plot()
            cv2.imshow('Roi', frame_)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def main():
    root1 = tk.Tk()
    app1 = VentanaDeTarifas(root1)
    root1.mainloop()
def main_2():
    root2 = tk.Tk()
    app2 = VentanaDePeaje(root2, "Ventana 2")
    root2.mainloop()

if __name__ == "__main__":
    detection_thread = threading.Thread(target=detection)
    gui_thread1 = threading.Thread(target=main)
    gui_thread2 = threading.Thread(target=main_2)

    detection_thread.start()
    gui_thread1.start()
    gui_thread2.start()