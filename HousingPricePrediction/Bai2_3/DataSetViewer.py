from tkinter import *
from tkinter import ttk
import pandas as pd

class DataSetViewer:
    def __init__(self):
        pass

    def createUI(self):
        self.root = Tk()
        self.root.title("Dataset Viewer - House Pricing Prediction")
        self.root.geometry("800x600")

        main_panel = PanedWindow(self.root)
        main_panel.pack(fill=BOTH, expand=True)

        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                   'Avg. Area Number of Bedrooms', 'Area Population', 'Price')

        self.tree = ttk.Treeview(main_panel, columns=columns, show='headings')

        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor=CENTER)

        scroll = ttk.Scrollbar(main_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

    def show_data_list(self, fileName):
        df = pd.read_csv(fileName)

        # Dọn bảng trước khi chèn mới
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Thêm dữ liệu an toàn bằng iloc
        for i in range(len(df)):
            row = [df.iloc[i][j] for j in range(len(df.columns))]
            self.tree.insert("", END, values=row)

    def show_ui(self):
        self.root.mainloop()
