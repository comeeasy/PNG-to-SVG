import numpy as np
from svgpathtools import svg2paths, wsvg
import svgpathtools as svg
import os
import glob
from tqdm import tqdm

def bazier2line(bazier_svg, num_of_segments=10):
    paths, _ = svg2paths(bazier_svg)
    
    new_paths = []
    for path in paths:
        new_paths_raw = svg.Path()
        for stroke in path:
            if isinstance(stroke, svg.path.CubicBezier):
                bazier = stroke
                
                P0 = np.array((bazier.start.real, bazier.start.imag))
                P1 = np.array((bazier.control1.real, bazier.control1.imag))
                P2 = np.array((bazier.control2.real, bazier.control2.imag))
                P3 = np.array((bazier.end.real, bazier.end.imag))

                cur_pos = P0
                for t in np.linspace(0., 1., num_of_segments + 1):
                    next_pos = np.power((1-t), 3)*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3
                    new_paths_raw.append(svg.Line(complex(cur_pos[0], cur_pos[1]), complex(next_pos[0], next_pos[1])))
                    
                    cur_pos = next_pos
            else:
                new_paths_raw.append(stroke)
            
        new_paths.append(new_paths_raw)
    return new_paths

def purify(strokes):
    data = []
    for seq in strokes:
        if len(seq[:, 0]) <= 38000 and len(seq[:, 0]) > 10:
            seq = np.minimum(seq, 1000)
        seq = np.maximum(seq, -1000)
        seq = np.array(seq, dtype = np.float32)
        data.append(seq)
    return data

def calculate_normalizing_scale_factor(strokes):
    """Calculate the normalizing factor explained in appendix of sketch-rnn."""
    data = []
    for i in range(len(strokes)):
        for j in range(len(strokes[i])):
            data.append(strokes[i][j, 0])
            data.append(strokes[i][j, 1])
    data = np.array(data)
    return np.std(data)

def normalize(strokes):
    """Normalize entire dataset (delta_x, delta_y) by the scaling factor."""
    data = []
    # scale_factor = calculate_normalizing_scale_factor(strokes)
    
    # to range it into [-1, 1] find max length
    scale_factor = np.max(np.abs(strokes))
    
    for seq in strokes:
        seq[:, 0:2] /= scale_factor
        data.append(seq)
    return data

def max_size(strokes):
    """larger sequence length in the data set"""
    sizes = [len(seq) for seq in strokes]
    return max(sizes)