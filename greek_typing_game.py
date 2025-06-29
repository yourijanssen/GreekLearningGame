import random
import unicodedata
from player_stats import load_player_stats, save_player_stats, update_mode_stats
import time
import sys

# Terminal color codes (optional, works in many terminals)
def color(text, code):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

def green(text): return color(text, '92')
def red(text):   return color(text, '91')
def yellow(text): return color(text, '93')
def blue(text): return color(text, '94')
def magenta(text): return color(text, '95')
def bold(text):  return color(text, '1')

# Fun message function for big streaks
def congrats_streak(streak):
    if streak >= 20: 
        print(bold(green(f"🌟 WOW! {streak} answers in a row! You're a legend! 🌟\n")))
    elif streak >= 10: 
        print(yellow(f"🔥 {streak} correct in a row! Keep going! 🔥\n"))
    elif streak >= 5: 
        print(blue(f"👏 {streak} correct answers streak! 👏\n"))

greek_letters = [
    ('α', 'alpha / άλφα (alfa)'),
    ('Α', 'ALPHA / ΆΛΦΑ (ALFA)'),
    ('β', 'beta / βήτα (vita)'),
    ('Β', 'BETA / ΒΉΤΑ (VITA)'),
    ('γ', 'gamma / γάμα (gama)'),
    ('Γ', 'GAMMA / ΓΆΜΑ (GAMA)'),
    ('δ', 'delta / δέλτα (delta)'),
    ('Δ', 'DELTA / ΔΈΛΤΑ (DELTA)'),
    ('ε', 'epsilon / έψιλον (epsilon)'),
    ('Ε', 'EPSILON / ΈΨΙΛΟΝ (EPSILON)'),
    ('ζ', 'zeta / ζήτα (zita)'),
    ('Ζ', 'ZETA / ΖΉΤΑ (ZITA)'),
    ('η', 'eta / ήτα (ita)'),
    ('Η', 'ETA / ΉΤΑ (ITA)'),
    ('θ', 'theta / θήτα (thita)'),
    ('Θ', 'THETA / ΘΉΤΑ (THITA)'),
    ('ι', 'iota / γιώτα (giota)'),
    ('Ι', 'IOTA / ΓΙΏΤΑ (GIOTA)'),
    ('κ', 'kappa / κάππα (kapa)'),
    ('Κ', 'KAPPA / ΚΆΠΠΑ (KAPA)'),
    ('λ', 'lambda / λάμδα (lamda)'),
    ('Λ', 'LAMBDA / ΛΆΜΔΑ (LAMDA)'),
    ('μ', 'mu / μι (mi)'),
    ('Μ', 'MU / ΜΙ (MI)'),
    ('ν', 'nu / νι (ni)'),
    ('Ν', 'NU / ΝΙ (NI)'),
    ('ξ', 'xi / ξι (ksi)'),
    ('Ξ', 'XI / ΞΙ (KSI)'),
    ('ο', 'omicron / όμικρον (omikron)'),
    ('Ο', 'OMICRON / ΌΜΙΚΡΟΝ (OMIKRON)'),
    ('π', 'pi / πι (pi)'),
    ('Π', 'PI / ΠΙ (PI)'),
    ('ρ', 'rho / ρο (ro)'),
    ('Ρ', 'RHO / ΡΟ (RO)'),
    ('σ', 'sigma / σίγμα (sigma)'),
    ('ς', 'final sigma / τελικό σίγμα (teliko sigma)'),
    ('Σ', 'SIGMA / ΣΊΓΜΑ (SIGMA)'),
    ('τ', 'tau / ταυ (taf)'),
    ('Τ', 'TAU / ΤΑΥ (TAF)'),
    ('υ', 'upsilon / ύψιλον (ipsilon)'),
    ('Υ', 'UPSILON / ΎΨΙΛΟΝ (IPSILON)'),
    ('φ', 'phi / φι (fi)'),
    ('Φ', 'PHI / ΦΙ (FI)'),
    ('χ', 'chi / χι (hi)'),
    ('Χ', 'CHI / ΧΙ (HI)'),
    ('ψ', 'psi / ψι (psi)'),
    ('Ψ', 'PSI / ΨΙ (PSI)'),
    ('ω', 'omega / ωμέγα (omega)'),
    ('Ω', 'OMEGA / ΩΜΈΓΑ (OMEGA)'),
]

