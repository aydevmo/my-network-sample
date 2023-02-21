Note:
     
The basic infrastructure code is done. Now we have deployed lambda functions in 5 different AWS regions. Soon I’ll add a 5 x 5 matrix to show the network latency from these 5 AWS regions to other 5 regional/local ISP websites. It will be interesting.
     
However, the AWS lambda function is very limited. It can’t utilize ICMP Ping so we have to measure HTTP latency instead. Due to lack of time, I can only use HTTP HEAD method as a measurement. This would further affect the accuracy because the remote servers need to spend more time processing the header information. I hope the latency result can be at least dramatic enough to show the difference across the regions. 

( * 2/18/2023: I soon realized maybe we can use Python TCP/IP socket functions to measure TCP latency and I see people doing it, but I don’t have much time on hands at this point so we’ll just follow our old plan.)    
    
( * 2/20/2023: Some latency tests from certain regions really swing in a wide range. This makes me wonder if they have HTTP cache implemented in the infrastructure. We’d still use the results, and hopefully we could conduct a more accurate test in the future using Ansible and EC2 instances.)    
    
    
