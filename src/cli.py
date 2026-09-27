"""Interactive CLI detective terminal for Murder Mystery Engine."""

import sys
import time
from typing import Optional
from src.engine import ENGINE, GameSession
from src.models import AccusationRequest


class TerminalUI:
    """ANSI color and styling helpers."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    @classmethod
    def header(cls, text: str):
        print(f"\n{cls.BOLD}{cls.CYAN}═══ {text} ═══{cls.RESET}")

    @classmethod
    def alert(cls, text: str):
        print(f"{cls.BOLD}{cls.YELLOW}⚡ {text}{cls.RESET}")

    @classmethod
    def success(cls, text: str):
        print(f"{cls.BOLD}{cls.GREEN}✓ {text}{cls.RESET}")

    @classmethod
    def error(cls, text: str):
        print(f"{cls.BOLD}{cls.RED}✗ {text}{cls.RESET}")


def run_interactive_cli(case_id: str = "case_blackwood"):
    """Main terminal loop for the murder mystery game."""
    session = ENGINE.create_session(case_id)
    dossier = session.dossier

    print("\n" + "=" * 70)
    print(f"{TerminalUI.BOLD}{TerminalUI.MAGENTA}  🕵️  MURDER MYSTERY ENGINE — AI WHO-DUN-IT GENERATOR{TerminalUI.RESET}")
    print(f"{TerminalUI.DIM}  Powered by LangGraph Multi-Agent Stateful Orchestration{TerminalUI.RESET}")
    print("=" * 70)

    TerminalUI.header(f"CASE FILE: {dossier.title}")
    print(f"{TerminalUI.BOLD}Setting:{TerminalUI.RESET} {dossier.subtitle}")
    print(f"{TerminalUI.BOLD}Victim:{TerminalUI.RESET} {dossier.victim}")
    print(f"{TerminalUI.BOLD}Crime Scene:{TerminalUI.RESET} {dossier.crime_scene}")
    print(f"{TerminalUI.BOLD}Estimated Time of Death:{TerminalUI.RESET} {dossier.time_of_death}")
    print(f"\n{TerminalUI.DIM}{dossier.synopsis}{TerminalUI.RESET}")

    print(f"\n{TerminalUI.BOLD}PERSONS OF INTEREST:{TerminalUI.RESET}")
    for idx, s in enumerate(dossier.suspects, start=1):
        print(f"  [{idx}] {TerminalUI.BOLD}{s.name}{TerminalUI.RESET} ({s.role})")
        print(f"      Alibi: {TerminalUI.DIM}{s.alibi}{TerminalUI.RESET}")

    while session.remaining_turns > 0:
        print(f"\n{TerminalUI.BOLD}─── Detective Actions (Remaining Question Turns: {session.remaining_turns}) ───{TerminalUI.RESET}")
        print(" [1-3] Interrogate Suspect  |  [c] Evidence Locker  |  [a] Indict & Accuse  |  [q] Quit")
        
        try:
            choice = input(f"{TerminalUI.CYAN}Detective Command > {TerminalUI.RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nDetective retired from the case.")
            break

        if choice in ["q", "quit", "exit"]:
            print("Exiting investigation.")
            break

        if choice in ["c", "clues", "evidence"]:
            show_evidence_locker(session)
            continue

        if choice in ["a", "accuse", "indict"]:
            handle_accusation(session)
            break

        if choice in ["1", "2", "3"]:
            suspect_idx = int(choice) - 1
            if 0 <= suspect_idx < len(dossier.suspects):
                suspect = dossier.suspects[suspect_idx]
                interrogate_suspect(session, suspect.id, suspect.name)
            else:
                TerminalUI.error("Invalid suspect index.")
        else:
            TerminalUI.alert("Unknown command. Type 1, 2, 3, 'c' for clues, or 'a' to accuse.")

    if session.remaining_turns <= 0 and not session.scorecard:
        TerminalUI.alert("\nYour time at the crime scene has expired! You must now formalize your indictment.")
        handle_accusation(session)


def interrogate_suspect(session: GameSession, suspect_id: str, suspect_name: str):
    """Sub-loop to interrogate a specific suspect."""
    TerminalUI.header(f"INTERROGATION ROOM: {suspect_name}")
    print(f"{TerminalUI.DIM}Type your question to interrogate {suspect_name}. (Type 'back' to return to case board){TerminalUI.RESET}\n")

    while session.remaining_turns > 0:
        try:
            question = input(f"{TerminalUI.YELLOW}Question for {suspect_name} > {TerminalUI.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not question or question.lower() == "back":
            break

        print(f"{TerminalUI.DIM}*Analyzing psychological response & memory checkpointer...*{TerminalUI.RESET}")
        resp = session.interrogate(suspect_id, question)

        print(f"\n{TerminalUI.BOLD}{suspect_name}:{TerminalUI.RESET} \"{resp.answer}\"\n")

        if resp.clues_unlocked:
            for clue in resp.clues_unlocked:
                print(f"{TerminalUI.BOLD}{TerminalUI.GREEN}🔍 BREAKTHROUGH CLUE DISCOVERED!{TerminalUI.RESET}")
                print(f"   [{clue.category.upper()}] {TerminalUI.BOLD}{clue.title}{TerminalUI.RESET}")
                print(f"   {clue.description}\n")

        print(f"{TerminalUI.DIM}[Remaining question turns: {resp.remaining_turns}]{TerminalUI.RESET}")


def show_evidence_locker(session: GameSession):
    """Display discovered clues and forensic facts."""
    unlocked = session.get_unlocked_clues()
    TerminalUI.header("FORENSIC EVIDENCE LOCKER")
    if not unlocked:
        print(f"{TerminalUI.DIM}No physical or forensic breakthroughs yet. Keep probing suspects about the crime scene, timeline, and motives.{TerminalUI.RESET}")
    else:
        for idx, clue in enumerate(unlocked, start=1):
            print(f"  {idx}. [{clue.category.upper()}] {TerminalUI.BOLD}{clue.title}{TerminalUI.RESET}")
            print(f"     {clue.description}")
    print()


def handle_accusation(session: GameSession):
    """Formalize indictment and score against Truth Keeper agent."""
    dossier = session.dossier
    TerminalUI.header("COURT OF FORMAL INDICTMENT")
    print(f"{TerminalUI.BOLD}The suspects are gathered in the drawing room. Who is the murderer?{TerminalUI.RESET}")

    for idx, s in enumerate(dossier.suspects, start=1):
        print(f"  [{idx}] {s.name} ({s.role})")

    suspect_choice = input(f"\n{TerminalUI.CYAN}Accuse suspect number (1-{len(dossier.suspects)}) > {TerminalUI.RESET}").strip()
    try:
        s_idx = int(suspect_choice) - 1
        accused_id = dossier.suspects[s_idx].id
        accused_name = dossier.suspects[s_idx].name
    except (ValueError, IndexError):
        accused_id = dossier.suspects[0].id
        accused_name = dossier.suspects[0].name

    weapon = input(f"{TerminalUI.CYAN}Murder Weapon Used (e.g. Wolfsbane, Poison, Gas, etc.) > {TerminalUI.RESET}").strip()
    motive = input(f"{TerminalUI.CYAN}Motive Theory (Why did they do it?) > {TerminalUI.RESET}").strip()

    unlocked_ids = session.unlocked_clue_ids

    accusation = AccusationRequest(
        accused_suspect_id=accused_id,
        accused_weapon=weapon,
        motive_theory=motive,
        cited_clue_ids=unlocked_ids,
    )

    print(f"\n{TerminalUI.DIM}*Truth Keeper Agent evaluating ground-truth LangGraph state...*{TerminalUI.RESET}")
    scorecard = session.accuse(accusation)

    TerminalUI.header("VERDICT & DETECTIVE SCORECARD")
    if scorecard.is_solved:
        TerminalUI.success(f"CASE SOLVED! {scorecard.verdict_summary}")
    else:
        TerminalUI.error(f"CASE UNSOLVED! {scorecard.verdict_summary}")

    print(f"\n  Final Detective Score:  {TerminalUI.BOLD}{scorecard.total_score} / 100{TerminalUI.RESET}")
    print(f"  Assigned Rank:          {TerminalUI.BOLD}{scorecard.rank}{TerminalUI.RESET}")
    print(f"  Culprit Match:          {'✓ YES' if scorecard.culprit_match else '✗ NO'}")
    print(f"  Weapon Identified:      {'✓ YES' if scorecard.weapon_match else '✗ NO'}")
    print(f"  Motive Score:           {scorecard.motive_score} / 40")
    print(f"  Evidence Score:         {scorecard.evidence_score} / 30")

    print(f"\n{TerminalUI.BOLD}Ground Truth Dossier Revelation:{TerminalUI.RESET}")
    print(f"  Real Culprit:  {scorecard.ground_truth_culprit}")
    print(f"  Real Weapon:   {scorecard.ground_truth_weapon}")
    print(f"  True Motive:   {scorecard.ground_truth_motive}\n")


def run_demo_simulation(case_id: str = "case_blackwood") -> str:
    """Non-interactive simulation runner capturing complete gameplay output."""
    session = ENGINE.create_session(case_id)
    output_lines = []

    def log(msg: str):
        output_lines.append(msg)
        print(msg)

    log("=" * 75)
    log(f"DETECTIVE SIMULATION: Murder Mystery Engine ({session.dossier.title})")
    log("=" * 75)

    log(f"\n[PHASE 1: CRIME SCENE BRIEFING]")
    log(f"Victim:       {session.dossier.victim}")
    log(f"Scene:        {session.dossier.crime_scene}")
    log(f"Suspects:     {', '.join(s.name for s in session.dossier.suspects)}")

    log(f"\n[PHASE 2: INTERROGATING SUSPECT 1 — ARTHUR PENDELTON (BUTLER)]")
    resp1 = session.interrogate("butler_arthur", "Where were you when Lord Reginald was poisoned?")
    log(f"Detective: Where were you when Lord Reginald was poisoned?")
    log(f"Arthur: \"{resp1.answer}\"")

    log(f"\n[PHASE 3: INTERROGATING SUSPECT 2 — BEATRICE BLACKWOOD (HEIRESS)]")
    resp2 = session.interrogate("heiress_beatrice", "Did Lord Reginald mention amending his will?")
    log(f"Detective: Did Lord Reginald mention amending his will?")
    log(f"Beatrice: \"{resp2.answer}\"")

    log(f"\n[PHASE 4: INTERROGATING SUSPECT 3 — DR. ALISTAIR FINCH (PHYSICIAN)]")
    resp3 = session.interrogate("doctor_finch", "Did you examine the port decanter or prescribe Wolfsbane recently?")
    log(f"Detective: Did you examine the port decanter or prescribe Wolfsbane recently?")
    log(f"Dr. Finch: \"{resp3.answer}\"")

    if resp3.clues_unlocked:
        for c in resp3.clues_unlocked:
            log(f"  >>> FORENSIC CLUE REVEALED: [{c.title}] - {c.description}")

    resp4 = session.interrogate("doctor_finch", "Lord Reginald found your medical malpractice records regarding Lady Blackwood!")
    log(f"\nDetective: Lord Reginald found your medical malpractice records regarding Lady Blackwood!")
    log(f"Dr. Finch: \"{resp4.answer}\"")

    if resp4.clues_unlocked:
        for c in resp4.clues_unlocked:
            log(f"  >>> FORENSIC CLUE REVEALED: [{c.title}] - {c.description}")

    log(f"\n[PHASE 5: COURT OF FORMAL ACCUSATION]")
    accusation = AccusationRequest(
        accused_suspect_id="doctor_finch",
        accused_weapon="Aconite Wolfsbane poison in port decanter",
        motive_theory="Dr. Finch killed Reginald to prevent exposure of his medical malpractice and murder of Lady Blackwood",
        cited_clue_ids=session.unlocked_clue_ids,
    )
    scorecard = session.accuse(accusation)

    log(f"Indictment Target: Dr. Alistair Finch")
    log(f"Accusation Status: {'SOLVED' if scorecard.is_solved else 'FAILED'}")
    log(f"Total Score:       {scorecard.total_score} / 100")
    log(f"Detective Rank:    {scorecard.rank}")
    log(f"Summary:           {scorecard.verdict_summary}")
    log("\n" + "=" * 75)
    log("SIMULATION RUN COMPLETED WITH ZERO ERRORS")
    log("=" * 75)

    return "\n".join(output_lines)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_simulation()
    else:
        run_interactive_cli()
