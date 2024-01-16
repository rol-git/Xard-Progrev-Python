import customtkinter
import datetime
import logging
import json as js
from threading import Thread
from .top import Top
from .bottom import Bottom
from .console import Console
from .heading import Heading
from utils.log import log


class MyFormatter(logging.Formatter):
    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%d.%m.%Y %H:%M:%S")
        return s


class MyHandlerText(logging.StreamHandler):
    def __init__(self, console):
        logging.StreamHandler.__init__(self)
        self.console = console

    def emit(self, record):
        msg = self.format(record)
        self.console.configure(state="normal")
        fully_scrolled_down = self.console.yview()[1] == 1
        self.console.insert("end", msg + "\n")
        self.flush()
        if fully_scrolled_down:
            self.console.see("end")
        self.console.configure(state="disabled")


class App(customtkinter.CTk):
    def __init__(self, log):
        super().__init__()
        self.log = log
        self.process = Thread()
        self.title("ultimate zksync/base dao")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.resizable(width=False, height=False)
        self.settings_heading = Heading(master=self, text="Настройки",
                                        font=customtkinter.CTkFont("Helvetica, Arial, sans-serif", 13, "bold"),
                                        bg_color="#1F6AA5")
        self.settings_heading.grid(row=0, column=0, padx=(10, 5), sticky="new")
        self.top = Top(master=self, corner_radius=0)
        self.top.grid(row=1, column=0, padx=(10, 5), pady=(0, 5), sticky="nsew")
        self.bottom = Bottom(master=self, corner_radius=0)
        self.bottom.grid(row=2, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")
        self.console_heading = Heading(master=self, text="Логи",
                                       font=customtkinter.CTkFont("Helvetica, Arial, sans-serif", 13, "bold"),
                                       bg_color="#1F6AA5")
        self.console_heading.grid(row=0, column=1, padx=(5, 10), sticky="new")
        self.console = Console(master=self, state="disabled", corner_radius=0, fg_color="gray17",
                               font=customtkinter.CTkFont("Helvetica, Arial, sans-serif", 13, "bold"),
                               wrap="word", padx=10, pady=10)
        self.console.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), rowspan=2, sticky="nsew")

    def process_opening(self):
        try:
            with open("files/config.json", encoding="utf-8") as f:
                config = js.load(f)
                if "entry_path" in config and config["entry_path"]:
                    self.top.entry_path_field.insert(0, config["entry_path"])
                if "txs_amount" in config and config["txs_amount"]:
                    self.top.txs_amount_field.insert(0, config["txs_amount"])
                if "tickets_amount" in config and config["tickets_amount"]:
                    self.top.tickets_amount_field.insert(0, config["tickets_amount"])
                if "balance_percent" in config and config["balance_percent"]:
                    self.top.balance_percent_field.insert(0, config["balance_percent"])
                if "max_price_impact" in config and config["max_price_impact"]:
                    self.top.price_impact_field.insert(0, config["max_price_impact"])
                if "delay" in config and config["delay"]:
                    self.top.delay_field.insert(0, config["delay"])
                if "timeout" in config and config["timeout"]:
                    self.top.timeout_field.insert(0, config["timeout"])
                if "shuffle" in config:
                    if config["shuffle"] == "on":
                        self.top.shuffle_checkbox.select()
                    elif config["shuffle"] == "off":
                        self.top.shuffle_checkbox.deselect()
                if "proxy" in config:
                    if config["proxy"] == "on":
                        self.top.proxy_checkbox.select()
                    elif config["proxy"] == "off":
                        self.top.proxy_checkbox.deselect()
                if isinstance(config["zksync_dex"], list) and len(config["zksync_dex"]) == \
                        len(self.bottom.zksync_dex_checkboxes):
                    for i in range(len(config["zksync_dex"])):
                        if config["zksync_dex"][i] == "on":
                            self.bottom.zksync_dex_checkboxes[i].select()
                        elif config["zksync_dex"][i] == "off":
                            self.bottom.zksync_dex_checkboxes[i].deselect()
                if isinstance(config["base_dex"], list) and len(config["base_dex"]) == \
                        len(self.bottom.base_dex_checkboxes):
                    for i in range(len(config["base_dex"])):
                        if config["base_dex"][i] == "on":
                            self.bottom.base_dex_checkboxes[i].select()
                        elif config["base_dex"][i] == "off":
                            self.bottom.base_dex_checkboxes[i].deselect()

        except Exception:
            pass

    def process_closing(self):
        config = {
            "entry_path": self.top.entry_path_field.get(),
            "txs_amount": self.top.txs_amount_field.get(),
            "tickets_amount": self.top.tickets_amount_field.get(),
            "balance_percent": self.top.balance_percent_field.get(),
            "max_price_impact": self.top.price_impact_field.get(),
            "delay": self.top.delay_field.get(),
            "timeout": self.top.timeout_field.get(),
            "shuffle": self.top.shuffle_checkbox.get(),
            "proxy": self.top.proxy_checkbox.get(),
            "zksync_dex": [checkbox.get() for checkbox in self.bottom.zksync_dex_checkboxes],
            "base_dex": [checkbox.get() for checkbox in self.bottom.base_dex_checkboxes]
        }
        with open("files/config.json", "w", encoding="utf-8") as f:
            js.dump(config, f, ensure_ascii=False)
        self.destroy()


def run_gui():
    customtkinter.set_appearance_mode("Dark")
    app = App(None)
    log.setLevel(logging.INFO)
    gui_handler = MyHandlerText(app.console)
    txt_handler = logging.FileHandler("files/log.txt", "a", "utf-8")
    log.addHandler(gui_handler)
    log.addHandler(txt_handler)
    formatter = MyFormatter(fmt="%(asctime)s - %(message)s\n")
    gui_handler.setFormatter(formatter)
    txt_handler.setFormatter(formatter)
    app.process_opening()
    app.protocol("WM_DELETE_WINDOW", app.process_closing)
    app.geometry("1370x870")
    app.log = log
    try:
        app.mainloop()
    except:
        app.process_closing()
