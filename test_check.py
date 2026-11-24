"""Auto-contrôle de check.py. Usage : python3 test_check.py (ou pytest)."""
import subprocess
import sys
import tempfile
from pathlib import Path

CHECK = Path(__file__).parent / 'sous-titres-en-fr' / 'check.py'
ALERTE = 'crédit supprimé ou modifié ?'
SANS_ERREUR = 'OK : aucune erreur'
REPLIQUE_EN = "1\n00:00:01,000 --> 00:00:02,000\nIt's fine.\n\n"
REPLIQUE_FR = "1\n00:00:01,000 --> 00:00:02,000\nÇa va.\n\n"


def bloc2(*lignes: str) -> str:
    return "2\n00:00:03,000 --> 00:00:05,000\n" + "\n".join(lignes) + "\n"


CREDIT = bloc2("Synced & corrected by -robtor-", "www.addic7ed.com")


def run_check(original: str, result: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        src, out = Path(tmp, 'a.srt'), Path(tmp, 'a_FR.srt')
        src.write_text(original, encoding='utf-8')
        out.write_text(result, encoding='utf-8')
        done = subprocess.run([sys.executable, str(CHECK), str(src), str(out)], capture_output=True, text=True)
        return done.stdout


def test_credit_supprime_est_signale() -> None:
    assert ALERTE in run_check(REPLIQUE_EN + CREDIT, REPLIQUE_FR)


def test_credit_traduit_est_signale() -> None:
    traduit = bloc2("Synchronisé et corrigé par -robtor-", "www.addic7ed.com")
    assert ALERTE in run_check(REPLIQUE_EN + CREDIT, REPLIQUE_FR + traduit)


def test_credit_conserve_ne_declenche_rien() -> None:
    assert SANS_ERREUR in run_check(REPLIQUE_EN + CREDIT, REPLIQUE_FR + CREDIT)


def test_credit_conserve_echappe_aux_autres_controles() -> None:
    credit = bloc2("- Translated by: Bob")  # tiret seul + « nom de locuteur ? » sur une réplique
    assert SANS_ERREUR in run_check(REPLIQUE_EN + credit, REPLIQUE_FR + credit)


def test_replique_avec_correct_by_n_est_pas_un_credit() -> None:
    original = REPLIQUE_EN + bloc2("That's correct, by the way.")
    assert SANS_ERREUR in run_check(original, REPLIQUE_FR + bloc2("C'est exact, au fait."))


PUB = bloc2("Advertise your product or brand here", "contact www.OpenSubtitles.org today")


def test_pub_supprimee_ne_declenche_rien() -> None:
    assert SANS_ERREUR in run_check(REPLIQUE_EN + PUB, REPLIQUE_FR)


def test_pub_conservee_est_signalee() -> None:
    assert 'publicité ?' in run_check(REPLIQUE_EN + PUB, REPLIQUE_FR + PUB)


if __name__ == '__main__':
    tests = [f for name, f in sorted(globals().items()) if name.startswith('test_')]
    failed = []
    for f in tests:
        try:
            f()
        except AssertionError:
            failed.append(f.__name__)
    print('\n'.join(f'ÉCHEC : {name}' for name in failed) or f'OK ({len(tests)} tests)')
    sys.exit(1 if failed else 0)
