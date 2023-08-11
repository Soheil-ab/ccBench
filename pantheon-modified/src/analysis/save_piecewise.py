#!/usr/bin/env python

from os import path
import sys
import json
from multiprocessing.pool import ThreadPool

import arg_parser
import parse_piecewise
from helpers import utils


class Save(object):
    def __init__(self, args):
        self.data_dir = path.abspath(args.data_dir)
        self.include_acklink = args.include_acklink
        self.no_graphs = args.no_graphs
        self.win_start_time_s = args.win_start
        self.win_end_time_s = args.win_end

        metadata_path = path.join(self.data_dir, 'pantheon_metadata.json')
        meta = utils.load_test_metadata(metadata_path)
        self.cc_schemes = utils.verify_schemes_with_meta(args.schemes, meta)

        self.run_times = meta['run_times']
        self.flows = meta['flows']
        self.runtime = meta['runtime']

    def parse_tunnel_log(self, cc, run_id):
        log_prefix = cc
        if self.flows == 0:
            log_prefix += '_mm'

        error = False
        ret = None

        link_directions = ['datalink']
        if self.include_acklink:
            link_directions.append('acklink')

        for link_t in link_directions:
            log_name = log_prefix + '_%s_run%s.log' % (link_t, run_id)
            log_path = path.join(self.data_dir, log_name)

            if not path.isfile(log_path):
                sys.stderr.write('Warning: %s does not exist\n' % log_path)
                error = True
                continue

            tput_graph_path = None
            delay_graph_path = None

            sys.stderr.write('$ parse_piecewise.py %s\n' % log_path)
            try:
                piecewise_results = parse_piecewise.ParsePiecewise(
                    tunnel_log=log_path,
                    win_start_time_s=self.win_start_time_s,win_end_time_s=self.win_end_time_s).run()
                #print(str(piecewise_results)+"\n")

            except Exception as exception:
                sys.stderr.write('Error: %s\n' % exception)
                sys.stderr.write('Warning: "parse_piecewise.py %s" failed but '
                                 'continued to run.\n' % log_path)
                error = True

            if error:
                continue

            if link_t == 'datalink':
                ret = piecewise_results
                duration = piecewise_results['duration'] / 1000.0

        if error:
            return None

        return ret

    def eval_performance(self):
        perf_data = {}

        for cc in self.cc_schemes:
            perf_data[cc] = {}

        cc_id = 0
        run_id = 1
        #pool = ThreadPool(processes=multiprocessing.cpu_count())
        pool = ThreadPool(processes=1)

        while cc_id < len(self.cc_schemes):
            cc = self.cc_schemes[cc_id]
            perf_data[cc][run_id] = pool.apply_async(
                self.parse_tunnel_log, args=(cc, run_id))

            run_id += 1
            if run_id > self.run_times:
                run_id = 1
                cc_id += 1

        for cc in self.cc_schemes:
            for run_id in xrange(1, 1 + self.run_times):
                try:
                    perf_data[cc][run_id] = perf_data[cc][run_id].get()
                except:
                    continue
                if perf_data[cc][run_id] is None:
                    continue

        return perf_data

    def run(self):
        perf_data = self.eval_performance()

        data_for_plot = {}
        data_for_plot_90 = {}
        data_for_plot_avg = {}
        data_for_plot_mean = {}
        data_for_json = {}

        for cc in perf_data:
            data_for_json[cc] = {}

            for run_id in perf_data[cc]:
                if perf_data[cc][run_id] is None:
                    continue

                flow_data = perf_data[cc][run_id]['flow_data']
                if flow_data is not None:
                    data_for_json[cc][run_id] = flow_data

        perf_path = path.join(self.data_dir, 'piecewise_perf_'+str(int(self.win_start_time_s))+'_'+str(int(self.win_end_time_s))+'.json')
        with open(perf_path, 'w') as fh:
            json.dump(data_for_json, fh)

def main():
    args = arg_parser.parse_save_piecewise()
    Save(args).run()


if __name__ == '__main__':
    main()
