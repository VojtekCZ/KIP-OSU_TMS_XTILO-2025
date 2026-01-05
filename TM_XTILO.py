from dataclasses import dataclass
from typing import List, Tuple, Optional

# === Data structures for the 3-tape TM ===

@dataclass(frozen=True)
class State:
    name: str
    start: bool = False
    end: bool = False

@dataclass
class Tape:
    symbols: List[str]  # e.g., ["1", "0", "0", "1", "0"]

@dataclass(frozen=True)
class Rule:
    currentState: State
    readSymbols: Tuple[str, str, str]      # (tape1, tape2, tape3)
    nextState: State
    writeSymbols: Tuple[str, str, str]     # (tape1, tape2, tape3)
    operations: Tuple[str, str, str]       # each of {'R', 'L', 'S'}

@dataclass
class Machine:
    rules: List[Rule]
    tapes: List[Tape]                       # 3 tapes
    heads: List[int]                        # 3 head positions
    currentState: State                     # current state


# === Blank symbol used across the machine ===
BLANK = "_"


# === State definitions (with requested renaming and roles in comments) ===
q0  = State("q0", start=True)      # q0: init and search first number
q1  = State("q1")                  # q1: copy the first number to the second tape
q2  = State("q2")                  # q2: detect end of the second number
q3  = State("q3")                  # q3: decide if it is 0 or 1 and route accordingly
q4  = State("q4")                  # q4: multiply the number on tape 2 by two
q5  = State("q5")                  # q5: append 0 at the end of the number on tape 2
q6  = State("q6")                  # q6: copy result of tape 3 back to tape 2
q7  = State("q7")                  # q7: detect end of tape 2 and next number on tape 1
q8  = State("q8")                  # q8: sum of tape 2 + tape 3 (START)
q9  = State("q9")                  # q9: sum with carry (CARRY)
q10 = State("q10", end=True)       # q10: halt (HALT)


