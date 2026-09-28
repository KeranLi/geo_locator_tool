import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from geo_locator import locate


class GeoLocatorApp(tk.Tk):
    """Bilingual GUI for natural-language geocoding. Developer: Keran Li."""

    def __init__(self):
        super().__init__()
        self.title("自然语言经纬度查询 | Natural-language Geocoder")
        self.geometry("900x600")
        self.minsize(760, 500)
        self._build_ui()

    def _build_ui(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="自然语言经纬度查询 | Natural-language Geocoder", font=("Microsoft YaHei UI", 18, "bold")).pack(anchor="w")
        ttk.Label(root, text="输入地点名称或完整地址，返回经纬度。 | Enter a place name or address to get coordinates.").pack(anchor="w", pady=(4, 14))

        form = ttk.LabelFrame(root, text="查询条件 | Query", padding=10)
        form.pack(fill="x")
        ttk.Label(form, text="地点 | Place:").grid(row=0, column=0, sticky="w")
        self.query = ttk.Entry(form, font=("Microsoft YaHei UI", 11))
        self.query.grid(row=0, column=1, sticky="ew", padx=8)
        self.query.insert(0, "新疆喀什地区阿克陶县克孜勒陶乡其木干村")
        self.query.bind("<Return>", lambda event: self.search())
        ttk.Label(form, text="国家/地区 | Country:").grid(row=1, column=0, sticky="w", pady=(9, 0))
        self.country = ttk.Entry(form)
        self.country.grid(row=1, column=1, sticky="ew", padx=8, pady=(9, 0))
        self.country.insert(0, "中国")
        self.search_button = ttk.Button(form, text="查询 | Search", command=self.search)
        self.search_button.grid(row=0, column=2, rowspan=2, padx=8, ipadx=12, ipady=8)
        form.columnconfigure(1, weight=1)

        options = ttk.LabelFrame(root, text="服务配置 | Service settings", padding=10)
        options.pack(fill="x", pady=(12, 0))
        ttk.Label(options, text="高德 Web Key | AMap Web Key:").grid(row=0, column=0, sticky="w")
        self.amap_key = ttk.Entry(options, show="*")
        self.amap_key.grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Label(options, text="留空使用 OSM | Leave blank for OSM").grid(row=0, column=2, sticky="w")
        options.columnconfigure(1, weight=1)

        box = ttk.LabelFrame(root, text="查询结果 | Results", padding=8)
        box.pack(fill="both", expand=True, pady=(12, 0))
        self.status = ttk.Label(box, text="就绪 | Ready")
        self.status.pack(anchor="w")
        columns = ("provider", "address", "location", "system")
        self.table = ttk.Treeview(box, columns=columns, show="headings")
        headings = ("数据源 | Provider", "匹配地址 | Address", "经度,纬度 | Lon,Lat", "坐标系 | CRS")
        for column, heading, width in zip(columns, headings, (130, 350, 170, 180)):
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, anchor="w")
        self.table.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(box, command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)
        ttk.Button(root, text="复制选中坐标 | Copy coordinate", command=self.copy_selected).pack(anchor="e", pady=(8, 0))
        ttk.Label(root, text="开发者 | Developer: Keran Li", foreground="#666666").pack(anchor="w", pady=(6, 0))

    def search(self):
        query = self.query.get().strip()
        if not query:
            messagebox.showwarning("提示 | Notice", "请输入地点名称。 | Please enter a place name.")
            return
        self.search_button.configure(state="disabled")
        self.status.configure(text="正在查询，请稍候…… | Searching...")
        self.table.delete(*self.table.get_children())
        key = self.amap_key.get().strip()
        if key:
            os.environ["AMAP_KEY"] = key
        threading.Thread(target=self._worker, args=(query, self.country.get().strip()), daemon=True).start()

    def _worker(self, query, country):
        try:
            self.after(0, self._show_results, locate(query, country))
        except Exception as exc:
            self.after(0, self._show_error, str(exc))

    def _show_results(self, rows):
        self.search_button.configure(state="normal")
        for row in rows:
            self.table.insert("", "end", values=(row.get("provider", ""), row.get("address", ""), row.get("location", ""), row.get("coordinate_system", "")))
        self.status.configure(text=f"找到 {len(rows)} 条结果 | {len(rows)} result(s)" if rows else "没有找到匹配地点 | No results")

    def _show_error(self, message):
        self.search_button.configure(state="normal")
        self.status.configure(text="查询失败 | Query failed")
        messagebox.showerror("查询失败 | Query failed", message)

    def copy_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("提示 | Notice", "请先选择一条结果。 | Select a result first.")
            return
        values = self.table.item(selected[0], "values")
        self.clipboard_clear()
        self.clipboard_append(values[2])
        self.status.configure(text=f"已复制坐标 | Copied: {values[2]}")


if __name__ == "__main__":
    GeoLocatorApp().mainloop()
