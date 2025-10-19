import numpy as np
import xlsxwriter
from sklearn.neural_network import MLPClassifier
from xlsxwriter.utility import xl_rowcol_to_cell

# ===================== Helpers =====================

def char_to_bits(ch: str):
    """Convert a character to 8 bits (MSB first)."""
    v = ord(ch)
    return np.array([(v >> i) & 1 for i in reversed(range(8))], dtype=int)

def build_char_model(correct_char, hidden=(8,), oversample=200):
    """Train an MLP that fires only for the correct character."""
    X, y = [], []
    correct_bits = char_to_bits(correct_char)
    for _ in range(oversample):
        X.append(correct_bits)
        y.append(1)
    for c in range(32, 127):
        if c == ord(correct_char):
            continue
        X.append(char_to_bits(chr(c)))
        y.append(0)
    X, y = np.array(X), np.array(y)
    clf = MLPClassifier(hidden_layer_sizes=hidden,
                        max_iter=2000, solver="lbfgs",
                        random_state=42)
    clf.fit(X, y)
    assert clf.predict([correct_bits])[0] == 1, f"Model failed for {correct_char}"
    return clf

def scale_weights(coefs, intercepts, scale=100):
    """Scale weights to ints for Excel stability."""
    W_scaled = [np.round(c*scale).astype(int) for c in coefs]
    b_scaled = [np.round(b*scale).astype(int) for b in intercepts]
    return W_scaled, b_scaled, scale

# ===================== Excel Writer =====================

def write_excel(flag: str, models, out_path="ExceLLM_charwise_fixed.xlsx"):
    N = len(flag)*8
    wb = xlsxwriter.Workbook(out_path)

    # MAIN
    main = wb.add_worksheet("MAIN")
    main.write("A1", "Enter flag:")
    main.write("A2", "Result:")
    main.write_formula("B2", '=IF(VERIFY!Z1=1,"✅ Correct","❌ Incorrect")')

    # BITS
    bits = wb.add_worksheet("BITS")
    for i in range(N):
        row = i + 2
        char_index = (i // 8) + 1
        bit_pos = 7 - (i % 8)
        formula = f"=MOD(QUOTIENT(IFERROR(CODE(MID(MAIN!B1,{char_index},1)),0),2^{bit_pos}),2)"
        bits.write_formula(row-1, 1, formula)
    bit_cells = [f"BITS!B{i+2}" for i in range(N)]

    # WEIGHTS
    wsh = wb.add_worksheet("WEIGHTS")
    model_refs = []
    row_ptr = 1

    for idx, clf in enumerate(models):
        W_scaled, b_scaled, scale = scale_weights(clf.coefs_, clf.intercepts_)

        refs = {}

        # W0 block (8 x hidden)
        W0_start = row_ptr
        for r in range(W_scaled[0].shape[0]):
            for c in range(W_scaled[0].shape[1]):
                wsh.write_number(row_ptr, c, int(W_scaled[0][r, c]))
            row_ptr += 1
        refs["W0"] = (W0_start, row_ptr-1, 0, W_scaled[0].shape[1]-1)

        # b0 block
        b0_start = row_ptr
        for val in b_scaled[0]:
            wsh.write_number(row_ptr, 0, int(val))
            row_ptr += 1
        refs["b0"] = (b0_start, row_ptr-1)

        # W1 block (hidden x 1)
        W1_start = row_ptr
        for r in range(W_scaled[1].shape[0]):
            wsh.write_number(row_ptr, 0, int(W_scaled[1][r, 0]))
            row_ptr += 1
        refs["W1"] = (W1_start, row_ptr-1)

        # b1
        b1_row = row_ptr
        wsh.write_number(b1_row, 0, int(b_scaled[1][0]))
        refs["b1"] = b1_row
        row_ptr += 2  # gap

        refs["scale"] = scale
        model_refs.append(refs)

    # VERIFY
    ver = wb.add_worksheet("VERIFY")
    char_outputs = []

    for idx, refs in enumerate(model_refs):
        start_bit = idx*8
        inputs_range = f"BITS!B{start_bit+2}:B{start_bit+9}"

        # Hidden layer neurons
        hidden_cells = []
        W0_start, W0_end, _, hidden_dim = refs["W0"]
        for h in range(hidden_dim+1):
            weights_range = f"WEIGHTS!A{W0_start+1+0+ h*0}:A{W0_end+1}"  # placeholder
        # Actually iterate columns properly
        for h in range(model_refs[idx]["W0"][3]+1):  # number of hidden neurons
            W0_start, W0_end, c0, c1 = refs["W0"]
            # Column h in W0
            col_letter = xlsxwriter.utility.xl_col_to_name(h)
            weights_range = f"WEIGHTS!{col_letter}{W0_start+1}:{col_letter}{W0_end+1}"
            b0_row = refs["b0"][0] + h
            bias_ref = f"WEIGHTS!A{b0_row+1}"
            expr = f"(SUMPRODUCT({inputs_range},{weights_range})+{bias_ref})/{refs['scale']}"
            outcell = f"C{10+idx*20+h}"
            ver.write_formula(outcell, f"=MAX(0,{expr})")
            hidden_cells.append(outcell)

        # Output neuron
        W1_start, W1_end = refs["W1"]
        weights_range = f"WEIGHTS!A{W1_start+1}:A{W1_end+1}"
        hidden_range = f"{hidden_cells[0]}:{hidden_cells[-1]}"
        bias_ref = f"WEIGHTS!A{refs['b1']+1}"
        expr = f"(SUMPRODUCT({hidden_range},{weights_range})+{bias_ref})/{refs['scale']}"
        outcell = f"H{10+idx*20}"
        ver.write_formula(outcell, f"=--({expr}>0)")
        char_outputs.append(outcell)

    # Final check
    ver.write_formula("Z1", f"=--(SUM({','.join(char_outputs)})={len(flag)})")

    wb.close()
    return out_path

# ===================== Main =====================

if __name__ == "__main__":
    flag = "sun{n0t_qu1t3_ch4t_GPT_l0l}"
    models = [build_char_model(ch) for ch in flag]
    path = write_excel(flag, models)
    print(f"[+] Wrote {path}")