greek_combinations = [
    ('αι', 'ai / αι (sounds like "e" in "let"), παιδί (child), και (and)'),
    ('ει', 'ei / ει (sounds like "ee" in "see"), είναι (is), σπίτι (house)'),
    ('οι', 'oi / οι (sounds like "ee" in "see"), οικογένεια (family), όλοι (everyone)'),
    ('υι', 'yi / υι (sounds like "ee" in "see", rare), υιός (son)'),
    ('αυ', 'au / αυ (sounds like "av" before vowels/voiced, "af" before unvoiced), αυγό (egg), αυτός (this), αύριο (tomorrow)'),
    ('ευ', 'eu / ευ (sounds like "ev" before vowels/voiced, "ef" before unvoiced), ευχαριστώ (thank you), ευρώ (euro), εύκολο (easy)'),
    ('ου', 'ou / ου (sounds like "oo" in "food"), ούτε (neither), που (that/who), ουρανός (sky)'),
    ('μπ', 'mp / μπ (b at start, mb in middle), μπάλα (ball), λάμπα (lamp)'),
    ('ντ', 'nt / ντ (d at start, nd in middle), ντομάτα (tomato), πάντα (always)'),
    ('γκ', 'gk / γκ (g as in "get"), γκολ (goal), αγκίστρι (hook)'),
    ('γγ', 'ng / γγ (ng in "song"), αγγίζω (I touch), άγγελος (angel)'),
    ('γχ', 'nch / γχ (as in "anchor"), άγχος (anxiety)'),
    ('τζ', 'tz / τζ (as in "tzatziki"), τζάμι (window pane), τζάκι (fireplace)'),
    ('ια', 'ia / ια (as in "ya"), ιάπωνας (Japanese), γιαγιά (grandmother)'),
    ('ιο', 'io / ιο (as in "yo"), βιόλα (viola), βιολί (violin)'),
('ιε', 'ie / ιε (as in "ye"), ιερέας (priest), ιερός (sacred), ιεραρχία (hierarchy)')
]

