import customtkinter
from tkintermapview import TkinterMapView
from tkinter import filedialog
import os.path
from convert import import_data


customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "TkinterMapView with CustomTkinter"
    WIDTH = 2000
    HEIGHT = 900

    # Render the main frame with map and left side buttons
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1,
                              pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(50, weight=5)

        # ========== Browse buttons ===============
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Upload vector folder",
                                                width=250,
                                                command=self.add)
        self.button_1.grid(pady=(10, 15), padx=(0, 0), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Upload vector file",
                                                width=250,
                                                command=lambda: self.browse_file("file"))
        self.button_2.grid(pady=(10, 15), padx=(10, 50), row=0, column=1)

        # ========== Browse buttons ===============

        # ========== Map tile select ===============
        self.map_label = customtkinter.CTkLabel(
            self.frame_left, text="Tile Server:", font=('arial', 20), anchor="w")
        self.map_label.grid(row=80, column=0, padx=(5, 0), pady=(0, 0))

        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                           command=self.change_map)
        self.map_option_menu.grid(
            row=80, column=1, padx=(5, 0), pady=(0, 0))
        # ========== Map tile select ===============

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0,
                             columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        # Set default values
        self.map_widget.set_address("Paris")
        self.map_option_menu.set("OpenStreetMap")

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def browse_file(self, path):
        # Ask the user to select files or folders
        if path == "folder":
            selected_path = filedialog.askdirectory(title="Select Folder")
        elif path == "file":
            selected_path = filedialog.askopenfilenames(
                title="Select File(s)", filetypes=(("All Files", ".*"),))

        i = 1
        self.loaded_layers = []
        for filename in selected_path:
            self.loaded_layers.append(import_data(filename))
            # Get file name and extension
            extracted_filename, file_extension = os.path.splitext(
                os.path.basename(filename))

            # set label
            new_label = customtkinter.CTkLabel(
                self.frame_left, text=extracted_filename + file_extension, font=('arial', 18))
            new_label.grid(row=i, column=0, columnspan=3, sticky="w")
            # Set checkbox to display layer on the map
            check_var = customtkinter.StringVar(value="on")
            checkbox = customtkinter.CTkCheckBox(self.frame_left, checkbox_height=18, text="Map display",
                                                 variable=check_var, onvalue="on", offvalue="off")
            checkbox.grid(row=i, column=1)
            i += 1

        exterior_coords = self.loaded_layers[0].iloc[0]["geometry"].exterior.coords
        corrected_coords = [(lon, lat) for lat, lon in exterior_coords]

        # Assign the corrected coordinates back to self.test as a list
        self.test = list(corrected_coords)

    def add(self):
        poly = self.map_widget.set_polygon(self.test,

                                           outline_color="red",
                                           border_width=2,

                                           name="switzerland_polygon")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


app = App()
app.start()
