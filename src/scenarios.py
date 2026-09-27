"""Curated mystery scenarios for Murder Mystery Engine."""

from typing import Dict
from src.models import MysteryDossier, Suspect, Clue


def get_case_blackwood() -> MysteryDossier:
    """Case 1: The Poisoned Chalice at Blackwood Manor."""
    return MysteryDossier(
        case_id="case_blackwood",
        title="The Poisoned Chalice at Blackwood Manor",
        subtitle="A rainy midnight in the Yorkshire Moors",
        victim="Lord Reginald Blackwood (Age 68, Eccentric Industrialist)",
        crime_scene="Private Study & Library, Blackwood Manor",
        time_of_death="Between 22:30 and 23:15, October 24th",
        weapon_used="Vintage 1928 Port laced with Aconite (Wolfsbane)",
        synopsis=(
            "Lord Reginald Blackwood was discovered slumped over his mahogany desk by the butler. "
            "His crystal decanter was half-empty, and a subtle scent of bitter almond and monkshood "
            "lingered in the study air. All doors and windows to the manor were locked from the storm outside. "
            "The culprit is in the room."
        ),
        suspects=[
            Suspect(
                id="butler_arthur",
                name="Arthur Pendelton",
                role="The Head Butler",
                bio="Served the Blackwood family for 32 years. Meticulous, rigid, and intensely traditional.",
                personality="Dignified, courteous, slightly pedantic. Deeply protective of manor traditions.",
                alibi="Claims he was polishing the silver in the lower pantry between 22:00 and 23:00, then brought Reginald his nightly tea tray at 23:15.",
                secret="Owes £4,000 to an underground London gambling syndicate and pawned a manor silver teapot last week.",
                is_guilty=False,
            ),
            Suspect(
                id="heiress_beatrice",
                name="Beatrice Blackwood",
                role="The Estranged Niece & Heiress",
                bio="A bohemian sculptor residing in Paris, summoned home urgently by Reginald three days ago.",
                personality="Cynical, sharp-tongued, defiant, highly expressive under pressure.",
                alibi="Claims she was in the conservatory smoking Turkish cigarettes and sketching the gargoyles from 22:15 until she heard Arthur scream.",
                secret="Found out Reginald amended his will yesterday to disinherit her. She broke into his desk earlier that afternoon and attempted to burn the will amendment, but got interrupted.",
                is_guilty=False,
            ),
            Suspect(
                id="doctor_finch",
                name="Dr. Alistair Finch",
                role="The Personal Physician & Family Friend",
                bio="Longtime physician to the late Lady Blackwood and Lord Reginald. Renowned apothecary scholar.",
                personality="Nervous, overly formal, speaks in precise medical terminology, visibly sweating.",
                alibi="Claims he retired to the guest bedroom on the second floor at 21:45 to read a treatise on botanical sedatives.",
                secret="Lord Reginald had discovered that Dr. Finch falsified Lady Blackwood's autopsy three years ago to conceal a fatal morphine dosage error. Reginald gave Finch until morning to surrender his medical license.",
                is_guilty=True,
            ),
        ],
        clues=[
            Clue(
                id="clue_wolfsbane",
                title="Monkshood Residue in Crystal Glass",
                description="Forensic chemical traces of concentrated Aconitum napellus (Wolfsbane) confirmed in the dregs of Lord Reginald's port glass.",
                category="forensic",
                trigger_keywords=["port", "glass", "wine", "poison", "drink", "cup", "decanter", "toxicology"],
            ),
            Clue(
                id="clue_apothecary_ledger",
                title="Torn Apothecary Requisition Sheet",
                description="A slip from Finch's personal clinic in Leeds ordering 50ml of liquid Aconite extract, dated just 4 days ago.",
                category="physical",
                trigger_keywords=["medicine", "bag", "clinic", "prescription", "ledger", "dr", "doctor", "finch", "drugs", "supplies"],
            ),
            Clue(
                id="clue_blackmail_draft",
                title="Lord Reginald's Unsent Letter to the Medical Board",
                description="A signed memorandum in the desk blotter reporting Dr. Alistair Finch for gross negligence and malpractice in Lady Blackwood's passing.",
                category="testimonial",
                trigger_keywords=["letter", "desk", "will", "motive", "wife", "lady", "blackmail", "paper", "blotter", "malpractice"],
            ),
            Clue(
                id="clue_muddy_footprints",
                title="Size 9 Oxford Shoe Prints by the Conservatory",
                description="Traces of conservatory mud matching orthopedic soles used exclusively by Dr. Finch leading toward the study rear terrace.",
                category="physical",
                trigger_keywords=["shoes", "mud", "footprint", "conservatory", "terrace", "ground", "path", "floor"],
            ),
        ],
        true_culprit_id="doctor_finch",
        true_motive="Preventing Lord Reginald from submitting evidence of medical malpractice and murder to the British Medical Council.",
        true_weapon="Aconite (Wolfsbane) poison introduced into Lord Reginald's port wine.",
    )