greek_words = [
    ('μάνα', 'mother'),
    ('νερό', 'water'),
    ('ψωμί', 'bread'),
    ('σπίτι', 'house'),
    ('φίλος', 'friend'),
    ('βιβλίο', 'book'),
    ('δέντρο', 'tree'),
    ('αυτοκίνητο', 'car'),
    ('παιδί', 'child'),
    ('ήλιος', 'sun'),
    ('θήκη', 'case'),
    ('δάσκαλος', 'teacher (male)'),
    ('δασκάλα', 'teacher (female)'),
    ('σκύλος', 'dog'),
    ('γάτα', 'cat'),
    ('καφές', 'coffee'),
    ('μήλο', 'apple'),
    ('τραπέζι', 'table'),
    ('καρέκλα', 'chair'),
    ('γλώσσα', 'language/tongue'),
    ('πόρτα', 'door'),
    ('αγόρι', 'boy'),
    ('κορίτσι', 'girl'),
    ('ψάρι', 'fish'),
    ('κουζίνα', 'kitchen'),
    ('παράθυρο', 'window'),
    ('βουνό', 'mountain'),
    ('θάλασσα', 'sea'),
    ('μένω', 'I live'),
    ('θέλω', 'I want'),
    ('έχω', 'I have'),
    ('είμαι', 'I am'),
    ('τρέχω', 'I run'),
    ('διαβάζω', 'I read'),
    ('γράφω', 'I write'),
    ('λέω', 'I say'),
    ('βλέπω', 'I see'),
    ('ακούω', 'I hear'),
    ('ωραίος', 'beautiful/handsome (male)'),
    ('ωραία', 'beautiful (female/neutral)'),
    ('μεγάλος', 'big/large'),
    ('μικρός', 'small/little'),
    ('καλός', 'good'),
       ('αγάπη', 'love'),
    ('φιλιά', 'kisses'),
    ('αγκαλιά', 'hug'),
    ('αγόρι μου', 'my boyfriend'),
    ('κορίτσι μου', 'my girl / my girlfriend'),
    ('καρδιά', 'heart'),
    ('σχέση', 'relationship'),
    ('σε σκέφτομαι', 'I think of you'),
    ('μου λείπεις', 'I miss you'),
    ('σ\' αγαπώ', 'I love you'),
    ('πάμε βόλτα', 'let\'s go for a walk'),
    ('σπίτι σου', 'your house'),
    ('σπίτι μου', 'my house'),
    ('ταινία', 'movie'),
    ('βγαίνουμε έξω', 'we go out'),
    ('μαζί', 'together'),
    ('χέρι', 'hand'),
    ('πάρκο', 'park'),
    ('παραλία', 'beach'),
    ('εστιατόριο', 'restaurant'),
    ('δείπνο', 'dinner'),
    ('πρωινό', 'breakfast'),
    ('καφές μαζί', 'coffee together'),
    ('ταξίδι', 'trip or travel'),
    ('δώρο', 'gift'),
    ('έκπληξη', 'surprise'),
    ('γέλιο', 'laughter'),
    ('αστέρι μου', 'my star'),
    ('ζωή μου', 'my life'),
    ('καλή νύχτα', 'good night'),
    ('όνειρα γλυκά', 'sweet dreams'),
    ('χαρά', 'joy'),
    ('φιλί', 'kiss'),
    ('φλερτ', 'flirt'),
    ('ευτυχία', 'happiness'),
    ('πικ νικ', 'picnic'),
    ('βόλτα', 'walk, outing'),
    ('τραγούδι', 'song'),
    ('χορός', 'dance'),
    ('εκδρομή', 'excursion, trip'),
    ('κουβέντα', 'chat / talk')
]

