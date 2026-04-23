import customtkinter as ctk

def button_callback():
    print("button pressed")

def main():
    # Setup
    app = ctk.CTk()
    app.title("E-Voting Client")
    app.geometry("400x150")
    
    # Widgets
    button = ctk.CTkButton(app, text="Send vote", command=button_callback)
    button.grid(row=0, column=0, padx=20, pady=20)
    
    # Loop
    app.mainloop()

if __name__ == "__main__":
    main()
