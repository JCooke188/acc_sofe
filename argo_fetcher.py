"""
Grabs Argo float data from the euro argo database using argopy
Saves the data to a netcdf file for later use

Author: Justin Cooke

Usage:
    python argo_fetcher.py \
        --bbox 140 160 -60 -50 \
        --depth-range 0 2000 \
        --start-date 2011-01 \
        --end-date 2026-10 \
        --output-dir /path/to/out \
        --array-dim [1d 2d] 
"""

from __future__ import annotations

import argparse
import logging
import time

from datetime import datetime, timezone
from pathlib import Path

import argopy
from argopy.errors import DataNotFound

LOG = logging.getLogger('floats')

MAX_ATTEMPTS = 3

def format_coord(value, is_lat=True):
    """Format a coordinate with direction suffix."""
    direction = ('S' if value < 0 else 'N') if is_lat else ('W' if value < 0 else 'E')
    return f"{abs(value)}{direction}"

def main():
    parser = argparse.ArgumentParser(description='Download Argo float data for spice variance anomaly analysis')
    parser.add_argument('--bbox',required=True,type=float,nargs=4,metavar=('LON_MIN','LON_MAX','LAT_MIN','LAT_MAX'))
    parser.add_argument('--depth-range',required=True,type=float,nargs=2,metavar=('DPTH_MIN','DPTH_MAX'))
    parser.add_argument('--start-date',required=True)
    parser.add_argument('--end-date',required=True)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--array-dim',default='2d',choices=['1d','2d'],help='Fetched data are returned as a 2D array collection of vertical profiles (2d), 1D array available (1d)')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    start_dt = datetime.strptime(args.start_date, '%Y-%m')
    end_dt = datetime.strptime(args.end_date, '%Y-%m')
    # argopy's end bound is exclusive, so query through the first of the next month
    end_query = datetime(end_dt.year + end_dt.month // 12, end_dt.month % 12 + 1, 1)
    LOG.info(f'Starting: {start_dt.date()} through end of {end_dt:%Y-%m}')
    bbox = tuple(args.bbox)
    LOG.info(f'BBox: lon {bbox[0]}-{bbox[1]}, lat {bbox[2]}-{bbox[3]}')
    dpth = tuple(args.depth_range)
    LOG.info(f'Depth range: {dpth[0]}-{dpth[1]} [dbar]')
    dim_type = args.array_dim
    LOG.info(f'Data are returned as: {dim_type} array')

    """
    Run DataFetcher, by default, only grabs Argo with physical data (i.e., T/S/P)
    Uses research ready data with good quality flags only
    """

    region = [bbox[0],bbox[1],bbox[2],bbox[3],dpth[0],dpth[1],
              start_dt.strftime('%Y-%m-%d'),end_query.strftime('%Y-%m-%d')]

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            ds = argopy.DataFetcher(ds='phy',mode='research').region(region).to_xarray()
            break
        except DataNotFound:
            LOG.warning('No data matched the request; nothing written')
            return
        except Exception as exc:
            if attempt == MAX_ATTEMPTS:
                LOG.error(f'Failed after {MAX_ATTEMPTS} attempts: {exc}')
                raise
            wait = 10 * attempt
            LOG.warning(f'Attempt {attempt}/{MAX_ATTEMPTS} failed ({exc}); retrying in {wait}s')
            time.sleep(wait)

    if dim_type == '2d':
        ds = ds.argo.point2profile()
 
    fn = f'{format_coord(bbox[0],False)}{format_coord(bbox[1],False)}{format_coord(bbox[2],True)}{format_coord(bbox[3],True)}_{dim_type}_{start_dt:%Y%m}{end_dt:%Y%m}.nc'
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
 
    ds.to_netcdf(output_path / fn)
 
    LOG.info('Done')

if __name__ == '__main__':
    main()