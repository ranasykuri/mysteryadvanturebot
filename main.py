#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Mystery Adventure Bot - Text-based Adventure Game
=======================================================
A mysterious adventure game where players wake up in an unknown location
and must explore, solve puzzles, and make choices to uncover the mystery.

Author: Mystery Game Dev
Version: 1.0
"""

import sys
import json
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field


# ==================== ENUMS & DATA CLASSES ====================

class GameState(Enum):
    """Enumeration for different game states"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    ENDED = "ended"


class EndingType(Enum):
    """Enumeration for different story endings"""
    GOOD = "good"
    BAD = "bad"
    SECRET = "secret"


@dataclass
class Item:
    """Represents an inventory item"""
    id: str
    name: str
    description: str
    
    def __repr__(self) -> str:
        return f"{self.name}"


@dataclass
class Dialogue:
    """Represents an NPC dialogue option"""
    text: str
    response: str
    next_action: Optional[str] = None
    requires_item: Optional[str] = None
    unlocks_location: Optional[str] = None


@dataclass
class NPC:
    """Represents a Non-Player Character"""
    id: str
    name: str
    location_id: str
    description: str
    dialogues: List[Dialogue] = field(default_factory=list)
    met: bool = False


@dataclass
class Puzzle:
    """Represents a puzzle or riddle"""
    id: str
    location_id: str
    question: str
    correct_answer: str
    hints: List[str] = field(default_factory=list)
    reward: Optional[str] = None
    solved: bool = False


@dataclass
class Location:
    """Represents a game location/room"""
    id: str
    name: str
    description: str
    locked: bool = False
    visited: bool = False
    items: List[str] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    exits: Dict[str, str] = field(default_factory=dict)
    puzzle: Optional[str] = None
    unlock_requirements: Optional[List[str]] = None


@dataclass
class PlayerState:
    """Represents the current player state"""
    name: str = "Pemain"
    current_location: str = "starting_room"
    inventory: List[Item] = field(default_factory=list)
    visited_locations: Set[str] = field(default_factory=set)
    completed_puzzles: Set[str] = field(default_factory=set)
    unlocked_locations: Set[str] = field(default_factory=set)
    special_flags: Dict[str, bool] = field(default_factory=dict)


# ==================== STORY DATA ====================

