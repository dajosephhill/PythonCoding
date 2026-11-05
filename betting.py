import json
import math
import os
import random
import select
import shutil
import sys
import tempfile
import time


STARTING_BALANCE = 1000
SAVE_VERSION = 7
APP_VERSION = time.strftime(
    "%Y.%m.%d.%H%M%S",
    time.localtime(os.path.getmtime(__file__)),
)
BANKRUPTCY_BALANCE = 50
BANKRUPTCY_FULL_LIQUIDATION_CHANCE = 5
BANKRUPTCY_PARTIAL_LIQUIDATION_RATE = 0.25
MIN_NUMBER = 0
MAX_NUMBER = 36
ANIMATION_DELAY = 0.12
CASINO_FAVOR_WEIGHT = 65
SPORT_FAVOR_WEIGHT = 75
ROUND_PAYOUT_BOOST = 1.5
BONUS_WHEEL_CHANCE = 5
BONUS_WHEEL_WIN_CHANCE = 90
LUCKY_BONUS_CHANCE = 5
GLITCH_CHANCE = 0.005
GLITCH_REWARD_PERCENT = 10
BET_HISTORY_LIMIT = 10
BONUS_WHEEL_SPIN_STEPS = 60
STREAK_PENALTY_START = 6
STREAK_PENALTY_STEP = 10
STREAK_FORCED_LOSS = 10
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "betting_balance.json")
LEGACY_SAVE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ".betting_balance.json",
)
HORSE_RETURN = 2
BOXING_RETURN = 2
SOCCER_TEAM_RETURN = 1
SOCCER_NO_GOAL_RETURN = 3
NRL_PLAYER_RETURN = 1
NRL_NO_PENALTY_RETURN = 2
DICE_SINGLE_RETURN = 3
DICE_PAIR_RETURN = 15
JOB_REWARD_PERCENT_RANGE = (20, 50)
JOB_TIME_LIMIT = 15
JOB_SENTENCES = (
    "The cat is on the bed.",
    "I like to eat apples.",
    "The sun is hot today.",
    "We play in the park.",
    "My dog can run fast.",
    "She has a red hat.",
    "The bus is at the stop.",
    "He went to the shop.",
    "Birds can fly in the sky.",
    "Please close the door.",
    "The cup is on the desk.",
    "I see a big blue car.",
    "We had fun at the beach.",
    "The baby is fast asleep.",
    "A fish can swim.",
    "It is time for lunch.",
    "The moon is out tonight.",
    "My shoes are by the door.",
    "They went home after school.",
    "Please pass me the book.",
)
WATER_ROULETTE_RETURN_PERCENT = (150, 250)
WATER_ROULETTE_STOCK_LOSS_PERCENT = (25, 50)
BONUS_WHEEL_SEGMENTS = (
    "LOSE",
    "2x", "2x", "2x",
    "2.5x", "2.5x", "2.5x",
    "3x", "3x", "3x",
)
ROUND_MODES = {
    "roulette": "roulette",
    "high_card": "high card",
    "blackjack": "blackjack",
    "jackpot": "jackpot wheel",
    "dice": "dice",
    "horse": "horse racing",
    "soccer": "soccer",
    "nrl": "NRL",
    "boxing": "boxing",
    "job": "job",
    "water_roulette": "water-gun roulette",
}
MARKET_ASSETS = {
    "gold": {
        "name": "Gold",
        "initial_price": 100,
        "volatility": (3, 8),
    },
    "ai": {
        "name": "AI",
        "initial_price": 100,
        "volatility": (3, 8),
    },
    "casino_stores": {
        "name": "Casino Stores",
        "initial_price": 150,
        "volatility": (5, 15),
    },
}
MARKET_MIN_PRICE = 50
MARKET_MIN_PRICES = {
    asset: MARKET_MIN_PRICE for asset in MARKET_ASSETS
}
MARKET_PRICES = {
    asset: details["initial_price"] for asset, details in MARKET_ASSETS.items()
}
MARKET_HOLDINGS = {asset: 0 for asset in MARKET_ASSETS}
MARKET_HISTORY = []
MARKET_ROUND = 0
MARKET_PRICE_FREEZE_ROUNDS = 0
MARKET_ROUND_COST_PERCENT = (10, 15)
MARKET_ROUND_MIN_COST = 1500
MARKET_PAYOUT_INTERVAL = 5
MARKET_PAYOUT_PERCENT = 40
BET_ROUNDS_SINCE_TAX = 0
TAX_INTERVAL = random.randint(15, 20)
MARKET_TAX_RATE = (10, 15)
MARKET_ROBBERY_RATE = (20, 30)
AI_EXTRA_LOSS_RATE = 0.10
BROKER_THEFT_RATE = 0.15
GOLD_MINE_DROP_RATE = 0.15
MARKET_TREND_CONTINUATION_CHANCE = 0.85
MARKET_DIP_RATE = 0.25
MARKET_RALLY_RATE = 0.25
MARKET_SKYROCKET_RATE = 1.0
GOLD_DISCOVERY_RISE_RATE = 0.20
MARKET_EVENT_DEFAULTS = {
    "robbery": 1,
    "crash": 1,
    "ai_loss": 6,
    "broker_theft": 1,
    "friendly_broker": 10,
    "virus": 1,
    "gold_mine": 4,
    "gold_discovery": 5,
    "dip": 1,
    "rally": 8,
    "skyrocket": 8,
}
SAVE_MIGRATIONS = {
    1: {
        "market_event_chances": {
            "skyrocket": (1, MARKET_EVENT_DEFAULTS["skyrocket"]),
        },
    },
    5: {
        "market_event_chances": {
            "crash": (5, MARKET_EVENT_DEFAULTS["crash"]),
            "broker_theft": (3, MARKET_EVENT_DEFAULTS["broker_theft"]),
        },
    },
    6: {
        "market_event_chances": {
            "friendly_broker": (3, MARKET_EVENT_DEFAULTS["friendly_broker"]),
            "gold_discovery": (1, MARKET_EVENT_DEFAULTS["gold_discovery"]),
            "rally": (4, MARKET_EVENT_DEFAULTS["rally"]),
            "skyrocket": (5, MARKET_EVENT_DEFAULTS["skyrocket"]),
        },
    },
}
MARKET_EVENT_NAMES = {
    "robbery": "Robbery",
    "crash": "Market crash",
    "ai_loss": "AI stock loss",
    "broker_theft": "Broker theft",
    "friendly_broker": "Friendly broker",
    "virus": "Virus installed",
    "gold_mine": "Gold mine discovery",
    "gold_discovery": "Gold discovery",
    "dip": "Market dip",
    "rally": "Market rally",
    "skyrocket": "Market skyrocket",
}
MARKET_EVENT_CHANCES = dict(MARKET_EVENT_DEFAULTS)
ODDS_CHANGE_PERCENTAGE_POINTS = 10
ODDS_CHANGE_DURATION = 25
ODDS_CHANGE_ROUNDS_REMAINING = 0
ODDS_UPGRADE_COST_RATE = 0.90
ODDS_UPGRADE_MIN_COST = 3000
ODDS_RESET_COST_RATE = 0.95
ODDS_RESET_MIN_COST = 1500
DUCKCOIN_BALANCE = 0.0
DUCKCOIN_WATER_SPILL_CHANCE = 5
DUCKCOIN_WATER_SPILL_DURATION = (10, 15)
DUCKCOIN_WATER_SPILL_ROUNDS = 0
DUCKCOIN_ROUND = 0
DUCKCOIN_COMPONENTS = {"gpu": 1, "cpu": 1, "memory": 1}
DUCKCOIN_PC_GENERATION = 1
DUCKCOIN_SOFTWARE_VERSION = 1
DUCKCOIN_ROUNDS_TO_UPDATE = 50
DUCKCOIN_PC_OUTDATED = False
DUCKCOIN_UPDATE_INTERVAL = 50
DUCKCOIN_TECH_ADVANCEMENT_CHANCE = 20
DUCKCOIN_COMPONENTS_BASE_COST = {"gpu": 150, "cpu": 100, "memory": 50}
DUCKCOIN_COMPONENT_BALANCE_RATE = {"gpu": 0.08, "cpu": 0.05, "memory": 0.04}
DUCKCOIN_PC_BASE_COST = 750
DUCKCOIN_PC_BALANCE_RATE = 0.15
MAX_BALANCE_REACHED = STARTING_BALANCE
JACKPOT_ZERO_MULTIPLIER = 6
LAST_GAME_MODE = None
RECENT_BETS = []
SAME_MODE_STREAK = 0
CURRENT_ROUND_BOOSTS = None
CURRENT_DISABLED_MODE = None
ROUND_BOOST_MODES = tuple(
    game_mode
    for game_mode in ROUND_MODES
    if game_mode not in ("job", "water_roulette")
)

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}
SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
RANK_VALUES = {rank: value for value, rank in enumerate(RANKS, start=2)}


