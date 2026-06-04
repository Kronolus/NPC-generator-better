RACE_PRESETS = {
    "Human": {
        "description": "Přizpůsobiví lidé, vhodní pro každé město.",
        "traits": ["ambiciózní", "rychle se přizpůsobí", "má široké kontakty"],
        "samples": ["Aldric", "Mira", "Jonas", "Helena", "Tomas", "Elena", "Karel", "Seren", "Radan", "Vilem"],
        "templates": ["{first} {last}", "{first} z rodu {last}", "{first} od Staré brány"],
        "rules": {
            "syllables_start": ["Al", "Bel", "Cor", "Dar", "El", "Fer", "Gal", "Har", "Jon", "Kel", "Lor", "Mar", "Nor", "Ser", "Tor"],
            "syllables_mid": ["dri", "wen", "mar", "tha", "lor", "vash", "den", "riel", "ven", "dor", "mir", "gan", "lin", "bar"],
            "syllables_end": ["on", "a", "en", "is", "ar", "or", "us", "eth", "ian", "iel"],
            "forbidden": ["xxx", "qq"],
            "surname_style": "civil",
        },
    },
    "Elf": {
        "description": "Dlouhověcí elfové s vazbou na umění, magii a staré rody.",
        "traits": ["trpělivý", "všímavý", "zná staré příběhy"],
        "samples": ["Faelar", "Aeris", "Lieth", "Shaera", "Vaelis", "Elarion", "Thamior", "Aelar", "Myriil"],
        "templates": ["{first} {last}", "{first} z domu {last}"],
        "rules": {
            "syllables_start": ["Ae", "Fa", "Li", "Sa", "Thae", "Va", "Eli", "Shae", "Myr", "Ael"],
            "syllables_mid": ["lae", "riel", "thil", "nor", "lith", "myr", "vyr", "sil", "drel", "aer"],
            "syllables_end": ["th", "riel", "n", "lin", "ael", "ion", "ir", "wyn"],
            "soft_letters": "aeilyrthmn",
            "surname_style": "poetic",
        },
    },
    "Dwarf": {
        "description": "Trpaslíci spojení s řemeslem, klany, kovem a pamětí rodu.",
        "traits": ["tvrdohlavý", "ctí řemeslo", "pamatuje si staré křivdy"],
        "samples": ["Borin", "Dori", "Thorin", "Kragin", "Bromli", "Durga", "Helja", "Dain", "Kilda"],
        "templates": ["{first} {last}son", "{first} z klanu {last}"],
        "rules": {
            "syllables_start": ["Brom", "Dur", "Gim", "Kil", "Thro", "Balin", "Dain", "Krag", "Grund"],
            "syllables_mid": ["in", "ur", "mir", "gor", "rak", "dun", "bar", "grim"],
            "syllables_end": ["son", "ek", "ar", "orn", "li", "ga"],
            "hard_letters": "kgdrbt",
            "surname_style": "clan",
        },
    },
    "Halfling": {
        "description": "Malí, společenští a často podceňovaní obyvatelé měst.",
        "traits": ["přátelský", "nenápadný", "zná místní drby"],
        "samples": ["Pip", "Milo", "Rosie", "Tilda", "Bram", "Nela", "Fendo", "Lobelia"],
        "templates": ["{first} {last}", "{first} z Malé uličky"],
        "rules": {
            "syllables_start": ["Pi", "Mi", "Ro", "Til", "Bra", "Nel", "Fen", "Lo", "Tob"],
            "syllables_mid": ["li", "bo", "ra", "do", "fi", "mi", "la"],
            "syllables_end": ["p", "lo", "sie", "da", "m", "la", "do", "by"],
            "surname_style": "cozy",
        },
    },
    "Gnome": {
        "description": "Zvědaví vynálezci, iluzionisté, písaři a obchodníci s podivnostmi.",
        "traits": ["zvědavý", "mluví rychle", "sbírá nebezpečné nápady"],
        "samples": ["Fizzik", "Nim", "Talli", "Boddyn", "Zanna", "Pock", "Wizzle", "Nibwick"],
        "templates": ["{first} {last}", "{first} Šroubek"],
        "rules": {
            "syllables_start": ["Fi", "Ni", "Ta", "Bo", "Za", "Po", "Wi", "Nib", "Tik"],
            "syllables_mid": ["zz", "dd", "lli", "wick", "nib", "pock", "bo"],
            "syllables_end": ["ik", "im", "li", "yn", "na", "le", "ock"],
            "surname_style": "craft",
        },
    },
    "Tiefling": {
        "description": "Lidé s pekelným dědictvím, často sledovaní předsudky.",
        "traits": ["odolný vůči pomluvám", "působí výrazně", "má ostrý humor"],
        "samples": ["Zareth", "Nyx", "Akta", "Morthos", "Kallista", "Damakos", "Skarra", "Vex"],
        "templates": ["{first}", "{first} Bezejmenný", "{first} Rudý roh"],
        "rules": {
            "syllables_start": ["Za", "Ny", "Ak", "Mor", "Kal", "Dam", "Skar", "Vex", "Raz"],
            "syllables_mid": ["reth", "x", "ta", "thor", "lis", "mak", "vyr", "zar"],
            "syllables_end": ["eth", "yx", "a", "os", "is", "ra", "ven"],
            "surname_style": "virtue_or_vice",
        },
    },
    "Dragonborn": {
        "description": "Hrdí dračí potomci, často vázaní ctí, řádem a klanem.",
        "traits": ["hrdý", "mluví přímo", "dbá na čest"],
        "samples": ["Arjhan", "Balasar", "Rhogar", "Akra", "Daar", "Kava", "Medrash", "Torinn"],
        "templates": ["{first} z klanu {last}", "{first}"],
        "rules": {
            "syllables_start": ["Ar", "Bal", "Rho", "Ak", "Daar", "Ka", "Med", "Tor", "Sora"],
            "syllables_mid": ["jhan", "las", "gar", "kra", "rash", "rax", "thar"],
            "syllables_end": ["an", "ar", "ra", "ash", "inn", "ax"],
            "surname_style": "clan",
        },
    },
    "Half-Orc": {
        "description": "Silní a často nepochopení lidé na pomezí dvou světů.",
        "traits": ["přímý", "chrání své lidi", "nerad ztrácí čas"],
        "samples": ["Gorruk", "Morga", "Thava", "Keth", "Ugra", "Brog", "Grash"],
        "templates": ["{first}", "{first} Železná pěst"],
        "rules": {
            "syllables_start": ["Gor", "Mor", "Tha", "Ket", "Ug", "Brog", "Gra", "Dur"],
            "syllables_mid": ["ruk", "ga", "va", "th", "gra", "mog", "bur"],
            "syllables_end": ["uk", "a", "eth", "og", "ash", "ar"],
            "surname_style": "brutal",
        },
    },
    "Goblin": {
        "description": "Rychlí přeživší, kšeftaři, šmelináři a malí géniové chaosu.",
        "traits": ["rychlý", "podezřívavý", "umí sehnat skoro cokoliv"],
        "samples": ["Snik", "Grib", "Nakka", "Pox", "Vrik", "Tiz", "Zub", "Krek"],
        "templates": ["{first}", "{first} Kapsář"],
        "rules": {
            "syllables_start": ["Sn", "Gr", "Nak", "Pox", "Vr", "Tiz", "Zub", "Krek"],
            "syllables_mid": ["i", "ak", "ox", "ri", "iz", "ub", "ek"],
            "syllables_end": ["ik", "ib", "ka", "x", "k", "z", "ub"],
            "surname_style": "street",
        },
    },
}

