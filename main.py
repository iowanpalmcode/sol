import streamlit as st
import random
import time
import json
import os
import streamlit.components.v1 as components

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
    {"planet": "Earth", "name": "Earthling", "preferences": ["Space Stew"], "credits": 150},
    {"planet": "Earth", "name": "Hungry Man", "preferences": ["Cosmopolitan Ice Cream"], "credits": 150},
    {"planet": "Earth", "name": "Gym Bro", "preferences": ["Space Stew"], "credits": 150},
    {"planet": "Earth", "name": "Health Nut", "preferences": ["Cosmopolitan Ice Cream"], "credits": 150},
    {"planet": "Mars", "name": "Martian", "preferences": ["Martian Salad"], "credits": 200},
    {"planet": "Mars", "name": "Space Miner", "preferences": ["Martian Salad"], "credits": 200},
    {"planet": "Venus", "name": "Venusian", "preferences": ["Venusian Soup"], "credits": 250},
    {"planet": "55 Cancri e", "name": "Cancrian", "preferences": ["Exoplanet Elixir"], "credits": 300},
    {"planet": "WASP-76b", "name": "WASPian", "preferences": ["Nebula Nachos"], "credits": 350},
    {"planet": "Kepler-10b", "name": "Keplerian", "preferences": ["Galactic Gumbo"], "credits": 400},
    {"planet": "Gliese 436 b", "name": "Gliesian", "preferences": ["The Hot Stuff"], "credits": 450},
    {"planet": "CoRoT-7b", "name": "CoRoTian", "preferences": ["Nebula Noodles"], "credits": 500},
    {"planet": "Kepler-22b", "name": "Kepler-22ian", "preferences": ["Lunar Lasagna"], "credits": 550},
    {"planet": "K2-18b", "name": "K2-18ian", "preferences": ["Solar Flare Fajitas"], "credits": 600},
    {"planet": "GJ 1214 b", "name": "GJ 1214ian", "preferences": ["Solar Flare Fajitas"], "credits": 650},
    {"planet": "LHS 1140 b", "name": "LHS 1140ian", "preferences": ["Lunar Lasagna"], "credits": 700},
    {"planet": "TRAPPIST-1e", "name": "TRAPPISTian", "preferences": ["Stellar Stir-Fry"], "credits": 750},
    {"planet": "HD 189733 b", "name": "HD 189733ian", "preferences": ["Meteorite Meatballs"], "credits": 800},
    {"planet": "WASP-12b", "name": "WASP-12ian", "preferences": ["Astro Omelette"], "credits": 850},
    {"planet": "Kepler-16b", "name": "Kepler-16ian", "preferences": ["Binary-Sun Paella"], "credits": 900},
    {"planet": "WASP-17b", "name": "WASP-17ian", "preferences": ["Puffy-Cloud Pancakes"], "credits": 950},
    {"planet": "PSR B1257+12 c", "name": "PSR B1257+12ian", "preferences": ["Gamma-Ray Risotto"], "credits": 1000},
    {"planet": "Proxima Centauri b", "name": "Proxima Centaurian", "preferences": ["Red-Dwarf Jam"], "credits": 1050},
    {"planet": "Kepler-452b", "name": "Kepler-452ian", "preferences": ["Ancient Solar Bread"], "credits": 1100},
    {"planet": "TRAPPIST-1f", "name": "TRAPPIST-1fian", "preferences": ["Frost-Bloom Sorbet"], "credits": 1150},
    {"planet": "Teegarden's Star b", "name": "Teegarden's Starian", "preferences": ["Velvet Moss Salad"], "credits": 1250},
]

