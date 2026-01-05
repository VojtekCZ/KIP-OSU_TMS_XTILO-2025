# 3‑Tape Deterministic Turing Machine — Binary Product

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

This project implements a **deterministic 3‑tape Turing machine simulator in Python**. The machine calculates the product of a sequence of **binary numbers** separated by the epsilon symbol `#`.

The mathematical function implemented is:

$$
\text{fun}(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} x_i
$$

Where each $x_i$ is a binary number.

---

## 🏗️ Architecture & Logic

This simulator uses a multi-tape approach to handle arithmetic operations efficiently without destroying the input immediately.

### Tapes Overview
| Tape | Name | Role |
| :--- | :--- | :--- |
| **Tape 1** | **Input** | Holds the sequence of binary numbers (read-only until processed). |
| **Tape 2** | **Accumulator** | Stores the progressively computed product. |
| **Tape 3** | **Workspace** | Scratchpad used during addition and multiplication operations. |

### Alphabet
The machine operates on the following set of symbols:
* `{ '0', '1' }`: Binary digits.
* `#`: Separator between numbers (epsilon).
* `_`: Blank symbol (represented as `_` in logic, but acts as empty space).

---

## ⚙️ States and Transitions

The machine uses 11 distinct states to control the flow, from reading input to complex multiplication logic (shift-and-add).

### State Definitions

| State | Role | Description |
| :--- | :--- | :--- |
| **q0** | Init | Initialization and search for the first number. |
| **q1** | Copy | Copies the first number from Tape 1 to Tape 2. |
| **q2** | End Check | Detects the end of the second number. |
| **q3** | Decision | Decides based on the digit (0 or 1) and routes logic. |
| **q4** | Shift | Multiplies the number on Tape 2 by two (bit shift). |
| **q5** | Append | Appends `0` at the end of the number on Tape 2. |
| **q6** | Restore | Copies result from Tape 3 back to Tape 2. |
| **q7** | Next Num | Detects end of Tape 2 and moves to the next number on Tape 1. |
| **q8** | Sum | Performs addition: Tape 2 + Tape 3 (formerly START). |
| **q9** | Carry | Handles addition with carry bit (formerly CARRY). |
| **q10** | **Halt** | Final state. Computation is finished. |

### Transition Rules Format
The rules are defined in the code as tuples:

```python
(current_state, read_t1, read_t2, read_t3) = (next_state, write_t1, write_t2, write_t3, move_t1, move_t2, move_t3)
```

Where movement operations are:

L: Left

R: Right

S: Stay

🚀 How to Run
Prerequisites
Python 3.8 or higher.

Running the Simulator
Simply run the script in your terminal:
```bash
TM_XTILO.py
```

Configuration
You can toggle the verbose mode in the run() function:

verbose=True: Shows a detailed step-by-step visualization, including the tape contents and the head position (/\) for every step.

verbose=False: Shows only the start and end snapshots.

📝 Usage & Input
To calculate a different product, you need to edit the Tape 1 initialization in the __main__ block of the script.

Input Format
Numbers must be binary (0, 1) and separated by #. The tape should be padded with blanks or hashes as needed.

Example Code Modification:
```python
BLANK = "_"

# Edit Tape 1 here (Example: 2 * 2 * 2 in binary is 10 * 10 * 10)
# Input sequence: # # 1 0 # 1 0 # 1 0 # #
tape1 = Tape(["#", "#", "1", "0", "#", "1", "0", "#", "1", "0", "#", "#"])
tape2 = Tape([BLANK])
tape3 = Tape([BLANK])

machine = Machine(
    rules=rules,
    tapes=[tape1, tape2, tape3],
    heads=[0, 0, 0],
    currentState=q0
)
```

📊 Example OutputInput: $10_2 \times 10_2 \times 10_2$ (Decimal: $2 \times 2 \times 2 = 8$)Console Output (Verbose):
```Plaintext
Start state: q0
tape1: #  #  1  0  #  1  0  #  1  0  #  #
       /\  (head=0)
tape2: _
       /\  (head=0)
tape3: _
       /\  (head=0)

... [Hundreds of steps omitted] ...

End state: q10 (steps=NNN)

Final result on Tape 2:
Product: 1000
```
(Binary 1000 is 8 in decimal)

⚖️ License & References
License: MIT License — Free to use and modify for academic and personal purposes.

Original Concept: Rezigned — Turing Machine Overview.
