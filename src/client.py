import os
import customtkinter as ctk
from PIL import Image

ALL_CANDIDATES = ["Candidate A", "Candidate B", "Candidate C"]
CANDIDATES_INFO = {
    "Candidate A": "An experienced leader focusing on infrastructure and education transparency.",
    "Candidate B": "Innovator bringing tech-driven solutions for better community engagement.",
    "Candidate C": "Grassroots advocate dedicated to environmental sustainability and local business."
}
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
AVATAR_PATH = os.path.join(ASSETS_DIR, "avatar.png")


class CandidateCard(ctk.CTkFrame):
    def __init__(self, master, candidate_name, image, command=None, **kwargs):
        super().__init__(master, corner_radius=10, fg_color="transparent", border_width=2, border_color="gray70", **kwargs)
        self.candidate_name = candidate_name
        self.command = command
        self.is_selected = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Image
        self.image_label = ctk.CTkLabel(self, text="", image=image)
        self.image_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="nsew")

        # Name
        self.name_label = ctk.CTkLabel(self, text=candidate_name, font=("Arial", 14, "bold"))
        self.name_label.grid(row=1, column=0, pady=(0, 10), padx=10)

        # Bind click events for selection
        self.bind("<Button-1>", self._on_click)
        self.image_label.bind("<Button-1>", self._on_click)
        self.name_label.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if self.command:
            self.command(self.candidate_name, self)

    def set_selected(self, selected):
        self.is_selected = selected
        if self.is_selected:
            self.configure(border_color="#3B8ED0", fg_color=("#D4E6F1", "#1F538D"))
        else:
            self.configure(border_color="gray70", fg_color="transparent")


class VotingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("E-Voting Client")
        self.geometry("600x450")
        self.selected_candidate = None
        self.cards = []

        # Load resources
        self._load_image()

        # Layout configuring
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self, text="Secure E-Voting", font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        # Responsive Grid Frame (invisible scrollbar)
        self.grid_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.grid_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Hide the actual scrollbar widget
        self.grid_frame._scrollbar.grid_forget()

        # Populate Cards
        self._create_candidate_cards()

        # Description Label
        self.desc_label = ctk.CTkLabel(
            self, text="Please select a candidate to view their platform.",
            font=("Arial", 14), justify="center", wraplength=500
        )
        self.desc_label.grid(row=2, column=0, pady=(10, 10), padx=20, sticky="n")

        # Submit Button
        self.submit_btn = ctk.CTkButton(
            self, text="Send Vote", command=self.on_submit, height=40, font=("Arial", 15)
        )
        self.submit_btn.grid(row=3, column=0, pady=(10, 5), padx=20, sticky="ew")

        # Warning Note
        self.note_label = ctk.CTkLabel(
            self, text="Note: You can only vote once. You cannot change your vote after submitting.",
            font=("Arial", 12, "italic"), text_color="gray60"
        )
        self.note_label.grid(row=4, column=0, pady=(0, 20), padx=20, sticky="ew")

    def _load_image(self):
        if os.path.exists(AVATAR_PATH):
            pil_image = Image.open(AVATAR_PATH)
            self.avatar_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(100, 100))
        else:
            # Fallback if image not found
            self.avatar_img = None

    def _create_candidate_cards(self):
        # Setup a responsive grid layout
        columns = 3
        for i in range(columns):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        for i, candidate in enumerate(ALL_CANDIDATES):
            card = CandidateCard(
                self.grid_frame,
                candidate_name=candidate,
                image=self.avatar_img,
                command=self.on_card_selected
            )
            
            row = i // columns
            col = i % columns
            
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.cards.append(card)

    def on_card_selected(self, candidate_name, selected_card):
        self.selected_candidate = candidate_name
        
        # Deselect all, select one
        for card in self.cards:
            card.set_selected(card == selected_card)

        # Update description
        description = CANDIDATES_INFO.get(candidate_name, "No description available.")
        self.desc_label.configure(text=description)

    def on_submit(self):
        if self.selected_candidate is None:
            print("Please select a candidate.")
            return

        print(f"selected: {self.selected_candidate}")


def main():
    app = VotingApp()
    app.mainloop()

if __name__ == "__main__":
    main()
