#!/usr/bin/env python
"""Fetch ATLAS exclusion contours from HEPData and save as CSV.

Downloads YAML tables for:
- SUSY-2019-09 (compressed EWKino: Wino-bino and Higgsino)
- SUSY-2018-32 (direct sleptons)
- Stop pair (all-hadronic tt+MET)

Saves parsed (x, y) arrays to results/atlas_contours/.
"""

import os
import csv
import urllib.request

import yaml

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT_DIR = os.path.join(PROJECT_ROOT, 'results', 'atlas_contours')
os.makedirs(OUT_DIR, exist_ok=True)

HEPDATA_BASE = 'https://www.hepdata.net/download/table'

# Table definitions: (inspire_id, table_name, output_csv, transform_fn_name)
TABLES = [
    # SUSY-2019-09: Wino-bino (m_parent vs m_LSP plane)
    ('ins1866951', 'Fig 16a WZ Exclusion: Wino-bino(+), Obs',
     'susy2019_09_wino_obs.csv', 'wino_bino'),
    ('ins1866951', 'Fig 16a WZ Exclusion: Wino-bino(+), Exp',
     'susy2019_09_wino_exp.csv', 'wino_bino'),
    # SUSY-2019-09: Higgsino (m_chi20 vs Δm plane)
    ('ins1866951', 'Fig 16d WZ Exclusion: Higgsino ($\\Delta m$), Obs',
     'susy2019_09_higgsino_obs.csv', 'higgsino_dm'),
    ('ins1866951', 'Fig 16d WZ Exclusion: Higgsino ($\\Delta m$), Exp',
     'susy2019_09_higgsino_exp.csv', 'higgsino_dm'),
    # SUSY-2018-32: direct sleptons (m_slepton vs m_chi10)
    ('ins1750597', 'Exclusion contour (obs) 3',
     'susy2018_32_slepton_obs.csv', 'slepton'),
    ('ins1750597', 'Exclusion contour (exp) 3',
     'susy2018_32_slepton_exp.csv', 'slepton'),
    # Stop pair (m_stop vs m_chi10)
    ('ins1793461', 'stop_obs',
     'stop_hadronic_obs.csv', 'stop'),
    ('ins1793461', 'stop_exp',
     'stop_hadronic_exp.csv', 'stop'),
]


def fetch_yaml(inspire_id, table_name):
    """Download a HEPData YAML table and return parsed dict."""
    url = f'{HEPDATA_BASE}/{inspire_id}/{urllib.request.quote(table_name)}/yaml'
    print(f'  Fetching: {url}')
    req = urllib.request.Request(url, headers={'User-Agent': 'SUSY_agent/1.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = yaml.safe_load(resp.read())
    return data


def extract_xy(data):
    """Extract (x_values, y_values) from HEPData YAML structure."""
    indep = data['independent_variables'][0]['values']
    dep = data['dependent_variables'][0]['values']
    x_vals = [v['value'] for v in indep]
    y_vals = [v['value'] for v in dep]
    return x_vals, y_vals


def transform_wino_bino(x_raw, y_raw):
    """Wino-bino: raw axes are (m_parent=m_chi1pm/chi20, m_LSP=m_chi10).
    Our EWKino plot: x=m_chi10, y=m_chi1pm. So swap."""
    return y_raw, x_raw  # m_chi10, m_chi1pm


def transform_higgsino_dm(x_raw, y_raw):
    """Higgsino: raw axes are (m_chi20, Δm).
    Convert: m_chi10 = m_chi20 - Δm, m_chi1pm ≈ m_chi20.
    Our EWKino plot: x=m_chi10, y=m_chi1pm."""
    m_chi10 = [x - y for x, y in zip(x_raw, y_raw)]
    m_chi1pm = list(x_raw)  # m_chi20 ≈ m_chi1pm for Higgsinos
    return m_chi10, m_chi1pm


def transform_slepton(x_raw, y_raw):
    """Slepton: raw axes are (m_slepton, m_chi10).
    Our plot: x=m_chi10, y=m_slepton. So swap."""
    return y_raw, x_raw


def transform_stop(x_raw, y_raw):
    """Stop: raw axes are (m_stop, m_chi10).
    Our plot: x=m_chi10, y=m_stop. So swap."""
    return y_raw, x_raw


TRANSFORMS = {
    'wino_bino': transform_wino_bino,
    'higgsino_dm': transform_higgsino_dm,
    'slepton': transform_slepton,
    'stop': transform_stop,
}


def write_csv(filepath, x_vals, y_vals, x_label='x', y_label='y'):
    """Write 2-column CSV."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([x_label, y_label])
        for x, y in zip(x_vals, y_vals):
            writer.writerow([f'{x:.4f}', f'{y:.4f}'])


def main():
    print('=' * 60)
    print('ATLAS Exclusion Contour Fetcher (HEPData)')
    print('=' * 60)

    for inspire_id, table_name, out_csv, transform_name in TABLES:
        print(f'\n[{out_csv}]')
        try:
            data = fetch_yaml(inspire_id, table_name)
            x_raw, y_raw = extract_xy(data)
            transform_fn = TRANSFORMS[transform_name]
            x_out, y_out = transform_fn(x_raw, y_raw)

            # Determine column labels based on transform
            if transform_name in ('wino_bino', 'higgsino_dm'):
                labels = ('m_chi10', 'm_chi1pm')
            elif transform_name == 'slepton':
                labels = ('m_chi10', 'm_slepton')
            elif transform_name == 'stop':
                labels = ('m_chi10', 'm_stop')
            else:
                labels = ('x', 'y')

            out_path = os.path.join(OUT_DIR, out_csv)
            write_csv(out_path, x_out, y_out, *labels)
            print(f'  -> {len(x_out)} points saved to {out_csv}')

        except Exception as e:
            print(f'  ERROR: {e}')

    print(f'\nAll contours saved to {OUT_DIR}/')
    print('Done.')


if __name__ == '__main__':
    main()
