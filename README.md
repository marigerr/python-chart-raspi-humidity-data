Run Tracker.py as cron task
Setup with crontab -e
View existing tasks with crontab -l

Example below runs every 4 hours everyday
More info at https://www.raspberrypi.org/documentation/linux/usage/cron.md

0 0 * * *  python ~/Absolute/Path/To/tracker.py
0 4 * * *  python ~/Absolute/Path/To/tracker.py
0 8 * * *  python ~/Absolute/Path/To/tracker.py
0 12 * * *  python ~/Absolute/Path/To/tracker.py
0 16 * * *  python ~/Absolute/Path/To/tracker.py
0 20 * * *  python ~/Absolute/Path/To/tracker.py
