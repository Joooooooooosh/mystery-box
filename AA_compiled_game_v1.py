from tkinter import *
from functools import partial # To prevent unwanted windows
import random


class Start: 
    def __init__(self, parent,): 
        

        # GUI to get starting balance and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.push_me_button = Button(text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):

        # Retrieve starting balance 
        starting_balance = 50
        stakes = 1

        Game(self, stakes, starting_balance)

        # Hide start up window 
        root.withdraw()

        # Set Initial balance to zero
        self.starting_funds = IntVar ()
        self.starting_funds.set(0)

        # Mystery Heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
        font="Arial 19 bold")
        self.mystery_box_label.grid(row=0)

        # Initial Instructions (row 1)
        self.mystery_instructions = Label(self.start_frame, font="Arial 10 italic",
        text="Please enter a dollar amount "
        "(between $5 and $50) in the box "
        "below, Then choose the stakes. "
        "The higher the stakes, "
        "the more you win!",
        wrap=275, justify=LEFT, padx=10, pady=10)
        self.mystery_instructions.grid(row=1)

        # Entry box (row 2)
        #self.start_amount_entry = Entry(self.start_frame, font="Arial 19 bold")
        #self.start_amount_entry.grid(row=2)

        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame,
        font="Arial 14 bold", width=10)
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame,
        font="Arial 14 bold",
        text="Add Funds",
        command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon",
        text="", font="Arial 10 bold", wrap=275,
        justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # button frame (row 3)
        self.stakes_frame = Frame(self.start_frame)
        self.stakes_frame.grid(row=3)

        # Buttons go here
        button_font = "Arial 12 bold"
        # Low (yellow) stakes button
        self.lowstakes_button = Button(self.stakes_frame, text="Low ($5)",
        command=lambda: self.to_game(1),
        font= button_font, bg="#FFFF33")
        self.lowstakes_button.grid(row=0, column=1, padx=5, pady=10)

        # Medium (orange) stakes button
        self.mediumstakes_button = Button(self.stakes_frame, text="Medium ($10)",
        command=lambda: self.to_game(2),
        font= button_font, bg="orange")
        self.mediumstakes_button.grid(row=0, column=2, padx=5, pady=10)

        # High (green) stakes button
        self.highstakes_button = Button(self.stakes_frame, text="High ($15)",
        command=lambda: self.to_game(3),
        font= button_font, bg="green")
        self.highstakes_button.grid(row=0, column=3, padx=5, pady=10)

        # Disable all stakes buttons at start
        self.lowstakes_button.config(state=DISABLED)
        self.mediumstakes_button.config(state=DISABLED)
        self.highstakes_button.config(state=DISABLED)

        # Help Button
        self.help_button = Button(self.start_frame, text="How to Play",
        bg="#808080", fg="white", font=button_font)
        self.help_button.grid(row=4, pady=10)




    def check_funds(self):

        print("checking...")

        starting_balance = self.start_amount_entry.get()
      

        # Set error background colours
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # Disable all stakes buttons in case user changes mind and
        # decreases amount entered
        self.lowstakes_button.config(state=NORMAL)
        self.mediumstakes_button.config(state=NORMAL)
        self.highstakes_button.config(state=NORMAL)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you " \
                                "can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in " \
                                "this game is $50"

            elif starting_balance >= 15:
                # enable low and medium stakes buttons
                self.lowstakes_button.config(state=NORMAL)
                self.mediumstakes_button.config(state=NORMAL)
            else:
                self.lowstakes_button.config(state=NORMAL)


        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (no text / decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            # set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):

        # retrieve starting balance
        starting_balance = self.starting_funds.get()

        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()       


class Game:
    def __init__(self, partner, stakes, starting_balance):

        
        print(stakes)
        print(starting_balance)

        # initialise variables
        self.balance = IntVar()

        # Set starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # Get value of stakes 
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # List for holding statistics
        self.round_stats_list = []
        self.game_stats_list=[starting_balance, starting_balance]

        # GUI Setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # Heading row
        self.heading_label = Label(self.game_frame, text="Heading",
        font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Balance Label
        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)
        
        self.balance_label = Label(self.game_frame, text="Balance")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Gain",
        padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

    def reveal_boxes(self):
        # retrieve the balance from the initial function
        current_balance = self.balance.get()

        # Adjust the balance (subtract game cost and add pay out)
        # For testing purposes, just add 2
        current_balance += 2

        # Set balance to adjusted balance
        self.balance.set(current_balance)

        #Edit label so user can see their balance
        self.balance_label.configure(text="Balance: {}".format(current_balance))


class Help:
    def __init__(self, partner):

        # disable help button
        partner.help_button.config(state=DISABLED)

        # Sets up child window (ie: help box)
        self.help_box = Toplevel()

        # If users press cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame
        self.help_frame = Frame(self.help_box, width=300)
        self.help_frame.grid()

        # Set up Help heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions",
        font="arial 10 bold")
        self.how_heading.grid(row=0)

        # Help text (label, row 1)

        help_text="Choose an amount to play with and then choose the stakes. " \
                "Higher stakes cost more per round but you can win more as " \
                "well.\n\n" \
                "When you enter the play area, you will see three mystery " \
                "boxes. To reveal the contents of the boxes, click the " \
                "'Open Boxes' button. If dont have enough money to play, " \
                "the button will turn red and you will need to quite the " \
                "game.\n\n" \
                "The contents of the boxes will be added to your balance.  " \
                "The boxes could contain...\n\n" \
                "Low: Lead ($0) | Copper ($1) | Silver ($2) | Gold ($10)\n" \
                "Medium: Lead ($0) | Copper ($2) | Silver ($4) | Gold ($25)\n" \
                "High: Lead ($0) | Copper ($5) | Silver ($10) | Gold ($50)\n\n" \
                "If each box contains gold, you earn $30 (low stakes). If " \
                "they contained copper, silver and gold, you would recieve " \
                "$13 ($1 + $2 + $10) and so on."

        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text=help_text,
        justify=LEFT, wrap=400, padx=10, pady=10)
        self.help_text.grid(row=1)
 

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10,
        bg="orange", fg="White", font="arial 15 bold", pady=10, command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()
        
    



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()