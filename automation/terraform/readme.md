Note:
     
The basic infrastructure code is done. Now we have deployed lambda functions in 5 different AWS regions. Soon I’ll add a 5 x 5 matrix to show the network latency from these 5 AWS regions to other 5 regional/local ISP websites. It will be interesting.
     
However, the AWS lambda function is very limited. It can’t utilize ICMP Ping so we have to measure HTTP latency instead. Due to lack of time, I can only use HTTP HEAD method as a measurement. This would further affect the accuracy because the remote servers need to spend more time processing the header information. I hope the latency result can be at least dramatic enough to show the difference across the regions. 