customeremojis = {
    "Earth": "🌍", "Mars": "🔴", "Venus": "♀️", "55 Cancri e": "💎", "WASP-76b": "🌧️",
    "Kepler-10b": "🌋", "Gliese 436 b": "🔥", "CoRoT-7b": "⚡", "Kepler-22b": "🌊",
    "K2-18b": "🍯", "GJ 1214 b": "🍬", "LHS 1140 b": "🍄", "TRAPPIST-1e": "🍵",
    "HD 189733 b": "🔹", "WASP-12b": "🥚", "Kepler-16b": "🌞", "WASP-17b": "☁️",
    "PSR B1257+12 c": "🧄", "Proxima Centauri b": "🍓", "Kepler-452b": "🌾",
    "TRAPPIST-1f": "❄️", "Teegarden's Star b": "🍀"
}

# --- PERSISTENCE SYSTEM ---
def get_save_file(username):
    return f"save_{username.lower().replace(' ', '_')}.json"

def save_game(username):
    save_data = {
        "inventory": st.session_state.inventory,
        "credits": st.session_state.credits,
        "ship_level": st.session_state.ship_level,
        "location": st.session_state.location,
        "rebirths": st.session_state.rebirths,
        "password": st.session_state.password,
    }
    with open(get_save_file(username), "w") as f:
        json.dump(save_data, f)

def load_game(username):
    filename = get_save_file(username)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            st.session_state.inventory = data.get("inventory", {})
            st.session_state.credits = data.get("credits", 0)
            st.session_state.ship_level = data.get("ship_level", 1)
            st.session_state.location = data.get("location", "Earth")
            st.session_state.rebirths = data.get("rebirths", 0)
            st.session_state.password = data.get("password", "")
    else:
        st.session_state.inventory = {}
        st.session_state.credits = 0
        st.session_state.ship_level = 1
        st.session_state.location = "Earth"
        st.session_state.rebirths = 0
        # Password is set during the registration phase of login

# --- INITIALIZATION ---
st.set_page_config(page_title="Cosmopolitan", page_icon="🚀", layout="wide")

