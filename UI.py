import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import os
from PIL import Image, ImageTk
import HandTrackingModule as htm


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (GuidePage, StartPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class ListImgPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.buttonFrame = tk.Frame(self)
        # self.buttonFrame.grid(row=1, column=0, sticky='nsew')
        # button1 = ttk.Button(self.buttonFrame, text="Hướng dẫn",
        #                      command=lambda: controller.show_frame(GuidePage))
        # button1.grid(row=1, column=0)
        # button2 = ttk.Button(self, text="SetUp", command=lambda: controller.show_frame(StartPage))
        # button2.grid(row=1, column=0)
        # canvas = tk.Canvas(self, width=640, height=480, bg="blue")
        # canvas.grid(row=0, column=0, sticky="nsew")
        # path = "FingerImage"
        # for name in os.listdir(path):
        #     print(name)
        # img = ImageTk.PhotoImage(Image.open(path))
        # canvas.create_image(30, 50, image=img)


class GuidePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label0 = ttk.Label(self, text="Nắm bàn tay tương ứng với số 0", font=("Courier", 18))
        label0.place(x=0, y=0)
        label1 = ttk.Label(self, text="Ngón tay cái tương ứng với số 1", font=("Courier", 18))
        label1.place(x=0, y=30)
        label2 = ttk.Label(self, text="Ngón trỏ tương ứng với số 2", font=("Courier", 18))
        label2.place(x=0, y=60)
        label3 = ttk.Label(self, text="Ngón giữa tương ứng với số 4", font=("Courier", 18))
        label3.place(x=0, y=90)
        label4 = ttk.Label(self, text="Ngón áp út tương ứng với số 8", font=("Courier", 18))
        label4.place(x=0, y=120)
        label5 = ttk.Label(self, text="Ngón tay út tương ứng với số 16", font=("Courier", 18))
        label5.place(x=0, y=150)
        label6 = ttk.Label(self, text="Kết hợp các ngón tay để tạo thành số khác", font=("Courier", 18))
        label6.place(x=0, y=180)
        label7 = ttk.Label(self, text="nhau. Ví dụ số 14 là kết hợp của ngón trỏ", font=("Courier", 18))
        label7.place(x=0, y=210)
        label8 = ttk.Label(self, text="+ ngón giữa + ngón áp út", font=("Courier", 18))
        label8.place(x=0, y=240)
        label9 = ttk.Label(self, text="Để thiết lập hình ảnh tương ứng với ngón tay", font=("Courier", 18))
        label9.place(x=0, y=270)
        label10 = ttk.Label(self, text="xin vui lòng vào mục SetUp", font=("Courier", 18))
        label10.place(x=0, y=300)
        label11 = ttk.Label(self, text="Chương trình cho phép điều khiển tối đa", font=("Courier", 18))
        label11.place(x=0, y=330)
        label12 = ttk.Label(self, text="32 thiết bị khác nhau", font=("Courier", 18))
        label12.place(x=0, y=360)
        # button1 = ttk.Button(self, text="Hiển thị các hành động đã chọn",
        #                      command=lambda: controller.show_frame(ListImgPage))
        # button1.grid(row=1, column=1, padx=100, pady=480)
        button2 = ttk.Button(self, text="SetUp", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=1, column=2, padx=0, pady=480)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.cameraFrame = tk.Frame(self, bg="gray")
        self.cameraFrame.grid(row=0, column=0, sticky="nsew")

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=1, column=0, sticky='nsew')

        self.button1 = tk.Button(self.buttonFrame, text="Hướng dẫn",
                                 command=lambda: controller.show_frame(GuidePage))
        self.button1.grid(row=1, column=0, padx=50)

        # self.button2 = tk.Button(self.buttonFrame, text="Hiển thị các hành động đã chọn",
        #                          command=lambda: controller.show_frame(ListImgPage))
        # self.button2.grid(row=1, column=1, padx=10)

        self.path = ""

        def UploadAction():
            filename = filedialog.askopenfilename()
            self.path = filename
            self.button4 = tk.Button(self.buttonFrame, text="Save Image", command=save)
            self.button4.grid(row=1, column=3, padx=30, sticky='nsew')

        self.button3 = tk.Button(self.buttonFrame, text="Chọn file ảnh", command=UploadAction)
        self.button3.grid(row=1, column=2, sticky='nsew')

        wCam, hCam = 640, 480
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        self.lmain = tk.Label(self.cameraFrame)
        self.lmain.pack()

        detector = htm.handDetector(detectionCon=0.75)
        fingers_idx = [[17, 1, 2, 3, 4],
                       [0, 5, 6, 7, 8],
                       [0, 9, 10, 11, 12],
                       [0, 13, 14, 15, 16],
                       [0, 17, 18, 19, 20]]

        def is_obtuse(p1, p2, p3):
            v1 = [p1[1] - p2[1], p1[2] - p2[2]]
            v2 = [p3[1] - p2[1], p3[2] - p2[2]]
            return (v1[0] * v2[0] + v1[1] * v2[1]) < 0

        self.num = 0

        def show_cam2():
            success, cam = cap.read()
            cam = cv2.flip(cam, 1)
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
            img = detector.findHands(cam)

            lmList = detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                fingers = []
                for ids in fingers_idx:
                    if is_obtuse(lmList[ids[0]], lmList[ids[2]], lmList[ids[4]]):
                        fingers.append(1)
                    else:
                        fingers.append(0)

                res = int("".join(str(x) for x in reversed(fingers)), 2)
                folderPath = "FingerImage"
                imPath = str(res) + ".jpg"

                if os.path.exists(folderPath + "/" + imPath):
                    img[0:130, 510:600] = cv2.imread(f'{folderPath}/{imPath}')
                self.num = res
                if self.path:
                    img[0:130, 0:90] = cv2.imread(self.path)

                cv2.rectangle(img, (20, 225), (260, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(res), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 25)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
            self.lmain.after(1, show_cam2)

        show_cam2()

        def save():
            image = Image.open(self.path)
            resize_image = image.resize((90, 130))
            path = "C:\\Users\\Nguyen Van Huy\\Downloads\\" + str(self.num) + ".jpg"
            resize_image.save(path)
            print(path)
            self.path = ""


win = tkinterApp()
win.geometry("640x510")
win.mainloop()