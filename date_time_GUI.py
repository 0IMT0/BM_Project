import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta, time

def create_date_selector():
    root = tk.Tk()
    root.title("Date Selector App")

    # Variables to store user selections
    start_date_var = tk.StringVar()
    end_date_var = tk.StringVar()
    market_type_var = tk.StringVar()
    selected_period = tk.StringVar()  # Store the selected time period

    # Create widgets
    create_widgets(root, start_date_var, end_date_var, market_type_var, selected_period)

    # Run the main loop
    root.mainloop()

    # Return the selected values
    return start_date_var.get(), end_date_var.get(), market_type_var.get()

def create_widgets(root, start_date_var, end_date_var, market_type_var, selected_period):
    def on_period_combobox_change(event):
        selected_period.set(root.focus_get().get())

        # Enable the calendar selector based on the selected time period
        calendar_selector.configure(state="normal" if selected_period.get() in ["1 Day", "1 Week", "1 Month"] else "disabled")

        # Reset start and end date entries
        start_date_var.set("")
        end_date_var.set("")

        # Update the date entries when the time period is selected
        if selected_period.get() == "1 Day":
            calendar_selector.bind("<<DateEntrySelected>>", on_date_selected)
        elif selected_period.get() == "1 Week":
            calendar_selector.bind("<<DateEntrySelected>>", on_week_selected)
        elif selected_period.get() == "1 Month":
            calendar_selector.bind("<<DateEntrySelected>>", on_month_selected)

    def format_time_set(dt_obj):
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S%z")

    def on_date_selected(event):
        # Automatically update the start and end date for 1 Day
        selected_date = calendar_selector.get_date()
        end_date = datetime.combine(selected_date, time(23, 59, 59)) + timedelta(days=0, hours=0, minutes=0, seconds=0)
        start_date_var.set(format_time_set(selected_date))
        end_date_var.set(format_time_set(end_date))

    def on_week_selected(event):
        # Automatically update the start and end date for 1 Week
        selected_date = calendar_selector.get_date()
        start_date = selected_date - timedelta(days=selected_date.weekday())
        end_date = datetime.combine(selected_date, time(23, 59, 59)) + timedelta(days=6, hours=0, minutes=0, seconds=0)
        start_date_var.set(format_time_set(start_date))
        end_date_var.set(format_time_set(end_date))

    def on_month_selected(event):
        # Automatically update the start and end date for 1 Month
        selected_date = calendar_selector.get_date()
        start_date = datetime(selected_date.year, selected_date.month, 1)
        end_date = (start_date.replace(day=1, month=start_date.month + 1) - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        start_date_var.set(format_time_set(start_date))
        end_date_var.set(format_time_set(end_date))

    # Period Label and Combobox
    period_label = tk.Label(root, text="Select Time Period:")
    period_label.pack(pady=10)

    period_combobox = ttk.Combobox(root, values=["1 Day", "1 Week", "1 Month"])
    period_combobox.pack(pady=10)
    period_combobox.bind("<<ComboboxSelected>>", on_period_combobox_change)

    # Date Selection Heading Label
    date_heading_label = tk.Label(root, text="Date Selector", font=('Helvetica', 12, 'bold'))
    date_heading_label.pack(pady=10)

    # Calendar Selector
    calendar_selector = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2,
                                  year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                                  date_pattern="y-mm-dd", state="disabled", maxdate=datetime.now())
    calendar_selector.pack(pady=10)

    # Start Date Label and Entry (read-only)
    start_date_label = tk.Label(root, text="Start Date:")
    start_date_label.pack()

    start_date_entry = ttk.Entry(root, textvariable=start_date_var, state="readonly")
    start_date_entry.pack()

    # End Date Label and Entry (read-only)
    end_date_label = tk.Label(root, text="End Date:")
    end_date_label.pack()

    end_date_entry = ttk.Entry(root, textvariable=end_date_var, state="readonly")
    end_date_entry.pack()

    # Market Type Label and Radiobuttons
    market_label = tk.Label(root, text="Select Market Type:")
    market_label.pack(pady=10)

    bid_radio = ttk.Radiobutton(root, text="Bid", variable=market_type_var, value="Bid")
    bid_radio.pack()

    offer_radio = ttk.Radiobutton(root, text="Offer", variable=market_type_var, value="Offer")
    offer_radio.pack()

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=root.destroy)
    submit_button.pack(pady=20)


#TEST CODE:

### Get the selected values
#start_date, end_date, market_type = create_date_selector()
### Display the selected values
#print(f"Start Date: {start_date}, End Date: {end_date}, Market Type: {market_type}")