greek_numbers = [
    ('1', 'ένα'),
    ('2', 'δύο'),
    ('3', 'τρία'),
    ('4', 'τέσσερα'),
    ('5', 'πέντε'),
    ('6', 'έξι'),
    ('7', 'επτά'),
    ('8', 'οκτώ'),
    ('9', 'εννιά'),
    ('10', 'δέκα'),
    ('11', 'έντεκα'),
    ('12', 'δώδεκα'),
    ('13', 'δεκατρία'),
    ('14', 'δεκατέσσερα'),
    ('15', 'δεκαπέντε'),
    ('16', 'δεκαέξι'),
    ('17', 'δεκαεπτά'),
    ('18', 'δεκαοκτώ'),
    ('19', 'δεκαεννιά'),
    ('20', 'είκοσι'),
    ('21', 'είκοσι ένα'),
    ('22', 'είκοσι δύο'),
    ('23', 'είκοσι τρία'),
    ('24', 'είκοσι τέσσερα'),
    ('25', 'είκοσι πέντε'),
    ('26', 'είκοσι έξι'),
    ('27', 'είκοσι επτά'),
    ('28', 'είκοσι οκτώ'),
    ('29', 'είκοσι εννιά'),
    ('30', 'τριάντα'),
    ('31', 'τριάντα ένα'),
    ('32', 'τριάντα δύο'),
    ('33', 'τριάντα τρία'),
    ('34', 'τριάντα τέσσερα'),
    ('35', 'τριάντα πέντε'),
    ('36', 'τριάντα έξι'),
    ('37', 'τριάντα επτά'),
    ('38', 'τριάντα οκτώ'),
    ('39', 'τριάντα εννιά'),
    ('40', 'σαράντα'),
    ('41', 'σαράντα ένα'),
    ('42', 'σαράντα δύο'),
    ('43', 'σαράντα τρία'),
    ('44', 'σαράντα τέσσερα'),
    ('45', 'σαράντα πέντε'),
    ('46', 'σαράντα έξι'),
    ('47', 'σαράντα επτά'),
    ('48', 'σαράντα οκτώ'),
    ('49', 'σαράντα εννιά'),
    ('50', 'πενήντα'),
    ('51', 'πενήντα ένα'),
    ('52', 'πενήντα δύο'),
    ('53', 'πενήντα τρία'),
    ('54', 'πενήντα τέσσερα'),
    ('55', 'πενήντα πέντε'),
    ('56', 'πενήντα έξι'),
    ('57', 'πενήντα επτά'),
    ('58', 'πενήντα οκτώ'),
    ('59', 'πενήντα εννιά'),
    ('60', 'εξήντα'),
    ('61', 'εξήντα ένα'),
    ('62', 'εξήντα δύο'),
    ('63', 'εξήντα τρία'),
    ('64', 'εξήντα τέσσερα'),
    ('65', 'εξήντα πέντε'),
    ('66', 'εξήντα έξι'),
    ('67', 'εξήντα επτά'),
    ('68', 'εξήντα οκτώ'),
    ('69', 'εξήντα εννιά'),
    ('70', 'εβδομήντα'),
    ('71', 'εβδομήντα ένα'),
    ('72', 'εβδομήντα δύο'),
    ('73', 'εβδομήντα τρία'),
    ('74', 'εβδομήντα τέσσερα'),
    ('75', 'εβδομήντα πέντε'),
    ('76', 'εβδομήντα έξι'),
    ('77', 'εβδομήντα επτά'),
    ('78', 'εβδομήντα οκτώ'),
    ('79', 'εβδομήντα εννιά'),
    ('80', 'ογδόντα'),
    ('81', 'ογδόντα ένα'),
    ('82', 'ογδόντα δύο'),
    ('83', 'ογδόντα τρία'),
    ('84', 'ογδόντα τέσσερα'),
    ('85', 'ογδόντα πέντε'),
    ('86', 'ογδόντα έξι'),
    ('87', 'ογδόντα επτά'),
    ('88', 'ογδόντα οκτώ'),
    ('89', 'ογδόντα εννιά'),
    ('90', 'ενενήντα'),
    ('91', 'ενενήντα ένα'),
    ('92', 'ενενήντα δύο'),
    ('93', 'ενενήντα τρία'),
    ('94', 'ενενήντα τέσσερα'),
    ('95', 'ενενήντα πέντε'),
    ('96', 'ενενήντα έξι'),
    ('97', 'ενενήντα επτά'),
    ('98', 'ενενήντα οκτώ'),
    ('99', 'ενενήντα εννιά'),
    ('100', 'εκατό')
]

