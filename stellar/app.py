"""Demo CLI: simula la puntería sobre la secuencia secreta."""
from stellar.catalog.repo import Repo
from stellar.engine.state_machine import StateMachine
from stellar.seed import build_demo
from stellar.ui.guide import render_guide
from stellar.ui.reveal import reveal_frames


def main():
    con, ev, seq = build_demo()
    repo = Repo(con)
    sm = StateMachine(repo, ev)
    t = 0.0
    pointing = [repo.star(i) for i in seq] + [repo.star_by_name("Sirius")]
    for s in pointing:
        print(render_guide(repo, sm.node_id, len(sm.buffer)), "\n")
        for _ in range(3):
            sm.feed(s["ra_deg"], s["dec_deg"], t)
            t += 0.8
    if sm.revealed:
        for f in reveal_frames(sm.revealed["data"].decode()):
            last = f
        print(last["text"])


if __name__ == "__main__":
    main()
