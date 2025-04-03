import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import random, time, math

class BlackjackGame:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Blackjack")
        self.balance = 100
        self.bet = 0
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.card_images = []
        self.soft = ""
        self.bg_color = "#009a4d"
        self.accent_color = "#00d169"
        self.card_back_color = "blue"

        self.setup_ui()
        
    def load_card_back(self):
        card_back_image = Image.open(f"assets/backs/{self.card_back_color}_back.png")
        card_back_image = card_back_image.resize((55, 80))
        self.card_back = ImageTk.PhotoImage(card_back_image)

    def setup_ui(self):
        self.root.geometry("385x385")
        self.root.configure(background=self.bg_color)

        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}", background=self.bg_color, fg="white")
        self.balance_label.pack()
        
        self.bet_label = tk.Label(self.root, text="Bet: $0", background=self.bg_color, fg="white", font=(font.nametofont("TkDefaultFont").actual(), 10, "bold"))
        self.bet_label.pack()

        self.bet_entry = tk.Entry(self.root, background=self.accent_color)
        self.bet_entry.pack()
        
        self.bet_button = tk.Button(self.root, text="Place Bet", command=self.place_bet, background=self.accent_color, activebackground=self.accent_color)
        self.bet_button.pack()
        
        self.player_frame = tk.Frame(self.root, background=self.bg_color, pady=5)
        self.player_frame.pack()
        
        self.dealer_frame = tk.Frame(self.root, background=self.bg_color, pady=5)
        self.dealer_frame.pack()
        
        self.button_frame = tk.Frame(self.root, background=self.bg_color)
        self.button_frame.pack()

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, state=tk.DISABLED, background=self.accent_color, activebackground=self.accent_color)
        self.hit_button.pack(side=tk.LEFT, padx=2)
        
        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, state=tk.DISABLED, background=self.accent_color, activebackground=self.accent_color)
        self.stand_button.pack(side=tk.LEFT, padx=2)

        self.double_down_button = tk.Button(self.button_frame, text="Double Down", command=self.double_down, state=tk.DISABLED, background=self.accent_color, activebackground=self.accent_color)
        self.double_down_button.pack(side=tk.LEFT, padx=2)

        self.player_total_label = tk.Label(self.root, text="Your total: 0", background=self.bg_color, fg="white")
        self.player_total_label.pack()
        
        self.dealer_total_label = tk.Label(self.root, text="Dealer's total: ?", background=self.bg_color, fg="white")
        self.dealer_total_label.pack()
        
        self.player_total_label.config(text=f"Your total: {self.calculate_score(self.player_hand)}")
        self.dealer_total_label.config(text="Dealer's total: ?")

        self.result_label = tk.Label(self.root, text="", background=self.bg_color, fg="white", font=("Segoe UI Variable", 10, "bold"))
        self.result_label.pack()

        self.load_card_back()
        card_label = tk.Label(self.player_frame, image=self.card_back, background=self.bg_color)
        card_label.pack(side=tk.LEFT, padx=2)
        card_label = tk.Label(self.player_frame, image=self.card_back, background=self.bg_color)
        card_label.pack(side=tk.LEFT, padx=2)        
        card_label = tk.Label(self.dealer_frame, image=self.card_back, background=self.bg_color)
        card_label.pack(side=tk.LEFT, padx=2)
        card_label = tk.Label(self.dealer_frame, image=self.card_back, background=self.bg_color)
        card_label.pack(side=tk.LEFT, padx=2)

    def create_deck(self):
        suits = ['H', 'D', 'C', 'S']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'value': value, 'suit': suit} for suit in suits for value in values] * 4

    def deal_card(self, hand):
        card = random.choice(self.deck)
        self.deck.remove(card)
        hand.append(card)
        self.clear_table()
        self.add_player_cards()
        self.add_dealer_cards()

    def calculate_score(self, hand):
        score = 0
        aces = 0
        for card in hand:
            if card['value'] in ['J', 'Q', 'K']:
                score += 10
            elif card['value'] == 'A':
                aces += 1
                score += 11
                self.soft = "Soft "
            else:
                score += int(card['value'])
        
        while score > 21 and aces:
            score -= 10
            aces -= 1
            self.soft = ""
        
        return score

    def clear_table(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

    def add_player_cards(self):
        for card in self.player_hand:
            self.draw_card(self.player_frame, card)

        self.player_total_label.config(text=f"Your total: {self.soft}{self.calculate_score(self.player_hand)}")
        
    def add_dealer_cards(self, reveal_dealer=False):
        for i, card in enumerate(self.dealer_hand):
            if i == 0 and not reveal_dealer:
                self.draw_card(self.dealer_frame, None)
            else:
                self.draw_card(self.dealer_frame, card)

        if reveal_dealer:
            self.dealer_total_label.config(text=f"Dealer's total: {self.soft}{self.calculate_score(self.dealer_hand)}")
        else:
            self.dealer_total_label.config(text="Dealer's total: ?")

    def draw_card(self, frame, card):
        if card:
            card_face_image = Image.open(f"assets/cards/{card["value"]}{card["suit"]}.png")
            card_face_image = card_face_image.resize((55, 80))
            card_face = ImageTk.PhotoImage(card_face_image)
            self.card_images.append(card_face)
            card_label = tk.Label(frame, image=card_face, background=self.bg_color)
            card_label.pack(side=tk.LEFT, padx=2)
        else:
            card_label = tk.Label(frame, image=self.card_back, background=self.bg_color)
            card_label.pack(side=tk.LEFT, padx=2)

    def place_bet(self):
        bet_str = self.bet_entry.get()
        if bet_str == "all":
            bet_amount = self.balance
        elif bet_str == "half":
            bet_amount = self.balance // 2
        else:
            try:
                bet_amount = int(bet_str)
            except ValueError:
                return
        if bet_amount <= 0 or bet_amount > self.balance:
            return
        self.bet = bet_amount
        self.balance -= self.bet
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_label.config(text=f"Bet: ${self.bet}")
        self.bet_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_down_button.config(state=tk.NORMAL)
        self.result_label.config(text="")
        self.clear_table()
        
        self.player_hand = []
        self.dealer_hand = []
        self.deal_card(self.player_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.dealer_hand)
        if self.calculate_score(self.player_hand) == 21:
            self.balance += math.floor(self.bet * 2.5)
            self.result_label.config(text="Blackjack! You win!")
            self.end_round()
            self.new_round()

    def new_round(self):
        self.bet = 0
        self.bet_label.config(text=f"Bet: ${self.bet}")
        self.bet_button.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        
    def double_down(self):
        self.hit(True)

    def hit(self, double=False):
        if double:
            bet_amount = self.bet
            if bet_amount > self.balance:
                return
            total_bet = bet_amount * 2
            self.balance -= bet_amount
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.bet_label.config(text=f"Bet: ${total_bet}")

        self.deal_card(self.player_hand)
        player_score = self.calculate_score(self.player_hand)

        if player_score > 21:
            self.result_label.config(text="You busted!")
            self.end_round()
            self.new_round()
        elif double:
            self.stand()

    def stand(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
        
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        if player_score > dealer_score:
            self.balance += self.bet * 2
            self.result_label.config(text="You win!")
            self.end_round()
            self.new_round()
        elif dealer_score > 21:
            self.balance += self.bet * 2
            self.result_label.config(text="Dealer busted! You win.")
            self.end_round()
            self.new_round()
        elif player_score == dealer_score:
            self.balance += self.bet
            self.result_label.config(text="It's a push!")
            self.end_round()
            self.new_round()
        else:
            self.result_label.config(text="Dealer wins!")
            self.end_round()
            self.new_round()

    def end_round(self):
        if self.balance == 0:
            self.balance = 1
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.clear_table()
        self.add_player_cards()
        self.add_dealer_cards(True)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()