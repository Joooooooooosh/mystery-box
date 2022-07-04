from tkinter import *
from functools import partial # To prevent unwanted windows
import random
from winreg import REG_LEGAL_CHANGE_FILTER
from xml.dom.expatbuilder import FragmentBuilder

class Game:
    def __init__(self, partner, stakes, starting_balance,):
        print(stakes)
        print(starting_balance)

        # initialise variables
        self.balance = IntVar()
        # Set starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # Get value of stake (use it as a multipier when calculating winnings)
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # List for holding statistics
        self.round_stats_list = []
        self.game_stats_list=[starting_balance, starting_balance]

        # GUI Setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # If users press cross at top, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # Heading row
        self.heading_label = Label(self.game_frame, text="Play",
        font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Instructions Label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
        text="Press <enter> or click the 'Open Boxes' button to reveal the contents of the mystery boxes.",
        font="Arial 10", padx=10, pady=10)
        self.instructions_label.grid(row=1)

        # Boxes go here (row 2)

        box_text = "Arial 16 bold"
        box_back = "#b9ea96"
        box_width = 5

        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)

        self.prize1_label = Label(self.box_frame, text="\n?", bg=box_back, width = box_width, padx=10, pady=10)
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, text="\n?", bg=box_back, width = box_width, padx=10, pady=10)
        self.prize2_label.grid(row=0, column=1, padx=10)

        self.prize3_label = Label(self.box_frame, text="\n?", bg=box_back, width = box_width, padx=10, pady=10)

        self.prize3_label.grid(row=0, column=2)

        # Play button goes here (row 3)
        self.play_button = Button(self.game_frame, text="Open Boxes",
        bg="#FFFF33", font="Arial 15 bold", width=20,
        padx=10, pady=10, command=self.reveal_boxes)
        self.play_button.grid(row=3)

        # Bind button to <enter> (users can push enter to reveal the boxes)

        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

        # Balance Label (row 4)

        start_text = "Game Cost: ${} \n "" \nHow much " \
            "will you win?".format(stakes *5)

        self.balance_label = Label(self.game_frame, font="Arial 12 bold", fg="green",
        text=start_text, wrap=300,
        justify=LEFT)
        self.balance_label.grid(row=4, pady=10)

        # Help and Game Stats button (row 5)
        self.help_export_frame = Frame(self.game_frame)
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules",
        font="Arial 15 bold", command=self.to_help,
        bg="#808080", fg="white")
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats",
        font="Arial 15 bold",
        bg="#003366", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white",
        bg="#660000", font="Arial 15 bold", width=20,
        command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def reveal_boxes(self):
        # Retrieve the balance from the initial function
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prizes = []
        stats_prizes = []
        backgrounds = []
        for item in range(0, 3):
            prize_num = random.randint(1,100)

            if 0 < prize_num <= 5:
                prize = "gold\n(${})".format(5 * stakes_multiplier)
                prize_list = "gold (${})".format(5 * stakes_multiplier)
                back_color = "#CEA935" # Gold Colour
                round_winnings += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver\n(${})".format(2 * stakes_multiplier)
                prize_list = "silver (${})".format(2 * stakes_multiplier)
                back_color = "#B7B7B5" # Silver Colour
                round_winnings += 2 * stakes_multiplier
            elif 5 < prize_num <= 65:
                prize = "copper\n(${})".format(stakes_multiplier)
                prize_list = "copper (${})".format( stakes_multiplier)
                back_color = "#BC7F61" # Copper Colour
                round_winnings +=   stakes_multiplier
            else:
                prize = "lead\n($0)"
                prize_list = "lead ($0)"
                back_color = "#595E71" # Lead Colour

            prizes.append(prize)
            stats_prizes.append(prize_list)
            backgrounds.append(back_color)

        self.prize1_label.config(text=prizes[0], bg=backgrounds[0])
        self.prize2_label.config(text=prizes[1], bg=backgrounds[1])
        self.prize3_label.config(text=prizes[2], bg=backgrounds[2])



        # Deduct cost of game
        current_balance -= 5 * stakes_multiplier
        # Add Winnings
        current_balance += round_winnings

        # Set Balance to new Balance
        self.balance.set(current_balance)
        # update game_stats_list with current balance
        self.game_stats_list[1] = current_balance

        balance_statement="Game Cost: ${}\nPayback: ${} \n" \
            "Current Balance: ${}".format(5 * stakes_multiplier,
            round_winnings,
            current_balance)

        # Add round results to statistics list
        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: " \
                        "${}".format(stats_prizes[0], stats_prizes[1],
                                    stats_prizes[2],
                                    5 * stakes_multiplier,round_winnings,
                                    current_balance)
        self.round_stats_list.append(round_summary)
        print(self.round_stats_list)

        # Edit label so user can see their balance
        self.balance_label.configure(text=balance_statement)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\n" \
                                "Your balance is tooo low. You can only quit " \
                                "or view your stats. Sorry about that. ".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold",
            text= balance_statement)


    def to_quit(self):
        root.destroy()