greek_sentences = [
    ('Το παιδί τρέχει.', 'The child is running.'),
    ('Η γάτα κοιμάται.', 'The cat is sleeping.'),
    ('Ο πατέρας διαβάζει.', 'The father is reading.'),
    ('Είμαι στο σπίτι.', 'I am at home.'),
    ('Η μητέρα τρώει ψωμί.', 'The mother is eating bread.'),
    ('Το κορίτσι πίνει νερό.', 'The girl is drinking water.'),
    ('Ο φίλος μου είναι καλός.', 'My friend is good.'),
    ('Η θάλασσα είναι μεγάλη.', 'The sea is big.'),
    ('Το βιβλίο είναι πάνω στο τραπέζι.', 'The book is on the table.'),
    ('Έχω μια ωραία ιδέα.', 'I have a nice idea.'),
    ('Η πόρτα είναι ανοιχτή.', 'The door is open.'),
    ('Το αγόρι γράφει ένα γράμμα.', 'The boy is writing a letter.'),
    ('Ο ήλιος λάμπει.', 'The sun is shining.'),
    ('Η καρέκλα είναι δίπλα στο παράθυρο.', 'The chair is next to the window.'),
    ('Η δασκάλα μιλάει στην τάξη.', 'The teacher is speaking in the class.'),
    ('Το σκυλί παίζει στον κήπο.', 'The dog is playing in the yard.'),
    ('Το βουνό είναι ψηλό.', 'The mountain is tall.'),
    ('Θέλω να διαβάσω.', 'I want to read.'),
    ('Το παιδί έχει ένα μήλο.', 'The child has an apple.'),
    ('Ο καιρός είναι όμορφος σήμερα.', 'The weather is beautiful today.'),
        ('Το σχολείο είναι κλειστό.', 'The school is closed.'),
    ('Η μαμά μαγειρεύει στην κουζίνα.', 'Mom is cooking in the kitchen.'),
    ('Το τρένο φτάνει στον σταθμό.', 'The train arrives at the station.'),
    ('Το ποδήλατο είναι καινούριο.', 'The bicycle is new.'),
    ('Ο παππούς πίνει καφέ.', 'Grandpa is drinking coffee.'),
    ('Η θεια διαβάζει εφημερίδα.', 'Aunt is reading a newspaper.'),
    ('Τα παιδιά ζωγραφίζουν έναν ήλιο.', 'The children draw a sun.'),
    ('Το ψάρι κολυμπάει στη θάλασσα.', 'The fish swims in the sea.'),
    ('Ο μαθητής γράφει στο τετράδιο.', 'The student writes in the notebook.'),
    ('Το παράθυρο είναι ανοιχτό.', 'The window is open.'),
    ('Η μηχανή είναι γρήγορη.', 'The motorcycle is fast.'),
    ('Το δωμάτιο είναι καθαρό.', 'The room is clean.'),
    ('Η γέφυρα είναι μεγάλη.', 'The bridge is big.'),
    ('Το φως είναι δυνατό.', 'The light is strong.'),
    ('Η μέρα είναι ζεστή.', 'The day is warm.'),
    ('Ο δάσκαλος φοράει γυαλιά.', 'The teacher wears glasses.'),
    ('Η τσάντα είναι βαριά.', 'The bag is heavy.'),
    ('Το μολύβι είναι κόκκινο.', 'The pencil is red.'),
    ('Η φίλη μου μένει εδώ.', 'My (female) friend lives here.'),
    ('Το λεωφορείο έρχεται.', 'The bus is coming.'),
      ('Η βροχή πέφτει δυνατά.', 'The rain is falling hard.'),
    ('Ο άνθρωπος περπατά στο πάρκο.', 'The man walks in the park.'),
    ('Η γιαγιά πλέκει ένα πουλόβερ.', 'Grandma is knitting a sweater.'),
    ('Το φρούτο είναι γλυκό.', 'The fruit is sweet.'),
    ('Η τηλεόραση είναι σβηστή.', 'The television is off.'),
    ('Το αυτοκίνητο είναι μπλε.', 'The car is blue.'),
    ('Το δέντρο έχει πράσινα φύλλα.', 'The tree has green leaves.'),
    ('Το τηλέφωνο χτυπάει.', 'The phone is ringing.'),
    ('Το παιδί γελάει.', 'The child is laughing.'),
    ('Η μητέρα αγοράζει ψωμί.', 'The mother buys bread.'),
    ('Το ποτήρι είναι γεμάτο νερό.', 'The glass is full of water.'),
    ('Το παιδί διαβάζει ένα βιβλίο.', 'The child reads a book.'),
    ('Το πουλί τραγουδάει στο κλαδί.', 'The bird sings on the branch.'),
    ('Η ώρα είναι επτά.', 'It is seven o’clock.'),
    ('Το λουλούδι είναι όμορφο.', 'The flower is beautiful.'),
    ('Ο πατέρας οδηγεί το αυτοκίνητο.', 'The father drives the car.'),
    ('Το ψωμί είναι στο τραπέζι.', 'The bread is on the table.'),
    ('Η αλεπού τρέχει στο δάσος.', 'The fox runs in the forest.'),
    ('Το παιδί μαθαίνει ελληνικά.', 'The child learns Greek.'),
    ('Ο γιατρός εργάζεται στο νοσοκομείο.', 'The doctor works at the hospital.')
]

