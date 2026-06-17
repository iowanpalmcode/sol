import streamlit as st
import random
import time
import json
import os

# --- PERSISTENCE SYSTEM (SAVE/LOAD) ---
# SAVE_FILE = "savegame.json"

def save_game():
    """Saves the current session state to a JSON file."""
    save_data = {
        "inventory": st.session_state.inventory,
        "credits": st.session_state.credits,
        "ship_level": st.session_state.ship_level,
        "location": st.session_state.location,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(save_data, f)

def load_game():
    """Loads data from the JSON file into session state."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            st.session_state.inventory = data.get("inventory", {})
            st.session_state.credits = data.get("credits", 0)
            st.session_state.ship_level = data.get("ship_level", 1)
            st.session_state.location = data.get("location", "Earth")
    else:
        # Default starting values if no save file exists
        st.session_state.inventory = {}
        st.session_state.credits = 0
        st.session_state.ship_level = 1
        st.session_state.location = "Earth"

# --- DATA CONFIGURATION ---
PLANET_INFO = {
    "Earth": {"ingredients": ["Water", "Oxygen", "Food"], "base_price": 100},
    "Mars": {"ingredients": ["Iron", "Silicon", "Water"], "base_price": 150},
    "Venus": {"ingredients": ["Sulfuric Acid", "Carbon Dioxide"], "base_price": 200},
    "55 Cancri e": {"ingredients": ["Diamond", "Salt"], "base_price": 300},
    "WASP-76b": {"ingredients": ["Iron", "Rain"], "base_price": 350},
    "Kepler-10b": {"ingredients": ["Magma", "Marmalade"], "base_price": 400},
    "Gliese 436 b": {"ingredients": ["Burning", "Ice"], "base_price": 450},
    "CoRoT-7b": {"ingredients": ["Heavy", "Metal"], "base_price": 500},
    "Kepler-22b": {"ingredients": ["Abyssal Kelp"], "base_price": 550},
    "K2-18b": {"ingredients": ["Hydrogen-Mist Honey"], "base_price": 600},
    "GJ 1214 b": {"ingredients": ["Steam-Condensed Sugar"], "base_price": 650},
    "LHS 1140 b": {"ingredients": ["Glacial Truffles"], "base_price": 700},
    "TRAPPIST-1e": {"ingredients": ["Tidal-Lock Tea Leaves"], "base_price": 750},
    "HD 189733 b": {"ingredients": ["Cobalt Glass Shards"], "base_price": 800},
    "WASP-12b": {"ingredients": ["Egg-Shaped Essence"], "base_price": 850},
    "Kepler-16b": {"ingredients": ["Binary-Sun Saffron"], "base_price": 900},
    "WASP-17b": {"ingredients": ["Puffy-Cloud Flour"], "base_price": 950},
    "PSR B1257+12 c": {"ingredients": ["Gamma-Ray Garlic"], "base_price": 1000},
    "Proxima Centauri b": {"ingredients": ["Red-Dwarf Berries"], "base_price": 1050},
    "Kepler-452b": {"ingredients": ["Ancient Solar Grain"], "base_price": 1100},
    "TRAPPIST-1f": {"ingredients": ["Frost-Bloom Flower"], "base_price": 1150},
    "LHS 1140 b_2": {"ingredients": ["Deep-Silt Pepper"], "base_price": 1200}, 
    "Teegarden's Star b": {"ingredients": ["Velvet Moss"], "base_price": 1250}
}

RECIPES = {
    "Space Stew": {"ingredients": ["Water", "Food"], "credits": 150},
    "Martian Salad": {"ingredients": ["Iron", "Silicon"], "credits": 200},
    "Venusian Soup": {"ingredients": ["Sulfuric Acid", "Carbon Dioxide"], "credits": 250},
    "Cosmopolitan Ice Cream": {"ingredients": ["Water", "Oxygen"], "credits": 300},
    "Exoplanet Elixir": {"ingredients": ["Diamond", "Salt"], "credits": 400},
    "Galactic Gumbo": {"ingredients": ["Magma", "Marmalade"], "credits": 450},
    "Nebula Noodles": {"ingredients": ["Heavy", "Metal"], "credits": 500},
    "Stellar Stir-Fry": {"ingredients": ["Tidal-Lock Tea Leaves"], "credits": 550},
    "The Hot Stuff": {"ingredients": ["Burning", "Ice"], "credits": 600},
    "Solar Flare Fajitas": {"ingredients": ["Hydrogen-Mist Honey", "Steam-Condensed Sugar"], "credits": 650},
    "Lunar Lasagna": {"ingredients": ["Glacial Truffles", "Tidal-Lock Tea Leaves"], "credits": 700},
    "Meteorite Meatballs": {"ingredients": ["Cobalt Glass Shards", "Egg-Shaped Essence"], "credits": 750},
    "Astro Avocado Toast": {"ingredients": ["Binary-Sun Saffron", "Puffy-Cloud Flour"], "credits": 800},
    "Cosmic Curry": {"ingredients": ["Gamma-Ray Garlic", "Red-Dwarf Berries"], "credits": 850},
    "Chicken of the Cosmos": {"ingredients": ["Ancient Solar Grain", "Frost-Bloom Flower"], "credits": 900},
    "Galactic Gazpacho": {"ingredients": ["Deep-Silt Pepper", "Velvet Moss"], "credits": 950},
    "Nebula Nachos": {"ingredients": ["Water", "Iron", "Sulfuric Acid"], "credits": 500},
    "Stellar Sushi": {"ingredients": ["Oxygen", "Silicon", "Carbon Dioxide"], "credits": 550},
    "Astro Omelette": {"ingredients": ["Egg-Shaped Essence"], "credits": 650},
    "Binary-Sun Paella": {"ingredients": ["Binary-Sun Saffron"], "credits": 700},
    "Puffy-Cloud Pancakes": {"ingredients": ["Puffy-Cloud Flour"], "credits": 750},
    "Gamma-Ray Risotto": {"ingredients": ["Gamma-Ray Garlic"], "credits": 800},
    "Red-Dwarf Jam": {"ingredients": ["Red-Dwarf Berries"], "credits": 850},
    "Ancient Solar Bread": {"ingredients": ["Ancient Solar Grain"], "credits": 900},
    "Frost-Bloom Sorbet": {"ingredients": ["Frost-Bloom Flower"], "credits": 950},
    "Deep-Silt Chili": {"ingredients": ["Deep-Silt Pepper"], "credits": 1000},
    "Velvet Moss Salad": {"ingredients": ["Velvet Moss"], "credits": 1050},
    "Teegarden's Tacos": {"ingredients": ["Velvet Moss", "Gamma-Ray Garlic"], "credits": 1100},
    "The Ultimate Space Feast": {"ingredients": ["Diamond", "Magma", "Heavy", "Tidal-Lock Tea Leaves", "Cobalt Glass Shards"], "credits": 1500}
}

randomeventdict = {
    "pirates": {"description": "Encountered space pirates! Lost some credits.", "effect": lambda: (random.randint(-200, -50), {})},
    "asteroid": {"description": "Navigated an asteroid field! Found a rare ingredient.", "effect": lambda: (0, {"Asteroid Ore": 1})},
    "aliens": {"description": "Encountered friendly aliens! Gained credits.", "effect": lambda: (random.randint(100, 300), {})},
    "nothing": {"description": "Exploration was uneventful.", "effect": lambda: (0, {})},
    "Cosmopolitan Party": {"description": "Attended a space party! Gained credits and a cocktail.", "effect": lambda: (random.randint(50, 150), {"Cosmopolitan Cocktail": 1})},
    "Space Llama": {"description": "Encountered a space llama! Gained wool but lost credits.", "effect": lambda: (random.randint(-100, -20), {"Space Llama Wool": 1})},
    "Black Hole": {"description": "Got too close to a black hole! Lost everything!", "effect": lambda: ("RESET", {})},
    "Wormhole": {"description": "Traveled through a wormhole! Teleported and gathered local items.", "effect": lambda: ("WARP", {})},
    "Supernova": {"description": "Witnessed a supernova! Gained cosmic dust.", "effect": lambda: (random.randint(-150, -50), {"Cosmic Dust": 1})},
    "Time Dilation": {"description": "Time dilation! Gained Neutron Star Spice.", "effect": lambda: (random.randint(-120, -30), {"Neutron Star Spice": 1})},
    "Alien Market": {"description": "Traded credits for an Alien Artifact.", "effect": lambda: (random.randint(-200, -50), {"Alien Artifact": 1})},
    "Space Anomaly": {"description": "Found a Space Anomaly!", "effect": lambda: (random.randint(-100, -20), {random.choice(["Anomalous Crystal", "Quantum Spice", "Dark Matter Essence"]): 1})},
    "Cosmic Storm": {"description": "Cosmic storm! Lost credits.", "effect": lambda: (random.randint(-150, -50), {})},
    "Galactic Festival": {"description": "Attended a festival! Gained a souvenir.", "effect": lambda: (random.randint(50, 150), {"Festival Souvenir": 1})},
    "Asteroid Mining": {"description": "Found rich minerals!", "effect": lambda: (random.randint(100, 300), {"Asteroid Ore": 1})}
}

customers = [
    {"planet": "Earth", "name": "Earthling", "preferences": ["Water", "Food"], "credits": 150},
    {"planet": "Earth", "name": "Hungry Man", "preferences": ["Water", "Iron"], "credits": 150},
    {"planet": "Earth", "name": "Gym Bro", "preferences": ["Food", "Iron","Salt"], "credits": 150},
    {"planet": "Earth", "name": "Health Nut", "preferences": ["Water", "Oxygen","Glacial Truffles"], "credits": 150},
    {"planet": "Mars", "name": "Martian", "preferences": ["Iron", "Silicon"], "credits": 200},
    {"planet": "Mars", "name": "Space Miner", "preferences": ["Iron", "Heavy"], "credits": 200},
    {"planet": "Venus", "name": "Venusian", "preferences": ["Sulfuric Acid", "Carbon Dioxide"], "credits": 250},
    {"planet": "55 Cancri e", "name": "Cancrian", "preferences": ["Diamond", "Salt"], "credits": 300},
    {"planet": "WASP-76b", "name": "WASPian", "preferences": ["Iron", "Rain"], "credits": 350},
    {"planet": "Kepler-10b", "name": "Keplerian", "preferences": ["Magma", "Marmalade"], "credits": 400},
    {"planet": "Gliese 436 b", "name": "Gliesian", "preferences": ["Burning", "Ice"], "credits": 450},
    {"planet": "CoRoT-7b", "name": "CoRoTian", "preferences": ["Heavy", "Metal"], "credits": 500},
    {"planet": "Kepler-22b", "name": "Kepler-22ian", "preferences": ["Abyssal Kelp"], "credits": 550},
    {"planet": "K2-18b", "name": "K2-18ian", "preferences": ["Hydrogen-Mist Honey"], "credits": 600},
    {"planet": "GJ 1214 b", "name": "GJ 1214ian", "preferences": ["Steam-Condensed Sugar"], "credits": 650},
    {"planet": "LHS 1140 b", "name": "LHS 1140ian", "preferences": ["Glacial Truffles"], "credits": 700},
    {"planet": "TRAPPIST-1e", "name": "TRAPPISTian", "preferences": ["Tidal-Lock Tea Leaves"], "credits": 750},
    {"planet": "HD 189733 b", "name": "HD 189733ian", "preferences": ["Cobalt Glass Shards"], "credits": 800},
    {"planet": "WASP-12b", "name": "WASP-12ian", "preferences": ["Egg-Shaped Essence"], "credits": 850},
    {"planet": "Kepler-16b", "name": "Kepler-16ian", "preferences": ["Binary-Sun Saffron"], "credits": 900},
    {"planet": "WASP-17b", "name": "WASP-17ian", "preferences": ["Puffy-Cloud Flour"], "credits": 950},
    {"planet": "PSR B1257+12 c", "name": "PSR B1257+12ian", "preferences": ["Gamma-Ray Garlic"], "credits": 1000},
    {"planet": "Proxima Centauri b", "name": "Proxima Centaurian", "preferences": ["Red-Dwarf Berries"], "credits": 1050},
    {"planet": "Kepler-452b", "name": "Kepler-452ian", "preferences": ["Ancient Solar Grain"], "credits": 1100},
    {"planet": "TRAPPIST-1f", "name": "TRAPPIST-1fian", "preferences": ["Frost-Bloom Flower"], "credits": 1150},
    {"planet": "Teegarden's Star b", "name": "Teegarden's Starian", "preferences": ["Velvet Moss"], "credits": 1250},
]

customeremojis = {
    "Earth": "🌍", "Mars": "🔴", "Venus": "♀️", "55 Cancri e": "💎", "WASP-76b": "🌧️",
    "Kepler-10b": "🌋", "Gliese 436 b": "🔥", "CoRoT-7b": "⚡", "Kepler-22b": "🌊",
    "K2-18b": "🍯", "GJ 1214 b": "🍬", "LHS 1140 b": "🍄", "TRAPPIST-1e": "🍵",
    "HD 189733 b": "🔹", "WASP-12b": "🥚", "Kepler-16b": "🌞", "WASP-17b": "☁️",
    "PSR B1257+12 c": "🧄", "Proxima Centauri b": "🍓", "Kepler-452b": "🌾",
    "TRAPPIST-1f": "❄️", "Teegarden's Star b": "🍀"
}

# --- INITIALIZE SESSION STATE ---
# Load from file immediately
load_game()

if 'active_customers' not in st.session_state: 
    st.session_state.active_customers = []

st.set_page_config(page_title="Cosmopolitan", page_icon="🚀", layout="wide")
st.title("🚀 Cosmopolitan")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌌 Explore", "🍳 Cook","📦 Cargo","📖 Ingredients","📖 Recipes","🥄 Restaurant"])

with st.sidebar:
    st.header("Ship Status")
    st.write(f"Level: {st.session_state.ship_level}")
    st.write(f"Credits: {st.session_state.credits}")
    cost = st.session_state.ship_level * 100
    if st.button(f"Upgrade Ship ({cost} credits)"):
        if st.session_state.credits >= cost:
            st.session_state.credits -= cost
            st.session_state.ship_level += 1
            save_game() # SAVE after upgrade
            st.success("Ship upgraded!")
            st.rerun()
        else:
            st.error("Not enough credits!")

def random_event():
    choice = random.choice(list(randomeventdict.keys()))
    event = randomeventdict[choice]
    st.info(event["description"])
    credit_change, item_change = event["effect"]()
    if credit_change == "RESET":
        st.session_state.credits = 0
        st.session_state.inventory.clear()
    elif credit_change == "WARP":
        new_planet = random.choice(list(PLANET_INFO.keys()))
        st.session_state.location = new_planet
        for ing in PLANET_INFO[new_planet]["ingredients"]:
            st.session_state.inventory[ing] = st.session_state.inventory.get(ing, 0) + 1
        st.write(f"Teleported to {new_planet} and gathered ingredients!")
    else:
        st.session_state.credits += credit_change
        for item, qty in item_change.items():
            st.session_state.inventory[item] = st.session_state.inventory.get(item, 0) + qty
    save_game() # SAVE after event

with tab1:
    st.header("Explore")
    if st.session_state.ship_level <= 3:
        options = ["Earth", "Mars", "Venus"]
    elif st.session_state.ship_level <= 7:
        options = ["Earth", "Mars", "Venus", "55 Cancri e", "WASP-76b", "Kepler-10b"]
    elif st.session_state.ship_level <= 12:
        options = ["Earth", "Mars", "Venus", "55 Cancri e", "WASP-76b", "Kepler-10b", "Gliese 436 b", "CoRoT-7b", "Kepler-22b"]
    else:
        options = list(PLANET_INFO.keys())
    planet = st.selectbox("Select a planet to explore:", options)
    if st.button("Explore"):
        st.session_state.location = planet
        st.success(f"Exploring {planet}...")
        time.sleep(1)
        for ing in PLANET_INFO[planet]["ingredients"]:
            st.session_state.inventory[ing] = st.session_state.inventory.get(ing, 0) + 1
        st.success(f"Gathered: {', '.join(PLANET_INFO[planet]['ingredients'])}")
        save_game() # SAVE after gathering
        random_event()

with tab2:
    st.header("Cook")
    recipe = st.selectbox("Select a recipe to cook:", list(RECIPES.keys()))
    if st.button("Cook"):
        required = RECIPES[recipe]["ingredients"]
        if all(st.session_state.inventory.get(ing, 0) > 0 for ing in required):
            for ing in required:
                st.session_state.inventory[ing] -= 1
            st.session_state.inventory[recipe] = st.session_state.inventory.get(recipe, 0) + 1
            save_game() # SAVE after cooking
            st.success(f"Cooked {recipe}!")
        else:
            st.error("Missing ingredients!")

with tab3:
    st.header("Cargo")
    planet_filter = st.selectbox("Filter cargo by planet:", ["All"] + list(PLANET_INFO.keys()))
    if planet_filter != "All":
        cargo_options = [ing for ing in st.session_state.inventory if ing in PLANET_INFO[planet_filter]["ingredients"]]
    else:
        cargo_options = list(st.session_state.inventory.keys())
    for ing in cargo_options:
        st.write(f"{ing}: {st.session_state.inventory[ing]} units")

with tab4:
    st.header("Ingredients")
    planet_filter = st.selectbox("Filter ingredients by planet:", ["All"] + list(PLANET_INFO.keys()))
    if planet_filter != "All":
        inventory_options = [ing for ing in st.session_state.inventory if ing in PLANET_INFO[planet_filter]["ingredients"]]
    else:
        inventory_options = list(st.session_state.inventory.keys())
    for ing in inventory_options:
        st.write(f"{ing}: {st.session_state.inventory[ing]} units")

with tab5:
    st.header("Recipe Book")
    ingredient_filter = st.multiselect("Filter recipes by ingredients:", list(set(ing for r in RECIPES.values() for ing in r["ingredients"])))
    if ingredient_filter:
        recipe_options = [r for r, details in RECIPES.items() if all(ing in details["ingredients"] for ing in ingredient_filter)]
    else:
        recipe_options = list(RECIPES.keys())
    for r in recipe_options:
        st.write(f"**{r}** (Requires: {', '.join(RECIPES[r]['ingredients'])}, Rewards: {RECIPES[r]['credits']} credits)")

# --- RESTAURANT TAB ---
with tab6:
    st.header("Restaurant")
    
    if not st.session_state.active_customers:
        potential = [c for c in customers if all(st.session_state.inventory.get(ing, 0) > 0 for ing in c["preferences"])]
        if potential:
            selected = random.sample(potential, min(3, len(potential)))
            for s in selected:
                st.session_state.active_customers.append({"data": s, "arrival_time": time.time()})
        else:
            st.write("No customers are visiting right now.")

    if st.session_state.active_customers:
        container = st.container()
        with container:
            leaving_indices = []
            for idx, entry in enumerate(st.session_state.active_customers):
                customer = entry["data"]
                elapsed = time.time() - entry["arrival_time"]
                remaining = max(0, 30 - int(elapsed))
                
                if remaining <= 0:
                    leaving_indices.append(idx)
                    continue

                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    emoji = customeremojis.get(customer['planet'], "🚀")
                    st.write(f"**{customer['name']}** {emoji} (Wants: {', '.join(customer['preferences'])})")
                with col2:
                    st.write(f"⏳ {remaining}s")
                with col3:
                    st.write(f"Reward: {customer['credits']}¢")
                    if st.button(f"Serve", key=f"serve_{idx}"):
                        if all(st.session_state.inventory.get(ing, 0) > 0 for ing in customer["preferences"]):
                            for ing in customer["preferences"]:
                                st.session_state.inventory[ing] -= 1
                            st.session_state.credits += customer["credits"]
                            save_game() # SAVE after serving
                            st.session_state.active_customers.pop(idx)
                            potential = [c for c in customers if all(st.session_state.inventory.get(ing, 0) > 0 for ing in c["preferences"])]
                            if potential:
                                new_c = random.choice(potential)
                                st.session_state.active_customers.append({"data": new_c, "arrival_time": time.time()})
                            st.rerun()
                        else:
                            st.error("Missing ingredients!")

            if leaving_indices:
                for index in sorted(leaving_indices, reverse=True):
                    cust_who_left = st.session_state.active_customers.pop(index)
                    st.session_state.credits = max(0, st.session_state.credits - 50)
                    save_game() # SAVE after penalty
                    st.warning(f"{cust_who_left['data']['name']} left! Lost 50 credits.")
                    potential = [c for c in customers if all(st.session_state.inventory.get(ing, 0) > 0 for ing in c["preferences"])]
                    if potential:
                        new_c = random.choice(potential)
                        st.session_state.active_customers.append({"data": new_c, "arrival_time": time.time()})
                st.rerun()

        time.sleep(1)
        st.rerun()