def load_balance():
    global MARKET_PRICES, MARKET_HOLDINGS, MARKET_ROUND, MARKET_PRICE_FREEZE_ROUNDS
    global MARKET_MIN_PRICES
    global BET_ROUNDS_SINCE_TAX, TAX_INTERVAL, MARKET_HISTORY
    global RECENT_BETS
    global MARKET_EVENT_CHANCES, ODDS_CHANGE_ROUNDS_REMAINING
    global DUCKCOIN_BALANCE, DUCKCOIN_ROUND, DUCKCOIN_COMPONENTS
    global DUCKCOIN_PC_GENERATION, DUCKCOIN_SOFTWARE_VERSION
    global DUCKCOIN_ROUNDS_TO_UPDATE, DUCKCOIN_PC_OUTDATED
    global DUCKCOIN_WATER_SPILL_ROUNDS, MAX_BALANCE_REACHED
    save_path = SAVE_FILE
    try:
        with open(save_path, encoding="utf-8") as save_file:
            data = json.load(save_file)
    except FileNotFoundError:
        try:
            with open(LEGACY_SAVE_FILE, encoding="utf-8") as save_file:
                data = json.load(save_file)
            save_path = LEGACY_SAVE_FILE
        except FileNotFoundError:
            return STARTING_BALANCE

    balance = data.get("balance") if isinstance(data, dict) else None
    if type(balance) is not int or balance < 0:
        raise ValueError(f"Invalid balance in save file: {save_path}")
    migrated = False
    if isinstance(data, dict):
        save_version = data.get("save_version", 1)
        if type(save_version) is not int or not 1 <= save_version <= SAVE_VERSION:
            raise ValueError(f"Invalid save version in save file: {save_path}")
        source_save_version = save_version
        prices = data.get("market_prices", MARKET_PRICES)
        minimum_prices = data.get(
            "market_min_prices",
            {asset: MARKET_MIN_PRICE for asset in MARKET_ASSETS},
        )
        holdings = data.get("market_holdings", MARKET_HOLDINGS)
        market_round = data.get("market_round", MARKET_ROUND)
        price_freeze_rounds = data.get(
            "market_price_freeze_rounds",
            MARKET_PRICE_FREEZE_ROUNDS,
        )
        bets_since_tax = data.get(
            "bets_since_tax",
            BET_ROUNDS_SINCE_TAX,
        )
        tax_interval = data.get("tax_interval", TAX_INTERVAL)
        market_history = data.get("market_history", [])
        recent_bets = data.get("recent_bets", [])
        event_chances = data.get(
            "market_event_chances",
            MARKET_EVENT_DEFAULTS,
        )
        if isinstance(event_chances, dict):
            event_chances = {
                **MARKET_EVENT_DEFAULTS,
                **event_chances,
            }
        odds_change_rounds = data.get(
            "odds_change_rounds_remaining",
            0,
        )
        while save_version < SAVE_VERSION:
            migration = SAVE_MIGRATIONS.get(save_version, {})
            if isinstance(event_chances, dict) and not odds_change_rounds:
                for event, (old_chance, new_chance) in migration.get(
                    "market_event_chances",
                    {},
                ).items():
                    if event_chances.get(event) == old_chance:
                        event_chances[event] = new_chance
            save_version += 1
            migrated = True
        duckcoin_balance = data.get("duckcoin_balance", 0.0)
        duckcoin_water_spill_rounds = data.get(
            "duckcoin_water_spill_rounds",
            0,
        )
        max_balance_reached = data.get("max_balance_reached", balance)
        duckcoin_round = data.get("duckcoin_round", 0)
        duckcoin_components = data.get(
            "duckcoin_components",
            {"gpu": 1, "cpu": 1, "memory": 1},
        )
        duckcoin_pc_generation = data.get("duckcoin_pc_generation", 1)
        duckcoin_software_version = data.get("duckcoin_software_version", 1)
        duckcoin_rounds_to_update = data.get(
            "duckcoin_rounds_to_update",
            DUCKCOIN_UPDATE_INTERVAL,
        )
        if source_save_version < 3:
            duckcoin_rounds_to_update = DUCKCOIN_UPDATE_INTERVAL
        duckcoin_pc_outdated = data.get("duckcoin_pc_outdated", False)
        if (
            not isinstance(prices, dict)
            or any(asset not in prices for asset in ("gold", "ai"))
            or any(
                type(prices[asset]) is not int or prices[asset] < 1
                for asset in MARKET_ASSETS
                if asset in prices
            )
            or not isinstance(minimum_prices, dict)
            or set(minimum_prices) != set(MARKET_ASSETS)
            or any(
                type(minimum_prices[asset]) is not int
                or minimum_prices[asset] < MARKET_MIN_PRICE
                for asset in MARKET_ASSETS
            )
            or not isinstance(holdings, dict)
            or any(asset not in holdings for asset in ("gold", "ai"))
            or any(
                type(holdings[asset]) is not int or holdings[asset] < 0
                for asset in MARKET_ASSETS
                if asset in holdings
            )
            or type(market_round) is not int
            or market_round < 0
            or type(price_freeze_rounds) is not int
            or not 0 <= price_freeze_rounds <= 3
            or type(bets_since_tax) is not int
            or not 0 <= bets_since_tax < 20
            or type(tax_interval) is not int
            or not 15 <= tax_interval <= 20
            or bets_since_tax >= tax_interval
            or not isinstance(market_history, list)
            or any(
                not isinstance(entry, dict)
                or type(entry.get("round")) is not int
                or entry["round"] < 0
                or not isinstance(entry.get("prices"), dict)
                or not all(
                    asset in entry["prices"] for asset in ("gold", "ai")
                )
                or any(
                    asset not in MARKET_ASSETS
                    for asset in entry["prices"]
                )
                or any(
                    type(price) is not int or price < 1
                    for price in entry["prices"].values()
                )
                for entry in market_history
            )
            or not isinstance(event_chances, dict)
            or set(event_chances) != set(MARKET_EVENT_DEFAULTS)
            or any(
                type(event_chances.get(event)) is not int
                or not 0 <= event_chances[event] <= 100
                for event in MARKET_EVENT_DEFAULTS
            )
            or type(odds_change_rounds) is not int
            or not 0 <= odds_change_rounds <= ODDS_CHANGE_DURATION
            or type(duckcoin_balance) not in (int, float)
            or duckcoin_balance < 0
            or duckcoin_balance > 1e300
            or not math.isfinite(duckcoin_balance)
            or type(duckcoin_round) is not int
            or duckcoin_round < 0
            or not isinstance(duckcoin_components, dict)
            or set(duckcoin_components) != {"gpu", "cpu", "memory"}
            or any(
                type(level) is not int or not 1 <= level <= 10000
                for level in duckcoin_components.values()
            )
            or type(duckcoin_pc_generation) is not int
            or not 1 <= duckcoin_pc_generation <= 10000
            or type(duckcoin_software_version) is not int
            or not 1 <= duckcoin_software_version <= 10000
            or type(duckcoin_rounds_to_update) is not int
            or not 1 <= duckcoin_rounds_to_update <= DUCKCOIN_UPDATE_INTERVAL
            or type(duckcoin_pc_outdated) is not bool
            or type(duckcoin_water_spill_rounds) is not int
            or not 0 <= duckcoin_water_spill_rounds
            < max(DUCKCOIN_WATER_SPILL_DURATION)
            or type(max_balance_reached) is not int
            or max_balance_reached < balance
        ):
            raise ValueError(f"Invalid market data in save file: {save_path}")
        if (
            not isinstance(recent_bets, list)
            or len(recent_bets) > BET_HISTORY_LIMIT
            or any(type(bet) is not int or bet < 1 for bet in recent_bets)
        ):
            raise ValueError(f"Invalid bet history in save file: {save_path}")
        MARKET_PRICES = {
            asset: max(
                minimum_prices[asset],
                prices.get(asset, details["initial_price"]),
            )
            for asset, details in MARKET_ASSETS.items()
        }
        MARKET_MIN_PRICES = dict(minimum_prices)
        MARKET_HOLDINGS = {
            asset: holdings.get(asset, 0) for asset in MARKET_ASSETS
        }
        MARKET_ROUND = market_round
        MARKET_PRICE_FREEZE_ROUNDS = price_freeze_rounds
        BET_ROUNDS_SINCE_TAX = bets_since_tax
        TAX_INTERVAL = tax_interval
        MARKET_HISTORY = market_history[-15:]
        RECENT_BETS = recent_bets
        MARKET_EVENT_CHANCES = dict(event_chances)
        ODDS_CHANGE_ROUNDS_REMAINING = odds_change_rounds
        DUCKCOIN_BALANCE = float(duckcoin_balance)
        DUCKCOIN_ROUND = duckcoin_round
        DUCKCOIN_COMPONENTS = dict(duckcoin_components)
        DUCKCOIN_PC_GENERATION = duckcoin_pc_generation
        DUCKCOIN_SOFTWARE_VERSION = duckcoin_software_version
        DUCKCOIN_ROUNDS_TO_UPDATE = duckcoin_rounds_to_update
        DUCKCOIN_PC_OUTDATED = duckcoin_pc_outdated
        DUCKCOIN_WATER_SPILL_ROUNDS = duckcoin_water_spill_rounds
        MAX_BALANCE_REACHED = max_balance_reached
    if save_path == LEGACY_SAVE_FILE or migrated:
        save_balance(balance)
    return balance


def save_balance(balance):
    global MAX_BALANCE_REACHED
    MAX_BALANCE_REACHED = max(MAX_BALANCE_REACHED, balance)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=os.path.dirname(SAVE_FILE),
            prefix=".betting_balance_",
            suffix=".tmp",
            delete=False,
        ) as save_file:
            temporary_path = save_file.name
            json.dump(
                {
                    "save_version": SAVE_VERSION,
                    "balance": balance,
                    "market_prices": MARKET_PRICES,
                    "market_min_prices": MARKET_MIN_PRICES,
                    "market_holdings": MARKET_HOLDINGS,
                    "market_history": MARKET_HISTORY[-15:],
                    "recent_bets": RECENT_BETS[-BET_HISTORY_LIMIT:],
                    "market_round": MARKET_ROUND,
                    "market_price_freeze_rounds": MARKET_PRICE_FREEZE_ROUNDS,
                    "bets_since_tax": BET_ROUNDS_SINCE_TAX,
                    "tax_interval": TAX_INTERVAL,
                    "market_event_chances": MARKET_EVENT_CHANCES,
                    "odds_change_rounds_remaining": ODDS_CHANGE_ROUNDS_REMAINING,
                    "duckcoin_balance": DUCKCOIN_BALANCE,
                    "duckcoin_water_spill_rounds": DUCKCOIN_WATER_SPILL_ROUNDS,
                    "duckcoin_round": DUCKCOIN_ROUND,
                    "duckcoin_components": DUCKCOIN_COMPONENTS,
                    "duckcoin_pc_generation": DUCKCOIN_PC_GENERATION,
                    "duckcoin_software_version": DUCKCOIN_SOFTWARE_VERSION,
                    "duckcoin_rounds_to_update": DUCKCOIN_ROUNDS_TO_UPDATE,
                    "duckcoin_pc_outdated": DUCKCOIN_PC_OUTDATED,
                    "max_balance_reached": MAX_BALANCE_REACHED,
                },
                save_file,
            )
            save_file.write("\n")
        os.replace(temporary_path, SAVE_FILE)
    except OSError:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)
        raise


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    elif os.environ.get("TERM"):
        os.system("clear")
    else:
        print()


def animate(label, frames=("|", "/", "-", "\\"), steps=18, delay=ANIMATION_DELAY):
    for index in range(steps):
        print(f"\r{label} {frames[index % len(frames)]}", end="", flush=True)
        time.sleep(delay)
    print("\r" + " " * 60 + "\r", end="", flush=True)


def terminal_dimensions():
    size = shutil.get_terminal_size(fallback=(80, 24))
    return max(size.columns, 20), max(size.lines, 8)


def draw_fullscreen(lines):
    columns, rows = terminal_dimensions()
    frame = [line[:columns].ljust(columns) for line in lines[:rows - 1]]
    frame.extend([" " * columns] * (rows - 1 - len(frame)))
    print("\033[2J\033[H" + "\n".join(frame), end="", flush=True)


def prompt_choice(prompt, choices):
    choices = tuple(choices)
    while True:
        answer = input(prompt).strip().lower()
        for choice in choices:
            if answer == choice.lower():
                return choice
        print(f"Choose one of: {', '.join(choices)}")


def prompt_menu(title, options):
    print(title)
    for name, description in options.items():
        print(f"  {name} — {description}")
    return prompt_choice("Type a name: ", options)


