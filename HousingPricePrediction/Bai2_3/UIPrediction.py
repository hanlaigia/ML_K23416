from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
from tkinter import filedialog as fd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import os
from datetime import datetime
import pickle

from DataSetViewer import DataSetViewer
from FileUtil import FileUtil


class UIPrediction:
    fileName = ""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # thư mục HousingPricePrediction
        self.dataset_dir = os.path.join(self.base_dir, "dataset")
        self.default_dataset = os.path.join(self.dataset_dir, "USA_Housing.csv")
        self.model_dir = os.path.join(self.base_dir, "Bai2_3")  # nơi lưu các model .zip/.pkl

    def create_ui(self):
        self.root = Tk()
        self.root.title("House Pricing Prediction - Faculty of Information Systems")
        self.root.geometry("1500x850")

        main_panel = PanedWindow(self.root)
        main_panel["bg"] = "yellow"
        main_panel.pack(fill=BOTH, expand=True)

        # --- Top Panel ---
        top_panel = PanedWindow(main_panel, height=80)
        top_panel["bg"] = "blue"
        main_panel.add(top_panel)
        top_panel.pack(fill=X, side=TOP, expand=False)

        font = Font(family="tahoma", size=18)
        title_label = Label(top_panel, text="House Pricing Prediction", font=font)
        title_label["bg"] = "yellow"
        top_panel.add(title_label)

        # --- Center Panel ---
        center_panel = PanedWindow(main_panel)
        main_panel.add(center_panel)
        center_panel["bg"] = "pink"
        center_panel.pack(fill=BOTH, expand=True)

        # --- Choose Dataset ---
        choose_dataset_panel = PanedWindow(center_panel, height=30)
        choose_dataset_panel["bg"] = "orange"
        center_panel.add(choose_dataset_panel)
        choose_dataset_panel.pack(fill=X)

        dataset_label = Label(choose_dataset_panel, text="Select Dataset:")
        self.selectedFileName = StringVar()
        self.selectedFileName.set(self.default_dataset)
        self.choose_dataset_entry = Entry(choose_dataset_panel, textvariable=self.selectedFileName)
        self.choose_dataset_button = Button(choose_dataset_panel, text="1. Pick Dataset", width=18,
                                            command=self.do_pick_data)
        self.view_dataset_button = Button(choose_dataset_panel, text="2. View Dataset", width=20,
                                          command=self.do_view_dataset)

        choose_dataset_panel.add(dataset_label)
        choose_dataset_panel.add(self.choose_dataset_entry)
        choose_dataset_panel.add(self.choose_dataset_button)
        choose_dataset_panel.add(self.view_dataset_button)

        # --- Training Rate ---
        training_rate_panel = PanedWindow(center_panel, height=30)
        center_panel.add(training_rate_panel)
        training_rate_panel.pack(fill=X)

        training_rate_label = Label(training_rate_panel, text="Training Rate:")
        self.training_rate = IntVar()
        self.training_rate.set(80)
        self.training_rate_entry = Entry(training_rate_panel, textvariable=self.training_rate, width=20)
        percent_label = Label(training_rate_panel, text="%", width=10, anchor="w", justify=LEFT)
        self.train_model_button = Button(training_rate_panel, text="3. Train Model", width=20, command=self.do_train)
        self.evaluate_model_button = Button(training_rate_panel, text="4. Evaluate Model", width=20,
                                            command=self.do_evaluation)

        training_rate_panel.add(training_rate_label)
        training_rate_panel.add(self.training_rate_entry)
        training_rate_panel.add(percent_label)
        training_rate_panel.add(self.train_model_button)
        training_rate_panel.add(self.evaluate_model_button)

        self.status = StringVar()
        self.status.set("")
        self.train_model_result_label = Label(training_rate_panel, textvariable=self.status)
        training_rate_panel.add(self.train_model_result_label)

        # --- Evaluation Table ---
        evaluate_panel = PanedWindow(center_panel, height=400)
        center_panel.add(evaluate_panel)
        evaluate_panel.pack(fill=X)

        table_evaluate_panel = PanedWindow(evaluate_panel, height=400)
        evaluate_panel.add(table_evaluate_panel)

        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                   'Avg. Area Number of Bedrooms', 'Area Population', 'Original Price', 'Prediction Price')

        self.tree = ttk.Treeview(table_evaluate_panel, columns=columns, show='headings')
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor=CENTER, stretch=NO, width=120)

        scrollBar = ttk.Scrollbar(table_evaluate_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollBar.set)
        scrollBar.pack(side=RIGHT, fill=BOTH, expand=True)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # --- Coefficient Panel ---
        coefficient_panel = PanedWindow(evaluate_panel)
        coefficient_panel["bg"] = "pink"
        evaluate_panel.add(coefficient_panel)

        coefficient_detail_label = Label(coefficient_panel, text="Coefficient:")
        coefficient_detail_label.pack(side=TOP, fill=X, expand=False)

        coefficient_detail_panel = PanedWindow(coefficient_panel, height=120)
        coefficient_panel.add(coefficient_detail_panel)

        self.coefficient_detail_text = Text(coefficient_detail_panel, height=12, width=50)
        scroll = Scrollbar(coefficient_detail_panel)
        self.coefficient_detail_text.configure(yscrollcommand=scroll.set)
        self.coefficient_detail_text.pack(side=LEFT, expand=False, fill=X)
        scroll.config(command=self.coefficient_detail_text.yview)
        scroll.pack(side=RIGHT, fill=Y, expand=True)

        # --- Metric Panel ---
        metric_panel = PanedWindow(coefficient_panel, height=30)
        coefficient_panel.add(metric_panel)
        metric_panel.pack(side=TOP, fill=BOTH, expand=True)

        self.mae_value = DoubleVar()
        mae_label = Label(metric_panel, text="Mean Absolute Error (MAE):")
        mae_label.grid(row=0, column=0)
        mae_entry = Entry(metric_panel, text="", width=20, textvariable=self.mae_value)
        mae_entry.grid(row=0, column=1)

        self.mse_value = DoubleVar()
        mse_label = Label(metric_panel, text="Mean Square Error (MSE):")
        mse_label.grid(row=1, column=0)
        mse_entry = Entry(metric_panel, text="", width=20, textvariable=self.mse_value)
        mse_entry.grid(row=1, column=1)

        self.rmse_value = DoubleVar()
        rmse_label = Label(metric_panel, text="Root Mean Square Error (RMSE):")
        rmse_label.grid(row=2, column=0)
        rmse_entry = Entry(metric_panel, text="", width=20, textvariable=self.rmse_value)
        rmse_entry.grid(row=2, column=1)

        savemodel_button = Button(metric_panel, text="5. Save Model", width=20, command=self.do_save_model)
        savemodel_button.grid(row=3, column=1)

        # --- Load Model Button ---
        loadmodel_panel = PanedWindow(center_panel, height=40)
        loadmodel_panel["bg"] = "yellow"
        center_panel.add(loadmodel_panel)
        loadmodel_panel.pack(fill=X, side=TOP)

        loadmodel_button = Button(loadmodel_panel, text="6. Load Model", command=self.do_load_model)
        loadmodel_button.pack(side=LEFT, padx=5)

        # --- Input Prediction ---
        input_prediction_panel = PanedWindow(center_panel)
        input_prediction_panel.pack(fill=BOTH, side=TOP, expand=True)

        labels = ["Avg. Area Income", "Avg. Area House Age", "Avg. Area Number of Rooms",
                  "Avg. Area Number of Bedrooms", "Area Population"]
        self.input_vars = [DoubleVar() for _ in labels]

        for i, label_text in enumerate(labels):
            lbl = Label(input_prediction_panel, text=f"{label_text}:")
            lbl.grid(row=i, column=0)
            entry = Entry(input_prediction_panel, width=40, textvariable=self.input_vars[i])
            entry.grid(row=i, column=1)

        prediction_button = Button(input_prediction_panel, text="7. Prediction House Pricing",
                                   command=self.do_prediction)
        prediction_button.grid(row=6, column=0)

        prediction_price_label = Label(input_prediction_panel, text="Prediction Price:")
        prediction_price_label.grid(row=6, column=1)
        self.prediction_price_value = DoubleVar()
        prediction_price_entry = Entry(input_prediction_panel, width=40, textvariable=self.prediction_price_value)
        prediction_price_entry.grid(row=6, column=2)

        # --- Footer ---
        designedby_panel = PanedWindow(main_panel, height=20)
        designedby_panel["bg"] = "cyan"
        main_panel.add(designedby_panel)
        designedby_panel.pack(fill=BOTH, side=BOTTOM)
        designedby_label = Label(designedby_panel, text="Designed by: Tran Duy Thanh")
        designedby_label["bg"] = "cyan"
        designedby_label.pack(side=LEFT)

    def show_ui(self):
        self.root.mainloop()

    def do_pick_data(self):
        filetypes = (("Dataset CSV", "*.csv"), ("All Files", "*.*"))
        s = fd.askopenfilename(title="Choose dataset", initialdir="./", filetypes=filetypes)
        self.selectedFileName.set(s)

    def do_view_dataset(self):
        viewer = DataSetViewer()
        viewer.createUI()
        viewer.show_data_list(self.selectedFileName.get())
        viewer.show_ui()

    def do_train(self):
        ratio = self.training_rate.get() / 100
        self.df = pd.read_csv(self.selectedFileName.get())

        self.X = self.df[['Avg. Area Income', 'Avg. Area House Age',
                          'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms',
                          'Area Population']]
        self.y = self.df['Price']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=1 - ratio, random_state=101)

        self.lm = LinearRegression()
        self.lm.fit(self.X_train, self.y_train)
        self.status.set("Training finished")
        messagebox.showinfo("info", "Training is finished")

    def do_evaluation(self):
        self.coefficient_detail_text.delete(1.0, END)
        self.coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
        self.coefficient_detail_text.insert(END, str(self.coeff_df))

        predictions = self.lm.predict(self.X_test)
        y_test_array = np.asarray(self.y_test)

        for i in range(len(self.X_test)):
            values = [self.X_test.iloc[i][0], self.X_test.iloc[i][1], self.X_test.iloc[i][2],
                      self.X_test.iloc[i][3], self.X_test.iloc[i][4], y_test_array[i], predictions[i]]
            self.tree.insert('', END, values=values)

        self.mae_value.set(metrics.mean_absolute_error(self.y_test, predictions))
        self.mse_value.set(metrics.mean_squared_error(self.y_test, predictions))
        self.rmse_value.set(np.sqrt(metrics.mean_squared_error(self.y_test, predictions)))

        self.status.set("Evaluation is finished")
        messagebox.showinfo("info", "Evaluation is finished")

    def do_save_model(self):
        if not hasattr(self, 'lm'):
            messagebox.showerror("Error", "Please train the model first!")
            return

        confirm = messagebox.askyesno("Confirm Save", "Do you want to save this model?")
        if not confirm:
            return

        filename = datetime.now().strftime("model_%Y%m%d_%H%M%S.pkl")
        path = os.path.join(self.model_dir, filename)

        with open(path, "wb") as f:
            pickle.dump(self.lm, f)

        messagebox.showinfo("info", f"Model saved successfully as {filename}")

    def do_load_model(self):
        files = [f for f in os.listdir(self.model_dir) if f.endswith(".pkl")]
        if not files:
            messagebox.showerror("Error", "No model to load!")
            return

        popup = Toplevel(self.root)
        popup.title("Select a model to load")
        popup.geometry("300x150")

        Label(popup, text="Choose a model:").pack(pady=10)
        model_var = StringVar()
        model_var.set(files[0])
        dropdown = OptionMenu(popup, model_var, *files)
        dropdown.pack(pady=5)

        def confirm_load():
            selected = model_var.get()
            path = os.path.join(self.model_dir, selected)
            with open(path, "rb") as f:
                self.lm = pickle.load(f)
            popup.destroy()
            messagebox.showinfo("info", f"Loaded model: {selected}")

        Button(popup, text="OK", command=confirm_load).pack(pady=10)

    def do_prediction(self):
        result = self.lm.predict([[v.get() for v in self.input_vars]])
        self.prediction_price_value.set(result[0])
