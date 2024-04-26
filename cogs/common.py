from bot_utilities.config_loader import load_current_language, load_instructions, config

# Chatbot and discord config

instructions = load_instructions()
allow_dm = config['ALLOW_DM']
active_channels = set()
trigger_words = config['TRIGGER']
smart_mention = config['SMART_MENTION']
presences = config["PRESENCES"]
presences_disabled = config["DISABLE_PRESENCE"]
internet_access = config['INTERNET_ACCESS']
instruc_config = config['DEFAULT_INSTRUCTION']

# Message history and config
message_history = {}
MAX_HISTORY = config['MAX_HISTORY']
replied_messages = {}
active_channels = {}

# Imagine config
blacklisted_words = config['BLACKLIST_WORDS']
prevent_nsfw = config['AI_NSFW_CONTENT_FILTER']

# Accessability
current_language = load_current_language()