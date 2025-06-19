import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pickle
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import numpy as np

class TravelPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Prediction Dashboard")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Initialize travel data
        self.travel_data = self.load_data()
        
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#4361ee", padx=20, pady=20)
        header_frame.grid(row=0, column=0, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            header_frame, text="🚀 Travel Prediction Dashboard", 
            font=("Arial", 20, "bold"), bg="#4361ee", fg="white"
        ).pack()
        
        tk.Label(
            header_frame, text="Track your travel patterns and predict future journeys using linear regression", 
            font=("Arial", 10), bg="#4361ee", fg="white"
        ).pack()
        
        # Main content
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel (Input)
        input_frame = ttk.LabelFrame(main_frame, text="📊 Add Travel Data", padding=15)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Form inputs
        tk.Label(input_frame, text="Date:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, sticky="ew", pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(input_frame, text="Distance (km):", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        self.distance_entry = tk.Entry(input_frame)
        self.distance_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        tk.Label(input_frame, text="Cost (₹):", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
        self.cost_entry = tk.Entry(input_frame)
        self.cost_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        add_button = tk.Button(
            input_frame, text="Add Travel Record", 
            bg="#4361ee", fg="white", command=self.add_travel_record
        )
        add_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Right panel (Prediction)
        prediction_frame = ttk.LabelFrame(main_frame, text="🔮 Predict 8th Day Travel", padding=15)
        prediction_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        predict_button = tk.Button(
            prediction_frame, text="Predict Future Travel", 
            bg="#3a0ca3", fg="white", command=self.predict_future_travel
        )
        predict_button.pack(fill="x", pady=10)
        
        self.prediction_result = tk.Frame(prediction_frame)
        self.prediction_result.pack(fill="x", pady=5)
        
        self.chart_frame = tk.Frame(prediction_frame)
        self.chart_frame.pack(fill="both", expand=True)
        
        # Bottom panel (History)
        history_frame = ttk.LabelFrame(main_frame, text="📝 Travel History", padding=15)
        history_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(1, weight=1)
        
        columns = ("date", "distance", "cost", "actions")
        self.tree = ttk.Treeview(
            history_frame, columns=columns, show="headings",
            selectmode="browse", height=10
        )
        
        self.tree.heading("date", text="Date")
        self.tree.heading("distance", text="Distance (km)")
        self.tree.heading("cost", text="Cost (₹)")
        self.tree.heading("actions", text="Actions")
        
        self.tree.column("date", width=150)
        self.tree.column("distance", width=100, anchor="center")
        self.tree.column("cost", width=100, anchor="center")
        self.tree.column("actions", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial render
        self.render_travel_data()
        
    def load_data(self):
        """Load travel data from file if exists"""
        if os.path.exists("travel_data.pkl"):
            with open("travel_data.pkl", "rb") as f:
                return pickle.load(f)
        return []
    
    def save_data(self):
        """Save travel data to file"""
        with open("travel_data.pkl", "wb") as f:
            pickle.dump(self.travel_data, f)
    
    def render_travel_data(self):
        """Render travel data in the treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not self.travel_data:
            return
            
        sorted_data = sorted(self.travel_data, key=lambda x: x['date'], reverse=True)
        
        for idx, item in enumerate(sorted_data):
            self.tree.insert("", "end", values=(
                item['date'].strftime("%Y-%m-%d"),
                f"{item['distance']:.1f}",
                f"{item['cost']:.2f}",
                "Delete"
            ), tags=(idx,))
            
        self.tree.tag_bind("delete", "<<TreeviewSelect>>", self.delete_record)
    
    def add_travel_record(self):
        """Add a new travel record"""
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
            distance = float(self.distance_entry.get())
            cost = float(self.cost_entry.get())
            
            if distance <= 0 or cost <= 0:
                raise ValueError("Values must be positive")
                
            new_record = {
                "date": date,
                "distance": distance,
                "cost": cost
            }
            
            self.travel_data.append(new_record)
            self.save_data()
            self.render_travel_data()
            
            # Clear inputs
            self.distance_entry.delete(0, "end")
            self.cost_entry.delete(0, "end")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
    
    def delete_record(self, event):
        """Delete selected travel record"""
        item = self.tree.selection()[0]
        index = int(self.tree.item(item, "tags")[0])
        
        if messagebox.askyesno("Confirm", "Delete this record?"):
            del self.travel_data[index]
            self.save_data()
            self.render_travel_data()
    
    def predict_future_travel(self):
        """Predict travel for 8 days from now"""
        if len(self.travel_data) < 3:
            messagebox.showwarning(
                "Not Enough Data", 
                "You need at least 3 travel records to make a prediction"
            )
            return
            
        # Clear previous prediction and chart
        for widget in self.prediction_result.winfo_children():
            widget.destroy()
            
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Prepare data for regression
        sorted_data = sorted(self.travel_data, key=lambda x: x['date'])
        
        # Convert dates to numeric (days since first record)
        first_date = sorted_data[0]['date']
        X = np.array([(d['date'] - first_date).days for d in sorted_data]).reshape(-1, 1)
        y = np.array([d['distance'] for d in sorted_data])
        
        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate prediction for 8 days from now
        today = datetime.now()
        prediction_date = today + timedelta(days=8)
        days_since_first = (prediction_date - first_date).days
        predicted_distance = model.predict([[days_since_first]])[0]
        
        # Calculate average cost per km and predict cost
        total_distance = sum(d['distance'] for d in self.travel_data)
        total_cost = sum(d['cost'] for d in self.travel_data)
        avg_cost_per_km = total_cost / total_distance
        predicted_cost = predicted_distance * avg_cost_per_km
        
        # Display prediction results
        tk.Label(
            self.prediction_result, 
            text=f"Predicted travel on {prediction_date.strftime('%Y-%m-%d')}:",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        tk.Label(
            self.prediction_result, 
            text=f"Distance: {predicted_distance:.1f} km",
            font=("Arial", 10, "bold"),
            fg="#4361ee"
        ).pack(anchor="w")
        
        tk.Label(
            self.prediction_result, 
            text=f"Estimated cost: ₹{predicted_cost:.2f}",
            font=("Arial", 10, "bold"),
            fg="#4361ee"
        ).pack(anchor="w")
        
        # Create and display regression chart
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter(X, y, color='blue', label='Actual Data')
        
        # Plot regression line
        x_line = np.linspace(0, days_since_first, 100).reshape(-1, 1)
        y_line = model.predict(x_line)
        ax.plot(x_line, y_line, color='red', label='Regression Line')
        
        # Plot prediction point
        ax.scatter([days_since_first], [predicted_distance], color='green', 
                   s=100, label='8th Day Prediction')
        
        ax.set_xlabel('Days Since First Record')
        ax.set_ylabel('Distance (km)')
        ax.set_title('Travel Distance Prediction')
        ax.legend()
        ax.grid(True)
        
        # Embed chart in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelPredictionApp(root)
    root.mainloop()
