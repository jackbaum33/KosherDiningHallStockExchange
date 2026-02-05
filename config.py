# --- CONFIGURATION ---
FRIENDS = ["Josh", "Jack", "Levi", "Shap", "Eitan", "Jonny", "Fisher", "Isaac", 
           "Charlie", "James", "Max", "Matan", "Sam", "Noah", "Jamie", "Oliver"]

CHICKEN_INDEX = [
    "Teriyaki Chicken", "North African Chicken", "Chicken Chimichurri", 
    "Chicken Tostada", "BBQ Chicken Drumsticks", "Chicken Fried Rice", 
    "Chicken Dakota", "Chicken Bahn Mi Sandwich", "BBQ Chicken on White Bun", 
    "Lebanese Chicken", "Herb Baked Chicken Thighs", "Roasted Chicken", 
    "Italian Chicken", "Taco Chicken", "Schwarma Pita Folds", "Gyro Chicken"
]

BEEF_INDEX = [
    "Beef and Three Mushroom Goulash", "Korean Chuck Eye", "Slow Roasted Chuck Eye", 
    "Beef Stew", "Beef Mostaccioli", "Sloppy Joes", "Beef Bulgogi", 
    "Sloppy Joe on Pretzel Bun", "Roast Beef Chipotle on Baguette", "Beef Hot Dogs", 
    "Corned Beef Sandwich", "Corned Beef", "Hamburger on Pretzel Bun", 
    "Lamb Gyro", "Lamb Korma", "Lamb Meatballs w/ Green Harissa Sauce"
]

MISC_INDEX = [
    "Turkey Chipotle on Baguette", "Turkey Dogs", "Kosher Deli", 
    "Salmon Chimmichuri", "Honey Glazed Salmon", "Whitefish RAS AL HANOUT", 
    "UNIT CHOICE MEAL", "Roasted Turkey Breast", "Brown Sugar Oatmeal", "Scrambled Eggs"
]

ALL_MEALS = CHICKEN_INDEX + BEEF_INDEX + MISC_INDEX

MEAL_CATEGORIES = {
    'Chicken': CHICKEN_INDEX,
    'Beef': BEEF_INDEX,
    'Misc': MISC_INDEX
}

# Trading configuration
INITIAL_BALANCE = 10000.0
INITIAL_HOUSE_SUPPLY = 500
IPO_START_PRICE = 200.0
IPO_DECAY_RATE = 1.0  # dollars per 3 seconds
IPO_DECAY_INTERVAL = 3  # seconds