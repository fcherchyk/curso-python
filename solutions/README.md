# Reference solutions

Look at each one **after** your tests pass.

To run a day's tests against the solution without touching your code:

```bash
cp week1/day1_idiomatic/exercises.py /tmp/mine.py                       # backup
cp solutions/week1/day1_idiomatic.py week1/day1_idiomatic/exercises.py
uv run pytest week1/day1_idiomatic
cp /tmp/mine.py week1/day1_idiomatic/exercises.py                       # restore
```
