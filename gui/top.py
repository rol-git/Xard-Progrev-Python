import customtkinter
from tkinter import messagebox
from threading import Thread
from work import arrange_settings


class Top(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(tuple(range(0, 10)), weight=1)
        self.entry_path_label = customtkinter.CTkLabel(
            self,
            text="Путь до аккаунтов:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.entry_path_label.grid(
            row=0,
            column=0,
            padx=30,
            pady=(20, 0),
            sticky="w",
        )

        self.entry_path_field = customtkinter.CTkEntry(
            self, font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.entry_path_field.grid(
            row=1, column=0, padx=30, pady=(0, 20), sticky="nsew")

        self.browse_accs_button = customtkinter.CTkButton(
            self, text="Обзор...", command=self.browse_accs,
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.browse_accs_button.grid(
            row=1, column=1, padx=30, pady=(0, 20), sticky="nsew")

        self.txs_amount_label = customtkinter.CTkLabel(
            self,
            text="Количество транзакций:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.txs_amount_label.grid(
            row=2,
            column=0,
            padx=30,
            sticky="w",
        )

        self.txs_amount_field = customtkinter.CTkEntry(
            self, placeholder_text="(от-до или значение)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.txs_amount_field.grid(row=3, column=0, padx=30,
                                   pady=(0, 20), sticky="nsew")

        self.balance_percent_label = customtkinter.CTkLabel(
            self,
            text="Процент от баланса в свапе:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.balance_percent_label.grid(
            row=2,
            column=1,
            padx=30,
            sticky="w",
        )

        self.balance_percent_field = customtkinter.CTkEntry(
            self, placeholder_text="(от-до или значение, %)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.balance_percent_field.grid(row=3, column=1, padx=30,
                                        pady=(0, 20), sticky="nsew")

        self.tickets_amount_label = customtkinter.CTkLabel(
            self,
            text="Билетов в GrapeDraw:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.tickets_amount_label.grid(
            row=4,
            column=0,
            padx=30,
            sticky="w",
        )

        self.tickets_amount_field = customtkinter.CTkEntry(
            self, placeholder_text="(от-до или значение)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.tickets_amount_field.grid(row=5, column=0, padx=30,
                                       pady=(0, 20), sticky="nsew")

        self.price_impact_label = customtkinter.CTkLabel(
            self,
            text="Максимальный price impact:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.price_impact_label.grid(
            row=4,
            column=1,
            padx=30,
            sticky="w",
        )

        self.price_impact_field = customtkinter.CTkEntry(
            self, placeholder_text="(значение, %)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.price_impact_field.grid(row=5, column=1, padx=30,
                                     pady=(0, 20), sticky="nsew")

        self.delay_label = customtkinter.CTkLabel(
            self,
            text="Секунд между транзакциями:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.delay_label.grid(
            row=6,
            column=0,
            padx=30,
            sticky="w",
        )

        self.delay_field = customtkinter.CTkEntry(
            self, placeholder_text="(от-до или значение)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.delay_field.grid(row=7, column=0, padx=30,
                              pady=(0, 20), sticky="nsew")

        self.timeout_label = customtkinter.CTkLabel(
            self,
            text="Секунд между аккаунтами:",
            anchor="w",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.timeout_label.grid(
            row=6,
            column=1,
            padx=30,
            sticky="w",
        )

        self.timeout_field = customtkinter.CTkEntry(
            self, placeholder_text="(от-до или значение)",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"), width=225)
        self.timeout_field.grid(row=7, column=1, padx=30,
                                pady=(0, 20), sticky="nsew")

        self.shuffle_checkbox = customtkinter.CTkCheckBox(self, text="Перемешивать аккаунты",
                                                          font=customtkinter.CTkFont(
                                                              family="Helvetica, Arial, sans-serif",
                                                              size=13, weight="bold"),
                                                          onvalue="on", offvalue="off")
        self.shuffle_checkbox.grid(row=8, column=0, padx=30, pady=(20, 20), sticky="nsew")

        self.proxy_checkbox = customtkinter.CTkCheckBox(self, text="Использовать proxy",
                                                        font=customtkinter.CTkFont(
                                                            family="Helvetica, Arial, sans-serif",
                                                            size=13, weight="bold"),
                                                        onvalue="on", offvalue="off")
        self.proxy_checkbox.grid(row=8, column=1, padx=30, pady=(20, 20), sticky="nsew")

        self.start_button = customtkinter.CTkButton(
            self, command=self.arrange_settings, text="Начать работу скрипта",
            font=customtkinter.CTkFont(family="Helvetica, Arial, sans-serif", size=13, weight="bold"))
        self.start_button.grid(
            row=9, column=0, padx=30, pady=(20, 20), columnspan=2, sticky="nsew")

    def browse_accs(self):
        filepath = customtkinter.filedialog.askopenfilename()
        if filepath:
            self.entry_path_field.delete(0, "end")
            self.entry_path_field.insert(0, filepath)

    def arrange_settings(self):
        if not self.master.process.is_alive():
            self.master.process = Thread(target=arrange_settings, args=(self.master,), daemon=True)
            self.master.process.start()
        else:
            messagebox.showinfo("Info", "Нужно дождаться конца выполнения предыдущего скрипта перед тем, "
                                        "как запустить новый!")
