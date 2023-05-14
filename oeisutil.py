def int_to_oeis_seq(n: int) -> str:
    seq_template = 'A000000'
    seq_id = str(n)
    seq_id = seq_template[:(len(seq_template) - len(seq_id))] + seq_id
    return seq_id