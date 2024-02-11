import datetime
import sys
from pathlib import Path

from calenderCalc.iCal import PregnancyICal

def main():
	cal = PregnancyICal()
	lastMonthlyPeriod = datetime.datetime(year=2023, month=12, day=12)
	cal.lastMonthlyPeriod = lastMonthlyPeriod
	cal.write(directory = Path.home() / "Downloads")
	

if __name__ == '__main__':
	sys.exit(main())  # pragma: no cover