# === Rules ===
rules: List[Rule] = [

    # q0: init and search first number
    Rule(q0,    ("#", BLANK, BLANK),   q0,    (BLANK, BLANK, BLANK),   ("R", "S", "S")),
    Rule(q0,    ("0", BLANK, BLANK),   q1,    ("0", "#",   BLANK),     ("S", "R", "S")),
    Rule(q0,    ("1", BLANK, BLANK),   q1,    ("1", "#",   BLANK),     ("S", "R", "S")),
    Rule(q0,    (BLANK, BLANK, BLANK), q10,   (BLANK, BLANK, BLANK),   ("S", "S", "S")),

    # q1: copy the first number to the second tape
    Rule(q1,    ("#", BLANK, BLANK),   q2,    ("#", BLANK, BLANK),     ("R", "S", "S")),
    Rule(q1,    ("0", BLANK, BLANK),   q1,    (BLANK, "0",  BLANK),    ("R", "R", "S")),
    Rule(q1,    ("1", BLANK, BLANK),   q1,    (BLANK, "1",  BLANK),    ("R", "R", "S")),
    Rule(q1,    (BLANK, BLANK, BLANK), q10,   (BLANK, BLANK, BLANK),   ("S", "S", "S")),

    # q2: detect end of the second number
    Rule(q2,    ("#", BLANK, BLANK),   q3,    ("#", BLANK, BLANK),     ("L", "S", "S")),
    Rule(q2,    ("#", "0",    BLANK),  q3,    ("#", "0",    BLANK),    ("L", "R", "S")),
    Rule(q2,    ("#", "1",    BLANK),  q3,    ("#", "1",    BLANK),    ("L", "R", "S")),
    Rule(q2,    ("0", BLANK, BLANK),   q2,    ("0", BLANK, BLANK),     ("R", "S", "S")),
    Rule(q2,    ("1", BLANK, BLANK),   q2,    ("1", BLANK, BLANK),     ("R", "S", "S")),
    Rule(q2,    (BLANK, BLANK, BLANK), q10,   (BLANK, BLANK, BLANK),   ("S", "S", "S")),

    # q3: decide whether it is 0 or 1 and route accordingly (to q8, q5, or q6)
    Rule(q3,    ("1", BLANK, BLANK),   q8,    ("1", BLANK, BLANK),     ("S", "L", "L")),
    Rule(q3,    ("0", BLANK, BLANK),   q5,    ("0", BLANK, BLANK),     ("S", "S", "S")),
    Rule(q3,    ("#", BLANK, BLANK),   q6,    ("#", BLANK, BLANK),     ("S", "L", "L")),

    # q4: multiply the number on tape 2 by two
    Rule(q4,    ("1", BLANK, BLANK),   q3,    ("#", "0",   BLANK),     ("L", "R", "S")),
    Rule(q4,    ("1", BLANK, "0"),     q4,    ("1", "0",   "0"),       ("S", "R", "R")),
    Rule(q4,    ("1", BLANK, "1"),     q4,    ("1", "0",   "1"),       ("S", "R", "R")),
    Rule(q4,    ("1", "#",   BLANK),   q4,    ("1", "#",   BLANK),     ("S", "R", "S")),
    Rule(q4,    ("1", "0",   BLANK),   q4,    ("1", "0",   BLANK),     ("S", "R", "S")),
    Rule(q4,    ("1", "1",   BLANK),   q4,    ("1", "1",   BLANK),     ("S", "R", "S")),
    Rule(q4,    ("1", "1",   "0"),     q4,    ("1", "1",   "0"),       ("S", "R", "R")),
    Rule(q4,    ("1", "1",   "1"),     q4,    ("1", "1",   "1"),       ("S", "R", "R")),
    Rule(q4,    ("1", "#",   "0"),     q4,    ("1", "#",   "0"),       ("S", "R", "R")),
    Rule(q4,    ("1", "#",   "1"),     q4,    ("1", "#",   "1"),       ("S", "R", "R")),
    Rule(q4,    ("1", "0",   "0"),     q4,    ("1", "0",   "0"),       ("S", "R", "R")),
    Rule(q4,    ("1", "0",   "1"),     q4,    ("1", "0",   "1"),       ("S", "R", "R")),

    # q5: append 0 at the end of the number on tape 2
    Rule(q5,    ("0", BLANK, BLANK),   q3,    ("#", "0",   BLANK),     ("L", "R", "S")),

    # q6: copy result of tape 3 back to tape 2
    Rule(q6,    ("#", "0",   "0"),     q6,    ("#", "0",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "1",   "0"),     q6,    ("#", "0",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "0",   "1"),     q6,    ("#", "1",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "1",   "1"),     q6,    ("#", "1",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "#",   "0"),     q6,    ("#", "0",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "#",   BLANK),   q6,    ("#", BLANK, BLANK),     ("S", "L", "S")),
    Rule(q6,    ("#", "#",   "1"),     q6,    ("#", "1",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", BLANK, "0"),     q6,    ("#", "0",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", BLANK, "1"),     q6,    ("#", "1",   BLANK),     ("S", "L", "L")),
    Rule(q6,    ("#", "0",   BLANK),   q6,    ("#", BLANK, BLANK),     ("S", "L", "S")),
    Rule(q6,    ("#", "1",   BLANK),   q6,    ("#", BLANK, BLANK),     ("S", "L", "S")),
    Rule(q6,    ("#", BLANK, BLANK),   q7,    ("#", BLANK, BLANK),     ("S", "R", "S")),

    # q7: detect end of tape 2 and next number on tape 1
    Rule(q7,    ("#", BLANK, BLANK),   q7,    ("#", BLANK, BLANK),     ("R", "R", "S")),
    Rule(q7,    ("#", "0",   BLANK),   q7,    ("#", "0",   BLANK),     ("R", "R", "S")),
    Rule(q7,    ("#", "1",   BLANK),   q7,    ("#", "1",   BLANK),     ("R", "R", "S")),
    Rule(q7,    ("0", "0",   BLANK),   q7,    ("0", "0",   BLANK),     ("S", "R", "S")),
    Rule(q7,    ("0", "1",   BLANK),   q7,    ("0", "1",   BLANK),     ("S", "R", "S")),
    Rule(q7,    ("1", "0",   BLANK),   q7,    ("1", "0",   BLANK),     ("S", "R", "S")),
    Rule(q7,    ("1", "1",   BLANK),   q7,    ("1", "1",   BLANK),     ("S", "R", "S")),
    Rule(q7,    ("0", BLANK, BLANK),   q2,    ("0", BLANK, BLANK),     ("S", "S", "S")),
    Rule(q7,    ("1", BLANK, BLANK),   q2,    ("1", BLANK, BLANK),     ("S", "S", "S")),
    Rule(q7,    (BLANK, "0", BLANK),   q7,    (BLANK, "0", BLANK),     ("S", "R", "S")),
    Rule(q7,    (BLANK, "1", BLANK),   q7,    (BLANK, "1", BLANK),     ("S", "R", "S")),
    Rule(q7,    (BLANK, BLANK, BLANK), q10,   (BLANK, BLANK, BLANK),   ("S", "S", "S")),

    # q8: sum of tape 2 + tape 3  (START)
    Rule(q8,    ("1", "1",   "1"),     q9,    ("1", "1",   "0"),       ("S", "L", "L")),  # 1+1=0 with carry
    Rule(q8,    ("1", "1",   "0"),     q8,    ("1", "1",   "1"),       ("S", "L", "L")),  # 1+0=1 no carry
    Rule(q8,    ("1", "0",   "1"),     q8,    ("1", "0",   "1"),       ("S", "L", "L")),  # 0+1=1 no carry
    Rule(q8,    ("1", "0",   "0"),     q8,    ("1", "0",   "0"),       ("S", "L", "L")),  # 0+0=0 no carry
    Rule(q8,    ("1", "1",   BLANK),   q8,    ("1", "1",   "1"),       ("S", "L", "L")),  # 1+blank=1
    Rule(q8,    ("1", BLANK, "1"),     q8,    ("1", BLANK, "1"),       ("S", "S", "L")),  # blank+1=1
    Rule(q8,    ("1", "0",   BLANK),   q8,    ("1", "0",   "0"),       ("S", "L", "L")),  # 0+blank=0
    Rule(q8,    ("1", BLANK, "0"),     q8,    ("1", BLANK, "0"),       ("S", "S", "L")),  # blank+0=0
    Rule(q8,    ("1", "#",   BLANK),   q4,    ("1", "#",   BLANK),     ("S", "S", "R")),  # #+blank=_
    Rule(q8,    ("1", "#",   "1"),     q8,    ("1", "#",   "1"),       ("S", "S", "L")),  # #+1=1
    Rule(q8,    ("1", "#",   "0"),     q8,    ("1", "#",   "0"),       ("S", "S", "L")),  # #+0=0
    Rule(q8,    ("1", BLANK, BLANK),   q4,    ("1", BLANK, BLANK),     ("S", "R", "R")),  # All done

    # q9: sum with carry  (CARRY)
    Rule(q9,    ("1", "1",   "1"),     q9,    ("1", "1",   "1"),       ("S", "L", "L")),  # 1+1+carry=1 with carry
    Rule(q9,    ("1", "1",   "0"),     q9,    ("1", "1",   "0"),       ("S", "L", "L")),  # 1+0+carry=0 with carry
    Rule(q9,    ("1", "0",   "1"),     q9,    ("1", "0",   "0"),       ("S", "L", "L")),  # 0+1+carry=0 with carry
    Rule(q9,    ("1", "0",   "0"),     q8,    ("1", "0",   "1"),       ("S", "L", "L")),  # 0+0+carry=1 no carry
    Rule(q9,    ("1", "1",   BLANK),   q9,    ("1", "1",   "0"),       ("S", "L", "L")),  # 1+blank+carry=0 with carry
    Rule(q9,    ("1", BLANK, "1"),     q9,    ("1", BLANK, "0"),       ("S", "S", "L")),  # blank+1+carry=0 with carry
    Rule(q9,    ("1", "#",   "1"),     q9,    ("1", "#",   "0"),       ("S", "S", "L")),  # # treated like blank on tape2
    Rule(q9,    ("1", "0",   BLANK),   q8,    ("1", "0",   "1"),       ("S", "L", "L")),  # 0+blank+carry=1 no carry
    Rule(q9,    ("1", BLANK, "0"),     q8,    ("1", BLANK, "1"),       ("S", "S", "L")),  # blank+0+carry=1 no carry
    Rule(q9,    ("1", "#",   "0"),     q8,    ("1", "#",   "1"),       ("S", "S", "L")),  # # treated like blank on tape2
    Rule(q9,    ("1", BLANK, BLANK),   q4,    ("1", BLANK, "1"),       ("S", "S", "R")),  # Just carry remaining
    Rule(q9,    ("1", "#",   BLANK),   q4,    ("1", "#",   "1"),       ("S", "S", "R")),  # Just carry remaining
]


# === Simulation helpers ===

def read_symbol(tape: Tape, head: int) -> str:
    """Return symbol under head; off-range => BLANK."""
    if head < 0 or head >= len(tape.symbols):
        return BLANK
    return tape.symbols[head]

def write_symbol(tape: Tape, heads: List[int], i: int, sym: str) -> None:
    """Write symbol to tape i; extends tape if needed."""
    head = heads[i]
    # extend left (infinite tape)
    if head < 0:
        missing = -head
        tape.symbols = [BLANK] * missing + tape.symbols
        head = 0
        heads[i] = head
    # extend right
    if head >= len(tape.symbols):
        tape.symbols.extend([BLANK] * (head - len(tape.symbols) + 1))
    tape.symbols[head] = sym

def move_head(heads: List[int], i: int, op: str) -> None:
    if op == "L":
        heads[i] -= 1
    elif op == "R":
        heads[i] += 1
    # "S" => no change

def find_rule(rules: List[Rule], state: State, triple: Tuple[str, str, str]) -> Optional[Rule]:
    for r in rules:
        if r.currentState == state and r.readSymbols == triple:
            return r
    return None


# === Single TM step ===
def step(machine: Machine) -> bool:
    """Perform one step of the machine. Returns True if progressed, False otherwise."""
    if machine.currentState.end:
        return False
    s1 = read_symbol(machine.tapes[0], machine.heads[0])
    s2 = read_symbol(machine.tapes[1], machine.heads[1])
    s3 = read_symbol(machine.tapes[2], machine.heads[2])
    rule = find_rule(machine.rules, machine.currentState, (s1, s2, s3))
    if rule is None:
        return False

    # write
    write_symbol(machine.tapes[0], machine.heads, 0, rule.writeSymbols[0])
    write_symbol(machine.tapes[1], machine.heads, 1, rule.writeSymbols[1])
    write_symbol(machine.tapes[2], machine.heads, 2, rule.writeSymbols[2])

    # move heads
    move_head(machine.heads, 0, rule.operations[0])
    move_head(machine.heads, 1, rule.operations[1])
    move_head(machine.heads, 2, rule.operations[2])

    # transition
    machine.currentState = rule.nextState
    return True


# === Pretty printing (optional verbose visualization) ===

def rule_str(rule: Rule) -> str:
    cs = rule.currentState.name
    ns = rule.nextState.name
    r  = rule.readSymbols
    w  = rule.writeSymbols
    ops = rule.operations
    return (f"{cs} -> {ns} | read=({r[0]},{r[1]},{r[2]}) "
            f"write=({w[0]},{w[1]},{w[2]}) ops=({ops[0]},{ops[1]},{ops[2]})")

def render_tape(tape: Tape, head: int, label: str = "tape") -> str:
    """
    Render a tape with fixed-width cells and a caret '/\\' under the head.
    This does not alter tape content; it's purely visual.
    """
    cell = 3  # width per cell for single-char symbols ('#','0','1','_')
    if len(tape.symbols) == 0:
        line = "(empty)"
        return f"{label}: {line}"

    line = "".join(f"{s:^{cell}}" for s in tape.symbols)

    # clamp caret to tape bounds for visualization
    idx = head
    if idx < 0:
        idx = 0
    elif idx >= len(tape.symbols):
        idx = len(tape.symbols) - 1
    caret_pos = idx * cell + (cell // 2)

    caret_line = " " * caret_pos + "/\\"
    return f"{label}: {line}\n       {caret_line}  (head={head})"

def print_machine_snapshot(machine: Machine, step_idx: int, rule_text: str) -> None:
    print(f"\nStep {step_idx}: state={machine.currentState.name}")
    print(f"  rule: {rule_text}")
    print(render_tape(machine.tapes[0], machine.heads[0], label="tape1"))
    print(render_tape(machine.tapes[1], machine.heads[1], label="tape2"))
    print(render_tape(machine.tapes[2], machine.heads[2], label="tape3"))
    print(f"  heads: {machine.heads}")

def run(machine: Machine, max_steps: int = 100000, verbose: bool = True) -> State:
    """Run the machine; print start state/tapes, each step (if verbose), and end state."""
    # initial snapshot
    print(f"Start state: {machine.currentState.name}")
    print(render_tape(machine.tapes[0], machine.heads[0], label="tape1"))
    print(render_tape(machine.tapes[1], machine.heads[1], label="tape2"))
    print(render_tape(machine.tapes[2], machine.heads[2], label="tape3"))
    print(f"heads: {machine.heads}")

    steps = 0
    while steps < max_steps and not machine.currentState.end:
        s1 = read_symbol(machine.tapes[0], machine.heads[0])
        s2 = read_symbol(machine.tapes[1], machine.heads[1])
        s3 = read_symbol(machine.tapes[2], machine.heads[2])
        rule = find_rule(machine.rules, machine.currentState, (s1, s2, s3))
        if rule is None:
            print("\nNo matching rule — machine halts.")
            break

        if verbose:
            print_machine_snapshot(machine, steps, rule_str(rule))

        progressed = step(machine)
        if not progressed:
            break
        steps += 1

    # final snapshot
    print(f"\nEnd state: {machine.currentState.name} (steps={steps})")
    print(render_tape(machine.tapes[0], machine.heads[0], label="tape1"))
    print(render_tape(machine.tapes[1], machine.heads[1], label="tape2"))
    print(render_tape(machine.tapes[2], machine.heads[2], label="tape3"))
    print(f"heads: {machine.heads}")
    return machine.currentState


# === Example initialization (kept as per your latest snippet) ===
if __name__ == "__main__":
    tape1 = Tape(["#", "#", "1", "0", "1", "#", "1", "0", "0", "1", "#", "1", "0", "1", "#", "1", "0", "0", "1","#", "#"])
    tape2 = Tape([BLANK])
    tape3 = Tape([BLANK])

    machine = Machine(
        rules=rules,
        tapes=[tape1, tape2, tape3],
        heads=[0, 0, 0],   # initial head positions
        currentState=q0    # initial state
    )

    # Run with verbose visualization (set verbose=False to print only start/end)
    final_state = run(machine, verbose=False)
