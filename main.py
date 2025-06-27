import calendar
from customtkinter import *
from datetime import datetime
import json

ICON_PATH = os.path.abspath("icon.ico")
app = CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
width = 400
height = 350

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

app.geometry(f"{width}x{height}+{x}+{y}")
app.title("Simple Calendar Program")
app.configure(fg_color="#A5BFCC")
app.resizable(False, False)
app.iconbitmap(ICON_PATH)

events_window = None
events_window_key = None

def calendaryes(current_month: int = None, current_year: int = None):
    try:
        now = datetime.now()
        if current_month is None:
            current_month = now.month
        if current_year is None:
            current_year = now.year

        month_matrix = calendar.monthcalendar(current_year, current_month)

        main_frame = CTkFrame(app, fg_color="transparent")
        main_frame.pack(pady=20, anchor="n")

        top_frame = CTkFrame(main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, pady=(0, 10))

        top_frame.grid_columnconfigure((0, 4), weight=1)


        def open_events_window(day):
            global events_window, events_window_key
            key = f"{current_year}-{day}-{current_month}"
            filename = 'data.json'

            if events_window is not None and events_window.winfo_exists():
                if events_window_key != key:
                    events_window.destroy()
                else:
                    events_window.focus()
                    return

            events_window_key = key
            events_window = CTkToplevel(app, fg_color="#F4EDD3")
            events_window.geometry(f"300x175+{x-300}+{y}")
            events_window.title(f"Events for {calendar.month_name[current_month]} {day}, {current_year}")
            events_window.after(200, lambda: events_window.iconbitmap(ICON_PATH))

            if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            event_texts = "\n".join(f"• {event}" for event in data.get(key, [])) or "No events."

            event_textbox = CTkTextbox(events_window, width=260, height=140, font=("Consolas", 12), wrap="word")
            event_textbox.grid(padx=20, pady=10)
            event_textbox.insert("1.0", f"Events for {calendar.month_name[current_month]} {day}, {current_year}:\n\n{event_texts}")
            event_textbox.configure(state="disabled")
            events_window.iconbitmap(ICON_PATH)

        
        def open_input_dialog(day):
            key = f"{current_year}-{day}-{current_month}"
            filename = 'data.json'

            dialog = CTkInputDialog(font=("Consolas", 20), text="Enter your event:", title="Event Input Window", fg_color="#F4EDD3")
            dialog.geometry(f"300x175+{x+400}+{y}")
            dialog.after(200, lambda: dialog.iconbitmap(ICON_PATH))
            text = dialog.get_input()

            if not text:
                return

            if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            if key in data:
                if isinstance(data[key], list):
                    data[key].append(text)
                else:
                    data[key] = [data[key], text]
            else:
                data[key] = [text]

            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)


        def prev_month():
            nonlocal current_month, current_year
            main_frame.destroy()

            if current_month == 1:
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1
            calendaryes(current_month, current_year)


        def next_month():
            nonlocal current_month, current_year
            if current_month == 12:
                current_month = 1
                current_year += 1
            else:
                current_month += 1
            main_frame.destroy()
            calendaryes(current_month, current_year)


        calendar_frame = CTkFrame(main_frame, fg_color="transparent")
        calendar_frame.grid(row=1, column=0, padx=20)


        def see_all_years():
            nonlocal calendar_frame
            if calendar_frame.winfo_exists():
                    calendar_frame.destroy()

            def get_year(y):
                main_frame.destroy()
                calendaryes(current_month, y)

            calendar_frame = CTkScrollableFrame(main_frame, fg_color="transparent", scrollbar_fg_color="#4C585B", scrollbar_button_color="#7E99A3", corner_radius=0, width=225)
            calendar_frame.grid(row=1, column=0, padx=20)
            
            start_year = current_year + 25
            end_year = current_year - 25
            for i, year in enumerate(range(start_year, end_year - 1, - 1)):
                if year >= 0:
                    label = CTkButton(calendar_frame, text=year, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 14), corner_radius=6, width=105, command=lambda y=year: get_year(y))
                else:
                    pass
                label.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="nsew")
            calendar_frame.after(100, lambda: calendar_frame._parent_canvas.yview_moveto(0.418))

        def see_all_months():
            nonlocal calendar_frame
            try:
                if calendar_frame.winfo_exists():
                    calendar_frame.destroy()
                
                def get_month(m):
                    month = list(calendar.month_name).index(m)
                    main_frame.destroy()
                    calendaryes(month, current_year)

                calendar_frame = CTkFrame(main_frame, fg_color="transparent")
                calendar_frame.grid(row=1, column=0, padx=20)
                for col in range(4):
                    calendar_frame.grid_columnconfigure(col, weight=1)

                for i in range(1, 13):
                    month_name = calendar.month_name[i]
                    label = CTkButton(calendar_frame, text=month_name, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 14), corner_radius=6, width=105, command=lambda m=month_name: get_month(m))
                    label.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5, sticky="nsew")

            except Exception as e:
                print("Error ", e)

        left_arrow = CTkButton(top_frame, text="<-", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, width=10, command=prev_month)
        month_gui = CTkButton(top_frame, text=f"{calendar.month_name[current_month]}", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, command=see_all_months, width=50)
        year_gui = CTkButton(top_frame, text=f"{current_year}", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, command=see_all_years, width=50)
        right_arrow = CTkButton(top_frame, text="->", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, width=10, command=next_month)

        left_arrow.grid(row=0, column=1, padx=5)
        month_gui.grid(row=0, column=2, padx=5)
        year_gui.grid(row=0, column=3, padx=5)
        right_arrow.grid(row=0, column=4, padx=5)

        for col in range(8):
            calendar_frame.grid_columnconfigure(col, weight=1)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = CTkLabel(calendar_frame, text=day, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 14), corner_radius=6)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        for week_idx, week in enumerate(month_matrix):
            for day_idx, day in enumerate(week):
                text = str(day) if day != 0 else " "
                if text == " ":
                    label = CTkLabel(calendar_frame, text=text, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10)
                else:
                    with open("data.json") as json_data:
                        try:
                            data = json.load(json_data)
                            key = f"{current_year}-{day}-{current_month}"
                            if len(data[key]) > 0 and len(data[key]) < 3:
                                label = CTkButton(calendar_frame, text=text, fg_color="#FFC300", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10, hover_color="#B0C4DE")
                                label.bind("<Button-1>", lambda e, d=day: open_events_window(d))
                                label.bind("<Button-3>", lambda e, d=day: open_input_dialog(d))
                            elif len(data[key]) >= 3:
                                label = CTkButton(calendar_frame, text=text, fg_color="#FF5733", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10, hover_color="#B0C4DE")
                                label.bind("<Button-1>", lambda e, d=day: open_events_window(d))
                                label.bind("<Button-3>", lambda e, d=day: open_input_dialog(d))
                            else:
                                label = CTkButton(calendar_frame, text=text, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10, hover_color="#B0C4DE")
                                label.bind("<Button-1>", lambda e, d=day: open_events_window(d))
                                label.bind("<Button-3>", lambda e, d=day: open_input_dialog(d))
                        except KeyError:
                            label = CTkButton(calendar_frame, text=text, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10, hover_color="#B0C4DE")
                            label.bind("<Button-1>", lambda e, d=day: open_events_window(d))
                            label.bind("<Button-3>", lambda e, d=day: open_input_dialog(d))
                label.grid(row=week_idx + 1, column=day_idx, padx=5, pady=5, sticky="nsew")

    except Exception as e:
        print("Error:", e)



calendaryes()
app.mainloop()
