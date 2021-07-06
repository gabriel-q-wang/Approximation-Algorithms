# CSE-6140-Project

https://github.gatech.edu/gwang340/CSE-6140-Project
Group Number = 40

[1] Li, Ryan Jun-Man     (Email: rli342@gatech.edu)\
[2] Morioka, Hatsune     (Email: hmorioka3@gatech.edu)\
[3] Shin, Bomm     (Email: bshin8@gatech.edu)\
[4] Wang, Gabriel Qi     (Email: gwang340@gatech.edu)\
\
Minimum Vertex Cover Problem

To run the executable, run the following command first to install all dependancies
```
pip install -r requirements.txt 
```

Note: Please insert the data directory with all the graphs in the code/ directory on the same level as main.py. When running any commands, also be in the code/ directory

If you would like to run all the algorithms for 10 minutes each for all the graphs in the DATA directory run the following bash script

Note: Assumes that the data directory with all the graphs is called DATA/ and on the same level as main.py
```
bash run_all.sh
```

Otherwise you will need to run all the algorithms one by one and input the arguments you want using this command
```
python main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff in seconds> --seed <random seed>
```

Or the shorthand
```
python main.py -i <filename> -a [BnB|Approx|LS1|LS2] -t <cutoff in seconds> -s <random seed>
```

If a seed is not provided, it will be assigned a seed. All other arguments are required, otherwise the code will error.