class StoryData:
    """Contains all story-related data for the game"""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.npcs: Dict[str, NPC] = {}
        self.items: Dict[str, Item] = {}
        self.puzzles: Dict[str, Puzzle] = {}
        self._initialize_story()
    
    def _initialize_story(self):
        """Initialize all story elements"""
        self._create_items()
        self._create_locations()
        self._create_npcs()
        self._create_puzzles()
    
    def _create_items(self):
        """Create all game items"""
        items_data = [
            ("old_key", "🔑 Kunci Tua", "Kunci berkarat yang sangat tua"),
            ("mysterious_note", "📝 Catatan Misterius", "Catatan dengan pesan samar"),
            ("crystal_gem", "💎 Kristal Bercahaya", "Kristal yang bercahaya biru"),
            ("ancient_coin", "🪙 Koin Kuno", "Koin emas dengan simbol aneh"),
            ("torch", "🔦 Obor", "Obor yang masih menyala terang"),
            ("diary", "📖 Buku Harian", "Buku harian dengan tulisan penting"),
        ]
        
        for item_id, item_name, item_desc in items_data:
            self.items[item_id] = Item(item_id, item_name, item_desc)
    
    def _create_locations(self):
        """Create all game locations"""
        
        # Lokasi 1: Ruang Awal
        self.locations["starting_room"] = Location(
            id="starting_room",
            name="🌑 Ruang Gelap",
            description="Anda terbangun di ruangan gelap dengan peluh dingin. Cahaya redup masuk dari celah. Aroma lembab dan tanah membanjiri udara.",
            locked=False,
            items=["mysterious_note", "old_key"],
            exits={"timur": "hallway"}
        )
        
        # Lokasi 2: Koridor
        self.locations["hallway"] = Location(
            id="hallway",
            name="🏚️ Koridor Panjang",
            description="Koridor panjang dengan dinding bata tua. Lukisan-lukisan aneh menghiasi dinding. Beberapa pintu terlihat di sekitar Anda.",
            locked=False,
            items=[],
            exits={
                "barat": "starting_room",
                "utara": "library",
                "selatan": "cellar",
            }
        )
        
        # Lokasi 3: Perpustakaan
        self.locations["library"] = Location(
            id="library",
            name="📚 Perpustakaan",
            description="Perpustakaan luas dengan rak buku mencapai langit-langit. Buku dan kertas berserakan di lantai. Meja besar penuh dengan catatan.",
            locked=False,
            items=["diary"],
            npcs=["librarian"],
            exits={
                "selatan": "hallway",
                "timur": "study_room",
            }
        )
        
        # Lokasi 4: Ruang Kerja
        self.locations["study_room"] = Location(
            id="study_room",
            name="✍️ Ruang Kerja",
            description="Ruang kerja dengan meja tulis besar. Pena, tinta, dan kertas berserakan. Di atas meja ada lukisan wanita dengan mata yang misterius.",
            locked=False,
            items=[],
            puzzle="study_puzzle",
            npcs=["scholar"],
            exits={
                "barat": "library",
                "utara": "tower",
            }
        )
        
        # Lokasi 5: Menara
        self.locations["tower"] = Location(
            id="tower",
            name="🗼 Menara Lonceng",
            description="Menara tinggi dengan lonceng besar yang tergantung diam. Dari sini Anda bisa melihat seluruh tempat yang tertutup kabut.",
            locked=True,
            unlock_requirements=["study_puzzle"],
            items=["crystal_gem"],
            exits={
                "selatan": "study_room",
                "utara": "secret_room",
            }
        )
        
        # Lokasi 6: Ruang Bawah Tanah
        self.locations["cellar"] = Location(
            id="cellar",
            name="🕷️ Ruang Bawah Tanah",
            description="Ruang bawah tanah yang basah dan dingin. Botol-botol dan barang penyimpanan tersebar. Suara air menetes dari langit-langit.",
            locked=False,
            items=["torch"],
            npcs=["gatekeeper"],
            exits={
                "utara": "hallway",
                "barat": "vault",
            }
        )
        
        # Lokasi 7: Kamar Rahasia
        self.locations["secret_room"] = Location(
            id="secret_room",
            name="✨ Kamar Rahasia",
            description="Ruangan tersembunyi penuh dengan peta kuno dan catatan penelitian. Di tengah ruangan ada altar dengan kristal besar yang bercahaya biru.",
            locked=True,
            unlock_requirements=["tower"],
            items=[],
            npcs=["spirit"],
            puzzle="vault_puzzle",
            exits={
                "selatan": "tower",
            }
        )
        
        # Lokasi 8: Vault Rahasia
        self.locations["vault"] = Location(
            id="vault",
            name="🔐 Vault Rahasia",
            description="Pintu besi berat terbuka lebar. Brankas kuno terlihat dengan dokumen penting. Di sini terletak kebenaran tentang siapa Anda.",
            locked=True,
            unlock_requirements=["vault_puzzle"],
            npcs=["keeper"],
            exits={
                "timur": "cellar",
            }
        )
    
    def _create_npcs(self):
        """Create all NPCs and their dialogues"""
        
        # NPC 1: Librarian
        librarian = NPC(
            id="librarian",
            name="👴 Petugas Perpustakaan",
            location_id="library",
            description="Pria tua dengan kacamata yang seperti hidup di perpustakaan"
        )
        librarian.dialogues = [
            Dialogue(
                text="Selamat datang... Anda adalah tamtamu yang pertama",
                response="Petugas perpustakaan itu memandang Anda. 'Cari jawaban di ruang kerja,' katanya."
            ),
        ]
        self.npcs["librarian"] = librarian
        
        # NPC 2: Scholar
        scholar = NPC(
            id="scholar",
            name="🧠 Ulama Tua",
            location_id="study_room",
            description="Seorang pria yang terlihat seperti peneliti"
        )
        scholar.dialogues = [
            Dialogue(
                text="Siapa Anda?",
                response="'Seseorang tertinggal di sini. Pecahkan teka-teki untuk melanjutkan.'"
            ),
        ]
        self.npcs["scholar"] = scholar
    
    def _create_puzzles(self):
        """Create all puzzles and riddles"""
        
        # Puzzle 1: Study Room - Literary Cipher
        self.puzzles["study_puzzle"] = Puzzle(
            id="study_puzzle",
            location_id="study_room",
            question="""📚 Teka-teki pada meja:
'Buku pertama di rak ketiga: A...'
'Buku terakhir di rak pertama: B...'
'Buku kedua di rak kedua: C...'

Ambil huruf pertama tiap judul. Apa akronimnya?
- Rak 1: 'Beauty', 'Cosmos', 'Dreams'
- Rak 2: 'Evolution', 'Foundations', 'Gravity'
- Rak 3: 'Ancient', 'Beyond', 'Crystals'""",
            correct_answer="baf",
            hints=[
                "🔍 Perhatikan urutannya dengan hati-hati",
                "📖 Ambil huruf pertama dari judul",
                "🧩 Buku pertama rak 3, terakhir rak 1, kedua rak 2",
                "✓ Jawabannya 3 huruf"
            ],
            reward="tower"
        )
        
        # Puzzle 2: Secret Room - Pattern Vault
        self.puzzles["vault_puzzle"] = Puzzle(
            id="vault_puzzle",
            location_id="secret_room",
            question="""🔐 Pada altar, urutan angka tertulis:
2, 4, 8, 16, ?, ?, ?

Isilah 3 angka berikutnya. Ketikkan angka ketiga.""",
            correct_answer="128",
            hints=[
                "🔍 Setiap angka 2x lipat dari sebelumnya",
                "📊 Deret geometri dengan rasio 2",
                "✏️ Setelah 16 adalah 32, 64, 128",
                "🎯 Kamu mencari angka yang ke-6"
            ],
            reward="vault"
        )


