# CS549 Performance Analysis Of Computer Networks - Assignment 2
### Objective: The Download Dilemma: Investigating Factors Affecting Network Performance with WGET
### Tasks
- **Task-1:**  
  - Write a C/Java/Perl/Python program cpuhog that executes a while loop N times. Pass the number of iterations as a command-line argument. Measure the execution time in 3 ways:  
    - use the stopwatch function on your cellphone or wristwatch;  
    - use the time command;  
    - use the time() + getrusage() functions before/after the while loop.  
  - Vary the number of executions of the while loop such that the execution times range from a few milliseconds to one minute. Compare the three methods of time measurement and explain any differences
- **Task-2:**
  - Design experiments to use wget to measure network throughput. Use a fractional factorial design. Consider the following factors: file size, download speed limit (a wget option), number of concurrent file downloads running (write a script that spawns the desired number of concurrent downloads), time of day. Files to be downloaded are available here:
  ```
    1B https://cloud.iitmandi.ac.in/f/36c1c10b5caf46948ee9/?dl=1
    1kB https://cloud.iitmandi.ac.in/f/fef3ed77ad16482582f9/?dl=1
    10kB https://cloud.iitmandi.ac.in/f/f760934703f647c49dbb/?dl=1
    100kB https://cloud.iitmandi.ac.in/f/5d31e8769b954109be61/?dl=1
    500kB https://cloud.iitmandi.ac.in/f/0e1dfdb780e845129513/?dl=1
    1MB https://cloud.iitmandi.ac.in/f/07109a50545d4930a714/?dl=1
    10MB https://cloud.iitmandi.ac.in/f/2984f340696b4ab8b301/?dl=1
    100MB https://cloud.iitmandi.ac.in/f/c200476d3ce247e08c87/?dl=1
    500MB https://cloud.iitmandi.ac.in/f/d276f3cbe766409db927/?dl=1
  ```
  - Conduct the experiments and tabulate the data. Use the ranking method and the range method to analyse the impact of the factors. Identify the two factors that have the greatest impact. Now, analyse the effects of these 2 factors using
the allocation of variance technique. If needed, run a few more experiments with different levels of these 2 factors.