class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_history)

        # disable help button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # Sets up child window 
        self.stats_box = Toplevel ()

        # If users press cross at top, closes help and 'releases' help button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Set up GUI Frame
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()

        # Set up help heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Statistics",
        font="arial 19 bold")
        self.stats_heading_label.grid(row=0)

        # To Export <instructions> (row 1)
        self.export_instructions = Label(self.stats_frame,
                                        text="Here are your Game Statistics."
                                            "Please use the Export button to "
                                            "access the results of each "
                                            "round that you played", wrap=250,
                                            font="arial 10 italic",
                                            justify=LEFT, fg="green",
                                            padx=10, pady=10)
        self.export_instructions.grid(row=1)

        # Starting Balance (row 2)
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)

        # Starting balance (row 2.0)

        self.start_balance_label = Label(self.details_frame,
        text="Starting Balance:", font=heading,
        anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content,
        text="${}".format(game_stats[0]), anchor="w")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

        # Current Balance (row 2.2)
        self.current_balance_label = Label(self.details_frame,
        text="Current Balance:", font=heading, anchor="e")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label = Label(self.details_frame, font=content,
        text="${}".format(game_stats[1]), anchor="w")
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"

        # Amount won / lost (row 2.3)
        self.wind_loss_label = Label(self.details_frame,
        text=win_loss, font=heading,
        anchor="e")
        self.wind_loss_label.grid(row=2, column=0, padx=0)

        self.wind_loss_value_label = Label(self.details_frame, font=content,
        text="${}".format(amount),
        fg=win_loss_fg, anchor="w")
        self.wind_loss_value_label.grid(row=2, column=1, padx=0)

        # Rounds Played (row 2.4)
        self.games_played_label = Label(self.details_frame,
        text="Rounds Played:", font=heading,
        anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)

        self.game_played_value_label = Label(self.details_frame, font=content,
        text=len(game_history),
        anchor="w")
        self.game_played_value_label.grid(row=4, column=1, padx=0)

        self.export_dismiss_frame = Frame(self.stats_frame)
        self.export_dismiss_frame.grid(row=3)

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.export_dismiss_frame, text="Dismiss", width=10,
        bg="orange", fg="White", font="arial 15 bold", pady=10, command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=0, column=0, pady=10)

        self.export_button = Button(self.export_dismiss_frame, text="Export", width=10,
        bg="pink", fg="White", font="arial 15 bold", pady=10)
        self.export_button.grid(row=0, column=1, pady=10)


    def close_stats(self, partner):
        # Put help button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

class Export: 

 def __init__(self, partner, game_history, all_game_stats):

        print(game_history)

        # disable help button
        partner.export_button.config(state=DISABLED)
        
        # Sets up child window 
        self.export_box = Toplevel ()

        # If users press cross at top, closes help and 'releases' help button

        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # Set up GUI Frame
        self.export_frame = Frame(self.export_box, width=300,)
        self.export_frame.grid()

        # Set up Export heading 
        self.how_heading = Label(self.export_frame, text="Export / " "Instructions",
        font="arial 14 bold")
        self.how_heading.grid(row=0)

        # Export Instructions 
        self.export_text = Label(self.export_frame, text="Enter a filename in the "
                                                            "box below and press the "
                                                            "Save button to save your "
                                                            "calculation history to "
                                                            "text file.",
                                justify=LEFT, width=40, wrap=250)
        self.export_text.grid(row=1)

        # Warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you "
                                                        "enter below already "
                                                        "exists, its contents "
                                                        "will be replaced with "
                                                        "your calculation history", 
                                justify=LEFT, bg="#ffafaf", fg="maroon",
                                font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # Filename Entry Box 
        self.filename_entry = Entry(self.export_frame, width=20,
        font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # Error Message Labels
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # Save / Cancel Frame
        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)

        # Save and Cancel Buttons
        self.save_button = Button(self.save_cancel_frame, text="Save",
        font="Arial 15 bold", bg="#003366", fg="white", command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=0)

        self.cancel_button = Button(self.save_cancel_frame, text="Cancel",
        font="Arial 15 bold", bg="#660000", fg="white", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1)

def save_history(self, partner, game_history, game_stats):

    # Regular expression to check filename is valid
    valid_char = "[A-Za-z0-9_]"
    has_error = "no"

    filename = self.filename_entry.get()
    print(filename)

    for letter in filename:
        if re.match(valid_char, letter):
            continue

        elif letter == " ":
            problem = "(no spaces allowed)"

        else:
            problem = ("(no {}'s allowed)".format(letter))
        has_error = "yes"
        break

    if filename == "":
        problem = "can't be blank"
        has_error = "yes"

    if has_error == "yes":
        # Display error message
        self.save_error_label.config(text="Invalid filename - {}".format(problem))
        # Change entry box background to pink
        self.filename_entry.config(bg="#ffafaf")
        print()

    else:
        # If there are no errors, generate text file and then close dialogue
        # add .txt suffix
        f = filename + ".txt"

        # create file to hold data
        f.write("Game statistics\n\n")

        # Heading for Stats
        f.write("Game Statistics\n\n")

        # Game stats
        for round in game_stats:
            f.write(round + "\n")

            # Heading for rounds
            f.write("\nRound Detials\n\n")

            # add new line at end of each item
            for item in game_history:
                f.write(item + "\n")

        # close file
        f.close()








# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Game()
    root.mainloop()