# ==================== GAME ENGINE ====================

class GameEngine:
    """Main game engine that manages game logic and flow"""
    
    def __init__(self):
        self.state = GameState.MENU
        self.story = StoryData()
        self.player = PlayerState()
        self.game_over = False
        self.ending_type: Optional[EndingType] = None
        
        # Initialize unlocked locations
        self.player.unlocked_locations.add("starting_room")
        self.player.unlocked_locations.add("hallway")
    
    def start_game(self, player_name: str):
        """Start a new game"""
        self.player.name = player_name
        self.state = GameState.PLAYING
        self._display_intro()
    
    def _display_intro(self):
        """Display game introduction"""
        clear_screen()
        print("\n" + "="*70)
        print("  🎮 THE MYSTERY ADVENTURE BOT - Petualangan Penuh Misteri")
        print("="*70 + "\n")
        
        print(f"👋 Selamat datang, {self.player.name}!\n")
        print("😵 Anda terbangun dengan pikiran yang kosong...")
        print("🌑 Tidak mengingat siapa Anda atau bagaimana Anda sampai di sini...")
        print("\n🔊 Dalam gelap yang mengelilingi, terdengar suara yang jauh-jauh.")
        print("💭 Ada sesuatu yang penting untuk ditemukan...\n")
        print("-"*70)
    
    def check_location_access(self, location_id: str) -> Tuple[bool, str]:
        """Check if player can access a location"""
        if location_id not in self.story.locations:
            return False, "Lokasi tidak ditemukan."
        
        location = self.story.locations[location_id]
        
        if location.locked:
            if location_id not in self.player.unlocked_locations:
                if location.unlock_requirements:
                    required = location.unlock_requirements[0]
                    if required in self.player.completed_puzzles or \
                       required in self.player.unlocked_locations:
                        # Unlock location
                        self.player.unlocked_locations.add(location_id)
                        return True, "Lokasi telah terbuka!"
                    else:
                        return False, f"Lokasi ini terkunci. Anda memerlukan: {required}"
                else:
                    return False, "Lokasi ini terkunci dan tidak dapat dibuka."
            else:
                return True, ""
        
        return True, ""
    
    def move_to_location(self, direction: str) -> Tuple[bool, str]:
        """Move player to a different location"""
        current_location = self.story.locations[self.player.current_location]
        
        if direction not in current_location.exits:
            return False, f"➡️ {self.player.name}, arah tersebut tidak tersedia."
        
        next_location_id = current_location.exits[direction]
        can_access, msg = self.check_location_access(next_location_id)
        
        if not can_access:
            return False, f"🚫 {self.player.name}, {msg}"
        
        self.player.current_location = next_location_id
        self.player.visited_locations.add(next_location_id)
        
        return True, f"🚶 {self.player.name} berjalan ke {direction}..."
    
    def pick_up_item(self, item_name: str) -> Tuple[bool, str]:
        """Pick up an item from the current location"""
        location = self.story.locations[self.player.current_location]
        
        # Find item by name or id
        item_id = None
        for available_item_id in location.items:
            item = self.story.items[available_item_id]
            if item_name.lower() in item.name.lower() or \
               item_name.lower() in item.id.lower():
                item_id = available_item_id
                break
        
        if not item_id:
            return False, f"❌ {self.player.name}, item tidak ditemukan di sini."
        
        item = self.story.items[item_id]
        self.player.inventory.append(item)
        location.items.remove(item_id)
        
        return True, f"✅ {self.player.name}, Anda mengambil {item.name}!"
    
    def check_inventory(self) -> str:
        """Check player's inventory"""
        if not self.player.inventory:
            return f"🎒 {self.player.name}, inventaris Anda kosong."
        
        result = f"🎒 === INVENTARIS {self.player.name.upper()} ===\n"
        for i, item in enumerate(self.player.inventory, 1):
            result += f"{i}. {item.name}\n"
        return result
    
    def interact_with_npc(self, npc_name: str) -> Tuple[bool, str]:
        """Interact with an NPC"""
        location = self.story.locations[self.player.current_location]
        
        # Find NPC in current location
        npc_id = None
        for available_npc_id in location.npcs:
            npc = self.story.npcs[available_npc_id]
            if npc_name.lower() in npc.name.lower() or \
               npc_name.lower() in npc.id.lower():
                npc_id = available_npc_id
                break
        
        if not npc_id:
            return False, f"👤 {self.player.name}, NPC tidak ditemukan di lokasi ini."
        
        npc = self.story.npcs[npc_id]
        npc.met = True
        
        return True, self._display_npc_dialogue(npc)
    
    def _display_npc_dialogue(self, npc: NPC) -> str:
        """Display NPC dialogue options"""
        result = f"\n[{npc.name}]\n💬 \"{npc.dialogues[0].text}\"\n\n"
        result += f"💭 {npc.dialogues[0].response}\n"
        
        return result
    
    def solve_puzzle(self, puzzle_id: str, answer: str) -> Tuple[bool, str]:
        """Attempt to solve a puzzle"""
        if puzzle_id not in self.story.puzzles:
            return False, f"❌ {self.player.name}, puzzle tidak ditemukan."
        
        puzzle = self.story.puzzles[puzzle_id]
        
        if puzzle.solved:
            return False, f"✅ {self.player.name}, Anda sudah menyelesaikan puzzle ini."
        
        if answer.lower() == puzzle.correct_answer.lower():
            puzzle.solved = True
            self.player.completed_puzzles.add(puzzle_id)
            
            if puzzle.reward:
                self.player.unlocked_locations.add(puzzle.reward)
                return True, f"🎉 {self.player.name}, BENAR! Lokasi baru terbuka: {self.story.locations[puzzle.reward].name}"
            else:
                return True, f"🎉 {self.player.name}, BENAR! Puzzle selesai!"
        else:
            return False, f"❌ {self.player.name}, jawaban salah. Coba lagi!"
    
    def get_puzzle_hint(self, puzzle_id: str) -> str:
        """Get a hint for a puzzle"""
        if puzzle_id not in self.story.puzzles:
            return f"❌ {self.player.name}, puzzle tidak ditemukan."
        
        puzzle = self.story.puzzles[puzzle_id]
        
        if not puzzle.hints:
            return f"❓ {self.player.name}, tidak ada hint tersedia untuk puzzle ini."
        
        if not hasattr(puzzle, '_hint_index'):
            puzzle._hint_index = 0
        
        if puzzle._hint_index < len(puzzle.hints):
            hint = puzzle.hints[puzzle._hint_index]
            puzzle._hint_index += 1
            return f"💡 {self.player.name}, {hint}"
        else:
            return f"❓ {self.player.name}, Anda sudah mendapatkan semua hint untuk puzzle ini."
    
    def examine_location(self) -> str:
        """Get detailed description of current location"""
        location = self.story.locations[self.player.current_location]
        
        result = f"\n{'='*70}\n"
        result += f"📍 LOKASI: {location.name}\n"
        result += f"👤 {self.player.name}\n"
        result += f"{'='*70}\n\n"
        result += f"{location.description}\n\n"
        
        if location.items:
            result += "📦 Item yang tersedia:\n"
            for item_id in location.items:
                item = self.story.items[item_id]
                result += f"  • {item.name}\n"
        else:
            result += "📦 Tidak ada item di sini.\n"
        
        result += "\n"
        
        if location.npcs:
            result += "👥 Orang yang ada di sini:\n"
            for npc_id in location.npcs:
                npc = self.story.npcs[npc_id]
                result += f"  • {npc.name}\n"
        
        result += "\n"
        
        if location.exits:
            result += "🚪 Arah yang tersedia:\n"
            for direction, target_loc_id in location.exits.items():
                target_loc = self.story.locations[target_loc_id]
                status = "✅" if target_loc_id in self.player.unlocked_locations else "❌"
                result += f"  {status} {direction.upper()}: {target_loc.name}\n"
        
        return result
    
    def check_ending(self) -> Optional[EndingType]:
        """Check if game has reached an ending"""
        location_id = self.player.current_location
        
        # Secret Ending
        if location_id == "hidden_chamber" and \
           "crystal_gem" in [item.id for item in self.player.inventory]:
            self.ending_type = EndingType.SECRET
            return EndingType.SECRET
        
        # Good Ending
        if location_id == "secret_vault" and \
           len(self.player.completed_puzzles) >= 3:
            self.ending_type = EndingType.GOOD
            return EndingType.GOOD
        
        # Bad Ending (terjebak terlalu lama)
        if len(self.player.visited_locations) < 3 and \
           self.player.special_flags.get("lost_too_long", False):
            self.ending_type = EndingType.BAD
            return EndingType.BAD
        
        return None
    
    def display_ending(self):
        """Display the ending based on ending type"""
        clear_screen()
        print("\n" + "="*70)
        
        if self.ending_type == EndingType.SECRET:
            print("  ✨ ENDING RAHASIA: TRANSCENDENCE ✨")
            print("="*70 + "\n")
            print(f"""🎉 {self.player.name}...

Kristal bercahaya di tangan Anda mulai berdenyut seperti detak jantung.

Cahaya biru memancar, menerangi seluruh ruangan. Roh kuno akhirnya terbebas.

Tubuh Anda menjadi cahaya, menyatu dengan kristal. Kesadaran meluas, 
melampaui dimensi, melampaui waktu.

Anda bukan lagi manusia biasa.
Anda adalah bagian dari dimensi ini - Penjaga yang menunggu generasi berikutnya.

═══════════════════════════════════════════════════════════════════════════
                        ✨ TRANSCENDENCE ✨
                Anda telah melampaui batas-batas realitas.
═══════════════════════════════════════════════════════════════════════════
            """)
        
        elif self.ending_type == EndingType.GOOD:
            print("  ✓ ENDING BAIK: KEBEBASAN")
            print("="*70 + "\n")
            print(f"""🎉 {self.player.name}...

Penjaga vault memberikan alat kristal untuk membuka portal kembali.

Dengan pengetahuan yang telah Anda kumpulkan, Anda merekalibrasi perangkat.
Cahaya terang memancar. Ruang bergetar dan mulai memudar.

Anda melangkah melalui portal - kembali ke dunia nyata.

Di sisi lain, kolega Anda menunggu dengan terkejut:
'Dr. Chen... Anda hilang 20 tahun yang lalu!'

Tapi untuk Anda, hanya beberapa jam telah berlalu.

Dengan pengetahuan dari dimensi lain, Anda akan mengubah dunia.

═══════════════════════════════════════════════════════════════════════════
                        ✓ KEBEBASAN ✓
                Anda telah melarikan diri dan membawa kebenaran.
═══════════════════════════════════════════════════════════════════════════
            """)
        
        elif self.ending_type == EndingType.BAD:
            print("  ✗ ENDING BURUK: TERJEBAK SELAMANYA")
            print("="*70 + "\n")
            print(f"""😱 {self.player.name}...

Anda telah berjalan dalam lingkaran berkali-kali. 
Koridor-koridor terlihat semakin gelap.

Pikiran Anda kabur. Realitas dan mimpi bercampur.

Suara-suara lain terdengar dalam pikiran, berbisik dengan tidak sabar,
menunggu Anda bergabung dengan mereka.

Anda telah menjadi bagian dari misteri ini.

═══════════════════════════════════════════════════════════════════════════
                        ✗ TERJEBAK SELAMANYA ✗
                Tidak ada jalan keluar dari tempat ini.
        ==================================================================
            """)
    
    def get_game_status(self) -> str:
        """Get current game status"""
        location = self.story.locations[self.player.current_location]
        
        status = f"\n[STATUS] {self.player.name}\n"
        status += f"Lokasi: {location.name}\n"
        status += f"Lokasi Dikunjungi: {len(self.player.visited_locations)}\n"
        status += f"Puzzle Selesai: {len(self.player.completed_puzzles)}\n"
        status += f"Item: {len(self.player.inventory)}\n"
        
        return status