# --- LOGIN SYSTEM WITH VISUALS ---
if 'username' not in st.session_state:
    # Landing Page Visuals
    st.markdown("""
        <style>
        .main-title {
            font-size: 60px !important;
            text-align: center;
            color: white;
            text-shadow: 2px 2px #ff00ff, 4px 4px #00ffff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">🚀 COSMOPOLITAN</h1>', unsafe_allow_html=True)
    # Stunning space visual
    st.image("https://images.unsplash.com/photo-1462331940025-496a885651ad?q=80&w=2080&auto=format&fit=crop", 
             use_column_width=True, caption="The Galactic Kitchen Awaits...")

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("---")
        # We use a state machine for the login process
        if 'auth_step' not in st.session_state:
            st.session_state.auth_step = "NAME"

        if st.session_state.auth_step == "NAME":
            name = st.text_input("Enter your Pilot Name:", "")
            if st.button("Proceed"):
                if name:
                    st.session_state.temp_name = name
                    # Check if account exists
                    if os.path.exists(get_save_file(name)):
                        st.session_state.auth_step = "LOGIN"
                    else:
                        st.session_state.auth_step = "REGISTER"
                    st.rerun()
                else:
                    st.error("Name cannot be empty!")

        elif st.session_state.auth_step == "LOGIN":
            st.info(f"Welcome back, Pilot {st.session_state.temp_name}! Please verify your identity.")
            pwd = st.text_input("Enter Password:", type="password")
            if st.button("Login"):
                # Peek at the password in the file
                with open(get_save_file(st.session_state.temp_name), "r") as f:
                    data = json.load(f)
                    if pwd == data.get("password"):
                        st.session_state.username = st.session_state.temp_name
                        st.session_state.password = pwd
                        st.session_state.auth_step = "COMPLETE"
                        st.rerun()
                    else:
                        st.error("Incorrect password!")
                
        elif st.session_state.auth_step == "REGISTER":
            st.info(f"Welcome, New Pilot! Create your credentials for {st.session_state.temp_name}.")
            pwd = st.text_input("Create a Password:", type="password")
            confirm_pwd = st.text_input("Confirm Password:", type="password")
            if st.button("Initialize Account"):
                if pwd and pwd == confirm_pwd:
                    st.session_state.username = st.session_state.temp_name
                    st.session_state.password = pwd
                    # Create initial file
                    load_game(st.session_state.username)
                    save_game(st.session_state.username)
                    st.session_state.auth_step = "COMPLETE"
                    st.rerun()
                else:
                    st.error("Passwords do not match or are empty!")

    st.stop() # Stop execution until login is complete

# Load game after username is established
if 'game_loaded' not in st.session_state:
    load_game(st.session_state.username)
    st.session_state.game_loaded = True

if 'active_customers' not in st.session_state: 
    st.session_state.active_customers = []
if 'music_enabled' not in st.session_state:
    st.session_state.music_enabled = True
if 'reset_step' not in st.session_state:
    st.session_state.reset_step = 0

# --- AUDIO SYSTEM (HIDDEN) ---
if st.session_state.music_enabled:
    audio_html = """
        <audio autoplay loop style="display:none;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementsByTagName('audio')[0];
            audio.volume = 0.5;
        </script>
    """
    components.html(audio_html, height=0)

st.title("🚀 Cosmopolitan")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌌 Explore", "🍳 Cook","📦 Cargo","📖 Recipes","🥄 Restaurant", "⚙️ Settings"])

with st.sidebar:
    st.header("Ship Status")
    st.write(f"**Pilot:** {st.session_state.username}")
    st.write(f"Level: {st.session_state.ship_level}")
    st.write(f"Credits: {st.session_state.credits}")
    
    cost = st.session_state.ship_level * 100
    if st.button(f"Upgrade Ship ({cost} credits)"):
        if st.session_state.credits >= cost:
            st.session_state.credits -= cost
            st.session_state.ship_level += 1
            save_game(st.session_state.username)
            st.success("Ship upgraded!")
            st.rerun()
        else:
            st.error("Not enough credits!")
            
    st.write(f"Current Location: {st.session_state.location}")
    st.write("---")
    
    rebirth_cost = 15000 * (1.5 ** st.session_state.rebirths)
    if st.button(f"Rebirth ({int(rebirth_cost)} credits)"):
        if st.session_state.credits >= rebirth_cost:
            st.session_state.credits -= rebirth_cost
            st.session_state.rebirths += 1
            st.session_state.inventory.clear()
            st.session_state.credits = 0
            st.session_state.ship_level = 1
            st.session_state.location = "Earth"
            save_game(st.session_state.username)
            st.success("Reborn!")
            st.rerun()
        else:
            st.error("Not enough credits!")
    st.write(f"Rebirths: {st.session_state.rebirths}")

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
    save_game(st.session_state.username)

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
        st.balloons()
        st.success(f"Gathered: {', '.join(PLANET_INFO[planet]['ingredients'])}")
        save_game(st.session_state.username)
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
            save_game(st.session_state.username)
            st.success(f"Cooked {recipe}!")
        else:
            st.error("Missing ingredients!")

with tab3:
    st.header("Cargo")
    planet_filter = st.selectbox("Filter cargo by planet of origin:", ["All"] + list(PLANET_INFO.keys()))
    all_items = list(st.session_state.inventory.items())
    if planet_filter != "All":
        allowed_ingredients = PLANET_INFO[planet_filter]["ingredients"]
        cargo_options = [item for item, qty in all_items if item in allowed_ingredients]
        st.write(f"Showing items from {planet_filter}:")
    else:
        cargo_options = [item for item, qty in all_items]
    if not cargo_options:
        st.write("Cargo hold is empty or no matching items found.")
    for ing in cargo_options:
        st.write(f"{ing}: {st.session_state.inventory[ing]} units")

with tab4:
    st.header("Recipe Book")
    ingredient_filter = st.multiselect("Filter recipes by ingredients:", list(set(ing for r in RECIPES.values() for ing in r["ingredients"])))
    if ingredient_filter:
        recipe_options = [r for r, details in RECIPES.items() if all(ing in details["ingredients"] for ing in ingredient_filter)]
    else:
        recipe_options = list(RECIPES.keys())
    for r in recipe_options:
        st.write(f"**{r}** (Requires: {', '.join(RECIPES[r]['ingredients'])}, Rewards: {RECIPES[r]['credits']} credits)")

with tab5:
    st.header("Restaurant")
    if not st.session_state.active_customers:
        potential = [c for c in customers if all(st.session_state.inventory.get(meal, 0) > 0 for meal in c["preferences"])]
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
                        if all(st.session_state.inventory.get(meal, 0) > 0 for meal in customer["preferences"]):
                            for meal in customer["preferences"]:
                                st.session_state.inventory[meal] -= 1
                            st.session_state.credits += customer["credits"]
                            save_game(st.session_state.username)
                            st.session_state.active_customers.pop(idx)
                            st.rerun()
                        else:
                            st.error("You don't have the prepared meal!")

            if leaving_indices:
                for index in sorted(leaving_indices, reverse=True):
                    cust_who_left = st.session_state.active_customers.pop(index)
                    st.session_state.credits = max(0, st.session_state.credits - 50)
                    save_game(st.session_state.username)
                st.rerun()
        time.sleep(1)
        st.rerun()

with tab6:
    st.header("Settings")
    
    # 1. Audio
    st.subheader("Audio")
    music_on = st.toggle("Enable Background Music", value=st.session_state.music_enabled)
    if music_on != st.session_state.music_enabled:
        st.session_state.music_enabled = music_on
        st.rerun()

    st.write("---")
    
    # 2. Change Password
    st.subheader("Security")
    if st.button("Change Password"):
        st.session_state.changing_pwd = True
    
    if st.session_state.get('changing_pwd'):
        with st.expander("Updating Password", expanded=True):
            old_p = st.text_input("Current Password:", type="password")
            new_p = st.text_input("New Password:", type="password")
            conf_p = st.text_input("Confirm New Password:", type="password")
            
            if st.button("Update Password"):
                if old_p == st.session_state.password:
                    if new_p == conf_p and new_p != "":
                        st.session_state.password = new_p
                        save_game(st.session_state.username)
                        st.success("Password updated successfully!")
                        st.session_state.changing_pwd = False
                        st.rerun()
                    else:
                        st.error("New passwords do not match or are empty!")
                else:
                    st.error("Current password incorrect!")
            if st.button("Cancel"):
                st.session_state.changing_pwd = False
                st.rerun()

    st.write("---")
    st.subheader("Danger Zone")
    if st.session_state.reset_step == 0:
        if st.button("Reset All Progress"):
            st.session_state.reset_step = 1
            st.rerun()
    elif st.session_state.reset_step == 1:
        st.warning("Are you sure you want to wipe your save file?")
        if st.button("Yes, I'm sure"):
            st.session_state.reset_step = 2
            st.rerun()
        if st.button("No, go back"):
            st.session_state.reset_step = 0
            st.rerun()
    elif st.session_state.reset_step == 2:
        st.error("ARE YOU ABSOLUTELY SURE? This cannot be undone!")
        if st.button("YES, WIPE EVERYTHING"):
            st.session_state.inventory = {}
            st.session_state.credits = 0
            st.session_state.ship_level = 1
            st.session_state.location = "Earth"
            st.session_state.rebirths = 0
            filename = get_save_file(st.session_state.username)
            if os.path.exists(filename):
                os.remove(filename)
            st.session_state.reset_step = 0
            st.success("Game Reset!")
            st.rerun()
        if st.button("Wait, no!"):
            st.session_state.reset_step = 0
            st.rerun()
