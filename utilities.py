
def sci_2_latex(value, fmt='.2e'):
    sci = (f'%{fmt}'%(value)).split('e')
    return f'{sci[0]} × 10^{{{sci[1]}}}'

