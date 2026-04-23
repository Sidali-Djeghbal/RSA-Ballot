import customtkinter as ctk

ALL_CANDIDATES = ["Option A", "Option B", "Option C"]
selected_candidate= ALL_CANDIDATES[0]

def update_selected_candidate(choice):
    global selected_candidate

    if not choice in ALL_CANDIDATES:
        raise ValueError("Tried to select invalid candidate! Aborting")

    selected_candidate = choice

def on_submit():
    if selected_candidate is None:
        print("Please select a candidate.")
        return

    print(f"selected: {selected_candidate}")

def main():
    # Setup
    app = ctk.CTk()
    app.title("E-Voting Client")
    app.geometry("400x300")
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=1)
    
    # Widgets
    form = ctk.CTkFrame(app, width=350, corner_radius=12)
    form.grid(row=0, column=0)
    form.grid_propagate(False)
    form.columnconfigure(0, weight=1)
    
    ctk.CTkLabel(form, text="Choose your candidate", anchor="w").grid(
        row=0,
        column=0,
        sticky="ew",
        padx=30,
        pady=(20, 0),
    )

    select = ctk.CTkOptionMenu(form, values=ALL_CANDIDATES, command=update_selected_candidate).grid(
        row=1,
        column=0,
        sticky="ew",
        padx=30,
    )
    
    button = ctk.CTkButton(form, text="Send vote", command=on_submit).grid(
        row=2,
        column=0,
        sticky="ew",
        padx=30,
        pady=(20, 30),
    )
    
    # Loop
    app.mainloop()

if __name__ == "__main__":
    main()
