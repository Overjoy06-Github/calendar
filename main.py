import calendar
from customtkinter import *
from datetime import datetime
import json

ICON_PATH = os.path.abspath("calendar-app/icon.ico")
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
app.iconbitmap(ICON_PATH)

events_window = None
events_window_key = None


def calendaryes(current_month: int = None, current_year = datetime.now().year):
    try:
        if current_month is None:
            now = datetime.now()
            current_month = current_month or now.month

        month_matrix = calendar.monthcalendar(current_year, current_month)

        main_frame = CTkFrame(app, fg_color="transparent")
        main_frame.pack(pady=20, anchor="n")

        top_frame = CTkFrame(main_frame, fg_color="transparent")
        top_frame.grid(row=0, column=0, pady=(0, 10))

        top_frame.grid_columnconfigure((0, 4), weight=1)

        def set_event(day):
            global events_window, events_window_key
            key = f"{current_month}-{day}"
            filename = 'calendar-app/data.json'

            if events_window is not None and events_window.winfo_exists():
                if events_window_key != key:
                    events_window.destroy()
                else:
                    events_window.focus()
                    return

            events_window_key = key

            events_window = CTkToplevel(app, fg_color="#F4EDD3")
            events_window.geometry(f"300x175+{x-300}+{y}")
            events_window.title(f"Events for {calendar.month_name[current_month]} {day}")
            events_window.after(200, lambda: events_window.iconbitmap(ICON_PATH))

            dialog = CTkInputDialog(font=("Consolas", 20),text="Enter your event:", title="Event Input Window", fg_color="#F4EDD3")
            dialog.geometry(f"300x175+{x+400}+{y}")
            dialog.after(200, lambda: dialog.iconbitmap(ICON_PATH))
            text = dialog.get_input()
            
            if not text:
                text = None  

            if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError:
                        data = {}
            else:
                data = {}

            if text:
                if key in data:
                    if isinstance(data[key], list):
                        data[key].append(text)
                    else:
                        data[key] = [data[key], text]
                else:
                    data[key] = [text]

                with open(filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

            if key in data:
                event_texts = "\n".join(f"• {event}" for event in data[key])
            else:
                event_texts = "No events."

            event_textbox = CTkTextbox(events_window, width=260, height=140, font=("Consolas", 12), wrap="word")
            event_textbox.grid(padx=20, pady=10)
            event_textbox.insert("1.0", f"Events for {calendar.month_name[current_month]} {day}:\n\n{event_texts}")
            event_textbox.configure(state="disabled")
            events_window.iconbitmap(ICON_PATH)


        def prev_month():
            main_frame.destroy()
            calendaryes(current_month-1)


        def next_month():
            nonlocal current_month
            if current_month == 12:
                current_month = 1
            else:
                current_month += 1
            main_frame.destroy()
            calendaryes(current_month, current_year)


        left_arrow = CTkButton(top_frame, text="<-", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, width=10, command=prev_month)
        month_gui = CTkLabel(top_frame, text=calendar.month_name[current_month], fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10)
        right_arrow = CTkButton(top_frame, text="->", fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 16), corner_radius=10, width=10, command=next_month)

        left_arrow.grid(row=0, column=1, padx=10)
        month_gui.grid(row=0, column=2, padx=10)
        right_arrow.grid(row=0, column=3, padx=10)

        calendar_frame = CTkFrame(main_frame, fg_color="transparent")
        calendar_frame.grid(row=1, column=0, padx=20)

        for col in range(7):
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
                    label = CTkButton(calendar_frame, text=text, fg_color="#7E99A3", bg_color="#A5BFCC", font=("Consolas", 12), corner_radius=6, width=10, command=lambda d=day: set_event(d))
                label.grid(row=week_idx + 1, column=day_idx, padx=5, pady=5, sticky="nsew")

    except Exception as e:
        print("Error:", e)

    app.mainloop()


calendaryes()