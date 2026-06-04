import random
from collections import Counter, defaultdict
from .utils import safe_json_list, safe_json_dict

SURNAME_PARTS = {
    "civil": (["Nov", "Hart", "Bel", "Mor", "Val", "Rav", "Star"], ["ák", "man", "son", "ford", "brook", "stone"]),
    "poetic": (["Moon", "Sil", "Ael", "Star", "Lun", "Evers"], ["whisper", "leaf", "song", "bloom", "fall", "light"]),
    "clan": (["Iron", "Stone", "Hammer", "Gold", "Deep", "Fire"], ["beard", "hand", "forge", "shield", "born", "delver"]),
    "cozy": (["Apple", "Good", "Small", "Honey", "Green", "Under"], ["barrel", "hill", "field", "kettle", "bottle", "bush"]),
    "craft": (["Cog", "Fizz", "Copper", "Needle", "Spark", "Tinker"], ["wrench", "pin", "snap", "bolt", "wick", "gear"]),
    "virtue_or_vice": (["Ash", "Grim", "Red", "Vain", "Sorrow", "Hope"], ["mark", "thorn", "vow", "kiss", "scar", "veil"]),
    "brutal": (["Blood", "Iron", "Broken", "Skull", "Black", "Grim"], ["fist", "jaw", "tusk", "axe", "hide", "scar"]),
    "street": (["Rat", "Mud", "Coin", "Tin", "Sewer", "Quick"], ["finger", "bit", "snatch", "grin", "spark", "stab"]),
}

class SmartNameGenerator:
    """Offline AI-like generator.

    Není to API model. Je to lokální heuristický generátor:
    - bere vzorová jména rasy
    - naučí se obvyklé dvojice písmen
    - míchá slabiky podle pravidel rasy
    - filtruje špatně znějící výsledky
    - umí vytvořit příjmení podle kultury
    """

    def __init__(self, rng=None):
        self.rng = rng or random.Random()

    def generate(self, race_obj=None, style="smart", full_name=True):
        samples = safe_json_list(race_obj.sample_names) if race_obj else []
        templates = safe_json_list(race_obj.name_templates) if race_obj else []
        rules = safe_json_dict(getattr(race_obj, "name_rules", "{}")) if race_obj else {}

        if style == "template" and templates:
            first = self._first_name(samples, rules)
            last = self._surname(rules)
            try:
                return self.rng.choice(templates).format(first=first, last=last)
            except Exception:
                return f"{first} {last}" if full_name else first

        if style == "markov" and samples:
            first = self._markov(samples)
        else:
            first = self._first_name(samples, rules)

        if not full_name:
            return first

        if self.rng.random() < 0.55:
            return first

        return f"{first} {self._surname(rules)}"

    def _first_name(self, samples, rules):
        candidates = []
        for _ in range(30):
            if samples and self.rng.random() < 0.35:
                candidates.append(self._sample_blend(samples, rules))
            elif samples and self.rng.random() < 0.25:
                candidates.append(self._markov(samples))
            else:
                candidates.append(self._syllable_name(rules))

        candidates = [c for c in candidates if self._is_good(c, rules)]
        if not candidates:
            return self._syllable_name(rules)

        return max(candidates, key=lambda n: self._score(n, samples, rules)).capitalize()

    def _syllable_name(self, rules):
        start = rules.get("syllables_start") or ["A", "E", "Ka", "La", "Ro", "Va", "Mi"]
        mid = rules.get("syllables_mid") or ["ra", "lo", "mi", "ta", "cor", "ven"]
        end = rules.get("syllables_end") or ["el", "a", "o", "en", "is", "or"]

        pattern = self.rng.choice(["se", "sme", "sme", "smme", "see"])
        text = ""
        for p in pattern:
            if p == "s":
                text += self.rng.choice(start)
            elif p == "m":
                text += self.rng.choice(mid)
            else:
                text += self.rng.choice(end)
        return self._clean(text)

    def _sample_blend(self, samples, rules):
        a = self.rng.choice(samples)
        b = self.rng.choice(samples)
        a_cut = max(1, len(a) // 2 + self.rng.randint(-1, 1))
        b_cut = max(1, len(b) // 2 + self.rng.randint(-1, 1))
        return self._clean(a[:a_cut] + b[b_cut:])

    def _markov(self, samples, order=2, max_len=12):
        model = defaultdict(list)
        for name in samples:
            s = "^" * order + name.strip().lower() + "$"
            for i in range(len(s) - order):
                model[s[i:i + order]].append(s[i + order])

        key = "^" * order
        out = ""
        for _ in range(max_len):
            choices = model.get(key)
            if not choices:
                break
            ch = self.rng.choice(choices)
            if ch == "$":
                break
            out += ch
            key = (key + ch)[-order:]

        return self._clean(out)

    def _surname(self, rules):
        style = rules.get("surname_style", "civil")
        left, right = SURNAME_PARTS.get(style, SURNAME_PARTS["civil"])
        return self.rng.choice(left) + self.rng.choice(right)

    def _clean(self, text):
        text = "".join(ch for ch in text if ch.isalpha() or ch in "-' ")
        text = text.strip("-' ")
        while "  " in text:
            text = text.replace("  ", " ")
        return text.capitalize() or "Bezejmenný"

    def _is_good(self, name, rules):
        n = name.lower()
        if len(n) < 3 or len(n) > 16:
            return False
        if any(bad in n for bad in rules.get("forbidden", [])):
            return False
        if any(ch * 3 in n for ch in "abcdefghijklmnopqrstuvwxyz"):
            return False
        vowels = sum(1 for ch in n if ch in "aeiouyáéíóúůý")
        return vowels >= 1

    def _score(self, name, samples, rules):
        n = name.lower()
        score = 0
        if 4 <= len(n) <= 10:
            score += 3
        if 11 <= len(n) <= 13:
            score += 1
        common_letters = Counter("".join(samples).lower()) if samples else Counter()
        score += sum(common_letters.get(ch, 0) for ch in set(n)) / 10
        if n[-1] in "aeinorsythx":
            score += 1
        return score
