# CS549 Performance Analysis Of Computer Networks - Assignment 3
### Objective: Linux OS Virtual Network Containers Performance Analysis
### Tasks:
- Create two network namespaces, say `NetNsA` and `NetNsB`. In each of these, create one network interface. Experiment with the following:
  - Run ping between `NetNsA` and `NetNsB`.
  - Add a queue discipline with fixed delay of say 50 ms, and run ping
  - Add a variable delay of 50ms and run ping\
Compare the three.
- In this exercise, you will investigate the performance of a mix of `elephant` and `mouse` flows between 2 hosts. The 2 hosts may be either 2 network namespaces on a single laptop/PC (created above), or 2 PCs/laptops connected by Ethernet in a lab. Use `scp` or `ftp` to generate flows.
  - Write a script `elephant` that transfers a very large file between the two hosts using **FTP**. If necessary, the script repeats the transfer back-to-back so that the total duration, T<sub>expt</sub> is 10s of seconds. Write a script `mouse` that transfers a very small file between the two hosts using **SCP**. The script repeats the transfer with a random inter-file gap drawn from an exponential distribution so that the total duration is T<sub>expt</sub>. Each script records the start and end times and the file size of each transfer.
  - Write a control script that runs the `elephant` script and N<sub>m</sub> `mouse` scripts in parallel.
  - Repeat for several values of N<sub>m</sub>. Plot `elephant` throughput X<sub>e</sub> vs. N<sub>m</sub> for different `mouse` file sizes.