greek_fill_blanks = [
    ("Εγώ _______ (τρέχω) στο πάρκο κάθε μέρα.", "τρέχω", "I run"),
    ("Η Μαρία _______ (τρώω) ψωμί.", "τρώει", "Maria eats bread"),
    ("Εμείς _______ (γράφω) μία επιστολή.", "γράφουμε", "We write a letter"),
    ("Αύριο _______ (είμαι) Παρασκευή.", "είναι", "Tomorrow is Friday"),
    ("Ο Νίκος _______ (παίζω) ποδόσφαιρο.", "παίζει", "Nikos plays soccer"),
    ("Η δασκάλα _______ (μιλάω) στην τάξη.", "μιλάει", "The teacher speaks in class"),
    ("Εσύ _______ (έχω) σκύλο;", "έχεις", "Do you have a dog?"),
    ("Το παιδί _______ (ζωγραφίζω) έναν ήλιο.", "ζωγραφίζει", "The child draws a sun"),
    ("Εσείς _______ (διαβάζω) βιβλία;", "διαβάζετε", "Do you (plural) read books?"),
    ("Το αυτοκίνητο _______ (είμαι) μπλε.", "είναι", "The car is blue"),
]

stats = load_player_stats()
game_start_time = time.time()

def play_letters():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_letters)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    # Start timing!
    start_time = time.time()

    while items:
        letter, name = items[0]
        ans = input(f"Type this Greek letter: {strip_greek_accents(letter)} ({name}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(letter):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == letter:
                print(green(f"✅ Correct! (with accents) Streak: {streak}  | Progress: {correct_count}/{len(greek_letters)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {letter}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_letters)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct letter was: {letter} ({name})."))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        # Only runs if loop is not exited early (all items completed)
        total_time = time.time() - start_time  # in seconds
        minutes = int(total_time // 60)
        seconds = total_time % 60
        print(green("🎉 Congratulations! You typed all Greek letters correctly in this round! 🎉\n"))
        print(yellow(f"⏱️ You completed {len(greek_letters)} letters in {minutes} min {seconds:.2f} sec."))

        # Store/check/update record in stats!
        # Prepare key for time records
        if "fastest_times" not in stats:
            stats["fastest_times"] = {}
        prev_best = stats["fastest_times"].get("letters")

        # If first run or new record, update and celebrate
        if (prev_best is None) or (total_time < prev_best):
            stats["fastest_times"]["letters"] = total_time
            print(green("\n🎊 NEW RECORD! You set your fastest letters time! 🎊"))
            print(yellow(f" 🏁 New record: {minutes} min {seconds:.2f} sec\n"))
        else:
            # Show all-time best as well
            pmin = int(prev_best // 60)
            psec = prev_best % 60
            print(cyan(f"Your best all-time is {pmin} min {psec:.2f} sec."))

    update_mode_stats(stats, "letters", correct_count, best_streak)

def strip_greek_accents(s):
    # Removes Greek accents/diacritics/tremas
    return ''.join(
        c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)
    )

def play_words():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_words)
    random.shuffle(items)
    streak = 0
    correct_count = 0
    best_streak = 0
    quit_early = False  # Track manual exit

    while items:
        word, meaning = items[0]
        ans = input(f"Type this Greek word: {strip_greek_accents(word)} (means: {meaning}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(word):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == word:
                print(green(f"✅ Correct! (with proper accents) Streak: {streak}  | Progress: {correct_count}/{len(greek_words)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {word}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_words)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct word was: {word}."))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all Greek words correctly in this round! 🎉\n"))

    update_mode_stats(stats, "words", correct_count, best_streak)

def play_sentences():
    print("Type 'm' to return to the main menu.\n")
    print("Choose mode:")
    print("1) Type the Greek for the given English meaning 🎯")
    print("2) Type the English for the given Greek sentence 🚀")
    print("3) Copy the Greek sentence to practice typing (copy mode) ✍️")
    mode = input("Your choice (1, 2 or 3): ").strip()
    items = list(greek_sentences)
    random.shuffle(items)
    streak = correct_count = best_streak = 0

    while items:
        sentence, translation = items[0]

        if mode == '1':  # English to Greek
            print(f"\nEnglish meaning: {yellow(translation)}")
            ans = input("Type the Greek sentence (no accents required):\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if strip_greek_accents(ans) == strip_greek_accents(sentence):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == sentence:
                    print(green("✅ Correct! (with accents)"))
                else:
                    print(yellow(f"✅ Correct (no accents). Full sentence with accents is:\n  {sentence}"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. Correct Greek sentence was:\n  {sentence}"))
                print(yellow(f"English meaning: {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        elif mode == '2':  # Greek to English
            print(f"\nGreek sentence: {yellow(sentence)}")
            print(f"English meaning: {yellow(translation)}")  # Always show, as requested
            ans = input("Type the English translation:\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if ans.strip().lower() == translation.strip().lower():
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                print(green("✅ Correct!"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. The correct English was:\n  {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        elif mode == '3':  # Copy/Typing practice
            print(f"\nPractice typing this Greek sentence:")
            print(f"{yellow(sentence)}")
            print(f"English meaning: {yellow(translation)}")
            ans = input("Type the Greek sentence (no accents required):\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if strip_greek_accents(ans) == strip_greek_accents(sentence):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == sentence:
                    print(green("✅ Correct! (with accents)"))
                else:
                    print(yellow(f"✅ Correct (no accents). Proper spelling is:\n  {sentence}"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. Correct Greek sentence was:\n  {sentence}"))
                print(yellow(f"English meaning: {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        else:
            print(red("Invalid mode choice. Please restart this section.\n"))
            break
    else:
        print(green("🎉 Congratulations! You completed all Greek sentences this round! 🎉\n"))
    update_mode_stats(stats, "sentences", correct_count, best_streak)

def play_combinations():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_combinations)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    while items:
        combo, sound = items[0]
        ans = input(f"Type this Greek combination: {strip_greek_accents(combo)} (pronounced: {sound}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(combo):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == combo:
                print(green(f"✅ Correct! (with accents) Streak: {streak} | Progress: {correct_count}/{len(greek_combinations)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {combo}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_combinations)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct combination was: {combo}"))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all Greek combinations correctly in this round! 🎉\n"))
    update_mode_stats(stats, "combinations", correct_count, best_streak)

def play_numbers():
    print("Type 'm' to return to the main menu.\n")
    print("Choose practice range:")
    print("1) Numbers 1-10")
    print("2) Numbers 1-100")
    choice = input("Your choice (1 or 2): ").strip()
    if choice == '1':
        number_range = set(str(i) for i in range(1, 11))
        items = [x for x in greek_numbers if x[0] in number_range]
    elif choice == '2':
        items = list(greek_numbers)
    else:
        print(red("Invalid selection. Returning to menu.\n"))
        return

    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False
    total = len(items)   # <<< Store the starting total for progress display

    while items:
        number, greek = items[0]
        if random.choice([True, False]):
            ans = input(f"How do you write {yellow(number)} in Greek? ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                quit_early = True
                break
            elif strip_greek_accents(ans) == strip_greek_accents(greek):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == greek:
                    print(green(f"✅ Correct! (with accents) {number} is '{greek}'. Streak: {streak}"))
                else:
                    print(yellow(f"✅ Correct (without accents)! The proper spelling is: '{greek}'"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{total}\n"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. {number} in Greek is: '{greek}'"))
                print(red(f"Your streak was: {streak}"))
                streak = 0
                random.shuffle(items)
        else:
            ans = input(f"Which number is '{yellow(strip_greek_accents(greek))}'? ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                quit_early = True
                break
            elif ans == number:
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                print(green(f"✅ Correct! '{greek}' is {number}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{total}\n"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. '{greek}' is: {number}"))
                print(red(f"Your streak was: {streak}"))
                streak = 0
                random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all selected Greek numbers correctly in this round! 🎉\n"))
    update_mode_stats(stats, "numbers", correct_count, best_streak)

def play_fill_blanks():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_fill_blanks)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    while items:
        sentence, correct, hint = items[0]
        ans = input(f"Fill in the blank: {sentence}\nHint: {hint}\n> ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(correct):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == correct:
                print(green("✅ Correct!"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {correct}"))
            print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_fill_blanks)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct answer is: {correct}"))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You solved all fill-in-the-blank questions!\n"))
    update_mode_stats(stats, "fill_blanks", correct_count, best_streak)

def show_stats(stats):
    import datetime

    # Color helpers (same as elsewhere)
    def green(t):   return f"\033[92m{t}\033[0m"
    def cyan(t):    return f"\033[96m{t}\033[0m"
    def magenta(t): return f"\033[95m{t}\033[0m"
    def yellow(t):  return f"\033[93m{t}\033[0m"
    def bold(t):    return f"\033[1m{t}\033[0m"

    def minutes_seconds(secs):
        mins = int(secs) // 60
        s = int(secs) % 60
        return f"{mins} min {s} sec"

    print(bold(magenta("\n🏆 === Your Greek Learning Stats === 🏆")))
    print(f"⏱️  Total play time: {yellow(minutes_seconds(stats.get('playtime_seconds',0)))}")

    games_played = stats.get('games_played', {})
    correct_answers = stats.get('correct_answers', {})
    best_streak = stats.get('best_streak', {})
    modes = set(games_played) | set(correct_answers) | set(best_streak)

    fastest = stats.get("fastest_times", {})
    if "letters" in fastest:
        mins = int(fastest["letters"] // 60)
        secs = fastest["letters"] % 60
        print(yellow(f"🏁 Fastest time for all letters: {mins} min {secs:.2f} sec"))

    if not modes:
        print(cyan("(No games played yet!)"))
    else:
        # Fancy table output per mode
        for mode in sorted(modes):
            print(bold(f"\n📚 {mode.capitalize()}"))
            print(f"   🎮 Games played:  {green(games_played.get(mode, 0))}")
            print(f"   ✅ Correct:       {cyan(correct_answers.get(mode, 0))}")
            print(f"   🔥 Best streak:   {yellow(best_streak.get(mode, 0))}")

    lp = stats.get('last_played', None)
    if lp:
        # Supports if it's epoch or already string
        if isinstance(lp, (int, float)):
            dt = datetime.datetime.fromtimestamp(lp)
        else:
            dt = lp
        print(f"\n⌛ Last played: {bold(str(dt))}")
    print(magenta("="*36)+"\n")

# Main Menu loop
def cyan(t): return f"\033[96m{t}\033[0m"
def yellow(t): return f"\033[93m{t}\033[0m"
def bold(t): return f"\033[1m{t}\033[0m"
def magenta(t): return f"\033[95m{t}\033[0m"

def print_menu_header():
    print(magenta("\n" + "=" * 40))
    print(bold(yellow("🇬🇷 Greek Learning Game Menu 🇬🇷").center(40)))
    print(magenta("=" * 40))

def main_menu():
    while True:
        print_menu_header()
        print(bold(f"""
{cyan('1')}  {bold('Letters')}           🔤
{cyan('2')}  {bold('Combinations')}      🔗
{cyan('3')}  {bold('Words')}             📝
{cyan('4')}  {bold('Sentences')}         ✍️
{cyan('5')}  {bold('Numbers')}           🔢
{cyan('6')}  {bold('Fill in the Blank')} ___
{cyan('7')}  {bold('Show my stats')}     📊
{cyan('0')}  {bold('Quit')}              🚪
"""))
        mode = input(yellow("Type your choice: ")).strip()
        print()
        if mode == "1":
            play_letters()
        elif mode == "2":
            play_combinations()
        elif mode == "3":
            play_words()
        elif mode == "4":
            play_sentences()
        elif mode == "5":
            play_numbers()
        elif mode == "6":
            play_fill_blanks()
        elif mode == "7":
            show_stats(stats)
        elif mode == "0":
            print(bold("Bye! 👋 Happy learning!"))
            break
        else:
            print(cyan("Please choose a valid option.\n"))

# Then in your actual script, run:
main_menu()

game_end_time = time.time()
stats["playtime_seconds"] += int(game_end_time - game_start_time)
save_player_stats(stats)