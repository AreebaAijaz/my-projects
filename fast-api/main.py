from fastapi import FastAPI
import random

app = FastAPI()

# 1. Use lists instead of sets
side_hustles = [
    "Freelancing - Start offering your services online.",
    "Dropshipping - Sell products online without holding inventory.",
    "Affiliate Marketing - Promote products and earn commissions.",
    "Online Tutoring - Teach subjects or skills through video calls.",
    "Content Creation – Create videos or posts and monetize your audience.",
    "Sell Digital Products – Make and sell eBooks, templates, or tools.",
    "Social Media Management – Manage accounts for small businesses.",
    "Stock Photography – Sell your photos on stock platforms.",
    "Print on Demand – Design and sell custom products like shirts or mugs.",
    "Virtual Assistant – Help businesses with admin tasks remotely."
]

money_quotes = [
    "Don’t tell me what you value, show me your budget, and I'll tell you what you value. — Joe Biden",
    "Too many people spend money they haven't earned, to buy things they don't want, to impress people they don't like. — Will Rogers",
    "An investment in knowledge pays the best interest. — Benjamin Franklin",
    "The rich invest in time, the poor invest in money. — Warren Buffett",
    "It’s not your salary that makes you rich, it's your spending habits. — Charles A. Jaffe",
    "Never spend your money before you have earned it. — Thomas Jefferson",
    "Do not save what is left after spending, but spend what is left after saving. — Warren Buffett",
    "Money is only a tool. It will take you wherever you wish, but it will not replace you as the driver. — Ayn Rand",
    "Formal education will make you a living; self-education will make you a fortune. — Jim Rohn",
    "The goal isn’t more money. The goal is living life on your own terms. — Chris Brogan"
]

@app.get("/side_hustles")
def get_side_hustles():
    """Returns a random side hustle idea"""
    return {"side_hustle": random.choice(side_hustles)}

@app.get("/money_quotes")
def get_money_quotes():
    """Returns a random money quote"""
    return {"money_quote": random.choice(money_quotes)}
