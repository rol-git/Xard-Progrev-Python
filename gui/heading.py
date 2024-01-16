import customtkinter


class Heading(customtkinter.CTkLabel):
    def __init__(
            self,
            master,
            **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
