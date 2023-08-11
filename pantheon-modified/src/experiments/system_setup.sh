#sudo sysctl -q net.ipv4.tcp_wmem="4096 32768 4194304" #Doubling the default value from 16384 to 32768
# allow testing with buffers up to 128MB
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
# increase Linux autotuning TCP buffer limit to 64MB
sudo sysctl -w net.ipv4.tcp_rmem="4096 87380 67108864"
sudo sysctl -w net.ipv4.tcp_wmem="4096 65536 67108864"
# increase the length of the processor input queue
sudo sysctl -w  net.core.netdev_max_backlog=250000

sudo sysctl -w -q net.ipv4.tcp_low_latency=1
sudo sysctl -w -q net.ipv4.tcp_autocorking=0
sudo sysctl -w -q net.ipv4.tcp_no_metrics_save=1
sudo sysctl -w -q net.ipv4.ip_forward=1


#DEBUGGED! :D
#What happaned?! mahimahi couldn't make enough interfaces ==>some servers couldn't initiate!
#Solution increase max of inotify:
sudo sysctl -w -q fs.inotify.max_user_watches=524288
sudo sysctl -w -q fs.inotify.max_user_instances=524288


# Enabling CCs
sudo sysctl -w net.ipv4.tcp_congestion_control=vegas
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr2
sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo sysctl -w net.ipv4.tcp_congestion_control=cdg
sudo sysctl -w net.ipv4.tcp_congestion_control=hybla
sudo sysctl -w net.ipv4.tcp_congestion_control=highspeed
sudo sysctl -w net.ipv4.tcp_congestion_control=illinois
sudo sysctl -w net.ipv4.tcp_congestion_control=westwood
sudo sysctl -w net.ipv4.tcp_congestion_control=yeah
sudo sysctl -w net.ipv4.tcp_congestion_control=htcp
sudo sysctl -w net.ipv4.tcp_congestion_control=bic
sudo sysctl -w net.ipv4.tcp_congestion_control=veno
sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