# ==================== USER INTERFACE ====================

def clear_screen():
    """Clear the console screen"""
    import os
    os.system('clear' if os.name != 'nt' else 'cls')


def display_main_menu():
    """Display the main menu"""
    clear_screen()
    print("\n" + "="*70)
    print("  🎮 THE MYSTERY ADVENTURE BOT")
    print("  Petualangan yang Penuh Misteri")
    print("="*70 + "\n")
    print("1️⃣  Mulai Permainan Baru")
    print("2️⃣  Tentang Game")
    print("3️⃣  Keluar")
    print("\n" + "-"*70)


def display_game_menu():
    """Display the in-game menu"""
    print("\n" + "-"*70)
    print("⚡ PERINTAH YANG BISA DIGUNAKAN:")
    print("  📍 lihat         - Lihat lokasi saat ini")
    print("  🎒 inventaris    - Lihat inventaris Anda")
    print("  🤲 ambil [item]  - Ambil item (contoh: ambil kunci)")
    print("  👥 bicara [npc]  - Bicara dengan NPC")
    print("  🧩 puzzle        - Lihat puzzle di lokasi ini")
    print("  ✍️  jawab [teks]  - Jawab puzzle")
    print("  💡 hint          - Dapatkan hint untuk puzzle")
    print("  🚪 ke [arah]     - Pindah ke lokasi (utara, selatan, timur, barat)")
    print("  📊 status        - Lihat status permainan")
    print("  ❓ bantuan       - Tampilkan bantuan")
    print("  🚪 keluar        - Keluar dari permainan")
    print("-"*70)


