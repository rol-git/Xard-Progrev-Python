import customtkinter


class Bottom(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((tuple(range(0, 9))), weight=1)
        self.zksync_label = customtkinter.CTkLabel(
            self,
            text="ZkSync:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"),
            width=120
        )
        self.zksync_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="w",
        )

        self.zksync_dex_checkboxes = []

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Grape (Lottery)",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=1, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Dmail",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=1, column=1, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="ZkStars (NFT Mint)",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=1, column=2, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Izumi",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=2, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="WooFi",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=2, column=1, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Maverick",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=2, column=2, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="SyncSwap",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=3, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.zksync_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="SpaceFi",
                                                                    font=customtkinter.CTkFont(
                                                                        family="Helvetica, Arial, sans-serif",
                                                                        size=13, weight="bold"),
                                                                    onvalue="on",
                                                                    offvalue="off"))
        self.zksync_dex_checkboxes[-1].grid(row=3, column=1, padx=35, pady=(0, 20), sticky="nsew")

        self.base_label = customtkinter.CTkLabel(
            self,
            text="Base:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"),
            width=120
        )
        self.base_label.grid(
            row=5,
            column=0,
            pady=(0, 10),
            padx=20,
            sticky="w",
        )

        self.base_dex_checkboxes = []

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Grape (Lottery)",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=6, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Dmail",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=6, column=1, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="ZkStars (NFT Mint)",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=6, column=2, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Izumi",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=7, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="WooFi",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=7, column=1, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Maverick",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=7, column=2, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="Uniswap",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=8, column=0, padx=35, pady=(0, 20), sticky="nsew")

        self.base_dex_checkboxes.append(customtkinter.CTkCheckBox(self, text="PancakeSwap",
                                                                  font=customtkinter.CTkFont(
                                                                      family="Helvetica, Arial, sans-serif",
                                                                      size=13, weight="bold"),
                                                                  onvalue="on",
                                                                  offvalue="off"))
        self.base_dex_checkboxes[-1].grid(row=8, column=1, padx=35, pady=(0, 20), sticky="nsew")