def get_case_silicon_valley() -> MysteryDossier:
    """Case 2: The Terminal Bug at SynthCorp AI."""
    return MysteryDossier(
        case_id="case_silicon_valley",
        title="The Terminal Bug at SynthCorp AI",
        subtitle="San Francisco SoMa Server Facility, 2:00 AM",
        victim="Julian Vance (VP of Frontier AI Research)",
        crime_scene="Deep-Compute Server Hall 4B, SynthCorp Headquarters",
        time_of_death="01:15 AM, Friday morning",
        weapon_used="FM-200 Fire Suppression Gas forced deployment with manual door magnetic interlock override",
        synopsis=(
            "Julian Vance was discovered lifeless inside the cold aisle of Server Hall 4B. "
            "The fire suppression system discharged 400 lbs of clean agent gas, displacing all oxygen. "
            "The manual emergency abort lever was zip-tied shut from the outside. "
            "A billion-dollar Series C funding round closes at 9:00 AM."
        ),
        suspects=[
            Suspect(
                id="ceo_sterling",
                name="David Sterling",
                role="Founder & CEO",
                bio="Charismatic tech founder celebrated on Forbes 30 under 30. Obsessed with market valuation.",
                personality="Hyper-articulate, impatient, exudes venture-backed confidence, prone to aggressive deflection.",
                alibi="Claims he was on an overseas Zoom call with a sovereign wealth investor in Abu Dhabi from his penthouse between 00:30 and 02:00.",
                secret="Julian discovered that SynthCorp's flagship benchmark was evaluated on poisoned test data and leaked prompt caches. Julian refused to sign the investor deck and threatened to whistleblow at morning open.",
                is_guilty=True,
            ),
            Suspect(
                id="infra_maya",
                name="Maya Lin",
                role="Principal Infrastructure Engineer",
                bio="Maintains the GPU cluster. Known for running custom kernel patches to keep thermals under 70C.",
                personality="Blunt, caffeine-fueled, defensive about cluster uptime, skeptical of executive leadership.",
                alibi="Claims she was in the hardware lab soldering optical transceivers and monitoring Grafana alerts until 02:30.",
                secret="She secretly bypassed the building's thermal sensors last month to overclock the H100 clusters, which technically violated city fire codes.",
                is_guilty=False,
            ),
            Suspect(
                id="fde_tariq",
                name="Tariq Vance",
                role="Forward Deployed Engineer (and Julian's Brother)",
                bio="Deploys SynthCorp models to military and enterprise customers on-prem.",
                personality="Intense, quiet, loyal to engineering principles, holds deep grudges against corporate bureaucracy.",
                alibi="Claims he was in a shared Slack huddle troubleshooting an edge deployment in Singapore until 01:45.",
                secret="He had access to Julian's laptop and was quietly downloading the model weights to launch an open-source competitor.",
                is_guilty=False,
            ),
        ],
        clues=[
            Clue(
                id="clue_keycard_logs",
                title="Master Keycard Timestamp Log",
                description="Physical access badge #001 (assigned to CEO David Sterling) swiped into Server Hall 4B airlock at 01:08 AM.",
                category="forensic",
                trigger_keywords=["badge", "keycard", "log", "access", "door", "swipe", "rfid", "security", "time"],
            ),
            Clue(
                id="clue_audit_memo",
                title="Encrypted Whistleblower Dossier",
                description="Julian's uncommitted branch 'feature/expose_benchmark_fraud' documenting falsified MMLU & GSM8k metrics submitted to Series C VCs.",
                category="testimonial",
                trigger_keywords=["benchmark", "whistleblower", "fraud", "audit", "investor", "paper", "github", "commit", "metrics"],
            ),
            Clue(
                id="clue_ziptie",
                title="Industrial Carbon-Fiber Zip Tie",
                description="A rare orange fluoropolymer zip tie used to lock the FM-200 emergency abort handle; identical ties were shipped to Sterling's executive suite.",
                category="physical",
                trigger_keywords=["ziptie", "tie", "abort", "handle", "lever", "override", "gas", "fire", "orange"],
            ),
        ],
        true_culprit_id="ceo_sterling",
        true_motive="Silencing Julian to protect the $500M Series C valuation and conceal fraudulent model benchmarks.",
        true_weapon="FM-200 Fire Suppression Gas manual override and door lock.",
    )


def load_scenario(case_id: str = "case_blackwood") -> MysteryDossier:
    """Load a fresh mystery dossier by case ID."""
    if case_id == "case_silicon_valley":
        return get_case_silicon_valley()
    return get_case_blackwood()