def get_player_input(prompt: str = "> ") -> str:
    """Get player input from command line"""
    try:
        return input(prompt).strip().lower()
    except EOFError:
        return "keluar"


def display_help():
    """Display help information"""
    clear_screen()
    print("\n" + "="*70)
    print("  [?] BANTUAN DAN PANDUAN")
    print("="*70 + "\n")
    
    print("TUJUAN GAME:")
    print("----------")
    print("* Ingat identitas Anda")
    print("* Temukan cara keluar dari tempat ini")
    print("* Ungkap misteri di balik situasi ini")
    print()
    print("TIPS BERMAIN:")
    print("-----------")
    print("* Jelajahi semua lokasi dan bicara dengan semua NPC")
    print("* Kumpulkan semua item yang tersedia")
    print("* Selesaikan puzzle untuk membuka lokasi baru")
    print("* Baca deskripsi dengan seksama - ada petunjuk tersembunyi")
    print("* Setiap keputusan penting")
    print()
    print("SISTEM PUZZLE:")
    print("-------------")
    print("Beberapa lokasi memiliki puzzle. Gunakan 'hint' jika terjebak!")
    print()
    print("ENDING:")
    print("------")
    print("Ada 3 ending berbeda tergantung pilihan dan item yang Anda kumpulkan.")
    print()
    print("SELAMAT BERMAIN!")
    
    print("-"*70)
    input("Tekan Enter untuk melanjutkan...")