CITY_PRESETS = [
    {"name": "Lothmar", "region": "Centrální království", "atmosphere": "rušné obchodní město", "danger_level": "střední", "notes": "Tržiště, chrám, archiv a stará kanalizace.", "demographics": [{"race": "Human", "weight": 60}, {"race": "Elf", "weight": 15}, {"race": "Dwarf", "weight": 10}, {"race": "Halfling", "weight": 10}, {"race": "Tiefling", "weight": 5}]},
    {"name": "Kamenobrod", "region": "Horské údolí", "atmosphere": "těžební město", "danger_level": "vysoká", "notes": "Doly, klany, staré štoly a nelegální tavírny.", "demographics": [{"race": "Dwarf", "weight": 45}, {"race": "Human", "weight": 30}, {"race": "Gnome", "weight": 10}, {"race": "Half-Orc", "weight": 10}, {"race": "Goblin", "weight": 5}]},
    {"name": "Mlžný Přístav", "region": "Pobřeží", "atmosphere": "špinavé přístavní město", "danger_level": "vysoká", "notes": "Pašeráci, rybáři, tajné kulty a ztracené lodě.", "demographics": [{"race": "Human", "weight": 45}, {"race": "Goblin", "weight": 15}, {"race": "Tiefling", "weight": 15}, {"race": "Half-Orc", "weight": 15}, {"race": "Dragonborn", "weight": 10}]},
]

