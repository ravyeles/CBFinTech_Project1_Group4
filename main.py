from typing import Tuple
import customtkinter as ctk

#Sets the appearance mode and default color theme for the entire application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#Define the main variables
stock_symbols = ""
investment_amount = 0
investment_time_horizon = 0


class App(ctk.CTk):
    def __init__(self):
        super().__init__()     

        #Set user variables
        timvar=ctk.IntVar()
        strvar=ctk.StringVar()
        amtvar=ctk.DoubleVar()

        #Portflio Title and Grid Configuration
        self.title("Portfolio Analyzer")
        self.geometry("800x450")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=10)
        
        #Create the label for the user to input the stock symbol
        self.stock_label = ctk.CTkLabel(self, text="Enter a comma separated list of 5 stock symbols:",wraplength=350, justify=ctk.LEFT)
        self.stock_label.grid(column=0, row=0, rowspan=2, sticky=ctk.W, padx=5, pady=5)
        #Create the entry box for the user to input a comma separated list of 5 stock symbols
        self.stock_entry = ctk.CTkEntry(self)
        self.stock_entry.grid(column=1, row=0, rowspan=2, sticky=ctk.E, padx=5, pady=5)

        #Create the label for users to input the total amount they'd like to invest
        self.investment_amt = ctk.CTkLabel(self, text="Enter the amount you'd like to invest:",wraplength=350, justify=ctk.LEFT)
        self.investment_amt.grid(column=0, row=2, sticky=ctk.W, padx=5, pady=5)
        #Create the entry box for the user to input the total amount they'd like to invest
        self.investment_entry = ctk.CTkEntry(self)
        self.investment_entry.grid(column=1, row=2, sticky=ctk.E, padx=5, pady=5)

        #Create the label for users to input the total amount they'd like to invest
        self.investment_horizon = ctk.CTkLabel(self, text="Enter the time in years you'd like to stay invested:",wraplength=350, justify=ctk.LEFT)
        self.investment_horizon.grid(column=0, row=3, sticky=ctk.W, padx=5, pady=5)
        #Create the entry box for the user to input the total amount they'd like to invest
        self.horizon_entry = ctk.CTkEntry(self)
        self.horizon_entry.grid(column=1, row=3, sticky=ctk.E, padx=5, pady=5)

        #Create the button that will run the analysis
        self.analyze_button = ctk.CTkButton(self, text="Analyze This!", command=self.analyze_function)
        self.analyze_button.grid(column=2, row=0, rowspan=4, padx=5, pady=5, sticky=ctk.W+ctk.E+ctk.N+ctk.S)

        #Create the widget to display the results
        display_results_widget = ctk.CTkText(self, wrap=ctk.WORD, width=50, height=20)
        display_results_widget.grid(column=0, row=4, columnspan=3, rowspan=15, padx=5, pady=5, sticky=ctk.W+ctk.E+ctk.N+ctk.S)


    def analyze_function(self):
        print("Button clicked")
        stock_symbols = self.stock_entry.get()
        investment_amount = self.investment_entry.get()
        investment_time_horizon = self.horizon_entry.get()
        #Clear previous results
        display_results_widget.delete(1.0,ctk.END)
        #Call the function to display the results
        #calculate_results(stock_symbols, investment_amount, investment_time_horizon)
        #Display the results
        display_results_widget.insert(ctk.END, f"Stock Symbols: {stock_symbols}\nInvestment Amount: {investment_amount}\nInvestment Time Horizon: {investment_time_horizon}")
        #print(f"Stock Symbols: {stock_symbols}/nInvestment Amount: {investment_amount}/nInvestment Time Horizon: {investment_time_horizon}")

if __name__ == "__main__":
    app = App()
    # Runs the app
    app.mainloop()    