def get_about():
    """Get about information"""
    clear_screen()
    print("\n" + "="*70)
    print("  TENTANG THE MYSTERY ADVENTURE BOT")
    print("="*70 + "\n")
    
    print("DESKRIPSI:")
    print("---------")
    print("Game petualangan berbasis teks yang imersif di mana Anda berperan")
    print("sebagai Dr. Chen, ilmuwan yang terjebak dalam dimensi alternatif.")
    print()
    print("FITUR:")
    print("-----")
    print("* Cerita Bercabang - Pilihan Anda mempengaruhi alur")
    print("* 3 Ending Berbeda - Baik, Buruk, dan Rahasia")
    print("* 2 Puzzle Logika - Tantangan yang menarik")
    print("* 5 NPC Interaktif - Karakter dengan dialog unik")
    print("* 8 Lokasi Unik - Atmosfer misterius yang kaya")
    print("* Sistem Inventaris - Kumpulkan item untuk melanjutkan")
    print("* Progressive Unlock - Buka lokasi saat Anda maju")
    print()
    print("7 LOKASI UNTUK DIJELAJAHI:")
    print("-------------------------")
    print("1. Ruang Gelap (Start)")
    print("2. Koridor Panjang")
    print("3. Perpustakaan")
    print("4. Ruang Kerja")
    print("5. Menara Lonceng")
    print("6. Ruang Bawah Tanah")
    print("7. Vault Rahasia (+ 1 lokasi tersembunyi)")
    print()
    print("VERSI: 1.0")
    print("PLATFORM: Terminal/Command Line")
    print("BAHASA: Indonesian")
    print()
    print("="*70)
    print("   Dibuat dengan passion untuk pecinta misteri dan petualangan!")
    print("="*70)
    
    print("-"*70)
    input("Tekan Enter untuk melanjutkan...")


