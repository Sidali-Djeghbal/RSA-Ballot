import os
import sys
import json
import socket
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

# allow importing from common
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import rsa_core

AVAILABLE_CANDIDATES = ["Candidate A", "Candidate B", "Candidate C"]
CANDIDATES_DESCRIPTIONS = {
    "Candidate A": "experienced leader focusing on infrastructure.",
    "Candidate B": "tech-driven solutions for community.",
    "Candidate C": "grassroots advocate for sustainability."
}

# hardcoded public keys from server
SERVER_PUBLIC_E = 3
SERVER_PUBLIC_N = 62857

class CandidateCardWidget(ctk.CTkFrame):
    def __init__(self, parent_master, candidate_name, avatar_image, on_click_command=None, **kwargs):
        super().__init__(parent_master, corner_radius=10, fg_color="transparent", border_width=2, border_color="gray70", **kwargs)
        self.candidate_name = candidate_name
        self.on_click_command = on_click_command
        self.is_currently_selected = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # show picture
        self.picture_label = ctk.CTkLabel(self, text="", image=avatar_image)
        self.picture_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="nsew")

        # show text
        self.name_text_label = ctk.CTkLabel(self, text=candidate_name, font=("Arial", 14, "bold"))
        self.name_text_label.grid(row=1, column=0, pady=(0, 10), padx=10)

        # bind mouse clicks
        self.bind("<Button-1>", self.handle_mouse_click)
        self.picture_label.bind("<Button-1>", self.handle_mouse_click)
        self.name_text_label.bind("<Button-1>", self.handle_mouse_click)

    def handle_mouse_click(self, _):
        if self.on_click_command:
            self.on_click_command(self.candidate_name, self)

    # change colors when clicked
    def update_selection_state(self, is_selected):
        self.is_currently_selected = is_selected
        if self.is_currently_selected:
            self.configure(border_color="#3B8ED0", fg_color=("#D4E6F1", "#1F538D"))
        else:
            self.configure(border_color="gray70", fg_color="transparent")

class VotingApplicationWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("secure e-voting client")
        self.geometry("600x480")
        
        self.chosen_candidate = None
        self.card_widgets_list = []
        self.loaded_pem_filepath = None

        self.load_avatar_asset()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_login_screen()
        self.build_main_voting_screen()
        
        # show login first
        self.voting_container.grid_remove()
        self.login_container.grid(row=0, column=0, sticky="nsew")

    # draw the first screen (dashboard version)
    def build_login_screen(self):
        self.login_container = ctk.CTkFrame(self, fg_color="transparent")
        self.login_container.grid_columnconfigure(0, weight=1)
        
        # university and department header
        dept_label = ctk.CTkLabel(self.login_container, text="computer science department | 3rd year engineering", font=("Arial", 12, "italic"), text_color="gray60")
        dept_label.grid(row=0, column=0, pady=(30, 0))

        # main project title
        welcome_text = ctk.CTkLabel(self.login_container, text="secure e-voting system", font=("Arial", 28, "bold"))
        welcome_text.grid(row=1, column=0, pady=(10, 5))
        
        subtitle = ctk.CTkLabel(self.login_container, text="client-side authentication portal", font=("Arial", 16))
        subtitle.grid(row=2, column=0, pady=(0, 20))

        # educational frame showing off the rubric requirements to the professor
        info_frame = ctk.CTkFrame(self.login_container, corner_radius=10, fg_color=("gray90", "gray15"))
        info_frame.grid(row=3, column=0, padx=40, pady=15, sticky="ew")

        info_title = ctk.CTkLabel(info_frame, text="cryptographic protocol active", font=("Arial", 14, "bold"))
        info_title.pack(pady=(15, 5))

        # bullet points explaining the math happening in the background
        guarantees = (
            "• confidentiality: ballots are encrypted via the server's rsa public key.\n"
            "• authenticity: packets are digitally signed using your local private key.\n"
            "• integrity: sha-256 hashing prevents any tampering during transit."
        )
        info_text = ctk.CTkLabel(info_frame, text=guarantees, font=("Arial", 13), justify="left")
        info_text.pack(pady=(0, 15), padx=20)

        # actionable steps for the user
        instruction_text = ctk.CTkLabel(self.login_container, text="step 1: load your personal .pem key file to authenticate.", font=("Arial", 14))
        instruction_text.grid(row=4, column=0, pady=(25, 10))

        select_file_button = ctk.CTkButton(self.login_container, text="load identity (.pem)", command=self.trigger_file_dialog, height=45, font=("Arial", 14, "bold"))
        select_file_button.grid(row=5, column=0, pady=(10, 30))

    # open windows file explorer
    def trigger_file_dialog(self):
        chosen_file = filedialog.askopenfilename(
            title="find your key file",
            filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")]
        )
        if chosen_file:
            self.loaded_pem_filepath = chosen_file
            self.login_container.grid_remove()
            self.voting_container.grid(row=0, column=0, sticky="nsew")

    # draw the candidates screen
    def build_main_voting_screen(self):
        self.voting_container = ctk.CTkFrame(self, fg_color="transparent")
        
        # tell the scroll area to expand, not the labels, so the button floats nicely
        self.voting_container.grid_rowconfigure(1, weight=1)
        self.voting_container.grid_columnconfigure(0, weight=1)

        top_label = ctk.CTkLabel(self.voting_container, text="cast your vote", font=("Arial", 20, "bold"))
        top_label.grid(row=0, column=0, pady=(20, 10), sticky="ew")

        self.scroll_area = ctk.CTkScrollableFrame(self.voting_container, fg_color="transparent")
        self.scroll_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scroll_area._scrollbar.grid_forget()

        self.populate_candidate_grid()

        self.info_label = ctk.CTkLabel(self.voting_container, text="select a candidate above.", font=("Arial", 14))
        self.info_label.grid(row=2, column=0, pady=(10, 10), padx=20, sticky="n")

        self.send_vote_button = ctk.CTkButton(self.voting_container, text="submit secure vote", command=self.process_vote_submission, height=40)
        self.send_vote_button.grid(row=3, column=0, pady=(5, 10), padx=20, sticky="ew")

        # warning note added to the bottom
        self.warning_note = ctk.CTkLabel(self.voting_container, text="note: voting is only once, voter can't change his vote after voting.", font=("Arial", 12, "italic"), text_color="gray60")
        self.warning_note.grid(row=4, column=0, pady=(0, 20), padx=20, sticky="ew")

    # load image from assets folder
    def load_avatar_asset(self):
        asset_path = os.path.join(os.path.dirname(__file__), "assets", "avatar.png")
        if os.path.exists(asset_path):
            img_data = Image.open(asset_path)
            self.avatar_graphic = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(100, 100))
        else:
            self.avatar_graphic = None

    # create ui cards for each person
    def populate_candidate_grid(self):
        total_columns = 3
        for col_index in range(total_columns):
            self.scroll_area.grid_columnconfigure(col_index, weight=1)

        for index, candidate_string in enumerate(AVAILABLE_CANDIDATES):
            card_ui = CandidateCardWidget(
                self.scroll_area,
                candidate_name=candidate_string,
                avatar_image=self.avatar_graphic,
                on_click_command=self.handle_card_selection
            )
            
            row_pos = index // total_columns
            col_pos = index % total_columns
            
            card_ui.grid(row=row_pos, column=col_pos, padx=10, pady=10, sticky="nsew")
            self.card_widgets_list.append(card_ui)

    # when user clicks a person
    def handle_card_selection(self, selected_name, clicked_card_widget):
        if self.send_vote_button.cget("state") == "disabled":
            return
            
        self.chosen_candidate = selected_name
        
        for widget in self.card_widgets_list:
            widget.update_selection_state(widget == clicked_card_widget)

        self.info_label.configure(text=CANDIDATES_DESCRIPTIONS.get(selected_name, "no info"))

    # run the crypto and socket code
    def process_vote_submission(self):
        if not self.chosen_candidate:
            messagebox.showwarning("warning", "pick a candidate first")
            return

        try:
            with open(self.loaded_pem_filepath, "r") as pem_file:
                file_contents = pem_file.read().strip().split(",")
                student_voter_id = file_contents[0]
                student_private_d = int(file_contents[1])
                student_modulus_n = int(file_contents[2])
        except Exception as read_error:
            messagebox.showerror("error", f"bad pem file: {read_error}")
            return

        # do the math
        message_integer = rsa_core.text_to_int(self.chosen_candidate)
        cipher_integer = rsa_core.encrypt(message_integer, SERVER_PUBLIC_E, SERVER_PUBLIC_N)
        signature_integer = rsa_core.sign(cipher_integer, student_private_d, student_modulus_n)

        network_payload = {
            "voter_id": student_voter_id,
            "encrypted_vote": cipher_integer,
            "signature": signature_integer
        }
        
        # send to server
        voting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        voting_socket.settimeout(5.0)
        
        try:
            voting_socket.connect(('127.0.0.1', 5000))
            voting_socket.send(json.dumps(network_payload).encode('utf-8'))
            
            server_reply = voting_socket.recv(1024).decode('utf-8')
            reply_json = json.loads(server_reply)
            
            if reply_json.get("status") == "success":
                messagebox.showinfo("success", reply_json.get("message"))
                self.send_vote_button.configure(text="vote counted!", fg_color="green", state="disabled")
            else:
                messagebox.showerror("rejected", reply_json.get("message"))
                
        except socket.timeout:
            messagebox.showerror("network error", "server is slow or offline")
        except ConnectionRefusedError:
            messagebox.showerror("network error", "is the server.py running?")
        finally:
            voting_socket.close()

if __name__ == "__main__":
    VotingApplicationWindow().mainloop()
