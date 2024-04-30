import tkinter as tk

version = "1.0.0"

if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"Watchdog v.{version}")

    def select_dir():
        pass

    root_x = 800
    root_y = 600

    offset_x = root.winfo_screenwidth() // 2
    offset_y = root.winfo_screenheight() // 2

    bg_color = "white"

    root.geometry(f"{root_x}x{root_y}+{offset_x-(root_x//2)}+{offset_y-(root_y//2)}")
    
    frame = tk.Frame(root, width=root_x, height=root_y, bg=bg_color)
    frame.grid(row=0, column=0)
    frame.pack_propagate(False)

    tk.Label(frame, text="Source Directory:", bg=bg_color, font=("TkMenuFont", 14)).pack(padx=20)
    tk.Button(frame, text="Browse", font=("TkHeadingFont", 20), bg=bg_color, cursor="hand2", command=lambda:select_dir()).pack(padx=20)

    root.mainloop()