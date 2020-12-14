import postscript as ps

def make_rotated_circle(angle, fill):
    return '\n'.join((ps.rotate(angle),
                      ps.text_in_cell(0, 0,
                                      4, 1,
                                      ps.Text(0.1, 0.1,
                                              '/LiberationSerif', 13,
                                              'Im text in a rect'),
                                      fill_value=fill)))

print(ps.translate(10, 10),
      ps.line(-10, 0,
              10, 0),
      ps.line(0, 10,
              0, -10),
      ps.for_loop(0, 1, 360,
                  make_rotated_circle,
                  {'angle' : 'index',
                   'fill' : 'index 0.0025 mul'}))