def prompt_int(prompt, minimum, maximum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Enter a whole number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            limit = f"{minimum} to {maximum}" if maximum is not None else f"at least {minimum}"
            print(f"Enter a number from {limit}.")
            continue
        return value


def format_money(amount):
    suffixes = ("", "K", "M", "B", "T", "Q", "Qi", "Sx", "Sp", "Oc", "No")
    scaled = abs(amount)
    suffix_index = 0
    while scaled >= 1000 and suffix_index < len(suffixes) - 1:
        scaled /= 1000
        suffix_index += 1
    if suffix_index == 0:
        return f"${amount}"
    if scaled >= 999.5 and suffix_index < len(suffixes) - 1:
        scaled /= 1000
        suffix_index += 1
    if scaled < 100:
        display_value = f"{scaled:.1f}".rstrip("0").rstrip(".")
    else:
        display_value = f"{scaled:.0f}"
    sign = "-" if amount < 0 else ""
    return f"{sign}${display_value}{suffixes[suffix_index]}"


def prompt_stake(balance):
    return prompt_int(f"Bet amount (balance {format_money(balance)}): $", 1, balance)


def prompt_timed_text(prompt, timeout):
    print(prompt, end="", flush=True)
    deadline = time.monotonic() + timeout
    if os.name == "nt":
        import msvcrt

        characters = []
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                while msvcrt.kbhit():
                    msvcrt.getwch()
                print()
                return None
            if not msvcrt.kbhit():
                time.sleep(min(0.01, remaining))
                continue

            character = msvcrt.getwch()
            if character == "\r":
                print()
                return "".join(characters), time.monotonic() <= deadline
            if character == "\003":
                raise KeyboardInterrupt
            if character in ("\x00", "\xe0"):
                msvcrt.getwch()
            elif character in ("\b", "\x7f"):
                if characters:
                    characters.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                characters.append(character)
                sys.stdout.write(character)
                sys.stdout.flush()

    readable, _, _ = select.select([sys.stdin], [], [], timeout)
    if not readable:
        return None
    answer = sys.stdin.readline().rstrip("\r\n")
    return answer, time.monotonic() <= deadline


def get_round_boosts():
    global CURRENT_ROUND_BOOSTS, CURRENT_DISABLED_MODE
    if CURRENT_ROUND_BOOSTS is None or CURRENT_DISABLED_MODE is None:
        CURRENT_ROUND_BOOSTS = tuple(random.sample(ROUND_BOOST_MODES, 2))
        CURRENT_DISABLED_MODE = random.choice(tuple(ROUND_MODES))
    return CURRENT_ROUND_BOOSTS


def available_mode_options(options, mode_by_option):
    return {
        option: description
        for option, description in options.items()
        if mode_by_option.get(option) != CURRENT_DISABLED_MODE
    }


def favored_outcome(preferred, alternatives, favor_weight):
    alternatives = tuple(alternatives)
    if not alternatives:
        return preferred
    weights = [favor_weight] + [
        (100 - favor_weight) / len(alternatives)
    ] * len(alternatives)
    return random.choices((preferred, *alternatives), weights=weights, k=1)[0]


def begin_round(game_mode, balance):
    global LAST_GAME_MODE, SAME_MODE_STREAK
    if game_mode == LAST_GAME_MODE:
        SAME_MODE_STREAK += 1
    else:
        LAST_GAME_MODE = game_mode
        SAME_MODE_STREAK = 1

    win_mode, payout_mode = get_round_boosts()
    clear_screen()
    print("\033[1;36m=== THE PLAY MONEY CLUB ===\033[0m")
    print(f"Balance: {format_money(balance)}")
    return game_mode == win_mode, game_mode == payout_mode


def apply_payout_boost(payout, won, boosted):
    if won and boosted:
        boosted_payout = math.floor(payout * ROUND_PAYOUT_BOOST)
        print(
            f"\033[1;33mPayout boost: "
            f"{format_money(boosted_payout - payout)} extra.\033[0m"
        )
        return boosted_payout
    return payout


def restore_empty_balance(balance):
    if balance <= 0:
        stock_value = sum(
            MARKET_HOLDINGS[asset] * MARKET_PRICES[asset]
            for asset in MARKET_ASSETS
        )
        if stock_value:
            sell_all = (
                random.randint(1, 100)
                <= BANKRUPTCY_FULL_LIQUIDATION_CHANCE
            )
            for asset, details in MARKET_ASSETS.items():
                owned_shares = MARKET_HOLDINGS[asset]
                if owned_shares:
                    shares_to_sell = (
                        owned_shares
                        if sell_all
                        else max(
                            1,
                            math.floor(
                                owned_shares
                                * BANKRUPTCY_PARTIAL_LIQUIDATION_RATE
                            ),
                        )
                    )
                    proceeds = shares_to_sell * MARKET_PRICES[asset]
                    balance += proceeds
                    MARKET_HOLDINGS[asset] -= shares_to_sell
                    print(
                        f"Sold {shares_to_sell} of {owned_shares} "
                        f"{details['name']} share(s) "
                        f"for {format_money(proceeds)} to recover your balance."
                    )
            save_balance(balance)
            return balance

        print(
            f"You're out of play money and have no stocks to sell. "
            f"A {format_money(BANKRUPTCY_BALANCE)} recovery balance is ready."
        )
        input("Press Enter to continue...")
        save_balance(BANKRUPTCY_BALANCE)
        return BANKRUPTCY_BALANCE
    return balance


def apply_end_of_bet_cash_event(balance):
    global BET_ROUNDS_SINCE_TAX, TAX_INTERVAL
    BET_ROUNDS_SINCE_TAX += 1

    if BET_ROUNDS_SINCE_TAX >= TAX_INTERVAL:
        completed_interval = TAX_INTERVAL
        BET_ROUNDS_SINCE_TAX = 0
        if balance > 0:
            tax_percent = random.randint(*MARKET_TAX_RATE)
            tax = math.floor(balance * tax_percent / 100)
            balance -= tax
            print(
                f"\033[1;31mThe tax collector arrives after "
                f"{completed_interval} bets and takes {format_money(tax)} "
                f"({tax_percent}% of your cash). Your shares are untouched.\033[0m"
            )
        TAX_INTERVAL = random.randint(15, 20)
        return balance

    if (
        balance > 0
        and random.randint(1, 100) <= MARKET_EVENT_CHANCES["robbery"]
    ):
        robbery_percent = random.randint(*MARKET_ROBBERY_RATE)
        stolen = math.floor(balance * robbery_percent / 100)
        balance -= stolen
        print(
            f"\033[1;31mA robber strikes and steals {format_money(stolen)} "
            f"({robbery_percent}% of your cash). "
            "Your shares are untouched.\033[0m"
        )
    return balance


def record_bet(stake):
    RECENT_BETS.append(stake)
    del RECENT_BETS[:-BET_HISTORY_LIMIT]


def apply_bet_glitch(balance, stake=None):
    if stake is not None:
        record_bet(stake)

    if random.random() >= GLITCH_CHANCE:
        return balance

    reward = sum(RECENT_BETS) * GLITCH_REWARD_PERCENT // 100
    balance += reward
    bet_count = len(RECENT_BETS)
    bet_word = "bet" if bet_count == 1 else "bets"
    print(
        f"\033[1;33mGLITCH! You received {format_money(reward)} "
        f"({GLITCH_REWARD_PERCENT}% of your last {bet_count} "
        f"{bet_word}).\033[0m"
    )
    return balance


def show_banner(balance):
    clear_screen()
    win_mode, payout_mode = get_round_boosts()
    print("\033[1;36m=== THE PLAY MONEY CLUB ===\033[0m")
    print(f"Version: {APP_VERSION}")
    print(f"Balance: {format_money(balance)}")
    print(f"Higher win chance this round: {ROUND_MODES[win_mode]}")
    print(
        f"Higher payout this round: {ROUND_MODES[payout_mode]}"
    )
    print(f"Unavailable this round: {ROUND_MODES[CURRENT_DISABLED_MODE]}")
    print("All events are simulated with rotating round boosts.")
    print("A bonus wheel may appear after any round.")
    print("Each casino/sport round has a 0.5% glitch chance.")
    print("A glitch pays 10% of the sum of your last 10 bets.")
    print("-" * 58)


def show_result(won, payout, balance, game_mode, stake=None):
    global CURRENT_ROUND_BOOSTS, CURRENT_DISABLED_MODE
    streak_forced = SAME_MODE_STREAK >= STREAK_FORCED_LOSS
    streak_penalty = (
        min(
            100,
            (SAME_MODE_STREAK - STREAK_PENALTY_START + 1) * STREAK_PENALTY_STEP,
        )
        if SAME_MODE_STREAK >= STREAK_PENALTY_START
        else 0
    )
    if streak_forced or (won and streak_penalty and random.randint(1, 100) <= streak_penalty):
        balance -= payout
        payout = 0
        won = False

    bonus = 0
    if random.randint(1, 100) <= LUCKY_BONUS_CHANCE:
        bonus_percent = random.randint(10, 12)
        bonus = math.floor(balance * bonus_percent / 100)
        balance += bonus
        print(
            f"\033[1;33mLucky bonus! Extra {format_money(bonus)} "
            f"({bonus_percent}% of your balance) added.\033[0m"
        )

    balance = advance_market_round(balance)
    balance = apply_end_of_bet_cash_event(balance)
    if game_mode in ROUND_MODES:
        balance = apply_bet_glitch(balance, stake)
    save_balance(balance)
    if won:
        print(f"\033[1;32mWIN! Payout: {format_money(payout)}\033[0m")
    else:
        print("\033[1;31mNo win this round.\033[0m")
    print(f"Balance: {format_money(balance)}")
    input("Press Enter to continue...")
    balance = bonus_wheel(balance)
    CURRENT_ROUND_BOOSTS = None
    CURRENT_DISABLED_MODE = None
    return balance


def bonus_wheel(balance):
    if random.randint(1, 100) > BONUS_WHEEL_CHANCE:
        return balance

    print("\n\033[1;36mBONUS WHEEL APPEARED!\033[0m")
    print("Optional side bet: 90% winning segments, returning 2x, 2.5x, or 3x.")
    if balance <= 0:
        print("You need a positive balance to play the bonus wheel.")
        return balance
    if prompt_choice("Spin the bonus wheel? (yes/no): ", ("yes", "no")) == "no":
        return balance

    stake = prompt_stake(balance)
    balance -= stake
    record_bet(stake)
    if random.randint(1, 100) <= BONUS_WHEEL_WIN_CHANCE:
        winning_indexes = tuple(
            index for index, segment in enumerate(BONUS_WHEEL_SEGMENTS)
            if segment != "LOSE"
        )
        target_index = random.choice(winning_indexes)
    else:
        target_index = BONUS_WHEEL_SEGMENTS.index("LOSE")
    spin_steps = BONUS_WHEEL_SPIN_STEPS
    print("The bonus wheel is spinning...")
    for step in range(spin_steps + 1):
        offset = spin_steps - step
        index = (target_index - offset) % len(BONUS_WHEEL_SEGMENTS)
        previous = BONUS_WHEEL_SEGMENTS[(index - 1) % len(BONUS_WHEEL_SEGMENTS)]
        current = BONUS_WHEEL_SEGMENTS[index]
        following = BONUS_WHEEL_SEGMENTS[(index + 1) % len(BONUS_WHEEL_SEGMENTS)]
        print(
            f"\r  [{previous:^4}]  >[{current:^4}]<  [{following:^4}]",
            end="",
            flush=True,
        )
        time.sleep(0.06 + (step / spin_steps) ** 3 * 0.35)
    print()

    result = BONUS_WHEEL_SEGMENTS[target_index]
    print(f"\033[1;35mThe wheel lands on {result}!\033[0m")
    if result == "LOSE":
        print("\033[1;31mNo bonus payout this spin.\033[0m")
    else:
        multiplier = float(result[:-1])
        payout = math.floor(stake * multiplier)
        balance += payout
        print(
            f"\033[1;32mBonus wheel payout: {format_money(payout)} "
            f"({result} total return).\033[0m"
        )
    balance = advance_market_round(balance)
    balance = apply_end_of_bet_cash_event(balance)
    print(f"Balance: {format_money(balance)}")
    save_balance(balance)
    input("Press Enter to continue...")
    return balance


def animate_roulette(result):
    print("\n\033[1;33m=== Roulette wheel ===\033[0m")
    print("The wheel is spinning...")
    spin_count = 28
    for step in range(spin_count):
        number = result if step == spin_count - 1 else random.randint(MIN_NUMBER, MAX_NUMBER)
        color = "green" if number == 0 else ("red" if number in RED_NUMBERS else "black")
        background = {"green": 42, "red": 41, "black": 40}[color]
        print(f"\r  \033[{background}m  {number:>2}  \033[0m  {color:<5}", end="", flush=True)
        time.sleep(0.06 + step * 0.012)
    print()


def roulette(balance):
    win_boost, payout_boost = begin_round("roulette", balance)
    print("\nROULETTE TABLE")
    mode = prompt_menu("Choose a roulette mode:", {
        "number": "exact number",
        "color": "red or black",
        "parity": "even or odd",
        "half": "low or high",
        "dozen": "first, second, or third dozen",
    })

    bet = None
    if mode == "number":
        bet = prompt_int("Pick a number (0-36): ", MIN_NUMBER, MAX_NUMBER)
    elif mode == "color":
        bet = prompt_menu("Choose a color:", {
            "red": "red numbers",
            "black": "black numbers",
        })
    elif mode == "parity":
        bet = prompt_menu("Choose parity:", {
            "even": "even numbers",
            "odd": "odd numbers",
        })
    elif mode == "half":
        bet = prompt_menu("Choose a half:", {
            "low": "numbers 1-18",
            "high": "numbers 19-36",
        })
    else:
        bet = prompt_menu("Choose a dozen:", {
            "first": "numbers 1-12",
            "second": "numbers 13-24",
            "third": "numbers 25-36",
        })

    if mode == "color":
        minimum_color_stake = max(1, math.ceil(balance * 0.01))
        stake = prompt_int(
            f"Bet amount (balance {format_money(balance)}; minimum 1% "
            f"{format_money(minimum_color_stake)}): $",
            minimum_color_stake,
            balance,
        )
    else:
        stake = prompt_stake(balance)
    balance -= stake
    print(f"\nBet locked: {format_money(stake)} on {bet}.")
    numbers = tuple(range(MIN_NUMBER, MAX_NUMBER + 1))
    if mode == "number":
        result = favored_outcome(
            bet,
            (number for number in numbers if number != bet),
            70 if win_boost else 30,
        )
    elif mode == "color":
        result = None if random.randint(1, 100) <= 2 else random.choice(numbers)
    else:
        def matches_bet(number):
            if mode == "parity":
                return number != 0 and ("even" if number % 2 == 0 else "odd") == bet
            if mode == "half":
                return number != 0 and ("low" if number <= 18 else "high") == bet
            dozen = ("first", "second", "third")[(number - 1) // 12] if number else ""
            return dozen == bet

        matching = tuple(number for number in numbers if matches_bet(number))
        nonmatching = tuple(number for number in numbers if not matches_bet(number))
        result = random.choice(
            matching
            if random.randint(1, 100) <= (
                85 if win_boost else CASINO_FAVOR_WEIGHT
            )
            else nonmatching
        )
    if result is None:
        print("\033[1;31mThe ball fell on the ground. No result!\033[0m")
    else:
        animate_roulette(result)
        color = "green" if result == 0 else ("red" if result in RED_NUMBERS else "black")
        print(f"\033[1;35mRoulette lands on {result} ({color})\033[0m")

    won = False
    multiplier = 0
    payout = 0
    if mode == "number":
        won, multiplier = result == bet, 50
    elif mode == "color":
        if result is not None:
            won = color == bet or color == "green"
            if color == "green":
                payout = stake * 4 if won else 0
            elif won:
                payout = math.floor(stake * random.uniform(1.5, 2.5))
    elif mode == "parity":
        won = result != 0 and ("even" if result % 2 == 0 else "odd") == bet
        multiplier = 2
    elif mode == "half":
        won = result != 0 and ("low" if result <= 18 else "high") == bet
        multiplier = 2
    else:
        dozen = ("first", "second", "third")[(result - 1) // 12] if result else ""
        won, multiplier = dozen == bet, 3

    if mode == "number":
        payout = stake * multiplier if won else 0
    elif result == 0:
        won = mode == "color"
        payout = stake * 4 if won else 0
    elif mode != "color":
        payout = stake * multiplier if won else 0
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "roulette", stake)
    return balance


def draw_card(deck):
    rank, suit = deck.pop()
    return rank, suit


def card_name(card):
    return f"{card[0]} of {card[1]}"


def card_value(card):
    return RANK_VALUES[card[0]]


def high_card(balance):
    win_boost, payout_boost = begin_round("high_card", balance)
    stake = prompt_stake(balance)
    balance -= stake
    deck = [(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    player, dealer = draw_card(deck), draw_card(deck)
    swap_chance = 70 if win_boost else 30
    if card_value(player) < card_value(dealer) and random.randint(1, 100) <= swap_chance:
        player, dealer = dealer, player
    animate("Dealing cards", steps=12, delay=0.2)
    print(f"Your card: {card_name(player)}")
    print(f"Dealer card: {card_name(dealer)}")
    if card_value(player) == card_value(dealer):
        payout = stake
        balance += payout
        print("Tie — your bet is returned.")
        balance = show_result(False, payout, balance, "high_card", stake)
    else:
        won = card_value(player) > card_value(dealer)
        payout = stake * 2 if won else 0
        payout = apply_payout_boost(payout, won, payout_boost)
        balance += payout
        balance = show_result(won, payout, balance, "high_card", stake)
    return balance


def blackjack_total(hand):
    total = sum(11 if rank == "A" else min(RANK_VALUES[rank], 10) for rank, _ in hand)
    aces = sum(rank == "A" for rank, _ in hand)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def blackjack(balance):
    win_boost, payout_boost = begin_round("blackjack", balance)
    stake = prompt_stake(balance)
    balance -= stake
    deck = [(rank, suit) for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    player = [draw_card(deck), draw_card(deck)]
    dealer = [draw_card(deck), draw_card(deck)]

    animate("Dealing blackjack", steps=12, delay=0.2)
    print("Your cards: " + ", ".join(card_name(card) for card in player))
    print(f"Dealer shows: {card_name(dealer[0])}")
    while blackjack_total(player) < 21:
        action = prompt_menu("Choose your move:", {
            "hit": "draw another card",
            "stand": "keep your current hand",
        })
        if action == "stand":
            break
        player.append(draw_card(deck))
        animate("Drawing", steps=5, delay=0.16)
        print(f"Your hand: {', '.join(card_name(card) for card in player)}")
        print(f"Total: {blackjack_total(player)}")

    dealer_stand_total = 13 if win_boost else 15
    while blackjack_total(player) <= 21 and blackjack_total(dealer) < dealer_stand_total:
        dealer.append(draw_card(deck))
        animate("Dealer draws", steps=5, delay=0.16)

    player_total, dealer_total = blackjack_total(player), blackjack_total(dealer)
    print(f"Your total: {player_total} | Dealer total: {dealer_total}")
    print("Dealer cards: " + ", ".join(card_name(card) for card in dealer))
    if player_total > 21 or (dealer_total <= 21 and dealer_total > player_total):
        won, payout = False, 0
    elif player_total == dealer_total:
        won, payout = False, stake
        balance += payout
        print("Push — your bet is returned.")
    else:
        won = True
        natural = len(player) == 2 and player_total == 21
        payout = int(stake * 2.5) if natural else stake * 2
        payout = apply_payout_boost(payout, won, payout_boost)
        balance += payout
    balance = show_result(won, payout, balance, "blackjack", stake)
    return balance


def cards(balance):
    while True:
        balance = restore_empty_balance(balance)
        show_banner(balance)
        options = available_mode_options({
            "high": "beat the dealer's card; tie refunds bet",
            "blackjack": "hit or stand",
            "back": "return to the casino menu",
        }, {
            "high": "high_card",
            "blackjack": "blackjack",
        })
        style = prompt_menu("CARD TABLE", options)
        if style == "high":
            balance = high_card(balance)
        elif style == "blackjack":
            balance = blackjack(balance)
        else:
            return balance


def jackpot_wheel(balance):
    win_boost, payout_boost = begin_round("jackpot", balance)
    print("\nJACKPOT WHEEL")
    stake = prompt_stake(balance)
    balance -= stake
    segments = (0, 0, 1, 1, 2, 3, 4, 6)
    print("Match any pair or three of a kind.")
    favor_weight = 85 if win_boost else CASINO_FAVOR_WEIGHT
    if random.randint(1, 100) <= favor_weight:
        if random.randint(1, 100) <= (20 if win_boost else 8):
            triple = random.choice((2, 3, 4, 6))
            results = [triple] * 3
        else:
            pair = random.choice(segments)
            single = random.choice(tuple(value for value in segments if value != pair))
            results = [pair, pair, single]
            random.shuffle(results)
    else:
        results = [random.choice(segments) for _ in range(3)]
    reels = [random.choice(segments) for _ in range(3)]
    stop_steps = (12, 19, 26)

    print("       REEL 1    REEL 2    REEL 3")
    for step in range(stop_steps[-1] + 1):
        for index in range(3):
            if step >= stop_steps[index]:
                reels[index] = results[index]
            else:
                reels[index] = random.choice(segments)
        print(
            f"\r       [{reels[0]:>2}]      [{reels[1]:>2}]      [{reels[2]:>2}]",
            end="",
            flush=True,
        )
        time.sleep(0.10 + step * 0.012)

    print(f"\n\033[1;35mFinal reels: {results[0]} | {results[1]} | {results[2]}\033[0m")
    triple_match = results[0] == results[1] == results[2]
    if triple_match:
        multiplier = results[0] or JACKPOT_ZERO_MULTIPLIER
    elif len(set(results)) == 2:
        multiplier = 1.5
    else:
        multiplier = 0
    payout = int(stake * multiplier)
    if triple_match and results[0] == 0:
        print(
            f"\033[1;35mZero jackpot! All three zeroes pay "
            f"{JACKPOT_ZERO_MULTIPLIER}x.\033[0m"
        )
    elif triple_match:
        print("\033[1;35mTriple match!\033[0m")
    elif multiplier:
        print("\033[1;35mPair match!\033[0m")
    else:
        print("\033[1;31mNo match this spin.\033[0m")
    payout = apply_payout_boost(payout, multiplier > 0, payout_boost)
    balance += payout
    balance = show_result(multiplier > 0, payout, balance, "jackpot", stake)
    return balance


def dice_roll(balance):
    _, payout_boost = begin_round("dice", balance)
    print("\nDICE — PICK THE FACES")
    bet_type = prompt_menu("Choose your bet:", {
        "one": "pick one face; it must appear on either die",
        "two": "pick two different faces; both must appear",
    })
    first_pick = prompt_int("Pick a face (1-6): ", 1, 6)
    picks = {first_pick}
    if bet_type == "two":
        while True:
            second_pick = prompt_int("Pick a different face (1-6): ", 1, 6)
            if second_pick != first_pick:
                picks.add(second_pick)
                break
            print("Choose a different face from your first pick.")

    stake = prompt_stake(balance)
    balance -= stake
    result = (random.randint(1, 6), random.randint(1, 6))

    print("Rolling the dice...")
    for frame in range(14):
        faces = result if frame == 13 else (random.randint(1, 6), random.randint(1, 6))
        print(f"\r  [{faces[0]}]  [{faces[1]}]", end="", flush=True)
        time.sleep(0.06 + frame * 0.008)
    print(f"\nDice: {result[0]} and {result[1]}")
    won = (
        bool(picks.intersection(result))
        if bet_type == "one"
        else picks.issubset(result)
    )
    multiplier = DICE_SINGLE_RETURN if bet_type == "one" else DICE_PAIR_RETURN
    payout = stake * multiplier if won else 0
    if won:
        print("\033[1;32mYour picked face bet wins!\033[0m")
    else:
        print("\033[1;31mYour picked face bet loses.\033[0m")
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "dice", stake)
    return balance


def job(balance):
    begin_round("job", balance)
    sentence = random.choice(JOB_SENTENCES)
    print("\nJOB — type the sentence exactly as shown.")
    print(
        f"You have {JOB_TIME_LIMIT} seconds. "
        f"Complete it correctly to earn a random "
        f"{JOB_REWARD_PERCENT_RANGE[0]}–{JOB_REWARD_PERCENT_RANGE[1]}% "
        "of your current balance."
    )
    print(f"\n{sentence}")
    answer = prompt_timed_text("Type the sentence: ", JOB_TIME_LIMIT)
    won = answer is not None and answer[1] and answer[0] == sentence
    reward_percent = (
        random.randint(*JOB_REWARD_PERCENT_RANGE) if won else 0
    )
    payout = math.floor(balance * reward_percent / 100) if won else 0
    if answer is None:
        print("\033[1;31mTime ran out. No job reward this round.\033[0m")
    elif not answer[1]:
        print("\033[1;31mTime ran out. No job reward this round.\033[0m")
    elif not won:
        print("\033[1;31mThe sentence didn't match exactly. No job reward.\033[0m")
    else:
        print(
            f"\033[1;32mJob completed! You earned {format_money(payout)} "
            f"({reward_percent}% of your balance).\033[0m"
        )
    balance += payout
    return show_result(won, payout, balance, "job")


def water_roulette(balance):
    begin_round("water_roulette", balance)
    print(
        "\nWATER-GUN ROULETTE — a toy water blaster game; "
        "no real weapons are involved."
    )
    opponent = random.choice(("Riley", "Casey", "Jordan", "Taylor"))
    stake = prompt_stake(balance)
    balance -= stake
    print(
        f"You and {opponent} take turns. There are six turns, "
        "with one water shot and five blanks."
    )

    chamber = [False] * 5 + [True]
    random.shuffle(chamber)
    player_starts = random.choice((True, False))
    player_hit = False
    for turn, fires in enumerate(chamber):
        is_player_turn = (turn % 2 == 0) == player_starts
        shooter = "You" if is_player_turn else opponent
        print(f"\nTurn {turn + 1}: {shooter} pulls the trigger...")
        if fires:
            print(f"SPLASH! The water shot hits {shooter}.")
            player_hit = is_player_turn
            break
        print("Blank! No water.")

    payout = 0
    if player_hit:
        balance = 5
        loss_percent = random.randint(*WATER_ROULETTE_STOCK_LOSS_PERCENT)
        total_shares_lost = 0
        for asset, details in MARKET_ASSETS.items():
            shares_owned = MARKET_HOLDINGS[asset]
            expected_loss = shares_owned * loss_percent / 100
            shares_lost = math.floor(expected_loss)
            if random.random() < expected_loss - shares_lost:
                shares_lost += 1
            shares_lost = min(shares_owned, shares_lost)
            MARKET_HOLDINGS[asset] -= shares_lost
            total_shares_lost += shares_lost
            if shares_lost:
                print(
                    f"Lost {shares_lost} {details['name']} share(s) "
                    f"to the splash."
                )
        print(
            f"\033[1;31mYou were splashed! Your cash is reduced to $5, "
            f"and {loss_percent}% of each stock holding is lost "
            "(rounded to whole shares).\033[0m"
        )
        if total_shares_lost == 0:
            print("No whole shares were lost this time.")
    else:
        return_percent = random.randint(*WATER_ROULETTE_RETURN_PERCENT)
        payout = math.floor(stake * return_percent / 100)
        balance += payout
        print(
            f"\033[1;32mYou survived! Your {format_money(stake)} bet returns "
            f"{format_money(payout)} total ({return_percent}% of the bet).\033[0m"
        )

    return show_result(
        player_hit is False,
        payout,
        balance,
        "water_roulette",
        stake,
    )


def casino(balance):
    while True:
        balance = restore_empty_balance(balance)
        show_banner(balance)
        options = available_mode_options({
            "roulette": "bet on a number, color, parity, half, or dozen",
            "cards": "high card or blackjack",
            "jackpot": "match symbols on the reels",
            "dice": "pick one face or two faces that must both appear",
            "job": f"type a random sentence in {JOB_TIME_LIMIT} seconds",
            "water_roulette": (
                "take turns in a toy water-blaster game; survive or get splashed"
            ),
            "back": "return to the main menu",
        }, {
            "roulette": "roulette",
            "jackpot": "jackpot",
            "dice": "dice",
            "job": "job",
            "water_roulette": "water_roulette",
        })
        choice = prompt_menu("CASINO", options)
        if choice == "roulette":
            balance = roulette(balance)
        elif choice == "cards":
            balance = cards(balance)
        elif choice == "jackpot":
            balance = jackpot_wheel(balance)
        elif choice == "dice":
            balance = dice_roll(balance)
        elif choice == "job":
            balance = job(balance)
        elif choice == "water_roulette":
            balance = water_roulette(balance)
        else:
            return balance


def horse_racing(balance):
    win_boost, payout_boost = begin_round("horse", balance)
    horses = ("Comet", "Thunder", "Midnight", "Rocket", "Maple")
    print("\nHORSE RACING — choose a horse")
    selection_name = prompt_menu("Choose your horse:", {
        "comet": "grey",
        "thunder": "chestnut",
        "midnight": "dark",
        "rocket": "bay",
        "maple": "golden",
    })
    selection = ("comet", "thunder", "midnight", "rocket", "maple").index(selection_name)
    stake = prompt_stake(balance)
    balance -= stake
    winner = favored_outcome(
        selection,
        (index for index in range(len(horses)) if index != selection),
        90 if win_boost else SPORT_FAVOR_WEIGHT,
    )
    positions = [0] * len(horses)
    columns, rows = terminal_dimensions()
    finish = max(8, columns - 14)
    lane_rows = [
        2 + round(index * max(0, rows - 7) / (len(horses) - 1))
        for index in range(len(horses))
    ]
    frame_count = 0
    while max(positions) < finish:
        for index in range(len(horses)):
            positions[index] += random.randint(0, 3)
            if index != winner:
                positions[index] = min(positions[index], finish - 1)
        screen = ["\033[1;36mHORSE RACE  |  FINISH: " + "-" * max(1, columns - 27) + ">\033[0m"]
        screen.extend([""] * (rows - 1))
        for index, horse in enumerate(horses):
            distance = min(positions[index], finish)
            track = "=" * distance + ">" + "." * (finish - distance)
            screen[lane_rows[index]] = f"{horse:<8} |{track}|"
        screen[-2] = " " * max(0, columns // 2 - 12) + "[ FINISH LINE ]"
        draw_fullscreen(screen)
        frame_count += 1
        time.sleep(max(0.06, ANIMATION_DELAY * 1.2 - frame_count * 0.001))
        if max(positions) >= finish:
            break
    positions[winner] = max(positions) + 1
    time.sleep(0.5)
    print(f"\n\033[1;35m{horses[winner]} wins the race!\033[0m")
    won = selection == winner
    payout = stake * HORSE_RETURN if won else 0
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "horse", stake)
    return balance


def animate_match_game(title, home_marker, away_marker, outcome, steps=26):
    width, height = terminal_dimensions()
    field_width = max(10, width - 10)
    field_length = field_width - 2
    status_row = max(5, height // 2)
    soccer_goal = outcome if outcome in ("home", "away") else None
    nrl_penalty = outcome not in ("none", "home", "away")

    for frame in range(steps):
        progress = frame / (steps - 1)
        attack_from_left = soccer_goal != "away" if title == "SOCCER" else True
        ball_position = round(progress * (field_length - 1))
        if not attack_from_left:
            ball_position = field_length - 1 - ball_position
        is_final_sequence = frame >= steps - 5

        if title == "SOCCER":
            pitch = ["-"] * field_length
            pitch[field_length // 2] = "|"
            pitch[ball_position] = "o"
            if is_final_sequence and soccer_goal:
                action = f"GOAL! {home_marker if outcome == 'home' else away_marker} finds the net!"
            elif is_final_sequence:
                action = "Shot on target... saved! Full time: no goal."
            elif progress < 0.25:
                action = f"{home_marker} builds from the back and moves into attack."
            elif progress < 0.55:
                action = f"{away_marker} presses as the ball moves through midfield."
            else:
                action = "A quick pass opens space near the penalty area!"
            field = f"{home_marker} [" + "".join(pitch) + f"] {away_marker}"
            heading = "SOCCER  |  ATTACK BUILD-UP"
        else:
            pitch = ["-"] * field_length
            for yard_line in range(5, field_length, 10):
                pitch[yard_line] = "+"
            pitch[ball_position] = "o"
            if is_final_sequence and nrl_penalty:
                action = f"REFEREE: penalty to {outcome.title()}!"
            elif is_final_sequence:
                action = "Play continues — no penalty called."
            elif progress < 0.25:
                action = "Kick-off! The defensive line charges forward."
            elif progress < 0.55:
                action = "Tackle made — players reset for the next play-the-ball."
            else:
                action = "The attack probes the line; the referee watches closely."
            field = f"{home_marker} [" + "".join(pitch) + f"] {away_marker}"
            heading = "NRL  |  FIVE-TACKLE SET"

        screen = [f"\033[1;36m{heading}  |  SIMULATED MATCH\033[0m"]
        screen.extend([""] * (height - 1))
        screen[2] = "+" + "-" * field_width + "+"
        screen[3] = field
        screen[4] = "+" + "-" * field_width + "+"
        screen[status_row] = " " * max(0, width // 2 - len(action) // 2) + action
        screen[-2] = " " * max(0, width // 2 - 17) + (
            "The match result is simulated."
        )
        draw_fullscreen(screen)
        time.sleep(ANIMATION_DELAY * 0.9)


def soccer_first_scorer(balance):
    win_boost, payout_boost = begin_round("soccer", balance)
    teams = {"home": "Harbour FC", "away": "Mountain United"}
    print("\nSOCCER — who scores first?")
    selection = prompt_menu("Choose who scores first:", {
        "home": "Harbour FC",
        "away": "Mountain United",
        "none": "no goal",
    })
    stake = prompt_stake(balance)
    balance -= stake
    outcome = favored_outcome(
        selection,
        (option for option in ("home", "away", "none") if option != selection),
        90 if win_boost else SPORT_FAVOR_WEIGHT,
    )
    animate_match_game("SOCCER", "H", "M", outcome)
    if outcome == "none":
        print("Full time: no goals were scored.")
    else:
        print(f"\033[1;35mGOAL! {teams[outcome]} scores first!\033[0m")
    won = selection == outcome
    multiplier = SOCCER_NO_GOAL_RETURN if outcome == "none" else SOCCER_TEAM_RETURN
    payout = stake * multiplier if won else 0
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "soccer", stake)
    return balance


def nrl_first_penalty(balance):
    win_boost, payout_boost = begin_round("nrl", balance)
    players = {
        "alex": "Alex Carter",
        "jord": "Jordan Lee",
        "sam": "Sam Taylor",
        "riley": "Riley Morgan",
    }
    print("\nNRL — who gives away the first penalty?")
    selection = prompt_menu("Choose a player:", {
        "alex": "Alex Carter",
        "jord": "Jordan Lee",
        "sam": "Sam Taylor",
        "riley": "Riley Morgan",
        "none": "no penalty",
    })
    stake = prompt_stake(balance)
    balance -= stake
    outcome = favored_outcome(
        selection,
        (option for option in ("alex", "jord", "sam", "riley", "none") if option != selection),
        90 if win_boost else SPORT_FAVOR_WEIGHT,
    )
    animate_match_game("NRL", "A", "B", outcome)
    if outcome == "none":
        print("\033[1;35mThe match ends without a penalty.\033[0m")
    else:
        print(f"\033[1;35mFirst penalty: {players[outcome]}\033[0m")
    won = selection == outcome
    multiplier = NRL_NO_PENALTY_RETURN if outcome == "none" else NRL_PLAYER_RETURN
    payout = stake * multiplier if won else 0
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "nrl", stake)
    return balance


def boxing_match(balance):
    win_boost, payout_boost = begin_round("boxing", balance)
    fighters = {"red": "Atlas King", "blue": "Milo Stone"}
    print("\nBOXING — pick the winner")
    selection = prompt_menu("Choose your fighter:", {
        "red": f"{fighters['red']} (red corner)",
        "blue": f"{fighters['blue']} (blue corner)",
    })
    stake = prompt_stake(balance)
    balance -= stake
    outcome = favored_outcome(
        selection,
        (corner for corner in fighters if corner != selection),
        90 if win_boost else SPORT_FAVOR_WEIGHT,
    )

    width, height = terminal_dimensions()
    rounds = 5
    red_health = blue_health = 100
    print("\nThe bell rings — five-round exhibition!")
    for round_number in range(1, rounds + 1):
        for exchange in range(4):
            red_attacks = (round_number + exchange) % 2 == 0
            if red_attacks:
                blue_health = max(15, blue_health - random.randint(2, 8))
                action = f"{fighters['red']} throws a combination!"
            else:
                red_health = max(15, red_health - random.randint(2, 8))
                action = f"{fighters['blue']} counters with a sharp jab!"
            screen = [
                f"\033[1;36mBOXING  |  ROUND {round_number}/{rounds}\033[0m",
                "",
                f"RED  {fighters['red']:<14} [{'#' * (red_health // 10):<10}] {red_health:>3}%",
                f"BLUE {fighters['blue']:<14} [{'#' * (blue_health // 10):<10}] {blue_health:>3}%",
                "",
                " " * max(0, width // 2 - len(action) // 2) + action,
                "",
                " " * max(0, width // 2 - 15) + "The result is simulated.",
            ]
            draw_fullscreen(screen + [""] * max(0, height - len(screen)))
            time.sleep(ANIMATION_DELAY * 1.2)

    print(f"\n\033[1;35mThe judges award the bout to {fighters[outcome]}!\033[0m")
    won = selection == outcome
    payout = stake * BOXING_RETURN if won else 0
    payout = apply_payout_boost(payout, won, payout_boost)
    balance += payout
    balance = show_result(won, payout, balance, "boxing", stake)
    return balance


def sport(balance):
    while True:
        balance = restore_empty_balance(balance)
        show_banner(balance)
        options = available_mode_options({
            "horse": "pick a winner in an animated race",
            "soccer": "pick who scores the first goal",
            "nrl": "pick who gives away the first penalty",
            "boxing": "pick the winner of a five-round animated bout",
            "back": "return to the main menu",
        }, {
            "horse": "horse",
            "soccer": "soccer",
            "nrl": "nrl",
            "boxing": "boxing",
        })
        choice = prompt_menu("SPORT — simulated fixtures", options)
        if choice == "horse":
            balance = horse_racing(balance)
        elif choice == "soccer":
            balance = soccer_first_scorer(balance)
        elif choice == "nrl":
            balance = nrl_first_penalty(balance)
        elif choice == "boxing":
            balance = boxing_match(balance)
        else:
            return balance


def show_market(balance):
    print("\nSTOCK MARKET — simulated play-money market")
    print(f"Balance: {format_money(balance)} | Market round: {MARKET_ROUND}")
    print("Asset            Price/share   Minimum/share   Shares held   Holding value")
    for asset, details in MARKET_ASSETS.items():
        shares = MARKET_HOLDINGS[asset]
        price = MARKET_PRICES[asset]
        print(
            f"{details['name']:<16} {format_money(price):<12} "
            f"{format_money(MARKET_MIN_PRICES[asset]):<14} {shares:<13} "
            f"{format_money(shares * price)}"
        )
    print(
        "Each minimum rises 10% when its share price is at least 10% above it."
    )
    portfolio_value = sum(
        MARKET_HOLDINGS[asset] * MARKET_PRICES[asset]
        for asset in MARKET_ASSETS
    )
    print(f"Total portfolio value: {format_money(portfolio_value)}")
    changed_event_chances = {
        event: chance
        for event, chance in MARKET_EVENT_CHANCES.items()
        if chance != MARKET_EVENT_DEFAULTS[event]
    }
    if changed_event_chances:
        print("\nChanged market event chances:")
        for event, chance in changed_event_chances.items():
            print(f"  {MARKET_EVENT_NAMES[event]}: {chance}%")
    else:
        print("\nNo market event chances have been changed.")
    if ODDS_CHANGE_ROUNDS_REMAINING:
        print(
            f"Temporary odds expire in "
            f"{ODDS_CHANGE_ROUNDS_REMAINING} market round(s)."
        )


def pay_odds_service(balance, cost_rate, minimum_cost):
    cost = max(minimum_cost, math.ceil(balance * cost_rate))
    if cost > balance:
        print(
            f"You need at least {format_money(minimum_cost)} to use this service; "
            f"your balance is {format_money(balance)}."
        )
        return balance, False
    return balance - cost, True


def adjust_random_market_event_odds(balance):
    global ODDS_CHANGE_ROUNDS_REMAINING
    balance, paid = pay_odds_service(
        balance,
        ODDS_UPGRADE_COST_RATE,
        ODDS_UPGRADE_MIN_COST,
    )
    if not paid:
        return balance

    event = random.choice(tuple(MARKET_EVENT_CHANCES))
    old_chance = MARKET_EVENT_CHANCES[event]
    directions = tuple(
        direction
        for direction in (-1, 1)
        if 0 <= old_chance + direction * ODDS_CHANGE_PERCENTAGE_POINTS <= 100
    )
    direction = random.choice(directions)
    new_chance = max(
        0,
        min(
            100,
            old_chance + direction * ODDS_CHANGE_PERCENTAGE_POINTS,
        ),
    )
    MARKET_EVENT_CHANCES[event] = new_chance
    ODDS_CHANGE_ROUNDS_REMAINING = ODDS_CHANGE_DURATION
    change = new_chance - old_chance
    direction_word = "increased" if change > 0 else "decreased"
    print(
        f"Paid for event odds adjustment. {MARKET_EVENT_NAMES[event]} "
        f"chance {direction_word} from {old_chance}% to {new_chance}% "
        f"for up to {ODDS_CHANGE_DURATION} market rounds."
    )
    save_balance(balance)
    return balance


def reset_market_event_odds(balance):
    global MARKET_EVENT_CHANCES, ODDS_CHANGE_ROUNDS_REMAINING
    balance, paid = pay_odds_service(
        balance,
        ODDS_RESET_COST_RATE,
        ODDS_RESET_MIN_COST,
    )
    if not paid:
        return balance

    MARKET_EVENT_CHANCES = dict(MARKET_EVENT_DEFAULTS)
    ODDS_CHANGE_ROUNDS_REMAINING = 0
    print("All market event chances have been reset to their defaults.")
    save_balance(balance)
    return balance


def show_market_history():
    print("\nSTOCK MARKET HISTORY — last 15 market rounds")
    if not MARKET_HISTORY:
        print("No market history yet. Advance a market round to start the graph.")
        input("Press Enter to return...")
        return

    graph_width = 30
    for asset, details in MARKET_ASSETS.items():
        asset_history = [
            (
                entry["round"],
                entry["prices"].get(asset, details["initial_price"]),
            )
            for entry in MARKET_HISTORY
        ]
        highest_price = max(price for _, price in asset_history)
        print(f"\n{details['name']}:")
        for market_round, price in asset_history:
            bar_length = max(1, round(price / highest_price * graph_width))
            print(
                f"R{market_round:>4} {format_money(price):>7} | "
                f"{'#' * bar_length}"
            )
    input("Press Enter to return...")


def choose_market_asset():
    choice = prompt_menu("Choose an asset:", {
        asset: details["name"] for asset, details in MARKET_ASSETS.items()
    })
    return choice


def invest_in_market(balance):
    asset = choose_market_asset()
    price = MARKET_PRICES[asset]
    affordable_shares = balance // price
    if affordable_shares == 0:
        print(f"You need at least {format_money(price)} to buy one share.")
        return balance
    shares = prompt_int(
        f"Shares to buy at {format_money(price)} each "
        f"(up to {affordable_shares}): ",
        1,
        affordable_shares,
    )
    cost = shares * price
    balance -= cost
    MARKET_HOLDINGS[asset] += shares
    save_balance(balance)
    print(
        f"Bought {shares} {MARKET_ASSETS[asset]['name']} share(s) "
        f"for {format_money(cost)}."
    )
    return balance


def sell_market_shares(balance):
    asset = choose_market_asset()
    shares_owned = MARKET_HOLDINGS[asset]
    if shares_owned == 0:
        print(f"You don't own any {MARKET_ASSETS[asset]['name']} shares.")
        return balance
    shares = prompt_int(
        f"Shares to sell (you own {shares_owned}): ",
        1,
        shares_owned,
    )
    proceeds = shares * MARKET_PRICES[asset]
    MARKET_HOLDINGS[asset] -= shares
    balance += proceeds
    save_balance(balance)
    print(
        f"Sold {shares} {MARKET_ASSETS[asset]['name']} share(s) "
        f"for {format_money(proceeds)}."
    )
    return balance


def update_market_prices():
    global MARKET_PRICE_FREEZE_ROUNDS
    previous_directions = {}
    if len(MARKET_HISTORY) >= 2:
        previous_prices = MARKET_HISTORY[-2]["prices"]
        latest_prices = MARKET_HISTORY[-1]["prices"]
        for asset in MARKET_ASSETS:
            if latest_prices[asset] > previous_prices[asset]:
                previous_directions[asset] = "up"
            elif latest_prices[asset] < previous_prices[asset]:
                previous_directions[asset] = "down"

    for asset, details in MARKET_ASSETS.items():
        previous_direction = previous_directions.get(asset)
        if (
            asset != "casino_stores"
            and previous_direction
            and random.random() < MARKET_TREND_CONTINUATION_CHANCE
        ):
            direction = previous_direction
        else:
            direction = random.choice(("up", "down"))
        old_price = MARKET_PRICES[asset]
        if direction == "steady":
            new_price = old_price
            movement = "steady"
        else:
            change_percent = random.randint(*details["volatility"]) / 100
            multiplier = (
                1 + change_percent if direction == "up" else 1 - change_percent
            )
            new_price = max(
                MARKET_MIN_PRICES[asset],
                round(old_price * multiplier),
            )
            movement = "higher" if direction == "up" else "lower"
        MARKET_PRICES[asset] = new_price
        print(
            f"{details['name']}: {movement}, "
            f"{format_money(old_price)} -> {format_money(new_price)} per share."
        )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["gold_discovery"]:
        old_price = MARKET_PRICES["gold"]
        MARKET_PRICES["gold"] = max(
            MARKET_MIN_PRICES["gold"],
            math.floor(old_price * (1 + GOLD_DISCOVERY_RISE_RATE)),
        )
        print(
            f"\033[1;32mA major gold discovery sends gold soaring "
            f"{GOLD_DISCOVERY_RISE_RATE:.0%}: {format_money(old_price)} -> "
            f"{format_money(MARKET_PRICES['gold'])} per share.\033[0m"
        )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["gold_mine"]:
        old_price = MARKET_PRICES["gold"]
        MARKET_PRICES["gold"] = max(
            MARKET_MIN_PRICES["gold"],
            math.floor(old_price * (1 - GOLD_MINE_DROP_RATE)),
        )
        print(
            f"\033[1;31mA massive gold mine was formed, causing gold to "
            f"drop {GOLD_MINE_DROP_RATE:.0%}: {format_money(old_price)} -> "
            f"{format_money(MARKET_PRICES['gold'])} per share.\033[0m"
        )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["dip"]:
        for asset, details in MARKET_ASSETS.items():
            old_price = MARKET_PRICES[asset]
            MARKET_PRICES[asset] = max(
                MARKET_MIN_PRICES[asset],
                math.floor(old_price * (1 - MARKET_DIP_RATE)),
            )
            print(
                f"\033[1;31mMajor market dip: {details['name']} drops "
                f"{MARKET_DIP_RATE:.0%}, {format_money(old_price)} -> "
                f"{format_money(MARKET_PRICES[asset])} per share.\033[0m"
            )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["rally"]:
        for asset, details in MARKET_ASSETS.items():
            old_price = MARKET_PRICES[asset]
            MARKET_PRICES[asset] = math.floor(
                old_price * (1 + MARKET_RALLY_RATE)
            )
            print(
                f"\033[1;32mMarket rally: {details['name']} rises "
                f"{MARKET_RALLY_RATE:.0%}, {format_money(old_price)} -> "
                f"{format_money(MARKET_PRICES[asset])} per share.\033[0m"
            )
    crashed = random.randint(1, 100) <= MARKET_EVENT_CHANCES["crash"]
    if crashed:
        crash_percent = random.randint(25, 50)
        for asset, details in MARKET_ASSETS.items():
            old_price = MARKET_PRICES[asset]
            old_shares = MARKET_HOLDINGS[asset]
            MARKET_PRICES[asset] = max(
                MARKET_MIN_PRICES[asset],
                math.floor(old_price * (100 - crash_percent) / 100),
            )
            MARKET_HOLDINGS[asset] = math.floor(
                old_shares * (100 - crash_percent) / 100
            )
            print(
                f"\033[1;31mStock market crash! {details['name']} falls "
                f"{format_money(old_price)} -> "
                f"{format_money(MARKET_PRICES[asset])} per share; "
                f"your shares fall from {old_shares} to "
                f"{MARKET_HOLDINGS[asset]} ({crash_percent}% crash).\033[0m"
            )
        MARKET_PRICE_FREEZE_ROUNDS = 3
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["ai_loss"]:
        old_price = MARKET_PRICES["ai"]
        MARKET_PRICES["ai"] = max(
            MARKET_MIN_PRICES["ai"],
            math.floor(old_price * (1 - AI_EXTRA_LOSS_RATE)),
        )
        print(
            f"\033[1;31mAI stock drops an extra "
            f"{AI_EXTRA_LOSS_RATE:.0%}: {format_money(old_price)} -> "
            f"{format_money(MARKET_PRICES['ai'])} per share.\033[0m"
        )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["skyrocket"]:
        for asset, details in MARKET_ASSETS.items():
            old_price = MARKET_PRICES[asset]
            MARKET_PRICES[asset] = math.floor(
                old_price * (1 + MARKET_SKYROCKET_RATE)
            )
            print(
                f"\033[1;32mThe market skyrockets! {details['name']} rises "
                f"{MARKET_SKYROCKET_RATE:.0%}, {format_money(old_price)} -> "
                f"{format_money(MARKET_PRICES[asset])} per share.\033[0m"
            )


def raise_market_minimums():
    for asset, price in MARKET_PRICES.items():
        minimum_price = MARKET_MIN_PRICES[asset]
        next_minimum = (minimum_price * 11 + 9) // 10
        if price >= next_minimum:
            MARKET_MIN_PRICES[asset] = next_minimum


def advance_market_round(balance):
    global MARKET_ROUND, MARKET_PRICE_FREEZE_ROUNDS
    global MARKET_EVENT_CHANCES, ODDS_CHANGE_ROUNDS_REMAINING
    print("\nMarket update:")
    if MARKET_PRICE_FREEZE_ROUNDS:
        print(
            f"Stock prices are frozen after the crash for "
            f"{MARKET_PRICE_FREEZE_ROUNDS} more market round(s)."
        )
        MARKET_PRICE_FREEZE_ROUNDS -= 1
        raise_market_minimums()
    else:
        update_market_prices()
        raise_market_minimums()
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["broker_theft"]:
        stolen_holdings = {}
        for asset, details in MARKET_ASSETS.items():
            shares = math.floor(
                MARKET_HOLDINGS[asset] * BROKER_THEFT_RATE
            )
            if shares:
                MARKET_HOLDINGS[asset] -= shares
                stolen_holdings[asset] = shares
                print(
                    f"\033[1;31mA crooked broker steals {shares} "
                    f"{details['name']} share(s), "
                    f"{BROKER_THEFT_RATE:.0%} of your holdings.\033[0m"
                )
        if not stolen_holdings:
            print("A crooked broker tried to steal shares, but you own none.")
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["virus"]:
        casino_shares = MARKET_HOLDINGS["casino_stores"]
        if casino_shares:
            shares_lost = min(
                casino_shares,
                math.ceil(casino_shares * 0.75),
            )
            MARKET_HOLDINGS["casino_stores"] -= shares_lost
            print(
                f"\033[1;31mVirus installed! It corrupts your Casino Stores "
                f"shares: {shares_lost} of {casino_shares} shares lost "
                "(75%, rounded up to whole shares).\033[0m"
            )
        else:
            print(
                "\033[1;31mVirus installed! It targets Casino Stores, "
                "but you own no shares there.\033[0m"
            )
    if random.randint(1, 100) <= MARKET_EVENT_CHANCES["friendly_broker"]:
        gifted_shares = {}
        for _ in range(3):
            asset = random.choice(tuple(MARKET_ASSETS))
            MARKET_HOLDINGS[asset] += 1
            gifted_shares[asset] = gifted_shares.get(asset, 0) + 1
        gift_summary = ", ".join(
            f"{shares} {MARKET_ASSETS[asset]['name']}"
            f"{' share' if shares == 1 else ' shares'}"
            for asset, shares in gifted_shares.items()
        )
        print(
            f"\033[1;32mA friendly broker gives you 3 random shares: "
            f"{gift_summary}.\033[0m"
        )
    MARKET_ROUND += 1
    MARKET_HISTORY.append({
        "round": MARKET_ROUND,
        "prices": dict(MARKET_PRICES),
    })
    del MARKET_HISTORY[:-15]
    if MARKET_ROUND % MARKET_PAYOUT_INTERVAL == 0:
        proceeds = 0
        sold_holdings = {}
        for asset, details in MARKET_ASSETS.items():
            shares = math.floor(
                MARKET_HOLDINGS[asset] * MARKET_PAYOUT_PERCENT / 100
            )
            if shares:
                sold_holdings[asset] = shares
                MARKET_HOLDINGS[asset] -= shares
                proceeds += shares * MARKET_PRICES[asset]
        balance += proceeds
        print(
            f"\nEvery-{MARKET_PAYOUT_INTERVAL}-round share sale "
            f"({MARKET_PAYOUT_PERCENT}% at current prices):"
        )
        if sold_holdings:
            for asset, shares in sold_holdings.items():
                value = shares * MARKET_PRICES[asset]
                print(
                    f"Sold {shares} {MARKET_ASSETS[asset]['name']} share(s) "
                    f"for {format_money(value)}."
                )
        else:
            print("No whole shares were available to sell.")
        print(f"Sale proceeds added to cash: {format_money(proceeds)}.")
    if ODDS_CHANGE_ROUNDS_REMAINING:
        ODDS_CHANGE_ROUNDS_REMAINING -= 1
        if ODDS_CHANGE_ROUNDS_REMAINING == 0:
            MARKET_EVENT_CHANCES = dict(MARKET_EVENT_DEFAULTS)
            print("Temporary market event odds have expired and reset to defaults.")
    advance_duckcoin_round(balance)
    return balance


def duckcoin_market_price(balance):
    wealth_scale = max(balance, STARTING_BALANCE)
    price_rate = min(0.015, 0.003 + DUCKCOIN_ROUND * 0.00003)
    return max(5, math.floor(wealth_scale * price_rate))


def duckcoin_mining_performance():
    return (
        DUCKCOIN_COMPONENTS["gpu"] * 2
        + DUCKCOIN_COMPONENTS["cpu"]
        + DUCKCOIN_COMPONENTS["memory"]
        + (DUCKCOIN_PC_GENERATION - 1) * 2
    )


def duckcoin_software_requirement():
    return 3 + DUCKCOIN_SOFTWARE_VERSION * 2


def advance_duckcoin_round(balance):
    global DUCKCOIN_BALANCE, DUCKCOIN_ROUND
    global DUCKCOIN_SOFTWARE_VERSION, DUCKCOIN_ROUNDS_TO_UPDATE
    global DUCKCOIN_PC_OUTDATED
    global DUCKCOIN_WATER_SPILL_ROUNDS

    DUCKCOIN_ROUND += 1
    DUCKCOIN_ROUNDS_TO_UPDATE -= 1
    if DUCKCOIN_ROUNDS_TO_UPDATE == 0:
        DUCKCOIN_SOFTWARE_VERSION += 1
        DUCKCOIN_ROUNDS_TO_UPDATE = DUCKCOIN_UPDATE_INTERVAL
        print(
            f"\n\033[1;36mDuckcoin mining software updated to "
            f"v{DUCKCOIN_SOFTWARE_VERSION}.\033[0m"
        )
        if (
            not DUCKCOIN_PC_OUTDATED
            and random.randint(1, 100) <= DUCKCOIN_TECH_ADVANCEMENT_CHANCE
        ):
            DUCKCOIN_PC_OUTDATED = True
            print(
                "\033[1;33mA technology breakthrough requires a new PC "
                "and all-new components. Mining is severely slowed until "
                "you replace your computer.\033[0m"
            )

    performance = duckcoin_mining_performance()
    efficiency = min(1.0, performance / duckcoin_software_requirement())
    if DUCKCOIN_PC_OUTDATED:
        efficiency = min(efficiency, 0.15)
    base_generation = (
        0.3
        + DUCKCOIN_COMPONENTS["gpu"] * 0.2
        + DUCKCOIN_COMPONENTS["cpu"] * 0.1
        + DUCKCOIN_COMPONENTS["memory"] * 0.05
        + DUCKCOIN_SOFTWARE_VERSION * 0.1
    )
    water_spill_active = DUCKCOIN_WATER_SPILL_ROUNDS > 0
    if water_spill_active:
        DUCKCOIN_WATER_SPILL_ROUNDS -= 1
        print(
            f"\033[1;31mWater spill recovery: no Duckcoin earned this round. "
            f"{DUCKCOIN_WATER_SPILL_ROUNDS} round(s) remain.\033[0m"
        )
    elif random.randint(1, 100) <= DUCKCOIN_WATER_SPILL_CHANCE:
        spill_duration = random.randint(*DUCKCOIN_WATER_SPILL_DURATION)
        DUCKCOIN_WATER_SPILL_ROUNDS = spill_duration - 1
        water_spill_active = True
        print(
            f"\033[1;31mWater spill! Mining is stopped for "
            f"{spill_duration} rounds while the PC dries out.\033[0m"
        )

    generated = (
        0.0
        if water_spill_active
        else round(base_generation * efficiency, 3)
    )
    DUCKCOIN_BALANCE = round(DUCKCOIN_BALANCE + generated, 3)
    price = duckcoin_market_price(balance)
    if not water_spill_active:
        print(
            f"Duckcoin mining: +{generated:.3f} Duckcoin "
            f"(wallet {DUCKCOIN_BALANCE:.3f}; "
            f"current value {format_money(price)} per coin)."
        )


def show_duckcoin(balance):
    performance = duckcoin_mining_performance()
    requirement = duckcoin_software_requirement()
    efficiency = min(1.0, performance / requirement)
    if DUCKCOIN_PC_OUTDATED:
        efficiency = min(efficiency, 0.15)
    coin_price = duckcoin_market_price(balance)
    wallet_value = math.floor(DUCKCOIN_BALANCE * coin_price)
    print("\nDUCKCOIN — computer-powered crypto mining")
    print(
        f"Cash balance: {format_money(balance)} | "
        f"Mining round: {DUCKCOIN_ROUND}"
    )
    print(
        f"Duckcoin wallet: {DUCKCOIN_BALANCE:.3f} "
        f"(about {format_money(wallet_value)} "
        f"at {format_money(coin_price)} per coin)"
    )
    print(
        f"PC generation {DUCKCOIN_PC_GENERATION} | Software v"
        f"{DUCKCOIN_SOFTWARE_VERSION} "
        f"(updates in {DUCKCOIN_ROUNDS_TO_UPDATE} round(s))"
    )
    if DUCKCOIN_WATER_SPILL_ROUNDS:
        print(
            f"\033[1;31mWater spill recovery: no mining for "
            f"{DUCKCOIN_WATER_SPILL_ROUNDS} more round(s).\033[0m"
        )
    print(f"Highest cash balance: {format_money(MAX_BALANCE_REACHED)}")
    print(
        f"Hardware: GPU tier {DUCKCOIN_COMPONENTS['gpu']}, "
        f"CPU tier {DUCKCOIN_COMPONENTS['cpu']}, "
        f"Memory tier {DUCKCOIN_COMPONENTS['memory']}"
    )
    print(
        f"Mining performance: {performance}/{requirement} "
        f"({efficiency:.0%} efficiency)"
    )
    if DUCKCOIN_PC_OUTDATED:
        print("\033[1;31mYour PC is outdated; mining is capped at 15% speed.\033[0m")


def duckcoin_component_upgrade_cost(balance, component):
    next_tier = DUCKCOIN_COMPONENTS[component] + 1
    software_scale = 1 + (DUCKCOIN_SOFTWARE_VERSION - 1) * 0.08
    base_cost = math.ceil(
        DUCKCOIN_COMPONENTS_BASE_COST[component]
        * next_tier
        * DUCKCOIN_PC_GENERATION
        * software_scale
    )
    balance_cost = math.ceil(
        max(balance, MAX_BALANCE_REACHED, STARTING_BALANCE)
        * DUCKCOIN_COMPONENT_BALANCE_RATE[component]
    )
    return max(base_cost, balance_cost)


def upgrade_duckcoin_component(balance, component):
    maximum_tier = DUCKCOIN_PC_GENERATION + 2
    current_tier = DUCKCOIN_COMPONENTS[component]
    if current_tier >= maximum_tier:
        print(
            f"Your {component.upper()} is already at the current PC's "
            f"maximum tier ({maximum_tier})."
        )
        return balance

    cost = duckcoin_component_upgrade_cost(balance, component)
    if cost > balance:
        print(
            f"The {component.upper()} upgrade costs {format_money(cost)}; "
            f"your cash balance is {format_money(balance)}."
        )
        return balance

    DUCKCOIN_COMPONENTS[component] += 1
    balance -= cost
    print(
        f"Upgraded your {component.upper()} to tier "
        f"{DUCKCOIN_COMPONENTS[component]} for {format_money(cost)}."
    )
    save_balance(balance)
    return balance


def duckcoin_pc_upgrade_cost(balance):
    stage_scale = 1 + (DUCKCOIN_SOFTWARE_VERSION - 1) * 0.15
    base_cost = math.ceil(
        DUCKCOIN_PC_BASE_COST * DUCKCOIN_PC_GENERATION ** 2 * stage_scale
    )
    balance_cost = math.ceil(
        max(balance, MAX_BALANCE_REACHED, STARTING_BALANCE)
        * DUCKCOIN_PC_BALANCE_RATE
    )
    return max(base_cost, balance_cost)


def replace_duckcoin_pc(balance):
    global DUCKCOIN_PC_GENERATION, DUCKCOIN_COMPONENTS, DUCKCOIN_PC_OUTDATED
    cost = duckcoin_pc_upgrade_cost(balance)
    if cost > balance:
        print(
            f"A complete next-generation PC costs {format_money(cost)}; "
            f"your cash balance is {format_money(balance)}. "
            "Save up before replacing it."
        )
        return balance

    DUCKCOIN_PC_GENERATION += 1
    DUCKCOIN_COMPONENTS = {
        component: DUCKCOIN_PC_GENERATION
        for component in DUCKCOIN_COMPONENTS
    }
    DUCKCOIN_PC_OUTDATED = False
    balance -= cost
    print(
        f"Bought a complete generation {DUCKCOIN_PC_GENERATION} PC "
        f"with new GPU, CPU, and memory for {format_money(cost)}. Mining software "
        "is already up to date."
    )
    save_balance(balance)
    return balance


def sell_duckcoin(balance):
    global DUCKCOIN_BALANCE
    if DUCKCOIN_BALANCE <= 0:
        print("You have no Duckcoin to sell.")
        return balance

    coin_price = duckcoin_market_price(balance)
    proceeds = math.floor(DUCKCOIN_BALANCE * coin_price)
    sold = DUCKCOIN_BALANCE
    DUCKCOIN_BALANCE = 0.0
    balance += proceeds
    print(
        f"Sold {sold:.3f} Duckcoin for {format_money(proceeds)} "
        f"({format_money(coin_price)} per coin)."
    )
    save_balance(balance)
    return balance


def duckcoin_mining(balance):
    while True:
        show_banner(balance)
        show_duckcoin(balance)
        options = {
            "gpu": (
                f"upgrade GPU to tier {DUCKCOIN_COMPONENTS['gpu'] + 1} "
                f"for {format_money(duckcoin_component_upgrade_cost(balance, 'gpu'))}"
                if DUCKCOIN_COMPONENTS["gpu"] < DUCKCOIN_PC_GENERATION + 2
                else "GPU is at the current PC's maximum tier"
            ),
            "cpu": (
                f"upgrade CPU to tier {DUCKCOIN_COMPONENTS['cpu'] + 1} "
                f"for {format_money(duckcoin_component_upgrade_cost(balance, 'cpu'))}"
                if DUCKCOIN_COMPONENTS["cpu"] < DUCKCOIN_PC_GENERATION + 2
                else "CPU is at the current PC's maximum tier"
            ),
            "memory": (
                f"upgrade memory to tier {DUCKCOIN_COMPONENTS['memory'] + 1} "
                f"for {format_money(duckcoin_component_upgrade_cost(balance, 'memory'))}"
                if DUCKCOIN_COMPONENTS["memory"] < DUCKCOIN_PC_GENERATION + 2
                else "memory is at the current PC's maximum tier"
            ),
            "new_pc": (
                f"replace the entire PC and all components for "
                f"{format_money(duckcoin_pc_upgrade_cost(balance))}"
            ),
            "sell": "sell all Duckcoin in your wallet for cash",
            "back": "return to the main menu",
        }
        choice = prompt_menu("DUCKCOIN MINING", options)
        if choice in DUCKCOIN_COMPONENTS:
            balance = upgrade_duckcoin_component(balance, choice)
        elif choice == "new_pc":
            balance = replace_duckcoin_pc(balance)
        elif choice == "sell":
            balance = sell_duckcoin(balance)
        else:
            return balance


def investment_market(balance):
    while True:
        show_banner(balance)
        show_market(balance)
        choice = prompt_menu("MARKET", {
            "buy": "invest your balance in shares",
            "sell": "sell shares you own",
            "next": (
                f"advance one market round (minimum "
                f"{format_money(MARKET_ROUND_MIN_COST)}; 10–15% if higher)"
            ),
            "history": "view ASCII graphs of the last 15 market rounds",
            "adjust_odds": (
                f"pay 90% of cash (minimum {format_money(ODDS_UPGRADE_MIN_COST)}) "
                "to randomly change one event chance by ±10 points"
            ),
            "reset_odds": (
                f"pay 95% of cash (minimum {format_money(ODDS_RESET_MIN_COST)}) "
                "to restore all event chances to defaults"
            ),
            "back": "return to the main menu",
        })
        if choice == "buy":
            balance = invest_in_market(balance)
        elif choice == "sell":
            balance = sell_market_shares(balance)
        elif choice == "next":
            if balance < MARKET_ROUND_MIN_COST:
                print(
                    f"You need at least {format_money(MARKET_ROUND_MIN_COST)} "
                    "in cash "
                    "to advance a market round."
                )
                continue
            cost_percent = random.randint(*MARKET_ROUND_COST_PERCENT)
            round_cost = max(
                MARKET_ROUND_MIN_COST,
                math.ceil(balance * cost_percent / 100),
            )
            print(
                f"Advancing costs {cost_percent}% of your cash "
                f"(minimum {format_money(MARKET_ROUND_MIN_COST)}): "
                f"{format_money(round_cost)}."
            )
            balance -= round_cost
            balance = advance_market_round(balance)
            save_balance(balance)
            input("Press Enter to continue...")
        elif choice == "history":
            show_market_history()
        elif choice == "adjust_odds":
            balance = adjust_random_market_event_odds(balance)
        elif choice == "reset_odds":
            balance = reset_market_event_odds(balance)
        else:
            return balance


def main():
    balance = load_balance()
    while True:
        balance = restore_empty_balance(balance)
        show_banner(balance)
        options = available_mode_options({
            "casino": "roulette, card games, and the jackpot wheel",
            "sport": "simulated horse racing, soccer, NRL, and boxing",
            "market": "invest in gold, AI, and Casino Stores shares",
            "duckcoin": "mine crypto; upgrade costly PC parts and sell Duckcoin",
            "quit": "leave the game",
        }, {})
        choice = prompt_menu("Where would you like to go?", options)
        if choice == "casino":
            balance = casino(balance)
        elif choice == "sport":
            balance = sport(balance)
        elif choice == "market":
            balance = investment_market(balance)
        elif choice == "duckcoin":
            balance = duckcoin_mining(balance)
        else:
            save_balance(balance)
            print(f"Thanks for playing. Final balance: {format_money(balance)}")
            break


if __name__ == "__main__":
    main()