# ==================== MAIN GAME LOOP ====================

def main():
    """Main game loop"""
    engine = GameEngine()
    
    while True:
        if engine.state == GameState.MENU:
            display_main_menu()
            choice = get_player_input("Pilihan Anda: ")
            
            if choice == "1":
                player_name = input("\n👤 Masukkan nama Anda: ").strip()
                if not player_name:
                    player_name = "Penjelajah Misteri"
                engine.start_game(player_name)
                
            elif choice == "2":
                get_about()
                
            elif choice == "3":
                print("\n👋 Terima kasih telah bermain The Mystery Adventure Bot!")
                print("🌟 Sampai jumpa lagi!\n")
                sys.exit(0)
            else:
                print("❌ Pilihan tidak valid. Silakan coba lagi.")
                input("Tekan Enter untuk melanjutkan...")
        
        elif engine.state == GameState.PLAYING:
            # Check for ending
            if engine.check_ending():
                engine.display_ending()
                engine.state = GameState.ENDED
                continue
            
            # Show location
            print(engine.examine_location())
            
            display_game_menu()
            
            # Get player command
            command_input = get_player_input()
            
            if not command_input:
                continue
            
            # Parse command
            parts = command_input.split(maxsplit=1)
            command = parts[0] if parts else ""
            args = parts[1] if len(parts) > 1 else ""
            
            # Handle commands
            if command == "lihat":
                continue
            
            elif command == "inventaris":
                print(engine.check_inventory())
                input("\nTekan Enter untuk melanjutkan...")
            
            elif command == "ambil":
                if not args:
                    print(f"📦 {engine.player.name}, gunakan: ambil [nama item]")
                else:
                    success, message = engine.pick_up_item(args)
                    print(message)
                    input("\nTekan Enter untuk melanjutkan...")
            
            elif command == "bicara":
                if not args:
                    print(f"👥 {engine.player.name}, gunakan: bicara [nama NPC]")
                else:
                    success, message = engine.interact_with_npc(args)
                    if success:
                        print(message)
                    else:
                        print(message)
                    input("Tekan Enter untuk melanjutkan...")
            
            elif command == "puzzle":
                location = engine.story.locations[engine.player.current_location]
                if location.puzzle:
                    puzzle = engine.story.puzzles[location.puzzle]
                    print(f"\n🧩 PUZZLE DI LOKASI INI:\n{puzzle.question}")
                else:
                    print(f"❓ {engine.player.name}, tidak ada puzzle di lokasi ini.")
                input("\nTekan Enter untuk melanjutkan...")
            
            elif command == "jawab":
                location = engine.story.locations[engine.player.current_location]
                if location.puzzle:
                    if not args:
                        print(f"📝 {engine.player.name}, gunakan: jawab [jawaban Anda]")
                    else:
                        success, message = engine.solve_puzzle(location.puzzle, args)
                        print(message)
                else:
                    print(f"❓ {engine.player.name}, tidak ada puzzle di lokasi ini.")
                input("Tekan Enter untuk melanjutkan...")
            
            elif command == "hint":
                location = engine.story.locations[engine.player.current_location]
                if location.puzzle:
                    hint = engine.get_puzzle_hint(location.puzzle)
                    print(hint)
                else:
                    print(f"❓ {engine.player.name}, tidak ada puzzle di lokasi ini.")
                input("Tekan Enter untuk melanjutkan...")
            
            elif command == "ke":
                if not args:
                    print(f"🚪 {engine.player.name}, gunakan: ke [arah]")
                    print("   Arah: utara, selatan, timur, barat, keluar, rahasia")
                else:
                    success, message = engine.move_to_location(args)
                    if success:
                        print(message)
                    else:
                        print(message)
                    input("Tekan Enter untuk melanjutkan...")
            
            elif command == "status":
                print(engine.get_game_status())
                input("Tekan Enter untuk melanjutkan...")
            
            elif command == "bantuan":
                display_help()
            
            elif command == "keluar":
                confirm = input(f"\n❓ {engine.player.name}, apakah Anda yakin keluar? (y/n): ").lower()
                if confirm == "y":
                    print(f"\n👋 Sampai jumpa lagi, {engine.player.name}!\n")
                    sys.exit(0)
            
            else:
                print(f"❌ {engine.player.name}, perintah '{command}' tidak dikenal.")
                print("   Ketik 'bantuan' untuk melihat daftar perintah.")
                input("Tekan Enter untuk melanjutkan...")
        
        elif engine.state == GameState.ENDED:
            choice = input(f"\n❓ {engine.player.name}, ingin bermain lagi? (y/n): ").lower()
            if choice == "y":
                engine = GameEngine()
                engine.state = GameState.MENU
            else:
                print(f"\n👋 Terima kasih telah bermain, {engine.player.name}!\n")
                sys.exit(0)


if __name__ == "__main__":
    main()