PROFESSIONS = ["alchymista", "archivář", "barman", "bard", "bylinkář", "cechmistr", "dráteník", "důstojník stráže", "hostinský", "kartograf", "kovář", "klenotník", "kněz", "krysař", "léčitel", "lodník", "lovec odměn", "mág", "městský písař", "obchodník", "pašerák", "pekař", "pohřebník", "pouliční věštec", "právník", "průvodce", "řezník", "špeh", "tiskař", "učedník", "učenec", "žebrák", "zloděj"]
ROLES = ["spojenec", "informátor", "obchodník", "podezřelý", "rival", "zadavatel questu", "oběť problému", "komická postava", "skrytý padouch", "neutrální svědek"]
GENDERS = ["muž", "žena", "nebinární", "neznámé / tajené"]
SOCIAL_CLASSES = ["chudina", "pracující třída", "cechovní střed", "nižší šlechta", "bohatý měšťan", "vyvrženec", "cizinec bez práv"]
ALIGNMENTS = ["zákonné dobro", "neutrální dobro", "chaotické dobro", "zákonně neutrální", "pravý neutrál", "chaoticky neutrální", "zákonné zlo", "neutrální zlo", "chaotické zlo"]
PERSONALITIES = ["mluví klidně, ale nikdy neřekne všechno", "je hlučný, přímý a snadno se urazí", "působí přátelsky, ale neustále něco počítá", "má suchý humor a testuje trpělivost ostatních", "vypadá unaveně a chová se jako člověk, který toho ví moc", "je přehnaně zdvořilý, hlavně když lže", "s každým jedná jako s potenciálním zákazníkem", "nenávidí autority, ale bojí se otevřeného konfliktu", "je tichý, všímavý a pamatuje si detaily"]
MOTIVATIONS = ["chce splatit dluh, než si pro něj někdo přijde", "hledá ztraceného člena rodiny", "potřebuje ochránit svůj obchod", "chce získat místo v cechu", "chce se pomstít někomu z městské rady", "touží odejít z města, ale nemá jak", "chce dokázat, že není zbabělec", "snaží se skrýt minulost", "chce najít magický předmět, o kterém všichni tvrdí, že neexistuje"]
SECRETS = ["tajně pracuje pro konkurenční cech", "viděl vraždu, ale bojí se mluvit", "má doma zakázaný artefakt", "není tím, za koho se vydává", "dluží peníze nebezpečným lidem", "kdysi sloužil kultu, který se vrací do města", "zná tajný vstup do podzemí", "falšuje dokumenty pro šlechtu", "chrání monstrum, protože mu kdysi zachránilo život"]
FEARS = ["veřejné zostuzení", "oheň", "hluboká voda", "stráže", "magie mysli", "ztráta rodiny", "chudoba", "otevřené násilí", "staré doly", "šlechta"]
FLAWS = ["mluví dřív, než přemýšlí", "prodá informaci každému, kdo zaplatí", "nedokáže přiznat chybu", "pije, když je pod tlakem", "má slabost pro hazard", "nechá se snadno zastrašit", "věří špatným lidem", "všechno řeší podvodem"]
RUMORS = ["říká se, že po nocích mizí v kanalizaci", "někdo tvrdí, že mluví s mrtvými", "prý má mapu k zakázané části města", "lidé ho podezírají z pašování", "v poslední době se kolem něj pohybují cizí poslové", "někdo ho viděl hádat se s kapitánem stráže", "má prý klíč od staré městské brány"]
QUEST_HOOKS = ["požádá družinu, aby doručila balík bez otázek", "nabídne informace výměnou za ochranu", "prosí o nalezení zmizelé osoby", "chce, aby družina sledovala podezřelého šlechtice", "prodá mapu, která může být pravá nebo falešná", "potřebuje získat důkaz proti cechu", "varuje družinu před někým, kdo se tváří jako spojenec", "nabídne práci v podzemí města"]
USEFUL_INFO = ["ví, kdo uplácí stráže", "zná nejrychlejší cestu přes město", "umí rozpoznat padělané listiny", "má kontakt na léčitele", "ví o tajném skladu", "zná slabinu místního gangu", "má přístup do městského archivu", "slyšel jméno skutečného viníka"]
COMBAT_ROLES = ["nebojovník", "slabý civilista", "pouliční rváč", "strážný", "veterán", "akolyt", "mág učedník", "lovec", "zabiják", "boss nižší úrovně"]
STAT_HINTS = ["Použij statblok Commoner.", "Použij statblok Guard.", "Použij statblok Bandit.", "Použij statblok Scout.", "Použij statblok Cultist.", "Použij statblok Noble.", "Použij statblok Veteran, ale s nižším HP.", "Použij jednoduchý domácí statblok podle role."]
INVENTORY = ["svazek klíčů, špinavý kapesník, 2 stříbrné", "malý nůž, falešná pečeť, vosk", "deník, inkoust, mapa jedné čtvrti", "amulet bez magie, stará mince, prsten", "léčivá mast, jehla, nit, bylinky", "hrací kostky, dluhopis, rozbitý kompas", "lahvička podezřelé tekutiny, křída, provázek", "dopis bez podpisu, pečeť cechu, 5 zlatých"]
VOICES = ["mluví hlubokým hlasem a dělá dlouhé pauzy", "mluví rychle a polyká konce vět", "šeptá, i když nemusí", "má drsný hlas po kouři", "působí vzdělaně a používá přesná slova", "často používá špatná přísloví", "mluví jako někdo, kdo nechce být slyšen"]
APPEARANCE = {"build": ["hubená postava", "štíhlá a šlachovitá postava", "svalnatá postava", "statná postava", "drobná postava"], "height": ["velmi nízký", "spíše nízký", "průměrné výšky", "vyšší než průměr", "nápadně vysoký"], "hair": ["krátké vlasy", "dlouhé rozpuštěné vlasy", "pletené copy", "vyholená hlava", "vlnité vlasy po ramena", "neupravené vlasy"], "hair_color": ["černé", "hnědé", "blond", "ryšavé", "šedivé", "bílé", "tmavě zelené barvené"], "eyes": ["jasně modré oči", "tmavě hnědé oči", "zelené oči", "šedé oči", "jedno oko zakalené", "oči se zlatým odleskem"], "clothing": ["opotřebovaný plášť", "vyšívaný kabát", "tmavý kabát s kapucí", "koženou zástěru", "drahé šaty", "uniformu bez odznaku", "špinavé pracovní oblečení"], "mark": ["jizva přes tvář", "tetování runy", "chybějící prst", "popálenina na krku", "rodová pečeť na prstenu", "zlomený nos", "kovová náušnice"]}
