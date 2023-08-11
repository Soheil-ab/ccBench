#!/usr/bin/env python

from os import path
import sys
import itertools
import numpy as np
import arg_parser

class ParsePiecewise(object):
    def __init__(self, tunnel_log,win_start_time_s=0,win_end_time_s=100):
        self.tunnel_log = tunnel_log
        self.win_start_time_s = win_start_time_s
        self.win_end_time_s = win_end_time_s

    def parse_tunnel_log(self):
        tunlog = open(self.tunnel_log)

        self.flows = {}
        first_ts = None
        capacities = 0

        arrivals = {}
        departures = {}
        self.delays_t = {}
        self.delays = {}

        first_capacity = None
        last_capacity = None
        first_arrival = {}
        last_arrival = {}
        first_departure = {}
        last_departure = {}

        total_first_departure = None
        total_last_departure = None
        total_arrivals = 0
        total_departures = 0

        while True:
            line = tunlog.readline()
            if not line:
                break

            if line.startswith('#'):
                continue

            items = line.split()
            ts = float(items[0])
            event_type = items[1]
            num_bits = int(items[2]) * 8

            if ts<=self.win_start_time_s*1000:
                continue
            if ts>=self.win_end_time_s*1000:
                break

            if first_ts is None:
                first_ts = ts

            if event_type == '#':
                capacities = capacities + num_bits

                if first_capacity is None:
                    first_capacity = ts

                if last_capacity is None or ts > last_capacity:
                    last_capacity = ts

            elif event_type == '+':
                if len(items) == 4:
                    flow_id = int(items[-1])
                else:
                    flow_id = 0

                self.flows[flow_id] = True

                if flow_id not in arrivals:
                    arrivals[flow_id] = 0
                    first_arrival[flow_id] = ts

                if flow_id not in last_arrival:
                    last_arrival[flow_id] = ts
                else:
                    if ts > last_arrival[flow_id]:
                        last_arrival[flow_id] = ts

                arrivals[flow_id] = arrivals[flow_id] + num_bits
                total_arrivals += num_bits

            elif event_type == '-':
                if len(items) == 5:
                    flow_id = int(items[-1])
                else:
                    flow_id = 0

                self.flows[flow_id] = True

                if flow_id not in departures:
                    departures[flow_id] = 0
                    first_departure[flow_id] = ts

                if flow_id not in last_departure:
                    last_departure[flow_id] = ts
                else:
                    if ts > last_departure[flow_id]:
                        last_departure[flow_id] = ts

                departures[flow_id] = departures[flow_id] + num_bits
                total_departures += num_bits

                # update total variables
                if total_first_departure is None:
                    total_first_departure = ts
                if (total_last_departure is None or
                        ts > total_last_departure):
                    total_last_departure = ts

                # store delays in a list for each flow and sort later
                delay = float(items[3])
                if flow_id not in self.delays:
                    self.delays[flow_id] = []
                    self.delays_t[flow_id] = []
                self.delays[flow_id].append(delay)
                self.delays_t[flow_id].append((ts - first_ts) / 1000.0)

        tunlog.close()


        self.avg_capacity = None
        self.link_capacity = []
        self.link_capacity_t = []
        if capacities:
            # calculate average capacity
            if last_capacity == first_capacity:
                self.avg_capacity = 0
            else:
                delta = 1000.0 * (last_capacity - first_capacity)
                self.avg_capacity = capacities / delta

        # calculate ingress and egress throughput for each flow
        self.avg_ingress = {}
        self.avg_egress = {}
        self.percentile_delay_90th = {}
        self.mean_delay = {}
        self.avg_delay = {}
        self.percentile_delay = {}
        self.loss_rate = {}
        self.avg_gput = {}
        self.jitter = {}

        total_delays = []

        for flow_id in self.flows:
            self.avg_ingress[flow_id] = 0
            self.avg_egress[flow_id] = 0

            if flow_id in arrivals:
                # calculate average ingress and egress throughput
                first_arrival_ts = first_arrival[flow_id]
                last_arrival_ts = last_arrival[flow_id]

                if last_arrival_ts == first_arrival_ts:
                    self.avg_ingress[flow_id] = 0
                else:
                    delta = 1000.0 * (last_arrival_ts - first_arrival_ts)
                    #flow_arrivals = sum(arrivals[flow_id].values())
                    flow_arrivals = arrivals[flow_id]
                    self.avg_ingress[flow_id] = flow_arrivals / delta

            if flow_id in departures:
                first_departure_ts = first_departure[flow_id]
                last_departure_ts = last_departure[flow_id]

                if last_departure_ts == first_departure_ts:
                    self.avg_egress[flow_id] = 0
                else:
                    delta = 1000.0 * (last_departure_ts - first_departure_ts)
                    #flow_departures = sum(departures[flow_id].values())
                    flow_departures = departures[flow_id]
                    self.avg_egress[flow_id] = flow_departures / delta

            # calculate 95th percentile per-packet one-way delay
            self.percentile_delay_90th[flow_id] = None
            self.avg_delay[flow_id] = None
            self.mean_delay[flow_id] = None
            self.percentile_delay[flow_id] = None
            self.jitter[flow_id] = None
            if flow_id in self.delays:
                self.percentile_delay_90th[flow_id] = np.percentile(
                    self.delays[flow_id], 90, interpolation='higher')
                self.percentile_delay[flow_id] = np.percentile(
                    self.delays[flow_id], 95, interpolation='higher')
                self.avg_delay[flow_id] = np.average(self.delays[flow_id])
                self.mean_delay[flow_id] = np.mean(self.delays[flow_id])

                tmp = np.array(self.delays[flow_id])
                tmp -= self.avg_delay[flow_id]
                delta_times_from_avg = np.absolute(tmp)
                self.jitter[flow_id] = np.average(delta_times_from_avg)

                total_delays += self.delays[flow_id]

            # calculate loss rate for each flow
            if flow_id in arrivals and flow_id in departures:
                flow_arrivals = arrivals[flow_id]
                flow_departures = departures[flow_id]

                self.loss_rate[flow_id] = None
                if flow_arrivals > 0:
                    self.loss_rate[flow_id] = (
                        1 - 1.0 * flow_departures / flow_arrivals)
                    self.avg_gput[flow_id] = self.avg_egress[flow_id]*(1.0-self.loss_rate[flow_id])

        self.total_loss_rate = None
        if total_arrivals > 0:
            self.total_loss_rate = 1 - 1.0 * total_departures / total_arrivals

        # calculate total average throughput and 95th percentile delay
        self.total_avg_egress = None
        self.total_avg_gput = None
        if total_last_departure == total_first_departure:
            self.total_duration = 0
            self.total_avg_egress = 0
            self.total_avg_gput = 0
        else:
            self.total_duration = total_last_departure - total_first_departure
            self.total_avg_egress = total_departures / (
                1000.0 * self.total_duration)
            self.total_avg_gput = self.total_avg_egress*(1.0-self.total_loss_rate)

        self.total_percentile_delay = None
        if total_delays:
            self.total_percentile_delay = np.percentile(
                #total_delays, 95, interpolation='nearest')
                total_delays, 95, interpolation='higher')

        self.total_avg_delay = None
        if total_delays:
            self.total_avg_delay = np.average(total_delays)

        self.total_mean_delay = None
        if total_delays:
            self.total_mean_delay = np.mean(total_delays)

        self.total_90th_delay = None
        if total_delays:
            self.total_90th_delay = np.percentile(
                #total_delays, 90, interpolation='nearest')
                total_delays, 90, interpolation='higher')

            self.total_jitter = None
        if total_delays:
            tmp = np.array(total_delays)
            tmp -= self.total_avg_delay
            delta_times_from_avg = np.absolute(tmp)
            self.total_jitter = np.average(delta_times_from_avg)

    def flip(self, items, ncol):
        return list(itertools.chain(*[items[i::ncol] for i in range(ncol)]))

    def run(self):
        self.parse_tunnel_log()

        tunnel_results = {}
        tunnel_results['duration'] = self.total_duration
        flow_data = {}

        for flow_id in self.flows:
            if flow_id != 0:
                flow_data[flow_id] = {}
                flow_data[flow_id]['jitter'] = self.jitter[flow_id]
                flow_data[flow_id]['tput'] = self.avg_egress[flow_id]
                flow_data[flow_id]['gput'] = self.avg_gput[flow_id]
                flow_data[flow_id]['delay_90'] = self.percentile_delay_90th[flow_id]
                flow_data[flow_id]['delay_avg'] = self.avg_delay[flow_id]
                flow_data[flow_id]['delay_mean'] = self.mean_delay[flow_id]
                flow_data[flow_id]['delay'] = self.percentile_delay[flow_id]
                flow_data[flow_id]['loss'] = self.loss_rate[flow_id]

        tunnel_results['flow_data'] = flow_data

        return tunnel_results

def main():
    args = arg_parser.parse_tunnel_piecewise()

    parsed_piecewise = ParsePiecewise(tunnel_log=args.tunnel_log,
            win_start_time_s=args.win_start,win_end_time_s=args.win_end)

    results = parsed_piecewise.run()

    sys.stderr.write(str(results)+"\n")

if __name__ == '__main__':
    main()
